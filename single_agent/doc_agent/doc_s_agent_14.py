from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

load_dotenv()


agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[],
    system_prompt="한국어로 간단하게 답하세요",
    middleware=[PIIMiddleware("email", strategy="redact", apply_to_input=True)],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": '내 테스트 이메일은 learner@example.com이야. 입력 내용을 짧게 설명해줘'}]}
)

for message in result["messages"]:
    message.pretty_print()