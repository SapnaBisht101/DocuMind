import fitz  # PyMuPDF
from typing import Dict, Any

def extract_pdf(file_bytes: bytes) -> Dict[str, Any]:
    """Extracts text from a PDF, preserving page numbers."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        
        # Clean up excessive whitespace while preserving paragraph breaks
        cleaned_text = "\n".join(line for line in text.splitlines() if line.strip())
        
        if cleaned_text:
            pages.append({
                "page_number": page_num + 1,
                "content": cleaned_text
            })
            
    return {
        "file_type": "pdf",
        "page_count": len(doc),
        "pages": pages
    }

def extract_text(file_bytes: bytes, file_type: str) -> Dict[str, Any]:
    """Extracts text from plain text or Markdown files."""
    text = file_bytes.decode("utf-8", errors="replace").strip()
    
    return {
        "file_type": file_type,
        "page_count": 1,
        "pages": [{
            "page_number": 1,
            "content": text
        }]
    }