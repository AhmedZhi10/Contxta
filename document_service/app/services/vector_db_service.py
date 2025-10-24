# in: app/services/vector_db_service.py

from typing import List, Dict, Any
import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")

def add_embeddings_to_collection(
    chunks: List[str],
    embeddings: List[List[float]],
    filename: str,
    # NEW: We now accept a list of metadata dictionaries
    metadatas: List[Dict[str, Any]] 
):
    """
    Adds text chunks, embeddings, and metadata to the ChromaDB collection.
    """
    if not chunks:
        return

    # Create simple IDs like before
    ids = [f"{filename}_{i}" for i in range(len(chunks))]

    # Add the data to the collection, now including metadata
    collection.add(
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas, # <-- Add metadata here
        ids=ids
    )

    print(f"Successfully added {len(chunks)} chunks for {filename} to ChromaDB.")

def query_collection(
    query_embedding: List[float], 
    document_id: str, # NEW: We now accept a document_id to filter by
    n_results: int = 5
) -> List[str]:
    """
    Queries the collection to find similar chunks,
    FILTERED by a specific document_id.
    """
    
    # NEW: This 'where' filter is the magic.
    # It tells ChromaDB to ONLY search in documents
    # where the 'document_id' metadata field matches.
    where_filter = {"document_id": document_id}
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter # <-- Apply the filter here
    )
    
    return results['documents'][0]