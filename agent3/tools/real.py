from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage

import os

from dotenv import load_dotenv

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    import random
    if random.random() < 0.2:  # 20% chance of failure
        raise ConnectionError("Weather API timeout")
    return f"Sunny in {city}"

@tool
def get_time(timezone: str) -> str:
    """Get the current time in a timezone."""
    import random
    if random.random() < 0.1:  # 10% chance of failure
        raise ValueError("Invalid timezone")
    return f"12:00 PM in {timezone}"

@tool
def fallback_response(query: str) -> str:
    """Fallback if other tools fail."""
    return f"I couldn't process your request: {query}"

# --- Error Recovery ---
def safe_weather(city: str) -> str:
    try:
        return get_weather.invoke({"city": city})
    except Exception as e:
        print(f"Weather tool failed: {e}")
        return fallback_response.invoke({"query": f"weather in {city}"})

def safe_time(timezone: str) -> str:
    try:
        return get_time.invoke({"timezone": timezone})
    except Exception as e:
        print(f"Time tool failed: {e}")
        return fallback_response.invoke({"query": f"time in {timezone}"})

# --- Tool Routing ---
def route_query(input: dict) -> str:
    query = input["input"].lower()
    if "weather" in query:
        return "safe_weather"
    elif "time" in query:
        return "safe_time"
    else:
        return "fallback_response"

routed_chain = RunnableBranch(
    (lambda x: "weather" in x["input"].lower(), RunnableLambda(lambda x: safe_weather(x["input"]))),
    (lambda x: "time" in x["input"].lower(), RunnableLambda(lambda x: safe_time(x["input"]))),
    RunnableLambda(lambda x: fallback_response.invoke({"query": x["input"]})),
)

# --- Agent with Tools ---
tools = [get_weather, get_time, fallback_response]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
)
llm = llm.bind_tools(tools)


def run_agent(user_input: str) -> str:
    messages = [HumanMessage(content=user_input)]
    response = llm.invoke(messages)
    messages.append(response)

    tool_map = {
        "get_weather": get_weather,
        "get_time": get_time,
        "fallback_response": fallback_response,
    }

    for tool_call in response.tool_calls:
        tool_result = tool_map[tool_call["name"]].invoke(tool_call)
        tool_results.append(f"{tool_call['name']}: {tool_result}")
        messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))

    if tool_results:
        return " | ".join(tool_results)

    return response.content or ""

# --- Invoke ---
# Using routed chain
print(routed_chain.invoke({"input": "What's the weather in Paris?"}))
print(routed_chain.invoke({"input": "What time is it in London?"}))

# Using agent
print(run_agent("What's the weather in Paris and the time in London?"))