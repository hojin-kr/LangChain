# Project LangChain
LangChain은 LLM을 보다 편리하고 효율적으로 사용하기 위한 프레임워크입니다. 다양한 Provider를 지원하고 있으며 Prompt Template, Response Schema등의 기능을 사용해서  명확하며 재사용 가능한 Prompt를 구성하기에 도움을 주며 Respone Schema를 정의하여 반환의 형식(Struct)을 명확하고 의미론적으로 LLM에게 질의할 수 있도록 합니다.

1. Google의 Gemini를 활용한 기본적인 Prompt Invoke
2. Prompt의 기본적인 3가지 요소 (system, context, question)
3. Prompt Template과 Response Schema
4. RAG를 사용한 추가 정보 사용
5. Vector-Store와 Retriver로 지식 베이스 기능 구현

## Feature
- LLM: Google Gemini
- LLM Framework: LangChain
- API Framework: fastAPI


## Setup
1. 파이썬의 가상 독립된 가상 환경을 생성
```
python3 -m venv .venv
```
2. 필요 패키지 설치
```
.venv/bin/pip install -r requrement.txt
.venv/bin/fastapi dev main.py
```
> requrement.txt 사용하지 않고 각각 설치하고자 하는 경우 참조  
> [LangChain Provider Google Gen AI](https://python.langchain.com/v0.2/docs/integrations/platforms/google/)
> ```
>  .venv/bin/pip install -U langchain-google-genai
> ```  

## Google의 Gemini를 활용한 기본적인 Prompt Invoke
1. Google Gen AI API KEY 발급  
Google의 LLM Gemini를 API로 사용하기 위해서 API KEY를 발급 받습니다. GCP Console의 Credentials 에서 API KEY를 추가하고 역할을 추가합니다.  

![CreateGoogleAPIKey](assets/image.png)

2. 정상적으로 동작하는지 테스트  
샘플 코드 [sample/google-gemini-invoke.py](sample/google-gemini-invoke.py)
```
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "{YOUR_GOOGLE_API_KEY}"

llm = ChatGoogleGenerativeAI(model="gemini-pro")
res = llm.invoke("Hello Gemini")

print(res)
```
실행  
```
.venv/bin/python sample/google-gemini-invoke.py
```
출력  
metadata를 통해서 Google Gemini에서 사용되는 안전한 LLM위한 필터들을 살펴 볼 수 있습니다. 위험한 콘텐츠나 민감하거나 섹슈얼한 것들을 기본적으로 블록합니다. 추후 해당 블록 레벨을 조정하여 사용할 수 있습니다.  
(블록을 완전히 제거하는것은 엔터프라이즈에서 별도 협의가 필요합니다.)
```
content="Hello! I am not Gemini, I am Gemini, a multi-modal AI model, developed by Google. But I'm happy to help you with your questions or tasks to the best of my abilities." 

response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'safety_ratings': [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE', 'blocked': False}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE', 'blocked': False}, {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE', 'blocked': False}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE', 'blocked': False}]} id='run-66d8eb71-f615-4c3f-b867-c4f126793870-0' usage_metadata={'input_tokens': 3, 'output_tokens': 42, 'total_tokens': 45}
```

## Prompt의 기본적인 3가지 요소 (system, context, question)

- System: 모델에게 주고자하는 역할을 정의
- Context: 모델이 Prompt에 대해 동작하기에 참조해야하는 정보들, 문맥들
- Question: 해결하고자 하는 것 

Questtion의 경우에 모델이 Context와 Response format을 통해 추론하여 답변을 하도록 구성할 수 있으며, 직접 어떤 문제를 해결해달라는 Chat 형태가 될 수 있습니다. 다양한 형태가 될 수 있는 모델을 통해 해결하고자 하는 것을 전달하는것을 통칭했습니다.  

### 예시
```
<목표 & 페르소나>
모델에게 목표와 모델의 페르소나, 성격, 답변의 스타일을 정의합니다.
</목표 & 페르소나>

<안내> 
목표를 달성하는데 있어서 필요한 절차 안내 등을 명시합니다.
</안내>  

<제약조건>
모델에게 답변을 생성할 때, 제약할 조건을 제시합니다.
</제약조건>

<CONTEXT> 
모델에게 참조할 정보들을 줍니다.
</CONTEXT>  

<OUTPUT_FORMAT> 
답변의 형태를 정의합니다. 일반 문자열이 될 수 있고 XML이나 JSON등 다양한 형태가 될 수 있습니다.
</OUTPUT_FORMAT>  

<FEW_SHOT_EXAMPLES> 
답변을 생성하는데 참조할 수 있는 예시 질의와 답변 페어를 준비합니다.
</FEW_SHOT_EXAMPLES>  

```
> 참조
> [Google Gen AI 프롬프팅 전략 가이드](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies?hl=ko)

## Prompt Template과 Response Schema
LangChain의 Prompt Template과 Response Schema를 활용하면 프롬프트 전략을 편리하게 구사할 수 있으며 명확하게 프롬프트를 전달할 수 있습니다.

### Prompt Template
Prompt를 Tempalte으로 작성하여 System을 정의하고 퓨샷이나 질의를 정의하고 input으로 받도록 합니다.


```
# 간단한 예시
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "{input}"),
    ]
)
prompt = prompt_template.format_prompt(input="Hello Gemini")

```

### Response Schema
구조화된 반환을 정의합니다. 반환에 대한 속성을 지정하고 각 속성에 대한 설명을 추가합니다.

```
# 간단한 예시
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
```

### Prompt Template과 Response Schema를 활용
- system과 few-shot을 정의하고 유저로부터 입력 받은 Input을 전달합니다.
- 구조화된 schema를 정의하고 해당 형태로 반환을 받습니다.

[prompt Template과 Response Schema를 활용](sample/google-gemini-prompt-template-schema.py)   

반환
```
.venv/bin/python sample/google-gemini-prompt-template-schema.py  

[{'args': {'output': '힘든 날들이 계속되는 건 당연해요. 누구나 힘들 때가 있고, 그럴 땐 잠시 쉬어가는 것도 필요해요. 긍정적인 에너지를 찾아보고, 스스로에게 칭찬과 격려를 아끼지 마세요.', 'reason': '힘든 시기를 극복할 수 있도록 위로와 격려를 해줍니다.'}, 'type': 'Response'}]
```

```
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

```
