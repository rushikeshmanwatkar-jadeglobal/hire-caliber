from beanie import PydanticObjectId
from typing import List, Dict, Any, Optional
from app.db.models import Candidate


class CandidateDAO:

    @staticmethod
    async def get_candidate(
        id: Optional[PydanticObjectId] = None, where: Optional[Dict[str, Any]] = None
    ):
        try:
            if id is not None:
                candidate = Candidate.get(id)
            candidate = Candidate.find_one(where)
            if not candidate:
                raise ValueError("Could not find any candidate")
            return candidate
        except Exception as e:
            raise e

    @staticmethod
    async def create_candidate(
        name: str,
        profile: Dict[str, Any],
        score: Optional[float] = None,
        job_id: Optional[PydanticObjectId] = None,
        full_text: Optional[str] = None,
    ) -> Candidate:
        try:
            candidate = Candidate(
                name=name,
                standardized_profile=profile,
                relevance_score=score,
                job_id=job_id,
                full_text=full_text,
            )
            await candidate.insert()
            return candidate
        except Exception as e:
            raise e

    async def get_candidates_by_job_id(
        self, job_id: PydanticObjectId
    ) -> List[Candidate]:
        return (
            await Candidate.find(Candidate.job_id == job_id)
            .sort(-Candidate.relevance_score)  # type: ignore
            .to_list()
        )
