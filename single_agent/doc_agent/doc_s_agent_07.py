from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

load_dotenv()


@dataclass
class Context:
    user_id: str


@tool
def current_user(runtime: ToolRuntime[Context]) -> str:
    """실행 컨텍스트의 현재 사용자 ID 조회"""
    return runtime.context.user_id


agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[current_user],
    system_prompt="한국어로 간단하게 답하세요",
    context_schema=Context,
)


result = agent.invoke(
    {"messages": [{"role": "user", "content": 'current_user 도구로 내 사용자 ID를 확인해줘'}]}, context=Context(user_id="learner-001")
)


for message in result["messages"]:
    message.pretty_print()