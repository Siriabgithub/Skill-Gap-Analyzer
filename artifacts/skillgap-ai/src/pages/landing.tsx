import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { motion, type Variants } from "framer-motion";
import { ArrowRight, BarChart3, Database, Shield, Target, Zap, ChevronRight } from "lucide-react";

export default function Landing() {
  const container: Variants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item: Variants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" as const } }
  };

  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary/30 font-sans">
      <nav className="fixed top-0 w-full border-b border-border/50 bg-background/80 backdrop-blur-md z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Target className="w-6 h-6 text-primary" />
            <span className="font-mono font-bold text-xl tracking-tight">SKILLGAP</span>
          </div>
          <div className="flex gap-4">
            <Link href="/dashboard">
              <Button variant="ghost" className="font-mono text-sm uppercase">Login</Button>
            </Link>
            <Link href="/upload">
              <Button className="font-mono text-sm uppercase rounded-none">Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="pt-24 pb-16">
        {/* Hero Section */}
        <section className="px-6 py-24 md:py-32 relative overflow-hidden flex flex-col items-center text-center">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-background to-background pointer-events-none" />
          
          <motion.div 
            className="max-w-4xl relative z-10 space-y-8"
            initial="hidden"
            animate="show"
            variants={container}
          >
            <motion.div variants={item} className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary text-secondary-foreground text-sm font-mono border border-border">
              <span className="flex h-2 w-2 rounded-full bg-primary animate-pulse" />
              Intelligence for Ambitious Professionals
            </motion.div>
            
            <motion.h1 variants={item} className="text-5xl md:text-7xl font-bold tracking-tighter leading-[1.1]">
              Know Exactly What Stands Between You and Your Dream Job.
            </motion.h1>
            
            <motion.p variants={item} className="text-xl text-muted-foreground max-w-2xl mx-auto">
              A precision tool for your career. We analyze your resume against market data and job descriptions to give you the truth, not encouragement.
            </motion.p>
            
            <motion.div variants={item} className="flex items-center justify-center gap-4 pt-4">
              <Link href="/upload">
                <Button size="lg" className="h-12 px-8 text-base font-mono uppercase rounded-none group">
                  Start Analysis 
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link href="/dashboard">
                <Button size="lg" variant="outline" className="h-12 px-8 text-base font-mono uppercase rounded-none">
                  View Demo
                </Button>
              </Link>
            </motion.div>
          </motion.div>
        </section>

        {/* Dense Data Section */}
        <section className="py-24 border-y border-border/50 bg-secondary/20">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid md:grid-cols-3 gap-12">
              <div className="space-y-4">
                <Database className="w-8 h-8 text-primary" />
                <h3 className="text-xl font-bold font-mono uppercase tracking-tight">Market Intelligence</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Real-time analysis against millions of data points from actual hiring processes. See the skills that actually matter right now.
                </p>
              </div>
              <div className="space-y-4">
                <Target className="w-8 h-8 text-primary" />
                <h3 className="text-xl font-bold font-mono uppercase tracking-tight">Precision Matching</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Deep parsing of your experience. We don't just keyword match; we understand the context and application of your skills.
                </p>
              </div>
              <div className="space-y-4">
                <Shield className="w-8 h-8 text-primary" />
                <h3 className="text-xl font-bold font-mono uppercase tracking-tight">Radical Transparency</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Every recommendation is backed by data. We show you exactly where our confidence scores come from.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Feature 1 */}
        <section className="py-24 px-6">
          <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-16 items-center">
            <div className="space-y-6 order-2 md:order-1">
              <div className="aspect-square bg-card border border-border relative overflow-hidden p-8 flex flex-col justify-between">
                <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:32px_32px]" />
                <div className="space-y-4 relative z-10">
                  <div className="h-4 w-3/4 bg-muted rounded" />
                  <div className="h-4 w-1/2 bg-muted rounded" />
                  <div className="h-4 w-5/6 bg-muted rounded" />
                </div>
                <div className="relative z-10 mt-12 grid grid-cols-2 gap-4">
                  <div className="h-24 bg-primary/10 border border-primary/20 rounded flex items-center justify-center font-mono text-primary text-xl">84%</div>
                  <div className="h-24 bg-destructive/10 border border-destructive/20 rounded flex items-center justify-center font-mono text-destructive text-xl">-12%</div>
                </div>
              </div>
            </div>
            <div className="space-y-8 order-1 md:order-2">
              <h2 className="text-4xl font-bold tracking-tighter">Your career as a terminal.</h2>
              <p className="text-xl text-muted-foreground">
                Stop guessing what hiring managers want. Get a dense, signal-rich view of your current standing in the market.
              </p>
              <ul className="space-y-4 font-mono text-sm">
                <li className="flex items-center gap-3"><ChevronRight className="w-4 h-4 text-primary"/> Algorithmic ATS scoring</li>
                <li className="flex items-center gap-3"><ChevronRight className="w-4 h-4 text-primary"/> Required vs Missing skills matrix</li>
                <li className="flex items-center gap-3"><ChevronRight className="w-4 h-4 text-primary"/> Experience density analysis</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Action CTA */}
        <section className="py-32 px-6 bg-primary text-primary-foreground text-center">
          <div className="max-w-3xl mx-auto space-y-8">
            <h2 className="text-5xl font-bold tracking-tighter">Stop guessing. Start executing.</h2>
            <p className="text-xl opacity-90">
              Upload your resume and the job description you want. Get the truth in seconds.
            </p>
            <Link href="/upload">
              <Button size="lg" variant="secondary" className="h-14 px-10 text-lg font-mono uppercase rounded-none mt-8 text-primary hover:bg-secondary/90">
                Analyze My Resume
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="py-8 px-6 border-t border-border/50 text-center text-sm text-muted-foreground font-mono">
        <p>© {new Date().getFullYear()} SkillGap AI. Built for professionals.</p>
      </footer>
    </div>
  );
}
