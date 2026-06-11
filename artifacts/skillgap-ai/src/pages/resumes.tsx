import { AppLayout } from "@/components/layout/AppLayout";
import { useListResumes, useDeleteResume, getListResumesQueryKey } from "@workspace/api-client-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { FileText, Trash2, Loader2, AlertCircle } from "lucide-react";
import { format } from "date-fns";
import { toast } from "sonner";
import { useQueryClient } from "@tanstack/react-query";
import { Link } from "wouter";

export default function Resumes() {
  const { data: resumes, isLoading } = useListResumes();
  const deleteResume = useDeleteResume();
  const queryClient = useQueryClient();

  const handleDelete = (id: number) => {
    deleteResume.mutate({ id }, {
      onSuccess: () => {
        toast.success("Resume deleted");
        queryClient.invalidateQueries({ queryKey: getListResumesQueryKey() });
      },
      onError: () => toast.error("Failed to delete resume")
    });
  };

  return (
    <AppLayout>
      <div className="space-y-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold font-mono uppercase tracking-tight">Source Documents</h1>
            <p className="text-muted-foreground mt-2">Manage your uploaded resumes and source materials.</p>
          </div>
          <Link href="/upload">
            <Button className="font-mono text-xs uppercase rounded-none">Upload New</Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? (
            [...Array(3)].map((_, i) => <Skeleton key={i} className="h-40 rounded-xl" />)
          ) : resumes?.length ? (
            resumes.map(resume => (
              <Card key={resume.id} className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/30 transition-colors">
                <CardContent className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-primary/10 rounded text-primary">
                        <FileText className="w-6 h-6" />
                      </div>
                      <div>
                        <h3 className="font-medium truncate max-w-[150px]" title={resume.originalName}>
                          {resume.originalName}
                        </h3>
                        <p className="text-xs text-muted-foreground font-mono mt-1">
                          {format(new Date(resume.createdAt), "MMM d, yyyy")}
                        </p>
                      </div>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="text-muted-foreground hover:text-destructive h-8 w-8"
                      onClick={() => handleDelete(resume.id)}
                      disabled={deleteResume.isPending}
                    >
                      {deleteResume.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                    </Button>
                  </div>
                  
                  <div className="flex justify-between items-end mt-6">
                    <Badge variant="outline" className={`font-mono text-[10px] uppercase ${resume.status === 'ready' ? 'text-emerald-500 border-emerald-500/30' : 'text-amber-500 border-amber-500/30'}`}>
                      {resume.status}
                    </Badge>
                    <div className="text-xs text-muted-foreground">
                      {resume.skills?.length || 0} skills extracted
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="col-span-full py-12 flex flex-col items-center justify-center border border-dashed border-border rounded-lg bg-background/50">
              <AlertCircle className="w-12 h-12 text-muted-foreground mb-4 opacity-50" />
              <p className="text-muted-foreground mb-4">No source documents found.</p>
              <Link href="/upload">
                <Button variant="outline">Upload Resume</Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
