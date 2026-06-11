import type { SkillGapItem } from "@workspace/db";

export type RoadmapPhase = {
  skill: string;
  description: string;
  resources: LearningResource[];
  priority: "high" | "medium" | "low";
  estimatedHours: number;
  category: string;
};

export type LearningResource = {
  title: string;
  type: "course" | "article" | "documentation" | "video" | "practice";
  url: string;
  provider: string;
  isFree: boolean;
};

const RESOURCE_MAP: Record<string, LearningResource[]> = {
  Python: [
    { title: "Python for Everybody", type: "course", url: "https://www.coursera.org/specializations/python", provider: "Coursera / Michigan", isFree: false },
    { title: "Official Python Docs", type: "documentation", url: "https://docs.python.org/3/", provider: "Python.org", isFree: true },
    { title: "Real Python Tutorials", type: "article", url: "https://realpython.com/", provider: "Real Python", isFree: true },
  ],
  JavaScript: [
    { title: "JavaScript.info", type: "article", url: "https://javascript.info", provider: "javascript.info", isFree: true },
    { title: "freeCodeCamp JavaScript", type: "course", url: "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", provider: "freeCodeCamp", isFree: true },
  ],
  TypeScript: [
    { title: "TypeScript Handbook", type: "documentation", url: "https://www.typescriptlang.org/docs/", provider: "TypeScript.org", isFree: true },
    { title: "Execute Program: TypeScript", type: "practice", url: "https://www.executeprogram.com/courses/typescript", provider: "Execute Program", isFree: false },
  ],
  React: [
    { title: "React Official Docs", type: "documentation", url: "https://react.dev/", provider: "React", isFree: true },
    { title: "Scrimba React Course", type: "course", url: "https://scrimba.com/learn/learnreact", provider: "Scrimba", isFree: false },
  ],
  AWS: [
    { title: "AWS Cloud Practitioner Essentials", type: "course", url: "https://www.aws.training/Details/eLearning?id=60697", provider: "AWS Training", isFree: true },
    { title: "AWS Solutions Architect", type: "course", url: "https://aws.amazon.com/certification/certified-solutions-architect-associate/", provider: "AWS", isFree: false },
  ],
  Docker: [
    { title: "Docker Getting Started", type: "documentation", url: "https://docs.docker.com/get-started/", provider: "Docker", isFree: true },
    { title: "Docker & Kubernetes: The Practical Guide", type: "course", url: "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/", provider: "Udemy", isFree: false },
  ],
  Kubernetes: [
    { title: "Kubernetes Basics", type: "course", url: "https://kubernetes.io/docs/tutorials/kubernetes-basics/", provider: "Kubernetes.io", isFree: true },
    { title: "Certified Kubernetes Administrator", type: "course", url: "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/", provider: "Linux Foundation", isFree: false },
  ],
  "Machine Learning": [
    { title: "Machine Learning Specialization", type: "course", url: "https://www.coursera.org/specializations/machine-learning-introduction", provider: "Coursera / Andrew Ng", isFree: false },
    { title: "fast.ai Practical Deep Learning", type: "course", url: "https://course.fast.ai/", provider: "fast.ai", isFree: true },
  ],
  SQL: [
    { title: "SQLZoo", type: "practice", url: "https://sqlzoo.net/", provider: "SQLZoo", isFree: true },
    { title: "Mode SQL Tutorial", type: "article", url: "https://mode.com/sql-tutorial/", provider: "Mode", isFree: true },
  ],
  PostgreSQL: [
    { title: "PostgreSQL Official Tutorial", type: "documentation", url: "https://www.postgresql.org/docs/current/tutorial.html", provider: "PostgreSQL.org", isFree: true },
    { title: "PostgreSQL for Everybody", type: "course", url: "https://www.coursera.org/specializations/postgresql-for-everybody", provider: "Coursera", isFree: false },
  ],
  Terraform: [
    { title: "HashiCorp Learn Terraform", type: "documentation", url: "https://developer.hashicorp.com/terraform/tutorials", provider: "HashiCorp", isFree: true },
  ],
  "CI/CD": [
    { title: "GitHub Actions Docs", type: "documentation", url: "https://docs.github.com/en/actions", provider: "GitHub", isFree: true },
    { title: "GitLab CI/CD Tutorial", type: "article", url: "https://docs.gitlab.com/ee/ci/quick_start/", provider: "GitLab", isFree: true },
  ],
  Go: [
    { title: "A Tour of Go", type: "practice", url: "https://go.dev/tour/", provider: "Go.dev", isFree: true },
    { title: "Go by Example", type: "article", url: "https://gobyexample.com/", provider: "gobyexample.com", isFree: true },
  ],
  default: [
    { title: "Find courses on Coursera", type: "course", url: "https://www.coursera.org/search", provider: "Coursera", isFree: false },
    { title: "Find tutorials on YouTube", type: "video", url: "https://www.youtube.com", provider: "YouTube", isFree: true },
  ],
};

