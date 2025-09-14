from typing import List, Tuple, TypeVar, Union
from langchain_text_splitters import RecursiveCharacterTextSplitter
from io import BytesIO

from torch import chunk
from unstructured.partition.auto import partition
from app.db.chromadb import candidates_collection, jobs_collection
from app.llm.azure_openai_provider import AzureOpenAIProvider


class DocumentProcessor:
    """
    A class to parse documents into chunks and generate embeddings
    strictly using the Azure OpenAI service.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initializes the DocumentProcessor.

        Args:
            chunk_size: The character size for each text chunk.
            chunk_overlap: The character overlap between consecutive chunks.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        self.embedding_client = AzureOpenAIProvider(type="embedding")

        print("DocumentProcessor initialized to use Azure OpenAI embeddings.")

    def parse_document(self, file_bytes: bytes, filename: str) -> str:
        """Parses document bytes into clean text using unstructured."""
        try:
            if isinstance(file_bytes, bytes):
                file_stream = BytesIO(file_bytes)
            else:
                file_stream = file_bytes
            elements = partition(file=file_stream, file_filename=filename)
            return "\n\n".join([str(el) for el in elements])
        except Exception as e:
            raise

    def process_and_embed(self, doc_id: str, text: str, doc_type: str):
        try:
            chunks = self.text_splitter.split_text(text)

            if not chunks:
                print("No chunks were generated from the document.")
                return [], []

            response = self.embedding_client.embeddings(input=chunks)
            embeddings = [item.embedding for item in response.data]
            print(f"Successfully generated {len(embeddings)} embeddings.")
            if embeddings:
                metadata_list = [
                    {"document_id": doc_id, "document_type": doc_type, "chunk_num": i}
                    for i in range(len(chunks))
                ]
                chunk_ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

                # Add to ChromaDB
                candidates_collection.add(
                    ids=chunk_ids,
                    embeddings=embeddings,
                    metadatas=metadata_list,
                    documents=chunks,
                )

            return chunks, embeddings
        except Exception as e:
            raise e

    def process_and_embed_jobs(self, doc_id: str, text: str, doc_type: str):
        try:
            chunks = self.text_splitter.split_text(text)

            if not chunks:
                print("No chunks were generated from the document.")
                return [], []

            response = self.embedding_client.embeddings(input=chunks)
            embeddings = [item.embedding for item in response.data]
            print(f"Successfully generated {len(embeddings)} embeddings.")
            if embeddings:
                metadata_list = [
                    {"document_id": doc_id, "document_type": doc_type, "chunk_num": i}
                    for i in range(len(chunks))
                ]
                chunk_ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

                # Add to ChromaDB
                jobs_collection.add(
                    ids=chunk_ids,
                    embeddings=embeddings,
                    metadatas=metadata_list,
                    documents=chunks,
                )

            return chunks, embeddings
        except Exception as e:
            raise e
