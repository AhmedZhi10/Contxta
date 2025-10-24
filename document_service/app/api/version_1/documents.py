# in: app/api/v1/documents.py

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session

# Import security and database components
from app.database import get_session
from app.models.document import Document
from app.core.security import get_current_user, TokenPayload # <-- Import security
from app.celery_worker.tasks import process_document_task

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    # --- THIS LINE ADDS SECURITY ---
    token_payload: TokenPayload = Depends(get_current_user) # Require valid token
):
    """
    Accepts a file for an authenticated user, creates a database record
    linking the file to the user, and queues it for background processing.
    """
    unique_filename = f"{uuid.uuid4()}{Path(file.filename).suffix}"
    file_path = UPLOADS_DIR / unique_filename

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception:
        raise HTTPException(status_code=500, detail="Could not save file.")

    # --- SAVE USER ID ---
    # Extract user_id from the verified token payload
    user_id = token_payload.sub
    print(f"Upload initiated by user_id: {user_id}") # For debugging

    # Create the Document record, now including the user_id
    db_document = Document(
        original_filename=file.filename,
        saved_filename=unique_filename,
        user_id=user_id, # <-- Link the document to the user
        task_id=""
    )
    session.add(db_document)
    session.commit()
    session.refresh(db_document)

    # Send job to Celery (pass document ID and user ID if needed later)
    task = process_document_task.delay(str(file_path), file.filename, str(db_document.id))

    # Update the record with the task ID
    db_document.task_id = task.id
    session.add(db_document)
    session.commit()

    return {
        "detail": "File accepted and is being processed.",
        "document_id": db_document.id,
        "task_id": task.id
    }