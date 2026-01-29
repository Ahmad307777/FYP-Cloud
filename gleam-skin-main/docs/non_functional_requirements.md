# Non-Functional Requirements (NFR) - Survonica

This document outlines the quality attributes, design constraints, and compliance standards that the Survonica platform must meet to ensure a professional and secure user experience.

## 1. Performance
*   **Response Time**: The system shall load the dashboard and survey editor in less than 2 seconds under normal network conditions.
*   **AI Latency**: AI-powered features (generation, analysis) shall return results within 5-10 seconds, depending on the complexity of the request and Hugging Face API availability.
*   **Concurrence**: The system shall support at least 100 concurrent survey respondents per survey without degradation in response time.

## 2. Security
*   **Data Encryption**: All data in transit shall be encrypted using TLS 1.3 (HTTPS). Data at rest in MongoDB Atlas shall be encrypted using AES-256.
*   **Authentication**: Passwords must be hashed using PBKDF2 with a SHA256 salt (handled by Django/User models). 
*   **Authorization**: The system shall strictly enforce that only the survey creator (matching `user_id`) can edit or view the results of a specific survey.
*   **Session Management**: Secure sessions shall be used to track user state, with a default timeout of 24 hours.

## 3. Scalability
*   **Database Scalability**: The system shall use MongoDB Atlas, allowing for vertical and horizontal scaling (sharding) as the volume of survey responses grows.
*   **Backend Architecture**: The Django backend shall be stateless to support horizontal scaling behind a load balancer.
*   **AI Handling**: The use of an external Inference API (Hugging Face) ensures that the computational load of Llama models does not impact the core server's performance.

## 4. Usability
*   **Responsive Design**: The system shall be fully responsive, providing a high-quality experience on mobile, tablet, and desktop devices (using Tailwind CSS).
*   **Accessibility**: The UI shall follow WCAG 2.1 Level AA guidelines to ensure accessibility for users with disabilities (leveraging Shadcn UI's accessible components).
*   **Onboarding**: New users should be able to create their first AI-assisted survey in less than 3 minutes without referring to external documentation.

## 5. Reliability & Availability
*   **Uptime**: The system shall aim for 99.9% availability.
*   **Data Persistence**: All survey responses shall be committed to the database immediately upon submission to prevent data loss.
*   **Error Handling**: The system shall provide graceful degradation. If the AI service is unavailable, users should still be able to manually create/edit surveys.

## 6. Compliance & Industry Standards
*   **GDPR/Privacy**: The system shall provide mechanisms for "Right to be Forgotten" (deleting user data) and shall clearly state data collection purposes for respondents.
*   **Standardized API**: The system shall follow RESTful API principles for all backend services to ensure interoperability.
*   **Coding Standards**: The project shall maintain high code quality by adhering to ESLint (frontend) and PEP 8 (backend) standards.
