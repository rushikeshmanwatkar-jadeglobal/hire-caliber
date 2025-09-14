import numpy as np

from collections import defaultdict
from beanie import PydanticObjectId

from app.db.chromadb import jobs_collection, candidates_collection
from app.db.models import Candidate


async def find_matches_for_job(job_id: str, top_n: int = 10) -> list:
    """Finds top N candidate matches for a given job ID. (Now async)"""
    try:
        job_embeddings_data = jobs_collection.get(
            where={"document_id": job_id}, include=["embeddings"]
        )
        job_embeddings = job_embeddings_data.get("embeddings")

        if job_embeddings is None or (
            isinstance(job_embeddings, (list, np.ndarray)) and len(job_embeddings) == 0
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
            candidate_id = results["metadatas"][0][i]["document_id"]
            similarity = 1 - results["distances"][0][i]
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
            candidate_data = await Candidate.get(PydanticObjectId(cid_str))
            if candidate_data:
                final_matches.append(
                    {
                        "candidate_id": str(candidate_data.id),
                        "name": candidate_data.name,
                    }
                )

        return final_matches
    except Exception as e:
        raise e
