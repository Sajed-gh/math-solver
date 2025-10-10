from langchain.agents import tool
import sympy as sp

@tool
def symbolic_solver(expr_str: str) -> str:
    """
    Phase 1 safe version for ZeroShotAgent.
    Solves the expression for x.
    Example: 'x**2 - 1' -> [-1, 1]
    """
    try:
        x = sp.symbols("x")
        expr = sp.sympify(expr_str)
        result = sp.solve(expr, x)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
