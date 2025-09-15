# app/schemas/api_models.py
from click import Option
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from beanie import PydanticObjectId
from app.db.models import ProcessingStatus  # Reuse the enum


class DocumentStatusResponse(BaseModel):
    id: PydanticObjectId
    status: ProcessingStatus
    error: Optional[str] = None


class CandidateResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    name: str
    standardized_profile: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}  # Serialize ObjectId to string for JSON


class JobResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    title: str
    description: str

    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}


class MatchResult(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    name: str
    relevance_score: Optional[Any] = None
    standardized_profile: Optional[Any] = None

    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}
