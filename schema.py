from pydantic import BaseModel, Field
from typing import List

class Step(BaseModel):
    """A single step in a multi-step calculation."""
    step_number : int = Field(description="The sequential number of the step.")
    explanation : str = Field(description="A brief description of the goal of this step.")
    expression : str = Field(description="The mathematical expression used in this step.")
    

class MathReasoningOutput(BaseModel):
    """Structured output for solving a multi-step mathematical word problem."""
    givens: List[str] = Field(description="A list of known variables and facts extracted from the problem.")
    requested : str = Field(description="The final value or quantity the user is asking to find.")
    plan : List[str] = Field(description="A list of steps outlining the solution strategy.")
    calculation_steps : List[Step] = Field(description="A detailed, ordered list of calculation steps.")
    final_answer : str = Field(description="The final, concise numerical or textual answer.")