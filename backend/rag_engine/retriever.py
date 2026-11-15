# Embed user errors and queries, and retrieves relevant chunks from chroma Db via similarity search.

from backend.rag_engine.embeddings import EmbeddingService
from backend.rag_engine.vector_store import ChromaClient
from typing import List

class RetrieverService:
    def __init__(self):
        self.EmbeddingService = EmbeddingService()
        self.ChromaClient = ChromaClient()

    def retrieve_chunks(self, error: str, top_k:int = 5) -> List[dict]:
        error_embedding = self.EmbeddingService.create_embedding(error)
        results = self.ChromaClient.search(error_embedding=error_embedding, top_k=top_k)
        return results