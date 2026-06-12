"""
Module 3: Skill Gap Analysis
Full comparison: resume vs JD, match score, ATS score, radar chart, heatmap.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="Skill Gap Analysis · SkillGap AI", page_icon="🔍", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15,23,42,0.95); border-right:1px solid rgba(99,102,241,0.2); }
.glass-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:14px; }
.matched-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;
               background:rgba(34,211,238,0.12); color:#6ee7b7; border:1px solid rgba(34,211,238,0.3); }
.missing-req-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;
                   background:rgba(239,68,68,0.12); color:#fca5a5; border:1px solid rgba(239,68,68,0.25); }
.missing-pref-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;
                    background:rgba(245,158,11,0.1); color:#fcd34d; border:1px solid rgba(245,158,11,0.25); }
.stButton button { background:linear-gradient(135deg,#6366f1,#4f46e5)!important; color:white!important; border:none!important; border-radius:8px!important; font-weight:600!important; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }
</style>
""", unsafe_allow_html=True)

from utils.gap_analyzer import analyze_gap, get_priority_skills, generate_resume_improvements
from utils.charts import skill_match_gauge, ats_gauge, radar_chart, skill_gap_heatmap, missing_skills_bar, skills_category_pie, ats_breakdown_bar
import pandas as pd

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 🔍 Skill Gap Analysis")
st.markdown("<p style='color:#94a3b8;margin-bottom:24px'>Compare your resume against the job description. Get your match score, ATS score, skill gap matrix, and actionable improvement tips.</p>", unsafe_allow_html=True)

# ─── Prerequisites check ─────────────────────────────────────────────────────

has_resume = bool(st.session_state.get("resume_text"))
has_jd = bool(st.session_state.get("jd_text"))

if not has_resume or not has_jd:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:40px;text-align:center">
        <div style="font-size:3rem">⚠️</div>
        <div style="font-size:1.1rem;color:#e2e8f0;font-weight:600;margin-top:12px">Missing Data</div>
        <div style="color:#64748b;margin-top:8px;font-size:0.9rem">You need both a resume and a job description to run gap analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if not has_resume:
            st.error("❌ Resume not loaded — go to **Resume Analyzer**")
        else:
            st.success("✅ Resume loaded")
    with c2:
        if not has_jd:
            st.error("❌ Job description not loaded — go to **JD Analyzer**")
        else:
            st.success("✅ Job description loaded")
    st.stop()

# ─── Run analysis ─────────────────────────────────────────────────────────────

resume_text = st.session_state["resume_text"]
jd_text = st.session_state["jd_text"]
resume_skills = st.session_state.get("resume_skills", {})
jd_skills = st.session_state.get("jd_skills", {})
resume_analysis = st.session_state.get("resume_analysis", {})

# Re-extract if stale
if not resume_skills:
    from utils.skill_extractor import extract_skills
    resume_skills = extract_skills(resume_text)
    st.session_state["resume_skills"] = resume_skills

if not jd_skills:
    from utils.skill_extractor import extract_skills_from_jd
    jd_skills = extract_skills_from_jd(jd_text)
    st.session_state["jd_skills"] = jd_skills

if not resume_analysis:
    from utils.resume_parser import analyze_resume_structure
    resume_analysis = analyze_resume_structure(resume_text)
    st.session_state["resume_analysis"] = resume_analysis

run_col, _ = st.columns([2, 3])
with run_col:
    if st.button("🚀 Run Full Analysis", use_container_width=True):
        st.session_state.pop("gap_result", None)

with st.spinner("🤖 Computing skill gap analysis..."):
    if "gap_result" not in st.session_state:
        gap = analyze_gap(resume_skills, jd_skills, resume_text, jd_text, resume_analysis)
        st.session_state["gap_result"] = gap
    else:
        gap = st.session_state["gap_result"]

priority_skills = get_priority_skills(gap.missing_skills, jd_skills, top_n=8)
improvements = generate_resume_improvements(resume_analysis, gap)

# ─── Score Gauges ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 📊 Scores Overview")

g1, g2, g3, g4 = st.columns(4)
with g1:
    st.plotly_chart(skill_match_gauge(gap.match_score, "Match Score"), use_container_width=True)
with g2:
    st.plotly_chart(ats_gauge(gap.ats_score), use_container_width=True)
with g3:
    st.plotly_chart(skill_match_gauge(gap.semantic_score, "Semantic Score"), use_container_width=True)
with g4:
    st.plotly_chart(skill_match_gauge(gap.combined_score, "Overall Score"), use_container_width=True)

# Score interpretation
score = gap.combined_score
if score >= 80:
    st.success(f"🎉 **Excellent Match ({score:.0f}%)** — You're a strong candidate! Focus on the few missing skills to be even more competitive.")
