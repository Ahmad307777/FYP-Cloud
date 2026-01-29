# Survonica: Data Flow Diagram (DFD) Report

This document provides a formal representation of data flow within the Survonica system at two levels of abstraction.

## 1. DFD Level 0: Context Diagram
The Context Diagram represents the entire **Survonica System** as a single process and illustrates its interactions with external entities. Each functionality is represented by a distinct data flow arrow as requested.

```mermaid
graph TD
    %% External Entities
    Creator["Survey Creator"]
    Respondent["Respondent"]
    AI_Service["AI Service (Llama/SD)"]

    %% Main Process
    System(("(0) <br/> Survonica <br/> System"))

    %% Creator Interactions (Functionality-Specific Flows)
    Creator -- "1. Login Credentials" --> System
    System -- "2. Auth Status & Tokens" --> Creator
    Creator -- "3. Voice/Chat Commands" --> System
    System -- "4. AI-Generated Drafts" --> Creator
    Creator -- "5. Custom Branding (Logos/Fonts)" --> System
    Creator -- "6. Qualification Rules" --> System
    System -- "7. Redundancy/Bias Alerts" --> Creator
    Creator -- "8. Distribution Lists (Emails)" --> System
    System -- "9. Live Survey Links" --> Creator
    System -- "10. Analytics Reports & Insights" --> Creator

    %% Respondent Interactions
    System -- "11. Screening/Qualification Form" --> Respondent
    Respondent -- "12. Screening Answers" --> System
    System -- "13. Validated Survey Questions" --> Respondent
    Respondent -- "14. Completed Survey Responses" --> System
    System -- "15. Submission Confirmation" --> Respondent

    %% AI Service Interactions
    System -- "16. Content Generation Prompts" --> AI_Service
    AI_Service -- "17. Generated JSON (Q/A/Options)" --> System
    System -- "18. Image Generation Specs" --> AI_Service
    AI_Service -- "19. Generated Graphic Assets" --> System
    System -- "20. Raw Text Data for Analysis" --> AI_Service
    AI_Service -- "21. Sentiment/Trend Labels" --> System
```

---

## 2. DFD Level 1: Process Decomposition
Level 1 breaks down the system into its core functional components, surfacing internal data stores and process-to-process interactions.

```mermaid
graph LR
    %% External Entities
    Creator["Creator"]
    Res["Respondent"]
    AI["AI Service"]

    %% Data Stores
    D1[("D1: User Data")]
    D2[("D2: Survey Data")]
    D3[("D3: Response Data")]
    D4[("D4: Analytics Data")]

    %% Processes
    P1["(1.0) Auth & Profile Mgmt"]
    P2["(2.0) AI Survey Builder"]
    P3["(3.0) Qual & Screening Mgr"]
    P4["(4.0) Distribution Engine"]
    P5["(5.0) Survey Engine & QC"]
    P6["(6.0) AI Analytics Engine"]

    %% P1 Flows
    Creator -- "Credentials" --> P1
    P1 -- "User Records" --> D1
    D1 -- "Verified Profile" --> P1
    P1 -- "Auth Token" --> Creator

    %% P2 Flows
    Creator -- "Commands" --> P2
    P2 -- "Prompts" --> AI
    AI -- "Generated JSON" --> P2
    P2 -- "Draft Qs" --> Creator
    P2 -- "Survey Schema" --> D2

    %% P3 Flows
    Creator -- "Test Rules" --> P3
    P3 -- "Qual Tests" --> D2

    %% P4 Flows
    Creator -- "Target Emails" --> P4
    P4 -- "Survey ID" --> D2
    D2 -- "Survey Metadata" --> P4
    P4 -- "Public Links" --> Creator

    %% P5 Flows
    P4 -- "Link Access" --> Res
    Res -- "Screening Answers" --> P5
    D2 -- "Validation Rules" --> P5
    P5 -- "Survey Form" --> Res
    Res -- "Completed Response" --> P5
    P5 -- "Quality Scores" --> D3
    P5 -- "Raw Answers" --> D3

    %% P6 Flows
    Creator -- "Request Report" --> P6
    D3 -- "Raw Data" --> P6
    P6 -- "Text for NLP" --> AI
    AI -- "Sentiment Results" --> P6
    P6 -- "Insights" --> D4
    P6 -- "Reports" --> Creator
```

---

## 3. Data Flow Definitions

| ID | Data Flow | Source | Destination | Description |
| :--- | :--- | :--- | :--- | :--- |
| **1-2** | Auth Flow | Creator | P1.0 | Handles secure access and user identity setup. |
| **3-4** | Generative Flow | Creator | P2.0 | High-level commands used to drive the Llama 3.2 engine. |
| **7** | Quality Alerts | P2.0 | Creator | Proactive warnings about biased or duplicate questions. |
| **11-12** | Screening Flow | P5.0 | Respondent | Ensures respondents meet criteria before data collection. |
| **20-21** | Analytics Flow | P6.0 | AI Service | Deep analysis of natural language responses for sentiment. |

## 4. Formal DFD Rules Followed
1.  **Conservation of Data:** All processes have at least one input and one output.
2.  **No direct External Entity interactions:** All communication between Creator and Respondent passes through the system.
3.  **No direct Data Store interactions:** Data stores are only accessed/modified through a process.
4.  **Unique Flows:** Every label in Level 0 represents a distinct functional interaction, avoiding "Generic Data" labels.
