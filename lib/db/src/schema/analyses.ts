import { pgTable, text, serial, integer, timestamp, jsonb, real } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export type SkillGapItem = {
  name: string;
  category: string;
  priority: "high" | "medium" | "low";
  confidence: number;
  demandScore: number | null;
};

export const analysesTable = pgTable("analyses", {
  id: serial("id").primaryKey(),
  resumeId: integer("resume_id").notNull(),
  status: text("status").notNull().default("pending"),
  jobTitle: text("job_title"),
  jobDescription: text("job_description").notNull(),
  matchScore: real("match_score"),
  atsScore: real("ats_score"),
  missingSkills: jsonb("missing_skills").default([]).$type<SkillGapItem[]>(),
  strongSkills: jsonb("strong_skills").default([]).$type<SkillGapItem[]>(),
  improvementAreas: jsonb("improvement_areas").default([]).$type<string[]>(),
  atsRecommendations: jsonb("ats_recommendations").default([]).$type<string[]>(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertAnalysisSchema = createInsertSchema(analysesTable).omit({ id: true, createdAt: true });
export type InsertAnalysis = z.infer<typeof insertAnalysisSchema>;
export type Analysis = typeof analysesTable.$inferSelect;
