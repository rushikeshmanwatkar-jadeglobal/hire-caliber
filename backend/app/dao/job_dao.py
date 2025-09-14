from beanie import PydanticObjectId
from typing import Optional
from app.schemas.models import Job


class JobDAO:
    async def create_job(self, title: str, description: str) -> Job:
        job = Job(title=title, description=description)
        await job.insert()
        return job

    async def get_job_by_id(self, job_id: PydanticObjectId) -> Optional[Job]:
        return await Job.get(job_id)


job_dao = JobDAO()
