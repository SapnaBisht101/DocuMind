import chromadb
import os
from typing import List, Dict, Any

# Create a local directory for ChromaDB inside the backend folder
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")

# Initialize the persistent client
chroma_client = chromadb.PersistentClient(path=DB_DIR)

# Get or create our main collection (a collection is like a table in a relational DB)
collection = chroma_client.get_or_create_collection(name="documind_collection")

def index_chunks(document_id: str, filename: str, chunks: List[Dict[str, Any]]) -> int:
    """Embeds and stores document chunks in ChromaDB."""
    ids = []
    documents = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        # Create a unique ID for every single chunk
        chunk_id = f"{document_id}_chunk_{i}"
        
        ids.append(chunk_id)
        documents.append(chunk["content"])
        
        # Merge document-level info with chunk-level metadata
        meta = chunk["metadata"]
        meta["document_id"] = document_id
        meta["filename"] = filename
        metadatas.append(meta)
        
    # Add to ChromaDB. 
    # Because we didn't specify an embedding function, Chroma automatically 
    # uses its default local model (all-MiniLM-L6-v2) to embed the 'documents'.
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    return len(ids)