from langchain_google_genai import ChatGoogleGenerativeAI
import os

if os.environ["GOOGLE_API_KEY"] == "":
    os.environ["GOOGLE_API_KEY"] = "{YOUR_GOOGLE_API_KEY}"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001")
res = llm.invoke("Hello Gemini")

print(res)
