import os 
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.sympy_tool import symbolic_solver


load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]


llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature = 0.2,
    api_key=api_key
)

prompt_template = """
    You are a math assistant. 
    You will solve the problem step by step like an engineering student.
    Problem: {problem}

    Instructions:
    1. Identify what type of equation this is.
    3. Return your reasoning and the solution.
"""

prompt = PromptTemplate(
    input_variables=["problem"],
    template=prompt_template
)


tools = [symbolic_solver]

llm = llm.bind_tools(tools)



chain = prompt | llm


if __name__ == "__main__":
    print("🧠 AI Math Agent (Phase 1.5) — Tool-Bound Chain Mode")

    response = llm.invoke("x**3 - 6*x**2 + 11*x - 6")
    print("\n💬 Gemini Response:")
    print(response)

    # Correctly access tool_calls from AIMessage
    tool_calls = response.tool_calls

    if tool_calls:
        first_call = tool_calls[0]
        expr_str = first_call["args"]["expr_str"]
        solution = symbolic_solver.invoke(expr_str)
        print("💡 Computed Solution:", solution)
    else:
        print("No tool calls detected in the response.")

    