
from app.storage.vector_store import collection
from typing import List, Dict, Any

def retrieve_context(query: str, n_results: int = 4, document_id: str = None) -> List[Dict[str, Any]]:
    """Retrieves the most relevant chunks from ChromaDB."""
    # Filter by document_id if provided
    where_clause = {"document_id": document_id} if document_id else None
    
    # ChromaDB automatically generates the embedding for the query string using the same model
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_clause
    )
    
    contexts = []
    # collection.query returns a list of lists (one for each query text)
    if results["documents"] and len(results["documents"]) > 0:
        docs = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        for i in range(len(docs)):
            contexts.append({
                "content": docs[i],
                "page_number": metadatas[i].get("page_number", "Unknown"),
                "filename": metadatas[i].get("filename", "Unknown")
            })
            
    return contexts