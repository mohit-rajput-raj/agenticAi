
# from ..GemniniModel import Model


# model = Model()
# llm = model.get_llm()

# print(llm.invoke({"role": "user", "content": "Hello, how are you?"}).content)

import os
import sys

# Add the parent directory (agent3/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now use absolute import
from MyCustomGemniniModel import Model
from langchain_core.messages import HumanMessage


def main() -> None:
	model = Model()
	llm = model.get_llm()
	try:
		response = llm.invoke([HumanMessage(content="Hello, how are you?")])
		print(response.content)
	except Exception as exc:
		error_text = str(exc)
		if "ResourceExhausted" in error_text or "429" in error_text or "quota" in error_text.lower():
			print("Gemini API quota is exhausted right now. Please retry later or switch API key/project.")
			return
		raise


if __name__ == "__main__":
	main()