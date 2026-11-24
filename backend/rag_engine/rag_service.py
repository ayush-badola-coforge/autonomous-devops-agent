# Coordinates the complete RAG question-answering workflow.

from backend.rag_engine.embeddings import EmbeddingService
from backend.rag_engine.vector_store import ChromaClient
from backend.rag_engine.retriever import RetrieverService
from backend.rag_engine.prompt_builder import PromptBuilderService
from backend.rag_engine.llm import LLMService
from backend.rag_engine.logger import RAGLogger

class RAGService:
    def __init__(self):
        self.retriever = RetrieverService()
        self.prompt_builder = PromptBuilderService()
        self.llm = LLMService()

    def answer(self, error: str) -> str:
        chunks = self.retriever.retrieve_chunks(error, 2)
        contexts = [chunk["text"] for chunk in chunks]
        sources = [chunk["metadata"].get("source") for chunk in chunks]
        distances = [chunk["distance"] for chunk in chunks]
        context = "\n\n".join(contexts)
        prompt = self.prompt_builder.build(error, chunks)
        print("\nRetrieved Chunk Count:", len(chunks))

        for idx, chunk in enumerate(chunks):
            print(
                f"Chunk {idx + 1}: "
                f"{len(chunk['text'])} chars"
            )

        print(
            f"Total Context Length: "
            f"{len(context)}"
        )

        answer = self.llm.generate_answer(prompt)
        RAGLogger.log(
            question=error,
            contexts=contexts,
            answer=answer,
            sources=sources,
            similarity_scores=distances
        )
        return answer

    def answer_with_context(self, error: str) -> str:
        chunks = self.retriever.retrieve_chunks(error, 2)
        contexts = [chunk["text"] for chunk in chunks]
        sources = [chunk["metadata"].get("source") for chunk in chunks]
        distances = [chunk["distance"] for chunk in chunks]
        context = "\n\n".join(contexts)
        prompt = self.prompt_builder.build(error, chunks)
        answer = self.llm.generate_answer(prompt)
        return {
        "answer": answer,
        "contexts": contexts,
        "sources": sources,
        "distances": distances
    }

rag_service = RAGService()