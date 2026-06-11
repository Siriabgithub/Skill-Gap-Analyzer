export type SkillCategory =
  | "Programming Languages"
  | "Frameworks & Libraries"
  | "Cloud & DevOps"
  | "Databases"
  | "Data Science & ML"
  | "Tools & Platforms"
  | "Soft Skills"
  | "Security"
  | "Mobile"
  | "Design";

export type SkillEntry = {
  name: string;
  category: SkillCategory;
  aliases: string[];
  keywords: string[];
  demandScore: number;
  trendDirection: "rising" | "stable" | "declining";
  jobCount: number;
  growthRate: number;
};

export const SKILLS_DATABASE: SkillEntry[] = [
  { name: "Python", category: "Programming Languages", aliases: ["python3", "py"], keywords: ["python", "py", "django", "flask", "fastapi", "pandas", "numpy", "scikit", "pytorch", "tensorflow"], demandScore: 96, trendDirection: "rising", jobCount: 87400, growthRate: 18 },
  { name: "JavaScript", category: "Programming Languages", aliases: ["js", "es6", "es2015", "ecmascript"], keywords: ["javascript", "js", "es6", "node", "nodejs", "typescript", "ts"], demandScore: 94, trendDirection: "stable", jobCount: 92000, growthRate: 5 },
  { name: "TypeScript", category: "Programming Languages", aliases: ["ts"], keywords: ["typescript", "ts", "typed javascript"], demandScore: 88, trendDirection: "rising", jobCount: 54000, growthRate: 28 },
  { name: "Java", category: "Programming Languages", aliases: ["java8", "java11", "java17"], keywords: ["java", "spring", "springboot", "hibernate", "maven", "gradle"], demandScore: 82, trendDirection: "stable", jobCount: 68000, growthRate: 2 },
  { name: "Go", category: "Programming Languages", aliases: ["golang"], keywords: ["go", "golang", "goroutine", "grpc"], demandScore: 78, trendDirection: "rising", jobCount: 32000, growthRate: 22 },
  { name: "Rust", category: "Programming Languages", aliases: [], keywords: ["rust", "cargo", "tokio", "async rust"], demandScore: 70, trendDirection: "rising", jobCount: 14000, growthRate: 45 },
  { name: "C++", category: "Programming Languages", aliases: ["cpp", "c plus plus"], keywords: ["c++", "cpp", "stl", "boost", "cmake"], demandScore: 72, trendDirection: "stable", jobCount: 41000, growthRate: 3 },
  { name: "C#", category: "Programming Languages", aliases: ["csharp", "dotnet", ".net"], keywords: ["c#", "csharp", ".net", "dotnet", "asp.net", "unity"], demandScore: 74, trendDirection: "stable", jobCount: 45000, growthRate: 4 },
  { name: "React", category: "Frameworks & Libraries", aliases: ["reactjs", "react.js"], keywords: ["react", "jsx", "hooks", "redux", "react native", "next.js", "nextjs", "react query"], demandScore: 92, trendDirection: "rising", jobCount: 78000, growthRate: 15 },
  { name: "Node.js", category: "Frameworks & Libraries", aliases: ["nodejs", "node"], keywords: ["node", "nodejs", "express", "nestjs", "fastify", "koa"], demandScore: 86, trendDirection: "stable", jobCount: 62000, growthRate: 8 },
  { name: "Vue.js", category: "Frameworks & Libraries", aliases: ["vue", "vuejs"], keywords: ["vue", "vuejs", "vuex", "pinia", "nuxt"], demandScore: 72, trendDirection: "stable", jobCount: 28000, growthRate: 6 },
  { name: "Angular", category: "Frameworks & Libraries", aliases: ["angularjs"], keywords: ["angular", "angularjs", "rxjs", "ngrx"], demandScore: 68, trendDirection: "declining", jobCount: 24000, growthRate: -2 },
  { name: "Spring Boot", category: "Frameworks & Libraries", aliases: ["spring", "springboot"], keywords: ["spring boot", "spring framework", "spring mvc", "spring security"], demandScore: 75, trendDirection: "stable", jobCount: 38000, growthRate: 3 },
  { name: "Django", category: "Frameworks & Libraries", aliases: [], keywords: ["django", "django rest", "drf", "celery"], demandScore: 70, trendDirection: "stable", jobCount: 22000, growthRate: 5 },
  { name: "FastAPI", category: "Frameworks & Libraries", aliases: [], keywords: ["fastapi", "pydantic", "async python"], demandScore: 74, trendDirection: "rising", jobCount: 18000, growthRate: 38 },
  { name: "AWS", category: "Cloud & DevOps", aliases: ["amazon web services"], keywords: ["aws", "amazon web services", "ec2", "s3", "lambda", "cloudfront", "rds", "eks", "ecs", "cloudwatch", "iam", "vpc"], demandScore: 95, trendDirection: "rising", jobCount: 94000, growthRate: 20 },
  { name: "Azure", category: "Cloud & DevOps", aliases: ["microsoft azure"], keywords: ["azure", "microsoft azure", "azure devops", "aks", "azure functions", "cosmos db"], demandScore: 88, trendDirection: "rising", jobCount: 72000, growthRate: 24 },
  { name: "Google Cloud", category: "Cloud & DevOps", aliases: ["gcp", "google cloud platform"], keywords: ["gcp", "google cloud", "bigquery", "gke", "cloud run", "pubsub", "dataflow"], demandScore: 82, trendDirection: "rising", jobCount: 48000, growthRate: 26 },
  { name: "Docker", category: "Cloud & DevOps", aliases: [], keywords: ["docker", "dockerfile", "container", "compose", "docker-compose"], demandScore: 90, trendDirection: "rising", jobCount: 82000, growthRate: 16 },
  { name: "Kubernetes", category: "Cloud & DevOps", aliases: ["k8s"], keywords: ["kubernetes", "k8s", "kubectl", "helm", "pod", "deployment", "service mesh", "istio"], demandScore: 88, trendDirection: "rising", jobCount: 58000, growthRate: 25 },
  { name: "Terraform", category: "Cloud & DevOps", aliases: ["tf"], keywords: ["terraform", "terraform cloud", "hcl", "infrastructure as code", "iac"], demandScore: 84, trendDirection: "rising", jobCount: 42000, growthRate: 32 },
  { name: "CI/CD", category: "Cloud & DevOps", aliases: ["continuous integration", "continuous deployment"], keywords: ["ci/cd", "continuous integration", "jenkins", "github actions", "gitlab ci", "circle ci", "travis", "pipeline"], demandScore: 86, trendDirection: "rising", jobCount: 76000, growthRate: 18 },
  { name: "PostgreSQL", category: "Databases", aliases: ["postgres"], keywords: ["postgresql", "postgres", "psql", "pg"], demandScore: 84, trendDirection: "rising", jobCount: 52000, growthRate: 12 },
  { name: "MySQL", category: "Databases", aliases: [], keywords: ["mysql", "mariadb", "mysql workbench"], demandScore: 78, trendDirection: "stable", jobCount: 58000, growthRate: 3 },
  { name: "MongoDB", category: "Databases", aliases: ["mongo"], keywords: ["mongodb", "mongo", "mongoose", "atlas", "nosql document"], demandScore: 80, trendDirection: "stable", jobCount: 44000, growthRate: 8 },
  { name: "Redis", category: "Databases", aliases: [], keywords: ["redis", "cache", "pubsub", "redis cluster"], demandScore: 78, trendDirection: "rising", jobCount: 36000, growthRate: 14 },
  { name: "Elasticsearch", category: "Databases", aliases: ["elastic", "elk"], keywords: ["elasticsearch", "elastic", "kibana", "logstash", "elk stack"], demandScore: 72, trendDirection: "stable", jobCount: 26000, growthRate: 6 },
  { name: "Machine Learning", category: "Data Science & ML", aliases: ["ml"], keywords: ["machine learning", "ml", "scikit-learn", "sklearn", "supervised", "unsupervised", "classification", "regression", "clustering", "random forest", "gradient boosting", "xgboost"], demandScore: 90, trendDirection: "rising", jobCount: 52000, growthRate: 30 },
  { name: "Deep Learning", category: "Data Science & ML", aliases: ["dl", "neural networks"], keywords: ["deep learning", "neural network", "cnn", "rnn", "lstm", "transformer", "bert", "gpt", "pytorch", "tensorflow", "keras"], demandScore: 86, trendDirection: "rising", jobCount: 34000, growthRate: 38 },
  { name: "Data Analysis", category: "Data Science & ML", aliases: ["data analytics"], keywords: ["data analysis", "data analytics", "pandas", "numpy", "scipy", "jupyter", "statistical analysis", "eda"], demandScore: 88, trendDirection: "rising", jobCount: 64000, growthRate: 22 },
  { name: "SQL", category: "Databases", aliases: [], keywords: ["sql", "query", "database query", "stored procedure", "join", "aggregate", "window function"], demandScore: 92, trendDirection: "stable", jobCount: 86000, growthRate: 5 },
  { name: "Agile", category: "Soft Skills", aliases: ["scrum", "kanban"], keywords: ["agile", "scrum", "kanban", "sprint", "retrospective", "standup", "jira", "confluence"], demandScore: 82, trendDirection: "stable", jobCount: 78000, growthRate: 4 },
  { name: "GraphQL", category: "Frameworks & Libraries", aliases: [], keywords: ["graphql", "apollo", "relay", "graphene"], demandScore: 72, trendDirection: "rising", jobCount: 22000, growthRate: 18 },
  { name: "Git", category: "Tools & Platforms", aliases: ["github", "gitlab", "version control"], keywords: ["git", "github", "gitlab", "bitbucket", "version control", "branching"], demandScore: 94, trendDirection: "stable", jobCount: 96000, growthRate: 4 },
  { name: "Linux", category: "Tools & Platforms", aliases: ["unix", "bash"], keywords: ["linux", "unix", "bash", "shell script", "command line", "ubuntu", "centos", "debian"], demandScore: 86, trendDirection: "stable", jobCount: 72000, growthRate: 6 },
  { name: "React Native", category: "Mobile", aliases: ["rn"], keywords: ["react native", "mobile app", "ios", "android", "expo"], demandScore: 76, trendDirection: "rising", jobCount: 28000, growthRate: 20 },
  { name: "Cybersecurity", category: "Security", aliases: ["security", "infosec"], keywords: ["security", "cybersecurity", "penetration testing", "soc", "siem", "owasp", "vulnerability", "encryption", "ssl", "tls", "oauth"], demandScore: 88, trendDirection: "rising", jobCount: 56000, growthRate: 28 },
  { name: "Data Engineering", category: "Data Science & ML", aliases: ["de"], keywords: ["data engineering", "etl", "data pipeline", "apache spark", "kafka", "airflow", "dbt", "data warehouse"], demandScore: 86, trendDirection: "rising", jobCount: 38000, growthRate: 34 },
  { name: "LLM / AI Integration", category: "Data Science & ML", aliases: ["llm", "generative ai", "ai"], keywords: ["llm", "gpt", "openai", "langchain", "rag", "prompt engineering", "embeddings", "vector database", "generative ai", "fine-tuning"], demandScore: 95, trendDirection: "rising", jobCount: 28000, growthRate: 125 },
  { name: "System Design", category: "Soft Skills", aliases: [], keywords: ["system design", "scalability", "distributed systems", "microservices", "architecture", "high availability", "load balancing", "caching strategy"], demandScore: 84, trendDirection: "rising", jobCount: 46000, growthRate: 15 },
];

