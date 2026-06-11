import type { ExtractedSkill, SkillGapItem } from "@workspace/db";
import { extractRequiredSkillsFromJD, getSkillEntry } from "./skills-database.js";

export type AnalysisResult = {
  matchScore: number;
  atsScore: number;
  missingSkills: SkillGapItem[];
  strongSkills: SkillGapItem[];
  improvementAreas: string[];
  atsRecommendations: string[];
};

export function runSkillGapAnalysis(
  resumeSkills: ExtractedSkill[],
  jobDescription: string,
  resumeText: string,
): AnalysisResult {
  const jdSkills = extractRequiredSkillsFromJD(jobDescription);
  const resumeSkillNames = new Set(resumeSkills.map((s) => s.name.toLowerCase()));

  const missingSkills: SkillGapItem[] = [];
  const strongSkills: SkillGapItem[] = [];

  for (const jdSkill of jdSkills) {
    const inResume = resumeSkillNames.has(jdSkill.name.toLowerCase());
    const entry = getSkillEntry(jdSkill.name);

    if (inResume) {
      strongSkills.push({
        name: jdSkill.name,
        category: jdSkill.category,
        priority: jdSkill.priority,
        confidence: jdSkill.confidence,
        demandScore: entry?.demandScore ?? null,
      });
    } else {
      missingSkills.push({
        name: jdSkill.name,
        category: jdSkill.category,
        priority: jdSkill.priority,
        confidence: jdSkill.confidence,
        demandScore: entry?.demandScore ?? null,
      });
    }
  }

  const totalJdSkills = jdSkills.length;
  const matchedCount = strongSkills.length;
  const matchScore = totalJdSkills > 0 ? Math.round((matchedCount / totalJdSkills) * 100) : 0;

  const atsScore = computeAtsScore(resumeText, jobDescription, matchScore, resumeSkills);

  const improvementAreas = deriveImprovementAreas(missingSkills);
  const atsRecommendations = deriveAtsRecommendations(resumeText, missingSkills, atsScore);

  return {
    matchScore,
    atsScore,
    missingSkills: missingSkills.sort((a, b) => priorityWeight(b.priority) - priorityWeight(a.priority)),
    strongSkills: strongSkills.sort((a, b) => b.confidence - a.confidence),
    improvementAreas,
    atsRecommendations,
  };
}

function priorityWeight(p: "high" | "medium" | "low"): number {
  return p === "high" ? 3 : p === "medium" ? 2 : 1;
}

function computeAtsScore(resumeText: string, jobDescription: string, matchScore: number, skills: ExtractedSkill[]): number {
  const text = resumeText.toLowerCase();
  let score = 0;

  score += matchScore * 0.4;

  const sections = ["experience", "education", "skills", "summary", "objective", "certifications", "projects"];
  const foundSections = sections.filter((s) => text.includes(s));
  score += (foundSections.length / sections.length) * 25;

  const jdWords = jobDescription.toLowerCase().split(/\W+/).filter((w) => w.length > 4);
  const jdWordSet = new Set(jdWords);
  const resumeWords = text.split(/\W+/).filter((w) => w.length > 4);
  const resumeWordSet = new Set(resumeWords);
  const keywordOverlap = [...jdWordSet].filter((w) => resumeWordSet.has(w)).length / Math.max(jdWordSet.size, 1);
  score += keywordOverlap * 20;

  const hasQuantifiableAchievements = /\d+%|\d+ (users|customers|projects|teams|million|billion|k\b)/.test(text);
  if (hasQuantifiableAchievements) score += 10;

  const hasContactInfo = /email|phone|linkedin|github/.test(text);
  if (hasContactInfo) score += 5;

  return Math.min(Math.round(score), 100);
}

function deriveImprovementAreas(missing: SkillGapItem[]): string[] {
  const categories = new Set(missing.filter((s) => s.priority !== "low").map((s) => s.category));
  const areas: string[] = [];

  if (categories.has("Cloud & DevOps")) areas.push("Strengthen cloud infrastructure and DevOps practices");
  if (categories.has("Data Science & ML")) areas.push("Build expertise in data science and machine learning");
  if (categories.has("Frameworks & Libraries")) areas.push("Expand framework knowledge for the target tech stack");
  if (categories.has("Programming Languages")) areas.push("Acquire proficiency in required programming languages");
  if (categories.has("Databases")) areas.push("Deepen database and data storage knowledge");
  if (categories.has("Security")) areas.push("Develop security fundamentals and best practices");
  if (categories.has("Tools & Platforms")) areas.push("Familiarize with required tooling and platforms");

  const highPriorityMissing = missing.filter((s) => s.priority === "high");
  if (highPriorityMissing.length > 3) {
    areas.push("Focus on high-priority skill gaps before applying");
  }

  return areas.slice(0, 5);
}

function deriveAtsRecommendations(resumeText: string, missing: SkillGapItem[], atsScore: number): string[] {
  const recs: string[] = [];
  const text = resumeText.toLowerCase();

  if (atsScore < 50) recs.push("Add more keywords from the job description throughout your resume");
  if (!text.includes("summary") && !text.includes("objective")) recs.push("Add a professional summary section tailored to this role");
  if (!/\d+%/.test(text)) recs.push("Quantify achievements with metrics (e.g., 'Improved performance by 40%')");
  if (!text.includes("linkedin")) recs.push("Include your LinkedIn profile URL");

  const highMissing = missing.filter((s) => s.priority === "high").slice(0, 3);
  for (const skill of highMissing) {
    recs.push(`Add any existing experience with ${skill.name}, even if indirect`);
  }

  if (!text.includes("github") && !text.includes("portfolio")) {
    recs.push("Include a GitHub profile or portfolio link to showcase your work");
  }

  if (atsScore >= 70) recs.push("Strong keyword alignment — ensure formatting is ATS-compatible (no tables, images in text)");

  return recs.slice(0, 6);
}
