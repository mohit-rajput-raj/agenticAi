from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

# Define a human message template
human_template = HumanMessagePromptTemplate.from_template(
    "Tell me a {adjective} joke about {topic}."
)

# Create chat prompt
chat_prompt = ChatPromptTemplate.from_messages([human_template])

# Format the prompt
formatted_messages = chat_prompt.format_messages(adjective="funny", topic="chickens")
print(formatted_messages[0].content)
# Output: "Tell me a funny joke about chickens."