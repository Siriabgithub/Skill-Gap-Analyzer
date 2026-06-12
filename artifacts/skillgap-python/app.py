"""
SkillGap AI — Intelligent Career Readiness Platform
Main dashboard entry point
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

st.set_page_config(
    page_title="SkillGap AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* === Base dark theme === */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(99, 102, 241, 0.2);
}
[data-testid="stHeader"] { background: transparent; }

/* === Glass cards === */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    margin-bottom: 16px;
}
.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
}

/* === Metric cards === */
.metric-card {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-value {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* === Feature card === */
.feature-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 20px;
    height: 160px;
    transition: all 0.25s ease;
    cursor: pointer;
}
.feature-card:hover {
    background: rgba(99, 102, 241, 0.08);
    border-color: rgba(99, 102, 241, 0.35);
    transform: translateY(-4px);
}
.feature-icon { font-size: 2rem; margin-bottom: 8px; }
.feature-title { font-size: 1rem; font-weight: 600; color: #e2e8f0; }
.feature-desc { font-size: 0.82rem; color: #64748b; margin-top: 6px; line-height: 1.5; }

/* === Hero section === */
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #a78bfa 40%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #94a3b8;
    margin-bottom: 32px;
    max-width: 600px;
}

/* === Badges === */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-purple { background: rgba(99,102,241,0.2); color: #a78bfa; border: 1px solid rgba(99,102,241,0.3); }
.badge-cyan   { background: rgba(34,211,238,0.15); color: #22d3ee; border: 1px solid rgba(34,211,238,0.3); }
.badge-green  { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-amber  { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }

/* === Sidebar nav === */
[data-testid="stSidebarNav"] a { border-radius: 8px; }
[data-testid="stSidebarNav"] a:hover { background: rgba(99,102,241,0.15) !important; }

/* === Progress bars === */
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }

/* === Buttons === */
.stButton button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton button:hover { opacity: 0.9; transform: translateY(-1px); box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important; }

/* === Dividers === */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* === Mobile responsive === */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .metric-value { font-size: 1.8rem; }
    .glass-card { padding: 16px; }
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px">
        <div style="font-size:2.2rem">🎯</div>
        <div style="font-size:1.1rem;font-weight:700;color:#e2e8f0">SkillGap AI</div>
        <div style="font-size:0.75rem;color:#6366f1;letter-spacing:1px">CAREER READINESS PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Session state overview
    has_resume = "resume_text" in st.session_state and bool(st.session_state.get("resume_text"))
    has_jd = "jd_text" in st.session_state and bool(st.session_state.get("jd_text"))
    has_analysis = "gap_result" in st.session_state

    st.markdown("**📋 Session Status**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"{'✅' if has_resume else '⬜'} Resume")
        st.markdown(f"{'✅' if has_analysis else '⬜'} Analysis")
    with col2:
        st.markdown(f"{'✅' if has_jd else '⬜'} Job Description")
        st.markdown(f"{'✅' if has_analysis else '⬜'} Roadmap")

    st.divider()

    if has_analysis:
        gap = st.session_state.gap_result
        st.markdown("**📊 Quick Stats**")
        st.metric("Match Score", f"{gap.match_score:.0f}%", delta=f"{gap.match_score - 50:.0f} vs avg")
        st.metric("ATS Score", f"{gap.ats_score:.0f}/100")
        st.metric("Missing Skills", len(gap.missing_skills))

        st.divider()

    st.markdown("""
    <div style="font-size:0.72rem;color:#475569;text-align:center;padding-top:8px">
        Powered by NLP · scikit-learn · Plotly<br>
        <span style="color:#6366f1">v2.0 · Python Edition</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ─── Hero ─────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-title">SkillGap AI 🎯</div>
<div class="hero-subtitle">
    AI-powered resume analysis, skill gap detection, ATS scoring, and personalized
    30/60/90-day learning roadmaps — all in one professional dashboard.
</div>
""", unsafe_allow_html=True)

# Tech stack badges
st.markdown("""
<span class="badge badge-purple">🐍 Python</span>
<span class="badge badge-cyan">📊 NLP</span>
<span class="badge badge-green">🤖 ML-Powered</span>
<span class="badge badge-amber">📈 Market Intelligence</span>
<span class="badge badge-purple">📄 PDF/DOCX</span>
<span class="badge badge-cyan">⚡ Real-time Analysis</span>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Metrics ─────────────────────────────────────────────────────────────────

