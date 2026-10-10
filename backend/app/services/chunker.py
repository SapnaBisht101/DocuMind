from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

def chunk_document(extraction_result: Dict[str, Any], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict[str, Any]]:
    """Splits extracted pages into smaller chunks while preserving page metadata."""
    
    # This splitter keeps paragraphs and sentences together as much as possible
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,  # Overlap prevents cutting concepts in half
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []
    for page in extraction_result["pages"]:
        page_text = page["content"]
        page_num = page["page_number"]
        
        # Split the current page's text
        page_chunks = text_splitter.split_text(page_text)
        
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "page_number": page_num,
                    "chunk_index": i
                }
            })
            
    return chunks