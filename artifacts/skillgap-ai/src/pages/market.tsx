import { AppLayout } from "@/components/layout/AppLayout";
import { useGetMarketTrends } from "@workspace/api-client-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Minus, Activity } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function Market() {
  const { data: trends, isLoading } = useGetMarketTrends();

  // Mock historical data for the chart since API only provides current snapshot
  const generateTrendData = () => {
    return Array.from({ length: 6 }).map((_, i) => ({
      month: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'][i],
      ai: 40 + Math.random() * 60 + (i * 10),
      cloud: 60 + Math.random() * 20 + (i * 5),
      frontend: 70 + Math.random() * 10 - (i * 2),
    }));
  };

  const chartData = generateTrendData();

  if (isLoading) {
    return (
      <AppLayout>
        <div className="space-y-8">
          <Skeleton className="h-12 w-1/4" />
          <Skeleton className="h-[400px] w-full" />
          <div className="grid md:grid-cols-2 gap-8">
            <Skeleton className="h-[300px]" />
            <Skeleton className="h-[300px]" />
          </div>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="space-y-8 pb-12">
        <div>
          <h1 className="text-3xl font-bold font-mono tracking-tight uppercase flex items-center gap-3">
            <Activity className="w-8 h-8 text-primary" /> Market Pulse
          </h1>
          <p className="text-muted-foreground mt-2">Real-time skill demand and emerging technology trends.</p>
        </div>

        {/* Global Trend Chart */}
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader>
            <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground">Category Demand Velocity</CardTitle>
            <CardDescription>Relative growth of top tech categories over 6 months</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[350px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorAi" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorCloud" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--chart-2))" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="hsl(var(--chart-2))" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" tickLine={false} axisLine={false} />
                  <YAxis stroke="hsl(var(--muted-foreground))" tickLine={false} axisLine={false} />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '4px' }}
                    itemStyle={{ fontFamily: 'var(--font-mono)' }}
                  />
                  <Area type="monotone" dataKey="ai" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorAi)" name="AI/ML" />
                  <Area type="monotone" dataKey="cloud" stroke="hsl(var(--chart-2))" fillOpacity={1} fill="url(#colorCloud)" name="Cloud Infrastructure" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Trending Skills */}
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground flex items-center justify-between">
                <span>Top Trending Skills</span>
                <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">High Signal</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-1">
                {trends?.trendingSkills?.map((skill, i) => (
                  <div key={i} className="group flex items-center justify-between p-3 hover:bg-secondary/50 rounded-sm transition-colors border-b border-border/30 last:border-0">
                    <div className="flex items-center gap-3">
                      <div className="w-6 text-center font-mono text-xs text-muted-foreground">{i + 1}</div>
                      <div>
                        <div className="font-medium text-foreground">{skill.name}</div>
                        <div className="text-xs text-muted-foreground font-mono mt-0.5">{skill.category}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right hidden sm:block">
                        <div className="text-sm font-medium">{skill.demandScore}/100</div>
                        <div className="text-[10px] text-muted-foreground uppercase font-mono">Demand</div>
                      </div>
                      <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                        skill.trendDirection === 'rising' ? 'bg-emerald-500/10 text-emerald-500' :
                        skill.trendDirection === 'declining' ? 'bg-destructive/10 text-destructive' :
                        'bg-muted text-muted-foreground'
                      }`}>
                        {skill.trendDirection === 'rising' ? <TrendingUp className="w-4 h-4" /> :
                         skill.trendDirection === 'declining' ? <TrendingDown className="w-4 h-4" /> :
                         <Minus className="w-4 h-4" />}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Emerging Tech */}
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="font-mono text-sm uppercase tracking-wider text-muted-foreground flex items-center justify-between">
                <span>Emerging Technologies</span>
                <Badge variant="outline" className="bg-chart-4/10 text-chart-4 border-chart-4/20">Early Adopters</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-1">
                {trends?.emergingSkills?.map((skill, i) => (
                  <div key={i} className="flex items-center justify-between p-3 hover:bg-secondary/50 rounded-sm transition-colors border-b border-border/30 last:border-0">
                    <div>
                      <div className="font-medium text-foreground">{skill.name}</div>
                      <div className="text-xs text-muted-foreground font-mono mt-0.5">{skill.category}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-chart-4">+{skill.growthRate}%</div>
                      <div className="text-[10px] text-muted-foreground uppercase font-mono">Growth MoM</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
