from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

if os.environ["GOOGLE_API_KEY"] == "":
    os.environ["GOOGLE_API_KEY"] = "{YOUR_GOOGLE_API_KEY}"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001")

# prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "심리 상담가인데, 모든 질문에 긍정적으로 답변해줘"),
        (
            "user",
            [
                {
                    "type": "text",
                    "text": "내일이 오는게 무서워요"
                },
                {
                    "type": "text",
                    "text": 
                    """
                        - output: 내일은 내일의 태양이 뜹니다. 긍정적으로 하루를 시작해보세요.
                        - reason: 내일의 희망을 가질 수 있도록합니다.   
                    """
                },
                {
                    "type": "text",
                    "text": "{input}"
                }
            ],
         )
    ]
)

# response schema
schema = {
    "title": "Response",
    "description": "The output of the prompt",
    "type": "object",
    "properties": {
        "output": {
            "type": "string",
            "description": "The output of the prompt",
        },
        "reason": {
            "type": "string",
            "description": "The reason for the output",
        }
    }
}

chain = prompt | llm.with_structured_output(schema)
res = chain.invoke({"input": "기운이 없는 날이 계속되는것 같아요"})

print(res)
