from pydantic import BaseModel, Field
from typing import List

class Step(BaseModel):
    """A single, fully justified step in the mathematical derivation."""
    step_number: int = Field(description="The sequential number of the step.")
    
    # RESTORED: This is the concise logical anchor.
    justification: str = Field(
        description="A concise explanation of the logical action taken, explicitly referencing the mathematical principle or theorem (e.g., 'Substitute T(x) and simplify', 'By Mean Value Theorem', 'Algebraic Simplification'). NO verbose text, NO restating the result."
    )
    
    # CLEAN: This field is now strictly for LaTeX math.
    expression: str = Field(
        description="The resulting mathematical equation or expression for this step, fully written in LaTeX, enclosed in '$' or '$$' delimiters. Must contain ONLY LaTeX and NO prose."
    )

class Question(BaseModel):
    """Represents a single sub-question with its full reasoning."""
    question_label: str = Field(description="The label from the original problem (e.g., 'I.1', 'II.4').")
    givens: List[str] = Field(description="Known variables and facts.")
    requested: str = Field(description="The value or quantity to prove or find.")
    
    relies_on_questions: List[str] = Field(
        default_factory=list,
        description="List of prior question labels (e.g., ['I.1', 'II.3']) whose results are necessary for this solution. Empty if none."
    )
    # Rationale: This is the high-level guide.
    strategy_outline: List[str] = Field(description="A short list of high-level logical steps that serve as the guide for the 'steps' list below.")
    
    steps: List[Step] = Field(description="Ordered list of reasoning and calculation steps.")
    
    final_answer: str = Field(
        description="The final, concise numerical or symbolic result, fully written in LaTeX and enclosed in '$' or '$$'."
    )

class FullProblemOutput(BaseModel):
    """The root object for the entire multi-section, hierarchical problem."""
    problem_title: str = Field(description="The main title of the problem.")
    questions: List[Question] = Field(description="An ordered list of solutions for all sub-questions.")