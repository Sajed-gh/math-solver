import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import base64

system_prompt = """
You are a PDF expert.
""".strip()

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

# Initialize Gemini with the NEW top-level structured output
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0,
    api_key=api_key
)

# Open and read the PDF file content as bytes
with open("MP_MATHS_CENTRALE_2_2020.enonce.pdf", "rb") as f:
    pdf_bytes = f.read()

# Encode the PDF content to base64
pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

r = llm.invoke(
    [
        SystemMessage(content=system_prompt),
        HumanMessage(
            [
                {
                    "type": "media",
                    "data": pdf_base64,
                    "mime_type": "application/pdf",
                },
                "can you understand the math expressions here",
            ]
        ),
    ]
)

print(r)