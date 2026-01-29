import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Shield, Plus, Trash2, Check, Sparkles, Loader2, Clock } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { api } from "../lib/api";
import { Slider } from "@/components/ui/slider";

interface QualificationQuestion {
    question: string;
    options: string[];
    correctAnswer: number;
}

export default function QualificationTestPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const { toast } = useToast();

    const surveyData = location.state?.surveyData;
    const [topic, setTopic] = useState(surveyData?.title || "Pre-Qualification Test");
    const [questions, setQuestions] = useState<QualificationQuestion[]>([
        { question: "", options: ["", "", "", ""], correctAnswer: 0 }
    ]);
    const [saving, setSaving] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);
    const [numQuestionsToGenerate, setNumQuestionsToGenerate] = useState(3);
    const [timeLimit, setTimeLimit] = useState(0); // 0 = No limit

    const addQuestion = () => {
        setQuestions([...questions, { question: "", options: ["", "", "", ""], correctAnswer: 0 }]);
    };

    const removeQuestion = (index: number) => {
        setQuestions(questions.filter((_, i) => i !== index));
    };

    const updateQuestion = (index: number, field: keyof QualificationQuestion, value: any) => {
        const updated = [...questions];
        updated[index] = { ...updated[index], [field]: value };
        setQuestions(updated);
    };

    const updateOption = (qIndex: number, oIndex: number, value: string) => {
        const updated = [...questions];
        updated[qIndex].options[oIndex] = value;
        setQuestions(updated);
    };

    const handleGenerateAI = async () => {
        if (!topic.trim()) {
            toast({ title: "Topic Required", description: "Please enter a topic first", variant: "destructive" });
            return;
        }

        setIsGenerating(true);
        try {
            const data = await api.generateQualification(topic, numQuestionsToGenerate);
            if (Array.isArray(data) && data.length > 0) {
                // If it's the default single blank question, replace it
                if (questions.length === 1 && !questions[0].question) {
                    setQuestions(data);
                } else {
                    setQuestions([...questions, ...data]);
                }
                toast({ title: "Generated!", description: `Added ${data.length} qualification questions.` });
            } else {
                toast({ title: "No Result", description: "AI couldn't generate valid questions.", variant: "destructive" });
            }
        } catch (error) {
            toast({ title: "Error", description: "AI Generation failed", variant: "destructive" });
        } finally {
            setIsGenerating(false);
        }
    };

    const handleSave = async () => {
        // Validate
        const invalidQuestions = questions.filter(q =>
            !q.question.trim() || q.options.some(o => !o.trim())
        );

        if (invalidQuestions.length > 0) {
            toast({
                title: "Validation Error",
                description: "Please fill in all questions and options",
                variant: "destructive"
            });
            return;
        }

        setSaving(true);
        try {
            // First create or update the survey
            const sData = {
                ...surveyData,
                require_qualification: true,
                qualification_pass_score: 80
            };

            const survey = surveyData?.id
                ? await api.updateSurvey(surveyData.id, sData)
                : await api.saveSurvey(sData);

            // Then create qualification test using api helper
            await api.createQualificationTest({
                survey_id: survey.id,
                topic,
                questions,
                time_limit: timeLimit
            });

            toast({
                title: "Success!",
                description: "Survey and qualification test created successfully"
            });

            // Redirect back to editor with data and preview mode enabled
            navigate("/survey-editor", {
                state: {
                    surveyData: {
                        ...surveyData,
                        id: survey.id,
                        require_qualification: true,
                    },
                    template: surveyData.template, // Ensure template is passed back
                    showPreview: true
                }
            });
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.message || "Failed to create qualification test",
                variant: "destructive"
            });
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-subtle py-16 px-4">
            <div className="max-w-4xl mx-auto">
                <Card className="shadow-elegant">
                    <div className="h-2 bg-gradient-success" />
                    <CardHeader className="bg-gradient-card">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-14 h-14 rounded-2xl bg-gradient-success flex items-center justify-center">
                                <Shield className="w-7 h-7 text-success-foreground" />
                            </div>
                            <div>
                                <CardTitle className="text-2xl">Create Qualification Test</CardTitle>
                                <CardDescription>
                                    Set up pre-qualification questions to filter respondents
                                </CardDescription>
                            </div>
                        </div>
                    </CardHeader>

                    <CardContent className="p-8 space-y-8">
                        {/* Topic & Timer Settings */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <Label htmlFor="topic">Test Topic / Context</Label>
                                <Input
                                    id="topic"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    placeholder="e.g., Product Knowledge Test"
                                    className="mt-2"
                                />
                            </div>

                            <div>
                                <Label className="flex items-center gap-2">
                                    <Clock className="w-4 h-4 text-orange-500" />
                                    Time Limit (Minutes)
                                </Label>
                                <div className="flex items-center gap-4 mt-2">
                                    <Input
                                        type="number"
                                        min="0"
                                        value={timeLimit}
                                        onChange={(e) => setTimeLimit(parseInt(e.target.value) || 0)}
                                        className="w-24"
                                    />
                                    <span className="text-sm text-muted-foreground">
                                        {timeLimit === 0 ? "No Time Limit" : `${timeLimit} minutes`}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* AI Generator Panel */}
                        <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-6 space-y-4">
                            <div className="flex items-center gap-2 text-indigo-800 font-medium">
                                <Sparkles className="w-5 h-5" />
                                <h3>AI Question Generator</h3>
                            </div>

                            <div className="flex items-end gap-6">
                                <div className="flex-1 space-y-2">
                                    <Label className="text-xs text-indigo-600">Number of Questions to Generate: {numQuestionsToGenerate}</Label>
                                    <Slider
                                        value={[numQuestionsToGenerate]}
                                        min={1}
                                        max={5}
                                        step={1}
                                        onValueChange={(vals) => setNumQuestionsToGenerate(vals[0])}
                                        className="py-2"
                                    />
                                </div>
                                <Button
                                    onClick={handleGenerateAI}
                                    disabled={isGenerating}
                                    className="bg-indigo-600 hover:bg-indigo-700 text-white min-w-[140px]"
                                >
                                    {isGenerating ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Sparkles className="w-4 h-4 mr-2" />}
                                    {isGenerating ? "Creating..." : "Generate Test"}
                                </Button>
                            </div>
                        </div>

                        <div className="space-y-6">
                            {questions.map((q, qIndex) => (
                                <Card key={qIndex} className="border-2 group hover:border-indigo-200 transition-colors">
                                    <CardContent className="p-6">
                                        <div className="flex items-start justify-between mb-4">
                                            <h3 className="font-semibold text-lg text-gray-700">Question {qIndex + 1}</h3>
                                            <Button
                                                size="sm"
                                                variant="ghost"
                                                onClick={() => removeQuestion(qIndex)}
                                                className="text-gray-400 hover:text-red-600"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>

                                        <div className="space-y-4">
                                            <div>
                                                <Label>Question Text</Label>
                                                <Input
                                                    value={q.question}
                                                    onChange={(e) => updateQuestion(qIndex, 'question', e.target.value)}
                                                    placeholder="Enter your question..."
                                                    className="mt-2 font-medium"
                                                />
                                            </div>

                                            <div>
                                                <Label>Multiple Choice Options</Label>
                                                <div className="space-y-3 mt-2 pl-2 border-l-2 border-gray-100">
                                                    {q.options.map((option, oIndex) => (
                                                        <div key={oIndex} className="flex items-center gap-3">
                                                            <div className="relative flex items-center justify-center">
                                                                <input
                                                                    type="radio"
                                                                    name={`correct-${qIndex}`}
                                                                    checked={q.correctAnswer === oIndex}
                                                                    onChange={() => updateQuestion(qIndex, 'correctAnswer', oIndex)}
                                                                    className="w-4 h-4 text-green-600 focus:ring-green-500 border-gray-300"
                                                                />
                                                            </div>
                                                            <Input
                                                                value={option}
                                                                onChange={(e) => updateOption(qIndex, oIndex, e.target.value)}
                                                                placeholder={`Option ${oIndex + 1}`}
                                                                className={`flex-1 ${q.correctAnswer === oIndex ? 'border-green-300 bg-green-50' : ''}`}
                                                            />
                                                            {q.correctAnswer === oIndex && (
                                                                <span className="text-xs font-medium text-green-600">Correct Answer</span>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>

                        <Button
                            onClick={addQuestion}
                            variant="outline"
                            className="w-full border-dashed border-2 py-8 hover:bg-gray-50 hover:border-gray-300"
                        >
                            <Plus className="w-4 h-4 mr-2" />
                            Add Manual Question
                        </Button>

                        <div className="flex gap-4 pt-4 border-t sticky bottom-0 bg-white/80 backdrop-blur pb-4">
                            <Button
                                variant="outline"
                                onClick={() => navigate(-1)}
                                className="flex-1"
                            >
                                Back
                            </Button>
                            <Button
                                onClick={handleSave}
                                disabled={saving}
                                className="flex-1 bg-gradient-success shadow-lg hover:shadow-xl transition-all"
                            >
                                {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Check className="w-4 h-4 mr-2" />}
                                {saving ? "Saving..." : "Save & Enable Test"}
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
