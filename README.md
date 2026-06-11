# SkillGap AI

> Intelligent Career Readiness Platform — analyze resumes against job descriptions, detect skill gaps, generate ATS scores, and create personalized 30/60/90-day learning roadmaps.

![Node.js](https://img.shields.io/badge/Node.js-24-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Resume Upload** — drag-and-drop PDF or DOCX, automatic skill extraction via NLP pattern matching
- **Skill Gap Analysis** — compare your resume skills against any job description; 40+ skills tracked with market demand scores
- **ATS Scoring** — keyword overlap, section completeness, quantified achievements, contact info checks
- **Learning Roadmap** — personalized 30/60/90-day plan with curated resources (Coursera, freeCodeCamp, official docs)
- **Market Trends** — trending and emerging skills with demand scores and growth rates
- **Source Transparency** — confidence scores and data provenance for every recommendation
- **Dark-mode Dashboard** — command center with charts (Recharts), radar plots, and animated metrics

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React 18, Vite 7, Tailwind CSS, shadcn/ui, Framer Motion, Recharts |
| API | Express 5, TypeScript, Zod validation, Orval codegen |
| Database | PostgreSQL 16 + Drizzle ORM |
| File Parsing | pdf-parse (PDF), mammoth (DOCX), multer (upload) |
| Build | esbuild (API), Vite (frontend), pnpm workspaces |

---

## Prerequisites

- **Node.js** ≥ 24
- **pnpm** ≥ 10 — install with `npm install -g pnpm`
- **PostgreSQL** ≥ 14 — a running instance with a database created

---

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/skillgap-ai.git
cd skillgap-ai
```

### 2. Install dependencies

```bash
pnpm install
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/skillgap
SESSION_SECRET=your-random-secret-here
NODE_ENV=development
```

### 4. Run database migrations

```bash
pnpm --filter @workspace/db run push
```

### 5. Start the development servers

Open **two terminals**:

```bash
# Terminal 1 — API server (port 8080)
PORT=8080 pnpm --filter @workspace/api-server run dev

# Terminal 2 — Frontend (port 3000)
PORT=3000 BASE_PATH=/ pnpm --filter @workspace/skillgap-ai run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Production Build

Build everything into a single deployable bundle:

```bash
# Set environment
export DATABASE_URL="postgresql://..."
export SESSION_SECRET="your-secret"

# Build frontend then API
BASE_PATH=/ PORT=3000 pnpm --filter @workspace/skillgap-ai run build
pnpm --filter @workspace/api-server run build

# Start the production server (serves API + frontend)
PORT=8080 NODE_ENV=production node --enable-source-maps ./artifacts/api-server/dist/index.mjs
```

Visit [http://localhost:8080](http://localhost:8080).

---

## Deploying to Render

### One-click setup using `render.yaml`

This repo includes a `render.yaml` that provisions everything automatically.

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your GitHub repo
4. Render detects `render.yaml` and creates the services
5. Set the required environment variables in the Render dashboard:
   - `DATABASE_URL` — provided automatically by Render PostgreSQL
   - `SESSION_SECRET` — generate with `openssl rand -hex 32`

### Manual setup on Render

#### Step 1 — Create a PostgreSQL database

- Dashboard → **New** → **PostgreSQL**
- Copy the **Internal Database URL**

#### Step 2 — Create a Web Service

| Setting | Value |
|---|---|
| Runtime | Node |
| Build Command | `npm install -g pnpm && pnpm install && BASE_PATH=/ PORT=3000 pnpm --filter @workspace/skillgap-ai run build && pnpm --filter @workspace/api-server run build` |
| Start Command | `node --enable-source-maps ./artifacts/api-server/dist/index.mjs` |
| Node Version | 24 |

#### Step 3 — Set environment variables

| Variable | Value |
|---|---|
| `NODE_ENV` | `production` |
| `PORT` | `10000` *(Render sets this automatically)* |
| `DATABASE_URL` | *(Internal URL from Step 1)* |
| `SESSION_SECRET` | *(random 32-byte hex string)* |

#### Step 4 — Run database migrations

After first deploy, open the **Shell** tab in Render and run:

```bash
pnpm --filter @workspace/db run push
```

---

## Project Structure

```
skillgap-ai/
├── artifacts/
│   ├── api-server/          # Express API server
│   │   ├── src/
│   │   │   ├── lib/         # analysis-engine, file-parser, skills-database, roadmap-generator
│   │   │   ├── routes/      # resumes, analyses, dashboard, market, health
│   │   │   ├── app.ts       # Express app (with production static serving)
│   │   │   └── index.ts     # Server entry point
│   │   ├── uploads/         # Uploaded resume files (gitignored)
│   │   └── build.mjs        # esbuild config
│   └── skillgap-ai/         # React + Vite frontend
│       └── src/
│           ├── pages/       # landing, upload, dashboard, analysis-detail, roadmap, market, sources
│           └── components/  # UI components
├── lib/
│   ├── api-spec/            # OpenAPI spec (source of truth for codegen)
│   ├── api-client-react/    # Generated React Query hooks
│   ├── api-zod/             # Generated Zod schemas
│   └── db/                  # Drizzle ORM schema + migrations
├── .env.example             # Environment variable template
├── render.yaml              # Render deployment blueprint
└── pnpm-workspace.yaml      # pnpm workspace config
```

---

## Available Scripts

```bash
# Install all dependencies
pnpm install

# Run full typecheck
pnpm run typecheck

# Regenerate API client from OpenAPI spec
pnpm --filter @workspace/api-spec run codegen

# Push DB schema changes (dev only)
pnpm --filter @workspace/db run push

# Build everything
pnpm run build
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `SESSION_SECRET` | ✅ | Secret for session signing (32+ chars) |
| `NODE_ENV` | ✅ | `development` or `production` |
| `PORT` | ✅ | Port for the API server (Render sets this automatically) |

---

## Troubleshooting

**"PORT environment variable is required"**
→ Make sure `PORT` is set before starting. Example: `PORT=8080 node ...`

**"DATABASE_URL is not set"**
→ Copy `.env.example` to `.env` and fill in your PostgreSQL connection string.

**Resume stays "processing" forever**
→ Check the API server logs. PDF files must be valid; password-protected PDFs are not supported.

**DOCX upload fails**
→ Ensure the file is a proper `.docx` (not `.doc`). Legacy Word format is not supported.

**pnpm not found after clone**
→ Run `npm install -g pnpm` then retry.

**Build fails with "BASE_PATH is required"**
→ Set `BASE_PATH=/` before running the Vite build: `BASE_PATH=/ PORT=3000 pnpm --filter @workspace/skillgap-ai run build`

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/healthz` | Health check |
| POST | `/api/resumes/upload` | Upload PDF/DOCX resume |
| GET | `/api/resumes/:id` | Get resume status + extracted skills |
| POST | `/api/analyses` | Create skill gap analysis |
| GET | `/api/analyses/:id` | Get full analysis results |
| GET | `/api/analyses/:id/roadmap` | Get 30/60/90-day roadmap |
| GET | `/api/analyses/:id/sources` | Get data source transparency |
| GET | `/api/market-trends` | Get trending skills + demand scores |
| GET | `/api/dashboard/stats` | Get dashboard aggregate stats |

Full OpenAPI spec: [`lib/api-spec/openapi.yaml`](lib/api-spec/openapi.yaml)

---

## License

MIT
