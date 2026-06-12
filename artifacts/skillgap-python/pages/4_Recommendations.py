"""
Module 4: AI Recommendations & 30/60/90-Day Learning Roadmap
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="Recommendations · SkillGap AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15,23,42,0.95); border-right:1px solid rgba(99,102,241,0.2); }
.glass-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:14px; }
.roadmap-card { background:rgba(255,255,255,0.03); border-radius:16px; padding:24px; margin-bottom:20px; border-top:3px solid; }
.resource-link { display:inline-block; padding:4px 12px; border-radius:6px; font-size:0.78rem; color:#6366f1; border:1px solid rgba(99,102,241,0.3);
                 background:rgba(99,102,241,0.08); margin:3px; text-decoration:none; }
.cert-card { background:rgba(99,102,241,0.06); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:14px; margin:6px 0; }
.stButton button { background:linear-gradient(135deg,#6366f1,#4f46e5)!important; color:white!important; border:none!important; border-radius:8px!important; font-weight:600!important; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }
</style>
""", unsafe_allow_html=True)

from utils.recommender import generate_roadmap, generate_skill_recommendations, generate_learning_resources
from utils.gap_analyzer import get_priority_skills

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 🤖 AI Recommendations")
st.markdown("<p style='color:#94a3b8;margin-bottom:24px'>Personalized skill recommendations and a 30/60/90-day learning roadmap based on your gap analysis.</p>", unsafe_allow_html=True)

# ─── Prerequisites ────────────────────────────────────────────────────────────

gap = st.session_state.get("gap_result")
jd_skills = st.session_state.get("jd_skills", {})
resume_skills = st.session_state.get("resume_skills", {})

if not gap:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:48px;text-align:center">
        <div style="font-size:3rem">🤖</div>
        <div style="font-size:1.1rem;color:#e2e8f0;font-weight:600;margin-top:12px">No Analysis Yet</div>
        <div style="color:#64748b;margin-top:8px">Run <b>Skill Gap Analysis</b> first, then come back here for your personalized roadmap.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

job_title = st.session_state.get("jd_title", "the target role")

# ─── Generate recommendations ────────────────────────────────────────────────

with st.spinner("🤖 Generating personalized recommendations..."):
    recommendations = generate_skill_recommendations(gap.matched_skills, gap.missing_skills, jd_skills)
    roadmap = generate_roadmap(gap.missing_skills, jd_skills, gap.matched_skills, job_title)

# ─── Overview metrics ─────────────────────────────────────────────────────────

m1, m2, m3, m4 = st.columns(4)
m1.metric("🎯 Skills to Learn", roadmap.total_skills)
m2.metric("⏱️ Est. Effort", f"{roadmap.estimated_effort_hrs}h", help="Total estimated learning hours (~20h per skill)")
m3.metric("📋 Recommendations", len(recommendations))
m4.metric("📚 Resources", sum(len(r.get("resources", [])) for r in recommendations))

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["🗺️ 30/60/90 Roadmap", "🎯 Skill Recommendations", "📚 Resources"])

