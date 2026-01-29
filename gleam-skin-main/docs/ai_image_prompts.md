# AI Image Generation Prompts

Use these prompts with AI tools (like Gemini, ChatGPT w/ DALL-E, Midjourney) to generate the diagrams if you have quota or access to other tools.

## 1. Use Case Diagram Prompt
**Copy and paste this:**

> A professional, white-background UML Use Case Diagram for a survey system named 'Survonica'.
>
> **Actors:**
> *   **Survey Creator** (stick figure, left side)
> *   **Respondent** (stick figure, right side)
> *   **AI Service** (rectangular box, bottom or side)
>
> **System Boundary:** A large rectangle labeled "Survonica System" containing the use cases.
>
> **Use Cases (Ovals inside the boundary):**
> *   Login / Register
> *   Create Survey with AI Assistant
> *   Generate Questions from Chat
> *   Detect Redundancies
> *   Edit Survey Manually
> *   Distribute Survey
> *   View Analytics
> *   Take Survey
>
> **Relationships (Lines):**
> *   Solid lines connecting Creator to Login, Create, Edit, Distribute, Analytics.
> *   Solid line connecting Respondent to Take Survey.
> *   Dashed arrows labeled "<<include>>" from 'Create Survey' to 'Generate Questions' and 'Detect Redundancies'.
> *   Lines connecting 'Generate Questions' and 'Detect Redundancies' to the external 'AI Service' actor.
>
> **Style:** Clean, modern, blue and white color scheme, high logic visibility, no cluttered text.

---

## 2. Entity Relationship Diagram (ERD) Prompt
**Copy and paste this:**

> A professional Entity Relationship Diagram (ERD) for a survey application database.
>
> **Entities (Tables):**
> 1.  **User**: Fields (ID, Email, Password)
> 2.  **Survey**: Fields (ID, Title, Questions_JSON, Config, User_ID_FK)
> 3.  **QualificationTest**: Fields (ID, Topic, Min_Score, Survey_ID_FK)
> 4.  **SurveyResponse**: Fields (ID, Respondent_Email, Answers_JSON, Quality_Score, Survey_ID_FK)
> 5.  **AIModel**: Fields (ID, Name, Status, Accuracy)
>
> **Relationships (Crow's Foot Notation):**
> *   **User** has a **One-to-Many** relationship with **Survey**.
> *   **Survey** has a **One-to-Many** relationship with **SurveyResponse**.
> *   **Survey** has a **One-to-One** (or One-to-Many) relationship with **QualificationTest**.
>
> **Style:** Technical diagram, white background, standard Crow's Foot notation, distinct boxes for entities with headers for table names and lists for attributes. Use blue for headers and black for text.

---

## 3. Data Flow Diagram (DFD Level 0) Prompt
**Copy and paste this:**

> A DFD Level 0 (Context Diagram) for the 'Survonica' system.
>
> **Central Process:** A single circle or rounded rectangle in the center labeled "0. Survonica System".
>
> **External Entities (Squares):**
> 1.  **Survey Creator**
> 2.  **Respondent**
> 3.  **AI Service**
>
> **Data Flows (Arrows):**
> *   **Creator to System:** Login Credentials, commands (Create Survey), Configuration.
> *   **System to Creator:** Analytics Reports, Quality Alerts, Survey Links.
> *   **System to Respondent:** Survey Form, Qualification Test.
> *   **Respondent to System:** Completed Answers, Test Results.
> *   **System to AI Service:** Prompts, Raw Text for Analysis.
> *   **AI Service to System:** Generated Questions, Sentiment Analysis Results.
>
> **Style:** Standard Gane-Sarson or DeMarco notation. Clean lines, clearly labeled arrows, professional technical aesthetic.

---

## 4. System Architecture Diagram Prompt
**Copy and paste this:**

> A professional, high-level technical architecture diagram for a web application named 'Survonica'.
>
> **Architecture Layers:**
> 1. **Client Layer (Frontend):** A box labeled "React SPA (Vite + Tailwind CSS)". Inside, list: Auth, AI Survey Builder, Analytics Dashboard, Voice Assistant.
> 2. **API Layer (Backend)::** A box labeled "Django REST Framework". Inside, list: User Mgmt, Survey Logic, AI Integration Service, Response Auditor.
> 3. **Database Layer:** A cylinder icon labeled "PostgreSQL / Supabase (Relational DB)".
> 4. **AI Services (External):** A cloud icon labeled "Hugging Face Inference API". List: Llama 3.2 (Text/NLP), Stable Diffusion (Images).
>
> **Connections (Arrows):**
> *   Bidirectional arrow between **Client** and **API Layer** (HTTPS/JSON).
> *   Bidirectional arrow between **API Layer** and **Database** (DB Queries).
> *   One-way arrow from **API Layer** to **AI Services** (Prompts/Raw Data).
> *   One-way arrow from **AI Services** back to **API Layer** (Generated Content/Insights).
>
> **Style:** Modern, sleek, dark-blue and teal color palette. Use isometric 3D or clean 2D flat design. High resolution, professional tech whitepaper style, clear labels.
