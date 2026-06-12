"""
Market intelligence data module.
Provides curated demo data for the market insights dashboard.
"""

from __future__ import annotations

try:
    from data.skills_db import SKILLS_DATABASE, TOP_CERTIFICATIONS, INDUSTRY_DEMAND, get_trending_skills, get_high_demand_skills
except ImportError:
    from skills_db import SKILLS_DATABASE, TOP_CERTIFICATIONS, INDUSTRY_DEMAND, get_trending_skills, get_high_demand_skills


SALARY_TRENDS = [
    {"role": "ML Engineer", "2020": 118000, "2021": 125000, "2022": 132000, "2023": 140000, "2024": 150000, "2025": 160000},
    {"role": "Data Scientist", "2020": 105000, "2021": 112000, "2022": 118000, "2023": 125000, "2024": 132000, "2025": 140000},
    {"role": "Data Engineer", "2020": 108000, "2021": 115000, "2022": 122000, "2023": 130000, "2024": 138000, "2025": 148000},
    {"role": "DevOps Engineer", "2020": 110000, "2021": 118000, "2022": 125000, "2023": 132000, "2024": 140000, "2025": 150000},
    {"role": "Software Engineer", "2020": 105000, "2021": 112000, "2022": 120000, "2023": 128000, "2024": 135000, "2025": 142000},
    {"role": "Cloud Architect", "2020": 125000, "2021": 132000, "2022": 140000, "2023": 148000, "2024": 158000, "2025": 168000},
    {"role": "AI/LLM Engineer", "2020": 115000, "2021": 125000, "2022": 140000, "2023": 158000, "2024": 175000, "2025": 195000},
]

JOB_POSTINGS_TREND = [
    {"month": "Jan 2024", "python": 45200, "javascript": 38900, "aws": 32100, "kubernetes": 18400, "react": 31200},
    {"month": "Feb 2024", "python": 47100, "javascript": 40200, "aws": 33800, "kubernetes": 19200, "react": 32100},
    {"month": "Mar 2024", "python": 49800, "javascript": 41500, "aws": 35200, "kubernetes": 20100, "react": 33400},
    {"month": "Apr 2024", "python": 52300, "javascript": 42800, "aws": 36900, "kubernetes": 21500, "react": 34200},
    {"month": "May 2024", "python": 54900, "javascript": 44100, "aws": 38200, "kubernetes": 22800, "react": 35100},
    {"month": "Jun 2024", "python": 57200, "javascript": 45600, "aws": 40100, "kubernetes": 24200, "react": 36800},
    {"month": "Jul 2024", "python": 60100, "javascript": 47200, "aws": 42500, "kubernetes": 26100, "react": 38200},
    {"month": "Aug 2024", "python": 63400, "javascript": 48900, "aws": 44800, "kubernetes": 28400, "react": 39500},
    {"month": "Sep 2024", "python": 66800, "javascript": 50200, "aws": 47200, "kubernetes": 30800, "react": 41000},
    {"month": "Oct 2024", "python": 70200, "javascript": 51800, "aws": 49600, "kubernetes": 33200, "react": 42400},
    {"month": "Nov 2024", "python": 73100, "javascript": 53200, "aws": 52100, "kubernetes": 35900, "react": 43800},
    {"month": "Dec 2024", "python": 76500, "javascript": 54700, "aws": 54800, "kubernetes": 38700, "react": 45200},
]

AI_ML_SKILL_DEMAND = {
    "Large Language Models": 97,
    "Prompt Engineering": 92,
    "MLOps": 88,
    "Deep Learning": 90,
    "NLP": 88,
    "Computer Vision": 85,
    "Machine Learning": 94,
    "Reinforcement Learning": 75,
    "Data Analysis": 92,
    "Feature Engineering": 82,
    "Model Deployment": 85,
    "RAG Systems": 88,
}

