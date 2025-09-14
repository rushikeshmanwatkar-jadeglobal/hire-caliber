from beanie import PydanticObjectId
from typing import List
from fastapi import UploadFile
from app.dao.candidate_dao import candidate_dao
from app.dao.job_dao import job_dao
from app.db_clients.chroma_client import chroma_db_client
from app.utils import ai_utils, file_utils
from app.schemas.models import Candidate, Job


class TalentAcquisitionService:
    async def create_new_job(self, title: str, description: str) -> Job:
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

    async def process_resumes_for_job(
        self, job_id: str, resume_files: List[UploadFile]
    ) -> List[Candidate]:
        try:
            job = await job_dao.get_job_by_id(PydanticObjectId(job_id))
            if not job:
                raise ValueError(f"Job with ID {job_id} not found.")

            job_embedding = await ai_utils.get_embedding(job.description)
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
                candidate_embedding = await ai_utils.get_embedding(
                    summary_for_embedding
                )

                score = ai_utils.calculate_cosine_similarity(
                    job_embedding, candidate_embedding
                )

                new_candidate = await candidate_dao.create_candidate(
                    name=standardized_profile.get("personal_info", {}).get(
                        "name", "Unknown Candidate"
                    ),
                    profile=standardized_profile,
                    score=round(score * 100, 2),  # Store as a percentage
                    job_id=PydanticObjectId(job.id),
                )

                chroma_db_client.add_embedding(
                    collection_name="candidates_collection",
                    doc_id=str(new_candidate.id),
                    embedding=candidate_embedding,
                    metadata={"job_id": str(job.id)},
                )
                processed_candidates.append(new_candidate)

            return processed_candidates
        except Exception as e:
            raise e

    async def get_candidates_for_job(self, job_id: str) -> List[Candidate]:
        return await candidate_dao.get_candidates_by_job_id(PydanticObjectId(job_id))

    async def get_all_jobs(self) -> List[Job]:
        return await Job.find_all().to_list()


ta_service = TalentAcquisitionService()
