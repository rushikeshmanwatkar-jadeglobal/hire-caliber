# app/api/candidates.py
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
from beanie import PydanticObjectId

from app.db.models import Candidate, ProcessingStatus
from app.schemas.api_schemas import CandidateResponse, DocumentStatusResponse
from app.tasks.process import _process_resume

router = APIRouter(
    prefix="/candidates",  # All routes in this file will start with /candidates
    tags=["Candidates"],  # Group these endpoints in the API docs
)


@router.post("/upload", response_model=CandidateResponse, status_code=202)
async def upload_resume(file: UploadFile = File(...)):
    try:
        """Upload a resume, create a candidate record, and start background processing."""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file name found.")

        contents = await file.read()

        candidate = Candidate(filename=file.filename)
        await candidate.create()

        contents_b64 = base64.b64encode(contents).decode("utf-8")
        await _process_resume(str(candidate.id), contents_b64, file.filename)
        return CandidateResponse(**candidate.model_dump(by_alias=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
