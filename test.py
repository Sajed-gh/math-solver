import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import MathReasoningOutput

load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]

# Initialize Gemini with structured output
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0,
    api_key=api_key
).with_structured_output(MathReasoningOutput)

# Example math problem
math_problem = "Points A and B lie on a circle with radius 1, and arc AB⌢ has a length of π/3. What fraction of the circumference of the circle is the length of arc AB⌢?"

# Get structured reasoning
result: MathReasoningOutput = llm.invoke(math_problem)

# --- Print Structured Output ---
print("\n" + "="*25)
print("=== STRUCTURED REASONING RESULT ===")
print("="*25)

# 1. Givens
print("\n1. Givens:")
for given in result.givens:
    print(f"  - {given}")

# 2. Requested
print("\n2. Requested:")
print(f"  - {result.requested}")

# 3. Plan
print("\n3. Plan:")
for item in result.plan:
    print(f"  - {item}")
    
# 4. Step-by-step calculation
print("\n4. Step-by-step Calculation:")
for step in result.steps:
    print(f"  [{step.step_number}]: {step.explanation} -> {step.expression}")
    print(f"  [{step.step_number}]: {step.latex_explanation} -> {step.latex_expression}")

# 5. Final Answer
print("\n5. Final Answer:")
print(f"  {result.final_answer}")
print(f"  {result.latex_final_answer}")
print("="*25)
