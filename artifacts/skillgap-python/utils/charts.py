"""
Plotly chart builders for the SkillGap AI dashboard.
All charts use a consistent dark theme.
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px

DARK_TEMPLATE = "plotly_dark"
PRIMARY = "#6366f1"
SUCCESS = "#22d3ee"
WARNING = "#f59e0b"
DANGER = "#ef4444"
ACCENT = "#a78bfa"
BG = "rgba(17,24,39,0)"
GRID = "rgba(255,255,255,0.06)"
TEXT = "#e2e8f0"

PALETTE = [PRIMARY, SUCCESS, WARNING, DANGER, ACCENT, "#10b981", "#f97316", "#ec4899"]


def skill_match_gauge(match_score: float, label: str = "Match Score") -> go.Figure:
    color = SUCCESS if match_score >= 70 else (WARNING if match_score >= 40 else DANGER)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=match_score,
        title={"text": label, "font": {"size": 18, "color": TEXT}},
        delta={"reference": 70, "increasing": {"color": SUCCESS}, "decreasing": {"color": DANGER}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": TEXT, "tickfont": {"color": TEXT}},
            "bar": {"color": color},
            "bgcolor": "rgba(255,255,255,0.05)",
            "bordercolor": "rgba(255,255,255,0.1)",
            "steps": [
                {"range": [0, 40], "color": "rgba(239,68,68,0.15)"},
                {"range": [40, 70], "color": "rgba(245,158,11,0.15)"},
                {"range": [70, 100], "color": "rgba(34,211,238,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#fff", "width": 2},
                "thickness": 0.75,
                "value": 70,
            },
        },
        number={"suffix": "%", "font": {"color": TEXT, "size": 36}},
    ))
    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=250,
        margin=dict(l=30, r=30, t=60, b=20),
        font={"color": TEXT},
    )
    return fig


def ats_gauge(ats_score: float) -> go.Figure:
    return skill_match_gauge(ats_score, "ATS Score")


def radar_chart(
    categories: list[str],
    resume_scores: list[float],
    jd_scores: list[float],
) -> go.Figure:
    cats = categories + [categories[0]]
    r_vals = resume_scores + [resume_scores[0]]
    j_vals = jd_scores + [jd_scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=j_vals, theta=cats, fill="toself",
        name="Job Requirements",
        fillcolor="rgba(99,102,241,0.15)",
        line=dict(color=PRIMARY, width=2),
    ))
    fig.add_trace(go.Scatterpolar(
        r=r_vals, theta=cats, fill="toself",
        name="Your Profile",
        fillcolor="rgba(34,211,238,0.15)",
        line=dict(color=SUCCESS, width=2),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont={"color": TEXT, "size": 10}, gridcolor=GRID),
            angularaxis=dict(tickfont={"color": TEXT, "size": 11}),
            bgcolor="rgba(255,255,255,0.03)",
        ),
        showlegend=True,
        legend=dict(font={"color": TEXT}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        height=400,
        margin=dict(l=60, r=60, t=40, b=40),
        font={"color": TEXT},
    )
    return fig


def skill_gap_heatmap(
    matched_skills: list[str],
    missing_skills: list[str],
    jd_skills: dict[str, dict],
) -> go.Figure:
    all_skills = matched_skills[:15] + missing_skills[:15]
    if not all_skills:
        return go.Figure()

    z_values = []
    hover_text = []
    for skill in all_skills:
        in_resume = 1 if skill in matched_skills else 0
        in_jd = 1 if skill in {**dict.fromkeys(matched_skills), **dict.fromkeys(missing_skills)} else 0
        demand = jd_skills.get(skill, {}).get("demand_score", 50)
        level = jd_skills.get(skill, {}).get("requirement_level", "preferred")
        z_values.append([in_resume * 100, in_jd * demand])
        hover_text.append([f"Resume: {'✓' if in_resume else '✗'}", f"JD: {level.capitalize()} | Demand: {demand}/100"])

    fig = go.Figure(go.Heatmap(
        z=z_values,
        x=["Resume Match", "JD Demand"],
        y=all_skills,
        colorscale=[[0, "rgba(239,68,68,0.3)"], [0.5, "rgba(245,158,11,0.5)"], [1, "rgba(99,102,241,0.8)"]],
        text=hover_text,
        hovertemplate="%{y}<br>%{x}: %{text}<extra></extra>",
        showscale=True,
        colorbar=dict(tickfont={"color": TEXT}, title=dict(text="Score", font={"color": TEXT})),
    ))
    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=max(400, len(all_skills) * 25),
        margin=dict(l=160, r=20, t=40, b=60),
        xaxis=dict(tickfont={"color": TEXT}),
        yaxis=dict(tickfont={"color": TEXT}, autorange="reversed"),
        font={"color": TEXT},
    )
    return fig


def missing_skills_bar(priority_skills: list[dict]) -> go.Figure:
    if not priority_skills:
        return go.Figure()

    skills = [p["skill"].title() for p in priority_skills]
    demand = [p["demand_score"] for p in priority_skills]
    colors = [DANGER if p["requirement_level"] == "required" else WARNING for p in priority_skills]
    hover = [
        f"<b>{p['skill'].title()}</b><br>Category: {p['category']}<br>Demand: {p['demand_score']}/100<br>"
        f"Growth: +{p['growth_rate']}% YoY<br>Requirement: {p['requirement_level'].capitalize()}<br>"
        f"Time to learn: {p['time_to_learn']}"
        for p in priority_skills
    ]

    fig = go.Figure(go.Bar(
        x=demand,
        y=skills,
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.1)", width=1)),
        hovertext=hover,
        hoverinfo="text",
    ))
    fig.update_layout(
        title=dict(text="Missing Skills — Priority Order", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=max(300, len(skills) * 38),
        xaxis=dict(title="Market Demand Score", range=[0, 100], tickfont={"color": TEXT}, gridcolor=GRID),
        yaxis=dict(tickfont={"color": TEXT}, autorange="reversed"),
        margin=dict(l=20, r=20, t=50, b=40),
        font={"color": TEXT},
    )
    return fig


def skills_category_pie(category_breakdown: dict) -> go.Figure:
    if not category_breakdown:
        return go.Figure()

    labels = list(category_breakdown.keys())
    values = [v["matched"] for v in category_breakdown.values()]
    totals = [v["total"] for v in category_breakdown.values()]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=PALETTE[:len(labels)], line=dict(color="rgba(0,0,0,0.3)", width=2)),
        textfont={"color": "#fff", "size": 11},
        hovertemplate="<b>%{label}</b><br>Matched: %{value}<br><extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Matched Skills by Category", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        showlegend=True,
        legend=dict(font={"color": TEXT}, orientation="v"),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        font={"color": TEXT},
        annotations=[dict(text="Skills", x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(color=TEXT))],
    )
    return fig


def salary_trend_line(salary_trends: list[dict]) -> go.Figure:
    fig = go.Figure()
    years = ["2020", "2021", "2022", "2023", "2024", "2025"]
    for i, role in enumerate(salary_trends):
        fig.add_trace(go.Scatter(
            x=years,
            y=[role.get(y, 0) for y in years],
            mode="lines+markers",
            name=role["role"],
            line=dict(color=PALETTE[i % len(PALETTE)], width=2),
            marker=dict(size=6),
            hovertemplate=f"<b>{role['role']}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text="Average Salary Trends by Role ($USD)", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=400,
        xaxis=dict(title="Year", tickfont={"color": TEXT}, gridcolor=GRID),
        yaxis=dict(title="Salary ($)", tickfont={"color": TEXT}, gridcolor=GRID, tickformat="$,.0f"),
        legend=dict(font={"color": TEXT}),
        margin=dict(l=60, r=20, t=50, b=50),
        font={"color": TEXT},
    )
    return fig


def job_postings_trend(postings: list[dict]) -> go.Figure:
    fig = go.Figure()
    skills_to_plot = ["python", "javascript", "aws", "kubernetes", "react"]
    months = [p["month"] for p in postings]

    for i, skill in enumerate(skills_to_plot):
        fig.add_trace(go.Scatter(
            x=months,
            y=[p.get(skill, 0) for p in postings],
            mode="lines+markers",
            name=skill.title(),
            line=dict(color=PALETTE[i % len(PALETTE)], width=2),
            marker=dict(size=5),
            hovertemplate=f"<b>{skill.title()}</b><br>%{{x}}: %{{y:,}} jobs<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text="Job Postings Trend (2024)", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=380,
        xaxis=dict(tickangle=-45, tickfont={"color": TEXT, "size": 10}, gridcolor=GRID),
        yaxis=dict(title="Job Postings", tickfont={"color": TEXT}, gridcolor=GRID, tickformat=","),
        legend=dict(font={"color": TEXT}),
        margin=dict(l=60, r=20, t=50, b=80),
        font={"color": TEXT},
    )
    return fig


def demand_bar_chart(skills_data: list[dict], title: str = "Skill Demand Scores") -> go.Figure:
    names = [s["skill"].title() for s in skills_data[:12]]
    scores = [s.get("demand_score", s.get("interest_score", 0)) for s in skills_data[:12]]
    growth = [s.get("growth_rate", s.get("growth", 0)) for s in skills_data[:12]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=scores,
        name="Demand Score",
        marker=dict(
            color=scores,
            colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#6366f1"]],
            showscale=False,
        ),
        hovertemplate="<b>%{x}</b><br>Demand: %{y}/100<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=380,
        xaxis=dict(tickangle=-35, tickfont={"color": TEXT, "size": 10}, gridcolor=GRID),
        yaxis=dict(title="Score /100", tickfont={"color": TEXT}, gridcolor=GRID, range=[0, 105]),
        margin=dict(l=40, r=20, t=50, b=100),
        font={"color": TEXT},
    )
    return fig


def industry_heatmap(industry_demand: dict) -> go.Figure:
    industries = list(industry_demand.keys())
    skills = list({s for d in industry_demand.values() for s in d.keys()})
    z = [[industry_demand[ind].get(skill, 0) for skill in skills] for ind in industries]

    fig = go.Figure(go.Heatmap(
        z=z,
        x=skills,
        y=industries,
        colorscale=[[0, "rgba(99,102,241,0.1)"], [0.5, "rgba(99,102,241,0.5)"], [1, "rgba(99,102,241,1.0)"]],
        hovertemplate="<b>%{y}</b> — %{x}<br>Demand: %{z}/100<extra></extra>",
        colorbar=dict(tickfont={"color": TEXT}, title=dict(text="Demand", font={"color": TEXT})),
    ))
    fig.update_layout(
        title=dict(text="Skill Demand by Industry", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=350,
        xaxis=dict(tickfont={"color": TEXT}, tickangle=-30),
        yaxis=dict(tickfont={"color": TEXT}),
        margin=dict(l=120, r=20, t=50, b=80),
        font={"color": TEXT},
    )
    return fig


def emerging_skills_bar(emerging: list[dict]) -> go.Figure:
    skills = [e["skill"] for e in emerging[:10]]
    growth = [e["growth"] for e in emerging[:10]]
    interest = [e["interest_score"] for e in emerging[:10]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Growth Rate (%)", x=skills, y=growth,
        marker_color=PRIMARY,
        hovertemplate="<b>%{x}</b><br>Growth: +%{y}% YoY<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name="Interest Score", x=skills, y=interest,
        mode="lines+markers",
        line=dict(color=SUCCESS, width=2),
        marker=dict(size=8),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Interest: %{y}/100<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Emerging Skills 2025 — Growth vs Interest", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=400,
        xaxis=dict(tickangle=-35, tickfont={"color": TEXT, "size": 9}, gridcolor=GRID),
        yaxis=dict(title="Growth Rate (%)", tickfont={"color": TEXT}, gridcolor=GRID),
        yaxis2=dict(title="Interest Score", tickfont={"color": TEXT}, overlaying="y", side="right", range=[0, 110]),
        legend=dict(font={"color": TEXT}),
        margin=dict(l=60, r=60, t=50, b=100),
        font={"color": TEXT},
        barmode="group",
    )
    return fig


def ats_breakdown_bar(ats_breakdown: dict) -> go.Figure:
    labels_map = {
        "keyword_match": "Keyword Match",
        "section_completeness": "Section Completeness",
        "quantified_achievements": "Quantified Achievements",
        "word_count": "Word Count",
        "contact_completeness": "Contact Info",
        "certifications": "Certifications",
    }
    items = [(labels_map.get(k, k), v) for k, v in ats_breakdown.items() if k != "total"]
    max_vals = {
        "keyword_match": 30, "section_completeness": 25,
        "quantified_achievements": 20, "word_count": 10,
        "contact_completeness": 10, "certifications": 5,
    }

    labels = [i[0] for i in items]
    scores = [i[1] for i in items]
    maxes = [max_vals.get(k, 10) for k in ats_breakdown if k != "total"]
    pcts = [min(100, s / max(m, 1) * 100) for s, m in zip(scores, maxes)]
    colors = [SUCCESS if p >= 70 else (WARNING if p >= 40 else DANGER) for p in pcts]

    fig = go.Figure(go.Bar(
        x=scores, y=labels, orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.05)", width=1)),
        text=[f"{s:.1f} / {m}" for s, m in zip(scores, maxes)],
        textposition="outside",
        textfont={"color": TEXT},
        hovertemplate="<b>%{y}</b><br>Score: %{x}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="ATS Score Breakdown", font={"color": TEXT, "size": 15}),
        template=DARK_TEMPLATE,
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=320,
        xaxis=dict(title="Points", tickfont={"color": TEXT}, gridcolor=GRID),
        yaxis=dict(tickfont={"color": TEXT}),
        margin=dict(l=20, r=80, t=50, b=40),
        font={"color": TEXT},
    )
    return fig
