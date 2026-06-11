import { Switch, Route, Router as WouterRouter } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "next-themes";
import NotFound from "@/pages/not-found";
import Landing from "@/pages/landing";
import Upload from "@/pages/upload";
import Dashboard from "@/pages/dashboard";
import AnalysisDetail from "@/pages/analysis-detail";
import Roadmap from "@/pages/roadmap";
import Market from "@/pages/market";
import Sources from "@/pages/sources";
import Resumes from "@/pages/resumes";
import Analyses from "@/pages/analyses";

const queryClient = new QueryClient();

function Router() {
  return (
    <Switch>
      <Route path="/" component={Landing} />
      <Route path="/upload" component={Upload} />
      <Route path="/dashboard" component={Dashboard} />
      <Route path="/analyses" component={Analyses} />
      <Route path="/analyses/:id" component={AnalysisDetail} />
      <Route path="/resumes" component={Resumes} />
      <Route path="/roadmap/:id" component={Roadmap} />
      <Route path="/market" component={Market} />
      <Route path="/sources/:id" component={Sources} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark">
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <WouterRouter base={import.meta.env.BASE_URL?.replace(/\/$/, "") || ""}>
            <Router />
          </WouterRouter>
          <Toaster theme="dark" position="top-right" />
        </TooltipProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

export default App;
