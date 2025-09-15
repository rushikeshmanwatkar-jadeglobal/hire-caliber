from beanie import PydanticObjectId
from typing import Optional
from app.db.models import Job


class JobDAO:

    @staticmethod
    async def create_job(title: str, description: str) -> Job:
        job = Job(title=title, description=description)
        await job.insert()
        return job

    @staticmethod
    async def get_job_by_id(job_id: PydanticObjectId) -> Optional[Job]:
        try:
            return await Job.get(job_id)
        except Exception as e:
            raise e

    @staticmethod
    async def get_all_jobs():
        try:
            return await Job.find_all().to_list()
        except Exception as e:
            raise e
