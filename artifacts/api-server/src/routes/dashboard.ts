import { Router, type IRouter } from "express";
import { db, resumesTable, analysesTable } from "@workspace/db";
import { desc } from "drizzle-orm";
import type { SkillGapItem } from "@workspace/db";

const router: IRouter = Router();

router.get("/dashboard/stats", async (req, res): Promise<void> => {
  const resumes = await db.select().from(resumesTable);
  const analyses = await db.select().from(analysesTable).orderBy(desc(analysesTable.createdAt));

  const totalResumes = resumes.length;
  const totalAnalyses = analyses.length;

  const completedAnalyses = analyses.filter((a) => a.status === "completed");

  const avgAtsScore = completedAnalyses.length > 0
    ? Math.round(completedAnalyses.reduce((sum, a) => sum + (a.atsScore ?? 0), 0) / completedAnalyses.length)
    : 0;

  const avgMatchScore = completedAnalyses.length > 0
    ? Math.round(completedAnalyses.reduce((sum, a) => sum + (a.matchScore ?? 0), 0) / completedAnalyses.length)
    : 0;

  const skillFreqMap = new Map<string, { count: number; category: string }>();
  for (const analysis of completedAnalyses) {
    const missing = analysis.missingSkills as SkillGapItem[] | null;
    if (Array.isArray(missing)) {
      for (const skill of missing) {
        const prev = skillFreqMap.get(skill.name);
        if (prev) {
          prev.count++;
        } else {
          skillFreqMap.set(skill.name, { count: 1, category: skill.category });
        }
      }
    }
  }

  const topMissingSkills = Array.from(skillFreqMap.entries())
    .map(([skill, data]) => ({ skill, count: data.count, category: data.category }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8);

  const recentAnalyses = analyses.slice(0, 5).map((a) => ({
    id: a.id,
    resumeId: a.resumeId,
    status: a.status,
    createdAt: a.createdAt,
    jobTitle: a.jobTitle,
    matchScore: a.matchScore,
    atsScore: a.atsScore,
    missingSkillsCount: Array.isArray(a.missingSkills) ? (a.missingSkills as SkillGapItem[]).length : 0,
  }));

  res.json({
    totalResumes,
    totalAnalyses,
    avgAtsScore,
    avgMatchScore,
    topMissingSkills,
    recentAnalyses,
  });
});

export default router;
