from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from app.services.extractor_llm import extract_structured_data

router = APIRouter()

@router.post("/{document_id}/extract")
async def extract_document(document_id: str) -> Dict[str, Any]:
    """
    Analyzes a document's indexed chunks and extracts structured metadata.
    """
    result = extract_structured_data(document_id)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result