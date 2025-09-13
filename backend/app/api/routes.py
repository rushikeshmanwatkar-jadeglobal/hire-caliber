from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import UUID
from app.services.ta_service import ta_service, TalentAcquisitionService
from app.schemas.api_schemas import JobResponse, CandidateResponse, JobCreate

router = APIRouter(prefix="/jobs")


@router.post("/", status_code=201)
async def create_job(job_data: JobCreate):
    """Creates a new job posting."""
    try:
        job = await ta_service.create_new_job(
            title=job_data.title, description=job_data.description
        )
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {e}")


@router.get("/", response_model=List[JobResponse])
async def list_jobs():
    """Lists all available jobs."""
    return await ta_service.get_all_jobs()


@router.post(
    "/{job_id}/resumes",
)
async def upload_resumes(job_id: str, resume_files: UploadFile = File(...)):
    """Uploads resumes for a specific job and processes them."""
    if not resume_files:
        raise HTTPException(status_code=400, detail="No resume files provided.")
    try:
        candidates = await ta_service.process_resumes_for_job(job_id, [resume_files])
        return candidates
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred during processing: {e}"
        )


@router.get("/{job_id}/candidates", response_model=List[CandidateResponse])
async def get_job_candidates(job_id: str):
    """Retrieves all processed candidates for a specific job, sorted by score."""
    try:
        return await ta_service.get_candidates_for_job(job_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve candidates: {e}"
        )
