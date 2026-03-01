import os
from pathlib import Path
from typing import Optional, List
from config import config


class DocumentProcessor:
    
    SUPPORTED_FORMATS = config.SUPPORTED_FORMATS
    
    @staticmethod
    def process_file(file_path: str) -> Optional[str]:
        try:
            file_ext = Path(file_path).suffix.lower().strip(".")
            
            if file_ext not in DocumentProcessor.SUPPORTED_FORMATS:
                return None
            
            if file_ext == "txt":
                return DocumentProcessor._read_txt(file_path)
            elif file_ext == "pdf":
                return DocumentProcessor._read_pdf(file_path)
            elif file_ext == "docx":
                return DocumentProcessor._read_docx(file_path)
            elif file_ext == "md":
                return DocumentProcessor._read_txt(file_path)
            
            return None
            
        except Exception as e:
            print(f"Error processing file: {e}")
            return None
    
    @staticmethod
    def _read_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    @staticmethod
    def _read_pdf(file_path: str) -> Optional[str]:
        try:
            from PyPDF2 import PdfReader
            text = []
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    @staticmethod
    def _read_docx(file_path: str) -> Optional[str]:
        try:
            from docx import Document
            doc = Document(file_path)
            text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text)
            return "\n".join(text)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    
    @staticmethod
    def validate_file(file_path: str, file_size: int) -> tuple[bool, str]:
        if file_size > config.MAX_UPLOAD_SIZE_BYTES:
            return False, f"File too large. Max size: {config.MAX_UPLOAD_SIZE_MB}MB"
        
        file_ext = Path(file_path).suffix.lower().strip(".")
        if file_ext not in DocumentProcessor.SUPPORTED_FORMATS:
            return False, f"Unsupported format. Supported: {', '.join(DocumentProcessor.SUPPORTED_FORMATS)}"
        
        return True, "File is valid"
