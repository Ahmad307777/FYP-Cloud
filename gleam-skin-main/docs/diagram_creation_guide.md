# Manual Diagram Creation Guide (Draw.io)

Since you prefer to create the diagrams yourself to ensure they match your exact vision, here are the step-by-step instructions to recreate the **Pastel Style ERD** and **Activity Diagram** using **Draw.io** (free online tool).

## 1. Entity Relationship Diagram (ERD)

**Goal:** Create a "Pastel" aesthetic diagram showing the database structure.

**Step 1: Setup**
1.  Go to [draw.io](https://app.diagrams.net/).
2.  Create a New Diagram (Blank).
3.  On the left sidebar, search for "Entity Relation" to see table shapes.

**Step 2: Create Entities (The Boxes)**
Use the "Table" shape (or "List" shape) for each entity.
*   **Color Palette (Pastel):**
    *   **User Table:** Header `#D7CCC8` (Light Brown), Body `#EFEBE9`.
    *   **Survey Table:** Header `#B3E5FC` (Light Blue), Body `#E1F5FE`.
    *   **QualificationTest:** Header `#C8E6C9` (Light Green), Body `#E8F5E9`.
    *   **SurveyResponse:** Header `#FFF9C4` (Light Yellow), Body `#FFFDE7`.
    *   **RespondentQualification:** Header `#F8BBD0` (Light Pink), Body `#FCE4EC`.

**Step 3: Define Fields**
*   **User:** id (PK), username, email, password.
*   **Survey:** id (PK), user_id (FK), title, questions, is_active.
*   **QualificationTest:** id (PK), survey_id (FK), topic, time_limit.
*   **SurveyResponse:** id (PK), survey_id (FK), email, responses, score.
*   **RespondentQualification:** id (PK), survey_id (FK), email, passed.

**Step 4: Connect Them**
Use "Orthogonal" lines (Right-angled lines).
*   **User** `||--<` **Survey** (One-to-Many).
*   **Survey** `||--|` **QualificationTest** (One-to-One).
*   **Survey** `||--<` **SurveyResponse** (One-to-Many).
*   **Survey** `||--<` **RespondentQualification** (One-to-Many).

---

## 2. Activity Diagram

**Goal:** Show the flow `User -> System -> Respondent`.

**Step 1: Setup Swimlanes**
1.  Search for "Pool" or "Swimlane" in draw.io.
2.  Create a Pool with 3 Lanes:
    *   **Lane 1:** User (Survey Creator)
    *   **Lane 2:** System (AI & Backend)
    *   **Lane 3:** Respondent

**Step 2: The Flow**
*   **User Lane:**
    *   Start Circle -> Box "Login" -> Box "Dashboard".
    *   Diamond "Method?" -> "AI" or "Manual".
*   **System Lane:**
    *   Box "AI Generates Survey" (Connected from User AI choice).
    *   Box "AI Audits Bias" (Connected from User Manual choice).
*   **User Lane (Again):**
    *   Box "Review & Distribute".
*   **Respondent Lane:**
    *   Box "Access Link".
    *   Diamond "Qualified?".
    *   Box "Fill Survey".
*   **System Lane (Again):**
    *   Box "Calculate Trust Score".
*   **User Lane (Final):**
    *   Box "View Analytics" -> End Circle.

**Step 3: Styling**
*   Use Rounded Rectangles for actions.
*   Use Diamonds for decisions.
*   Keep colors consistent with your report theme (Blue/White/Grey).
