from langchain_core.prompts import PromptTemplate

# Define template with placeholders
template = """Tell me a {adjective} joke about {topic}."""

prompt = PromptTemplate.from_template(template)

# Format the prompt
formatted_prompt = prompt.format(adjective="funny", topic="chickens")
print(formatted_prompt)
# Output: "Tell me a funny joke about chickens."

# Use with an LLM
from langchain_community.llms import FakeListLLM
llm = FakeListLLM(responses=["Why did the chicken cross the road? To get to the other side!"])

chain = prompt | llm
print(chain.invoke({"adjective": "funny", "topic": "chickens"}))
# Output: "Why did the chicken cross the road? To get to the other side!"