REMOTE_WORK_STATS = {
    "Fully Remote": 42,
    "Hybrid": 38,
    "On-site": 20,
}

COMPANY_SIZE_DEMAND = {
    "Startup (1-50)": {"python": 88, "react": 82, "aws": 78, "docker": 75, "ml": 70},
    "Mid-size (51-500)": {"python": 90, "sql": 88, "aws": 85, "kubernetes": 72, "ml": 80},
    "Enterprise (500+)": {"java": 85, "sql": 92, "aws": 90, "azure": 80, "kubernetes": 85},
}

SKILLS_BY_EXPERIENCE = {
    "Entry Level (0-2 yrs)": [
        "Python", "SQL", "Git", "JavaScript", "Pandas", "NumPy",
        "Data Analysis", "Machine Learning Basics", "React",
    ],
    "Mid Level (3-5 yrs)": [
        "Machine Learning", "Deep Learning", "Docker", "AWS", "PostgreSQL",
        "FastAPI", "CI/CD", "Kubernetes basics", "NLP",
    ],
    "Senior Level (5+ yrs)": [
        "MLOps", "Kubernetes", "Terraform", "System Design", "LLMs",
        "Data Architecture", "Cloud Architecture", "Team Leadership",
    ],
}

TOP_TOOLS_2025 = [
    {"tool": "Python", "category": "Language", "usage_pct": 94},
    {"tool": "Git", "category": "DevOps", "usage_pct": 92},
    {"tool": "Docker", "category": "DevOps", "usage_pct": 78},
    {"tool": "VS Code", "category": "IDE", "usage_pct": 74},
    {"tool": "PostgreSQL", "category": "Database", "usage_pct": 71},
    {"tool": "AWS", "category": "Cloud", "usage_pct": 68},
    {"tool": "Jupyter Notebook", "category": "Data Science", "usage_pct": 66},
    {"tool": "Kubernetes", "category": "DevOps", "usage_pct": 52},
    {"tool": "PyTorch", "category": "ML Framework", "usage_pct": 50},
    {"tool": "Terraform", "category": "IaC", "usage_pct": 44},
    {"tool": "React", "category": "Frontend", "usage_pct": 62},
    {"tool": "Pandas", "category": "Data", "usage_pct": 72},
]

EMERGING_SKILLS_2025 = [
    {"skill": "AI Agents / Agentic AI", "growth": 250, "interest_score": 96},
    {"skill": "RAG (Retrieval-Augmented Generation)", "growth": 180, "interest_score": 92},
    {"skill": "Multimodal AI", "growth": 160, "interest_score": 90},
    {"skill": "WebAssembly", "growth": 95, "interest_score": 78},
    {"skill": "Edge AI / TinyML", "growth": 140, "interest_score": 82},
    {"skill": "Quantum Computing", "growth": 80, "interest_score": 72},
    {"skill": "Rust for Systems", "growth": 110, "interest_score": 80},
    {"skill": "dbt (Data Build Tool)", "growth": 120, "interest_score": 84},
    {"skill": "Observability / OpenTelemetry", "growth": 105, "interest_score": 79},
    {"skill": "Graph Neural Networks", "growth": 130, "interest_score": 77},
]


def get_market_overview() -> dict:
    """Return a summary of market intelligence metrics."""
    trending = get_trending_skills(10)
    high_demand = get_high_demand_skills(10)

    return {
        "trending_skills": trending,
        "high_demand_skills": high_demand,
        "top_certifications": TOP_CERTIFICATIONS[:8],
        "salary_trends": SALARY_TRENDS,
        "job_postings_trend": JOB_POSTINGS_TREND,
        "industry_demand": INDUSTRY_DEMAND,
        "remote_work_stats": REMOTE_WORK_STATS,
        "emerging_skills": EMERGING_SKILLS_2025,
        "top_tools": TOP_TOOLS_2025,
        "ai_ml_demand": AI_ML_SKILL_DEMAND,
    }
