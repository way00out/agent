from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

load_dotenv()


backend = StateBackend()

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[],
    system_prompt="한국어로 간단하게 답하세요",
    middleware=[
        FilesystemMiddleware(backend=backend),
    ],
)


result = agent.invoke(
    {"messages": [{"role": "user", "content": "write_file 도구로 /notes.txt에 '에이전트 실습'을 저장하고 read_file로 읽어줘"}]}
)

print(result["messages"][-1].content)
print("가상 파일 상태:", result.get("files", {}))