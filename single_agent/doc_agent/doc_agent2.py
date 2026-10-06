from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}"


agent = create_agent(
    model="openai:gpt-4o",
    tools=[get_weather],
    system_prompt="You are helpful assistant in Korean",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "샌프란시스코 날씨는 어때?"}]}
)

print(result["messages"][-1].content)