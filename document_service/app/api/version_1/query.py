
from fastapi import APIRouter, HTTPException, status, Depends, Path as FastAPIPath
from pydantic import BaseModel
from sqlmodel import Session, select

# Import security and database components
from app.database import get_session
from app.models.document import Document # <-- Import the Document model
from app.core.security import get_current_user, TokenPayload # <-- Import security
from app.celery_worker.tasks import create_embeddings
from app.services.vector_db_service import query_collection

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)

class QueryRequest(BaseModel):
    question: str

@router.post("/{document_id}")
def handle_query(
    request: QueryRequest,
    document_id: str = FastAPIPath(..., title="Document ID"),
    session: Session = Depends(get_session), # Get DB session
    # --- THIS LINE ADDS SECURITY ---
    token_payload: TokenPayload = Depends(get_current_user) # Require valid token
):
    """
    Receives a question for a specific document ID, verifies ownership,
    finds relevant chunks within that document, and returns them.
    """
    # --- CHECK OWNERSHIP ---
    user_id = token_payload.sub
    print(f"Query initiated by user_id: {user_id} for document_id: {document_id}")

    # Query the database to find the document AND check if it belongs to the user
    statement = select(Document).where(Document.id == document_id, Document.user_id == user_id)
    db_document = session.exec(statement).first()

    # If the document doesn't exist OR doesn't belong to the user, deny access
    if db_document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or you do not have permission to access it."
        )

    # --- Proceed with Query if Ownership is Verified ---
    try:
        question_embedding = create_embeddings([request.question], prefix="query: ")[0]

        relevant_chunks = query_collection(
            query_embedding=question_embedding,
            document_id=document_id # ChromaDB filter is still needed
        )

        context = "\n---\n".join(relevant_chunks)

        return {
            "detail": "Query successful.",
            "relevant_context": context
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the query: {e}"
        )