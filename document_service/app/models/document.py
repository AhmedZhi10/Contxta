# in: app/models/document.py

from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
import uuid

class DocumentStatus(str, Enum):
    """
    Enum to define the possible statuses of a document.
    """
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Document(SQLModel, table=True):
    """
    Represents the Document table in the PostgreSQL database.
    Stores metadata about the uploaded files.
    """
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    
    original_filename: str
    
    saved_filename: str = Field(index=True)
    
    task_id: str = Field(index=True, unique=True)
    
    status: DocumentStatus = Field(
        default=DocumentStatus.PENDING, index=True
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    
    # --- THIS IS THE NEW LINE ---
    # We will store the user's ID as a string for simplicity,
    # as it will come from the JWT token.
    user_id: str = Field(index=True)