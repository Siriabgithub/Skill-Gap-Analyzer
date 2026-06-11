import { Link, useLocation } from "wouter";
import { 
  LayoutDashboard, 
  Upload, 
  TrendingUp, 
  Settings, 
  LogOut,
  Target,
  FileText,
  Activity
} from "lucide-react";
import { cn } from "@/lib/utils";

interface AppLayoutProps {
  children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const [location] = useLocation();

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "New Analysis", href: "/upload", icon: Upload },
    { name: "Analyses", href: "/analyses", icon: Activity },
    { name: "Resumes", href: "/resumes", icon: FileText },
    { name: "Market Trends", href: "/market", icon: TrendingUp },
  ];

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden font-sans">
      <aside className="w-64 border-r border-border bg-sidebar flex flex-col justify-between hidden md:flex">
        <div className="p-6">
          <Link href="/dashboard" className="flex items-center gap-2 mb-8">
            <Target className="w-6 h-6 text-primary" />
            <span className="font-mono font-bold text-xl tracking-tight text-foreground">SKILLGAP</span>
          </Link>
          
          <nav className="space-y-1">
            {navigation.map((item) => {
              const isActive = location === item.href || (item.href !== '/' && location.startsWith(`${item.href}/`));
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors font-mono uppercase tracking-wide",
                    isActive 
                      ? "bg-sidebar-accent text-primary font-bold border-l-2 border-primary" 
                      : "text-sidebar-foreground hover:bg-sidebar-accent/50 hover:text-foreground border-l-2 border-transparent"
                  )}
                >
                  <item.icon className="w-4 h-4" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
        
        <div className="p-6 border-t border-sidebar-border">
          <nav className="space-y-1">
            <Link
              href="/"
              className="flex items-center gap-3 px-3 py-2 rounded-md text-sm text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors font-mono uppercase tracking-wide border-l-2 border-transparent"
            >
              <LogOut className="w-4 h-4" />
              Exit App
            </Link>
          </nav>
        </div>
      </aside>
      
      <main className="flex-1 flex flex-col overflow-hidden bg-background">
        <header className="h-16 border-b border-border flex items-center px-6 md:hidden">
          <Link href="/dashboard" className="flex items-center gap-2">
            <Target className="w-6 h-6 text-primary" />
            <span className="font-mono font-bold text-lg tracking-tight">SKILLGAP</span>
          </Link>
        </header>
        <div className="flex-1 overflow-y-auto p-6 md:p-10 relative">
          <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/5 via-background to-background" />
          <div className="relative z-10 max-w-7xl mx-auto">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
