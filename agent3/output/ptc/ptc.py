import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()
@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Sunny in {city}"

@tool
def get_time(timezone: str) -> str:
    """Get the current time in a timezone."""
    return f"12:00 PM in {timezone}"


llm = init_chat_model(
    model="gemini-2.5-flash",
    temperature=0,
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
)
llm = llm.bind_tools([get_weather, get_time])

messages = [HumanMessage(content="What's the weather in Paris and the time in London?")]
response = llm.invoke(messages)
messages.append(response)

tool_map = {
    "get_weather": get_weather,
    "get_time": get_time,
}

for tool_call in response.tool_calls:
    tool_result = tool_map[tool_call["name"]].invoke(tool_call)
    messages.append(
        ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
    )

final_response = llm.invoke(messages)
print(final_response.content)