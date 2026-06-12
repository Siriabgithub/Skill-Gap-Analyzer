"""
NLP-based skill extractor.
Uses keyword matching, alias resolution, and TF-IDF similarity for extraction.
"""

from __future__ import annotations

import re
import math
import logging
from collections import Counter

logger = logging.getLogger(__name__)

try:
    from data.skills_db import SKILLS_DATABASE, get_skill_by_alias, get_all_skill_names
except ImportError:
    from skills_db import SKILLS_DATABASE, get_skill_by_alias, get_all_skill_names


# ─── Extraction ───────────────────────────────────────────────────────────────

def extract_skills(text: str) -> dict[str, dict]:
    """
    Extract skills from free text.

    Returns:
        {canonical_skill_name: {"confidence": float, "evidence": [str], "category": str}}
    """
    text_lower = text.lower()
    found: dict[str, dict] = {}

    for skill_name, skill_data in SKILLS_DATABASE.items():
        evidence = []
        confidence = 0.0
        terms_to_check = [skill_name] + skill_data.get("aliases", [])

        for term in terms_to_check:
            term_lower = term.lower()
            # Whole-word / whole-phrase match
            pattern = r"(?<![a-z\-])(" + re.escape(term_lower) + r")(?![a-z\-])"
            matches = re.findall(pattern, text_lower)
            if matches:
                # Extract surrounding context for evidence
                for m in re.finditer(pattern, text_lower):
                    start = max(0, m.start() - 40)
                    end = min(len(text_lower), m.end() + 40)
                    snippet = text[start:end].strip()
                    snippet = re.sub(r"\s+", " ", snippet)
                    evidence.append(f"…{snippet}…")

                count = len(matches)
                # More occurrences = higher confidence (diminishing returns)
                term_confidence = min(1.0, 0.6 + 0.1 * math.log1p(count))

                # Exact canonical name match gets a bonus
                if term_lower == skill_name.lower():
                    term_confidence = min(1.0, term_confidence + 0.15)

                if term_confidence > confidence:
                    confidence = term_confidence

        if evidence:
            found[skill_name] = {
                "confidence": round(confidence, 3),
                "evidence": list(dict.fromkeys(evidence))[:3],
                "category": skill_data["category"],
                "demand_score": skill_data.get("demand_score", 0),
                "growth_rate": skill_data.get("growth_rate", 0),
            }

    return dict(sorted(found.items(), key=lambda x: x[1]["confidence"], reverse=True))


def extract_skills_from_jd(jd_text: str) -> dict[str, dict]:
    """
    Extract required and preferred skills from a job description.
    Adds 'requirement_level' key: 'required' | 'preferred' | 'nice_to_have'.
    """
    base_skills = extract_skills(jd_text)

    required_patterns = [
        r"required|must\s*have|essential|mandatory|minimum|necessari|prerequisite",
        r"you\s*(will|must|should|are\s*expected\s*to)",
        r"we\s*(require|need|expect)",
        r"qualifications",
    ]
    preferred_patterns = [
        r"preferred|nice\s*to\s*have|bonus|plus|desirable|optional|ideal|advantage",
        r"strong\s*(plus|advantage)",
        r"experience\s*with\s*is\s*a\s*plus",
    ]

    jd_lower = jd_text.lower()

    # Split JD into lines for context-aware classification
    lines = jd_lower.split("\n")
    required_lines = set()
    preferred_lines = set()

    for i, line in enumerate(lines):
        if any(re.search(p, line) for p in required_patterns):
            for j in range(i, min(i + 5, len(lines))):
                required_lines.add(j)
        if any(re.search(p, line) for p in preferred_patterns):
            for j in range(i, min(i + 5, len(lines))):
                preferred_lines.add(j)

    enriched: dict[str, dict] = {}
    for skill, data in base_skills.items():
        level = _classify_requirement_level(
            skill,
            SKILLS_DATABASE[skill].get("aliases", []),
            jd_lower,
            lines,
            required_lines,
            preferred_lines,
        )
        enriched[skill] = {**data, "requirement_level": level}

    return enriched


def _classify_requirement_level(
    skill: str,
    aliases: list[str],
    jd_lower: str,
    lines: list[str],
    required_lines: set[int],
    preferred_lines: set[int],
) -> str:
    terms = [skill] + aliases
    for i, line in enumerate(lines):
        if any(t.lower() in line for t in terms):
            if i in preferred_lines and i not in required_lines:
                return "preferred"
            if i in required_lines:
                return "required"
    # default: classify by demand score
    ds = SKILLS_DATABASE.get(skill, {}).get("demand_score", 50)
    return "required" if ds >= 80 else "preferred"


def compute_tfidf_similarity(text1: str, text2: str) -> float:
    """
    Compute a simple TF-IDF cosine similarity between two texts.
    Used for semantic skill overlap when keyword matching misses synonyms.
    """
    def tokenize(t: str) -> list[str]:
        t = re.sub(r"[^a-z0-9\s\+#\.]", " ", t.lower())
        tokens = t.split()
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "is", "are", "was", "were", "be", "been",
            "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "shall", "can", "not",
            "our", "their", "your", "we", "you", "they", "he", "she", "it",
            "this", "that", "these", "those", "such", "as", "by", "from",
            "into", "through", "during", "experience", "strong", "good",
            "excellent", "knowledge", "understanding", "familiarity",
        }
        return [tok for tok in tokens if tok not in stopwords and len(tok) > 1]

    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)

    if not tokens1 or not tokens2:
        return 0.0

    vocab = set(tokens1) | set(tokens2)
    tf1 = Counter(tokens1)
    tf2 = Counter(tokens2)

    def tfidf_vec(tf: Counter) -> dict[str, float]:
        total = sum(tf.values())
        return {w: tf[w] / total for w in vocab}

    v1 = tfidf_vec(tf1)
    v2 = tfidf_vec(tf2)

    dot = sum(v1.get(w, 0) * v2.get(w, 0) for w in vocab)
    mag1 = math.sqrt(sum(x ** 2 for x in v1.values()))
    mag2 = math.sqrt(sum(x ** 2 for x in v2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return round(dot / (mag1 * mag2), 4)


def get_skill_categories(skills: list[str]) -> dict[str, list[str]]:
    """Group a list of skill names by their category."""
    grouped: dict[str, list[str]] = {}
    for skill in skills:
        cat = SKILLS_DATABASE.get(skill, {}).get("category", "Other")
        grouped.setdefault(cat, []).append(skill)
    return grouped
