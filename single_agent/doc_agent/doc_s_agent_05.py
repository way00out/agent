from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents import AgentState

load_dotenv()


class LearningState(AgentState):
    user_id: str
    call_count: int

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[],
    system_prompt="한국어로 간단하게 답하세요",
    state_schema=LearningState,
)

result = agent.invoke(
    {
        "messages": [{"role": "user", "content": '에이전트 상태를 한 문장으로 설명해줘'}],
        "user_id": "learner-001",
        "call_count": 0,
    }
)


print(result["messages"][-1].content)
print("사용자 ID:", result["user_id"])
print("직접 전달한 호출 횟수:", result["call_count"])