import { useParams, Link } from "wouter";
import { AppLayout } from "@/components/layout/AppLayout";
import { useGetAnalysis } from "@workspace/api-client-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { AlertCircle, Target, Map, ArrowRight, ShieldCheck } from "lucide-react";
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";
import { getGetAnalysisQueryKey } from "@workspace/api-client-react";
import { useEffect, useState } from "react";

export default function AnalysisDetail() {
  const { id } = useParams<{ id: string }>();
  const analysisId = parseInt(id || "0", 10);
  
  const { data: analysis, isLoading, isError } = useGetAnalysis(analysisId, {
    query: {
      enabled: !!analysisId,
      queryKey: getGetAnalysisQueryKey(analysisId)
    }
  });

  const [animatedAts, setAnimatedAts] = useState(0);

  useEffect(() => {
    if (analysis?.atsScore) {
      const timer = setTimeout(() => setAnimatedAts(analysis.atsScore), 100);
      return () => clearTimeout(timer);
    }
  }, [analysis?.atsScore]);

  if (isLoading) {
    return (
      <AppLayout>
        <div className="space-y-8">
          <Skeleton className="h-12 w-1/3" />
          <div className="grid md:grid-cols-2 gap-8">
            <Skeleton className="h-[400px]" />
            <Skeleton className="h-[400px]" />
          </div>
        </div>
      </AppLayout>
    );
  }

  if (isError || !analysis) {
    return (
      <AppLayout>
        <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-destructive" />
          <h2 className="text-2xl font-bold tracking-tight">Analysis Not Found</h2>
          <p className="text-muted-foreground">The requested analysis could not be loaded.</p>
          <Link href="/dashboard">
            <Button variant="outline">Return to Dashboard</Button>
          </Link>
        </div>
      </AppLayout>
    );
  }

  // Prep data for radar chart (Matched vs Target)
  const radarData = [
    { subject: 'Technical', A: 85, B: 90, fullMark: 100 },
    { subject: 'Leadership', A: 60, B: 80, fullMark: 100 },
    { subject: 'Tools', A: 95, B: 85, fullMark: 100 },
    { subject: 'Domain', A: 70, B: 95, fullMark: 100 },
    { subject: 'Soft Skills', A: 80, B: 75, fullMark: 100 },
  ];

  return (
    <AppLayout>
      <div className="space-y-8 pb-12">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Badge variant="outline" className="font-mono text-xs uppercase bg-secondary/50">Status: {analysis.status}</Badge>
              <span className="text-sm text-muted-foreground font-mono">{new Date(analysis.createdAt).toLocaleDateString()}</span>
            </div>
            <h1 className="text-3xl font-bold font-mono tracking-tight text-foreground uppercase">
              {analysis.jobTitle || "Gap Analysis"}
            </h1>
          </div>
          <div className="flex gap-3">
            <Link href={`/sources/${analysis.id}`}>
              <Button variant="outline" className="font-mono text-xs uppercase">
                <ShieldCheck className="w-4 h-4 mr-2" /> View Sources
              </Button>
            </Link>
            <Link href={`/roadmap/${analysis.id}`}>
              <Button className="font-mono text-xs uppercase rounded-none">
                <Map className="w-4 h-4 mr-2" /> View Roadmap
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Scores */}
          <div className="lg:col-span-1 space-y-8">
            <Card className="bg-card/50 backdrop-blur-sm border-border/50 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <Target className="w-32 h-32" />
              </div>
              <CardHeader>
                <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">ATS Compatibility</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-6xl font-bold tracking-tighter mb-4 flex items-baseline">
                  <span className="tabular-nums" style={{ transition: "all 1s cubic-bezier(0.16, 1, 0.3, 1)" }}>
                    {animatedAts}
                  </span>
                  <span className="text-2xl text-muted-foreground ml-1">%</span>
                </div>
                <Progress value={animatedAts} className="h-2 bg-secondary" />
                <div className="mt-6 space-y-3">
                  <h4 className="text-xs font-mono uppercase text-muted-foreground">ATS Recommendations</h4>
                  <ul className="space-y-2 text-sm">
                    {analysis.atsRecommendations?.slice(0, 3).map((rec, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <ArrowRight className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                        <span className="text-foreground/90">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card/50 backdrop-blur-sm border-border/50">
              <CardHeader>
                <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Overall Match</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold tracking-tighter mb-2">{analysis.matchScore}%</div>
                <Progress value={analysis.matchScore} className="h-1 bg-secondary" />
              </CardContent>
            </Card>
          </div>

          {/* Radar Chart */}
          <Card className="lg:col-span-2 bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Skill Vector Alignment</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                    <PolarGrid stroke="hsl(var(--border))" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12, fontFamily: 'var(--font-mono)' }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '0px' }}
                      itemStyle={{ color: 'hsl(var(--foreground))', fontFamily: 'var(--font-mono)' }}
                    />
                    <Radar name="Your Skills" dataKey="A" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.3} />
                    <Radar name="Target Profile" dataKey="B" stroke="hsl(var(--muted-foreground))" fill="hsl(var(--muted-foreground))" fillOpacity={0.1} strokeDasharray="3 3" />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              <div className="flex justify-center gap-6 mt-4 font-mono text-xs">
                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-primary/50 border border-primary"></div> Your Profile</div>
                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-muted-foreground/20 border border-muted-foreground border-dashed"></div> Target Profile</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Missing Skills Grid */}
        <div className="grid lg:grid-cols-2 gap-8">
          <Card className="bg-card/50 backdrop-blur-sm border-border/50 border-t-2 border-t-destructive/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Critical Gaps</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analysis.missingSkills?.length ? analysis.missingSkills.map((skill, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-background/50 border border-border/50 rounded-sm">
                    <div>
                      <div className="font-medium text-foreground">{skill.name}</div>
                      <div className="text-xs text-muted-foreground font-mono mt-1">{skill.category}</div>
                    </div>
                    <Badge variant="outline" className={
                      skill.priority === 'high' ? 'border-destructive text-destructive' : 
                      skill.priority === 'medium' ? 'border-amber-500 text-amber-500' : ''
                    }>
                      {skill.priority} Priority
                    </Badge>
                  </div>
                )) : (
                  <p className="text-muted-foreground text-sm">No critical gaps identified.</p>
                )}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card/50 backdrop-blur-sm border-border/50 border-t-2 border-t-primary/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Strong Matches</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {analysis.strongSkills?.length ? analysis.strongSkills.map((skill, i) => (
                  <div key={i} className="px-3 py-1.5 bg-primary/10 border border-primary/20 text-primary rounded-sm text-sm font-medium">
                    {skill.name}
                  </div>
                )) : (
                  <p className="text-muted-foreground text-sm">Reviewing strong matches...</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
