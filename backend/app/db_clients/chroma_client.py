import chromadb
from typing import List, Optional

from app.config import settings


class ChromaDBClient:
    def __init__(self):
        # Using an in-memory instance for simplicity.
        # For production, use chromadb.PersistentClient(path="/path/to/db")
        # self.client = chromadb.Client(settings={"chroma_server_host": })
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HTTP_HOST,  # type: ignore
            port=settings.CHROMA_HTTP_PORT,  # type: ignore
        )
        self.candidates_collection = self.client.get_or_create_collection(
            name="candidates_collection"
        )
        self.jobs_collection = self.client.get_or_create_collection(
            name="jobs_collection"
        )

    def add_embedding(
        self, collection_name: str, doc_id: str, embedding: List[float], metadata: dict
    ):
        try:
            collection = self.client.get_collection(name=collection_name)
            collection.add(ids=[doc_id], embeddings=[embedding], metadatas=[metadata])
        except Exception as e:
            print("Error while adding embeddings", e)
            raise e

    def query_by_embedding(
        self,
        collection_name: str,
        query_embedding: List[float],
        top_k: int,
        filter_metadata: Optional[dict] = None,
    ) -> List[str]:
        collection = self.client.get_collection(name=collection_name)
        results = collection.query(
            query_embeddings=[query_embedding], n_results=top_k, where=filter_metadata
        )
        return results["ids"][0] if results and results["ids"] else []


# Singleton instance to be used across the application
chroma_db_client = ChromaDBClient()
