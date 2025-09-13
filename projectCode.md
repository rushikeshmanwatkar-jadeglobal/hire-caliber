### **Project Root Structure**

```
/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── config.py
│   ├── dao/
│   │   ├── candidate_dao.py
│   │   └── job_dao.py
│   ├── db_clients/
│   │   ├── chroma_client.py
│   │   └── mongo_client.py
│   ├── main.py
│   ├── schemas/
│   │   ├── api_schemas.py
│   │   └── db_models.py
│   ├── services/
│   │   └── ta_service.py
│   └── utils/
│       ├── ai_utils.py
│       └── file_utils.py
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.js
│       ├── components/
│       │   ├── CandidateDetailModal.js
│       │   ├── CandidateTable.js
│       │   └── FileUpload.js
│       ├── index.js
│       ├── pages/
│       │   └── Dashboard.js
│       └── services/
│           └── api.js
├── .env
└── requirements.txt
```

---

### **Backend: `/app`**

#### **File: `/.env`**

```
# MongoDB Configuration
MONGO_CONNECTION_STRING="mongodb://localhost:27017/jade_ta_db"

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_API_KEY"
AZURE_OPENAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
OPENAI_API_VERSION="2023-12-01-preview"
EMBEDDINGS_DEPLOYMENT_NAME="hackathon-em-group5"
CHAT_DEPLOYMENT_NAME="hackathon-group5"
```

#### **File: `/requirements.txt`**

```
fastapi
uvicorn[standard]
pydantic
pydantic-settings
beanie
motor
openai
python-dotenv
chromadb
pypdf
python-multipart
```

#### **File: `/app/config.py`**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    OPENAI_API_VERSION: str
    EMBEDDINGS_DEPLOYMENT_NAME: str
    CHAT_DEPLOYMENT_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
```

#### **File: `/app/db_clients/mongo_client.py`**

```python
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.schemas.db_models import Candidate, Job

async def initialize_database():
    """Initializes the MongoDB connection and Beanie ODM."""
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    await init_beanie(
        database=client.get_default_database(), 
        document_models=[Candidate, Job]
    )
```

#### **File: `/app/db_clients/chroma_client.py`**

```python
import chromadb
from typing import List

class ChromaDBClient:
    def __init__(self):
        # Using an in-memory instance for simplicity. 
        # For production, use chromadb.PersistentClient(path="/path/to/db")
        self.client = chromadb.Client()
        self.candidates_collection = self.client.get_or_create_collection(name="candidates_collection")
        self.jobs_collection = self.client.get_or_create_collection(name="jobs_collection")

    def add_embedding(self, collection_name: str, doc_id: str, embedding: List[float], metadata: dict):
        collection = self.client.get_collection(name=collection_name)
        collection.add(ids=[doc_id], embeddings=[embedding], metadatas=[metadata])

    def query_by_embedding(self, collection_name: str, query_embedding: List[float], top_k: int, filter_metadata: dict = None) -> List[str]:
        collection = self.client.get_collection(name=collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )
        return results["ids"][0] if results and results["ids"] else []

# Singleton instance to be used across the application
chroma_db_client = ChromaDBClient()
```

#### **File: `/app/schemas/db_models.py`**

```python
from beanie import Document
from pydantic import Field
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

