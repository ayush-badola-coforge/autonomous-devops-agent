# Generates vector embedding for document chunks and user queries.

from langchain_core.embeddings import Embeddings
from typing import List, Optional
import requests
from dotenv import load_dotenv
import os
from backend.fastapi_app.app.config import settings

class EmbeddingService:
    dimensions: Optional[int]=746
    API_URL: str=settings.API_URL
    headers: dict = {"Content-Type": "application/json", "X-API-KEY": settings.API_KEY}
    def create_embedding(self, text:str) -> List[float]:
        return self.create_embeddings([text])
    

    def create_embeddings(self, texts:List[str]) -> List[float]:
        payload = {
            "texts": texts,
            "dimensions": self.dimensions
        }
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        # print(f"-------------------{response.status_code}-------------------")
        # print(f"-------------------{response.text}-------------------")
        response.raise_for_status()
        data = response.json()
        embeddings = data["embeddings"]
        print(f"Usage Tokens: {data.get('usage', {}).get('input_tokens', 'N/A')}")
        return embeddings