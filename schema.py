from pydantic import BaseModel, Field
from typing import List, Optional

class Step(BaseModel):
    """A single mathematical derivation step."""
    # Removed step_number - use list index with enumerate()
    
    action: str = Field(
        description="Theorem/principle applied (e.g., 'Derivative rule', 'MVT', 'Substitute and simplify'). Max 10 words."
    )
    
    expr: str = Field(
        description="LaTeX expression only, enclosed in '$'. No prose."
    )

class Question(BaseModel):
    """Single sub-question with complete solution."""
    # Removed question_label - you know which Q you asked
    
    objective: str = Field(
        description="What to prove/find, including key given facts."
    )
    
    deps: List[str] = Field(
        default_factory=list,
        description="Prior question IDs needed (e.g., ['I.1', 'II.2']). Empty if independent."
    )
    
    steps: List[Step] = Field(
        description="Minimum necessary steps. Combine trivial algebra."
    )
    
    result: str = Field(
        description="Final answer in LaTeX with '$'. Use '$\\text{N/A}$' if non-numerical."
    )

class FullProblemOutput(BaseModel):
    """Complete multi-question solution."""
    title: str = Field(description="Problem title.")
    solutions: List[Question]