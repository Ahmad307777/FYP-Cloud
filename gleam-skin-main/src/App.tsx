import { Suspense, lazy } from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Loader2 } from "lucide-react";

// Lazy loading components to isolate crashes
const Landing = lazy(() => import("./pages/Landing"));
const Login = lazy(() => import("./pages/Login"));
const Signup = lazy(() => import("./pages/Signup"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const CreateSurvey = lazy(() => import("./pages/CreateSurvey"));
const MySurveys = lazy(() => import("./pages/MySurveys"));
const SurveyEditor = lazy(() => import("./pages/SurveyEditor"));
const SurveyResponse = lazy(() => import("./pages/SurveyResponse"));
const SurveyResults = lazy(() => import("./pages/SurveyResults"));
const NotFound = lazy(() => import("./pages/NotFound"));
const QualificationTest = lazy(() => import("./pages/QualificationTest"));
const QualityControl = lazy(() => import("./pages/QualityControl"));
const CreateQualificationTest = lazy(() => import("./pages/CreateQualificationTest"));
const AiSurveyAssistant = lazy(() => import("./pages/AiSurveyAssistant"));

const queryClient = new QueryClient();

const LoadingFallback = () => (
  <div className="min-h-screen w-full flex flex-col items-center justify-center bg-gray-50/50">
    <Loader2 className="w-10 h-10 text-primary animate-spin mb-4" />
    <p className="text-gray-500 font-medium animate-pulse">Loading Survonica...</p>
  </div>
);

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Suspense fallback={<LoadingFallback />}>
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/create" element={<CreateSurvey />} />
              <Route path="/ai-assistant" element={<AiSurveyAssistant />} />
              <Route path="/surveys" element={<MySurveys />} />
              <Route path="/editor/:id" element={<SurveyEditor />} />
              <Route path="/survey-editor" element={<SurveyEditor />} />
              <Route path="/quality-control" element={<QualityControl />} />
              <Route path="/create-qualification-test" element={<CreateQualificationTest />} />
              <Route path="/qualification/:surveyId" element={<QualificationTest />} />
              <Route path="/survey/:id" element={<SurveyResponse />} />
              <Route path="/results/:id" element={<SurveyResults />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
