# app/db/models.py
from typing import Optional, Dict, Any
from enum import Enum
from pymongo import ASCENDING
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class ProcessingStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class Candidate(Document):
    name: str
    full_text: Optional[str] = None
    error_message: Optional[str] = None
    job_id: Optional[PydanticObjectId] = None
    relevance_score: Optional[float] = None
    standardized_profile: Dict[str, Any]

    class Settings:
        name = "candidates"


class Job(Document):
    title: str
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING)
    full_text: Optional[str] = None
    error_message: Optional[str] = None

    class Settings:
        name = "jobs"  # MongoDB collection name
