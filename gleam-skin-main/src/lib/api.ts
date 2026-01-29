const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export const api = {
    // Auth
    login: async (credentials: any) => {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Login failed");
        return response.json();
    },

    register: async (data: any) => {
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Registration failed");
        return response.json();
    },

    logout: async () => {
        const response = await fetch(`${API_BASE_URL}/auth/logout/`, {
            method: "POST",
            credentials: "include",
        });
        return { success: true };
    },

    // Surveys
    getSurveys: async () => {
        const response = await fetch(`${API_BASE_URL}/surveys/`, {
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch surveys");
        return response.json();
    },

    getSurvey: async (id: string) => {
        const response = await fetch(`${API_BASE_URL}/surveys/${id}/`, {
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch survey");
        return response.json();
    },

    saveSurvey: async (data: any) => {
        const response = await fetch(`${API_BASE_URL}/surveys/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to save survey");
        return response.json();
    },

    updateSurvey: async (id: string, data: any) => {
        const response = await fetch(`${API_BASE_URL}/surveys/${id}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to update survey");
        return response.json();
    },

    deleteSurvey: async (id: string) => {
        const response = await fetch(`${API_BASE_URL}/surveys/${id}/`, {
            method: "DELETE",
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to delete survey");
        return true;
    },

    getSurveyResponses: async (surveyId: string) => {
        const response = await fetch(`${API_BASE_URL}/survey-responses/?survey=${surveyId}`, {
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch responses");
        return response.json();
    },

    submitSurveyResponse: async (data: any) => {
        const response = await fetch(`${API_BASE_URL}/survey-responses/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to submit response");
        return response.json();
    },

    getQualificationTests: async (surveyId: string) => {
        const response = await fetch(`${API_BASE_URL}/qualification-tests/?survey=${surveyId}`, {
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch qualification tests");
        return response.json();
    },

    sendInvites: async (id: string, data: any) => {
        const response = await fetch(`${API_BASE_URL}/surveys/${id}/send_invite/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to send invites");
        return response.json();
    },

    createQualificationTest: async (data: any) => {
        const response = await fetch(`${API_BASE_URL}/qualification-tests/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to create qualification test");
        return response.json();
    },

    generateQualification: async (topic: string, numQuestions: number) => {
        const response = await fetch(`${API_BASE_URL}/ai/generate-qualification/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, numQuestions }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to generate qualification test");
        return response.json();
    },

    // AI Assistant
    chatWithAI: async (messages: any[]) => {
        const response = await fetch(`${API_BASE_URL}/ai/chat/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("AI Chat failed");
        return response.json();
    },

    generateSurveyFromChat: async (messages: any[]) => {
        const response = await fetch(`${API_BASE_URL}/ai/generate-from-chat/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ conversation: messages }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("AI Generation failed");
        return response.json();
    },

    generateOptions: async (question: string) => {
        const response = await fetch(`${API_BASE_URL}/ai/generate-options/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to generate options");
        return response.json();
    },

    generateImage: async (prompt: string) => {
        const response = await fetch(`${API_BASE_URL}/ai/generate-image/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to generate image");
        return response.json();
    },

    auditQuality: async (questions: any[]) => {
        const response = await fetch(`${API_BASE_URL}/ai/audit-quality/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ questions }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to audit quality");
        return response.json();
    },

    analyzeSurvey: async (surveyId: string) => {
        const response = await fetch(`${API_BASE_URL}/ai/analyze/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ surveyId }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to analyze survey");
        return response.json();
    },

    detectRedundancy: async (questions: any[]) => {
        const response = await fetch(`${API_BASE_URL}/ai/detect-redundancy/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ questions }),
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to detect redundancy");
        return response.json();
    },

    trainLocalModel: async () => {
        const response = await fetch(`${API_BASE_URL}/ai/train/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
        });
        if (!response.ok) throw new Error("Training failed");
        return response.json();
    },

    getTrainedModels: async () => {
        const response = await fetch(`${API_BASE_URL}/ai/models/`, {
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch models");
        return response.json();
    },

    toggleModel: async (modelId: string) => {
        const response = await fetch(`${API_BASE_URL}/ai/models/${modelId}/toggle/`, {
            method: "POST",
            credentials: "include",
        });
        if (!response.ok) throw new Error("Toggle failed");
        return response.json();
    },
};