# ─── Roadmap Tab ─────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f"### 🗺️ Your Personalized Roadmap for **{job_title}**")

    phase_colors = {"day_30": "#6366f1", "day_60": "#22d3ee", "day_90": "#10b981"}
    phases = [
        (roadmap.day_30, "#6366f1", "🟣"),
        (roadmap.day_60, "#22d3ee", "🔵"),
        (roadmap.day_90, "#10b981", "🟢"),
    ]

    for phase, color, emoji in phases:
        if not phase.name:
            continue
        st.markdown(f"""
        <div class="roadmap-card" style="border-top-color:{color}">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
                <span style="font-size:1.5rem">{emoji}</span>
                <div>
                    <div style="font-size:1.1rem;font-weight:700;color:{color}">{phase.name}</div>
                    <div style="font-size:0.85rem;color:#64748b">{phase.duration}</div>
                </div>
            </div>
            <div style="color:#94a3b8;font-size:0.9rem;margin-bottom:14px"><b style="color:#e2e8f0">Goal:</b> {phase.goal}</div>
        </div>
        """, unsafe_allow_html=True)

        if phase.skills:
            st.markdown(f"**{emoji} Skills to Learn ({phase.duration})**")
            for skill_item in phase.skills:
                with st.expander(f"📚 {skill_item['skill'].title()} — {skill_item.get('time_to_learn', 'TBD')}", expanded=False):
                    c1, c2, c3 = st.columns(3)
                    level_color = "#ef4444" if skill_item.get("requirement_level") == "required" else "#f59e0b"
                    c1.markdown(f"**Requirement:** <span style='color:{level_color}'>{skill_item.get('requirement_level','preferred').capitalize()}</span>", unsafe_allow_html=True)
                    c2.markdown(f"**Market Demand:** {skill_item.get('demand_score', 0)}/100")
                    c3.markdown(f"**Growth Rate:** +{skill_item.get('growth_rate', 0)}% YoY")

                    if skill_item.get("description"):
                        st.markdown(f"*{skill_item['description']}*")

                    if skill_item.get("resources"):
                        st.markdown("**Learning Resources:**")
                        for res in skill_item["resources"]:
                            type_icon = {"course": "🎓", "tutorial": "📖", "documentation": "📄", "book": "📚", "certification": "🏅"}.get(res.get("type", ""), "🔗")
                            st.markdown(f"• {type_icon} [{res['name']}]({res['url']}) — *{res.get('type', 'resource').capitalize()}*")

                    if skill_item.get("related"):
                        related_str = ", ".join(skill_item["related"][:4])
                        st.markdown(f"**Related Skills:** {related_str}")

        # Milestones
        if phase.milestones:
            st.markdown(f"**🎯 Milestones ({phase.duration})**")
            for milestone in phase.milestones:
                st.markdown(f"""
                <div style="display:flex;align-items:start;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                    <span style="color:{color};margin-top:2px">◆</span>
                    <span style="color:#cbd5e1;font-size:0.88rem">{milestone}</span>
                </div>
                """, unsafe_allow_html=True)

        # Projects
        if phase.projects:
            st.markdown(f"**🛠️ Suggested Projects ({phase.duration})**")
            for proj in phase.projects[:2]:
                st.markdown(f"""
                <div class="glass-card" style="padding:14px 16px">
                    <div style="font-weight:600;color:#e2e8f0">{proj['title']}</div>
                    <div style="color:#64748b;font-size:0.85rem;margin-top:4px">{proj['description']}</div>
                    <div style="margin-top:6px;font-size:0.8rem;color:#94a3b8">Difficulty: <span style="color:{color}">{proj['difficulty']}</span>
                    {' · Skills: ' + ', '.join(proj.get('skills_used', [])[:3]) if proj.get('skills_used') else ''}</div>
                </div>
                """, unsafe_allow_html=True)

        # Certifications
        if phase.certifications:
            st.markdown(f"**📜 Recommended Certifications ({phase.duration})**")
            for cert in phase.certifications[:2]:
                st.markdown(f"""
                <div class="cert-card">
                    <span style="font-weight:600;color:#e2e8f0">{cert['name']}</span>
                    <span style="margin-left:8px;color:#64748b;font-size:0.82rem">by {cert['provider']}</span>
                    <span style="float:right;color:#10b981;font-size:0.82rem">{cert['salary_boost']}</span>
                    <div style="margin-top:4px;font-size:0.8rem;color:#6366f1">Demand: {cert['demand']}/100</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

# ─── Skill Recommendations Tab ────────────────────────────────────────────────
with tab2:
    st.markdown("### 🎯 Personalized Skill Recommendations")
    st.caption("Ranked by priority score = market demand × requirement weight × confidence")

    if not recommendations:
        st.info("No missing skills to recommend. You already match the job requirements well!")
    else:
        for rec in recommendations:
            confidence_color = "#22d3ee" if rec["confidence"] >= 80 else ("#f59e0b" if rec["confidence"] >= 60 else "#ef4444")
            level_color = "#ef4444" if rec["requirement_level"] == "required" else "#f59e0b"

            with st.expander(
                f"#{rec['rank']} · {rec['skill'].title()} — Confidence: {rec['confidence']:.0f}% | Demand: {rec['demand_score']}/100",
                expanded=rec["rank"] <= 3,
            ):
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f"**Requirement:** <span style='color:{level_color}'>{rec['requirement_level'].capitalize()}</span>", unsafe_allow_html=True)
                c2.markdown(f"**Growth Rate:** +{rec['growth_rate']}% YoY")
                c3.markdown(f"**Time to Learn:** {rec['time_to_learn']}")
                if rec["avg_salary_impact"]:
                    c4.markdown(f"**Avg Salary:** ${rec['avg_salary_impact']:,.0f}")

                st.markdown(f"""
                <div style="background:rgba(99,102,241,0.06);border-radius:8px;padding:12px;margin:10px 0">
                    <div style="font-size:0.82rem;color:#64748b;margin-bottom:4px">AI Explanation</div>
                    <div style="color:#cbd5e1;font-size:0.9rem">{rec['explanation']}</div>
                </div>
                """, unsafe_allow_html=True)

                if rec.get("resources"):
                    st.markdown("**📚 Learning Resources:**")
                    for res in rec["resources"]:
                        type_icon = {"course": "🎓", "tutorial": "📖", "documentation": "📄", "book": "📚", "certification": "🏅"}.get(res.get("type", ""), "🔗")
                        st.markdown(f"• {type_icon} [{res['name']}]({res['url']})")

                if rec.get("related_skills"):
                    st.markdown(f"**🔗 Related skills you already have:** {', '.join(rec['related_skills'])}")

                # Confidence meter
                st.markdown(f"**Recommendation Confidence:** {rec['confidence']:.1f}%")
                st.progress(rec["confidence"] / 100)

# ─── Resources Tab ────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### 📚 Curated Learning Resources")

    all_resources = generate_learning_resources(gap.missing_skills[:12])

    if not all_resources:
        st.info("No curated resources available for your missing skills.")
    else:
        resource_types = ["course", "tutorial", "documentation", "book", "certification"]
        for rtype in resource_types:
            type_icon = {"course": "🎓", "tutorial": "📖", "documentation": "📄", "book": "📚", "certification": "🏅"}.get(rtype, "🔗")
            type_resources = [
                (skill, res)
                for skill, resources in all_resources.items()
                for res in resources
                if res.get("type") == rtype
            ]
            if type_resources:
                st.markdown(f"#### {type_icon} {rtype.capitalize()}s")
                for skill, res in type_resources:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:12px;margin:4px 0;display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <span style="font-weight:600;color:#e2e8f0">{res['name']}</span>
                            <span style="margin-left:8px;font-size:0.78rem;padding:2px 8px;border-radius:10px;background:rgba(99,102,241,0.1);color:#a78bfa">{skill.title()}</span>
                        </div>
                        <a href="{res['url']}" target="_blank" style="color:#6366f1;font-size:0.82rem;text-decoration:none">Open →</a>
                    </div>
                    """, unsafe_allow_html=True)

# ─── Export roadmap ───────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 📥 Export Your Roadmap")

roadmap_text = f"# Learning Roadmap for {job_title}\n\n"
for phase in [roadmap.day_30, roadmap.day_60, roadmap.day_90]:
    if phase.name:
        roadmap_text += f"## {phase.name} ({phase.duration})\n"
        roadmap_text += f"**Goal:** {phase.goal}\n\n"
        if phase.skills:
            roadmap_text += "### Skills to Learn\n"
            for s in phase.skills:
                roadmap_text += f"- {s['skill'].title()} ({s.get('time_to_learn','')})\n"
        if phase.milestones:
            roadmap_text += "\n### Milestones\n"
            for m in phase.milestones:
                roadmap_text += f"- {m}\n"
        roadmap_text += "\n"

st.download_button(
    "📥 Download Roadmap (Markdown)",
    data=roadmap_text,
    file_name="learning_roadmap.md",
    mime="text/markdown",
    use_container_width=False,
)
