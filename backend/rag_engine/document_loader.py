# File to load and parse documents for the RAG engine

from pathlib import Path
from typing import List, Dict
import pymupdf

class ParseService:
    SUPPORTED_EXT = [".pdf", ".txt", ".md", ".docx"]
    def load_docs(self, data_dir:str) -> List[Dict]:
        documents=[]
        data_path=Path(data_dir)

        for file_path in data_path.rglob("*"):
            if(file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXT):
                content = self.extract_text(file_path)
                documents.append(
                    {
                        "file_name": file_path.name,
                        "file_path": str(file_path),
                        "content": content
                    }
                )
        return documents


    def extract_text(self, file_path:Path) -> str:
        extension = file_path.suffix.lower()

        if(extension == ".pdf"):
            return self._extract_pdf(file_path)
        if(extension == ".docx"):
            return self._extract_docx(file_path)
        if(extension in [".txt", ".md"]):
            return self._extract_text_file(file_path)

        raise ValueError(f"Unsupported file extension: {extension}")

    def _extract_text_file(self, file_path:Path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _extract_pdf(self, file_path:Path) -> str:
        text = ""

        pdf_document = pymupdf.open(file_path)

        for page in pdf_document:
            text += page.get_text()

        return text