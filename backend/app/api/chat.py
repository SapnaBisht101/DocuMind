from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.retriever import retrieve_context
from app.services.llm import generate_rag_answer

router = APIRouter()

# Define incoming request structure
class ChatRequest(BaseModel):
    query: str
    document_id: Optional[str] = None # Optional: Filter by specific document

# Define outgoing response structure
class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    # 1. Retrieve relevant chunks
    contexts = retrieve_context(request.query, n_results=3, document_id=request.document_id)
    
    # 2. Generate answer
    result = generate_rag_answer(request.query, contexts)
    
    return result