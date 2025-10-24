# in: app/services/document_processor.py
from pathlib import Path
from typing import List
import docx
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer,models



def _docx_to_text(file_path: Path) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text])

def _pdf_to_text(file_path: Path) -> str:
    reader = PdfReader(file_path)
    full_text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text.append(page_text)
    return "\n".join(full_text)

def extract_text_from_file(file_path: Path) -> str:
    """Validates and extracts text from a file."""
    allowed = {".pdf": _pdf_to_text, ".docx": _docx_to_text, ".txt": Path.read_text}
    if file_path.suffix not in allowed:
        raise ValueError(f"File type {file_path.suffix} is not supported.")
    
    try:
        if file_path.suffix == ".txt":
            return allowed[file_path.suffix](file_path, encoding="utf-8")
        return allowed[file_path.suffix](file_path)
    except Exception as e:
        raise IOError(f"Error processing file {file_path.name}: {e}")

def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
    """Splits a long text into smaller, overlapping chunks."""
    if not text:
        return []
    
    chunks = []
    start_index = 0
    while start_index < len(text):
        end_index = start_index + chunk_size
        chunks.append(text[start_index:end_index])
        start_index += chunk_size - chunk_overlap
    return chunks

