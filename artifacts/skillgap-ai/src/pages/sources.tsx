import { useParams, Link } from "wouter";
import { AppLayout } from "@/components/layout/AppLayout";
import { useGetAnalysisSources } from "@workspace/api-client-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Database, CheckCircle2, ChevronLeft } from "lucide-react";
import { getGetAnalysisSourcesQueryKey } from "@workspace/api-client-react";

export default function Sources() {
  const { id } = useParams<{ id: string }>();
  const analysisId = parseInt(id || "0", 10);
  
  const { data: sources, isLoading, isError } = useGetAnalysisSources(analysisId, {
    query: {
      enabled: !!analysisId,
      queryKey: getGetAnalysisSourcesQueryKey(analysisId)
    }
  });

  if (isLoading) {
    return (
      <AppLayout>
        <div className="space-y-8 max-w-4xl mx-auto">
          <Skeleton className="h-12 w-1/3" />
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <Skeleton key={i} className="h-24" />
            ))}
          </div>
        </div>
      </AppLayout>
    );
  }

  if (isError || !sources) {
    return (
      <AppLayout>
        <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-destructive" />
          <h2 className="text-2xl font-bold tracking-tight">Sources Not Found</h2>
          <p className="text-muted-foreground">Could not load the provenance data for this analysis.</p>
          <Link href={`/analyses/${analysisId}`} className="text-primary hover:underline">
            Return to Analysis
          </Link>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-8 pb-12">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Link href={`/analyses/${analysisId}`} className="text-sm font-mono text-muted-foreground hover:text-foreground transition-colors flex items-center">
              <ChevronLeft className="w-4 h-4 mr-1" /> Back to Analysis #{analysisId}
            </Link>
          </div>
          <h1 className="text-3xl font-bold font-mono tracking-tight uppercase flex items-center gap-3">
            <Database className="w-8 h-8 text-primary" /> Data Provenance
          </h1>
          <p className="text-muted-foreground mt-2">The exact sources and confidence levels behind our analysis models.</p>
        </div>

        <div className="space-y-4">
          {sources.map((source, i) => (
            <Card key={i} className="bg-card/50 backdrop-blur-sm border-border/50">
              <CardContent className="p-6">
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-bold text-foreground">{source.name}</h3>
                      {source.confidenceScore > 90 && (
                        <Badge variant="outline" className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20 font-mono text-[10px] uppercase">
                          <CheckCircle2 className="w-3 h-3 mr-1" /> Verified
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed max-w-2xl">
                      {source.description}
                    </p>
                    <div className="flex items-center gap-4 mt-4 pt-4 border-t border-border/30">
                      <div className="text-xs font-mono">
                        <span className="text-muted-foreground uppercase">Category:</span>{" "}
                        <span className="text-foreground">{source.category || 'General'}</span>
                      </div>
                      <div className="text-xs font-mono">
                        <span className="text-muted-foreground uppercase">Last Updated:</span>{" "}
                        <span className="text-foreground">{new Date(source.lastUpdated).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex flex-col items-end shrink-0 sm:pl-6 sm:border-l border-border/30">
                    <div className="text-3xl font-bold tracking-tighter text-primary">
                      {source.confidenceScore}%
                    </div>
                    <div className="text-[10px] text-muted-foreground font-mono uppercase tracking-widest mt-1">
                      Confidence
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="p-4 bg-secondary/30 rounded-lg border border-border/50 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-muted-foreground shrink-0 mt-0.5" />
          <p className="text-sm text-muted-foreground">
            SkillGap AI uses an ensemble approach. The final recommendations in your analysis are synthesized across these sources, weighted by their confidence scores for your specific industry.
          </p>
        </div>
      </div>
    </AppLayout>
  );
}
