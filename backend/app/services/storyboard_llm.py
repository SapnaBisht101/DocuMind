import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from app.storage.vector_store import collection
from app.models.storyboard import Storyboard

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None

MODE_INSTRUCTIONS = {
    "software": "Focus on screen-by-screen user journeys, backend API responsibilities, database requirements, and acceptance criteria.",
    "business": "Focus on business process steps, decision gateways, operational triggers, actor roles, and risk controls.",
    "research": "Focus on research phases, hypothesis testing steps, methodology execution, required resources, and evaluation criteria.",
    "presentation": "Focus on slide-by-slide layout, main message per slide, supporting evidence from document, and speaker notes."
}

def generate_storyboard_data(document_id: str, mode: str = "software") -> dict:
    """Generates a structured storyboard plan from document content using Gemini."""
    
    # 1. Fetch chunks for the document from ChromaDB
    results = collection.query(
        query_texts=[""],
        where={"document_id": document_id},
        n_results=50
    )
    
    if not results["documents"] or len(results["documents"][0]) == 0:
        return {"error": f"No content found for document ID: {document_id}"}
        
    chunks = results["documents"][0]
    full_text = "\n...\n".join(chunks)
    
    if len(full_text) > 100000:
        full_text = full_text[:100000] + "\n...[TRUNCATED]"

    mode_prompt = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["software"])
    
    system_instruction = (
        "You are an expert system architect and project strategist.\n"
        "Transform the provided document into a structured, step-by-step storyboard or implementation workflow.\n"
        f"Mode context: {mode_prompt}\n\n"
        "STRICT CRITERIA:\n"
        "1. Clearly distinguish explicit facts from reasonable AI recommendations.\n"
        "2. Set `is_explicit_requirement` to True ONLY if directly supported by the text.\n"
        "3. List any extra AI ideas in the `ai_recommendations` field."
    )

    prompt = f"Selected Mode: {mode}\n\nDocument Text:\n{full_text}\n\nGenerate the complete structured storyboard."

    if client:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=Storyboard,
            )
            
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            return {"error": f"Storyboard generation failed: {str(e)}"}
    else:
        # Mock fallback for keyless local testing
        return {
            "title": f"Mock {mode.title()} Storyboard",
            "mode": mode,
            "project_overview": "Mock project plan based on test document.",
            "target_audience_or_users": ["Developers", "End Users"],
            "steps": [
                {
                    "step_number": 1,
                    "title": "Document Analysis & Ingestion",
                    "purpose": "Parse and store document content for processing.",
                    "actor_or_role": "DocuMind Backend",
                    "inputs": ["Raw File (PDF/TXT/MD)"],
                    "processing_logic": "Extract text, generate embeddings, and index into ChromaDB.",
                    "expected_output": "Indexed document vector chunks.",
                    "is_explicit_requirement": True,
                    "supporting_source_refs": ["Page 1"]
                }
            ],
            "dependencies": ["FastAPI", "ChromaDB", "Gemini API"],
            "ai_recommendations": ["Add Redis caching for faster repeated queries."]
        }