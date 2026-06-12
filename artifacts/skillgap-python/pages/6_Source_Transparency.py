"""
Module 6: Source Transparency
Every recommendation with its data source, confidence score, and explanation.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="Source Transparency · SkillGap AI", page_icon="🔎", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15,23,42,0.95); border-right:1px solid rgba(99,102,241,0.2); }
.glass-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:14px; }
.source-badge { display:inline-block; padding:3px 10px; border-radius:6px; font-size:0.75rem; font-weight:600; margin:2px;
                background:rgba(99,102,241,0.12); color:#a78bfa; border:1px solid rgba(99,102,241,0.3); }
.confidence-bar-container { background:rgba(255,255,255,0.05); border-radius:4px; height:6px; margin-top:4px; }
.stButton button { background:linear-gradient(135deg,#6366f1,#4f46e5)!important; color:white!important; border:none!important; border-radius:8px!important; font-weight:600!important; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }
</style>
""", unsafe_allow_html=True)

from utils.recommender import generate_skill_recommendations
from utils.skill_extractor import extract_skills, extract_skills_from_jd
from data.skills_db import SKILLS_DATABASE
import pandas as pd
import json

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 🔎 Source Transparency")
st.markdown("""
<p style='color:#94a3b8;margin-bottom:12px'>
    Full data provenance for every skill extraction and recommendation. 
    We believe in <b style='color:#6366f1'>transparent AI</b> — you can see exactly why every recommendation was generated.
</p>
""", unsafe_allow_html=True)

# ─── Methodology Card ─────────────────────────────────────────────────────────

with st.expander("📖 How Our Analysis Works — Full Methodology", expanded=False):
    st.markdown("""
    ### Extraction Pipeline

    **Step 1: Skill Extraction (NLP Keyword Matching)**
    - Each skill in our database of 40+ curated skills has a list of canonical names and aliases
    - We use regular expression whole-word matching (`(?<![a-z-])term(?![a-z-])`) to find skills in text
    - Multiple occurrences increase confidence via `confidence = min(1.0, 0.6 + 0.1 × log(1 + count))`
    - Exact canonical name matches receive a +0.15 confidence bonus

    **Step 2: Requirement Classification**
    - JD text is scanned for "required/must-have/essential" and "preferred/nice-to-have/bonus" signals
    - Skills appearing near required signals are classified as **Required**; others as **Preferred**
    - Default fallback: skills with demand_score ≥ 80 → Required; others → Preferred

    **Step 3: Match Scoring**
    - **Match Score** = weighted overlap (required skills count ×2, preferred ×1)
    - **Semantic Score** = TF-IDF cosine similarity between resume text and JD text
    - **ATS Score** = composite: keyword match (30pts) + sections (25pts) + quantified achievements (20pts) + word count (10pts) + contact (10pts) + certifications (5pts)
    - **Combined Score** = Match × 0.50 + Semantic × 0.25 + ATS × 0.25

    **Step 4: Recommendation Ranking**
    - Priority Score = `demand_score × level_weight` where level_weight = 2.0 (required) or 1.0 (preferred)
    - Recommendation Confidence = `(demand × 0.5 + jd_confidence × 0.35 + level_bonus + growth_bonus) × 100`

    ### Data Sources
    - **Skills Database**: Curated database of 40+ technology skills with demand scores, growth rates, aliases, and learning resources
    - **Market Data**: Synthesized from job posting trends, developer surveys (Stack Overflow 2024), and industry reports
    - **Resources**: Manually curated from Coursera, edX, official documentation, and community tutorials
    """)

# ─── Check if analysis exists ─────────────────────────────────────────────────

gap = st.session_state.get("gap_result")
resume_skills = st.session_state.get("resume_skills", {})
jd_skills = st.session_state.get("jd_skills", {})
resume_text = st.session_state.get("resume_text", "")
jd_text = st.session_state.get("jd_text", "")

if not gap or not resume_skills or not jd_skills:
    st.info("Run a **Skill Gap Analysis** first to see full source transparency for your results.")

    # Show methodology demo
    st.markdown("---")
    st.markdown("### 📊 Skills Database Overview")
    st.markdown(f"Our curated skills database contains **{len(SKILLS_DATABASE)} skills** across multiple categories:")

    cat_counts: dict[str, int] = {}
    for skill_data in SKILLS_DATABASE.values():
        cat = skill_data["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    df_cats = pd.DataFrame([
        {"Category": cat, "Skills Count": count, "Avg Demand": round(
            sum(v["demand_score"] for k, v in SKILLS_DATABASE.items() if v["category"] == cat) / max(count, 1), 1
        )}
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1])
    ])
    st.dataframe(df_cats, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🔍 Sample Skill Entry — Data Provenance")
    sample_skill = "python"
    sample_data = SKILLS_DATABASE[sample_skill]
    st.markdown(f"**Skill: {sample_skill.title()}**")
    col1, col2 = st.columns(2)
    with col1:
        st.json({
            "canonical_name": sample_skill,
            "category": sample_data["category"],
            "demand_score": sample_data["demand_score"],
            "growth_rate": sample_data["growth_rate"],
            "aliases": sample_data["aliases"],
        })
    with col2:
        st.json({
            "description": sample_data["description"],
            "time_to_learn": sample_data["time_to_learn"],
            "avg_salary": sample_data["avg_salary"],
            "resources": [r["name"] for r in sample_data.get("resources", [])],
        })
    st.stop()

# ─── Analysis exists — show full transparency ─────────────────────────────────

recommendations = generate_skill_recommendations(gap.matched_skills, gap.missing_skills, jd_skills)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Score Breakdown", "🔧 Skill Evidence", "🤖 Recommendations Provenance", "🗄️ Skills DB"
])

