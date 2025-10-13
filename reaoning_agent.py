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
math_problem = "Differentiate x**2 * sin(x)"

# Get structured reasoning
result: MathReasoningOutput = llm.invoke(math_problem)

# Print structured output
print("=== Structured Reasoning ===")
print(result)

# Access individual parts
print("\nFinal Answer:", result.final_answer)
