from pydantic import BaseModel, Field
from typing import List, Optional

class Step(BaseModel):
    """A single, fully justified step in the mathematical derivation."""
    step_number: int = Field(description="The sequential number of the step.")
    
    justification: str = Field(
        description="A brief explanation of the logical action taken, explicitly referencing the mathematical principle, theorem, or definition used (e.g., 'Circumference Formula', 'Pythagorean Theorem', 'Algebraic simplification')."
    )
    
    expression: str = Field(
        description="The resulting mathematical equation or expression for this step, fully written in LaTeX, enclosed in '$' or '$$' delimiters. Must not be plain text."
    )

class Question(BaseModel):
    """Represents a single sub-question (e.g., I.1, II.3) with its full reasoning."""
    question_label: str = Field(description="The label from the original problem (e.g., 'I.1', 'II.4').")
    givens: List[str] = Field(description="Known variables and facts extracted from the problem.")
    requested: str = Field(description="The value or quantity to prove or find.")
    
    relies_on_questions: List[str] = Field(
        default_factory=list, # <-- THE CRITICAL CHANGE
        description="List of prior question labels (e.g., ['I.1', 'II.3']) whose results are necessary for this solution. Empty if none."
    )
    strategy_outline: List[str] = Field(description="A short list of high-level logical steps or the structure of the proof.")
    steps: List[Step] = Field(description="Ordered list of reasoning and calculation steps using LaTeX.")
    final_answer: str = Field(
        description="The final, concise numerical or symbolic result, fully written in LaTeX and enclosed in '$' or '$$'."
    )
    common_error_analysis: Optional[str] = Field(
        default=None,
        description="A brief explanation of a common mistake a student might make when solving this specific sub-question and why that mistake is wrong."
    )

class FullProblemOutput(BaseModel):
    """The root object for the entire multi-section, hierarchical problem."""
    problem_title: str = Field(description="The main title of the problem (e.g., 'Approximation of ln(x) par des suites').")
    questions: List[Question] = Field(description="An ordered list of solutions for all sub-questions.")
