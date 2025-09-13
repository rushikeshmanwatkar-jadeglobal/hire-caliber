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