# ─── Score Breakdown ─────────────────────────────────────────────────────────
with tab1:
    st.markdown("### 📊 Complete Score Calculation")

    scores = [
        ("Match Score", gap.match_score, "Weighted keyword overlap between resume and JD skills (required ×2, preferred ×1)"),
        ("Semantic Score", gap.semantic_score, "TF-IDF cosine similarity between full resume text and JD text"),
        ("ATS Score", gap.ats_score, "Composite ATS readiness: keywords + sections + achievements + contact + certifications"),
        ("Combined Score", gap.combined_score, "Weighted average: Match×0.50 + Semantic×0.25 + ATS×0.25"),
    ]

    for label, score, explanation in scores:
        color = "#22d3ee" if score >= 70 else ("#f59e0b" if score >= 40 else "#ef4444")
        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div style="font-weight:700;color:#e2e8f0">{label}</div>
                <div style="font-size:1.4rem;font-weight:700;color:{color}">{score:.1f}{'%' if label != 'ATS Score' else '/100'}</div>
            </div>
            <div style="color:#64748b;font-size:0.85rem;margin-top:6px">{explanation}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(score / 100)

    st.markdown("---")
    st.markdown("### 🔬 ATS Score Breakdown")
    ats_labels = {
        "keyword_match": ("Keyword Match", 30, "Skills on resume matching JD keywords, weighted by requirement level"),
        "section_completeness": ("Section Completeness", 25, "Presence of contact, summary, experience, skills, education sections"),
        "quantified_achievements": ("Quantified Achievements", 20, "Lines containing numbers, percentages, dollar amounts, or metrics"),
        "word_count": ("Word Count", 10, "Optimal range: 300–800 words = 10 pts; shorter/longer = partial credit"),
        "contact_completeness": ("Contact Info", 10, "Email (4pts), phone (3pts), LinkedIn (2pts), GitHub (1pt)"),
        "certifications": ("Certifications", 5, "Recognized certification keywords detected in resume"),
    }
    for key, (label, max_pts, explanation) in ats_labels.items():
        val = gap.ats_breakdown.get(key, 0)
        pct = val / max(max_pts, 1)
        color = "#22d3ee" if pct >= 0.7 else ("#f59e0b" if pct >= 0.4 else "#ef4444")
        st.markdown(f"""
        <div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <span style="color:#e2e8f0;font-weight:600">{label}</span>
                    <div style="color:#64748b;font-size:0.78rem;margin-top:2px">{explanation}</div>
                </div>
                <span style="color:{color};font-weight:700;font-size:1.05rem">{val:.1f} / {max_pts}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(1.0, pct))

# ─── Skill Evidence ───────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🔧 Skill Extraction Evidence")
    st.caption("Each skill detected in your resume, with the exact text snippets that triggered detection")

    col_res, col_jd = st.columns(2)

    with col_res:
        st.markdown("#### 📄 Resume Skills — Evidence")
        for skill, data in sorted(resume_skills.items(), key=lambda x: -x[1]["confidence"])[:20]:
            with st.expander(f"{skill.title()} — {data['confidence']*100:.0f}% confidence"):
                st.markdown(f"**Category:** {data['category']}")
                st.markdown(f"**Extraction Method:** Regex keyword + alias matching")
                confidence = data["confidence"]
                conf_color = "#22d3ee" if confidence >= 0.8 else ("#f59e0b" if confidence >= 0.6 else "#ef4444")
                st.markdown(f"**Confidence Score:** <span style='color:{conf_color}'>{confidence*100:.1f}%</span>", unsafe_allow_html=True)
                st.progress(confidence)
                if data.get("evidence"):
                    st.markdown("**Evidence (text snippets):**")
                    for ev in data["evidence"][:3]:
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.04);border-left:2px solid #6366f1;padding:6px 10px;margin:4px 0;font-size:0.82rem;color:#94a3b8;border-radius:0 6px 6px 0">
                            {ev}
                        </div>
                        """, unsafe_allow_html=True)

    with col_jd:
        st.markdown("#### 💼 JD Skills — Evidence")
        for skill, data in sorted(jd_skills.items(), key=lambda x: -x[1]["confidence"])[:20]:
            level = data.get("requirement_level", "preferred")
            level_color = "#ef4444" if level == "required" else "#f59e0b"
            with st.expander(f"{skill.title()} — {level.capitalize()} · {data['confidence']*100:.0f}%"):
                st.markdown(f"**Requirement Level:** <span style='color:{level_color}'>{level.capitalize()}</span>", unsafe_allow_html=True)
                st.markdown(f"**Classification Method:** Proximity to required/preferred signal words in JD")
                st.markdown(f"**Confidence:** {data['confidence']*100:.1f}%")
                st.progress(data["confidence"])
                if data.get("evidence"):
                    st.markdown("**Evidence:**")
                    for ev in data["evidence"][:2]:
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.04);border-left:2px solid {level_color};padding:6px 10px;margin:4px 0;font-size:0.82rem;color:#94a3b8;border-radius:0 6px 6px 0">
                            {ev}
                        </div>
                        """, unsafe_allow_html=True)

# ─── Recommendations Provenance ───────────────────────────────────────────────
with tab3:
    st.markdown("### 🤖 Recommendation Provenance")
    st.caption("Full data trail for every recommendation — why it was generated, what signals drove it")

    if not recommendations:
        st.info("No recommendations generated (you already match all job requirements).")
    else:
        for rec in recommendations:
            confidence = rec["confidence"]
            conf_color = "#22d3ee" if confidence >= 80 else ("#f59e0b" if confidence >= 60 else "#ef4444")

            with st.expander(
                f"#{rec['rank']} {rec['skill'].title()} — Confidence: {confidence:.1f}% | Rank Score: {rec['demand_score'] * (2 if rec['requirement_level']=='required' else 1):.0f}",
                expanded=rec["rank"] == 1,
            ):
                st.markdown("**📊 Scoring Signals:**")
                signals = [
                    ("JD Requirement Level", rec["requirement_level"].capitalize(), "#ef4444" if rec["requirement_level"] == "required" else "#f59e0b"),
                    ("JD Detection Confidence", f"{jd_skills.get(rec['skill'], {}).get('confidence', 0)*100:.1f}%", "#6366f1"),
                    ("Market Demand Score", f"{rec['demand_score']}/100", "#22d3ee"),
                    ("YoY Growth Rate", f"+{rec['growth_rate']}%", "#10b981"),
                    ("Requirement Weight", "2.0× (required)" if rec["requirement_level"] == "required" else "1.0× (preferred)", "#a78bfa"),
                    ("Final Recommendation Confidence", f"{confidence:.1f}%", conf_color),
                ]
                for sig_name, sig_val, sig_color in signals:
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                        <span style="color:#94a3b8;font-size:0.85rem">{sig_name}</span>
                        <span style="color:{sig_color};font-weight:600;font-size:0.85rem">{sig_val}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"**📝 Source:** `{rec['source']}`")
                st.markdown(f"**💬 Explanation:** {rec['explanation']}")

                if rec.get("related_skills"):
                    st.markdown(f"**🔗 Leverage:** You have related skills: {', '.join(rec['related_skills'])}")

# ─── Skills Database ─────────────────────────────────────────────────────────
with tab4:
    st.markdown("### 🗄️ Skills Database Reference")
    st.markdown(f"Showing all **{len(SKILLS_DATABASE)} skills** in the knowledge base:")

    search = st.text_input("🔍 Search skills database", placeholder="e.g. python, aws, machine learning...")

    db_rows = []
    for skill_name, skill_data in SKILLS_DATABASE.items():
        if search and search.lower() not in skill_name.lower() and not any(
            search.lower() in alias.lower() for alias in skill_data.get("aliases", [])
        ):
            continue
        db_rows.append({
            "Skill": skill_name.title(),
            "Category": skill_data["category"],
            "Demand Score": skill_data["demand_score"],
            "Growth Rate": f"+{skill_data['growth_rate']}% YoY",
            "Avg Salary": f"${skill_data.get('avg_salary',0):,.0f}" if skill_data.get("avg_salary") else "N/A",
            "Time to Learn": skill_data.get("time_to_learn", "Varies"),
            "Aliases": ", ".join(skill_data.get("aliases", [])[:3]),
        })

    if db_rows:
        df_db = pd.DataFrame(db_rows).sort_values("Demand Score", ascending=False)
        st.dataframe(df_db, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(db_rows)} of {len(SKILLS_DATABASE)} skills")
    else:
        st.info(f"No skills found matching '{search}'")

    st.markdown("---")
    st.markdown("### 📥 Export Full Database")
    db_json = {k: {
        "category": v["category"],
        "demand_score": v["demand_score"],
        "growth_rate": v["growth_rate"],
        "aliases": v["aliases"],
        "resources": v.get("resources", []),
    } for k, v in SKILLS_DATABASE.items()}

    st.download_button(
        "📥 Download Skills Database (JSON)",
        data=json.dumps(db_json, indent=2),
        file_name="skillgap_ai_skills_database.json",
        mime="application/json",
    )
