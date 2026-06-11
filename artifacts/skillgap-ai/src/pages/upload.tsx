import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { UploadCloud, FileText, CheckCircle2, ArrowRight, Loader2, X } from "lucide-react";
import { useUploadResume, useCreateAnalysis } from "@workspace/api-client-react";
import { useLocation } from "wouter";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

export default function Upload() {
  const [, setLocation] = useLocation();
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeId, setResumeId] = useState<number | null>(null);

  const uploadResume = useUploadResume();
  const createAnalysis = useCreateAnalysis();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      
      // Auto-upload
      uploadResume.mutate(
        { data: { file: selectedFile } },
        {
          onSuccess: (data) => {
            setResumeId(data.id);
            toast.success("Resume uploaded successfully");
          },
          onError: () => {
            toast.error("Failed to upload resume");
            setFile(null);
          }
        }
      );
    }
  };

  const handleAnalyze = () => {
    if (!resumeId) {
      toast.error("Please upload a resume first");
      return;
    }
    if (!jobDescription) {
      toast.error("Please provide a job description");
      return;
    }

    createAnalysis.mutate(
      {
        data: {
          resumeId,
          jobDescription,
          jobTitle: jobTitle || undefined
        }
      },
      {
        onSuccess: (data) => {
          toast.success("Analysis started");
          setLocation(`/analyses/${data.id}`);
        },
        onError: () => {
          toast.error("Failed to start analysis");
        }
      }
    );
  };

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold font-mono uppercase tracking-tight">New Analysis</h1>
          <p className="text-muted-foreground mt-2">Upload your current resume and the target job description to reveal the gap.</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">1. Source Data</CardTitle>
              <CardDescription>Upload your resume (PDF/DOCX)</CardDescription>
            </CardHeader>
            <CardContent>
              <AnimatePresence mode="wait">
                {!file ? (
                  <motion.div 
                    key="upload"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="border-2 border-dashed border-border rounded-lg p-12 text-center hover:border-primary/50 transition-colors cursor-pointer relative"
                  >
                    <input 
                      type="file" 
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      accept=".pdf,.doc,.docx"
                      onChange={handleFileChange}
                      disabled={uploadResume.isPending}
                    />
                    <div className="flex flex-col items-center space-y-4">
                      <div className="p-4 bg-primary/10 rounded-full text-primary">
                        {uploadResume.isPending ? <Loader2 className="w-8 h-8 animate-spin" /> : <UploadCloud className="w-8 h-8" />}
                      </div>
                      <div>
                        <p className="font-medium text-foreground">Click or drag file to upload</p>
                        <p className="text-sm text-muted-foreground mt-1">PDF, DOCX up to 10MB</p>
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div 
                    key="file"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="border border-primary/30 bg-primary/5 rounded-lg p-6 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-4">
                      <div className="p-3 bg-primary/20 rounded-full text-primary">
                        <FileText className="w-6 h-6" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground truncate max-w-[200px]">{file.name}</p>
                        <p className="text-sm text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </div>
                    {uploadResume.isPending ? (
                      <Loader2 className="w-5 h-5 text-primary animate-spin" />
                    ) : (
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                        <Button variant="ghost" size="icon" onClick={() => { setFile(null); setResumeId(null); }} className="h-8 w-8 text-muted-foreground hover:text-destructive">
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </CardContent>
          </Card>

          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">2. Target Vector</CardTitle>
              <CardDescription>Define the role you are aiming for</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="title" className="font-mono text-xs text-muted-foreground uppercase">Target Title (Optional)</Label>
                <Input 
                  id="title" 
                  placeholder="e.g. Senior Frontend Engineer" 
                  value={jobTitle}
                  onChange={e => setJobTitle(e.target.value)}
                  className="bg-background/50"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="jd" className="font-mono text-xs text-muted-foreground uppercase">Job Description</Label>
                <Textarea 
                  id="jd" 
                  placeholder="Paste the full job description here..." 
                  className="min-h-[200px] bg-background/50 resize-none font-sans text-sm"
                  value={jobDescription}
                  onChange={e => setJobDescription(e.target.value)}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="flex justify-end">
          <Button 
            size="lg" 
            className="h-14 px-8 font-mono uppercase tracking-wider rounded-none min-w-[200px]"
            onClick={handleAnalyze}
            disabled={!resumeId || !jobDescription || createAnalysis.isPending}
          >
            {createAnalysis.isPending ? (
              <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Processing...</>
            ) : (
              <>Initiate Analysis <ArrowRight className="ml-2 w-5 h-5" /></>
            )}
          </Button>
        </div>
      </div>
    </AppLayout>
  );
}