const ESTIMATED_HOURS: Record<string, number> = {
  Python: 40, JavaScript: 40, TypeScript: 20, React: 30, "Node.js": 25,
  AWS: 60, Docker: 20, Kubernetes: 40, "Machine Learning": 80, SQL: 20,
  PostgreSQL: 25, Terraform: 30, "CI/CD": 15, Go: 50, Rust: 60, Java: 50,
  "Data Analysis": 35, "Deep Learning": 80, "LLM / AI Integration": 30,
};

function getResources(skillName: string): LearningResource[] {
  return RESOURCE_MAP[skillName] ?? RESOURCE_MAP["default"];
}

function getHours(skillName: string): number {
  return ESTIMATED_HOURS[skillName] ?? 25;
}

function buildDescription(skill: string, phase: "30" | "60" | "90"): string {
  const descriptions: Record<string, Record<string, string>> = {
    "30": {
      high: `Get foundational understanding of ${skill}. Complete introductory resources and run your first working examples.`,
      medium: `Begin exploring ${skill} concepts and complete at least one beginner tutorial.`,
      low: `Briefly familiarize yourself with ${skill} fundamentals.`,
    },
    "60": {
      high: `Build hands-on projects using ${skill}. Apply it in a real or portfolio project.`,
      medium: `Practice ${skill} with intermediate exercises and contribute to a small project.`,
      low: `Deepen understanding of ${skill} with intermediate-level material.`,
    },
    "90": {
      high: `Achieve job-ready proficiency in ${skill}. Be ready to discuss and demonstrate in interviews.`,
      medium: `Reach solid intermediate proficiency in ${skill} and be comfortable discussing it.`,
      low: `Develop working familiarity with ${skill}.`,
    },
  };
  return descriptions[phase]["medium"];
}

export function generateRoadmap(missingSkills: SkillGapItem[]): {
  thirtyDayPlan: RoadmapPhase[];
  sixtyDayPlan: RoadmapPhase[];
  ninetyDayPlan: RoadmapPhase[];
} {
  const high = missingSkills.filter((s) => s.priority === "high");
  const medium = missingSkills.filter((s) => s.priority === "medium");
  const low = missingSkills.filter((s) => s.priority === "low");

  const thirtyDayPlan: RoadmapPhase[] = high.slice(0, 2).map((s) => ({
    skill: s.name,
    description: buildDescription(s.name, "30"),
    resources: getResources(s.name),
    priority: s.priority,
    estimatedHours: Math.round(getHours(s.name) * 0.3),
    category: s.category,
  }));

  const sixtyDayPlan: RoadmapPhase[] = [
    ...high.slice(2, 4),
    ...medium.slice(0, 2),
  ].map((s) => ({
    skill: s.name,
    description: buildDescription(s.name, "60"),
    resources: getResources(s.name),
    priority: s.priority,
    estimatedHours: Math.round(getHours(s.name) * 0.5),
    category: s.category,
  }));

  const ninetyDayPlan: RoadmapPhase[] = [
    ...medium.slice(2, 4),
    ...low.slice(0, 2),
    ...high.slice(0, 1).map((s) => ({ ...s, priority: "medium" as const })),
  ].map((s) => ({
    skill: s.name,
    description: buildDescription(s.name, "90"),
    resources: getResources(s.name),
    priority: s.priority,
    estimatedHours: Math.round(getHours(s.name) * 0.4),
    category: s.category,
  }));

  return {
    thirtyDayPlan: thirtyDayPlan.length ? thirtyDayPlan : [{ skill: "Review Job Requirements", description: "You already have most required skills. Focus on deepening expertise in your top skills.", resources: RESOURCE_MAP["default"], priority: "medium", estimatedHours: 10, category: "Soft Skills" }],
    sixtyDayPlan: sixtyDayPlan.length ? sixtyDayPlan : [{ skill: "Portfolio Projects", description: "Build 1-2 portfolio projects showcasing your strong skills from the job requirements.", resources: RESOURCE_MAP["default"], priority: "medium", estimatedHours: 20, category: "Tools & Platforms" }],
    ninetyDayPlan: ninetyDayPlan.length ? ninetyDayPlan : [{ skill: "Interview Preparation", description: "Practice technical interviews, system design, and behavioral questions for the target role.", resources: [{ title: "LeetCode", type: "practice", url: "https://leetcode.com", provider: "LeetCode", isFree: true }], priority: "high", estimatedHours: 30, category: "Soft Skills" }],
  };
}
