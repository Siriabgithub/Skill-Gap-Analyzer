import { Router, type IRouter } from "express";
import { db, resumesTable, analysesTable } from "@workspace/db";
import { eq, avg, count, desc } from "drizzle-orm";
import {
  CreateAnalysisBody,
  GetAnalysisParams,
  DeleteAnalysisParams,
  GetAnalysisRoadmapParams,
  GetAnalysisSourcesParams,
} from "@workspace/api-zod";
import { runSkillGapAnalysis } from "../lib/analysis-engine.js";
import { generateRoadmap } from "../lib/roadmap-generator.js";
import { logger } from "../lib/logger.js";

const router: IRouter = Router();

router.get("/analyses", async (req, res): Promise<void> => {
  const analyses = await db.select().from(analysesTable).orderBy(desc(analysesTable.createdAt));
  res.json(
    analyses.map((a) => ({
      id: a.id,
      resumeId: a.resumeId,
      status: a.status,
      createdAt: a.createdAt,
      jobTitle: a.jobTitle,
      matchScore: a.matchScore,
      atsScore: a.atsScore,
      missingSkillsCount: Array.isArray(a.missingSkills) ? a.missingSkills.length : 0,
    })),
  );
});

router.post("/analyses", async (req, res): Promise<void> => {
  const parsed = CreateAnalysisBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: parsed.error.message });
    return;
  }

  const { resumeId, jobDescription, jobTitle } = parsed.data;

  const [resume] = await db.select().from(resumesTable).where(eq(resumesTable.id, resumeId));
  if (!resume) {
    res.status(400).json({ error: "Resume not found" });
    return;
  }

  if (resume.status !== "ready") {
    res.status(400).json({ error: "Resume is still being processed. Please wait." });
    return;
  }

  const result = runSkillGapAnalysis(
    Array.isArray(resume.skills) ? resume.skills : [],
    jobDescription,
    resume.extractedText ?? "",
  );

  const [analysis] = await db.insert(analysesTable).values({
    resumeId,
    status: "completed",
    jobTitle: jobTitle ?? null,
    jobDescription,
    matchScore: result.matchScore,
    atsScore: result.atsScore,
    missingSkills: result.missingSkills,
    strongSkills: result.strongSkills,
    improvementAreas: result.improvementAreas,
    atsRecommendations: result.atsRecommendations,
  }).returning();

  logger.info({ analysisId: analysis.id, matchScore: result.matchScore, atsScore: result.atsScore }, "Analysis created");

  res.status(201).json({
    id: analysis.id,
    resumeId: analysis.resumeId,
    status: analysis.status,
    createdAt: analysis.createdAt,
    jobTitle: analysis.jobTitle,
    matchScore: analysis.matchScore,
    atsScore: analysis.atsScore,
    missingSkillsCount: result.missingSkills.length,
  });
});

router.get("/analyses/:id", async (req, res): Promise<void> => {
  const params = GetAnalysisParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [analysis] = await db.select().from(analysesTable).where(eq(analysesTable.id, params.data.id));
  if (!analysis) {
    res.status(404).json({ error: "Analysis not found" });
    return;
  }

  const [resume] = await db.select().from(resumesTable).where(eq(resumesTable.id, analysis.resumeId));

  res.json({
    id: analysis.id,
    resumeId: analysis.resumeId,
    status: analysis.status,
    createdAt: analysis.createdAt,
    jobTitle: analysis.jobTitle,
    jobDescription: analysis.jobDescription,
    matchScore: analysis.matchScore ?? 0,
    atsScore: analysis.atsScore ?? 0,
    missingSkills: analysis.missingSkills ?? [],
    strongSkills: analysis.strongSkills ?? [],
    improvementAreas: analysis.improvementAreas ?? [],
    atsRecommendations: analysis.atsRecommendations ?? [],
    resume: resume ?? null,
  });
});

router.delete("/analyses/:id", async (req, res): Promise<void> => {
  const params = DeleteAnalysisParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [analysis] = await db.delete(analysesTable).where(eq(analysesTable.id, params.data.id)).returning();
  if (!analysis) {
    res.status(404).json({ error: "Analysis not found" });
    return;
  }

  res.sendStatus(204);
});

router.get("/analyses/:id/roadmap", async (req, res): Promise<void> => {
  const params = GetAnalysisRoadmapParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [analysis] = await db.select().from(analysesTable).where(eq(analysesTable.id, params.data.id));
  if (!analysis) {
    res.status(404).json({ error: "Analysis not found" });
    return;
  }

  const missingSkills = Array.isArray(analysis.missingSkills) ? analysis.missingSkills : [];
  const roadmap = generateRoadmap(missingSkills);

  res.json({
    analysisId: analysis.id,
    ...roadmap,
  });
});

router.get("/analyses/:id/sources", async (req, res): Promise<void> => {
  const params = GetAnalysisSourcesParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [analysis] = await db.select().from(analysesTable).where(eq(analysesTable.id, params.data.id));
  if (!analysis) {
    res.status(404).json({ error: "Analysis not found" });
    return;
  }

  const sources = [
    {
      name: "User Resume",
      description: "Extracted text and skills from the uploaded resume document",
      lastUpdated: new Date(analysis.createdAt).toISOString().split("T")[0],
      confidenceScore: 0.95,
      category: "User Data",
    },
    {
      name: "Job Description",
      description: "Required and preferred skills extracted from the provided job description",
      lastUpdated: new Date(analysis.createdAt).toISOString().split("T")[0],
      confidenceScore: 0.90,
      category: "User Data",
    },
    {
      name: "SkillGap AI Skills Database",
      description: "Curated database of 40+ technical and professional skills with market demand scores, trend data, and NLP keyword patterns for accurate skill detection",
      lastUpdated: "2025-01-01",
      confidenceScore: 0.88,
      category: "Internal Database",
    },
    {
      name: "O*NET Online",
      description: "Occupational Information Network — comprehensive database of job characteristics and worker requirements maintained by the U.S. Department of Labor",
      lastUpdated: "2024-11-15",
      confidenceScore: 0.85,
      category: "External Dataset",
    },
    {
      name: "ESCO Skills Framework",
      description: "European Skills, Competences, Qualifications and Occupations — multilingual classification of skills and occupations used for skill categorization",
      lastUpdated: "2024-09-30",
      confidenceScore: 0.82,
      category: "External Dataset",
    },
    {
      name: "Job Market Trend Data",
      description: "Aggregated job posting demand scores and growth rates derived from major job board analytics (Indeed, LinkedIn, Glassdoor data proxies)",
      lastUpdated: "2025-01-15",
      confidenceScore: 0.79,
      category: "Market Intelligence",
    },
    {
      name: "ATS Pattern Library",
      description: "Known ATS (Applicant Tracking System) keyword patterns and scoring heuristics from Workday, Greenhouse, and Lever platforms",
      lastUpdated: "2024-12-01",
      confidenceScore: 0.80,
      category: "Internal Database",
    },
  ];

  res.json(sources);
});

export { router as analysesRouter };

export default router;
