# Coordinates the complete RAG question-answering workflow.

from backend.rag_engine.embeddings import EmbeddingService
from backend.rag_engine.vector_store import ChromaClient
from backend.rag_engine.retriever import RetrieverService
from backend.rag_engine.prompt_builder import PromptBuilderService
from backend.rag_engine.llm import LLMService

class RAGService:
    def __init__(self):
        self.retriever = RetrieverService()
        self.prompt_builder = PromptBuilderService()
        self.llm = LLMService()

    def answer(self, error: str) -> str:
        chunks = self.retriever.retrieve_chunks(error, 5)
        prompt = self.prompt_builder.build(error, chunks)
        answer = self.llm.generate_answer(prompt)
        return answer

rag_service = RAGService()