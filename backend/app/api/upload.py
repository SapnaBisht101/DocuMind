from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from typing import Dict, Any

from app.services.extractor import extract_pdf, extract_text
from app.services.chunker import chunk_document
# Added 'collection' import so we can delete documents
from app.storage.vector_store import index_chunks, collection 

router = APIRouter()
MAX_FILE_SIZE = 10 * 1024 * 1024 
ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "text/plain": "txt",
    "text/markdown": "md",
    "application/octet-stream": "md" 
}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    file_type = ALLOWED_MIME_TYPES[file.content_type]
    file_bytes = await file.read()
    
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large.")
        
    # 1. Extract
    try:
        if file_type == "pdf":
            extraction = extract_pdf(file_bytes)
        else:
            extraction = extract_text(file_bytes, file_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")

    # 2. Chunk
    chunks = chunk_document(extraction)

    # --- SAFETY CHECK ADDED HERE ---
    if not chunks or len(chunks) == 0:
        raise HTTPException(
            status_code=400, 
            detail="Could not extract any text from the document. Please ensure it contains readable text, not just scanned images."
        )

    # 3. Index in Vector DB
    document_id = str(uuid.uuid4()) # Generate a unique ID for this document
    indexed_count = index_chunks(document_id, file.filename, chunks)
    
    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "indexed",
        "total_pages": extraction.get("page_count", 0),
        "chunks_indexed": indexed_count
    }

# --- DELETE ENDPOINT ADDED HERE ---
@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Deletes all vector chunks associated with a document ID from ChromaDB."""
    try:
        # Check if the document exists by querying one chunk
        existing = collection.query(
            query_texts=[""],
            where={"document_id": document_id},
            n_results=1
        )
        
        if not existing["documents"] or len(existing["documents"][0]) == 0:
            raise HTTPException(status_code=404, detail="Document not found")

        # Delete all chunks matching the document_id
        collection.delete(where={"document_id": document_id})
        
        return {"status": "success", "message": f"Document {document_id} and all its chunks were deleted."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")