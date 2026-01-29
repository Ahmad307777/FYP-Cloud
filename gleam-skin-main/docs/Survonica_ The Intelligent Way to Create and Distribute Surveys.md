# Survonica: The Intelligent Way to Create and Distribute Surveys

**Final Year Project Proposal**  
**Session:** 2025-2026  
**Department:** Computer Science, Namal University Mianwali  
**Supervisor:** Dr. Ali Shahid | **Co-Supervisor:** Miss Sonia Safeer  

*A project submitted in partial fulfilment of the requirements for the degree of Bachelor of Science in Computer Science.*  
**Date:** 22 October 2025

---

## Contents
- [Project Abstract](#project-abstract)
- [1. Introduction](#1-introduction)
- [2. Problem Statement](#2-problem-statement)
- [3. Related Work](#3-related-work)
- [4. Project Rationale](#4-project-rationale)
    - [4.1 Aims and Objectives](#41-aims-and-objectives)
    - [4.2 Project Scope](#42-project-scope)
    - [4.3 Success Criterion](#43-success-criterion)
    - [4.4 Proposed Methodology and Architecture](#44-proposed-methodology-and-architecture)
- [5. Individual Tasks](#5-individual-tasks)
- [6. Tools and Technologies](#6-tools-and-technologies)
- [References](#references)

---

## Project Abstract
Survonica focuses on changing the way businesses and other institutions develop and share their surveys. Although survey tools like Google Forms and Typeform have made collecting data easier, they still do not fully address the issues of efficiency, personalization, and engaging the end user. They still require considerable manual data entry, have limited flexibility in the design of survey questions, and lack some basic features.

To address these gaps, Survonica is developing an AI-based web application that automates survey design using natural language inputs. Users will use a chatbot and describe the type of survey they wish to create, and the AI will generate relevant questions. Users will have the ability to edit survey questions to gain full control of the survey design. Survonica's ability to generate surveys makes it more interactive than existing tools. This will reduce the time, cost, and effort taken to create customized surveys, seamlessly combining web development and artificial intelligence.

---

## 1. Introduction
Surveys are essential in collecting data for decision-making in extensive fields such as business, education, healthcare, and research. Online surveys have become increasingly easy and fast to create and distribute thanks to platforms like Google Forms, Typeform, and SurveyMonkey.

However, the process of creating surveys remains lengthy and redundant. Companies are often forced to handcraft questionnaires, maintain proper formatting, and ensure they are engaging enough to garner high response rates. Respondents often face long or repeating surveys, leading to boredom or fatigue.

With the rapid development of Artificial Intelligence (AI) and Natural Language Processing (NLP), survey creation can now be automated and personalized. Survonica is an AI-driven platform that promises to revolutionize this process by combining chatbot interactions and automated question generation to minimize manual work and enhance participant interaction.

---

## 2. Problem Statement
Despite existing platforms, creating online surveys still involves considerable manual effort. Users must spend time designing attractive surveys, and questionnaires often contain redundant questions that affect efficiency and respondent experience. Ensuring a well-structured and logical flow typically requires manual review. There is a need for a smart, AI-powered, and user-friendly system that can automatically generate visually appealing surveys, detect and remove repetitive questions, and ensure a clear structure while maintaining flexibility.

---

## 3. Related Work
Current platforms include:
*   **SurveyMonkey:** User-friendly with sound analytics and "Build with AI" features, but limited editing possibilities.
*   **Google Forms:** Free and integrated with Google Workspace, ideal for simple data gathering but lacks advanced AI features.
*   **Typeform:** Focuses on user experience with conversational forms, but can be costly for premium features.

### Weaknesses of Current Platforms
*   Absence of profound AI integration (patchy question generation).
*   Low interactivity in chatbot creation.
*   Requirement for significant manual customization.
*   Cost barriers for premium analytics.

### Why Survonica is Better
*   **AI-Powered Survey Generation:** Uses natural language prompts and chatbot-style interaction.
*   **Smart Visual & Layout Customization:** Greater flexibility in editing designs and layouts.
*   **Cost-Effective & Scalable:** Accessible for university projects and small businesses.
*   **One-Stop AI Solution:** Combines generation, design, and structuring in one workflow.

---

## 4. Project Rationale
1.  **Skill Development:** Practical experience in software development and AI integration for computer science students.
2.  **Industrial Applicability:** Addressing gaps in current survey platforms with a strong AI-driven solution.

### 4.1 Aims and Objectives
**Aim:** To develop an AI-powered web-based survey creation platform that enables users to design visually appealing, non-redundant, and well-structured surveys with minimal manual effort.

**Objectives:**
*   Develop a user-friendly web application with an intuitive interface.
*   Automate survey layout and visual design using built-in templates.
*   Implement intelligent question similarity detection to remove redundancy.
*   Ensure well-structured survey flow using AI or rule-based logic.
*   Allow flexible manual editing for fine-tuning.

### 4.2 Project Scope
Survonica encompasses a web-based AI-powered platform designed to streamline survey generation. It includes an intuitive interface, automated layout templates, AI-driven redundancy detection, and logical flow organization, accessible in real-time for businesses and educational institutions.

### 4.3 Success Criterion
*   Deployment of a fully functional web-based platform.
*   Accurate AI chatbot handling of questions and redundancy.
*   Successful integration of visual and layout templates.
*   Logical structuring of survey flow.
*   Stable system operation with no critical errors.
*   Compliance with proposal requirements and supervisor endorsement.

### 4.4 Proposed Methodology and Architecture
The project follows an **Agile software development** and user-centered design approach.

#### 4.4.1 Requirements Gathering and Analysis
*   Study existing systems to identify gaps.
*   Document functional (survey creation, AI checking) and non-functional (performance, security) requirements.

#### 4.4.2 System Design
*   **Frontend:** HTML, CSS, JavaScript (React.js).
*   **Backend:** Python Django or Node.js.
*   **Database:** MySQL or MongoDB.
*   **AI Modules:** For redundancy detection and flow organization.

#### 4.4.3 Agile Development
*   Iterative development with continuous feedback.
*   Divided into sprints focusing on specific features.

#### 4.4.4 Development
*   Implementation according to planned architecture.

#### 4.4.5 Implementation
*   Deployment on a web server for real-time access.
*   Secure data flow and user authentication.

#### 4.4.6 Testing
*   Unit, integration, and User Acceptance Testing (UAT).
*   Refinement based on beta user feedback.

#### 4.4.7 Deployment and Launch
*   Cloud hosting (AWS, Azure, or Heroku).
*   Post-launch monitoring and iterative improvements.

#### 4.4.8 Future Goals
*   Voice-assisted survey creation.
*   Mobile application.
*   Integration with third-party tools like Google Workspace.

---

## Flow Chart
*(Refer to Figure 1 in the original document for the Flow Chart)*

## DFD Level 0
*(Refer to Figure 2 in the original document for the Data Flow Diagram)*

---

## 5. Individual Tasks

| Team Member | Activity | Tentative Date |
| :--- | :--- | :--- |
| Both | Planning and Setup (Tech Stack, Git/GitHub) | 1 Oct to 20 Oct 2025 |
| Ahmad Mustafa | Backend Development (API, Linking Frontend) | 15 Nov to 15 Feb |
| Abdul Qadeer | Front End Development | 1 Nov to 31 Jan |
| Ahmad Mustafa | Chatbot Integration (OpenAI API, Redundancy Detection) | 15 Dec to 15 March |
| Both | Testing and Debugging | 1 Feb to 31 Mar |
| Ahmad Mustafa | Deployment | 1 Apr to 3 Apr |
| Both | Documentation | 3 Apr to 1 May |

---

## 6. Tools and Technologies
*   **Programming Languages:** Python (Backend/AI) and JavaScript (Frontend).
*   **Frameworks:** React (Frontend) and Django/Node.js (Backend).
*   **AI Tools:** OpenAI API, Hugging Face (Natural Language Processing).
*   **Database:** MongoDB (Flexible storage for surveys and media).
*   **Deployment:** Microsoft Azure (Cloud hosting).
*   **Collaboration:** GitHub (Version control).

---

## Gantt Chart
*(Refer to Figure 3 in the original document for the Gantt Chart)*

---

## References
1. [SurveyMonkey](https://www.surveymonkey.com/home)
2. [Google Forms](https://docs.google.com/forms/u/0/?tgif=d)
3. [Typeform](https://admin.typeform.com/)
4. [Canva](https://www.canva.com/)
5. [Draw.io](https://www.drawio.com/)
6. [GitHub](https://github.com/)
