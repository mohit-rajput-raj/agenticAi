from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# Define system, human, and AI messages
system_template = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant that tells jokes."
)
human_template = HumanMessagePromptTemplate.from_template(
    "Tell me a {adjective} joke about {topic}."
)
ai_template = AIMessagePromptTemplate.from_template(
    "Here's one: {joke}"
)

# Build chat prompt
chat_prompt = ChatPromptTemplate.from_messages([
    system_template,
    human_template,
    ai_template,
])

# Format the prompt
formatted_messages = chat_prompt.format_messages(
    adjective="funny",
    topic="chickens",
    joke="Why did the chicken cross the road?",
)
for msg in formatted_messages:
    print(f"{msg.type}: {msg.content}")