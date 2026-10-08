from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[],
    system_prompt="한국어로 간단하게 답하세요",
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "lesson-6"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": '내 이름은 민수야. 기억해'}]}, config=config
)

print(result["messages"][-1].content)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "내 이름이 뭐였지?"}]},
    config=config,
)

print(result["messages"][-1].content)