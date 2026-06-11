# SkillGap AI – Intelligent Career Readiness Platform

A full-stack SaaS-style platform that analyzes resumes against job descriptions, detects skill gaps using NLP pattern matching, generates ATS scores, creates personalized 30/60/90-day learning roadmaps, and provides complete source transparency — all through an interactive dark-mode dashboard.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 8080)
- `pnpm --filter @workspace/skillgap-ai run dev` — run the frontend (port 20490)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Frontend: React + Vite, Tailwind CSS, shadcn/ui, Recharts, Framer Motion, next-themes
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- File parsing: `pdf-parse` (PDF), `mammoth` (DOCX), `multer` (upload)
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `lib/api-spec/openapi.yaml` — API contract (source of truth)
- `lib/db/src/schema/resumes.ts` — resumes table + types
- `lib/db/src/schema/analyses.ts` — analyses table + types
- `artifacts/api-server/src/lib/skills-database.ts` — 40+ skills with NLP patterns and market data
- `artifacts/api-server/src/lib/analysis-engine.ts` — skill gap analysis + ATS scoring logic
- `artifacts/api-server/src/lib/roadmap-generator.ts` — 30/60/90 day learning roadmap generator
- `artifacts/api-server/src/lib/file-parser.ts` — PDF/DOCX parsing
- `artifacts/api-server/uploads/` — uploaded resume files
- `artifacts/skillgap-ai/src/` — React frontend

## Architecture decisions

- Contract-first: OpenAPI spec gates codegen which gates frontend hooks — never hand-write API types
- NLP skill extraction uses keyword + alias pattern matching against a curated 40-skill database with market demand scores
- ATS scoring is computed from keyword overlap, section completeness, quantified achievements, and skill match ratio
- Resume parsing happens async after 201 response — client polls `GET /resumes/:id` for `status: "ready"`
- All roadmap and source data is generated server-side per analysis, not stored separately
- `lib/api-zod/tsconfig.json` includes `"dom"` lib to support `File`/`Blob` types from Orval's multipart generation

## Product

- **Landing page** — hero, features, how-it-works, animated sections
- **Resume upload** — drag-and-drop PDF/DOCX, job description paste, automatic skill extraction
- **Dashboard** — ATS score, match score, missing skills chart, recent analyses
- **Analysis detail** — radar chart, skill gap matrix, ATS recommendations
- **Learning roadmap** — 30/60/90 day timeline with resources and priorities
- **Market trends** — trending/emerging skills, category demand charts
- **Source transparency** — confidence scores and provenance for every recommendation

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- Always run `pnpm --filter @workspace/api-spec run codegen` after changing `openapi.yaml`
- Run `pnpm run typecheck:libs` before checking artifact packages if `lib/*` changed
- `lib/api-zod/tsconfig.json` must keep `"dom"` in lib or `File`/`Blob` types break codegen output
- Resume parsing is async — poll `GET /resumes/:id` until `status === "ready"` before running analysis
- Uploaded files stored in `artifacts/api-server/uploads/` — must exist before server starts

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
