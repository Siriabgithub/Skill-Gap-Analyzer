import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "wouter";
import { useGetDashboardStats } from "@workspace/api-client-react";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowUpRight, BarChart3, Activity, Briefcase } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { format } from "date-fns";
import { motion } from "framer-motion";

export default function Dashboard() {
  const { data: stats, isLoading } = useGetDashboardStats();

  return (
    <AppLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold font-mono uppercase tracking-tight text-foreground">Command Center</h1>
          <p className="text-muted-foreground mt-2">Overview of your career readiness and market alignment.</p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <Skeleton key={i} className="h-32 rounded-xl" />
            ))}
          </div>
        ) : stats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatsCard 
              title="Avg ATS Score" 
              value={`${Math.round(stats.avgAtsScore)}%`} 
              icon={Activity} 
              trend="+2%" 
            />
            <StatsCard 
              title="Avg Match Score" 
              value={`${Math.round(stats.avgMatchScore)}%`} 
              icon={Target} 
              trend="+5%" 
            />
            <StatsCard 
              title="Total Analyses" 
              value={stats.totalAnalyses.toString()} 
              icon={BarChart3} 
            />
            <StatsCard 
              title="Resumes Uploaded" 
              value={stats.totalResumes.toString()} 
              icon={Briefcase} 
            />
          </div>
        ) : null}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <Card className="col-span-1 lg:col-span-2 bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Top Missing Skills</CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <Skeleton className="h-[300px] w-full" />
              ) : stats?.topMissingSkills?.length ? (
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={stats.topMissingSkills} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="hsl(var(--border))" />
                      <XAxis type="number" hide />
                      <YAxis dataKey="skill" type="category" axisLine={false} tickLine={false} tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }} width={100} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                        itemStyle={{ color: 'hsl(var(--foreground))' }}
                      />
                      <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                        {stats.topMissingSkills.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={`hsl(var(--chart-${(index % 5) + 1}))`} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-[300px] flex items-center justify-center text-muted-foreground">No skill data available.</div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Recent Analyses</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {isLoading ? (
                  [...Array(3)].map((_, i) => <Skeleton key={i} className="h-16 w-full" />)
                ) : stats?.recentAnalyses?.length ? (
                  stats.recentAnalyses.slice(0, 4).map((analysis, i) => (
                    <motion.div 
                      key={analysis.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex flex-col gap-2 p-3 rounded-lg border border-border/50 bg-background/50 hover:border-primary/50 transition-colors"
                    >
                      <div className="flex justify-between items-start">
                        <span className="font-medium truncate pr-2" title={analysis.jobTitle || "Analysis"}>
                          {analysis.jobTitle || `Analysis #${analysis.id}`}
                        </span>
                        <span className="text-xs text-muted-foreground whitespace-nowrap">
                          {format(new Date(analysis.createdAt), "MMM d")}
                        </span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <div className="flex items-center gap-2">
                          <span className="text-muted-foreground">ATS:</span>
                          <span className="font-mono text-primary">{analysis.atsScore || 0}%</span>
                        </div>
                        <Link href={`/analyses/${analysis.id}`}>
                          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">View</Button>
                        </Link>
                      </div>
                    </motion.div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    No recent analyses found.
                  </div>
                )}
                <div className="pt-2">
                  <Link href="/upload">
                    <Button className="w-full" variant="outline">New Analysis</Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}

function StatsCard({ title, value, icon: Icon, trend }: { title: string, value: string, icon: any, trend?: string }) {
  return (
    <Card className="bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden relative group">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      <CardContent className="p-6">
        <div className="flex justify-between items-start">
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground uppercase font-mono tracking-wider">{title}</p>
            <p className="text-4xl font-bold tracking-tighter">{value}</p>
          </div>
          <div className="p-3 bg-primary/10 rounded-lg text-primary">
            <Icon className="w-5 h-5" />
          </div>
        </div>
        {trend && (
          <div className="mt-4 flex items-center text-sm">
            <ArrowUpRight className="w-4 h-4 text-emerald-500 mr-1" />
            <span className="text-emerald-500 font-medium">{trend}</span>
            <span className="text-muted-foreground ml-2">vs last month</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function Target(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="6" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  )
}
