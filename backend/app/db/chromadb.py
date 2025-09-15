# app/db/chromadb.py
import chromadb
from app.core.config import settings

client = chromadb.HttpClient(
    host=settings.CHROMA_HTTP_HOST, port=settings.CHROMA_HTTP_PORT
)

# This collection will store embeddings for both resumes and job descriptions
# The metadata will distinguish between them
candidates_collection = client.get_or_create_collection(name="candidates_collection")
jobs_collection = client.get_or_create_collection(name="jobs_collection")
