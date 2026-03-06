import fitz  # PyMuPDF
import docx
import io
import os
from typing import Optional

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from PDF bytes."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"PDF Extraction Error: {str(e)}")
        return ""

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts text from DOCX bytes."""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"DOCX Extraction Error: {str(e)}")
        return ""

def get_text_from_file(file_content: bytes, filename: str) -> Optional[str]:
    """Universal text extractor based on filename extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_content)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_content)
    elif ext == ".txt":
        return file_content.decode("utf-8", errors="ignore")
    else:
        return None
