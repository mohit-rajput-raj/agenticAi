import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import Annotated, TypedDict

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

model = init_chat_model(
    model="gemini-2.5-flash",
    temperature=0,
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
).bind_tools([add, multiply])


def call_model(state: State):
    response = model.invoke(state["messages"])
    return {"messages": [response]}


workflow = StateGraph(State)
workflow.add_node("llm", call_model)
workflow.add_node("tools", ToolNode([add, multiply]))
workflow.add_edge(START, "llm")
workflow.add_conditional_edges(
    "llm",
    tools_condition,
    {"tools": "tools", "__end__": "__end__"},
)
workflow.add_edge("tools", "llm")

# Compile and run
app = workflow.compile()
response = app.invoke({"messages": [HumanMessage(content="What is 2+2 and 3*3?")]})
print(response["messages"][-1].content)