from pydantic import BaseModel, Field
from typing import List, Optional

class Step(BaseModel):
    """A single step in a multi-step calculation."""
    step_number: int = Field(description="The sequential number of the step.")
    
    justification: str = Field(
        description="A brief explanation of the logical action taken, referencing the mathematical principle or definition used."
    )
    
    # Keep this for the core calculation
    expression: str = Field(
        description="The resulting mathematical equation or expression for this step, fully written in LaTeX, enclosed in '$' or '$$' delimiters."
    )

class MathReasoningOutput(BaseModel):
    """Structured output for solving a multi-step mathematical word problem."""
    givens: List[str] = Field(description="Known variables and facts extracted from the problem.")
    requested: str = Field(description="The value or quantity to find.")
    
    # ENHANCEMENT: Proof_Structure for complex logical arguments (like Induction)
    strategy_outline: List[str] = Field(description="A short list of high-level logical steps or the structure of the proof.")
    
    steps: List[Step] = Field(description="Ordered list of reasoning and calculation steps using LaTeX.")
    
    # ENHANCEMENT: Single LaTeX field for the final answer
    final_answer: str = Field(
        description="The final, concise numerical or symbolic result, fully written in LaTeX and enclosed in '$' or '$$'."
    )
    
    # ENHANCEMENT: Added Common Error Analysis for pedagogical value
    common_error_analysis: Optional[str] = Field(
        default=None,
        description="A brief explanation of a common mistake a student might make when solving this specific problem and why that mistake is wrong."
    )