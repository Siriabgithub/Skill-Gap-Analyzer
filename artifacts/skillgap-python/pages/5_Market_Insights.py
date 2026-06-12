"""
Module 5: Market Insights Dashboard
Trending skills, salary data, job postings, industry demand heatmaps.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="Market Insights · SkillGap AI", page_icon="📈", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15,23,42,0.95); border-right:1px solid rgba(99,102,241,0.2); }
.glass-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px; margin-bottom:14px; }
.trend-item { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.stButton button { background:linear-gradient(135deg,#6366f1,#4f46e5)!important; color:white!important; border:none!important; border-radius:8px!important; font-weight:600!important; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #22d3ee) !important; }
</style>
""", unsafe_allow_html=True)

from utils.market_data import get_market_overview, TOP_TOOLS_2025, SKILLS_BY_EXPERIENCE, REMOTE_WORK_STATS, COMPANY_SIZE_DEMAND
from utils.charts import salary_trend_line, job_postings_trend, demand_bar_chart, industry_heatmap, emerging_skills_bar
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

DARK_BG = "rgba(17,24,39,0)"

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 📈 Market Intelligence Dashboard")
st.markdown("<p style='color:#94a3b8;margin-bottom:24px'>Real-time market intelligence: trending skills, salary benchmarks, job posting trends, and industry-specific demand data for 2024–2025.</p>", unsafe_allow_html=True)

market = get_market_overview()

# ─── Top KPIs ─────────────────────────────────────────────────────────────────

k1, k2, k3, k4 = st.columns(4)
k1.metric("🔥 Fastest Growing", "Prompt Engineering", "+150% YoY")
k2.metric("💰 Highest Avg Salary", "AI/LLM Engineer", "$195k (2025)")
k3.metric("🏆 Most In-Demand", "Python", "95/100 demand")
k4.metric("⭐ Emerging #1", "AI Agents", "+250% interest")

st.markdown("---")

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔥 Trending Skills", "💰 Salaries", "📊 Job Postings", "🏭 Industry Demand", "🚀 Emerging 2025", "🛠️ Top Tools"
])

