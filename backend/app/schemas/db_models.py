from beanie import Document
from pydantic import Field
from typing import Optional, Dict, Any
from beanie import PydanticObjectId


class Job(Document):
    title: str
    description: str

    class Settings:
        name = "jobs"


class Candidate(Document):
    name: str
    job_id: PydanticObjectId
    relevance_score: Optional[float] = None
    standardized_profile: Dict[str, Any]

    class Settings:
        name = "candidates"
