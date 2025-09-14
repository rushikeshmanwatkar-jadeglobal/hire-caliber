# app/api/jobs.py
from typing import List
from fastapi import APIRouter, HTTPException, Body
from beanie import PydanticObjectId

from app.db.models import Job, ProcessingStatus
from app.schemas.api_schemas import JobResponse, DocumentStatusResponse, MatchResult
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/jobs", tags=["Jobs"])

from app.services.ta_service import TalentAcquisitionService
from app.schemas.api_schemas import JobResponse, CandidateResponse


@router.get("/", status_code=200)
async def list_jobs():
    """Lists all available jobs."""
    try:
        return await TalentAcquisitionService.get_all_jobs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=201)
async def upload_job_description(title: str = Body(...), content: str = Body(...)):
    """Upload a job description and start background processing."""
    try:
        job = await TalentAcquisitionService.create_new_job(
            title=title, description=content
        )
        return JobResponse(**job.model_dump(by_alias=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/matches")
async def get_job_matches(job_id: PydanticObjectId):
    """Get the top candidate matches for a specific job."""
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    try:
        matches = await MatchingService.find_matches_for_job(str(job.id))
        return matches
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# chroma run --path /chroma_db_path
