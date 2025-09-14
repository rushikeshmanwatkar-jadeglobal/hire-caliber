import base64
from beanie import PydanticObjectId
from typing import List, Optional
from fastapi import UploadFile
from app.dao.candidate_dao import CandidateDAO
from app.dao.job_dao import job_dao
from app.db_clients.chroma_client import chroma_db_client
from app.utils import ai_utils, file_utils
from app.schemas.models import Candidate, Job
from app.services.document_processor import DocumentProcessor

processor = DocumentProcessor()


class TalentAcquisitionService:

    @staticmethod
    async def create_new_job(title: str, description: str) -> Job:
        try:
            new_job = await job_dao.create_job(title=title, description=description)

            # Generate and store embedding for the job description
            job_embedding = await ai_utils.get_embedding(description)
            chroma_db_client.add_embedding(
                collection_name="jobs_collection",
                doc_id=str(new_job.id),
                embedding=job_embedding,
                metadata={"title": new_job.title, "job_id": str(new_job.id)},
            )
            return new_job
        except Exception as e:
            print("error while creating new job", e)
            raise e

    @staticmethod
    async def process_resumes_for_job(
        resume_files: List[UploadFile], job_id: Optional[str] = None
    ) -> List[Candidate]:
        try:
            processed_candidates = []
            for resume_file in resume_files:
                file_content = await resume_file.read()
                raw_text = file_utils.extract_text_from_pdf(file_content)  # type: ignore
                standardized_profile = await ai_utils.standardize_resume(raw_text)
                if "error" in standardized_profile:
                    continue  # Skip resumes that fail to parse

                summary_for_embedding = ai_utils.create_summary_from_profile(
                    standardized_profile
                )

                new_candidate = await CandidateDAO.create_candidate(
                    name=standardized_profile.get("personal_info", {}).get(
                        "name", "Unknown Candidate"
                    ),
                    profile=standardized_profile,
                )

                candidate_embedding = processor.process_and_embed(
                    doc_id=str(new_candidate.id),
                    text=summary_for_embedding,
                    doc_type="resume",
                )

                # if job_id is not None:
                #     job_pydantic_id = PydanticObjectId(job_id)
                #     job = await job_dao.get_job_by_id(job_pydantic_id)
                #     if not job:
                #         raise ValueError(f"Job with ID {job_id} not found.")

                #     job_embedding = await ai_utils.get_embedding(job.description)
                #     score = ai_utils.calculate_cosine_similarity(
                #         job_embedding, candidate_embedding
                #     )
                #     rounded_score = round(score * 100, 2)
                # chroma_db_client.add_embedding(
                #     collection_name="candidates_collection",
                #     doc_id=str(new_candidate.id),
                #     embedding=candidate_embedding,
                #     metadata={"job_id": str(job.id)},
                # )
                processed_candidates.append(new_candidate)

            return processed_candidates
        except Exception as e:
            raise e
