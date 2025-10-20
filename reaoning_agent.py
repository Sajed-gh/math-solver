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
problem_text = """
==================================================
=== Problème: Approximation de ln(x) par des suites ===
==================================================

On se place dans le cas où x est un réel fixé tel que $x \in [1, +\infty[$.
On définit les fonctions $T$ et $S$ par:
$$T(x) = \frac{x^2 - 1}{x^2 + 1} \quad \text{et} \quad S(x) = \frac{x^2 - 1}{2x}$$

On définit également les fonctions $f$ et $g$ par:
$$f(x) = \ln(x) - T(x) \quad \text{et} \quad g(x) = S(x) - \ln(x)$$

---
## Partie I : Étude des fonctions T, S, f, et g

### Question I.1
Prouver les inégalités suivantes pour tout $x \in [1, +\infty[$ :
$$T(x) \le 2T(\sqrt{x}) \quad \text{et} \quad 2S(\sqrt{x}) \le S(x)$$

### Question I.2
On considère les fonctions $f$ et $g$.
a) Montrer que les dérivées sont données par:
$$f'(x) = \frac{(x^2 - 1)^2}{x(x^2 + 1)^2} \quad \text{et} \quad g'(x) = \frac{(x-1)^2}{2x^2}$$
b) En déduire les encadrements suivants pour tout $x \in [1, +\infty[$ :
$$0 \le f'(x) \le (x-1)^2 \quad \text{et} \quad 0 \le g'(x) \le \frac{1}{2}(x-1)^2$$

### Question I.3
Sachant que $f(1)=0$ et $g(1)=0$, déduire des encadrements de la Question I.2 les encadrements suivants pour tout $x \in [1, +\infty[$ :
$$0 \le f(x) \le \frac{1}{3}(x-1)^3 \quad \text{et} \quad 0 \le g(x) \le \frac{1}{6}(x-1)^3$$

---
## Partie II : Étude de suites adjacentes

On fixe un réel $x \in ]1, +\infty[$. On pose $x_0 = x$.
Pour tout entier $n \in \mathbb{N}$, on définit la suite $(x_n)_{n \in \mathbb{N}}$ par la relation de récurrence :
$$x_{n+1} = \sqrt{x_n}$$

On définit également les suites $(t_n)_{n \in \mathbb{N}}$ et $(s_n)_{n \in \mathbb{N}}$ par :
$$t_n = 2^n T(x_n) \quad \text{et} \quad s_n = 2^n S(x_n)$$

### Question II.1
a) Déterminer la limite de la suite $(x_n)_{n \in \mathbb{N}}$.
b) Montrer que pour tout $n \in \mathbb{N}$, on a les inégalités :
$$t_n \le t_{n+1} \quad \text{et} \quad s_{n+1} \le s_n$$
c) En déduire la monotonie des suites $(t_n)_{n \in \mathbb{N}}$ et $(s_n)_{n \in \mathbb{N}}$.

### Question II.2
En utilisant la Question I.3, établir l'encadrement suivant pour tout $n \in \mathbb{N}$ :
$$t_n \le \ln(x) \le s_n$$

### Question II.3
a) Montrer la relation : $s_n - t_n = \frac{2^n (x_n - 1)^2}{2x_n (x_n + 1)}$.
b) En déduire que $\lim_{n \to +\infty} (s_n - t_n) = 0$.

### Question II.4
Que peut-on en déduire concernant la nature (convergence et limite) des suites $(t_n)_{n \in \mathbb{N}}$ et $(s_n)_{n \in \mathbb{N}}$ ?
"""

target_language = "French"

# --- REVISED SYSTEM INSTRUCTION (OPTIMIZED FOR CONCISENESS) ---
system_instruction = """Solve all questions strictly using logical reasoning.

- Focus on major logical moves; combine trivial algebra.
- Minimize step count while maintaining correctness.
- Check each inequality, derivative, or limit carefully.
- Ensure final answers match derivations.
- Use previous results efficiently (respect dependency relations).
- Prioritize rigor, clarity, and conciseness in steps.
- Check final answers for consistency with steps.
- Always include a 'result' field for each question, even if approximate.
"""
# Invoke LLM
# print("Invoking LLM for structured hierarchical solution...")
result: FullProblemOutput = llm.invoke([system_instruction, problem_text])


# ================================================================
# ======================  FORMATTED PRINT  ========================
# ================================================================
print("\n" + "="*50)
print(f"=== STRUCTURED REASONING RESULT: {result.title} ===")
print("="*50)

for idx,question in enumerate(result.solutions):
    print(f"\n## Question {idx}")
    print("--------------------------------------------------")
    
    print("  Objective:")
    print(question.objective)
    
    print(f"  Relies On: {', '.join(question.deps)}")
    
        
    print("\n  Detailed Derivation:")
    for num,step in enumerate(question.steps):
        print(f"    [{num}]: **{step.action}**")
        print(f"        {step.expr}")
        
    print("\n  Final Answer:")
    print(f"    {question.result}")

print("\n" + "="*50)