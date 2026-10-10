import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-2.5-flash")

# Initialize client only if an API key is provided
client = genai.Client(api_key=API_KEY) if API_KEY else None

def generate_rag_answer(query: str, contexts: list) -> dict:
    """Generates an answer grounded strictly in the provided contexts using Gemini."""
    if not contexts:
        return {
            "answer": "The available documents do not contain enough information to answer this question.",
            "sources": []
        }
        
    # Format context for the prompt
    context_text = ""
    for idx, ctx in enumerate(contexts):
        context_text += f"\n--- Source {idx+1} (File: {ctx['filename']}, Page: {ctx['page_number']}) ---\n{ctx['content']}\n"
        
    system_instruction = (
        "You are an expert document analyst. Answer the user's question using ONLY the provided context.\n"
        "If the answer is not contained in the context, clearly state that the available evidence is insufficient.\n"
        "When you state a fact, cite the source number in brackets like [Source 1]."
    )
    
    if client:
        try:
            # We use GenerateContentConfig to pass system instructions and temperature
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0 # Strict and deterministic
            )
            
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=f"Context:\n{context_text}\n\nQuestion: {query}",
                config=config
            )
            answer = response.text
        except Exception as e:
            answer = f"Error generating answer from Gemini: {str(e)}"
    else:
        # Mock mode if no API key is provided, allowing pipeline testing without paid calls
        answer = f"MOCK ANSWER: Based on the provided context, I can confirm the extraction was successful. [Source 1]"

    return {
        "answer": answer,
        "sources": contexts
    }