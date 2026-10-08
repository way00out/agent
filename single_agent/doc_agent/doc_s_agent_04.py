from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@tool
def search(query: str) -> str:
    """AI 에이전트 학습 자료 조회 - 로컬 모의 검색"""
    return (
        f"조회 질문: {query}\n"
        "에이전트는 모델이 도구를 선택하고 결과를 읽으며 작업을 수행한다"
        "system_prompt는 행동 지침이고 response_format은 응답 구조다"
        "checkpointer와 thread_id를 함께 사용하면 대화 이력을 유지한다"
    )

class Answer(BaseModel):
    summary: str = Field(description="핵심 내용을 서술어 없이 한국어로 요약")
    confidence: float = Field(ge=0, le=1, description="모델이 자기평가한 확신 정도")

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[search],
    system_prompt="학습자료는 search로 확인하고 한국어로 답하세요",
    response_format=Answer,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": 'search로 확인하고 AI 에이전트를 요약해줘'}]}
)


answer = result["structured_response"]

print(answer.model_dump_json(indent=2))
print("신뢰도 (모델의 자기평가):", answer.confidence)