m1, m2, m3, m4, m5 = st.columns(5)
metrics = [
    ("40+", "Skills Tracked"),
    ("NLP", "Extraction Engine"),
    ("6", "Analysis Modules"),
    ("90-Day", "Roadmap Generator"),
    ("100%", "Source Transparent"),
]
for col, (val, label) in zip([m1, m2, m3, m4, m5], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── How It Works ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="glass-card">
    <h3 style="color:#e2e8f0;margin-top:0">🚀 How It Works — 4 Simple Steps</h3>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:16px">
        <div style="text-align:center">
            <div style="font-size:2rem">📄</div>
            <div style="color:#6366f1;font-weight:700;margin:8px 0 4px">Step 1</div>
            <div style="color:#e2e8f0;font-weight:600;margin-bottom:4px">Upload Resume</div>
            <div style="color:#64748b;font-size:0.82rem">PDF, DOCX, or TXT — our NLP engine extracts your skills automatically</div>
        </div>
        <div style="text-align:center">
            <div style="font-size:2rem">💼</div>
            <div style="color:#a78bfa;font-weight:700;margin:8px 0 4px">Step 2</div>
            <div style="color:#e2e8f0;font-weight:600;margin-bottom:4px">Paste Job Description</div>
            <div style="color:#64748b;font-size:0.82rem">Paste any job description — we identify required and preferred skills</div>
        </div>
        <div style="text-align:center">
            <div style="font-size:2rem">🔍</div>
            <div style="color:#22d3ee;font-weight:700;margin:8px 0 4px">Step 3</div>
            <div style="color:#e2e8f0;font-weight:600;margin-bottom:4px">Analyze Gaps</div>
            <div style="color:#64748b;font-size:0.82rem">Get your match score, ATS score, missing skills, and strength areas</div>
        </div>
        <div style="text-align:center">
            <div style="font-size:2rem">🗺️</div>
            <div style="color:#10b981;font-weight:700;margin:8px 0 4px">Step 4</div>
            <div style="color:#e2e8f0;font-weight:600;margin-bottom:4px">Get Your Roadmap</div>
            <div style="color:#64748b;font-size:0.82rem">Receive a personalized 30/60/90-day learning plan with resources</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Feature Cards ────────────────────────────────────────────────────────────

st.markdown("### 🔧 Platform Modules")

features = [
    ("📄", "Resume Analyzer", "Upload PDF/DOCX. Extract skills, detect education, certifications, and quantified achievements.", "1_Resume_Analyzer"),
    ("💼", "JD Analyzer", "Paste or upload job descriptions. Identify required vs preferred skills automatically.", "2_JD_Analyzer"),
    ("🔍", "Skill Gap Analysis", "Compare resume vs JD. Get match score, ATS score, radar chart, and gap heatmap.", "3_Skill_Gap_Analysis"),
    ("🤖", "AI Recommendations", "Personalized skill recommendations with confidence scores and data provenance.", "4_Recommendations"),
    ("📈", "Market Insights", "Trending skills, salary data, job posting trends, and industry demand heatmaps.", "5_Market_Insights"),
    ("🔎", "Source Transparency", "Every recommendation with its source, confidence score, and full explanation.", "6_Source_Transparency"),
]

cols = st.columns(3)
for i, (icon, title, desc, page) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Quick Start CTA ─────────────────────────────────────────────────────────

if not (has_resume and has_jd):
    st.info("👈 **Get started** — Navigate to **Resume Analyzer** in the sidebar to upload your resume, or jump straight to **Skill Gap Analysis** if you already have results loaded.")
else:
    gap = st.session_state.get("gap_result")
    if gap:
        st.success(f"✅ Analysis complete! **Match Score: {gap.match_score:.0f}%** | **ATS Score: {gap.ats_score:.0f}/100** | Navigate to any module to explore your results.")
    else:
        st.info("✅ Resume and JD loaded! Navigate to **Skill Gap Analysis** to run your full analysis.")

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<hr>
<div style="text-align:center;color:#475569;font-size:0.8rem;padding:8px 0">
    SkillGap AI v2.0 — Python Edition &nbsp;·&nbsp; Built with Streamlit, scikit-learn, Plotly &nbsp;·&nbsp;
    <span style="color:#6366f1">Portfolio-ready · Deploy-ready</span>
</div>
""", unsafe_allow_html=True)
