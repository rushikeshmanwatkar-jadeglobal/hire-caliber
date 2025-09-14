# app/tasks/process.py
import base64
import asyncio
from beanie import PydanticObjectId

from app.core.celery_app import celery
from app.core.config import settings
from app.db.models import Candidate, Job, ProcessingStatus
from app.services.document_processor import DocumentProcessor

processor = DocumentProcessor()


async def _process_job(job_id_str: str, title: str, content: str):
    """The async logic for processing a job description."""
    job_id = PydanticObjectId(job_id_str)
    try:
        processor.process_and_embed_jobs(
            doc_id=job_id_str, text=content, doc_type="job"
        )
    except Exception as e:
        raise e
