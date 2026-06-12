"""
AI-powered recommendation engine.
Generates learning roadmaps, project ideas, certification suggestions,
and personalized career advice based on the gap analysis.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

try:
    from data.skills_db import SKILLS_DATABASE, TOP_CERTIFICATIONS
    from utils.gap_analyzer import GapAnalysisResult, get_priority_skills
except ImportError:
    from skills_db import SKILLS_DATABASE, TOP_CERTIFICATIONS
    from gap_analyzer import GapAnalysisResult, get_priority_skills


@dataclass
class RoadmapPhase:
    name: str
    duration: str
    goal: str
    skills: list[dict] = field(default_factory=list)
    projects: list[dict] = field(default_factory=list)
    certifications: list[dict] = field(default_factory=list)
    milestones: list[str] = field(default_factory=list)


@dataclass
class LearningRoadmap:
    day_30: RoadmapPhase = field(default_factory=lambda: RoadmapPhase("", "", ""))
    day_60: RoadmapPhase = field(default_factory=lambda: RoadmapPhase("", "", ""))
    day_90: RoadmapPhase = field(default_factory=lambda: RoadmapPhase("", "", ""))
    total_skills: int = 0
    estimated_effort_hrs: int = 0


def generate_roadmap(
    missing_skills: list[str],
    jd_skills: dict[str, dict],
    matched_skills: list[str],
    job_title: str = "the target role",
) -> LearningRoadmap:
    """Generate a personalized 30/60/90 day learning roadmap."""
    priority_skills = get_priority_skills(missing_skills, jd_skills, top_n=12)

    # Partition into three groups by priority rank
    high = priority_skills[:4]
    mid = priority_skills[4:8]
    low = priority_skills[8:12]

    roadmap = LearningRoadmap()

    roadmap.day_30 = RoadmapPhase(
        name="Foundation Sprint",
        duration="Days 1–30",
        goal="Close the most critical skill gaps identified by the job description",
        skills=_build_skill_items(high),
        projects=_suggest_projects(high, phase=1),
        certifications=_suggest_certifications(high),
        milestones=[
            "Complete beginner resources for top 2 missing skills",
            "Build at least 1 hands-on mini-project",
            "Update resume with newly acquired skills",
            "Apply to 5 relevant positions to test messaging",
        ],
    )

    roadmap.day_60 = RoadmapPhase(
        name="Growth Phase",
        duration="Days 31–60",
        goal="Deepen knowledge and start building portfolio evidence",
        skills=_build_skill_items(mid),
        projects=_suggest_projects(mid, phase=2),
        certifications=_suggest_certifications(mid),
        milestones=[
            "Complete intermediate resources for 2-3 additional skills",
            "Publish at least 1 project to GitHub",
            "Contribute to an open-source project",
            "Engage with the community (LinkedIn posts, meetups)",
        ],
    )

    roadmap.day_90 = RoadmapPhase(
        name="Mastery & Launch",
        duration="Days 61–90",
        goal="Achieve job-ready proficiency and accelerate your job search",
        skills=_build_skill_items(low),
        projects=_suggest_projects(low, phase=3),
        certifications=_suggest_certifications(low),
        milestones=[
            "Complete at least 1 industry certification",
            "Build a capstone project combining multiple skills",
            "Get 3+ LinkedIn recommendations",
            "Target 10+ applications per week",
        ],
    )

    roadmap.total_skills = len(priority_skills)
    roadmap.estimated_effort_hrs = len(priority_skills) * 20  # rough avg hours per skill

    return roadmap


def _build_skill_items(priority_skills: list[dict]) -> list[dict]:
    items = []
    for ps in priority_skills:
        skill = ps["skill"]
        db_entry = SKILLS_DATABASE.get(skill, {})
        resources = db_entry.get("resources", [])
        items.append({
            "skill": skill,
            "category": ps["category"],
            "requirement_level": ps["requirement_level"],
            "demand_score": ps["demand_score"],
            "growth_rate": ps["growth_rate"],
            "time_to_learn": ps["time_to_learn"],
            "avg_salary": ps["avg_salary"],
            "resources": resources[:2],
            "description": db_entry.get("description", ""),
            "related": db_entry.get("related", [])[:4],
        })
    return items


def _suggest_projects(priority_skills: list[dict], phase: int) -> list[dict]:
    """Generate project ideas relevant to the skill set."""
    projects = []
    categories = list({ps["category"] for ps in priority_skills})
    skill_names = [ps["skill"] for ps in priority_skills]

    project_templates = {
        "Data Science & ML": [
            {
                "title": "End-to-End ML Pipeline",
                "description": "Build a predictive model with data cleaning, feature engineering, training, and evaluation",
                "skills_used": [s for s in skill_names if s in ["python", "scikit-learn", "pandas", "numpy"]],
                "difficulty": "Intermediate",
                "github_topics": ["machine-learning", "python", "scikit-learn"],
            },
            {
                "title": "NLP Sentiment Analyzer",
                "description": "Classify sentiment in customer reviews using NLP techniques",
                "skills_used": [s for s in skill_names if "nlp" in s or "python" in s],
                "difficulty": "Intermediate",
                "github_topics": ["nlp", "sentiment-analysis", "python"],
            },
        ],
        "Data Engineering": [
            {
                "title": "Data Pipeline with Airflow",
                "description": "Build an automated ETL pipeline that ingests, transforms, and loads data",
                "skills_used": [s for s in skill_names if s in ["airflow", "python", "sql", "postgresql"]],
                "difficulty": "Intermediate",
                "github_topics": ["data-engineering", "airflow", "etl"],
            },
        ],
        "DevOps": [
            {
                "title": "Containerized Microservices App",
                "description": "Deploy a multi-service application using Docker and Kubernetes",
                "skills_used": [s for s in skill_names if s in ["docker", "kubernetes", "ci/cd"]],
                "difficulty": "Advanced",
                "github_topics": ["docker", "kubernetes", "devops"],
            },
        ],
        "Cloud Platforms": [
            {
                "title": "Serverless Data Processing",
                "description": "Build a serverless pipeline on AWS/GCP using cloud-native services",
                "skills_used": [s for s in skill_names if s in ["aws", "gcp", "azure", "python"]],
                "difficulty": "Intermediate",
                "github_topics": ["aws", "serverless", "cloud"],
            },
        ],
        "Web Frameworks": [
            {
                "title": "REST API with Authentication",
                "description": "Build a production-ready REST API with JWT auth, rate limiting, and docs",
                "skills_used": [s for s in skill_names if s in ["fastapi", "django", "postgresql"]],
                "difficulty": "Intermediate",
                "github_topics": ["rest-api", "fastapi", "postgresql"],
            },
        ],
    }

    phase_difficulty = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    target_difficulty = phase_difficulty.get(phase, "Intermediate")

    for cat in categories:
        if cat in project_templates:
            for proj in project_templates[cat]:
                proj_copy = dict(proj)
                proj_copy["difficulty"] = target_difficulty if phase == 1 else proj["difficulty"]
                if proj_copy not in projects:
                    projects.append(proj_copy)
                if len(projects) >= 3:
                    break
        if len(projects) >= 3:
            break

    if not projects:
        projects.append({
            "title": "Portfolio Project",
            "description": f"Build a project demonstrating {', '.join(skill_names[:3]) if skill_names else 'your skills'}",
            "skills_used": skill_names[:4],
            "difficulty": target_difficulty,
            "github_topics": ["portfolio", "project"],
        })

    return projects


def _suggest_certifications(priority_skills: list[dict]) -> list[dict]:
    """Suggest certifications relevant to the skill cluster."""
    skill_names = {ps["skill"] for ps in priority_skills}
    categories = {ps["category"] for ps in priority_skills}

    relevant_certs = []
    for cert in TOP_CERTIFICATIONS:
        name_lower = cert["name"].lower()
        if (
            any(s in name_lower for s in skill_names)
            or ("aws" in skill_names and "aws" in name_lower)
            or ("gcp" in skill_names and "google" in name_lower)
            or ("azure" in skill_names and "azure" in name_lower)
            or ("kubernetes" in skill_names and "kubernetes" in name_lower)
            or ("terraform" in skill_names and "terraform" in name_lower)
            or ("tensorflow" in skill_names and "tensorflow" in name_lower)
            or ("Data Science" in categories and "data" in name_lower)
            or ("Data Engineering" in categories and "data" in name_lower)
            or ("DevOps" in categories and any(w in name_lower for w in ["devops", "kubernetes", "terraform"]))
            or ("Cloud Platforms" in categories and any(w in name_lower for w in ["aws", "azure", "google"]))
        ):
            relevant_certs.append(cert)

    return relevant_certs[:3] if relevant_certs else TOP_CERTIFICATIONS[:2]


def generate_learning_resources(skills: list[str]) -> dict[str, list[dict]]:
    """Return curated learning resources for a list of skills."""
    resources: dict[str, list[dict]] = {}
    for skill in skills:
        db_entry = SKILLS_DATABASE.get(skill, {})
        skill_resources = db_entry.get("resources", [])
        if skill_resources:
            resources[skill] = skill_resources
    return resources


def generate_skill_recommendations(
    matched_skills: list[str],
    missing_skills: list[str],
    jd_skills: dict[str, dict],
) -> list[dict]:
    """
    Generate AI-style recommendations with source transparency.
    Each recommendation includes confidence, source, and explanation.
    """
    recommendations = []
    priority_skills = get_priority_skills(missing_skills, jd_skills, top_n=10)

    for i, ps in enumerate(priority_skills, 1):
        skill = ps["skill"]
        db_entry = SKILLS_DATABASE.get(skill, {})
        confidence = _compute_recommendation_confidence(ps, jd_skills)

        recommendations.append({
            "rank": i,
            "skill": skill,
            "category": ps["category"],
            "requirement_level": ps["requirement_level"],
            "confidence": confidence,
            "demand_score": ps["demand_score"],
            "growth_rate": ps["growth_rate"],
            "time_to_learn": ps["time_to_learn"],
            "avg_salary_impact": ps["avg_salary"],
            "description": db_entry.get("description", ""),
            "resources": db_entry.get("resources", [])[:3],
            "related_skills": [s for s in db_entry.get("related", []) if s in matched_skills][:3],
            "source": _get_recommendation_source(ps),
            "explanation": _generate_explanation(ps, matched_skills),
        })

    return recommendations


def _compute_recommendation_confidence(skill_data: dict, jd_skills: dict) -> float:
    demand = skill_data.get("demand_score", 50) / 100
    level_bonus = 0.15 if skill_data.get("requirement_level") == "required" else 0.0
    growth_bonus = min(0.1, skill_data.get("growth_rate", 0) / 1000)
    jd_confidence = jd_skills.get(skill_data["skill"], {}).get("confidence", 0.5)
    raw = (demand * 0.5 + jd_confidence * 0.35 + level_bonus + growth_bonus) * 100
    return round(min(99.0, raw), 1)


def _get_recommendation_source(skill_data: dict) -> str:
    parts = [
        f"JD keyword match (confidence: {skill_data.get('demand_score', 50)}%)",
        f"Market demand score: {skill_data.get('demand_score', 50)}/100",
        f"Requirement level: {skill_data.get('requirement_level', 'preferred').capitalize()}",
    ]
    return " | ".join(parts)


def _generate_explanation(skill_data: dict, matched_skills: list[str]) -> str:
    skill = skill_data["skill"]
    level = skill_data.get("requirement_level", "preferred")
    demand = skill_data.get("demand_score", 50)
    growth = skill_data.get("growth_rate", 0)
    db_entry = SKILLS_DATABASE.get(skill, {})
    related = [s for s in db_entry.get("related", []) if s in matched_skills]

    explanation = f"{skill.title()} is {'explicitly required' if level == 'required' else 'preferred'} in the job description. "
    explanation += f"It has a market demand score of {demand}/100 "
    if growth > 30:
        explanation += f"and is one of the fastest-growing skills ({growth}% YoY growth). "
    if related:
        explanation += f"You already have related skills ({', '.join(related[:2])}), which gives you a strong foundation. "
    explanation += f"Expected time to learn: {skill_data.get('time_to_learn', 'varies')}."

    return explanation
