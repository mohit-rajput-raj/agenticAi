from langchain_core.prompts import PromptTemplate

template = """Tell me a {adjective} joke about {topic}."""
prompt = PromptTemplate.from_template(template)

# Partially fill the prompt
partial_prompt = prompt.partial(adjective="funny")

# Now only `topic` is required
print(partial_prompt.format(topic="chickens"))
# Output: "Tell me a funny joke about chickens."