import path from "path";
import { logger } from "./logger.js";

export async function parseResumeFile(filePath: string): Promise<string> {
  const ext = path.extname(filePath).toLowerCase();

  if (ext === ".pdf") {
    return parsePdf(filePath);
  } else if (ext === ".docx") {
    return parseDocx(filePath);
  } else {
    throw new Error(`Unsupported file type: ${ext}`);
  }
}

async function parsePdf(filePath: string): Promise<string> {
  try {
    const fs = await import("fs");
    // pdf-parse@1.1.1 exports a plain CJS function (no .default wrapper needed)
    const pdfParse = (await import("pdf-parse")) as unknown as (buf: Buffer) => Promise<{ text: string }>;
    const buffer = fs.readFileSync(filePath);
    const data = await pdfParse(buffer);
    return data.text;
  } catch (err) {
    logger.error({ err, filePath }, "Failed to parse PDF");
    throw new Error("Failed to parse PDF file");
  }
}

async function parseDocx(filePath: string): Promise<string> {
  try {
    const mammoth = await import("mammoth");
    const result = await mammoth.extractRawText({ path: filePath });
    return result.value;
  } catch (err) {
    logger.error({ err, filePath }, "Failed to parse DOCX");
    throw new Error("Failed to parse DOCX file");
  }
}

export function extractStructuredSections(text: string): {
  education: string[];
  experience: string[];
  certifications: string[];
  yearsOfExperience: number | null;
} {
  const lines = text.split("\n").map((l) => l.trim()).filter(Boolean);
  const education: string[] = [];
  const experience: string[] = [];
  const certifications: string[] = [];

  let currentSection = "";

  for (const line of lines) {
    const lower = line.toLowerCase();

    if (/^education|^academic/i.test(lower)) { currentSection = "education"; continue; }
    if (/^experience|^work history|^employment/i.test(lower)) { currentSection = "experience"; continue; }
    if (/^certification|^licenses|^credentials/i.test(lower)) { currentSection = "certifications"; continue; }
    if (/^skills|^technical skills|^projects|^summary/i.test(lower)) { currentSection = "other"; continue; }

    if (line.length < 5) continue;

    if (currentSection === "education" && education.length < 5) education.push(line);
    if (currentSection === "experience" && experience.length < 8) experience.push(line);
    if (currentSection === "certifications" && certifications.length < 6) certifications.push(line);
  }

  const yearsMatch = text.match(/(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)/i);
  const yearsOfExperience = yearsMatch ? parseInt(yearsMatch[1], 10) : null;

  return { education, experience, certifications, yearsOfExperience };
}
