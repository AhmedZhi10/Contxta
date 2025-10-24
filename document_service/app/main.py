# in: app/main.py

from fastapi import FastAPI
from app.api.version_1 import documents, query
from app.database import create_db_and_tables # Import the function

# Create the main FastAPI app instance
app = FastAPI(title="Document Service")

@app.on_event("startup")
def on_startup():
    """
    Event handler that runs when the application starts.
    It creates the database tables.
    """
    print("Application startup: Creating database tables...")
    create_db_and_tables()
    print("Application startup: Database tables created.")

# Include the API routers
app.include_router(documents.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "ok"}