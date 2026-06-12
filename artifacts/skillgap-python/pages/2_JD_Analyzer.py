"""
Module 2: Job Description Analyzer
Paste or upload a JD; extract required/preferred skills.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="JD Analyzer · SkillGap AI", page_icon="💼", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15,23,42,0.95); border-right:1px solid rgba(99,102,241,0.2); }
.glass-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:14px; }
.required-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;
                background:rgba(239,68,68,0.12); color:#fca5a5; border:1px solid rgba(239,68,68,0.25); }
.preferred-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin:3px;
                 background:rgba(245,158,11,0.12); color:#fcd34d; border:1px solid rgba(245,158,11,0.25); }
.stButton button { background:linear-gradient(135deg,#6366f1,#4f46e5)!important; color:white!important; border:none!important; border-radius:8px!important; font-weight:600!important; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }
</style>
""", unsafe_allow_html=True)

from utils.resume_parser import parse_file
from utils.skill_extractor import extract_skills_from_jd, get_skill_categories
import pandas as pd

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 💼 Job Description Analyzer")
st.markdown("<p style='color:#94a3b8;margin-bottom:24px'>Paste or upload a job description. Our NLP engine classifies skills as required vs preferred and maps them to market demand data.</p>", unsafe_allow_html=True)

# ─── Input Options ────────────────────────────────────────────────────────────

tab_paste, tab_upload, tab_sample = st.tabs(["✍️ Paste JD", "📎 Upload JD File", "📋 Use Sample JD"])

with tab_paste:
    jd_input = st.text_area(
        "Paste your job description here",
        height=320,
        placeholder="""Example:
We are looking for a Senior Data Scientist to join our team.

Requirements:
- 3+ years of experience with Python and machine learning
- Strong knowledge of scikit-learn, pandas, and numpy
- Experience with SQL and PostgreSQL databases
- Familiarity with Docker and AWS

Nice to have:
- Experience with deep learning frameworks (PyTorch, TensorFlow)
- Knowledge of Apache Spark and Airflow
- MLOps experience with MLflow or Kubeflow
""",
    )
    if st.button("🔍 Analyze Job Description", use_container_width=True):
        if jd_input.strip():
            st.session_state["jd_text"] = jd_input
            st.session_state["jd_source"] = "pasted text"
        else:
            st.warning("Please paste a job description.")

