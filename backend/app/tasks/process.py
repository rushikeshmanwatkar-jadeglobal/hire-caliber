# app/tasks/process.py
import base64
import asyncio
from beanie import PydanticObjectId

from app.core.celery_app import celery
from app.core.config import settings
from app.db.models import Candidate, Job, ProcessingStatus
from app.services.document_processor import DocumentProcessor

processor = DocumentProcessor()


async def _process_resume(candidate_id_str: str, file_contents_b64: str, filename: str):
    """The async logic for processing a resume."""
    candidate_id = PydanticObjectId(candidate_id_str)
    try:
        await Candidate.find_one(Candidate.id == candidate_id).update(
            {"$set": {"status": ProcessingStatus.PROCESSING}}
        )

        file_bytes = base64.b64decode(file_contents_b64)
        full_text = processor.parse_document(file_bytes, filename)

        result = processor.process_and_embed(
            doc_id=candidate_id_str, text=full_text, doc_type="resume"
        )

        await Candidate.find_one(Candidate.id == candidate_id).update(
            {"$set": {"full_text": full_text, "status": ProcessingStatus.COMPLETED}}
        )
    except Exception as e:
        error_message = f"Failed to process resume: {e}"
        await Candidate.find_one(Candidate.id == candidate_id).update(
            {"$set": {"status": ProcessingStatus.ERROR, "error_message": error_message}}
        )


async def _process_job(job_id_str: str, title: str, content: str):
    """The async logic for processing a job description."""
    job_id = PydanticObjectId(job_id_str)
    try:
        await Job.find_one(Job.id == job_id).update(
            {"$set": {"status": ProcessingStatus.PROCESSING}}
        )

        processor.process_and_embed_jobs(
            doc_id=job_id_str, text=content, doc_type="job"
        )

        await Job.find_one(Job.id == job_id).update(
            {"$set": {"status": ProcessingStatus.COMPLETED}}
        )
    except Exception as e:
        error_message = f"Failed to process job description: {e}"
        await Job.find_one(Job.id == job_id).update(
            {"$set": {"status": ProcessingStatus.ERROR, "error_message": error_message}}
        )
