# app/db/models.py
from typing import Optional
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
    # Beanie automatically handles the `_id` field.
    filename: str
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING)
    full_text: Optional[str] = None
    error_message: Optional[str] = None

    class Settings:
        name = "candidates"  # MongoDB collection name


class Job(Document):
    title: str
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING)
    full_text: Optional[str] = None
    error_message: Optional[str] = None

    class Settings:
        name = "jobs"  # MongoDB collection name