class Job(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    title: str
    description: str

    class Settings:
        name = "jobs"

class Candidate(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str
    job_id: UUID
    relevance_score: Optional[float] = None
    standardized_profile: Dict[str, Any]

    class Settings:
        name = "candidates"
```

#### **File: `/app/schemas/api_schemas.py`**

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID

class JobCreate(BaseModel):
    title: str
    description: str

class JobResponse(JobCreate):
    id: UUID

class CandidateResponse(BaseModel):
    id: UUID
    name: str
    job_id: UUID
    relevance_score: Optional[float] = None
    standardized_profile: Dict[str, Any]
```

#### **File: `/app/dao/job_dao.py`**

```python
from uuid import UUID
from typing import Optional
from app.schemas.db_models import Job

class JobDAO:
    async def create_job(self, title: str, description: str) -> Job:
        job = Job(title=title, description=description)
        await job.insert()
        return job

    async def get_job_by_id(self, job_id: UUID) -> Optional[Job]:
        return await Job.get(job_id)

job_dao = JobDAO()
```

#### **File: `/app/dao/candidate_dao.py`**

```python
from uuid import UUID
from typing import List, Dict, Any
from app.schemas.db_models import Candidate

class CandidateDAO:
    async def create_candidate(self, name: str, profile: Dict[str, Any], score: float, job_id: UUID) -> Candidate:
        candidate = Candidate(
            name=name,
            standardized_profile=profile,
            relevance_score=score,
            job_id=job_id
        )
        await candidate.insert()
        return candidate
    
    async def get_candidates_by_job_id(self, job_id: UUID) -> List[Candidate]:
        return await Candidate.find(Candidate.job_id == job_id).sort(-Candidate.relevance_score).to_list()

candidate_dao = CandidateDAO()
```

#### **File: `/app/utils/file_utils.py`**

```python
from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(file_stream: BytesIO) -> str:
    """Extracts text content from a PDF file stream."""
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
```

#### **File: `/app/utils/ai_utils.py`**

```python
import json
import numpy as np
from openai import AsyncAzureOpenAI
from app.config import settings

# Initialize Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.OPENAI_API_VERSION,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
)

async def get_embedding(text: str) -> list[float]:
    """Generates embeddings for a given text using Azure OpenAI."""
    response = await client.embeddings.create(
        input=text,
        model=settings.EMBEDDINGS_DEPLOYMENT_NAME
    )
    return response.data[0].embedding

async def standardize_resume(raw_text: str) -> dict:
    """Uses a chat model to parse and standardize resume text into JSON."""
    system_prompt = """
    You are an expert HR assistant. Your task is to extract structured information from a resume.
    Provide the output in a valid JSON format. The JSON should contain the following keys: "name", "summary", "work_experience", "skills", and "education".
    - "name": The full name of the candidate.
    - "summary": A 2-3 sentence professional summary.
    - "work_experience": A list of objects, where each object has "title", "company", and "duration".
    - "skills": A list of key technical and soft skills.
    - "education": A list of objects with "degree" and "institution".
    IMPORTANT: Do not include any personal contact information (email, phone, address).
    """
    response = await client.chat.completions.create(
        model=settings.CHAT_DEPLOYMENT_NAME,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the resume text:\n\n{raw_text}"}
        ]
    )
    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, IndexError):
        return {"error": "Failed to parse resume content"}

def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculates the cosine similarity between two embedding vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    similarity = dot_product / (norm_a * norm_b)
    return float(similarity)

def create_summary_from_profile(profile: dict) -> str:
    """Creates a concise text summary from a standardized profile for embedding."""
    summary = profile.get("summary", "")
    skills = ", ".join(profile.get("skills", []))
    return f"Professional Summary: {summary}\nKey Skills: {skills}"
```

#### **File: `/app/services/ta_service.py`**

```python
from uuid import UUID
from typing import List
from fastapi import UploadFile
from app.dao.candidate_dao import candidate_dao
from app.dao.job_dao import job_dao
from app.db_clients.chroma_client import chroma_db_client
from app.utils import ai_utils, file_utils
from app.schemas.db_models import Candidate, Job

class TalentAcquisitionService:
    async def create_new_job(self, title: str, description: str) -> Job:
        new_job = await job_dao.create_job(title=title, description=description)
        
        # Generate and store embedding for the job description
        job_embedding = await ai_utils.get_embedding(description)
        chroma_db_client.add_embedding(
            collection_name="jobs_collection",
            doc_id=str(new_job.id),
            embedding=job_embedding,
            metadata={"title": new_job.title}
        )
        return new_job

    async def process_resumes_for_job(self, job_id: UUID, resume_files: List[UploadFile]) -> List[Candidate]:
        job = await job_dao.get_job_by_id(job_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} not found.")

        job_embedding = await ai_utils.get_embedding(job.description)
        processed_candidates = []

        for resume_file in resume_files:
            file_content = await resume_file.read()
            raw_text = file_utils.extract_text_from_pdf(file_content)
            
            standardized_profile = await ai_utils.standardize_resume(raw_text)
            if "error" in standardized_profile:
                continue # Skip resumes that fail to parse

            summary_for_embedding = ai_utils.create_summary_from_profile(standardized_profile)
            candidate_embedding = await ai_utils.get_embedding(summary_for_embedding)

            score = ai_utils.calculate_cosine_similarity(job_embedding, candidate_embedding)
            
            new_candidate = await candidate_dao.create_candidate(
                name=standardized_profile.get("name", "Unknown Candidate"),
                profile=standardized_profile,
                score=round(score * 100, 2), # Store as a percentage
                job_id=job.id
            )
            
            chroma_db_client.add_embedding(
                collection_name="candidates_collection",
                doc_id=str(new_candidate.id),
                embedding=candidate_embedding,
                metadata={"job_id": str(job.id)}
            )
            processed_candidates.append(new_candidate)
        
        return processed_candidates

    async def get_candidates_for_job(self, job_id: UUID) -> List[Candidate]:
        return await candidate_dao.get_candidates_by_job_id(job_id)
    
    async def get_all_jobs(self) -> List[Job]:
        return await Job.find_all().to_list()


ta_service = TalentAcquisitionService()
```

#### **File: `/app/api/routes.py`**

```python
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import UUID
from app.services.ta_service import ta_service, TalentAcquisitionService
from app.schemas.api_schemas import JobResponse, CandidateResponse, JobCreate

router = APIRouter()

@router.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job(job_data: JobCreate):
    """Creates a new job posting."""
    try:
        job = await ta_service.create_new_job(title=job_data.title, description=job_data.description)
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {e}")

@router.get("/jobs", response_model=List[JobResponse])
async def list_jobs():
    """Lists all available jobs."""
    return await ta_service.get_all_jobs()

@router.post("/jobs/{job_id}/resumes", response_model=List[CandidateResponse])
async def upload_resumes(job_id: UUID, resume_files: List[UploadFile] = File(...)):
    """Uploads resumes for a specific job and processes them."""
    if not resume_files:
        raise HTTPException(status_code=400, detail="No resume files provided.")
    try:
        candidates = await ta_service.process_resumes_for_job(job_id, resume_files)
        return candidates
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {e}")

@router.get("/jobs/{job_id}/candidates", response_model=List[CandidateResponse])
async def get_job_candidates(job_id: UUID):
    """Retrieves all processed candidates for a specific job, sorted by score."""
    try:
        return await ta_service.get_candidates_for_job(job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve candidates: {e}")
```

#### **File: `/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.db_clients.mongo_client import initialize_database

app = FastAPI(title="Jade TA Co-pilot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows the React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await initialize_database()

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Jade TA Co-pilot API"}
```

---

### **Frontend: `/frontend`**

#### **File: `/frontend/package.json`**

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.4",
    "@emotion/styled": "^11.11.5",
    "@mui/icons-material": "^5.15.15",
    "@mui/material": "^5.15.15",
    "axios": "^1.6.8",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://127.0.0.1:8000"
}
```

#### **File: `/frontend/src/services/api.js`**

```javascript
import axios from 'axios';

const apiClient = axios.create({
    baseURL: '/api', // Using proxy to redirect to http://127.0.0.1:8000/api
    headers: {
        'Content-Type': 'application/json',
    },
});

export const createJob = (jobData) => {
    return apiClient.post('/jobs', jobData);
};

export const getJobs = () => {
    return apiClient.get('/jobs');
};

export const uploadResumes = (jobId, files) => {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('resume_files', file);
    });
    return apiClient.post(`/jobs/${jobId}/resumes`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

export const getCandidates = (jobId) => {
    return apiClient.get(`/jobs/${jobId}/candidates`);
};
```

#### **File: `/frontend/src/index.js`**

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

const theme = createTheme({
    palette: {
        mode: 'dark',
    },
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <App />
        </ThemeProvider>
    </React.StrictMode>
);
```

#### **File: `/frontend/src/App.js`**

```javascript
import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import Dashboard from './pages/Dashboard';

function App() {
    return (
        <div>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div">
                        Jade TA Co-pilot
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container maxWidth="lg" sx={{ mt: 4 }}>
                <Dashboard />
            </Container>
        </div>
    );
}

export default App;
```

#### **File: `/frontend/src/components/FileUpload.js`**

```javascript
import React, { useState } from 'react';
import { Button, Box, CircularProgress, Typography, TextField, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const FileUpload = ({ jobs, onUpload, isLoading, onJobSelect }) => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [selectedJob, setSelectedJob] = useState('');

    const handleFileChange = (event) => {
        setSelectedFiles([...event.target.files]);
    };

    const handleJobChange = (event) => {
        const jobId = event.target.value;
        setSelectedJob(jobId);
        onJobSelect(jobId);
    };

    const handleUploadClick = () => {
        if (selectedFiles.length > 0 && selectedJob) {
            onUpload(selectedJob, selectedFiles);
        }
    };

    return (
        <Box sx={{ p: 2, border: '1px dashed grey', borderRadius: 2, textAlign: 'center' }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel id="job-select-label">Select Job</InputLabel>
                <Select
                    labelId="job-select-label"
                    value={selectedJob}
                    label="Select Job"
                    onChange={handleJobChange}
                    disabled={isLoading}
                >
                    {jobs.map((job) => (
                        <MenuItem key={job.id} value={job.id}>{job.title}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <Button
                component="label"
                variant="outlined"
                startIcon={<CloudUploadIcon />}
                disabled={!selectedJob || isLoading}
            >
                Select Resumes (PDF)
                <input type="file" hidden multiple accept=".pdf" onChange={handleFileChange} />
            </Button>
            
            {selectedFiles.length > 0 && (
                <Typography sx={{ mt: 1 }}>{selectedFiles.length} file(s) selected</Typography>
            )}

            <Box sx={{ mt: 2 }}>
                <Button
                    variant="contained"
                    onClick={handleUploadClick}
                    disabled={!selectedJob || selectedFiles.length === 0 || isLoading}
                >
                    {isLoading ? <CircularProgress size={24} /> : 'Process Resumes'}
                </Button>
            </Box>
        </Box>
    );
};

export default FileUpload;
```

#### **File: `/frontend/src/components/CandidateTable.js`**

```javascript
import React from 'react';
import {
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip,
    Typography, Box
} from '@mui/material';

const ScoreChip = ({ score }) => {
    let color = 'default';
    if (score >= 85) color = 'success';
    else if (score >= 70) color = 'warning';
    else color = 'error';
    return <Chip label={`${score}%`} color={color} />;
};

const CandidateTable = ({ candidates, onRowClick }) => {
    if (!candidates || candidates.length === 0) {
        return (
            <Typography variant="subtitle1" sx={{ mt: 3, textAlign: 'center' }}>
                No candidates processed for this job yet. Upload resumes to get started.
            </Typography>
        );
    }

    return (
        <TableContainer component={Paper} sx={{ mt: 3 }}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Relevance Score</TableCell>
                        <TableCell>Key Skills</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {candidates.map((candidate) => (
                        <TableRow
                            key={candidate.id}
                            hover
                            onClick={() => onRowClick(candidate)}
                            sx={{ cursor: 'pointer' }}
                        >
                            <TableCell>{candidate.name}</TableCell>
                            <TableCell><ScoreChip score={candidate.relevance_score} /></TableCell>
                            <TableCell>
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {candidate.standardized_profile.skills?.slice(0, 5).map((skill, index) => (
                                        <Chip key={index} label={skill} size="small" />
                                    ))}
                                </Box>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default CandidateTable;
```

#### **File: `/frontend/src/components/CandidateDetailModal.js`**

```javascript
import React from 'react';
import { Modal, Box, Typography, IconButton, Paper, Chip } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '60%',
    maxWidth: 800,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    maxHeight: '90vh',
    overflowY: 'auto'
};

const CandidateDetailModal = ({ candidate, open, onClose }) => {
    if (!candidate) return null;

    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={style}>
                <IconButton onClick={onClose} sx={{ position: 'absolute', right: 8, top: 8 }}>
                    <CloseIcon />
                </IconButton>
                <Typography variant="h5" component="h2">{candidate.name}</Typography>
                <Typography variant="h6" color="primary" gutterBottom>Relevance Score: {candidate.relevance_score}%</Typography>

                <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
                    <Typography variant="h6">Summary</Typography>
                    <Typography variant="body1">{candidate.standardized_profile.summary}</Typography>
                </Paper>

                <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
                    <Typography variant="h6">Skills</Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                        {candidate.standardized_profile.skills?.map((skill, i) => <Chip key={i} label={skill} />)}
                    </Box>
                </Paper>

                <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
                    <Typography variant="h6">Work Experience</Typography>
                    {candidate.standardized_profile.work_experience?.map((exp, i) => (
                        <Box key={i} sx={{ my: 1 }}>
                            <Typography variant="subtitle1" fontWeight="bold">{exp.title} at {exp.company}</Typography>
                            <Typography variant="body2" color="text.secondary">{exp.duration}</Typography>
                        </Box>
                    ))}
                </Paper>
            </Box>
        </Modal>
    );
};

export default CandidateDetailModal;
```

#### **File: `/frontend/src/pages/Dashboard.js`**

```javascript
import React, { useState, useEffect } from 'react';
import { Box, Typography, Alert } from '@mui/material';
import FileUpload from '../components/FileUpload';
import CandidateTable from '../components/CandidateTable';
import CandidateDetailModal from '../components/CandidateDetailModal';
import { getJobs, uploadResumes, getCandidates } from '../services/api';

const Dashboard = () => {
    const [jobs, setJobs] = useState([]);
    const [selectedJobId, setSelectedJobId] = useState('');
    const [candidates, setCandidates] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const response = await getJobs();
                setJobs(response.data);
            } catch (err) {
                setError('Failed to fetch jobs.');
            }
        };
        fetchJobs();
    }, []);

    useEffect(() => {
        const fetchCandidates = async () => {
            if (selectedJobId) {
                setIsLoading(true);
                try {
                    const response = await getCandidates(selectedJobId);
                    setCandidates(response.data);
                } catch (err) {
                    setError('Failed to fetch candidates for the selected job.');
                    setCandidates([]);
                } finally {
                    setIsLoading(false);
                }
            } else {
                setCandidates([]);
            }
        };
        fetchCandidates();
    }, [selectedJobId]);
    
    const handleUpload = async (jobId, files) => {
        setIsLoading(true);
        setError('');
        try {
            await uploadResumes(jobId, files);
            // After upload, refresh the candidate list
            const response = await getCandidates(jobId);
            setCandidates(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred during upload.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleRowClick = (candidate) => {
        setSelectedCandidate(candidate);
        setIsModalOpen(true);
    };

    return (
        <Box>
            <Typography variant="h4" gutterBottom>Candidate Screening</Typography>
            
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <FileUpload 
                jobs={jobs} 
                onUpload={handleUpload} 
                isLoading={isLoading} 
                onJobSelect={setSelectedJobId}
            />

            <CandidateTable candidates={candidates} onRowClick={handleRowClick} />
            
            <CandidateDetailModal 
                candidate={selectedCandidate} 
                open={isModalOpen} 
                onClose={() => setIsModalOpen(false)} 
            />
        </Box>
    );
};

export default Dashboard;
```