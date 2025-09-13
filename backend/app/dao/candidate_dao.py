from beanie import PydanticObjectId
from typing import List, Dict, Any
from app.schemas.db_models import Candidate


class CandidateDAO:

    async def create_candidate(
        self, name: str, profile: Dict[str, Any], score: float, job_id: PydanticObjectId
    ) -> Candidate:
        candidate = Candidate(
            name=name,
            standardized_profile=profile,
            relevance_score=score,
            job_id=job_id,
        )
        await candidate.insert()
        return candidate

    async def get_candidates_by_job_id(
        self, job_id: PydanticObjectId
    ) -> List[Candidate]:
        return (
            await Candidate.find(Candidate.job_id == job_id)
            .sort(-Candidate.relevance_score)  # type: ignore
            .to_list()
        )


candidate_dao = CandidateDAO()
