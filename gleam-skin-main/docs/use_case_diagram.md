# Survonica: Use Case Diagram

This document defines the actors and use cases for the Survonica system.

## 1. Use Case Diagram (Mermaid)

```mermaid
usecaseDiagram
    actor Creator as "Survey Creator"
    actor Respondent as "Respondent"
    actor AI as "AI Service"

    subgraph "Survonica System"
        usecase "Login / Register" as UC1
        usecase "Create Survey with AI Assistant" as UC2
        usecase "Generate Questions from Chat" as UC3
        usecase "Detect Redundancies & Bias" as UC4
        usecase "Generate Branding Images" as UC5
        usecase "Edit Survey Manually" as UC6
        usecase "Add Qualification Test" as UC7
        usecase "Distribute Survey (Email/Link)" as UC8
        usecase "View Real-time Analytics" as UC9
        usecase "Analyze Sentiments & Trends" as UC10
        
        usecase "Complete Qualification Test" as UC11
        usecase "Take Survey" as UC12
        usecase "Submit Response" as UC13
    end

    %% Creator Interactions
    Creator --> UC1
    Creator --> UC2
    Creator --> UC6
    Creator --> UC7
    Creator --> UC8
    Creator --> UC9
    Creator --> UC5

    %% Includes/Extensions
    UC2 ..> UC3 : <<include>>
    UC2 ..> UC4 : <<include>>
    UC9 ..> UC10 : <<include>>
    UC12 ..> UC11 : <<include>>
    UC12 ..> UC13 : <<include>>

    %% AI Service Interactions
    UC3 -- AI
    UC4 -- AI
    UC5 -- AI
    UC10 -- AI

    %% Respondent Interactions
    Respondent --> UC11
    Respondent --> UC12
```

## 2. Use Case Descriptions

| Use Case ID | Name | Actor(s) | Description |
| :--- | :--- | :--- | :--- |
| **UC1** | Login / Register | Creator | Allows the creator to access their account and manage surveys. |
| **UC2** | Create Survey with AI Assistant | Creator, AI | The main flow for generating a survey through a conversational interface. |
| **UC3** | Generate Questions from Chat | Creator, AI | Specifically handles the AI generation of questions based on user input. |
| **UC4** | Detect Redundancies & Bias | Creator, AI | Automatically scans questions to ensure high quality and no duplicates. |
| **UC5** | Generate Branding Images | Creator, AI | Uses DALL-E/Stable Diffusion to create logos or custom survey art. |
| **UC6** | Edit Survey Manually | Creator | Fine-tuning of questions, reordering, and adding custom logic. |
| **UC7** | Add Qualification Test | Creator | Defining criteria that respondents must meet to participate. |
| **UC8** | Distribute Survey | Creator | Sending emails or sharing links to reach the target audience. |
| **UC9** | View Real-time Analytics | Creator | Accessing a dashboard to see live response data and charts. |
| **UC10** | Analyze Sentiments | Creator, AI | Performing NLP analysis on open-ended text answers. |
| **UC11** | Complete Qual Test | Respondent | The screening process where respondents answer pre-requisite questions. |
| **UC12** | Take Survey | Respondent | The core activity of answering survey questions. |
| **UC13** | Submit Response | Respondent | Finalizing and saving the respondent's data to the system. |
