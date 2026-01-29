# Codewise Logic Explanation - Survonica

This document explains exactly how each feature works, which files are involved, and the specific functions used.

---

## 1. Authentication & Security
### How it works:
The system uses a custom session-based authentication for MongoDB. It doesn't use the default Django auth system because MongoDB (via MongoEngine) requires a different User model approach.

*   **File**: `backend/authentication/views.py`
*   **Functions**:
    *   `register_view(request)`: Validates input (regex for email, length for password), checks for existing users, hashes the password using `user.set_password()`, and saves it to MongoDB Atlas.
    *   `login_view(request)`: Authenticates credentials. If correct, it stores the MongoDB `user_id` in the `request.session`.
*   **Frontend Connection**: `src/pages/Login.tsx` and `Signup.tsx` send POST requests to these endpoints. Resulting user state is managed in the frontend by `authStore.ts`.

---

## 2. AI Survey Generation (Conversational)
### How it works:
This feature uses a "dual-prompt" strategy with Meta's **Llama 3.1** models via Hugging Face.

*   **File**: `backend/surveys/ai_helper.py`
*   **Functions**:
    *   `chat_with_llama(messages)`: This is the interactive chatbot logic. It takes the conversation history and a system prompt to act as a "Survey Designer."
    *   `generate_survey_from_conversation(conversation_history)`: This is the "Magic" button. It analyzes the *entire* chat history and forces the AI to output a valid JSON structure containing `title` and `questions`.
*   **API View**: `backend/surveys/views/ai_views.py` -> `generate_survey_from_chat`.
*   **Frontend**: `src/pages/AiSurveyAssistant.tsx` manages the chat UI and calls the generation endpoint.

---

## 3. Redundancy & Duplicate Detection
### How it works:
It uses AI "Semantic Similarity" rather than exact text matching. This means it can find two questions that are worded differently but ask the same thing.

*   **File**: `backend/surveys/ai_helper.py`
*   **Function**: `detect_duplicate_questions(questions)`
    *   **Logic**: It feeds the list of questions to Llama and asks it to return a JSON array of `indices` that are similar, along with a "reason."
*   **Frontend**: `src/components/RedundancyChecker.tsx` receives these indices and highlights them for the user to "Merge" or "Delete."

---

## 4. Qualification Tests (Screening)
### How it works:
Users can create a "Mini-Test" that acts as a gatekeeper. Respondent performance on this test determines if they can proceed to the main survey.

*   **File**: `backend/surveys/models.py`
*   **Structure**:
    *   `QualificationTest`: Stores the screening questions.
    *   `RespondentQualification`: Stores the result (pass/fail) for a specific user.
*   **Logic**: In `src/pages/SurveyResponse.tsx`, before showing the survey, the system checks if a `QualificationTest` exists for the survey ID. If it does, the user must pass it first.

---

## 5. Automated AI Analysis (Reporting)
### How it works:
When a creator views results, the system aggregates raw data and sends a summary to the AI for high-level insights.

*   **File**: `backend/surveys/ai_helper.py`
*   **Function**: `analyze_survey_results(...)`
    *   **Logic**:
        1.  **Aggregation**: It loops through all `SurveyResponse` objects and calculates percentages for multiple-choice questions.
        2.  **AI Prompting**: It sends this statistical summary + a sample of text answers to Llama.
        3.  **Insight Generation**: Llama returns a JSON report containing `sentiment`, `keyInsights`, and `improvementSuggestions`.
*   **Frontend**: `src/pages/SurveyResults.tsx` renders this AI-generated report alongside charts (likely using Recharts/Chart.js).

---

## 6. Survey Distribution (Email Invites)
### How it works:
The system integrates SMTP directly into the survey management workflow.

*   **File**: `backend/surveys/views/survey_views.py`
*   **Function**: `send_invite(request, pk)`
    *   **Logic**: It takes a list of emails and a `survey_id`, constructs a URL (`/survey/{id}`), and uses Django's `send_mail` function. It also saves domain restrictions (like `allowed_domains`) to the Survey model at the same time.
