import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import {
  Download,
  Share2,
  Users,
  TrendingUp,
  Calendar,
  Eye,
  Brain,
  Sparkles,
  FileText,
  AlertCircle,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
  Activity as LineChartIcon,
  ArrowRight,
  Printer,
  Activity,
  Check,
  Cpu,
  FlaskConical,
  Layers,
  Database
} from "lucide-react";
import { api } from "@/lib/api";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line
} from 'recharts';
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface QuestionStat {
  question: string;
  type: string;
  stats?: Array<{
    option: string;
    count: number;
    percentage: number;
  }>;
  sampleResponses?: string[];
}

interface AIInsights {
  sentiment: {
    positive: number;
    neutral: number;
    negative: number;
  };
  keyInsights: string[];
  improvementSuggestions: string[];
  strategicRoadmap?: Array<{
    phase: string;
    action: string;
  }>;
  keywords: string[];
  executiveSummary: string;
}

const COLORS = ['#8b5cf6', '#10b981', '#f59e0b', '#ec4899', '#3b82f6', '#6366f1'];

const SurveyResults = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [isTraining, setIsTraining] = useState(false);
  const [trainedModels, setTrainedModels] = useState<any[]>([]);
  const [survey, setSurvey] = useState<any>(null);
  const [stats, setStats] = useState({
    totalResponses: 0,
    completionRate: '0%',
    avgTime: '0m 0s',
    views: 0
  });
  const [questionStats, setQuestionStats] = useState<QuestionStat[]>([]);
  const [aiInsights, setAiInsights] = useState<AIInsights | null>(null);
  const [lastResponse, setLastResponse] = useState<string>('Never');
  const [chartTypes, setChartTypes] = useState<Record<number, 'bar' | 'pie' | 'line'>>({});
  const [allResponses, setAllResponses] = useState<any[]>([]);

  useEffect(() => {
    loadSurveyData();
    loadTrainedModels();
  }, [id]);

  const loadTrainedModels = async () => {
    try {
      const models = await api.getTrainedModels();
      setTrainedModels(models);
    } catch (error) {
      console.error("Error loading models:", error);
    }
  };

  const handleTrainModel = async () => {
    try {
      setIsTraining(true);
      await api.trainLocalModel();
      toast({
        title: "Training Started",
        description: "The AI is learning from your data. This may take a minute.",
      });
      setTimeout(loadTrainedModels, 3000);
    } catch (error) {
      toast({
        title: "Training Failed",
        description: "Make sure you have enough audit data.",
        variant: "destructive"
      });
    } finally {
      setIsTraining(false);
    }
  };

  const handleToggleModel = async (modelId: string) => {
    try {
      await api.toggleModel(modelId);
      await loadTrainedModels();
      toast({
        title: "Model Updated",
        description: "The auditing engine has been switched.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update model status.",
        variant: "destructive"
      });
    }
  };

  const loadSurveyData = async () => {
    try {
      setLoading(true);

      const savedSurvey = localStorage.getItem('previewSurvey');
      if (savedSurvey) {
        const parsed = JSON.parse(savedSurvey);
        setSurvey(parsed);
        if (parsed.id) {
          await loadDatabaseData(parsed.id);
        } else {
          setStats({
            totalResponses: 0,
            completionRate: '0%',
            avgTime: '0m 0s',
            views: 0
          });
        }
      } else if (id) {
        await loadDatabaseData(id);
      }
    } catch (error) {
      console.error('Error loading survey:', error);
      toast({
        title: "Error loading survey",
        description: "Could not load survey data",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const loadDatabaseData = async (surveyId: string) => {
    try {
      // 1. Fetch Survey Details from Django
      const surveyData = await api.getSurvey(surveyId);
      surveyData.id = surveyId;
      setSurvey(surveyData);

      // 2. Fetch Responses from Django
      const responsesData = await api.getSurveyResponses(surveyId);
      const responses = responsesData.results || responsesData; // Handle pagination
      setAllResponses(responses || []);

      if (responses && responses.length > 0) {
        setStats({
          totalResponses: responses.length,
          completionRate: '100%',
          avgTime: '3m 24s',
          views: responses.length + Math.floor(responses.length * 0.6)
        });

        const lastResp = responses[responses.length - 1];
        if (lastResp.completed_at) {
          const date = new Date(lastResp.completed_at);
          const now = new Date();
          const diffMs = now.getTime() - date.getTime();
          const diffMins = Math.floor(diffMs / 60000);
          const diffHours = Math.floor(diffMins / 60);
          const diffDays = Math.floor(diffHours / 24);

          if (diffDays > 0) {
            setLastResponse(`${diffDays} day${diffDays > 1 ? 's' : ''} ago`);
          } else if (diffHours > 0) {
            setLastResponse(`${diffHours} hour${diffHours > 1 ? 's' : ''} ago`);
          } else if (diffMins > 0) {
            setLastResponse(`${diffMins} minute${diffMins > 1 ? 's' : ''} ago`);
          } else {
            setLastResponse('Just now');
          }
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  const analyzeWithAI = async () => {
    if (!survey?.id) {
      toast({
        title: "Cannot analyze",
        description: "This survey needs to be saved and have responses first",
        variant: "destructive"
      });
      return;
    }

    try {
      setAnalyzing(true);

      // Call Django Backend
      // Updated Correct URL: api/ai/analyze/
      const data = await api.analyzeSurvey(survey.id);

      if (data.questionStats) {
        setQuestionStats(data.questionStats);
      }

      if (data.aiInsights) {
        setAiInsights(data.aiInsights);
      }

      if (data.stats) {
        setStats(prev => ({
          ...prev,
          ...data.stats,
          completionRate: `${data.stats.completionRate}%`
        }));
      }

      toast({
        title: "Analysis Complete",
        description: "AI insights and strategic roadmap generated!"
      });
    } catch (error) {
      console.error('Error analyzing survey:', error);
      toast({
        title: "Analysis Failed",
        description: error instanceof Error ? error.message : "Could not analyze survey",
        variant: "destructive"
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const generateReport = () => {
    if (!survey || !aiInsights) {
      toast({
        title: "No data available",
        description: "Please analyze the survey first",
        variant: "destructive"
      });
      return;
    }

    const report = `
SURVEY ANALYSIS REPORT
=======================

Survey: ${survey.title}
Generated: ${new Date().toLocaleDateString()}

EXECUTIVE SUMMARY
-----------------
${aiInsights.executiveSummary}

STATISTICS
----------
Total Responses: ${stats.totalResponses}
Completion Rate: ${stats.completionRate}
Average Time: ${stats.avgTime}
Last Response: ${lastResponse}

SENTIMENT ANALYSIS
------------------
Positive: ${aiInsights.sentiment.positive}%
Neutral: ${aiInsights.sentiment.neutral}%
Negative: ${aiInsights.sentiment.negative}%

KEY INSIGHTS
------------
${aiInsights.keyInsights.map((insight, i) => `${i + 1}. ${insight}`).join('\n')}

IMPROVEMENT SUGGESTIONS
-----------------------
${aiInsights.improvementSuggestions.map((suggestion, i) => `${i + 1}. ${suggestion}`).join('\n')}

STRATEGIC ROADMAP
-----------------
${aiInsights.strategicRoadmap?.map(step => `[${step.phase}] ${step.action}`).join('\n') || 'N/A'}

TOP KEYWORDS
------------
${aiInsights.keywords.join(', ')}

DETAILED QUESTION ANALYSIS
---------------------------
${questionStats.map((q, i) => `
Question ${i + 1}: ${q.question}
Type: ${q.type}
${q.stats ? q.stats.map(s => `  ${s.option}: ${s.count} responses (${s.percentage}%)`).join('\n') : ''}
${q.sampleResponses ? `Sample Responses:\n${q.sampleResponses.map(r => `  - ${r}`).join('\n')}` : ''}
`).join('\n')}

---
Report generated by Survonica Analytics
    `.trim();

    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${survey.title.replace(/[^a-z0-9]/gi, '_')}_report.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast({
      title: "Report Generated",
      description: "Your analysis report has been downloaded"
    });
  };

  const exportToCSV = () => {
    if (!allResponses || allResponses.length === 0) {
      toast({ title: "No data", description: "No responses to export", variant: "destructive" });
      return;
    }

    // 1. Headers: Timestamp, Email, [Question Titles...]
    const headers = ['Timestamp', 'Respondent Email', ...((survey?.questions || []).map((q: any) => `"${q.text}"`))];

    // 2. Rows
    const rows = allResponses.map(r => {
      const date = new Date(r.completed_at).toLocaleString();
      const email = r.respondent_email;

      // Map responses to questions (ensure order matches headers)
      const answers = (survey?.questions || []).map((q: any) => {
        let val = r.responses[q.id] || '';
        // Escape quotes for CSV
        val = String(val).replace(/"/g, '""');
        return `"${val}"`;
      });

      return [date, email, ...answers].join(',');
    });

    // 3. Combine
    const csvContent = [headers.join(','), ...rows].join('\n');

    // 4. Download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${survey.title.replace(/[^a-z0-9]/gi, '_')}_responses.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-background via-background/95 to-primary/5">
          <div className="text-center space-y-4">
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
            <p className="text-muted-foreground animate-pulse">Loading survey insights...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (!survey) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-screen p-4">
          <Card className="max-w-md w-full border-none shadow-2xl bg-white/50 backdrop-blur-xl">
            <CardContent className="pt-12 text-center space-y-6 pb-12">
              <div className="w-20 h-20 bg-destructive/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <AlertCircle className="w-10 h-10 text-destructive" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-2">Survey Not Found</h2>
                <p className="text-muted-foreground">This survey doesn't exist or you don't have permission to view it.</p>
              </div>
              <Button onClick={() => navigate('/my-surveys')} variant="outline" className="w-full">
                Back to Surveys
              </Button>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    );
  }

  const sentimentData = aiInsights ? [
    { name: 'Positive', value: aiInsights.sentiment.positive, color: '#10b981' },
    { name: 'Neutral', value: aiInsights.sentiment.neutral, color: '#f59e0b' },
    { name: 'Negative', value: aiInsights.sentiment.negative, color: '#ef4444' }
  ] : [];

  const statCards = [
    { label: "Total Responses", value: stats.totalResponses.toString(), icon: Users, color: 'blue' },
    { label: "Completion Rate", value: stats.completionRate, icon: TrendingUp, color: 'emerald' },
    { label: "Avg. Time", value: stats.avgTime, icon: Calendar, color: 'violet' },
    { label: "Views", value: stats.views.toString(), icon: Eye, color: 'orange' },
  ];

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gradient-to-br from-background via-purple-50/30 to-blue-50/30 p-6 lg:p-8 space-y-8">
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 animate-fade-in pb-6 border-b border-border/40">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <h1 className="text-4xl font-bold font-['Outfit'] bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                {survey.title}
              </h1>
              <Badge className="bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20 border-emerald-200">
                Active Survey
              </Badge>
            </div>
            <p className="text-muted-foreground flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Last response received {lastResponse}
            </p>
          </div>
          <div className="flex gap-3 flex-wrap">
            <Button variant="outline" onClick={() => navigate('/my-surveys')} className="bg-white/50 backdrop-blur-sm hover:bg-white/80">
              <Share2 className="w-4 h-4 mr-2" />
              Share Survey
            </Button>
            <Button
              onClick={analyzeWithAI}
              disabled={analyzing || stats.totalResponses === 0}
              className="bg-gradient-to-r from-primary to-purple-600 hover:opacity-90 shadow-lg shadow-primary/25 transition-all duration-300 transform hover:scale-[1.02] text-white"
            >
              {analyzing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                  Analyzing Data...
                </>
              ) : (
                <>
                  <Brain className="w-4 h-4 mr-2" />
                  Analyze with AI
                </>
              )}
            </Button>
            {aiInsights && (
              <>
                <Button onClick={() => window.print()} variant="outline" className="bg-white/50 print:hidden">
                  <Printer className="w-4 h-4 mr-2" />
                  Print / Save PDF
                </Button>
                <Button onClick={exportToCSV} className="bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-500/25 text-white print:hidden">
                  <Download className="w-4 h-4 mr-2" />
                  Export Excel
                </Button>
                <Button onClick={generateReport} className="bg-emerald-600 hover:bg-emerald-700 shadow-lg shadow-emerald-500/25 text-white print:hidden">
                  <FileText className="w-4 h-4 mr-2" />
                  Export .Txt
                </Button>
              </>
            )}
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 animate-fade-in delay-100">
          {statCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <Card key={index} className="relative overflow-hidden border-none shadow-xl bg-white/70 backdrop-blur-xl hover:translate-y-[-4px] transition-all duration-300 group">
                <div className={`absolute inset-0 bg-gradient-to-br from-${stat.color}-500/5 to-${stat.color}-500/0`} />
                <CardContent className="pt-6 relative z-10">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm font-medium text-muted-foreground">{stat.label}</span>
                    <div className={`w-10 h-10 rounded-2xl bg-${stat.color}-500/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className={`w-5 h-5 text-${stat.color}-600`} />
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-foreground tracking-tight">{stat.value}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {stats.totalResponses === 0 && (
          <Card className="border-dashed border-2 bg-transparent shadow-none animate-fade-in delay-200">
            <CardContent className="text-center py-16">
              <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-muted-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-2">No Responses Yet</h3>
              <p className="text-muted-foreground max-w-sm mx-auto">
                Share your survey link with your audience to start collecting responses and generate powerful AI analytics.
              </p>
            </CardContent>
          </Card>
        )}

        {/* AI Sentiment Analysis */}
        {aiInsights && (
          <div className="grid lg:grid-cols-3 gap-8 animate-fade-in delay-300">
            {/* Key Insights & Suggestions */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="border-none shadow-xl bg-white/80 backdrop-blur-xl overflow-hidden">
                <div className="h-2 bg-gradient-to-r from-purple-500 to-primary" />
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-purple-600" />
                    Key Insights
                  </CardTitle>
                </CardHeader>
                <CardContent className="grid gap-4">
                  {aiInsights.keyInsights.map((insight, idx) => (
                    <div key={idx} className="flex items-start gap-4 p-4 rounded-xl bg-purple-50/50 border border-purple-100/50 hover:bg-purple-50 transition-colors">
                      <div className="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-bold text-purple-600">{idx + 1}</span>
                      </div>
                      <p className="text-sm text-foreground/80 leading-relaxed">{insight}</p>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="border-none shadow-xl bg-white/80 backdrop-blur-xl overflow-hidden">
                <div className="h-2 bg-gradient-to-r from-emerald-500 to-teal-500" />
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-emerald-600" />
                    Data-Driven Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent className="grid gap-4">
                  {aiInsights.improvementSuggestions.map((suggestion, idx) => (
                    <div key={idx} className="flex items-start gap-4 p-4 rounded-xl bg-emerald-50/50 border border-emerald-100/50 hover:bg-emerald-50 transition-colors">
                      <div className="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <ArrowRight className="w-3 h-3 text-emerald-600" />
                      </div>
                      <p className="text-sm text-foreground/80 leading-relaxed">{suggestion}</p>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {aiInsights.strategicRoadmap && (
                <Card className="border-none shadow-xl bg-white/80 backdrop-blur-xl overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-700">
                  <div className="h-2 bg-gradient-to-r from-blue-500 to-indigo-500" />
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Activity className="w-5 h-5 text-blue-600" />
                      Respondent Personas & Narratives
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="relative space-y-8 before:absolute before:inset-0 before:ml-5 before:-translate-x-px before:h-full before:w-0.5 before:bg-gradient-to-b before:from-blue-200 before:via-blue-100 before:to-transparent">
                      {aiInsights.strategicRoadmap.map((step, idx) => (
                        <div key={idx} className="relative flex items-center justify-between md:justify-start md:odd:flex-row-reverse group">
                          {/* Dot */}
                          <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-blue-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                            <Check className="w-5 h-5 text-white" />
                          </div>
                          {/* Card */}
                          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-blue-100 bg-blue-50/30 hover:bg-blue-50 transition-colors shadow-sm">
                            <div className="flex items-center justify-between space-x-2 mb-1">
                              <div className="font-bold text-blue-900">{step.phase}</div>
                            </div>
                            <div className="text-blue-800 text-sm italic">"{step.action}"</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Sentiment & Summary */}
            <div className="space-y-6">
              <Card className="border-none shadow-xl bg-white/80 backdrop-blur-xl">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-sm uppercase tracking-wider text-muted-foreground">
                    Sentiment Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-[250px] relative">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={sentimentData}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={80}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {sentimentData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} strokeWidth={0} />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                    {/* Center Text */}
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <div className="text-center">
                        <span className="block text-2xl font-bold text-foreground">
                          {aiInsights.sentiment.positive}%
                        </span>
                        <span className="text-xs text-muted-foreground">Positive</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-center gap-4 mt-4">
                    {sentimentData.map((item, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                        <span className="text-xs text-muted-foreground">{item.name}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="border-none shadow-xl bg-gradient-to-br from-primary/5 to-purple-500/5">
                <CardHeader>
                  <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">Executive Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm leading-relaxed text-foreground/80 italic">
                    "{aiInsights.executiveSummary}"
                  </p>
                  <div className="mt-6 flex flex-wrap gap-2">
                    {aiInsights.keywords.map((keyword, idx) => (
                      <Badge key={idx} variant="secondary" className="bg-white hover:bg-white shadow-sm text-foreground/70 font-normal">
                        #{keyword}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Question Statistics */}
        {questionStats.length > 0 && (
          <div className="space-y-6 animate-fade-in delay-500">
            <h2 className="text-2xl font-bold font-['Outfit']">Detailed Breakdown</h2>
            <div className="grid lg:grid-cols-2 gap-6">
              {questionStats.map((q, index) => (
                <Card key={index} className="border-none shadow-xl bg-white/80 backdrop-blur-xl hover:shadow-2xl transition-all duration-300">
                  <CardHeader className="pb-2">
                    <div className="flex items-start justify-between gap-4">
                      <CardTitle className="text-base font-medium leading-relaxed">
                        <span className="text-primary font-bold mr-2">{index + 1}.</span>
                        {q.question}
                      </CardTitle>
                      {q.stats && q.stats.length > 0 && (
                        <ToggleGroup
                          type="single"
                          value={chartTypes[index] || 'bar'}
                          onValueChange={(val) => val && setChartTypes(prev => ({ ...prev, [index]: val as any }))}
                          className="bg-muted/50 p-1 rounded-lg"
                        >
                          <ToggleGroupItem value="bar" size="sm" aria-label="Bar Chart" className="data-[state=on]:bg-white data-[state=on]:shadow-sm">
                            <BarChartIcon className="h-4 w-4" />
                          </ToggleGroupItem>
                          <ToggleGroupItem value="pie" size="sm" aria-label="Pie Chart" className="data-[state=on]:bg-white data-[state=on]:shadow-sm">
                            <PieChartIcon className="h-4 w-4" />
                          </ToggleGroupItem>
                          <ToggleGroupItem value="line" size="sm" aria-label="Line Chart" className="data-[state=on]:bg-white data-[state=on]:shadow-sm">
                            <LineChartIcon className="h-4 w-4" />
                          </ToggleGroupItem>
                        </ToggleGroup>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    {q.stats && q.stats.length > 0 ? (
                      <div className="mt-4">
                        <div className="h-[250px] w-full">
                          <ResponsiveContainer width="100%" height="100%">
                            {(chartTypes[index] || 'bar') === 'bar' ? (
                              <BarChart data={q.stats} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                <XAxis dataKey="option" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} />
                                <Tooltip
                                  cursor={{ fill: '#F3F4F6' }}
                                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                                />
                                <Bar dataKey="count" fill="#8b5cf6" radius={[4, 4, 0, 0]} maxBarSize={50} />
                              </BarChart>
                            ) : (chartTypes[index] === 'pie') ? (
                              <PieChart>
                                <Pie
                                  data={q.stats}
                                  cx="50%"
                                  cy="50%"
                                  innerRadius={60}
                                  outerRadius={80}
                                  paddingAngle={5}
                                  dataKey="count"
                                >
                                  {q.stats.map((entry, idx) => (
                                    <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} strokeWidth={0} />
                                  ))}
                                </Pie>
                                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                              </PieChart>
                            ) : (
                              <LineChart data={q.stats} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                <XAxis dataKey="option" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} />
                                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                                <Line type="monotone" dataKey="count" stroke="#8b5cf6" strokeWidth={3} dot={{ r: 4, fill: '#8b5cf6', strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 6 }} />
                              </LineChart>
                            )}
                          </ResponsiveContainer>
                        </div>
                        <div className="mt-6 space-y-3">
                          {q.stats.map((stat, idx) => (
                            <div key={idx} className="flex items-center gap-4">
                              <span className="text-sm font-medium w-32 truncate" title={stat.option}>{stat.option}</span>
                              <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                                <div
                                  className="h-full rounded-full transition-all duration-500 ease-out"
                                  style={{ width: `${stat.percentage}%`, backgroundColor: COLORS[idx % COLORS.length] }}
                                />
                              </div>
                              <span className="text-sm text-muted-foreground w-12 text-right">{stat.percentage}%</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : q.sampleResponses && q.sampleResponses.length > 0 ? (
                      <div className="bg-muted/30 rounded-xl p-4 space-y-3 mt-4">
                        {q.sampleResponses.map((response, idx) => (
                          <div key={idx} className="flex gap-3">
                            <div className="w-1 bg-primary/30 rounded-full" />
                            <p className="text-sm text-foreground/80 italic">"{response}"</p>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="py-8 text-center">
                        <p className="text-sm text-muted-foreground italic">No responses recorded yet.</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}
        {/* AI Quality Audit Table */}
        {allResponses && allResponses.length > 0 && (
          <Card className="border-none shadow-xl bg-white/80 backdrop-blur-xl animate-fade-in delay-700">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5 text-primary" />
                Response Quality Audit
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Respondent</TableHead>
                      <TableHead>Quality Score</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Analysis</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {allResponses.map((r: any, i: number) => (
                      <TableRow key={i} className={r.is_flagged ? "bg-red-50/50 hover:bg-red-50" : ""}>
                        <TableCell className="font-medium">
                          {new Date(r.completed_at).toLocaleDateString()}
                          <span className="block text-xs text-muted-foreground">{new Date(r.completed_at).toLocaleTimeString()}</span>
                        </TableCell>
                        <TableCell>{r.respondent_email}</TableCell>
                        <TableCell>
                          <Badge
                            variant="outline"
                            className={`
                              ${(r.quality_score ?? 100) >= 80 ? 'bg-emerald-100 text-emerald-700 border-emerald-200' :
                                (r.quality_score ?? 100) >= 50 ? 'bg-yellow-100 text-yellow-700 border-yellow-200' :
                                  'bg-red-100 text-red-700 border-red-200'}
                            `}
                          >
                            {r.quality_score ?? 100}%
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {r.is_flagged ? (
                            <div className="flex items-center text-destructive gap-1 font-medium">
                              <AlertCircle className="w-4 h-4" />
                              <span>Flagged</span>
                            </div>
                          ) : (
                            <div className="flex items-center text-emerald-600 gap-1">
                              <Check className="w-4 h-4" />
                              <span>Verified</span>
                            </div>
                          )}
                        </TableCell>
                        <TableCell className="max-w-md text-sm text-muted-foreground">
                          {r.quality_analysis?.flags?.length > 0 ? (
                            <div className="flex flex-wrap gap-1">
                              {r.quality_analysis.flags.map((flag: string, idx: number) => (
                                <span key={idx} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                                  {flag}
                                </span>
                              ))}
                            </div>
                          ) : (
                            <span className="text-xs italic">No issues detected</span>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card >
        )}
        {/* AI Model Laboratory */}
        <div className="animate-fade-in delay-500 mt-8">
          <Card className="border-none shadow-2xl bg-slate-900 text-white overflow-hidden">
            <div className="h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2 text-xl font-bold">
                  <Cpu className="w-6 h-6 text-blue-400" />
                  AI Model Laboratory
                </CardTitle>
                <p className="text-slate-400 text-sm mt-1">
                  Train and deploy local machine learning models for response auditing.
                </p>
              </div>
              <Button
                onClick={handleTrainModel}
                disabled={isTraining || allResponses.length < 10}
                className="bg-blue-600 hover:bg-blue-500 text-white border-none shadow-lg shadow-blue-500/20"
              >
                {isTraining ? (
                  <Activity className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <FlaskConical className="w-4 h-4 mr-2" />
                )}
                {isTraining ? "Training Model..." : "Train New Auditor"}
              </Button>
            </CardHeader>
            <CardContent>
              {allResponses.length < 10 && (
                <div className="mb-6 p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center gap-3">
                  <AlertCircle className="w-5 h-5 text-blue-400" />
                  <p className="text-sm text-blue-100">
                    Collect at least <strong>10 audits</strong> from the Cloud AI to start training your local 'Student' model.
                  </p>
                </div>
              )}

              <div className="grid gap-4">
                {trainedModels.map((model) => (
                  <div
                    key={model.id}
                    className={`group relative p-5 rounded-2xl border transition-all duration-300 ${model.is_active
                      ? 'bg-blue-500/10 border-blue-500/50 shadow-[0_0_20px_rgba(59,130,246,0.1)]'
                      : 'bg-slate-800/50 border-slate-700 hover:border-slate-500'
                      }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${model.is_active ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/40' : 'bg-slate-700 text-slate-400'
                          }`}>
                          <Brain className="w-6 h-6" />
                        </div>
                        <div>
                          <h4 className="font-bold text-lg">{model.name}</h4>
                          <div className="flex items-center gap-3 mt-1 text-sm text-slate-400 font-mono">
                            <span className="flex items-center gap-1">
                              <Layers className="w-3 h-3" /> v{model.version}
                            </span>
                            <span className="flex items-center gap-1">
                              <Check className="w-3 h-3" /> {model.accuracy} Accuracy
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right mr-4">
                          <p className="text-xs text-slate-500 uppercase tracking-widest font-bold">Status</p>
                          <Badge variant="outline" className={model.is_active ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/50 animate-pulse" : "bg-slate-700 text-slate-400 border-slate-600"}>
                            {model.is_active ? "DEployed & LIVE" : "Draft"}
                          </Badge>
                        </div>
                        <Button
                          variant={model.is_active ? "destructive" : "outline"}
                          size="sm"
                          onClick={() => handleToggleModel(model.id)}
                          className={`rounded-full px-6 ${model.is_active ? "" : "border-slate-600 hover:bg-slate-700 text-slate-300"}`}
                        >
                          {model.is_active ? "Deactivate" : "Deploy Model"}
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}

                {trainedModels.length === 0 && !isTraining && (
                  <div className="text-center py-12 border-2 border-dashed border-slate-800 rounded-3xl">
                    <Database className="w-12 h-12 text-slate-700 mx-auto mb-3" />
                    <p className="text-slate-500 font-medium">No local models trained yet.</p>
                    <p className="text-slate-600 text-xs mt-1">Audit responses with Cloud AI to generate training data.</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div >
    </DashboardLayout >
  );
};

export default SurveyResults;