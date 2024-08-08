from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "{YOUR_GOOGLE_API_KEY}"

llm = ChatGoogleGenerativeAI(model="gemini-pro")
res = llm.invoke("Hello Gemini")

print(res)
