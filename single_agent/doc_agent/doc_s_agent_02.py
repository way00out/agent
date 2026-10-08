from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()


@tool
def search(query: str) -> str:
    """AI 에이전트 학습 자료 조회 - 로컬 모의 검색"""
    return (
        f"조회 질문: {query}\n"
        "에이전트는 모델이 도구를 선택하고 결과를 읽으며 작업을 수행한다."
        "system_prompt는 행동 지침이고 response_format은 응답 구조다."
        "checkpointer와 tread_id를 함께 사용하면 대화 이력을 유지한다."
    )


agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[search],
    system_prompt="학습 자료는 search로 확인하고 한국어로 답하세요",
)


result = agent.invoke(
    {"messages": [{"role": "user", "content": 'search 도구를 사용해서 AI 에이전트 학습 자료를 조회해줘'}]}
)


for message in result["messages"]:
    message.pretty_print()