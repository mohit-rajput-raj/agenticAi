"""Small runnable examples that show how LangChain runnables work.

This file focuses on the core idea:
- a runnable takes an input
- transforms it
- passes it to the next step

The examples below avoid external APIs so the flow is easy to understand.
"""

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough


def clean_text(text: str) -> str:
	"""Normalize whitespace and remove extra spaces."""
	return " ".join(text.strip().split())


def analyze_text(text: str) -> dict:
	"""Return a few simple facts about the text."""
	words = text.split()
	return {
		"text": text,
		"character_count": len(text),
		"word_count": len(words),
		"first_word": words[0] if words else "",
		"last_word": words[-1] if words else "",
	}


def build_summary(stats: dict) -> str:
	"""Convert the analysis dictionary into a readable summary string."""
	return (
		f"Text: {stats['text']}\n"
		f"Characters: {stats['character_count']}\n"
		f"Words: {stats['word_count']}\n"
		f"First word: {stats['first_word']}\n"
		f"Last word: {stats['last_word']}"
	)


def build_parallel_summary(result: dict) -> str:
	"""Show how parallel runnables can compute multiple views of the same input."""
	return (
		"Parallel runnable result:\n"
		f"- cleaned: {result['cleaned']}\n"
		f"- upper: {result['upper']}\n"
		f"- stats: {result['stats']}"
	)


cleaner = RunnableLambda(clean_text)
analyzer = RunnableLambda(analyze_text)
summarizer = RunnableLambda(build_summary)


# A simple linear chain: input -> clean -> analyze -> format.
text_chain = cleaner | analyzer | summarizer


# A parallel chain: the same input is sent to multiple branches.
parallel_chain = RunnableParallel(
	cleaned=cleaner,
	upper=cleaner | RunnableLambda(str.upper),
	stats=cleaner | analyzer,
) | RunnableLambda(build_parallel_summary)


def main() -> None:
	raw_text = "   LangChain   runnables   make pipelines easy.   "

	print("Linear runnable chain:")
	print(text_chain.invoke(raw_text))

	print("\nParallel runnable chain:")
	print(parallel_chain.invoke(raw_text))

	print("\nRunnablePassthrough example:")
	passthrough_chain = RunnablePassthrough.assign(
		cleaned=RunnableLambda(lambda data: clean_text(data["input"])),
		analysis=RunnableLambda(lambda data: analyze_text(clean_text(data["input"]))),
	)
	print(passthrough_chain.invoke({"input": raw_text}))


if __name__ == "__main__":
	main()