export function extractSkillsFromText(text: string): Array<{ name: string; category: SkillCategory; confidence: number; source: string }> {
  const normalizedText = text.toLowerCase();
  const found: Array<{ name: string; category: SkillCategory; confidence: number; source: string }> = [];
  const seen = new Set<string>();

  for (const skill of SKILLS_DATABASE) {
    if (seen.has(skill.name)) continue;

    let confidence = 0;
    let matched = false;

    for (const keyword of skill.keywords) {
      const kw = keyword.toLowerCase();
      if (normalizedText.includes(kw)) {
        confidence = Math.max(confidence, keyword === skill.name.toLowerCase() ? 1.0 : 0.85);
        matched = true;
      }
    }

    for (const alias of skill.aliases) {
      if (normalizedText.includes(alias.toLowerCase())) {
        confidence = Math.max(confidence, 0.9);
        matched = true;
      }
    }

    if (matched) {
      found.push({ name: skill.name, category: skill.category, confidence: Math.min(confidence, 1.0), source: "resume_text" });
      seen.add(skill.name);
    }
  }

  return found.sort((a, b) => b.confidence - a.confidence);
}

export function extractRequiredSkillsFromJD(text: string): Array<{ name: string; category: SkillCategory; confidence: number; priority: "high" | "medium" | "low" }> {
  const normalizedText = text.toLowerCase();
  const found: Array<{ name: string; category: SkillCategory; confidence: number; priority: "high" | "medium" | "low" }> = [];
  const seen = new Set<string>();

  const highPriorityMarkers = ["required", "must have", "must-have", "essential", "mandatory", "strong experience", "proficiency"];
  const lowPriorityMarkers = ["nice to have", "bonus", "preferred", "plus", "familiar with"];

  function getPriority(keyword: string): "high" | "medium" | "low" {
    const idx = normalizedText.indexOf(keyword.toLowerCase());
    if (idx === -1) return "medium";

    const surroundingText = normalizedText.substring(Math.max(0, idx - 100), idx + 100);

    if (highPriorityMarkers.some((m) => surroundingText.includes(m))) return "high";
    if (lowPriorityMarkers.some((m) => surroundingText.includes(m))) return "low";
    return "medium";
  }

  for (const skill of SKILLS_DATABASE) {
    if (seen.has(skill.name)) continue;

    let confidence = 0;
    let matchedKeyword = "";

    for (const keyword of skill.keywords) {
      if (normalizedText.includes(keyword.toLowerCase())) {
        confidence = Math.max(confidence, keyword === skill.name.toLowerCase() ? 1.0 : 0.85);
        matchedKeyword = keyword;
      }
    }

    for (const alias of skill.aliases) {
      if (normalizedText.includes(alias.toLowerCase())) {
        confidence = Math.max(confidence, 0.9);
        matchedKeyword = alias;
      }
    }

    if (confidence > 0) {
      found.push({ name: skill.name, category: skill.category, confidence, priority: getPriority(matchedKeyword) });
      seen.add(skill.name);
    }
  }

  return found.sort((a, b) => b.confidence - a.confidence);
}

export function getSkillEntry(skillName: string): SkillEntry | undefined {
  return SKILLS_DATABASE.find((s) => s.name.toLowerCase() === skillName.toLowerCase() || s.aliases.some((a) => a.toLowerCase() === skillName.toLowerCase()));
}