with tab_upload:
    jd_file = st.file_uploader("Upload JD (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    if jd_file:
        with st.spinner("Parsing JD file..."):
            jd_text_from_file, err = parse_file(jd_file)
        if err:
            st.error(f"❌ {err}")
        else:
            st.session_state["jd_text"] = jd_text_from_file
            st.session_state["jd_source"] = jd_file.name
            st.success(f"✅ Parsed {jd_file.name}")

with tab_sample:
    sample_jds = {
        "Senior Data Scientist": """
We are seeking a Senior Data Scientist with strong Python and machine learning skills.

Required Qualifications:
- 4+ years of experience in data science
- Proficiency in Python (pandas, numpy, scikit-learn)
- Strong knowledge of machine learning algorithms
- Experience with SQL and PostgreSQL
- Familiarity with AWS cloud services
- Experience with Docker and containerization
- Strong statistics and probability knowledge

Preferred Qualifications:
- Experience with deep learning (PyTorch or TensorFlow)
- Knowledge of Apache Spark and big data processing
- MLOps experience (MLflow, Kubeflow, or similar)
- Natural language processing (NLP) experience
- Familiarity with Airflow for pipeline orchestration

Responsibilities:
- Build and deploy machine learning models at scale
- Collaborate with engineering teams using Git and CI/CD
- Communicate findings to stakeholders
""",
        "DevOps Engineer": """
We are hiring a DevOps Engineer to scale our cloud infrastructure.

Requirements:
- 3+ years of DevOps or SRE experience
- Expert knowledge of Docker and Kubernetes
- Strong experience with AWS (EC2, S3, Lambda, EKS)
- Proficiency with Terraform or Ansible for IaC
- CI/CD pipeline experience (GitHub Actions, Jenkins)
- Linux/Bash scripting expertise
- Git version control proficiency

Nice to have:
- GCP or Azure experience
- Monitoring tools (Prometheus, Grafana)
- Python scripting for automation
- Experience with Helm charts
- Security certifications (CKA, AWS)
""",
        "Full Stack Engineer": """
Looking for a Full Stack Engineer to build our web platform.

Required Skills:
- 3+ years building web applications
- Strong JavaScript/TypeScript experience
- React or Next.js proficiency
- Node.js or Python backend experience
- PostgreSQL or MongoDB database experience
- REST API design and development
- Git and GitHub workflow

Good to have:
- Docker containerization
- AWS or GCP cloud experience
- GraphQL API experience
- CI/CD pipeline experience
- Agile/Scrum methodology
""",
    }
    selected = st.selectbox("Choose a sample job description:", list(sample_jds.keys()))
    if st.button("📋 Load Sample JD", use_container_width=True):
        st.session_state["jd_text"] = sample_jds[selected]
        st.session_state["jd_source"] = f"Sample: {selected}"
        st.session_state["jd_title"] = selected
        st.rerun()

# ─── Job title ────────────────────────────────────────────────────────────────

jd_text = st.session_state.get("jd_text", "")

if not jd_text:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:48px;text-align:center">
        <div style="font-size:3rem">💼</div>
        <div style="font-size:1.1rem;color:#e2e8f0;font-weight:600;margin-top:12px">Paste or Upload a Job Description</div>
        <div style="color:#64748b;margin-top:8px;font-size:0.9rem">Use one of the tabs above to get started</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Source banner ────────────────────────────────────────────────────────────

source = st.session_state.get("jd_source", "input")
st.success(f"✅ Job description loaded from **{source}** — {len(jd_text.split())} words")

col_title, col_clear = st.columns([3, 1])
with col_title:
    job_title = st.text_input(
        "Job Title (optional)",
        value=st.session_state.get("jd_title", ""),
        placeholder="e.g. Senior Data Scientist",
    )
    if job_title:
        st.session_state["jd_title"] = job_title

with col_clear:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear JD", use_container_width=True):
        for key in ["jd_text", "jd_source", "jd_title", "jd_skills"]:
            st.session_state.pop(key, None)
        st.rerun()

# ─── Analysis ─────────────────────────────────────────────────────────────────

with st.spinner("🤖 Analyzing job description..."):
    jd_skills = extract_skills_from_jd(jd_text)
    categorized = get_skill_categories(list(jd_skills.keys()))

st.session_state["jd_skills"] = jd_skills

required = {k: v for k, v in jd_skills.items() if v.get("requirement_level") == "required"}
preferred = {k: v for k, v in jd_skills.items() if v.get("requirement_level") != "required"}

# ─── Metrics ─────────────────────────────────────────────────────────────────

st.markdown("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔧 Total Skills Found", len(jd_skills))
m2.metric("🔴 Required Skills", len(required))
m3.metric("🟡 Preferred Skills", len(preferred))
m4.metric("📂 Categories", len(categorized))

# ─── Skills display ───────────────────────────────────────────────────────────

st.markdown("---")
col_req, col_pref = st.columns(2)

with col_req:
    st.markdown("### 🔴 Required Skills")
    st.caption("Must-have skills explicitly stated in the job description")
    if required:
        tags = "".join(
            f'<span class="required-tag">{k.title()}</span>'
            for k in sorted(required.keys())
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.info("No explicitly required skills classified. All skills treated as preferred.")

with col_pref:
    st.markdown("### 🟡 Preferred Skills")
    st.caption("Nice-to-have or bonus skills mentioned in the description")
    if preferred:
        tags = "".join(
            f'<span class="preferred-tag">{k.title()}</span>'
            for k in sorted(preferred.keys())
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.info("No preferred skills detected separately.")

# ─── Full Skills Table ────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### 📊 Full Skills Analysis")

df = pd.DataFrame([
    {
        "Skill": k.title(),
        "Category": v["category"],
        "Requirement": "🔴 Required" if v.get("requirement_level") == "required" else "🟡 Preferred",
        "Confidence": f"{v['confidence']*100:.0f}%",
        "Market Demand": f"{v['demand_score']}/100",
        "Growth Rate": f"+{v['growth_rate']}% YoY",
    }
    for k, v in sorted(jd_skills.items(), key=lambda x: (x[1].get("requirement_level", "z"), -x[1]["confidence"]))
])

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)

# ─── By category ─────────────────────────────────────────────────────────────

if categorized:
    st.markdown("---")
    st.markdown("### 📂 Skills by Category")
    for cat, cat_skills in sorted(categorized.items()):
        with st.expander(f"📂 {cat} ({len(cat_skills)} skills)"):
            for skill in cat_skills:
                data = jd_skills.get(skill, {})
                level = data.get("requirement_level", "preferred")
                level_badge = "🔴 Required" if level == "required" else "🟡 Preferred"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                    <span style="color:#e2e8f0">{skill.title()}</span>
                    <span style="color:#94a3b8;font-size:0.82rem">{level_badge} · Demand: {data.get('demand_score',0)}/100 · Confidence: {data.get('confidence',0)*100:.0f}%</span>
                </div>
                """, unsafe_allow_html=True)

# ─── Raw JD ───────────────────────────────────────────────────────────────────

with st.expander("📄 View Raw Job Description"):
    st.text_area("Job Description", value=jd_text, height=300, disabled=True)

# ─── Next step ────────────────────────────────────────────────────────────────

st.markdown("---")
has_resume = bool(st.session_state.get("resume_text"))
if has_resume:
    st.markdown("""
    <div style="background:rgba(34,211,238,0.07);border:1px solid rgba(34,211,238,0.25);border-radius:12px;padding:20px;text-align:center">
        <div style="font-size:1.05rem;font-weight:600;color:#e2e8f0">✅ Both resume and JD are loaded!</div>
        <div style="color:#64748b;margin-top:6px;font-size:0.88rem">Navigate to <b>Skill Gap Analysis</b> to see your full report, match score, and roadmap.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("⬅️ Next step: Go to **Resume Analyzer** to upload your resume, then run **Skill Gap Analysis**.")
