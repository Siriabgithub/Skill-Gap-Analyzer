import { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { UploadCloud, FileText, CheckCircle2, ArrowRight, Loader2, X, AlertCircle } from "lucide-react";
import { useUploadResume, useCreateAnalysis, useGetResume, ResumeStatus, getGetResumeQueryKey } from "@workspace/api-client-react";
import { useLocation } from "wouter";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

type ParseState = "idle" | "uploading" | "processing" | "ready" | "error";

export default function Upload() {
  const [, setLocation] = useLocation();
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [parseState, setParseState] = useState<ParseState>("idle");

  const uploadResume = useUploadResume();
  const createAnalysis = useCreateAnalysis();

  // Poll GET /resumes/:id every second until status is ready or error
  const { data: polledResume } = useGetResume(resumeId ?? 0, {
    query: {
      queryKey: getGetResumeQueryKey(resumeId ?? 0),
      enabled: resumeId !== null && (parseState === "processing" || parseState === "uploading"),
      refetchInterval: (query) => {
        const status = (query.state.data as { status?: string } | undefined)?.status;
        if (status === ResumeStatus.ready || status === ResumeStatus.error) return false;
        return 1000;
      },
    },
  });

  // React to polled status changes (onSuccess removed in React Query v5)
  useEffect(() => {
    if (!polledResume) return;
    if (polledResume.status === ResumeStatus.ready && parseState !== "ready") {
      setParseState("ready");
    } else if (polledResume.status === ResumeStatus.error && parseState !== "error") {
      setParseState("error");
      toast.error("Resume parsing failed — please try a different file");
    }
  }, [polledResume?.status]);

  const isReady = parseState === "ready";

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setParseState("uploading");
      setResumeId(null);

      uploadResume.mutate(
        { data: { file: selectedFile } },
        {
          onSuccess: (data) => {
            setResumeId(data.id);
            setParseState("processing");
          },
          onError: (err) => {
            const apiErr = err as { response?: { data?: { error?: string } } };
            const msg = apiErr?.response?.data?.error ?? "Failed to upload resume";
            toast.error(msg);
            setFile(null);
            setParseState("idle");
          },
        }
      );
    }
  };

  const handleAnalyze = () => {
    if (!resumeId || !isReady) {
      toast.error("Please wait for resume processing to complete");
      return;
    }
    if (!jobDescription.trim()) {
      toast.error("Please provide a job description");
      return;
    }

    createAnalysis.mutate(
      {
        data: {
          resumeId,
          jobDescription,
          jobTitle: jobTitle.trim() || undefined,
        },
      },
      {
        onSuccess: (data) => {
          toast.success("Analysis complete");
          setLocation(`/analyses/${data.id}`);
        },
        onError: (err) => {
          const apiErr = err as { response?: { data?: { error?: string } } };
          const msg = apiErr?.response?.data?.error ?? "Failed to start analysis";
          toast.error(msg);
        },
      }
    );
  };

  const handleRemoveFile = () => {
    setFile(null);
    setResumeId(null);
    setParseState("idle");
  };

  const stateLabel: Record<ParseState, string> = {
    idle: "",
    uploading: "Uploading...",
    processing: "Parsing resume...",
    ready: "Ready",
    error: "Parsing failed",
  };

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold font-mono uppercase tracking-tight">New Analysis</h1>
          <p className="text-muted-foreground mt-2">Upload your current resume and the target job description to reveal the gap.</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Resume Upload Card */}
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">1. Source Data</CardTitle>
              <CardDescription>Upload your resume (PDF/DOCX)</CardDescription>
            </CardHeader>
            <CardContent>
              <AnimatePresence mode="wait">
                {!file ? (
                  <motion.div
                    key="dropzone"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="border-2 border-dashed border-border rounded-lg p-12 text-center hover:border-primary/50 transition-colors cursor-pointer relative"
                  >
                    <input
                      type="file"
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                      disabled={parseState === "uploading"}
                    />
                    <div className="flex flex-col items-center space-y-4">
                      <div className="p-4 bg-primary/10 rounded-full text-primary">
                        <UploadCloud className="w-8 h-8" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">Click or drag file to upload</p>
                        <p className="text-sm text-muted-foreground mt-1">PDF, DOCX up to 10MB</p>
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="fileinfo"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="space-y-3"
                  >
                    <div className={`border rounded-lg p-5 flex items-center justify-between ${
                      parseState === "error"
                        ? "border-destructive/50 bg-destructive/5"
                        : isReady
                        ? "border-primary/30 bg-primary/5"
                        : "border-border/50 bg-muted/20"
                    }`}>
                      <div className="flex items-center gap-3 min-w-0">
                        <div className={`p-2.5 rounded-full shrink-0 ${
                          parseState === "error" ? "bg-destructive/20 text-destructive" :
                          isReady ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"
                        }`}>
                          <FileText className="w-5 h-5" />
                        </div>
                        <div className="min-w-0">
                          <p className="font-medium text-foreground truncate">{file.name}</p>
                          <p className="text-xs text-muted-foreground font-mono">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-1 shrink-0 ml-2">
                        {(parseState === "uploading" || parseState === "processing") ? (
                          <Loader2 className="w-5 h-5 text-primary animate-spin" />
                        ) : parseState === "error" ? (
                          <AlertCircle className="w-5 h-5 text-destructive" />
                        ) : (
                          <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                        )}
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={handleRemoveFile}
                          className="h-8 w-8 text-muted-foreground hover:text-destructive"
                          disabled={parseState === "uploading"}
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>

                    {parseState !== "idle" && (
                      <p className={`text-xs font-mono px-1 flex items-center gap-1.5 ${
                        parseState === "error" ? "text-destructive" :
                        isReady ? "text-emerald-500" : "text-muted-foreground"
                      }`}>
                        {(parseState === "uploading" || parseState === "processing") && (
                          <Loader2 className="w-3 h-3 animate-spin" />
                        )}
                        {stateLabel[parseState]}
                      </p>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </CardContent>
          </Card>

          {/* Job Description Card */}
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

        {/* Footer row: hint + action button */}
        <div className="flex items-center justify-between">
          <div className="text-sm font-mono text-muted-foreground">
            {parseState === "processing" && (
              <span className="flex items-center gap-2">
                <Loader2 className="w-3 h-3 animate-spin" />
                Parsing resume — wait before analyzing
              </span>
            )}
            {parseState === "error" && (
              <span className="flex items-center gap-2 text-destructive">
                <AlertCircle className="w-3 h-3" />
                Resume parsing failed — try a different file
              </span>
            )}
          </div>

          <Button
            size="lg"
            className="h-14 px-8 font-mono uppercase tracking-wider rounded-none min-w-[220px]"
            onClick={handleAnalyze}
            disabled={!isReady || !jobDescription.trim() || createAnalysis.isPending}
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
