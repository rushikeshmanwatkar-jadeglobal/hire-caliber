# app/api/jobs.py
from typing import List
from fastapi import APIRouter, HTTPException, Body
from beanie import PydanticObjectId

from app.db.models import Job, ProcessingStatus
from app.schemas.api_schemas import JobResponse, DocumentStatusResponse, MatchResult
from app.tasks.process import _process_job
from app.services.matching_service import find_matches_for_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

from app.services.ta_service import (
    TalentAcquisitionService,
    TalentAcquisitionService,
)
from app.schemas.api_schemas import JobResponse, CandidateResponse


@router.get("/", response_model=List[JobResponse])
async def list_jobs():
    """Lists all available jobs."""
    return await TalentAcquisitionService.get_all_jobs()


@router.post("/", response_model=JobResponse, status_code=202)
async def upload_job_description(title: str = Body(...), content: str = Body(...)):
    """Upload a job description and start background processing."""
    try:
        job = Job(title=title, full_text=content)
        await job.create()

        await _process_job(str(job.id), title, content)

        return JobResponse(**job.model_dump(by_alias=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/matches")
async def get_job_matches(job_id: PydanticObjectId):
    """Get the top candidate matches for a specific job."""
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job.status != ProcessingStatus.COMPLETED:
        raise HTTPException(
            status_code=409,
            detail=f"Job is still processing. Current status: {job.status}",
        )

    try:
        matches = await find_matches_for_job(str(job.id))
        return matches
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# chroma run --path /chroma_db_path
