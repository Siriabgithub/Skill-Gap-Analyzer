import { Router, type IRouter } from "express";
import healthRouter from "./health";
import resumesRouter from "./resumes";
import analysesRouter from "./analyses";
import marketRouter from "./market";
import dashboardRouter from "./dashboard";

const router: IRouter = Router();

router.use(healthRouter);
router.use(resumesRouter);
router.use(analysesRouter);
router.use(marketRouter);
router.use(dashboardRouter);

export default router;