# ─── Trending Skills ─────────────────────────────────────────────────────────
with tab1:
    col_chart, col_list = st.columns([2, 1])

    with col_chart:
        trending = market["trending_skills"]
        st.plotly_chart(demand_bar_chart(trending, "🔥 Top 12 Fastest-Growing Skills"), use_container_width=True)

    with col_list:
        st.markdown("#### 🏆 Top Skills by Demand")
        high_demand = market["high_demand_skills"][:10]
        for i, skill in enumerate(high_demand, 1):
            demand_pct = skill["demand_score"] / 100
            color = "#22d3ee" if demand_pct >= 0.9 else ("#6366f1" if demand_pct >= 0.8 else "#f59e0b")
            st.markdown(f"""
            <div class="trend-item">
                <div>
                    <span style="color:#64748b;font-size:0.78rem">#{i}</span>
                    <span style="color:#e2e8f0;font-weight:600;margin-left:8px">{skill['skill'].title()}</span>
                    <div style="font-size:0.75rem;color:#64748b;margin-left:16px">{skill.get('category','')}</div>
                </div>
                <span style="color:{color};font-weight:700">{skill['demand_score']}</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(demand_pct)

    st.markdown("---")

    # AI/ML specific
    st.markdown("#### 🤖 AI & Machine Learning Skill Demand")
    ai_data = [{"skill": k, "demand_score": v, "growth_rate": 0, "category": "AI/ML"} for k, v in market["ai_ml_demand"].items()]
    st.plotly_chart(demand_bar_chart(ai_data, "AI/ML Skill Demand Scores"), use_container_width=True)

# ─── Salaries ─────────────────────────────────────────────────────────────────
with tab2:
    st.plotly_chart(salary_trend_line(market["salary_trends"]), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💵 2025 Salary Benchmarks")

    salary_data = [
        {
            "Role": s["role"],
            "2023 Avg": f"${s['2023']:,.0f}",
            "2024 Avg": f"${s['2024']:,.0f}",
            "2025 Projected": f"${s['2025']:,.0f}",
            "YoY Growth": f"+{((s['2025']-s['2024'])/s['2024']*100):.0f}%",
        }
        for s in market["salary_trends"]
    ]
    df_salaries = pd.DataFrame(salary_data)
    st.dataframe(df_salaries, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🏠 Remote Work Split (Tech Industry, 2024)")
    col_donut, col_remote = st.columns([1, 1])
    with col_donut:
        fig = go.Figure(go.Pie(
            labels=list(REMOTE_WORK_STATS.keys()),
            values=list(REMOTE_WORK_STATS.values()),
            hole=0.55,
            marker=dict(colors=["#6366f1", "#22d3ee", "#f59e0b"]),
        ))
        fig.update_layout(
            template="plotly_dark", paper_bgcolor=DARK_BG, height=280,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[dict(text="Work Mode", x=0.5, y=0.5, font_size=13, showarrow=False)],
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_remote:
        for mode, pct in REMOTE_WORK_STATS.items():
            st.markdown(f"**{mode}:** {pct}%")
            st.progress(pct / 100)

# ─── Job Postings ─────────────────────────────────────────────────────────────
with tab3:
    st.plotly_chart(job_postings_trend(market["job_postings_trend"]), use_container_width=True)

    st.markdown("---")
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.markdown("#### 📊 Skills by Experience Level")
        for level, skills_list in SKILLS_BY_EXPERIENCE.items():
            with st.expander(f"**{level}**"):
                tags = " · ".join(f"`{s}`" for s in skills_list)
                st.markdown(tags)

    with col_j2:
        st.markdown("#### 🏢 Demand by Company Size")
        for size, skill_demands in COMPANY_SIZE_DEMAND.items():
            with st.expander(f"**{size}**"):
                for skill, demand in sorted(skill_demands.items(), key=lambda x: -x[1]):
                    col_s, col_d = st.columns([3, 1])
                    col_s.markdown(f"• {skill.title()}")
                    col_d.markdown(f"**{demand}/100**")
                    st.progress(demand / 100)

# ─── Industry Demand ──────────────────────────────────────────────────────────
with tab4:
    st.plotly_chart(industry_heatmap(market["industry_demand"]), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🏭 Industry Demand Breakdown")
    for industry, skill_dict in market["industry_demand"].items():
        with st.expander(f"**{industry}**"):
            df_ind = pd.DataFrame([
                {"Skill": k.title(), "Demand Score": v}
                for k, v in sorted(skill_dict.items(), key=lambda x: -x[1])
            ])
            for _, row in df_ind.iterrows():
                c1, c2, c3 = st.columns([2, 1, 3])
                c1.markdown(row["Skill"])
                c2.markdown(f"**{row['Demand Score']}/100**")
                c3.progress(row["Demand Score"] / 100)

# ─── Emerging Skills ──────────────────────────────────────────────────────────
with tab5:
    st.plotly_chart(emerging_skills_bar(market["emerging_skills"]), use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🚀 Emerging Skills to Watch in 2025")
    for i, skill in enumerate(market["emerging_skills"], 1):
        interest = skill["interest_score"]
        growth = skill["growth"]
        color = "#22d3ee" if interest >= 90 else ("#6366f1" if interest >= 80 else "#f59e0b")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px;margin:6px 0;display:flex;justify-content:space-between;align-items:center">
            <div>
                <span style="color:#64748b;font-size:0.78rem">#{i}</span>
                <span style="font-weight:600;color:#e2e8f0;margin-left:8px">{skill['skill']}</span>
            </div>
            <div style="text-align:right">
                <span style="color:{color};font-weight:700;font-size:1.1rem">+{growth}%</span>
                <div style="font-size:0.75rem;color:#64748b">YoY Growth · Interest: {interest}/100</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Top Tools ────────────────────────────────────────────────────────────────
with tab6:
    st.markdown("#### 🛠️ Most-Used Developer Tools & Technologies (2025 Survey)")

    tools_df = pd.DataFrame(TOP_TOOLS_2025)
    categories = tools_df["category"].unique().tolist()

    for cat in sorted(categories):
        cat_tools = tools_df[tools_df["category"] == cat].sort_values("usage_pct", ascending=False)
        st.markdown(f"**📂 {cat}**")
        for _, row in cat_tools.iterrows():
            c1, c2, c3 = st.columns([3, 1, 4])
            c1.markdown(f"• **{row['tool']}**")
            c2.markdown(f"{row['usage_pct']}%")
            c3.progress(row["usage_pct"] / 100)

    st.markdown("---")
    st.markdown("#### 🏅 Top Certifications by ROI")
    for cert in market["top_certifications"]:
        demand_pct = cert["demand"] / 100
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.2);border-radius:10px;padding:12px;margin:4px 0;display:flex;justify-content:space-between;align-items:center">
            <div>
                <span style="font-weight:600;color:#e2e8f0">{cert['name']}</span>
                <span style="color:#64748b;font-size:0.82rem;margin-left:8px">by {cert['provider']}</span>
            </div>
            <div style="text-align:right">
                <span style="color:#10b981;font-weight:700">{cert['salary_boost']}</span>
                <div style="font-size:0.75rem;color:#6366f1">Demand: {cert['demand']}/100</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
