from pydantic import BaseModel, Field
from typing import List, Optional

class Step(BaseModel):
    """A single step in a multi-step calculation."""
    step_number: int = Field(description="The sequential number of the step.")
    expression: str = Field(
        description="The simplified, plain-text mathematical expression used in this step."
    )
    explanation: str = Field(description="A brief, human-readable description of this step.")
    latex_expression: Optional[str] = Field(
        default=None,
        description="LaTeX math for this step, enclosed in '$' or '$$' delimiters."
    )
    latex_explanation: Optional[str] = Field(
        default=None,
        description="LaTeX-formatted rule or explanation if applicable."
    )

class MathReasoningOutput(BaseModel):
    """Structured output for solving a multi-step mathematical word problem."""
    givens: List[str] = Field(description="Known variables and facts extracted from the problem.")
    requested: str = Field(description="The value or quantity to find.")
    plan: List[str] = Field(description="A short list of high-level reasoning steps.")
    steps: List[Step] = Field(description="Ordered list of reasoning and calculation steps.")
    final_answer: str = Field(description="The final, concise result.")
    latex_final_answer: Optional[str] = Field(
        default=None,
        description="Final answer in LaTeX format, enclosed in '$' or '$$'."
    )
