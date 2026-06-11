import { Router, type IRouter } from "express";
import { SKILLS_DATABASE } from "../lib/skills-database.js";

const router: IRouter = Router();

router.get("/market-trends", async (_req, res): Promise<void> => {
  const trendingSkills = SKILLS_DATABASE
    .filter((s) => s.trendDirection === "rising" || s.trendDirection === "stable")
    .sort((a, b) => b.demandScore - a.demandScore)
    .slice(0, 15)
    .map((s) => ({
      name: s.name,
      demandScore: s.demandScore,
      trendDirection: s.trendDirection,
      category: s.category,
      jobCount: s.jobCount,
      growthRate: s.growthRate,
    }));

  const emergingSkills = SKILLS_DATABASE
    .filter((s) => s.growthRate >= 20)
    .sort((a, b) => b.growthRate - a.growthRate)
    .slice(0, 10)
    .map((s) => ({
      name: s.name,
      demandScore: s.demandScore,
      trendDirection: s.trendDirection,
      category: s.category,
      jobCount: s.jobCount,
      growthRate: s.growthRate,
    }));

  const categoryMap = new Map<string, { demandScores: number[]; skills: string[] }>();
  for (const skill of SKILLS_DATABASE) {
    if (!categoryMap.has(skill.category)) {
      categoryMap.set(skill.category, { demandScores: [], skills: [] });
    }
    const entry = categoryMap.get(skill.category)!;
    entry.demandScores.push(skill.demandScore);
    entry.skills.push(skill.name);
  }

  const topCategories = Array.from(categoryMap.entries()).map(([category, data]) => ({
    category,
    demandScore: Math.round(data.demandScores.reduce((a, b) => a + b, 0) / data.demandScores.length),
    skillCount: data.skills.length,
    topSkills: data.skills.slice(0, 3),
  })).sort((a, b) => b.demandScore - a.demandScore);

  res.json({
    trendingSkills,
    emergingSkills,
    topCategories,
    lastUpdated: new Date().toISOString().split("T")[0],
  });
});

export default router;
