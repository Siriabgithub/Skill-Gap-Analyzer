"""
Comprehensive skills database with categories, aliases, market demand,
learning resources, and related skills.
"""

SKILLS_DATABASE = {
    # ─── Programming Languages ───────────────────────────────────────────────
    "python": {
        "category": "Programming Languages",
        "aliases": ["python3", "python 3", "py"],
        "demand_score": 95,
        "growth_rate": 28,
        "avg_salary": 115000,
        "description": "High-level, general-purpose programming language",
        "resources": [
            {"name": "Python.org Official Docs", "url": "https://docs.python.org/3/", "type": "documentation"},
            {"name": "Python for Everybody (Coursera)", "url": "https://www.coursera.org/specializations/python", "type": "course"},
            {"name": "Real Python", "url": "https://realpython.com", "type": "tutorial"},
        ],
        "related": ["pandas", "numpy", "scikit-learn", "django", "fastapi"],
        "time_to_learn": "3-6 months",
    },
    "javascript": {
        "category": "Programming Languages",
        "aliases": ["js", "javascript es6", "es6", "es2015", "ecmascript"],
        "demand_score": 92,
        "growth_rate": 15,
        "avg_salary": 108000,
        "description": "Scripting language for web development",
        "resources": [
            {"name": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "type": "documentation"},
            {"name": "JavaScript.info", "url": "https://javascript.info", "type": "tutorial"},
            {"name": "freeCodeCamp JS", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "course"},
        ],
        "related": ["typescript", "react", "node.js", "vue.js", "angular"],
        "time_to_learn": "3-5 months",
    },
    "typescript": {
        "category": "Programming Languages",
        "aliases": ["ts", "type script"],
        "demand_score": 88,
        "growth_rate": 42,
        "avg_salary": 118000,
        "description": "Typed superset of JavaScript",
        "resources": [
            {"name": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "documentation"},
            {"name": "TypeScript Deep Dive", "url": "https://basarat.gitbook.io/typescript/", "type": "book"},
        ],
        "related": ["javascript", "react", "angular", "node.js"],
        "time_to_learn": "1-2 months",
    },
    "sql": {
        "category": "Databases",
        "aliases": ["structured query language", "mysql", "postgresql", "postgres", "sqlite", "t-sql", "pl/sql"],
        "demand_score": 90,
        "growth_rate": 12,
        "avg_salary": 98000,
        "description": "Language for managing relational databases",
        "resources": [
            {"name": "SQLZoo", "url": "https://sqlzoo.net", "type": "tutorial"},
            {"name": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "tutorial"},
            {"name": "Khan Academy SQL", "url": "https://www.khanacademy.org/computing/computer-programming/sql", "type": "course"},
        ],
        "related": ["postgresql", "mysql", "database design", "data warehouse"],
        "time_to_learn": "1-3 months",
    },
    "java": {
        "category": "Programming Languages",
        "aliases": ["java 8", "java 11", "java 17", "core java"],
        "demand_score": 85,
        "growth_rate": 5,
        "avg_salary": 110000,
        "description": "Object-oriented programming language",
        "resources": [
            {"name": "Oracle Java Docs", "url": "https://docs.oracle.com/en/java/", "type": "documentation"},
            {"name": "Java Programming (Coursera)", "url": "https://www.coursera.org/specializations/java-programming", "type": "course"},
        ],
        "related": ["spring boot", "maven", "gradle", "hibernate"],
        "time_to_learn": "4-8 months",
    },
    "r": {
        "category": "Programming Languages",
        "aliases": ["r programming", "r language", "rlang"],
        "demand_score": 72,
        "growth_rate": 8,
        "avg_salary": 98000,
        "description": "Statistical computing and graphics language",
        "resources": [
            {"name": "R for Data Science", "url": "https://r4ds.had.co.nz", "type": "book"},
            {"name": "Swirl (interactive R)", "url": "https://swirlstats.com", "type": "tutorial"},
        ],
        "related": ["ggplot2", "dplyr", "tidyverse", "statistics"],
        "time_to_learn": "2-4 months",
    },
    "go": {
        "category": "Programming Languages",
        "aliases": ["golang", "go lang"],
        "demand_score": 80,
        "growth_rate": 35,
        "avg_salary": 125000,
        "description": "Statically typed, compiled language by Google",
        "resources": [
            {"name": "Go Tour", "url": "https://go.dev/tour/", "type": "tutorial"},
            {"name": "Go by Example", "url": "https://gobyexample.com", "type": "tutorial"},
        ],
        "related": ["kubernetes", "docker", "microservices"],
        "time_to_learn": "2-4 months",
    },
    "rust": {
        "category": "Programming Languages",
        "aliases": ["rust lang", "rustlang"],
        "demand_score": 75,
        "growth_rate": 50,
        "avg_salary": 130000,
        "description": "Systems programming language focused on safety and performance",
        "resources": [
            {"name": "The Rust Book", "url": "https://doc.rust-lang.org/book/", "type": "book"},
            {"name": "Rustlings", "url": "https://github.com/rust-lang/rustlings", "type": "tutorial"},
        ],
        "related": ["webassembly", "systems programming"],
        "time_to_learn": "6-12 months",
    },
    "c++": {
        "category": "Programming Languages",
        "aliases": ["cpp", "c plus plus", "c/c++"],
        "demand_score": 78,
        "growth_rate": 3,
        "avg_salary": 112000,
        "description": "General-purpose systems programming language",
        "resources": [
            {"name": "cppreference.com", "url": "https://en.cppreference.com", "type": "documentation"},
            {"name": "LearnCpp.com", "url": "https://www.learncpp.com", "type": "tutorial"},
        ],
        "related": ["c", "embedded systems", "game development"],
        "time_to_learn": "6-12 months",
    },
    "scala": {
        "category": "Programming Languages",
        "aliases": ["scala lang"],
        "demand_score": 68,
        "growth_rate": 10,
        "avg_salary": 125000,
        "description": "Functional and object-oriented programming on the JVM",
        "resources": [
            {"name": "Scala Tour", "url": "https://docs.scala-lang.org/tour/tour-of-scala.html", "type": "documentation"},
        ],
        "related": ["apache spark", "java", "functional programming"],
        "time_to_learn": "4-6 months",
    },

    # ─── Data Science & ML ───────────────────────────────────────────────────
    "machine learning": {
        "category": "Data Science & ML",
        "aliases": ["ml", "supervised learning", "unsupervised learning", "predictive modeling"],
        "demand_score": 94,
        "growth_rate": 38,
        "avg_salary": 125000,
        "description": "Algorithms that learn from data to make predictions",
        "resources": [
            {"name": "Andrew Ng ML Course", "url": "https://www.coursera.org/learn/machine-learning", "type": "course"},
            {"name": "fast.ai", "url": "https://www.fast.ai", "type": "course"},
            {"name": "Hands-On ML (O'Reilly)", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "type": "book"},
        ],
        "related": ["python", "scikit-learn", "tensorflow", "pytorch", "statistics"],
        "time_to_learn": "6-12 months",
    },
    "deep learning": {
        "category": "Data Science & ML",
        "aliases": ["dl", "neural networks", "ann", "cnn", "rnn", "lstm", "transformer"],
        "demand_score": 90,
        "growth_rate": 45,
        "avg_salary": 135000,
        "description": "Neural network-based machine learning",
        "resources": [
            {"name": "Deep Learning Specialization (Coursera)", "url": "https://www.coursera.org/specializations/deep-learning", "type": "course"},
            {"name": "fast.ai Deep Learning", "url": "https://www.fast.ai", "type": "course"},
        ],
        "related": ["tensorflow", "pytorch", "keras", "computer vision", "nlp"],
        "time_to_learn": "6-18 months",
    },
    "natural language processing": {
        "category": "Data Science & ML",
        "aliases": ["nlp", "text mining", "text analytics", "computational linguistics"],
        "demand_score": 88,
        "growth_rate": 52,
        "avg_salary": 128000,
        "description": "Processing and analyzing human language with computers",
        "resources": [
            {"name": "Hugging Face Course", "url": "https://huggingface.co/course", "type": "course"},
            {"name": "spaCy Course", "url": "https://course.spacy.io", "type": "course"},
            {"name": "NLTK Book", "url": "https://www.nltk.org/book/", "type": "book"},
        ],
        "related": ["transformers", "bert", "gpt", "spacy", "nltk"],
        "time_to_learn": "4-8 months",
    },
    "data analysis": {
        "category": "Data Science & ML",
        "aliases": ["data analytics", "data analyst", "exploratory data analysis", "eda"],
        "demand_score": 92,
        "growth_rate": 25,
        "avg_salary": 90000,
        "description": "Examining datasets to draw conclusions",
        "resources": [
            {"name": "Google Data Analytics (Coursera)", "url": "https://www.coursera.org/professional-certificates/google-data-analytics", "type": "course"},
            {"name": "Python for Data Analysis", "url": "https://wesmckinney.com/book/", "type": "book"},
        ],
        "related": ["pandas", "numpy", "matplotlib", "sql", "statistics"],
        "time_to_learn": "2-4 months",
    },
    "statistics": {
        "category": "Data Science & ML",
        "aliases": ["statistical analysis", "statistical modeling", "biostatistics", "bayesian statistics"],
        "demand_score": 85,
        "growth_rate": 18,
        "avg_salary": 95000,
        "description": "Mathematical analysis of data",
        "resources": [
            {"name": "Statistics and Probability (Khan Academy)", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "course"},
            {"name": "Think Stats", "url": "https://greenteapress.com/thinkstats2/html/", "type": "book"},
        ],
        "related": ["python", "r", "probability", "hypothesis testing"],
        "time_to_learn": "2-6 months",
    },
    "computer vision": {
        "category": "Data Science & ML",
        "aliases": ["cv", "image processing", "image recognition", "object detection"],
        "demand_score": 85,
        "growth_rate": 40,
        "avg_salary": 130000,
        "description": "Teaching computers to interpret visual data",
        "resources": [
            {"name": "CS231n Stanford", "url": "http://cs231n.stanford.edu", "type": "course"},
            {"name": "OpenCV Tutorials", "url": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html", "type": "tutorial"},
        ],
        "related": ["deep learning", "pytorch", "tensorflow", "opencv"],
        "time_to_learn": "6-12 months",
    },
    "large language models": {
        "category": "Data Science & ML",
        "aliases": ["llm", "llms", "gpt", "chatgpt", "generative ai", "gen ai", "foundation models"],
        "demand_score": 97,
        "growth_rate": 120,
        "avg_salary": 145000,
        "description": "Large-scale language models for generation and understanding",
        "resources": [
            {"name": "Hugging Face LLM Course", "url": "https://huggingface.co/course", "type": "course"},
            {"name": "LangChain Docs", "url": "https://docs.langchain.com", "type": "documentation"},
        ],
        "related": ["nlp", "transformers", "langchain", "prompt engineering"],
        "time_to_learn": "3-6 months",
    },

    # ─── Python Libraries ────────────────────────────────────────────────────
    "pandas": {
        "category": "Python Libraries",
        "aliases": ["pd", "pandas dataframe"],
        "demand_score": 90,
        "growth_rate": 20,
        "avg_salary": 105000,
        "description": "Data manipulation and analysis library for Python",
        "resources": [
            {"name": "Pandas Docs", "url": "https://pandas.pydata.org/docs/", "type": "documentation"},
            {"name": "Pandas Tutorial (Kaggle)", "url": "https://www.kaggle.com/learn/pandas", "type": "course"},
        ],
        "related": ["python", "numpy", "matplotlib", "data analysis"],
        "time_to_learn": "1-2 months",
    },
    "numpy": {
        "category": "Python Libraries",
        "aliases": ["np", "numpy arrays"],
        "demand_score": 88,
        "growth_rate": 15,
        "avg_salary": 105000,
        "description": "Numerical computing library for Python",
        "resources": [
            {"name": "NumPy Docs", "url": "https://numpy.org/doc/stable/", "type": "documentation"},
            {"name": "NumPy Tutorial", "url": "https://numpy.org/learn/", "type": "tutorial"},
        ],
        "related": ["python", "pandas", "scipy", "machine learning"],
        "time_to_learn": "2-4 weeks",
    },
    "scikit-learn": {
        "category": "Python Libraries",
        "aliases": ["sklearn", "scikit learn", "sk-learn"],
        "demand_score": 88,
        "growth_rate": 22,
        "avg_salary": 115000,
        "description": "Machine learning library for Python",
        "resources": [
            {"name": "scikit-learn Docs", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "documentation"},
            {"name": "Introduction to ML with Python", "url": "https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/", "type": "book"},
        ],
        "related": ["python", "numpy", "pandas", "machine learning"],
        "time_to_learn": "1-3 months",
    },
    "tensorflow": {
        "category": "Python Libraries",
        "aliases": ["tf", "tensorflow 2", "tensorflow2", "keras"],
        "demand_score": 87,
        "growth_rate": 18,
        "avg_salary": 128000,
        "description": "Open-source deep learning framework by Google",
        "resources": [
            {"name": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "tutorial"},
            {"name": "Hands-On ML (TF edition)", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "type": "book"},
        ],
        "related": ["keras", "deep learning", "python", "computer vision"],
        "time_to_learn": "3-6 months",
    },
    "pytorch": {
        "category": "Python Libraries",
        "aliases": ["torch", "py torch"],
        "demand_score": 89,
        "growth_rate": 40,
        "avg_salary": 132000,
        "description": "Open-source deep learning framework by Meta",
        "resources": [
            {"name": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "type": "tutorial"},
            {"name": "Deep Learning with PyTorch", "url": "https://pytorch.org/deep-learning-with-pytorch", "type": "book"},
        ],
        "related": ["deep learning", "python", "computer vision", "nlp"],
        "time_to_learn": "3-6 months",
    },
    "matplotlib": {
        "category": "Python Libraries",
        "aliases": ["plt", "mpl", "matplotlib pyplot"],
        "demand_score": 82,
        "growth_rate": 10,
        "avg_salary": 100000,
        "description": "Comprehensive library for creating visualizations in Python",
        "resources": [
            {"name": "Matplotlib Docs", "url": "https://matplotlib.org/stable/contents.html", "type": "documentation"},
            {"name": "Scientific Visualization: Python + Matplotlib", "url": "https://github.com/rougier/scientific-visualization-book", "type": "book"},
        ],
        "related": ["python", "seaborn", "plotly", "data visualization"],
        "time_to_learn": "2-4 weeks",
    },

    # ─── Cloud Platforms ─────────────────────────────────────────────────────
    "aws": {
        "category": "Cloud Platforms",
        "aliases": ["amazon web services", "amazon aws", "s3", "ec2", "lambda", "dynamodb", "redshift"],
        "demand_score": 93,
        "growth_rate": 25,
        "avg_salary": 128000,
        "description": "Amazon's comprehensive cloud computing platform",
        "resources": [
            {"name": "AWS Skill Builder", "url": "https://skillbuilder.aws", "type": "course"},
            {"name": "AWS Free Tier", "url": "https://aws.amazon.com/free/", "type": "tutorial"},
            {"name": "AWS Certified Solutions Architect", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "type": "certification"},
        ],
        "related": ["cloud computing", "devops", "terraform", "kubernetes"],
        "time_to_learn": "6-12 months",
    },
    "gcp": {
        "category": "Cloud Platforms",
        "aliases": ["google cloud", "google cloud platform", "bigquery", "gke", "cloud run"],
        "demand_score": 85,
        "growth_rate": 30,
        "avg_salary": 125000,
        "description": "Google's cloud computing platform",
        "resources": [
            {"name": "Google Cloud Skills Boost", "url": "https://cloudskillsboost.google", "type": "course"},
        ],
        "related": ["bigquery", "kubernetes", "cloud computing", "data engineering"],
        "time_to_learn": "4-8 months",
    },
    "azure": {
        "category": "Cloud Platforms",
        "aliases": ["microsoft azure", "ms azure", "azure cloud", "azure devops"],
        "demand_score": 88,
        "growth_rate": 22,
        "avg_salary": 122000,
        "description": "Microsoft's cloud computing platform",
        "resources": [
            {"name": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/azure/", "type": "course"},
            {"name": "AZ-900 Certification", "url": "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/", "type": "certification"},
        ],
        "related": ["cloud computing", "devops", "kubernetes", "active directory"],
        "time_to_learn": "4-8 months",
    },

    # ─── DevOps & Infrastructure ─────────────────────────────────────────────
    "docker": {
        "category": "DevOps",
        "aliases": ["containers", "containerization", "docker compose", "dockerfile"],
        "demand_score": 90,
        "growth_rate": 28,
        "avg_salary": 118000,
        "description": "Platform for building and running containerized applications",
        "resources": [
            {"name": "Docker Official Docs", "url": "https://docs.docker.com", "type": "documentation"},
            {"name": "Docker Mastery (Udemy)", "url": "https://www.udemy.com/course/docker-mastery/", "type": "course"},
        ],
        "related": ["kubernetes", "devops", "ci/cd", "microservices"],
        "time_to_learn": "1-3 months",
    },
    "kubernetes": {
        "category": "DevOps",
        "aliases": ["k8s", "k8", "kube", "orchestration"],
        "demand_score": 88,
        "growth_rate": 35,
        "avg_salary": 130000,
        "description": "Container orchestration platform",
        "resources": [
            {"name": "Kubernetes Docs", "url": "https://kubernetes.io/docs/", "type": "documentation"},
            {"name": "CKA Certification", "url": "https://www.cncf.io/certification/cka/", "type": "certification"},
        ],
        "related": ["docker", "devops", "cloud computing", "helm"],
        "time_to_learn": "3-6 months",
    },
    "terraform": {
        "category": "DevOps",
        "aliases": ["iac", "infrastructure as code", "tf"],
        "demand_score": 85,
        "growth_rate": 40,
        "avg_salary": 128000,
        "description": "Infrastructure as code tool",
        "resources": [
            {"name": "Terraform Docs", "url": "https://www.terraform.io/docs", "type": "documentation"},
            {"name": "Terraform Associate Certification", "url": "https://www.hashicorp.com/certification/terraform-associate", "type": "certification"},
        ],
        "related": ["aws", "gcp", "azure", "devops", "ansible"],
        "time_to_learn": "2-4 months",
    },
    "ci/cd": {
        "category": "DevOps",
        "aliases": ["continuous integration", "continuous deployment", "continuous delivery", "github actions", "jenkins", "gitlab ci", "circle ci"],
        "demand_score": 87,
        "growth_rate": 30,
        "avg_salary": 118000,
        "description": "Automated software delivery practices",
        "resources": [
            {"name": "GitHub Actions Docs", "url": "https://docs.github.com/en/actions", "type": "documentation"},
            {"name": "Jenkins Tutorial", "url": "https://www.jenkins.io/doc/tutorials/", "type": "tutorial"},
        ],
        "related": ["devops", "docker", "git", "testing"],
        "time_to_learn": "2-4 months",
    },
    "git": {
        "category": "DevOps",
        "aliases": ["github", "gitlab", "bitbucket", "version control", "git flow"],
        "demand_score": 95,
        "growth_rate": 8,
        "avg_salary": 95000,
        "description": "Distributed version control system",
        "resources": [
            {"name": "Pro Git Book", "url": "https://git-scm.com/book/en/v2", "type": "book"},
            {"name": "GitHub Learning Lab", "url": "https://lab.github.com", "type": "tutorial"},
        ],
        "related": ["github", "devops", "ci/cd", "open source"],
        "time_to_learn": "1-4 weeks",
    },

    # ─── Data Engineering ────────────────────────────────────────────────────
    "apache spark": {
        "category": "Data Engineering",
        "aliases": ["spark", "pyspark", "databricks"],
        "demand_score": 85,
        "growth_rate": 20,
        "avg_salary": 128000,
        "description": "Distributed computing framework for big data",
        "resources": [
            {"name": "Apache Spark Docs", "url": "https://spark.apache.org/docs/latest/", "type": "documentation"},
            {"name": "Databricks Academy", "url": "https://academy.databricks.com", "type": "course"},
        ],
        "related": ["scala", "python", "hadoop", "kafka", "data engineering"],
        "time_to_learn": "3-6 months",
    },
    "apache kafka": {
        "category": "Data Engineering",
        "aliases": ["kafka", "event streaming", "message queue", "confluent"],
        "demand_score": 82,
        "growth_rate": 30,
        "avg_salary": 125000,
        "description": "Distributed event streaming platform",
        "resources": [
            {"name": "Confluent Kafka Tutorials", "url": "https://developer.confluent.io/tutorials/", "type": "tutorial"},
        ],
        "related": ["apache spark", "data engineering", "microservices"],
        "time_to_learn": "2-4 months",
    },
    "airflow": {
        "category": "Data Engineering",
        "aliases": ["apache airflow", "workflow orchestration", "dag"],
        "demand_score": 80,
        "growth_rate": 28,
        "avg_salary": 122000,
        "description": "Platform to programmatically author, schedule and monitor workflows",
        "resources": [
            {"name": "Airflow Docs", "url": "https://airflow.apache.org/docs/", "type": "documentation"},
        ],
        "related": ["python", "data engineering", "etl", "apache spark"],
        "time_to_learn": "2-3 months",
    },
    "etl": {
        "category": "Data Engineering",
        "aliases": ["extract transform load", "data pipeline", "data integration", "dbt", "fivetran"],
        "demand_score": 83,
        "growth_rate": 22,
        "avg_salary": 112000,
        "description": "Extract, Transform, Load data pipeline processes",
        "resources": [
            {"name": "dbt Learn", "url": "https://learn.getdbt.com", "type": "course"},
        ],
        "related": ["sql", "airflow", "data warehouse", "python"],
        "time_to_learn": "2-4 months",
    },

    # ─── Databases ───────────────────────────────────────────────────────────
    "postgresql": {
        "category": "Databases",
        "aliases": ["postgres", "pg", "psql"],
        "demand_score": 88,
        "growth_rate": 15,
        "avg_salary": 105000,
        "description": "Advanced open-source relational database",
        "resources": [
            {"name": "PostgreSQL Docs", "url": "https://www.postgresql.org/docs/", "type": "documentation"},
            {"name": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com", "type": "tutorial"},
        ],
        "related": ["sql", "database design", "data engineering"],
        "time_to_learn": "1-3 months",
    },
    "mongodb": {
        "category": "Databases",
        "aliases": ["mongo", "nosql", "document database"],
        "demand_score": 82,
        "growth_rate": 18,
        "avg_salary": 108000,
        "description": "Document-oriented NoSQL database",
        "resources": [
            {"name": "MongoDB University", "url": "https://university.mongodb.com", "type": "course"},
        ],
        "related": ["nosql", "node.js", "database design"],
        "time_to_learn": "1-2 months",
    },
    "redis": {
        "category": "Databases",
        "aliases": ["redis cache", "in-memory database", "cache"],
        "demand_score": 80,
        "growth_rate": 20,
        "avg_salary": 110000,
        "description": "In-memory data structure store",
        "resources": [
            {"name": "Redis Docs", "url": "https://redis.io/documentation", "type": "documentation"},
            {"name": "Redis University", "url": "https://university.redis.com", "type": "course"},
        ],
        "related": ["caching", "database design", "microservices"],
        "time_to_learn": "2-4 weeks",
    },

    # ─── Web Frameworks ──────────────────────────────────────────────────────
    "react": {
        "category": "Web Frameworks",
        "aliases": ["reactjs", "react.js", "react hooks", "next.js", "nextjs"],
        "demand_score": 90,
        "growth_rate": 20,
        "avg_salary": 115000,
        "description": "JavaScript library for building user interfaces",
        "resources": [
            {"name": "React Docs", "url": "https://react.dev", "type": "documentation"},
            {"name": "React Tutorial (freeCodeCamp)", "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/#react", "type": "course"},
        ],
        "related": ["javascript", "typescript", "node.js", "redux"],
        "time_to_learn": "3-5 months",
    },
    "django": {
        "category": "Web Frameworks",
        "aliases": ["django rest framework", "drf", "django orm"],
        "demand_score": 80,
        "growth_rate": 12,
        "avg_salary": 108000,
        "description": "High-level Python web framework",
        "resources": [
            {"name": "Django Docs", "url": "https://docs.djangoproject.com", "type": "documentation"},
            {"name": "Django for Beginners", "url": "https://djangoforbeginners.com", "type": "book"},
        ],
        "related": ["python", "postgresql", "rest api", "docker"],
        "time_to_learn": "2-4 months",
    },
    "fastapi": {
        "category": "Web Frameworks",
        "aliases": ["fast api", "fastapi framework"],
        "demand_score": 83,
        "growth_rate": 55,
        "avg_salary": 115000,
        "description": "Modern, fast Python web framework for APIs",
        "resources": [
            {"name": "FastAPI Docs", "url": "https://fastapi.tiangolo.com", "type": "documentation"},
        ],
        "related": ["python", "pydantic", "docker", "rest api"],
        "time_to_learn": "1-2 months",
    },

    # ─── Data Visualization ──────────────────────────────────────────────────
    "data visualization": {
        "category": "Data Visualization",
        "aliases": ["dataviz", "tableau", "power bi", "looker", "grafana", "data studio"],
        "demand_score": 88,
        "growth_rate": 25,
        "avg_salary": 98000,
        "description": "Visual representation of data for insight communication",
        "resources": [
            {"name": "Tableau Public", "url": "https://public.tableau.com/app/learn/how-to-videos", "type": "tutorial"},
            {"name": "Power BI Learning", "url": "https://powerbi.microsoft.com/en-us/learning/", "type": "course"},
            {"name": "Plotly Documentation", "url": "https://plotly.com/python/", "type": "documentation"},
        ],
        "related": ["tableau", "power bi", "matplotlib", "plotly", "sql"],
        "time_to_learn": "2-4 months",
    },

    # ─── MLOps ───────────────────────────────────────────────────────────────
    "mlops": {
        "category": "MLOps",
        "aliases": ["ml ops", "ml engineering", "model deployment", "model serving", "mlflow", "kubeflow"],
        "demand_score": 88,
        "growth_rate": 65,
        "avg_salary": 135000,
        "description": "Practices for deploying and maintaining ML models in production",
        "resources": [
            {"name": "MLOps Zoomcamp", "url": "https://github.com/DataTalksClub/mlops-zoomcamp", "type": "course"},
            {"name": "MLflow Docs", "url": "https://mlflow.org/docs/latest/index.html", "type": "documentation"},
        ],
        "related": ["machine learning", "docker", "kubernetes", "ci/cd", "python"],
        "time_to_learn": "4-8 months",
    },
    "prompt engineering": {
        "category": "MLOps",
        "aliases": ["prompt design", "llm prompting", "chain of thought", "rag", "retrieval augmented generation"],
        "demand_score": 92,
        "growth_rate": 150,
        "avg_salary": 130000,
        "description": "Designing effective prompts for large language models",
        "resources": [
            {"name": "Prompt Engineering Guide", "url": "https://www.promptingguide.ai", "type": "tutorial"},
            {"name": "DeepLearning.AI Prompt Engineering", "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "type": "course"},
        ],
        "related": ["large language models", "nlp", "openai", "langchain"],
        "time_to_learn": "1-2 months",
    },

    # ─── Soft Skills ─────────────────────────────────────────────────────────
    "communication": {
        "category": "Soft Skills",
        "aliases": ["written communication", "verbal communication", "presentation skills", "storytelling"],
        "demand_score": 95,
        "growth_rate": 5,
        "avg_salary": 0,
        "description": "Ability to convey information effectively",
        "resources": [
            {"name": "Coursera Communication Skills", "url": "https://www.coursera.org/courses?query=communication%20skills", "type": "course"},
        ],
        "related": ["leadership", "collaboration", "problem solving"],
        "time_to_learn": "Ongoing",
    },
    "problem solving": {
        "category": "Soft Skills",
        "aliases": ["critical thinking", "analytical thinking", "troubleshooting", "debugging"],
        "demand_score": 97,
        "growth_rate": 8,
        "avg_salary": 0,
        "description": "Ability to analyze problems and develop solutions",
        "resources": [],
        "related": ["algorithms", "data structures", "communication"],
        "time_to_learn": "Ongoing",
    },
    "agile": {
        "category": "Project Management",
        "aliases": ["scrum", "kanban", "jira", "sprint", "agile methodology", "scrum master"],
        "demand_score": 85,
        "growth_rate": 12,
        "avg_salary": 95000,
        "description": "Iterative project management methodology",
        "resources": [
            {"name": "Scrum.org", "url": "https://www.scrum.org/resources", "type": "tutorial"},
            {"name": "Agile Manifesto", "url": "https://agilemanifesto.org", "type": "documentation"},
        ],
        "related": ["project management", "collaboration", "devops"],
        "time_to_learn": "1-2 months",
    },

    # ─── Security ────────────────────────────────────────────────────────────
    "cybersecurity": {
        "category": "Security",
        "aliases": ["security", "information security", "infosec", "penetration testing", "ethical hacking", "soc"],
        "demand_score": 90,
        "growth_rate": 35,
        "avg_salary": 115000,
        "description": "Protection of computer systems from digital attacks",
        "resources": [
            {"name": "CompTIA Security+", "url": "https://www.comptia.org/certifications/security", "type": "certification"},
            {"name": "TryHackMe", "url": "https://tryhackme.com", "type": "tutorial"},
        ],
        "related": ["networking", "linux", "python", "cloud security"],
        "time_to_learn": "6-12 months",
    },

    # ─── Networking & Systems ────────────────────────────────────────────────
    "linux": {
        "category": "Systems",
        "aliases": ["unix", "bash", "shell scripting", "command line", "linux administration"],
        "demand_score": 85,
        "growth_rate": 10,
        "avg_salary": 105000,
        "description": "Open-source operating system and scripting",
        "resources": [
            {"name": "Linux Command Line (William Shotts)", "url": "https://linuxcommand.org/tlcl.php", "type": "book"},
            {"name": "Bash Scripting Tutorial", "url": "https://linuxconfig.org/bash-scripting-tutorial", "type": "tutorial"},
        ],
        "related": ["devops", "docker", "cybersecurity", "system administration"],
        "time_to_learn": "1-3 months",
    },
    "api development": {
        "category": "Web Development",
        "aliases": ["rest api", "restful", "graphql", "api design", "microservices", "grpc"],
        "demand_score": 88,
        "growth_rate": 20,
        "avg_salary": 115000,
        "description": "Building and designing APIs for system integration",
        "resources": [
            {"name": "REST API Design Best Practices", "url": "https://restfulapi.net", "type": "tutorial"},
            {"name": "GraphQL Tutorial", "url": "https://graphql.org/learn/", "type": "documentation"},
        ],
        "related": ["fastapi", "django", "node.js", "microservices"],
        "time_to_learn": "2-4 months",
    },
}

# ─── Category summaries ───────────────────────────────────────────────────────

SKILL_CATEGORIES = list({v["category"] for v in SKILLS_DATABASE.values()})

TOP_CERTIFICATIONS = [
    {"name": "AWS Solutions Architect", "provider": "Amazon", "demand": 92, "salary_boost": "+$18k"},
    {"name": "Google Professional Data Engineer", "provider": "Google", "demand": 88, "salary_boost": "+$15k"},
    {"name": "CKA (Kubernetes Administrator)", "provider": "CNCF", "demand": 86, "salary_boost": "+$14k"},
    {"name": "Terraform Associate", "provider": "HashiCorp", "demand": 84, "salary_boost": "+$12k"},
    {"name": "TensorFlow Developer Certificate", "provider": "Google", "demand": 82, "salary_boost": "+$13k"},
    {"name": "Azure Data Scientist Associate", "provider": "Microsoft", "demand": 85, "salary_boost": "+$14k"},
    {"name": "Databricks Certified ML Professional", "provider": "Databricks", "demand": 81, "salary_boost": "+$16k"},
    {"name": "CompTIA Security+", "provider": "CompTIA", "demand": 83, "salary_boost": "+$10k"},
    {"name": "dbt Certified Analytics Engineer", "provider": "dbt Labs", "demand": 79, "salary_boost": "+$11k"},
    {"name": "MongoDB Developer", "provider": "MongoDB", "demand": 75, "salary_boost": "+$8k"},
]

INDUSTRY_DEMAND = {
    "Technology": {"python": 95, "javascript": 90, "cloud": 92, "ai/ml": 95, "devops": 88},
    "Finance": {"python": 88, "sql": 92, "risk modeling": 85, "big data": 80, "cybersecurity": 88},
    "Healthcare": {"python": 78, "sql": 85, "hl7 fhir": 70, "data privacy": 82, "statistics": 88},
    "E-commerce": {"javascript": 90, "python": 85, "recommendation systems": 82, "sql": 85, "docker": 80},
    "Manufacturing": {"python": 72, "iot": 80, "computer vision": 78, "robotics": 75, "plc": 68},
}


def get_all_skill_names() -> list[str]:
    """Return all skill names and their aliases as a flat list."""
    names = []
    for skill_name, skill_data in SKILLS_DATABASE.items():
        names.append(skill_name)
        names.extend(skill_data.get("aliases", []))
    return names


def get_skill_by_alias(term: str) -> str | None:
    """Map an alias/synonym back to the canonical skill name."""
    term_lower = term.lower().strip()
    for skill_name, skill_data in SKILLS_DATABASE.items():
        if term_lower == skill_name:
            return skill_name
        if term_lower in [a.lower() for a in skill_data.get("aliases", [])]:
            return skill_name
    return None


def get_trending_skills(top_n: int = 10) -> list[dict]:
    """Return top_n skills sorted by growth_rate descending."""
    return sorted(
        [{"skill": k, **v} for k, v in SKILLS_DATABASE.items()],
        key=lambda x: x.get("growth_rate", 0),
        reverse=True,
    )[:top_n]


def get_high_demand_skills(top_n: int = 10) -> list[dict]:
    """Return top_n skills sorted by demand_score descending."""
    return sorted(
        [{"skill": k, **v} for k, v in SKILLS_DATABASE.items()],
        key=lambda x: x.get("demand_score", 0),
        reverse=True,
    )[:top_n]
