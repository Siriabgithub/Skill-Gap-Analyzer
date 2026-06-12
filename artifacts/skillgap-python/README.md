# SkillGap AI — Python Edition 🎯

> AI-Powered Resume and Skill Gap Analyzer built with Python and Streamlit.
> No Node.js. No React. No pnpm. Pure Python.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

| Module | Description |
|---|---|
| 📄 Resume Analyzer | Upload PDF/DOCX/TXT — NLP extracts skills, education, certifications, quantified achievements |
| 💼 JD Analyzer | Paste or upload job descriptions — classify required vs preferred skills |
| 🔍 Skill Gap Analysis | Match score, ATS score, semantic score, radar chart, gap heatmap |
| 🤖 AI Recommendations | Personalized 30/60/90-day learning roadmap with curated resources |
| 📈 Market Insights | Trending skills, salary trends, job posting data, industry heatmaps |
| 🔎 Source Transparency | Full data provenance — confidence scores and evidence for every result |

---

## Tech Stack

- **Python 3.11** — primary language
- **Streamlit** — interactive web UI
- **Plotly** — interactive charts and visualizations
- **scikit-learn** — TF-IDF similarity scoring
- **pdfplumber / PyPDF2** — PDF text extraction
- **python-docx** — DOCX parsing
- **pandas / numpy** — data manipulation

---

## Local Setup

### Prerequisites
- Python 3.11+
- pip or conda

### Install

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/skillgap-ai-python.git
cd skillgap-ai-python

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
skillgap-python/
├── app.py                    # Main dashboard (entry point)
├── requirements.txt
├── runtime.txt               # Python version for Render
├── Procfile                  # Render/Heroku start command
├── .streamlit/
│   └── config.toml           # Streamlit dark theme config
├── pages/
│   ├── 1_Resume_Analyzer.py
│   ├── 2_JD_Analyzer.py
│   ├── 3_Skill_Gap_Analysis.py
│   ├── 4_Recommendations.py
│   ├── 5_Market_Insights.py
│   └── 6_Source_Transparency.py
├── utils/
│   ├── resume_parser.py      # PDF/DOCX/TXT text extraction
│   ├── skill_extractor.py    # NLP skill extraction
│   ├── gap_analyzer.py       # Gap analysis + ATS scoring
│   ├── recommender.py        # Roadmap + recommendations
│   ├── market_data.py        # Market intelligence data
│   └── charts.py             # Plotly chart builders
├── data/
│   └── skills_db.py          # 40+ skills with demand scores, aliases, resources
├── uploads/                  # Temporary file uploads (gitignored)
└── exports/                  # Generated reports (gitignored)
```

---

## Deploy to Render

### One-click via render.yaml

Push this directory to GitHub, then on [render.com](https://render.com):

1. **New** → **Web Service**
2. Connect your GitHub repo
3. Render auto-detects the Procfile

### Manual setup

| Setting | Value |
|---|---|
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0` |

No environment variables required for basic usage.

---

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → select `app.py` as the main file
4. Deploy — free tier available!

---

## Deploy to Railway

```bash
railway init
railway up
```

Railway auto-detects `Procfile` and `requirements.txt`.

---

## How It Works

### Skill Extraction (NLP)
- 40+ curated skills with canonical names and aliases
- Regex whole-word matching: `(?<![a-z-])term(?![a-z-])`
- Confidence = `min(1.0, 0.6 + 0.1 × log(1 + count))`
- Exact name match → +0.15 confidence bonus

### Gap Analysis
- **Match Score** = weighted skill overlap (required ×2, preferred ×1)
- **Semantic Score** = TF-IDF cosine similarity (resume vs JD full text)
- **ATS Score** = composite: keywords (30) + sections (25) + achievements (20) + word count (10) + contact (10) + certifications (5)
- **Combined Score** = Match×0.50 + Semantic×0.25 + ATS×0.25

### Roadmap Generation
- Skills ranked by `priority_score = demand_score × requirement_weight`
- Split into 30/60/90 day phases by priority tier
- Each skill includes curated learning resources, estimated time, and related skills

---

## Portfolio Value

This project demonstrates:
- **NLP Engineering**: text extraction, keyword matching, semantic similarity
- **Data Science**: scoring algorithms, TF-IDF, pandas/numpy
- **Data Visualization**: Plotly interactive charts, Streamlit dashboards
- **Software Architecture**: modular Python, separation of concerns
- **Production-readiness**: multi-platform deployment, error handling

---

## License

MIT
