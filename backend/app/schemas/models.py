# app/schemas/models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class ProcessingStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class BaseDocument(BaseModel):
    status: ProcessingStatus = ProcessingStatus.PENDING
    full_text: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            # If you use ObjectId, you need an encoder
            # from bson import ObjectId
            # ObjectId: str
        }


class Candidate(BaseDocument):
    filename: str


class Job(BaseDocument):
    title: str
    description: str


class MatchResult(BaseModel):
    candidate_id: str
    candidate_filename: str
    score: float
    justification: Optional[str] = (
        "Score is based on semantic similarity of resume chunks to the job description."
    )
