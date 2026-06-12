"""
Skill gap analyzer: compares resume skills against job description skills,
produces match scores, missing skills, strength areas, and ATS scoring.
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

try:
    from data.skills_db import SKILLS_DATABASE
    from utils.skill_extractor import compute_tfidf_similarity
except ImportError:
    from skills_db import SKILLS_DATABASE
    from skill_extractor import compute_tfidf_similarity


@dataclass
class GapAnalysisResult:
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    extra_skills: list[str] = field(default_factory=list)
    required_missing: list[str] = field(default_factory=list)
    preferred_missing: list[str] = field(default_factory=list)
    match_score: float = 0.0
    ats_score: float = 0.0
    semantic_score: float = 0.0
    combined_score: float = 0.0
    strength_areas: list[str] = field(default_factory=list)
    weak_areas: list[str] = field(default_factory=list)
    ats_breakdown: dict = field(default_factory=dict)
    category_breakdown: dict = field(default_factory=dict)


def analyze_gap(
    resume_skills: dict[str, dict],
    jd_skills: dict[str, dict],
    resume_text: str,
    jd_text: str,
    resume_analysis: dict,
) -> GapAnalysisResult:
    """
    Full gap analysis between a parsed resume and a job description.

    Args:
        resume_skills: {skill_name: {confidence, category, ...}}
        jd_skills: {skill_name: {confidence, requirement_level, category, ...}}
        resume_text: raw resume text
        jd_text: raw JD text
        resume_analysis: structural analysis from resume_parser.analyze_resume_structure

    Returns:
        GapAnalysisResult
    """
    result = GapAnalysisResult()

    resume_set = set(resume_skills.keys())
    jd_set = set(jd_skills.keys())

    result.matched_skills = sorted(resume_set & jd_set)
    result.missing_skills = sorted(jd_set - resume_set)
    result.extra_skills = sorted(resume_set - jd_set)

    required_jd = {s for s, d in jd_skills.items() if d.get("requirement_level") == "required"}
    preferred_jd = {s for s, d in jd_skills.items() if d.get("requirement_level") == "preferred"}

    result.required_missing = sorted(required_jd - resume_set)
    result.preferred_missing = sorted(preferred_jd - resume_set)

    # ─── Match score (keyword overlap) ───────────────────────────────────────
    if jd_set:
        # Weight required skills more heavily
        total_weight = len(required_jd) * 2 + len(preferred_jd) * 1
        matched_weight = len(resume_set & required_jd) * 2 + len(resume_set & preferred_jd) * 1

        if total_weight > 0:
            result.match_score = round((matched_weight / total_weight) * 100, 1)
        else:
            result.match_score = round((len(result.matched_skills) / max(len(jd_set), 1)) * 100, 1)
    else:
        result.match_score = 0.0

    # ─── Semantic score (TF-IDF cosine similarity) ────────────────────────────
    result.semantic_score = round(
        compute_tfidf_similarity(resume_text, jd_text) * 100, 1
    )

    # ─── ATS score ────────────────────────────────────────────────────────────
    ats_components = _compute_ats_score(resume_analysis, result.match_score, jd_text, resume_text)
    result.ats_score = ats_components["total"]
    result.ats_breakdown = ats_components

    # ─── Combined score (weighted average) ───────────────────────────────────
    result.combined_score = round(
        result.match_score * 0.50
        + result.semantic_score * 0.25
        + result.ats_score * 0.25,
        1,
    )

    # ─── Strength / weak areas (by category) ─────────────────────────────────
    category_matched: dict[str, int] = {}
    category_total: dict[str, int] = {}

    for skill in result.matched_skills:
        cat = SKILLS_DATABASE.get(skill, {}).get("category", "Other")
        category_matched[cat] = category_matched.get(cat, 0) + 1
        category_total[cat] = category_total.get(cat, 0) + 1

    for skill in result.missing_skills:
        cat = SKILLS_DATABASE.get(skill, {}).get("category", "Other")
        category_total[cat] = category_total.get(cat, 0) + 1

    result.category_breakdown = {
        cat: {
            "matched": category_matched.get(cat, 0),
            "total": category_total.get(cat, 0),
            "pct": round(category_matched.get(cat, 0) / max(category_total.get(cat, 1), 1) * 100, 1),
        }
        for cat in category_total
    }

    for cat, stats in result.category_breakdown.items():
        if stats["pct"] >= 70:
            result.strength_areas.append(cat)
        elif stats["pct"] <= 30 and stats["total"] >= 2:
            result.weak_areas.append(cat)

    return result


def _compute_ats_score(
    resume_analysis: dict,
    match_score: float,
    jd_text: str,
    resume_text: str,
) -> dict:
    """
    Compute ATS score from structural and keyword factors.
    """
    components: dict[str, float] = {}

    # Keyword match contribution (30 pts)
    components["keyword_match"] = round(match_score * 0.30, 1)

    # Section completeness (25 pts)
    sections_score = 0.0
    if resume_analysis.get("has_contact"):
        sections_score += 6
    if resume_analysis.get("has_summary"):
        sections_score += 5
    if resume_analysis.get("has_experience"):
        sections_score += 7
    if resume_analysis.get("has_skills"):
        sections_score += 4
    if resume_analysis.get("has_education"):
        sections_score += 3
    components["section_completeness"] = min(25.0, sections_score)

    # Quantified achievements (20 pts)
    n_quantified = len(resume_analysis.get("quantified_achievements", []))
    components["quantified_achievements"] = min(20.0, n_quantified * 4.0)

    # Word count (10 pts)
    wc = resume_analysis.get("word_count", 0)
    if 300 <= wc <= 800:
        components["word_count"] = 10.0
    elif 200 <= wc < 300 or 800 < wc <= 1000:
        components["word_count"] = 6.0
    else:
        components["word_count"] = 2.0

    # Contact info completeness (10 pts)
    contact = resume_analysis.get("contact_info", {})
    contact_score = 0
    if contact.get("email"):
        contact_score += 4
    if contact.get("phone"):
        contact_score += 3
    if contact.get("linkedin"):
        contact_score += 2
    if contact.get("github"):
        contact_score += 1
    components["contact_completeness"] = float(min(10, contact_score))

    # Certifications (5 pts)
    n_certs = len(resume_analysis.get("certifications_detected", []))
    components["certifications"] = min(5.0, n_certs * 2.5)

    total = round(sum(components.values()), 1)
    components["total"] = min(100.0, total)

    return components


def get_priority_skills(
    missing_skills: list[str],
    jd_skills: dict[str, dict],
    top_n: int = 8,
) -> list[dict]:
    """
    Rank missing skills by priority (demand score × requirement level weight).
    """
    scored = []
    for skill in missing_skills:
        db_entry = SKILLS_DATABASE.get(skill, {})
        jd_entry = jd_skills.get(skill, {})
        level = jd_entry.get("requirement_level", "preferred")
        level_weight = 2.0 if level == "required" else 1.0
        demand = db_entry.get("demand_score", 50)
        priority_score = demand * level_weight

        scored.append({
            "skill": skill,
            "category": db_entry.get("category", "Other"),
            "demand_score": demand,
            "growth_rate": db_entry.get("growth_rate", 0),
            "requirement_level": level,
            "priority_score": priority_score,
            "time_to_learn": db_entry.get("time_to_learn", "Unknown"),
            "avg_salary": db_entry.get("avg_salary", 0),
        })

    return sorted(scored, key=lambda x: x["priority_score"], reverse=True)[:top_n]


def generate_resume_improvements(resume_analysis: dict, gap_result: GapAnalysisResult) -> list[dict]:
    """Generate specific resume improvement suggestions."""
    suggestions = []

    if not resume_analysis.get("has_summary"):
        suggestions.append({
            "category": "Content",
            "priority": "High",
            "suggestion": "Add a professional summary (2-3 sentences highlighting your value proposition)",
            "impact": "ATS +5 pts, recruiter engagement +40%",
        })

    if not resume_analysis.get("quantified_achievements") or len(resume_analysis.get("quantified_achievements", [])) < 3:
        suggestions.append({
            "category": "Impact",
            "priority": "High",
            "suggestion": "Add quantified achievements (e.g., 'Improved performance by 35%', 'Managed team of 8')",
            "impact": "ATS +8 pts, interview rate +60%",
        })

    if not resume_analysis.get("contact_info", {}).get("linkedin"):
        suggestions.append({
            "category": "Contact",
            "priority": "Medium",
            "suggestion": "Add your LinkedIn profile URL",
            "impact": "ATS +2 pts, recruiter outreach +25%",
        })

    if not resume_analysis.get("contact_info", {}).get("github"):
        suggestions.append({
            "category": "Contact",
            "priority": "Medium",
            "suggestion": "Add your GitHub profile URL (especially important for technical roles)",
            "impact": "Credibility +30% for engineering roles",
        })

    if gap_result.required_missing:
        top_missing = gap_result.required_missing[:3]
        suggestions.append({
            "category": "Keywords",
            "priority": "High",
            "suggestion": f"Add these required skills if you have them: {', '.join(top_missing)}",
            "impact": "ATS keyword match +15-25 pts",
        })

    wc = resume_analysis.get("word_count", 0)
    if wc < 300:
        suggestions.append({
            "category": "Length",
            "priority": "Medium",
            "suggestion": "Expand your resume — currently too brief. Add more detail to experience bullets.",
            "impact": "ATS completeness +8 pts",
        })
    elif wc > 1000:
        suggestions.append({
            "category": "Length",
            "priority": "Low",
            "suggestion": "Consider condensing your resume. Aim for 400-800 words for most roles.",
            "impact": "Readability improvement",
        })

    if not resume_analysis.get("certifications_detected"):
        suggestions.append({
            "category": "Certifications",
            "priority": "Medium",
            "suggestion": "Add relevant certifications to strengthen credibility",
            "impact": "ATS +5 pts, recruiter confidence +20%",
        })

    return suggestions
