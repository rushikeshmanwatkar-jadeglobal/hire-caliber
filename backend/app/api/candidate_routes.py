# app/api/candidates.py
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.api_schemas import CandidateResponse
from app.services.ta_service import TalentAcquisitionService

router = APIRouter(
    prefix="/candidates",  # All routes in this file will start with /candidates
    tags=["Candidates"],  # Group these endpoints in the API docs
)


@router.post("/upload", status_code=201)
async def upload_resume(files: List[UploadFile] | UploadFile = File(...)):
    try:
        """Upload a resume, create a candidate record, and start background processing."""
        files = files if isinstance(files, list) else [files]

        new_candidates = await TalentAcquisitionService.process_resumes_for_job(
            resume_files=files
        )
        response = []
        if len(new_candidates) == 0:
            raise RuntimeError("No candidates were added!")

        if len(new_candidates) > 1:
            for candidate in new_candidates:
                r = CandidateResponse(**candidate.model_dump(by_alias=True))
                response.append(r)
        else:
            r = CandidateResponse(**new_candidates[0].model_dump(by_alias=True))
            response.append(r)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
