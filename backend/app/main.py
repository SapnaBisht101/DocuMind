from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload

from app.api import upload, chat, extractor, storyboards


app = FastAPI(
    title="DocuMind AI",
    description="Intelligent Document Analysis and RAG API",
    version="0.1.0"
)

# Configure CORS for local development (React defaults to 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We will include the upload router here shortly
app.include_router(upload.router, prefix="/api/documents", tags=["documents"])



app.include_router(extractor.router, prefix="/api/documents", tags=["extraction"]) 
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(storyboards.router, prefix="/api/storyboards", tags=["storyboards"])  # ADDED
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "DocuMind API is running"}