elif score >= 60:
    st.warning(f"⚡ **Good Match ({score:.0f}%)** — You meet many requirements. Closing the key skill gaps will significantly improve your chances.")
elif score >= 40:
    st.warning(f"📈 **Moderate Match ({score:.0f}%)** — Some alignment, but notable gaps exist. Focus on required skills first.")
else:
    st.error(f"🎯 **Stretch Role ({score:.0f}%)** — Significant gap detected. This is a growth opportunity — invest in the learning roadmap.")

# ─── Skills Summary ───────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🔧 Skills Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("✅ Matched", len(gap.matched_skills), help="Skills on both your resume and the JD")
c2.metric("🔴 Required Missing", len(gap.required_missing), help="Must-have skills you're missing")
c3.metric("🟡 Preferred Missing", len(gap.preferred_missing), help="Nice-to-have skills you're missing")
c4.metric("⭐ Extra Skills", len(gap.extra_skills), help="Skills on your resume not in this JD")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🗺️ Radar Chart", "🔥 Skill Heatmap", "📊 Missing Skills", "📂 Categories", "📋 ATS Details", "💡 Improvements"
])

# ─── Radar Chart ─────────────────────────────────────────────────────────────
with tab1:
    if gap.category_breakdown:
        cats = list(gap.category_breakdown.keys())[:8]
        jd_scores = [gap.category_breakdown[c]["total"] * 10 for c in cats]
        resume_scores = [gap.category_breakdown[c]["matched"] * 10 for c in cats]
        # Normalize to 0-100
        max_jd = max(jd_scores) if jd_scores else 1
        jd_norm = [min(100, s / max(max_jd, 1) * 100) for s in jd_scores]
        resume_norm = [min(100, s / max(max_jd, 1) * 100) for s in resume_scores]
        st.plotly_chart(radar_chart(cats, resume_norm, jd_norm), use_container_width=True)
        st.caption("Blue = Your Profile · Purple = Job Requirements")
    else:
        st.info("Not enough category data to build radar chart.")

# ─── Heatmap ─────────────────────────────────────────────────────────────────
with tab2:
    if gap.matched_skills or gap.missing_skills:
        st.plotly_chart(
            skill_gap_heatmap(gap.matched_skills[:12], gap.missing_skills[:12], jd_skills),
            use_container_width=True,
        )
        col_leg1, col_leg2 = st.columns(2)
        with col_leg1:
            st.markdown('<span style="color:#6ee7b7">■</span> **Matched** — present in both resume and JD', unsafe_allow_html=True)
        with col_leg2:
            st.markdown('<span style="color:#fca5a5">■</span> **Missing** — in JD but not on resume', unsafe_allow_html=True)
    else:
        st.info("No skills to display in heatmap.")

# ─── Missing Skills ───────────────────────────────────────────────────────────
with tab3:
    col_req, col_pref = st.columns(2)

    with col_req:
        st.markdown("#### 🔴 Required Skills Missing")
        if gap.required_missing:
            for s in gap.required_missing:
                data = jd_skills.get(s, {})
                st.markdown(f'<span class="missing-req-tag">{s.title()}</span>', unsafe_allow_html=True)
        else:
            st.success("✅ You have all required skills!")

    with col_pref:
        st.markdown("#### 🟡 Preferred Skills Missing")
        if gap.preferred_missing:
            for s in gap.preferred_missing:
                st.markdown(f'<span class="missing-pref-tag">{s.title()}</span>', unsafe_allow_html=True)
        else:
            st.success("✅ You have all preferred skills!")

    st.markdown("---")
    if priority_skills:
        st.plotly_chart(missing_skills_bar(priority_skills), use_container_width=True)

    st.markdown("#### ✅ Matched Skills")
    if gap.matched_skills:
        tags = "".join(f'<span class="matched-tag">{s.title()}</span>' for s in gap.matched_skills)
        st.markdown(tags, unsafe_allow_html=True)

    st.markdown("#### ⭐ Your Extra Skills (Not in JD)")
    st.caption("These could still be valuable — mention them in your cover letter!")
    if gap.extra_skills:
        tags = "".join(
            f'<span style="display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.77rem;font-weight:600;margin:2px;background:rgba(99,102,241,0.1);color:#a78bfa;border:1px solid rgba(99,102,241,0.2)">{s.title()}</span>'
            for s in gap.extra_skills
        )
        st.markdown(tags, unsafe_allow_html=True)

