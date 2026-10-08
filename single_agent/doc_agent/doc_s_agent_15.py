from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()


@tool
def preview_note(text: str) -> str:
    """메모 저장 모의 실행 - 실제 파일 생성 없음"""
    return f"모의 저장 완료: {text}"

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[preview_note],
    system_prompt="한국어로 간단하게 답하세요",
    checkpointer=InMemorySaver(),
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"preview_note": True})],
)

config = {"configurable": {"thread_id": "lesson-15"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "preview_note 도구로 '에이전트 학습 완료'라는 메모를 저장해줘"}]}, config=config
)


while result.get("__interrupt__"):
    decisions = []
    for interrupt in result["__interrupt__"]:
        for request in interrupt.value["action_requests"]:
            print("승인 대기:", request)
            if input("모의 저장을 승인할까요? [y/N]: ").strip().lower() =="y":
                decisions.append({"type": "approve"})
            else:
                decisions.append({"type": "reject", "message": "사용자가 저장을 거절했습니다"})
    result = agent.invoke(Command(resume={"decisions": decisions}), config=config)


for message in result["messages"]:
    message.pretty_print()