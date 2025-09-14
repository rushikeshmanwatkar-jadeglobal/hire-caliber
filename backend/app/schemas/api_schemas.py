# app/schemas/api_models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from beanie import PydanticObjectId
from app.db.models import ProcessingStatus  # Reuse the enum


class DocumentStatusResponse(BaseModel):
    id: PydanticObjectId
    status: ProcessingStatus
    error: Optional[str] = None


class CandidateResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    filename: str
    status: ProcessingStatus

    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}  # Serialize ObjectId to string for JSON


class JobResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    title: str
    status: ProcessingStatus

    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}


class MatchResult(BaseModel):
    candidate_id: PydanticObjectId
    candidate_filename: str
    score: float
    justification: Optional[str] = (
        "Score is based on semantic similarity of resume chunks to the job description."
    )

    class Config:
        json_encoders = {PydanticObjectId: str}
