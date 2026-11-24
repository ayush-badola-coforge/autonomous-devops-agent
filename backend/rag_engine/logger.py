import json
from pathlib import Path
from datetime import datetime


class RAGLogger:

    LOG_FILE = Path("backend/logs/rag_logs.jsonl")

    @classmethod
    def log(cls, question: str, contexts: list[str], answer: str, sources: list[str], similarity_scores: list[float]):

        cls.LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "retrieved_contexts": contexts,
            "sources": sources,
            "similarity_scores": similarity_scores,
            "answer": answer
        }

        with open(
            cls.LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:
            file.write(
                json.dumps(log_entry) + "\n"
            )