import os

from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model

load_dotenv()

checkpointer = InMemorySaver()

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
)


def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.add_edge(START, "model")

graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "conversation-1"}}

# Test conversation
output = graph.invoke({"messages": [{"role": "user", "content": "Hi, I'm Alice"}]}, config)
print(output["messages"][-1].content)

output = graph.invoke({"messages": [{"role": "user", "content": "What's my name?"}]}, config)
print(output["messages"][-1].content)