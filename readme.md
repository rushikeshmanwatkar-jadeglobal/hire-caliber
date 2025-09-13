# Hire Caliber

**Hire Caliber** is an AI-powered solution designed to transform and accelerate Talent Acquisition (TA) workflows. It acts as an intelligent assistant for recruiters, automating repetitive tasks like resume screening and standardization, allowing the TA team to focus on high-value strategic interactions.

This application leverages state-of-the-art Generative AI to parse unstructured resumes, extract key information, and score candidates based on their relevance to a specific job description, all presented in a clean and intuitive web interface.

## Features

-   **Automated Resume Screening**: Upload multiple resumes (PDFs) for a specific job opening.
-   **AI-Powered Standardization**: Each resume is automatically parsed into a structured JSON format, extracting key details like professional summary, work experience, skills, and education.
-   **Semantic Relevance Scoring**: Candidates are scored and ranked based on the semantic similarity of their profile to the job description, going beyond simple keyword matching.
-   **Clean Recruiter Dashboard**: View a sortable list of candidates with standardized profiles for easy comparison.
-   **Detailed Candidate View**: Click on any candidate to see their full, parsed profile in a modal view.
-   **Modular & Scalable Architecture**: Built with a decoupled frontend and backend, using specialized databases for optimal performance.

## Tech Stack

The project is built with a modern, scalable, and AI-native technology stack.

### Backend

-   **Framework**: **FastAPI** - A high-performance Python web framework for building asynchronous APIs.
-   **AI/LLM**: **Azure OpenAI Service**
    -   `gpt-5-mini`: For structured data extraction (resume parsing).
    -   `text-embedding-3-small`: For generating vector embeddings for semantic search.
-   **Application Database**: **MongoDB** - A NoSQL document database for storing job and candidate metadata.
-   **Database ODM**: **Beanie ODM** - An asynchronous Python Object-Document Mapper for MongoDB, built on Pydantic.
-   **Vector Database**: **ChromaDB** - An open-source embedding database for storing and querying vector embeddings with high efficiency.
-   **Language**: Python 3.10+
-   **Key Libraries**: `uvicorn`, `openai`, `motor`, `pypdf`, `python-multipart`.

### Frontend

-   **Framework**: **React** - A JavaScript library for building user interfaces.
-   **UI Library**: **Material-UI (MUI)** - A comprehensive suite of UI tools to implement Google's Material Design.
-   **API Client**: **Axios** - A promise-based HTTP client for making requests to the backend.
-   **Language**: JavaScript (ES6+)

### Deployment (Recommended)

-   **Cloud Provider**: Microsoft Azure
-   **Hosting**: Azure App Service for frontend and backend.
-   **Database Hosting**: Azure Cosmos DB (with MongoDB API) and a containerized ChromaDB instance.
-   **CI/CD**: GitHub Actions.

## Project Architecture

The application follows a modular, service-oriented architecture with a clear separation of concerns:

-   **Frontend**: A standalone React single-page application (SPA).
-   **Backend API**: A FastAPI application that exposes RESTful endpoints.
-   **Service Layer**: Encapsulates the core business logic, orchestrating calls between different components.
-   **Data Access Objects (DAO)**: Manages all interactions with MongoDB via Beanie.
-   **Database Clients**: Dedicated modules for initializing and interacting with MongoDB and ChromaDB.
-   **Dual Database Strategy**:
    1.  **MongoDB**: Stores structured metadata (jobs, candidate profiles).
    2.  **ChromaDB**: Stores vector embeddings for fast similarity search.


*(Note: Replace this with your actual architecture diagram if you have one)*

## Getting Started

### Prerequisites

-   Python 3.10+ and `pip`
-   Node.js v16+ and `npm` or `yarn`
-   MongoDB instance (local or cloud-based)
-   Access to Azure OpenAI with deployed models for chat (`gpt-5-mini`) and embeddings (`text-embedding-3-small`).

### 1. Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    -   Create a file named `.env` in the project root.
    -   Copy the contents from the provided `.env` example and fill in your actual credentials.
    ```env
    # .env
    MONGO_CONNECTION_STRING="mongodb://localhost:27017/jade_hire_caliber"
    AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY"
    AZURE_OPENAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
    OPENAI_API_VERSION="2023-12-01-preview"
    EMBEDDINGS_DEPLOYMENT_NAME="hackathon-em-group5"
    CHAT_DEPLOYMENT_NAME="hackathon-group5"
    ```

5.  **Run the backend server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. You can access the auto-generated documentation at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install JavaScript dependencies:**
    ```bash
    npm install
    ```

3.  **Start the React development server:**
    ```bash
    npm start
    ```
    The frontend application will open in your browser at `http://localhost:3000`. The `proxy` setting in `package.json` will automatically forward API requests to the backend server.

## API Endpoints

The backend exposes the following RESTful API endpoints, prefixed with `/api`.

| Method | Endpoint                             | Description                                            |
| :----- | :----------------------------------- | :----------------------------------------------------- |
| `POST` | `/jobs`                              | Creates a new job posting.                             |
| `GET`  | `/jobs`                              | Retrieves a list of all job postings.                  |
| `POST` | `/jobs/{job_id}/resumes`             | Uploads one or more resume files for a specific job.   |
| `GET`  | `/jobs/{job_id}/candidates`          | Retrieves all processed candidates for a specific job. |

### Example Payloads

**POST /jobs**
```json
{
  "title": "Senior Backend Engineer",
  "description": "We are looking for a Senior Backend Engineer with experience in Python, FastAPI, and cloud services..."
}
```

**POST /jobs/{job_id}/resumes**
-   This is a `multipart/form-data` request.
-   The files should be sent under the key `resume_files`.