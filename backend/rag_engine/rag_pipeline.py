# Ingestion file for the RAG engine. Brings together parsing, chunking and embedding.

from backend.rag_engine.document_loader import ParseService
from backend.rag_engine.chunking import ChunkService
from backend.rag_engine.embeddings import EmbeddingService
from backend.rag_engine.vector_store import ChromaClient

class IngestionService:
    def __init__(self):
        self.parser = ParseService()
        self.chunker = ChunkService()
        self.embedder = EmbeddingService()
        self.chroma = ChromaClient()

    def ingest(self, data_dir: str) -> None:
        
        print("Starting ingestion process...")
        documents = self.parser.load_docs(data_dir)
        total_chunks=0
        for document in documents:
            print(f"Processing {document['file_name']}...")
            chunks = self.chunker.split_text(document["content"])
            for index, chunk in enumerate(chunks):
                embedding = (self.embedder.create_embedding(chunk))
                metadata = {
                    "source": document["file_name"],
                    "chunk_index": index,
                    "file_path": document["file_path"]
                }
                self.chroma.add_document(
                    document_id=f"{document['file_name']}_{index}",
                    text=chunk,
                    embedding=embedding,
                    metadata=metadata
                )
                # print(f"\nChunk {index + 1}")
                # print(f"Text: {chunk}")
                # print(f"Embedding dimensions: {len(embedding)}")
                # print(f"First 5 embedding values: {embedding[:5]}")
                # print(f"Metadata: {metadata}")
                total_chunks+=1
        print(
            f"Ingestion Complete."
            f"Stored {total_chunks} chunks."
            f"Collection Count: {self.chroma.get_collection_count()}"
        )

if __name__ == "__main__":
    ingestion = IngestionService()
    ingestion.ingest("data/documents")