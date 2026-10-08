from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware import MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware
from deepagents.backends.utils import create_file_data

load_dotenv()


backend = StateBackend()

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[],
    system_prompt="한국어로 간단하게 답하세요",
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model="openai:gpt-5-mini", backend=backend),
        MemoryMiddleware(backend=backend, sources=["/AGENTS.md"]),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)

files = {
    "/AGENTS.md": create_file_data("학습자는 초보자입니다. 구체적인 예시로 설명하세요"),
    "/skills/agent-study/SKILL.md": create_file_data(
        "---\nname: agent-study\ndescription: AI agent learning guidance\n---\n"
        "Teach in order: model, tools, prompt, structured output."
    ),
}

result = agent.invoke(
    {"messages": [{"role": "user", "content": '에이전트 학습을 어떤 순서로 하면 좋을지 알려줘'}], "files": files}
)

print(result["messages"][-1].content)