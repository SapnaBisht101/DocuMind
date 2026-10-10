import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
from app.storage.vector_store import collection
from app.models.extraction import DocumentSummary

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.5-flash")

# Initialize client only if an API key is provided
client = genai.Client(api_key=API_KEY) if API_KEY else None

def extract_structured_data(document_id: str) -> dict:
    """Extracts structured JSON from a specific document using Gemini."""
    
    # 1. Retrieve ALL chunks for this document from ChromaDB
    results = collection.query(
        query_texts=[""], # Empty query to just filter by metadata
        where={"document_id": document_id},
        n_results=50 # Grab up to 50 chunks to form a comprehensive view
    )
    
    if not results["documents"] or len(results["documents"][0]) == 0:
        return {"error": f"No content found for document ID: {document_id}"}
        
    # 2. Reconstruct the document context
    chunks = results["documents"][0]
    full_text = "\n...\n".join(chunks)
    
    # We enforce a rough character limit to avoid blowing up the context window for huge documents MVP
    # In a production app, we would use Map-Reduce for massive documents.
    if len(full_text) > 100000:
        full_text = full_text[:100000] + "\n...[TRUNCATED]"

    system_instruction = "You are a data extraction assistant. Extract the required structured data from the provided document text."
    prompt = f"Document Text:\n{full_text}\n\nExtract the requested information."

    if client:
        try:
            # We configure Gemini to output JSON matching our Pydantic model
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1, # Low temperature for factual extraction
                response_mime_type="application/json",
                response_schema=DocumentSummary,
            )
            
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config
            )
            
            # The SDK returns a JSON string that conforms to the schema. We parse it back to a Python dictionary.
            parsed_json = json.loads(response.text)
            return parsed_json
            
        except Exception as e:
            return {"error": f"Extraction failed: {str(e)}"}
    else:
        # Mock response for testing without an API key
        return {
            "title": "Mock Document Title",
            "document_type": "Test Document",
            "executive_summary": "This is a mock summary because no API key was provided.",
            "key_topics": ["Testing", "DocuMind"],
            "entities": [{"name": "DocuMind AI", "type": "Software Platform"}],
            "action_items": []
        }