from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langgraph.store.memory import InMemoryStore
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os

load_dotenv()
# A dictionary to store history for different sessions
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


model = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", api_key=os.getenv("GEMINI_API_KEY"))
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{chat_history}"),
    ("human", "{snippet}")
])
chain = chat_prompt | model
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="snippet",
    history_messages_key="chat_history"
)

# First turn of conversation
res1 = chain_with_history.invoke(
    {"snippet": "what is (2+2)/2?"},
    config={"configurable": {"session_id": "session_1"}}
)
print("First Response:")
print(res1.content)
print("-" * 50)

# Second turn of conversation (relies on history)
res2 = chain_with_history.invoke(
    {"snippet": "multiply that result by 10"},
    config={"configurable": {"session_id": "session_1"}}
)
print("Second Response (using history):")
print(res2.content)
print("-" * 50)

# Print the messages stored in the session history
print("Stored Session History:")
for msg in store["session_1"].messages:
    print(f"{type(msg).__name__}: {msg.content}")