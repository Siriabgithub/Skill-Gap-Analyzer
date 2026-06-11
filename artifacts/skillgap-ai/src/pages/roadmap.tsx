import { useParams, Link } from "wouter";
import { AppLayout } from "@/components/layout/AppLayout";
import { useGetAnalysisRoadmap } from "@workspace/api-client-react";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Clock, BookOpen, ChevronRight, ExternalLink } from "lucide-react";
import { getGetAnalysisRoadmapQueryKey } from "@workspace/api-client-react";

export default function Roadmap() {
  const { id } = useParams<{ id: string }>();
  const analysisId = parseInt(id || "0", 10);
  
  const { data: roadmap, isLoading, isError } = useGetAnalysisRoadmap(analysisId, {
    query: {
      enabled: !!analysisId,
      queryKey: getGetAnalysisRoadmapQueryKey(analysisId)
    }
  });

  if (isLoading) {
    return (
      <AppLayout>
        <div className="space-y-8 max-w-4xl mx-auto">
          <Skeleton className="h-12 w-1/3" />
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <Skeleton key={i} className="h-32" />
            ))}
          </div>
        </div>
      </AppLayout>
    );
  }

  if (isError || !roadmap) {
    return (
      <AppLayout>
        <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-destructive" />
          <h2 className="text-2xl font-bold tracking-tight">Roadmap Not Found</h2>
          <p className="text-muted-foreground">The learning roadmap could not be loaded.</p>
          <Link href={`/analyses/${analysisId}`}>
            <Button variant="outline">Return to Analysis</Button>
          </Link>
        </div>
      </AppLayout>
    );
  }

  const phases = [
    { title: "First 30 Days: Critical Gaps", items: roadmap.thirtyDayPlan, color: "border-destructive" },
    { title: "Day 31-60: Core Competencies", items: roadmap.sixtyDayPlan, color: "border-primary" },
    { title: "Day 61-90: Mastery & Polish", items: roadmap.ninetyDayPlan, color: "border-muted-foreground" },
  ];

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-12 pb-24">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Link href={`/analyses/${analysisId}`} className="text-sm font-mono text-muted-foreground hover:text-foreground transition-colors flex items-center">
              Analysis #{analysisId} <ChevronRight className="w-3 h-3 mx-1" /> Roadmap
            </Link>
          </div>
          <h1 className="text-3xl font-bold font-mono tracking-tight uppercase">Execution Plan</h1>
          <p className="text-muted-foreground mt-2">A structured timeline to acquire your missing skills.</p>
        </div>

        <div className="relative pl-6 md:pl-0">
          <div className="absolute left-6 top-0 bottom-0 w-px bg-border md:left-1/2 md:-ml-px hidden md:block" />
          
          <div className="space-y-16">
            {phases.map((phase, phaseIndex) => (
              <div key={phaseIndex} className="relative">
                <div className="sticky top-20 z-10 bg-background/95 backdrop-blur py-4 mb-8 md:text-center">
                  <h2 className="text-xl font-bold font-mono uppercase tracking-widest inline-flex items-center gap-3 px-4 py-2 bg-secondary border border-border rounded-sm">
                    <div className={`w-2 h-2 rounded-full bg-current ${phase.color.replace('border-', 'text-')}`} />
                    {phase.title}
                  </h2>
                </div>

                <div className="space-y-6">
                  {phase.items?.map((item, itemIndex) => (
                    <div key={itemIndex} className={`relative flex flex-col md:flex-row gap-6 md:justify-between ${itemIndex % 2 === 0 ? 'md:flex-row-reverse' : ''}`}>
                      <div className="absolute -left-8 md:left-1/2 md:-ml-[5px] top-6 w-[10px] h-[10px] rounded-full bg-background border-2 border-primary z-10" />
                      
                      <div className="md:w-[45%]">
                        <Card className={`bg-card/50 backdrop-blur-sm border-l-4 ${phase.color} border-y-border/50 border-r-border/50 hover:bg-card/80 transition-colors`}>
                          <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                              <div>
                                <h3 className="text-lg font-bold text-foreground">{item.skill}</h3>
                                <div className="flex items-center gap-2 mt-1">
                                  <Badge variant="outline" className="font-mono text-[10px] uppercase">{item.category}</Badge>
                                  <span className="text-xs text-muted-foreground flex items-center font-mono">
                                    <Clock className="w-3 h-3 mr-1" /> {item.estimatedHours}h
                                  </span>
                                </div>
                              </div>
                            </div>
                            
                            <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
                              {item.description}
                            </p>

                            <div className="space-y-3">
                              <h4 className="text-xs font-mono uppercase text-foreground/70 flex items-center gap-2">
                                <BookOpen className="w-3 h-3" /> Recommended Resources
                              </h4>
                              <div className="space-y-2">
                                {item.resources.map((res, i) => (
                                  <a 
                                    key={i} 
                                    href={res.url} 
                                    target="_blank" 
                                    rel="noreferrer"
                                    className="flex items-start justify-between p-2 rounded bg-background/50 border border-border/30 hover:border-primary/50 transition-colors group"
                                  >
                                    <div className="flex flex-col">
                                      <span className="text-sm font-medium group-hover:text-primary transition-colors line-clamp-1">{res.title}</span>
                                      <span className="text-[10px] text-muted-foreground font-mono uppercase">{res.provider} • {res.type} {res.isFree && '• FREE'}</span>
                                    </div>
                                    <ExternalLink className="w-4 h-4 text-muted-foreground opacity-50 group-hover:opacity-100 group-hover:text-primary transition-all shrink-0 mt-0.5" />
                                  </a>
                                ))}
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </div>
                      
                      <div className="hidden md:block md:w-[45%]" />
                    </div>
                  ))}
                  
                  {(!phase.items || phase.items.length === 0) && (
                    <div className="text-center py-8 text-muted-foreground border border-dashed border-border rounded-lg md:w-[45%] mx-auto">
                      No items scheduled for this phase.
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
