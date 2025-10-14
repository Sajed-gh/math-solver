import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import MathReasoningOutput # Assuming the revised schema above is in schema.py

load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]

# Initialize Gemini with structured output
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0, # Keep temperature low for high accuracy/rigor
    api_key=api_key
).with_structured_output(MathReasoningOutput)

# Example math problem
math_problem = "Points A and B lie on a circle with radius 1, and arc AB⌢ has a length of π/3. What fraction of the circumference of the circle is the length of arc AB⌢?"

# --- ENHANCEMENT: Direct the Model's Reasoning with a detailed prompt ---

system_instruction = """
You are a highly rigorous, university-level mathematics tutor. Your task is to solve the user's math problem and structure your reasoning STRICTLY according to the provided JSON schema.

RULES FOR REASONING AND OUTPUT:
1.  **Justification is King:** In the 'steps', the 'justification' field must clearly state the specific mathematical rule, formula, or principle being applied (e.g., 'Circumference Formula', 'Definition of a Fraction', 'Isolating Variable'). Do not just say 'calculate' or 'substitute'; state *what* is being calculated or *what* formula is used.
2.  **LaTeX is Mandatory:** Every single mathematical expression, equation, or numerical result MUST be enclosed in LaTeX delimiters '$' or '$$'. The 'latex_expression' field must contain the complete equation for the step.
3.  **Strategy Outline:** The 'strategy_outline' must list the necessary high-level steps *before* calculation begins.
4.  **Common Errors:** Generate a plausible 'common_error_analysis' specific to this problem to enhance pedagogical value.
"""

# The instruction is now packed into the invocation logic
result: MathReasoningOutput = llm.invoke([system_instruction, math_problem])

# --- Print Structured Output (Adjusted to match new schema) ---
print("\n" + "="*25)
print("=== STRUCTURED REASONING RESULT (Enhanced) ===")
print("="*25)

# 1. Givens
print("\n1. Givens:")
for given in result.givens:
    print(f"  - {given}")

# 2. Requested
print("\n2. Requested:")
print(f"  - {result.requested}")

# 3. Strategy Outline
print("\n3. Strategy Outline:")
for item in result.strategy_outline:
    print(f"  - {item}")
    
# 4. Step-by-step Calculation (Simplified print, only showing one math field)
print("\n4. Step-by-step Calculation:")
for step in result.steps:
    print(f"  [{step.step_number}]: {step.justification}")
    print(f"  \t-> {step.expression}") # Only printing the LaTeX version
    
# 5. Final Answer
print("\n5. Final Answer:")
print(f"  {result.final_answer}")

# 6. Common Error Analysis
if result.common_error_analysis:
    print("\n6. Common Error Analysis:")
    print(f"  {result.common_error_analysis}")
print("="*25)