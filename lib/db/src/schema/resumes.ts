import { pgTable, text, serial, integer, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export const resumesTable = pgTable("resumes", {
  id: serial("id").primaryKey(),
  filename: text("filename").notNull(),
  originalName: text("original_name").notNull(),
  status: text("status").notNull().default("processing"),
  extractedText: text("extracted_text"),
  skills: jsonb("skills").default([]).$type<ExtractedSkill[]>(),
  education: jsonb("education").default([]).$type<string[]>(),
  experience: jsonb("experience").default([]).$type<string[]>(),
  certifications: jsonb("certifications").default([]).$type<string[]>(),
  yearsOfExperience: integer("years_of_experience"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type ExtractedSkill = {
  name: string;
  confidence: number;
  category: string;
  source: string;
};

export const insertResumeSchema = createInsertSchema(resumesTable).omit({ id: true, createdAt: true });
export type InsertResume = z.infer<typeof insertResumeSchema>;
export type Resume = typeof resumesTable.$inferSelect;
