from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from app.services.storyboard_llm import generate_storyboard_data

router = APIRouter()

class StoryboardRequest(BaseModel):
    document_id: str
    mode: Optional[str] = "software"  # software, business, research, presentation

@router.post("/generate")
async def generate_storyboard(request: StoryboardRequest) -> Dict[str, Any]:
    """Generates an actionable storyboard or workflow plan for a document."""
    if request.mode not in ["software", "business", "research", "presentation"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid mode. Allowed modes: 'software', 'business', 'research', 'presentation'."
        )
        
    result = generate_storyboard_data(request.document_id, mode=request.mode)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result