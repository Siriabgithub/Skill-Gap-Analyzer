import { Router, type IRouter } from "express";
import multer from "multer";
import path from "path";
import fs from "fs";
import { db, resumesTable } from "@workspace/db";
import { eq } from "drizzle-orm";
import { GetResumeParams, DeleteResumeParams } from "@workspace/api-zod";
import { parseResumeFile, extractStructuredSections } from "../lib/file-parser.js";
import { extractSkillsFromText } from "../lib/skills-database.js";
import { logger } from "../lib/logger.js";

const workspaceRoot = process.cwd().endsWith(path.join("artifacts", "api-server"))
  ? path.resolve(process.cwd(), "../..")
  : process.cwd();

const uploadsDir = path.resolve(workspaceRoot, "artifacts/api-server/uploads");
if (!fs.existsSync(uploadsDir)) fs.mkdirSync(uploadsDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => cb(null, uploadsDir),
  filename: (_req, file, cb) => {
    const unique = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
    cb(null, `${unique}${path.extname(file.originalname)}`);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (_req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (ext === ".pdf" || ext === ".docx") {
      cb(null, true);
    } else {
      cb(new Error("Only PDF and DOCX files are allowed"));
    }
  },
});

const router: IRouter = Router();

router.get("/resumes", async (req, res): Promise<void> => {
  const resumes = await db.select().from(resumesTable).orderBy(resumesTable.createdAt);
  res.json(resumes);
});

router.post("/resumes/upload", upload.single("file"), async (req, res): Promise<void> => {
  if (!req.file) {
    res.status(400).json({ error: "No file uploaded" });
    return;
  }

  const [resume] = await db.insert(resumesTable).values({
    filename: req.file.filename,
    originalName: req.file.originalname,
    status: "processing",
  }).returning();

  res.status(201).json(resume);

  (async () => {
    try {
      const text = await parseResumeFile(req.file!.path);
      const skills = extractSkillsFromText(text);
      const sections = extractStructuredSections(text);

      await db.update(resumesTable).set({
        status: "ready",
        extractedText: text.substring(0, 5000),
        skills,
        education: sections.education,
        experience: sections.experience,
        certifications: sections.certifications,
        yearsOfExperience: sections.yearsOfExperience,
      }).where(eq(resumesTable.id, resume.id));

      logger.info({ resumeId: resume.id }, "Resume parsed successfully");
    } catch (err) {
      logger.error({ err, resumeId: resume.id }, "Failed to parse resume");
      await db.update(resumesTable).set({ status: "error" }).where(eq(resumesTable.id, resume.id));
    }
  })();
});

router.get("/resumes/:id", async (req, res): Promise<void> => {
  const params = GetResumeParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [resume] = await db.select().from(resumesTable).where(eq(resumesTable.id, params.data.id));
  if (!resume) {
    res.status(404).json({ error: "Resume not found" });
    return;
  }

  res.json(resume);
});

router.delete("/resumes/:id", async (req, res): Promise<void> => {
  const params = DeleteResumeParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [resume] = await db.delete(resumesTable).where(eq(resumesTable.id, params.data.id)).returning();
  if (!resume) {
    res.status(404).json({ error: "Resume not found" });
    return;
  }

  const filePath = path.resolve(uploadsDir, resume.filename);
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
  }

  res.sendStatus(204);
});

export default router;
