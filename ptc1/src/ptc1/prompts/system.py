from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are a helpful AI assistant.

Rules:
1. Give accurate answers.
2. Do not invent information.
3. Ask for clarification when required.
4. Explain complex topics step by step.
"""

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("placeholder", "{messages}"),
])