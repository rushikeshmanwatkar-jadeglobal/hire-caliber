import numpy as np

from collections import defaultdict
from beanie import PydanticObjectId

from app.db.chromadb import jobs_collection, candidates_collection
from app.db.models import Candidate
from app.schemas.api_schemas import MatchResult
from app.db_clients.chroma_client import chroma_db_client
from langchain_chroma import Chroma


class MatchingService:
    @staticmethod
    async def find_matches_for_job(job_id: str, top_n: int = 10) -> list:
        """Finds top N candidate matches for a given job ID. (Now async)"""
        try:
            job_embeddings_data = jobs_collection.get(
                where={"document_id": job_id}, include=["embeddings"]
            )
            job_embeddings = job_embeddings_data.get("embeddings")

            if job_embeddings is None or (
                isinstance(job_embeddings, (list, np.ndarray))
                and len(job_embeddings) == 0
            ):
                raise ValueError(
                    f"No embeddings found for job ID {job_id}. Has it been processed?"
                )
            results = candidates_collection.query(
                query_embeddings=job_embeddings,
                n_results=top_n * 5,
                where={"document_type": "resume"},
            )

            best_scores = {}
            for i in range(len(results["ids"][0])):
                candidate_id = results["metadatas"][0][i]["document_id"]  # type: ignore
                similarity = 1 - results["distances"][0][i]  # type: ignore

                if (
                    candidate_id not in best_scores
                    or similarity > best_scores[candidate_id]
                ):
                    best_scores[candidate_id] = similarity

            ranked_candidates = sorted(
                best_scores.items(), key=lambda item: item[1], reverse=True
            )

            final_matches = []
            for cid_str in ranked_candidates[:top_n]:
                candidate_data = await Candidate.get(PydanticObjectId(cid_str[0]))
                if candidate_data:
                    response_candidate = MatchResult(
                        **candidate_data.model_dump(by_alias=True)
                    )
                    response_candidate.relevance_score = cid_str[1]
                    final_matches.append(response_candidate)

            return final_matches
        except Exception as e:
            raise e
