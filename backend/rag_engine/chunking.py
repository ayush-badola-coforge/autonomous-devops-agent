# Breaks the document in chunks for the RAG engine.

from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkService:
    def __init__(self, chunk_size: int=800, chunk_overlap: int=150):
        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len
            )
        )
    def split_text(self, text:str) -> list:
        return self.splitter.split_text(text)