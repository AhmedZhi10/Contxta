# in: app/celery_worker/tasks.py

from pathlib import Path
from typing import List
import os
from .celery_app import celery
from sentence_transformers import SentenceTransformer, models
from sqlmodel import select

# Import components for database interaction inside the task
from app.database import get_task_session
from app.models.document import Document, DocumentStatus

# Import text processing functions
from app.services.document_proccesor import (
    extract_text_from_file,
    split_text_into_chunks,
)
from app.services.vector_db_service import add_embeddings_to_collection

# --- Model Loading Logic (as before) ---
embedding_model = None

def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        print(f"Worker (PID: {os.getpid()}) is loading E5 model...")
        MODEL_PATH = "local_models/intfloat-multilingual-e5-base"
        word_embedding_model = models.Transformer(MODEL_PATH)
        pooling_model = models.Pooling(word_embedding_dimension=word_embedding_model.get_word_embedding_dimension())
        embedding_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        print(f"Worker (PID: {os.getpid()}) model loaded successfully.")
    return embedding_model

def create_embeddings(chunks: List[str], prefix: str = "") -> List[List[float]]:
    model = get_embedding_model()
    if not chunks: return []
    prefixed_chunks = [f"{prefix}{chunk}" for chunk in chunks]
    embeddings = model.encode(prefixed_chunks).tolist()
    return embeddings

# --- Updated Celery Task ---
@celery.task(name="process_document_task")
def process_document_task(file_path_str: str, original_filename: str, document_id_str: str):
    """
    Celery task that processes a document and updates its status in the database.
    """
    print(f"Task started for document ID: {document_id_str}")
    
    # Use our special session manager for tasks
    with get_task_session() as session:
        try:
            # Find the document record in the database
            statement = select(Document).where(Document.id == document_id_str)
            document = session.exec(statement).one()
            
            # --- Perform the processing ---
            file_path = Path(file_path_str)
            raw_text = extract_text_from_file(file_path)
            chunks = split_text_into_chunks(raw_text)
            embeddings = create_embeddings(chunks, prefix="passage: ")
            
            chunk_metadatas = [{"document_id": document_id_str}] * len(chunks)
            
            add_embeddings_to_collection(
                chunks=chunks,
                embeddings=embeddings,
                filename=original_filename,
                metadatas=chunk_metadatas # <-- Pass the new metadata
            )
            # --- Update status to COMPLETED ---
            document.status = DocumentStatus.COMPLETED
            session.add(document)
            session.commit()
            
            print(f"Successfully processed document ID: {document_id_str}")
            return {"status": "Success", "chunks_stored": len(chunks)}
        
        except Exception as e:
            # In case of any error, update status to FAILED
            print(f"Error processing document ID {document_id_str}: {e}")
            statement = select(Document).where(Document.id == document_id_str)
            document = session.exec(statement).one_or_none()
            if document:
                document.status = DocumentStatus.FAILED
                session.add(document)
                session.commit()
            # Re-raise the exception to mark the task as 'FAILED' in Celery logs
            raise e