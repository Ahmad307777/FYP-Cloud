# Functional Requirements - Survonica

Survonica is an intelligent survey platform that leverages AI to simplify survey design, improve question quality, and provide deep insights from responses.

## 1. User Management & Authentication
| Requirement ID | Description |
| :--- | :--- |

| FR-1.1 | The system shall allow users to create an account with email and password. |
| FR-1.2 | The system shall allow users to log in securely. |
| FR-1.3 | The system shall provide a dashboard for users to manage their surveys (list, edit, delete, view results). |

## 2. AI-Powered Survey Creation
| Requirement ID | Description |
| :--- | :--- |
| FR-2.1 | The system shall provide an AI Assistant (chatbot) to help users brainstorm and generate surveys through conversation. |
| FR-2.2 | The system shall automatically generate a structured survey (title, description, questions) from a conversation history. |
| FR-2.3 | The system shall detect redundant or duplicate questions using AI and suggest removals or merges. |
| FR-2.4 | The system shall generate suggested multiple-choice options for questions using AI. |
| FR-2.5 | The system shall allow users to generate custom images for survey branding or questions using AI text-to-image. |

## 3. Survey Editing & Customization
- **FR-3.1**: The system shall provide a visual Survey Editor to manually add, edit, or reorder questions.
- **FR-3.2**: The system shall support multiple question types (e.g., Multiple Choice, Text, Rating Scales).
- **FR-3.3**: The system shall allow users to apply visual templates to surveys for professional styling.
- **FR-3.4**: The system shall allow users to preview surveys before publication.

## 4. Quality Control & Quality Screening
- **FR-4.1**: The system shall allow creators to define Qualification Tests to screen respondents.
- **FR-4.2**: The system shall prevent unqualified respondents from accessing the main survey based on test performance.
- **FR-4.3**: The system shall allow creators to set domain restrictions (e.g., only allowing respondents from a specific corporate domain).

## 5. Survey Distribution
- **FR-5.1**: The system shall allow creators to send email invitations to potential respondents directly from the platform.
- **FR-5.2**: The system shall generate a unique public URL for each survey for easy sharing.
- **FR-5.3**: The system shall allow creators to track the number of invitations sent and responses received.

## 6. Response Collection
- **FR-6.1**: The system shall provide a clean, responsive interface for respondents to participate in surveys.
- **FR-6.2**: The system shall securely store respondent answers in the database (MongoDB).
- **FR-6.3**: The system shall ensure that mandatory questions are answered before submission.

## 7. Reporting & AI Analysis
- **FR-7.1**: The system shall provide a real-time dashboard for survey results.
- **FR-7.2**: The system shall use AI to analyze open-ended responses and identify sentiment or key themes.
- **FR-7.3**: The system shall provide summary statistics (e.g., percentages, averages) for all survey data.
