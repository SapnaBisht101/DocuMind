from pydantic import BaseModel, Field
from typing import List, Optional

class StoryboardStep(BaseModel):
    step_number: int = Field(description="The sequential step or screen number.")
    title: str = Field(description="Action-oriented title for this step.")
    purpose: str = Field(description="Why this step is necessary.")
    actor_or_role: str = Field(description="Who or what performs this action (e.g., 'User', 'Backend API', 'System').")
    inputs: List[str] = Field(description="Required inputs or prerequisites for this step.")
    processing_logic: str = Field(description="Detailed logic, business rules, or user interaction happening in this step.")
    expected_output: str = Field(description="The result or artifact produced by this step.")
    is_explicit_requirement: bool = Field(description="True if explicitly stated in the document; False if recommended by AI.")
    supporting_source_refs: Optional[List[str]] = Field(default=[], description="Source references or page numbers backing this step.")

class Storyboard(BaseModel):
    title: str = Field(description="Overall title of the generated workflow or storyboard.")
    mode: str = Field(description="Generation mode used (e.g., 'software', 'business', 'research', 'presentation').")
    project_overview: str = Field(description="Executive summary of the project or process.")
    target_audience_or_users: List[str] = Field(description="Target audience, personas, or system actors.")
    steps: List[StoryboardStep] = Field(description="Ordered list of steps forming the complete storyboard.")
    dependencies: List[str] = Field(description="Key technical, operational, or resource dependencies.")
    ai_recommendations: List[str] = Field(description="Explicit list of AI suggestions that were NOT in the original document.")