from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[],
    system_prompt="한국어로 간단하게 답하세요.",
)


result = agent.invoke(
    {"messages": [{"role": "user", "content": 'AI 에이전트란 무엇인지 한 문장으로 설명해줘.'}]}
)

print(result["messages"][-1].content)