# Survonica: Entity Relationship Diagram (ERD)

This document describes the database schema and relationships for the Survonica system using Mermaid.

## Mermaid ER Diagram

```mermaid
erDiagram
    User ||--o{ Survey : "creates"
    Survey ||--o{ QualificationTest : "has"
    Survey ||--o{ SurveyResponse : "collects"
    Survey ||--o{ RespondentQualification : "validates"
    
    User {
        string id PK
        string email
        string password_hash
    }

    Survey {
        string id PK
        string user_id FK
        string title
        string description
        string template
        json questions
        boolean require_qualification
        int qualification_pass_score
        string[] allowed_domains
        json design
        int response_counter
        datetime created_at
    }

    QualificationTest {
        string id PK
        string survey_id FK
        string topic
        json questions
        int time_limit
        datetime created_at
    }

    SurveyResponse {
        string id PK
        string survey_id FK
        string respondent_email
        json responses
        int quality_score
        json quality_analysis
        boolean is_flagged
        datetime completed_at
    }

    RespondentQualification {
        string id PK
        string survey_id FK
        string respondent_email
        string qualification_name
        int score
        boolean passed
        datetime created_at
    }

    AIModel {
        string id PK
        string name
        string version
        string type
        string status
        boolean is_active
        string model_path
    }
```

## Entity Descriptions

1. **User**: Represents the survey creator. (Managed via Authentication Service).
2. **Survey**: The core entity storing survey structure, settings, and questions.
3. **QualificationTest**: Optional pre-screening test attached to a survey.
4. **SurveyResponse**: Stores the actual answers provided by a respondent, including quality metrics.
5. **RespondentQualification**: records the result of a respondent taking a qualification test.
6. **AIModel**: Metadata about local AI models used for quality/sentiment analysis.
