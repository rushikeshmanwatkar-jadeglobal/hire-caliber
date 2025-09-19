# Hire Caliber

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![React Version](https://img.shields.io/badge/react-18%2B-blue)](https://reactjs.org/)

Hire Caliber is an AI-powered Talent Acquisition Co-pilot designed to revolutionize the recruitment lifecycle. By leveraging state-of-the-art Generative AI and semantic search technologies, this platform automates and enhances critical TA workflows, enabling recruiters to identify and engage top-tier candidates with unparalleled speed and accuracy.

The system addresses key industry pain points, including manual resume screening bottlenecks, inconsistent candidate data, and the challenge of matching nuanced job requirements with complex candidate histories.

---

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Key Features](#key-features)
3.  [Architecture Overview](#architecture-overview)
4.  [Technology Stack](#technology-stack)
5.  [Prerequisites](#prerequisites)
6.  [Setup and Installation](#setup-and-installation)
7.  [Configuration](#configuration)
8.  [Running the Application](#running-the-application)
9.  [Core API Endpoints](#core-api-endpoints)
10. [Deployment Strategy](#deployment-strategy)
11. [Contributing](#contributing)
12. [License](#license)

## Project Overview

Hire Caliber provides a robust solution to augment the capabilities of Talent Acquisition teams. The platform ingests job descriptions and candidate resumes, using Large Language Models (LLMs) to intelligently parse and standardize unstructured data into a consistent, queryable format.

The core innovation lies in its multi-vector semantic matching engine. Instead of relying on keyword searches, Hire Caliber chunks rich candidate profiles and generates high-dimensional vector embeddings for each component. This allows for a granular, context-aware comparison against job requirements, uncovering strong matches that traditional systems would miss. The result is a highly accurate, ranked list of candidates, significantly reducing time-to-hire and improving the quality of the talent pipeline.

## Key Features

-   **AI-Powered Resume Standardization:** Utilizes Azure OpenAI's chat models to parse any resume format (PDF) into a detailed and structured JSON object, including work experience, skills, and project-level responsibilities.
-   **Multi-Vector Semantic Search:** Chunks standardized candidate profiles and job descriptions into meaningful components, embedding each for fine-grained similarity matching.
-   **Intelligent Candidate Ranking:** Employs cosine similarity on vector embeddings to score and rank candidates based on their holistic relevance to a job, not just keyword density.
-   **Scalable Microservice Architecture:** Decoupled FastAPI backend and React frontend ensure modularity, independent scaling, and maintainability.
-   **Dual-Database Strategy:** Leverages MongoDB for flexible metadata storage and ChromaDB for high-performance vector similarity search.
-   **Centralized Management:** Provides a clean, intuitive user interface for managing job postings and reviewing ranked candidate shortlists.

## Architecture Overview

The application is architected with a clear separation of concerns, ensuring scalability and robustness.

```   
                                         +----------------------+
                                         |   User (Recruiter) |
                                         +----------------------+
                                                    |
                                         +----------------------+
                                         | React Frontend (MUI) | 
                                         +----------------------+
                                                    |
                                         +----------------------+
                                         |   FastAPI Backend    |
                                         +----------+-----------+
                                                    |
                      +-----------------------------+-----------------------------+
                      |                             |                             |
                      v                             v                             v
             +-------------------+         +---------------------+         +-------------------+
             |   Azure OpenAI    |         |   MongoDB           |         |    ChromaDB       |
             |  (Chat & Embed)   |         | (Beanie ODM)        |         | (Vector Store)    |
             | - Standardization |         | - Candidate Profiles|         | - Resume Chunks   |
             | - Embeddings      |         | - Job Metadata      |         | - Job Embeddings  |
             +-------------------+         +---------------------+         +-------------------+
```

**Data Flow:**
1.  A recruiter uploads a job description and candidate resumes via the React frontend.
2.  The FastAPI backend receives the request and orchestrates the workflow.
3.  **Standardization:** The raw resume text is sent to the Azure OpenAI chat model to be converted into a rich JSON profile, which is stored in MongoDB.
4.  **Chunking & Embedding:** The standardized profile is converted into a detailed text document, chunked, and each chunk is sent to the Azure OpenAI embedding model.
5.  **Storage:** The resulting vectors are stored in ChromaDB, with metadata linking back to the candidate's unique ID in MongoDB.
6.  **Matching:** When a search is initiated, the job embedding is queried against the candidate vectors in ChromaDB to find the most relevant chunks.
7.  **Ranking:** The system aggregates scores to rank candidates, who are then presented on the frontend.

## Technology Stack

| Category                  | Technology                                     |
| ------------------------- | ---------------------------------------------- |
| **Backend**               | Python 3.12+, FastAPI, Beanie ODM              |
| **Frontend**              | React 18+, Material UI (MUI), Axios            |
| **AI & Machine Learning** | Azure OpenAI (Chat & Embedding Models)         |
| **Databases**             | MongoDB, ChromaDB (Vector DB) |
| **DevOps**                | Docker, Uvicorn |
| **Core Libraries**        | Pydantic, LangChain, NumPy    |

## Prerequisites

Ensure the following tools are installed on your local development machine:
-   Python 3.12 or higher
-   Node.js v18.0 or higher (with npm)
-   Docker and Docker Compose (for containerized deployment)
-   An active Microsoft Azure subscription with access to Azure OpenAI Service.

## Setup and Installation

Follow these steps to set up the project locally.

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/rushikeshmanwatkar-jadeglobal/hire-caliber.git
    cd hire-caliber
    ```

2.  **Backend Setup**
    ```sh
    # Navigate to the backend directory
    cd app

    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install Python dependencies
    pip install -r ../requirements.txt

    # Create and configure the .env file (see Configuration section below)
    cp .env.example .env
    # Edit .env with your credentials
    ```

3.  **Frontend Setup**
    ```sh
    # Navigate to the frontend directory from the root
    cd frontend

    # Install Node.js dependencies
    npm install
    ```

## Configuration

The backend relies on environment variables for configuration. Create a `.env` file in the project root by copying the example file:

```sh
cp .env.example .env
```

Then, populate the `.env` file with your specific credentials:

```env
# MongoDB Configuration
MONGO_CONNECTION_STRING="mongodb://localhost:27017/hire_caliber_db"

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY"
AZURE_OPENAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
OPENAI_API_VERSION="2023-12-01-preview"
EMBEDDINGS_DEPLOYMENT_NAME="your-embedding-deployment-name"
CHAT_DEPLOYMENT_NAME="your-chat-model-deployment-name"
```

## Running the Application

1.  **Start the Backend Server**
    From the project root directory:
    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be accessible at `http://localhost:8000`.

2.  **Start the Frontend Development Server**
    From the `/frontend` directory:
    ```sh
    npm start
    ```
    The application will be accessible at `http://localhost:3000`.

## Core API Endpoints

| Method | Endpoint                            | Description                                        |
| :----- | :---------------------------------- | :------------------------------------------------- |
| `POST` | `/api/jobs`                         | Creates a new job posting.                         |
| `GET`  | `/api/jobs`                         | Retrieves a list of all job postings.              |
| `POST` | `/api/candidates/upload`        | Uploads and creates a candidate from the resume.  |
| `GET`  | `/api/{job_id}/matches`     | Retrieves ranked candidates for a specific job.    |



## Contributing

Contributions are welcome. Please adhere to the project's coding standards and submit a pull request with a clear description of the changes. (Further contribution guidelines to be documented).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.