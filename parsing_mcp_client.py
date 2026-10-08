import asyncio
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter


PROJECT_DIR = Path(__file__).resolve().parents[1]
MCP_SERVER = PROJECT_DIR / "parsing_mcp_server.py"
SAMPLE_DOCUMENT = PROJECT_DIR / "sample/천안캠퍼스_캡스톤_프로젝트.pdf"


async def main():
    load_dotenv(PROJECT_DIR / ".env")

    async with MCPAdapter(MCP_SERVER) as adapter:
        tools = await adapter.list_tools()

        print("MCP Tools:")
        for tool in tools:
            print("-", tool.name)

        agent = create_agent(
            model="openai:gpt-5.5",
            tools=tools,
        )

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"MCP 도구를 사용해서 {SAMPLE_DOCUMENT} 문서를 파싱하고 결과를 간단히 요약해줘"
                        ),
                    }
                ]
            }
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())