# ─── Categories ───────────────────────────────────────────────────────────────
with tab4:
    if gap.category_breakdown:
        col_pie, col_table = st.columns([1, 1])
        with col_pie:
            st.plotly_chart(skills_category_pie(gap.category_breakdown), use_container_width=True)
        with col_table:
            st.markdown("**Category Breakdown**")
            df = pd.DataFrame([
                {
                    "Category": cat,
                    "Matched": d["matched"],
                    "Total in JD": d["total"],
                    "Coverage": f"{d['pct']:.0f}%",
                    "Status": "💪 Strong" if d["pct"] >= 70 else ("⚠️ Partial" if d["pct"] >= 30 else "🔴 Weak"),
                }
                for cat, d in gap.category_breakdown.items()
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)

        col_s, col_w = st.columns(2)
        with col_s:
            st.markdown("**💪 Strength Areas**")
            if gap.strength_areas:
                for a in gap.strength_areas:
                    st.success(f"✅ {a}")
            else:
                st.info("No dominant strength categories identified.")
        with col_w:
            st.markdown("**🎯 Areas to Improve**")
            if gap.weak_areas:
                for a in gap.weak_areas:
                    st.warning(f"⚡ {a}")
            else:
                st.success("No major weak areas detected!")

# ─── ATS Details ─────────────────────────────────────────────────────────────
with tab5:
    st.plotly_chart(ats_breakdown_bar(gap.ats_breakdown), use_container_width=True)

    st.markdown("**ATS Score Component Details**")
    ats_labels = {
        "keyword_match": ("Keyword Match", 30),
        "section_completeness": ("Section Completeness", 25),
        "quantified_achievements": ("Quantified Achievements", 20),
        "word_count": ("Word Count", 10),
        "contact_completeness": ("Contact Info", 10),
        "certifications": ("Certifications", 5),
    }
    for key, (label, max_pts) in ats_labels.items():
        score_val = gap.ats_breakdown.get(key, 0)
        pct = score_val / max_pts
        color = "🟢" if pct >= 0.7 else ("🟡" if pct >= 0.4 else "🔴")
        st.markdown(f"{color} **{label}:** {score_val:.1f} / {max_pts} pts")
        st.progress(min(1.0, pct))

    st.markdown(f"**Total ATS Score: {gap.ats_score:.1f} / 100**")

# ─── Improvements ─────────────────────────────────────────────────────────────
with tab6:
    st.markdown("### 💡 Resume Improvement Suggestions")
    if improvements:
        for imp in improvements:
            priority_color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22d3ee"}.get(imp["priority"], "#6366f1")
            st.markdown(f"""
            <div class="glass-card" style="border-left:3px solid {priority_color}">
                <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                        <span style="font-weight:700;color:#e2e8f0">{imp['category']}</span>
                        <span style="margin-left:8px;padding:2px 8px;border-radius:10px;font-size:0.72rem;background:{priority_color}20;color:{priority_color};border:1px solid {priority_color}40">{imp['priority']} Priority</span>
                    </div>
                    <div style="font-size:0.78rem;color:#6366f1">{imp.get('impact','')}</div>
                </div>
                <div style="margin-top:8px;color:#cbd5e1;font-size:0.9rem">{imp['suggestion']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("🎉 Your resume looks well-structured! Check the other tabs for skill-specific recommendations.")

# ─── Export ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 📥 Export Results")

col_e1, col_e2 = st.columns(2)
with col_e1:
    export_data = {
        "match_score": gap.match_score,
        "ats_score": gap.ats_score,
        "semantic_score": gap.semantic_score,
        "combined_score": gap.combined_score,
        "matched_skills": gap.matched_skills,
        "required_missing": gap.required_missing,
        "preferred_missing": gap.preferred_missing,
        "strength_areas": gap.strength_areas,
        "weak_areas": gap.weak_areas,
    }
    import json
    st.download_button(
        "📥 Download JSON Report",
        data=json.dumps(export_data, indent=2),
        file_name="skillgap_analysis.json",
        mime="application/json",
        use_container_width=True,
    )

with col_e2:
    if gap.matched_skills or gap.missing_skills:
        df_export = pd.DataFrame([
            {"Skill": s, "Status": "Matched", "Requirement": jd_skills.get(s, {}).get("requirement_level", ""), "Demand": jd_skills.get(s, {}).get("demand_score", 0)}
            for s in gap.matched_skills
        ] + [
            {"Skill": s, "Status": "Missing", "Requirement": jd_skills.get(s, {}).get("requirement_level", ""), "Demand": jd_skills.get(s, {}).get("demand_score", 0)}
            for s in gap.missing_skills
        ])
        csv = df_export.to_csv(index=False)
        st.download_button(
            "📊 Download CSV Report",
            data=csv,
            file_name="skillgap_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )
