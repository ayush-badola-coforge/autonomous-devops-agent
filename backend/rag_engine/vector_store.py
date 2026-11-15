# All chroma Db operations. Vector Db storage.

import chromadb

from typing import List
from backend.fastapi_app.app.config import settings

class ChromaClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_data")
        self.collection = (self.client.get_or_create_collection(name=settings.COLLECTION_NAME))

    def add_document(self, document_id: str, text:str, embedding: List[float], metadata: dict) -> None:
        self.collection.add(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    def get_collection_count(self) -> int:
        return self.collection.count()

    def search(self, error_embedding: List[float], top_k: int) -> List[dict]:
        results = self.collection.query(query_embeddings=[error_embedding], n_results=top_k)

        formatted_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(documents, metadatas, distances):
            formatted_results.append({
                "text": doc,
                "metadata": meta,
                "distance": dist
            })
        return formatted_results