import { AppLayout } from "@/components/layout/AppLayout";
import { useListAnalyses, useDeleteAnalysis, getListAnalysesQueryKey } from "@workspace/api-client-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Target, Trash2, Loader2, ArrowRight } from "lucide-react";
import { format } from "date-fns";
import { toast } from "sonner";
import { useQueryClient } from "@tanstack/react-query";
import { Link } from "wouter";

export default function Analyses() {
  const { data: analyses, isLoading } = useListAnalyses();
  const deleteAnalysis = useDeleteAnalysis();
  const queryClient = useQueryClient();

  const handleDelete = (id: number) => {
    deleteAnalysis.mutate({ id }, {
      onSuccess: () => {
        toast.success("Analysis deleted");
        queryClient.invalidateQueries({ queryKey: getListAnalysesQueryKey() });
      },
      onError: () => toast.error("Failed to delete analysis")
    });
  };

  return (
    <AppLayout>
      <div className="space-y-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold font-mono uppercase tracking-tight">Analysis History</h1>
            <p className="text-muted-foreground mt-2">Review your past skill gap analyses and targeted roles.</p>
          </div>
          <Link href="/upload">
            <Button className="font-mono text-xs uppercase rounded-none">New Analysis</Button>
          </Link>
        </div>

        <div className="space-y-4">
          {isLoading ? (
            [...Array(4)].map((_, i) => <Skeleton key={i} className="h-24 w-full rounded-xl" />)
          ) : analyses?.length ? (
            analyses.map(analysis => (
              <Card key={analysis.id} className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/50 transition-all group">
                <CardContent className="p-0">
                  <div className="flex flex-col md:flex-row md:items-center justify-between p-4 md:p-6 gap-4">
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-secondary rounded-lg shrink-0">
                        <Target className="w-6 h-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold text-foreground truncate max-w-[300px] md:max-w-md">
                          {analysis.jobTitle || `Analysis #${analysis.id}`}
                        </h3>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-xs font-mono text-muted-foreground">
                            {format(new Date(analysis.createdAt), "MMM d, yyyy")}
                          </span>
                          <Badge variant="outline" className={`font-mono text-[10px] uppercase ${analysis.status === 'completed' ? 'text-emerald-500 border-emerald-500/30' : 'text-amber-500 border-amber-500/30'}`}>
                            {analysis.status}
                          </Badge>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-6 md:gap-8 self-start md:self-auto border-t md:border-t-0 md:border-l border-border/50 pt-4 md:pt-0 md:pl-6 w-full md:w-auto">
                      <div className="flex flex-col items-center">
                        <span className="text-xl font-bold text-primary font-mono">{analysis.atsScore || 0}%</span>
                        <span className="text-[10px] uppercase font-mono text-muted-foreground tracking-wider">ATS Score</span>
                      </div>
                      <div className="flex flex-col items-center">
                        <span className="text-xl font-bold font-mono">{analysis.matchScore || 0}%</span>
                        <span className="text-[10px] uppercase font-mono text-muted-foreground tracking-wider">Match</span>
                      </div>
                      
                      <div className="flex-1 md:flex-none flex justify-end gap-2 ml-auto">
                        <Link href={`/analyses/${analysis.id}`}>
                          <Button variant="outline" size="sm" className="font-mono text-xs uppercase hidden sm:flex">
                            View Details
                          </Button>
                        </Link>
                        <Link href={`/analyses/${analysis.id}`}>
                          <Button size="icon" variant="ghost" className="sm:hidden text-primary">
                            <ArrowRight className="w-4 h-4" />
                          </Button>
                        </Link>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="text-muted-foreground hover:text-destructive shrink-0"
                          onClick={() => handleDelete(analysis.id)}
                          disabled={deleteAnalysis.isPending}
                        >
                          {deleteAnalysis.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="py-16 text-center border border-dashed border-border rounded-lg bg-background/50">
              <p className="text-muted-foreground mb-4">No analyses found.</p>
              <Link href="/upload">
                <Button variant="outline">Create Your First Analysis</Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
