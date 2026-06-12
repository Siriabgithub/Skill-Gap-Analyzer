"""
Module 1: Resume Analyzer
Upload PDF/DOCX, extract text, detect skills, education, certifications.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="Resume Analyzer · SkillGap AI", page_icon="📄", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15,23,42,0.95); border-right:1px solid rgba(99,102,241,0.2); }
.glass-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:14px; }
.skill-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;
             background:rgba(99,102,241,0.15); color:#a78bfa; border:1px solid rgba(99,102,241,0.3); transition:0.2s; }
.skill-tag:hover { background:rgba(99,102,241,0.3); }
.section-header { font-size:1.2rem; font-weight:700; color:#e2e8f0; margin:20px 0 12px; display:flex; align-items:center; gap:8px; }
.info-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); color:#cbd5e1; font-size:0.88rem; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }
.stButton button { background:linear-gradient(135deg,#6366f1,#4f46e5)!important; color:white!important; border:none!important; border-radius:8px!important; font-weight:600!important; }
</style>
""", unsafe_allow_html=True)

from utils.resume_parser import parse_file, analyze_resume_structure, detect_education, detect_certifications, detect_quantified_achievements
from utils.skill_extractor import extract_skills, get_skill_categories

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 📄 Resume Analyzer")
st.markdown("<p style='color:#94a3b8;margin-bottom:24px'>Upload your resume in PDF, DOCX, or TXT format. Our NLP engine extracts skills, education, certifications, and structural insights.</p>", unsafe_allow_html=True)

# ─── Upload ───────────────────────────────────────────────────────────────────

col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Drop your resume here",
        type=["pdf", "docx", "txt"],
        help="Supports PDF, DOCX, and plain text files up to 10 MB",
    )

with col_info:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight:600;color:#e2e8f0;margin-bottom:10px">📝 Supported Formats</div>
        <div class="info-row"><span>PDF</span><span style="color:#22d3ee">✓ pdfplumber</span></div>
        <div class="info-row"><span>DOCX</span><span style="color:#22d3ee">✓ python-docx</span></div>
        <div class="info-row"><span>TXT</span><span style="color:#22d3ee">✓ UTF-8</span></div>
        <div style="margin-top:10px;font-size:0.78rem;color:#64748b">Max size: 10 MB<br>Password-protected PDFs not supported</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Or paste text ────────────────────────────────────────────────────────────

with st.expander("✏️ Or paste resume text directly"):
    pasted_text = st.text_area(
        "Paste your resume content here",
        height=250,
        placeholder="Copy and paste your full resume text here...",
    )
    if st.button("Analyze Pasted Text", use_container_width=True):
        if pasted_text.strip():
            st.session_state["resume_text"] = pasted_text
            st.session_state["resume_source"] = "pasted text"
            st.rerun()
        else:
            st.warning("Please paste some text first.")

# ─── Parse ────────────────────────────────────────────────────────────────────

if uploaded_file is not None:
    with st.spinner("🔍 Parsing resume..."):
        text, error = parse_file(uploaded_file)

    if error:
        st.error(f"❌ **Parse Error:** {error}")
        st.stop()

    st.session_state["resume_text"] = text
    st.session_state["resume_source"] = uploaded_file.name
    st.session_state["resume_filename"] = uploaded_file.name

resume_text = st.session_state.get("resume_text", "")

