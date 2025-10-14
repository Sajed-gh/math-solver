import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import FullProblemOutput # Assuming the revised schema above is in schema.py

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

# Initialize Gemini with the NEW top-level structured output
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0,
    api_key=api_key
).with_structured_output(FullProblemOutput)

# Problem Section I from the user's request
math_problem_section_i = """
Approximation de ln(x) par des suites

I. Quelques inégalités

Dans cette partie, x est un réel quelconque de l'intervalle [1, +∞[.

Definitions:
Pour tout réel strictement positif x, on pose T(x) = (x^2 - 1) / (x^2 + 1) et S(x) = (x^2 - 1) / (2x).
De plus, on pose f(x) = ln(x) - T(x) et g(x) = S(x) - ln(x). (On note que f(1)=g(1)=0)

Questions:
1. Prouver les inégalités : T(x) ≤ 2T(√x) et 2S(√x) ≤ S(x).
2. Prouver les encadrements : 0 ≤ f'(x) ≤ (x-1)^2 et 0 ≤ g'(x) ≤ (1/2)(x-1)^2.
3. En déduire les encadrements : 0 ≤ f(x) ≤ (1/3)(x-1)^3 et 0 ≤ g(x) ≤ (1/6)(x-1)^3.
"""

target_language = "French"

# --- REVISED SYSTEM INSTRUCTION ---
system_instruction = """
You are a highly rigorous, university-level mathematics tutor. Your task is to solve the multi-part problem and structure your reasoning STRICTLY according to the FullProblemOutput JSON schema.

**LANGUAGE RULE:** All text fields MUST be written entirely in {target_language}.

RULES FOR REASONING AND OUTPUT:
1.  **Step Granularity:** Each 'Step' object must represent a **major logical transition or calculation**. Do NOT separate simple algebraic manipulations (like distributing, factoring, or moving a term) into separate steps. Combine multiple small algebraic actions into a single step with a comprehensive 'justification'.
2.  **Justification is King:** The 'justification' field must be a complete sentence explaining the combined operation (e.g., 'Substitution and simplification of the expression $2T(\sqrt{x})$').
3.  **Dependency Tracking:** Explicitly populate 'relies_on_questions'.
4.  **LaTeX is Mandatory:** Every mathematical expression must be enclosed in LaTeX delimiters '$' or '$$' within the 'expression' field.
"""

# Invoke LLM
print("Invoking LLM for structured hierarchical solution...")
result: FullProblemOutput = llm.invoke([system_instruction, math_problem_section_i])

# --- REVISED PRINTING METHOD FOR HIERARCHICAL SCHEMA ---
print("\n" + "="*50)
print(f"=== STRUCTURED REASONING RESULT: {result.problem_title} ===")
print("="*50)

for question in result.questions:
    print(f"\n## Question {question.question_label}")
    print("--------------------------------------------------")
    
    # 1. Givens & Requested
    print("  Givens:")
    for given in question.givens:
        print(f"    - {given}")
    print(f"  Requested: {question.requested}")
    
    # 2. Dependency Tracking
    if question.relies_on_questions:
        print(f"  Relies On: {', '.join(question.relies_on_questions)}")
    
    # 3. Strategy Outline
    print("\n  Strategy Outline:")
    for item in question.strategy_outline:
        print(f"    - {item}")
        
    # 4. Step-by-step Calculation
    print("\n  Step-by-step Derivation:")
    for step in question.steps:
        print(f"    [{step.step_number}]: **{step.justification}**")
        print(f"    \t{step.expression}")
        
    # 5. Final Answer
    print("\n  Final Answer:")
    print(f"    {question.final_answer}")
    
    # 6. Common Error Analysis
    if question.common_error_analysis:
        print("\n  Common Error Analysis:")
        print(f"    {question.common_error_analysis}")

print("\n" + "="*50)
