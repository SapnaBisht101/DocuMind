from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedEntity(BaseModel):
    name: str = Field(description="The name of the entity, person, or organization.")
    type: str = Field(description="The type of entity (e.g., 'Person', 'Company', 'Technology').")

class DocumentSummary(BaseModel):
    title: str = Field(description="The inferred title of the document.")
    document_type: str = Field(description="The type of document (e.g., 'Research Paper', 'Meeting Notes', 'General Text').")
    executive_summary: str = Field(description="A concise summary of the document's main points.")
    key_topics: List[str] = Field(description="A list of 3-5 main topics discussed in the document.")
    entities: List[ExtractedEntity] = Field(description="Key entities mentioned in the text.")
    action_items: Optional[List[str]] = Field(default=None, description="Any explicit action items or next steps found in the document.")