if not resume_text:
    st.markdown("""
    <div class="glass-card" style="text-align:center;padding:48px 24px">
        <div style="font-size:3rem;margin-bottom:12px">📤</div>
        <div style="font-size:1.1rem;color:#e2e8f0;font-weight:600">Upload Your Resume to Begin</div>
        <div style="color:#64748b;margin-top:8px;font-size:0.9rem">
            Drag and drop a file above, or paste text directly
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Success banner ───────────────────────────────────────────────────────────

source = st.session_state.get("resume_source", "uploaded file")
st.success(f"✅ Resume parsed from **{source}** — {len(resume_text.split())} words extracted")

# ─── Analysis ─────────────────────────────────────────────────────────────────

with st.spinner("🤖 Running NLP analysis..."):
    analysis = analyze_resume_structure(resume_text)
    skills = extract_skills(resume_text)
    categorized = get_skill_categories(list(skills.keys()))

st.session_state["resume_skills"] = skills
st.session_state["resume_analysis"] = analysis

# ─── Top Metrics ─────────────────────────────────────────────────────────────

st.markdown("---")
m1, m2, m3, m4 = st.columns(4)

completeness = analysis["completeness_score"]
color = "#22d3ee" if completeness >= 70 else ("#f59e0b" if completeness >= 40 else "#ef4444")

m1.metric("🏆 Completeness", f"{completeness}/100",
          delta="Good" if completeness >= 70 else "Needs Work")
m2.metric("🔧 Skills Detected", len(skills))
m3.metric("📝 Word Count", analysis["word_count"])
m4.metric("🚨 ATS Risks", len(analysis["ats_risks"]))

# ─── Progress bar ─────────────────────────────────────────────────────────────

st.markdown(f"**Resume Completeness Score:** {completeness}/100")
st.progress(completeness / 100)

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🔧 Skills", "🏛️ Sections", "🎓 Education", "📜 Certifications", "📋 Raw Text"]
)

# ── Skills Tab ────────────────────────────────────────────────────────────────
with tab1:
    if not skills:
        st.info("No skills detected. Try a more detailed resume.")
    else:
        st.markdown(f"**{len(skills)} skills detected** — sorted by confidence")

        # By category
        for category, cat_skills in sorted(categorized.items()):
            st.markdown(f"<div class='section-header'>📂 {category}</div>", unsafe_allow_html=True)
            tags_html = "".join(
                f'<span class="skill-tag" title="Confidence: {skills[s][\"confidence\"]*100:.0f}%">'
                f'{s.title()} <span style="opacity:0.6">{skills[s]["confidence"]*100:.0f}%</span></span>'
                for s in cat_skills
                if s in skills
            )
            st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("---")

        # Confidence table
        st.markdown("**🎯 Skill Confidence Breakdown**")
        import pandas as pd
        skill_df = pd.DataFrame([
            {
                "Skill": k.title(),
                "Category": v["category"],
                "Confidence": f"{v['confidence']*100:.0f}%",
                "Demand Score": f"{v['demand_score']}/100",
                "Growth Rate": f"+{v['growth_rate']}% YoY",
            }
            for k, v in sorted(skills.items(), key=lambda x: x[1]["confidence"], reverse=True)
        ])
        st.dataframe(skill_df, use_container_width=True, hide_index=True)

# ── Sections Tab ──────────────────────────────────────────────────────────────
with tab2:
    col_sec, col_risk = st.columns([1, 1])
    with col_sec:
        st.markdown("**✅ Detected Sections**")
        for section in analysis["sections_found"]:
            st.markdown(f"• {section.title().replace('_', ' ')}")

        st.markdown("---")
        st.markdown("**📞 Contact Information**")
        contact = analysis.get("contact_info", {})
        if contact:
            for key, value in contact.items():
                st.markdown(f"• **{key.title()}:** `{value}`")
        else:
            st.warning("No contact info detected. Add email and LinkedIn URL.")

        if analysis.get("quantified_achievements"):
            st.markdown("---")
            st.markdown("**📊 Quantified Achievements Detected**")
            for qa in analysis["quantified_achievements"][:8]:
                st.markdown(f"""
                <div style="background:rgba(34,211,238,0.06);border:1px solid rgba(34,211,238,0.2);
                border-radius:8px;padding:8px 12px;margin:4px 0;font-size:0.85rem;color:#cbd5e1">
                    📌 {qa}
                </div>
                """, unsafe_allow_html=True)

    with col_risk:
        st.markdown("**⚠️ ATS Risk Factors**")
        if analysis["ats_risks"]:
            for risk in analysis["ats_risks"]:
                st.markdown(f"""
                <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);
                border-radius:8px;padding:8px 12px;margin:6px 0;color:#fca5a5;font-size:0.88rem">
                    ⚠️ {risk}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 No major ATS risks detected!")

        st.markdown("---")
        st.markdown("**📊 Section Checklist**")
        checks = {
            "Contact Info": analysis["has_contact"],
            "Professional Summary": analysis["has_summary"],
            "Work Experience": analysis["has_experience"],
            "Skills Section": analysis["has_skills"],
            "Education": analysis["has_education"],
        }
        for label, present in checks.items():
            icon = "✅" if present else "❌"
            color = "#22d3ee" if present else "#ef4444"
            st.markdown(f'<div style="color:{color};margin:4px 0">{icon} {label}</div>', unsafe_allow_html=True)

# ── Education Tab ─────────────────────────────────────────────────────────────
with tab3:
    edu = analysis.get("education_detected", [])
    if edu:
        st.markdown(f"**{len(edu)} education entries detected:**")
        for e in edu:
            st.markdown(f"""
            <div class="glass-card" style="margin:6px 0;padding:14px 16px">
                🎓 <span style="color:#e2e8f0">{e}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No education entries detected. Make sure your resume has a clear Education section.")

# ── Certifications Tab ────────────────────────────────────────────────────────
with tab4:
    certs = analysis.get("certifications_detected", [])
    if certs:
        st.markdown(f"**{len(certs)} certifications detected:**")
        for c in certs:
            st.markdown(f"""
            <div class="glass-card" style="margin:6px 0;padding:14px 16px">
                📜 <span style="color:#e2e8f0">{c}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No certifications detected. Adding relevant certifications can boost your ATS score by up to 5 points.")

# ── Raw Text Tab ──────────────────────────────────────────────────────────────
with tab5:
    st.markdown(f"**Extracted text ({len(resume_text)} chars, {analysis['word_count']} words):**")
    st.text_area("Resume Text", value=resume_text, height=400, disabled=True)

# ─── Next Step CTA ────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.25);border-radius:12px;padding:20px;text-align:center">
    <div style="font-size:1.05rem;font-weight:600;color:#e2e8f0">✅ Resume analyzed! Next step: Add a Job Description</div>
    <div style="color:#64748b;margin-top:6px;font-size:0.88rem">Navigate to <b>JD Analyzer</b> in the sidebar, then run <b>Skill Gap Analysis</b> for your full report.</div>
</div>
""", unsafe_allow_html=True)
