import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()

@tool
def englishGreeting() -> str:
    """Returns an English greeting."""
    return "Good morning!"

@tool
def mohitNumbersTool(a:int) -> int:
   """mohit formula to find mohitnumber"""

   return a**2 + 2*a + 1


def build_model():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("No Gemini API key found.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # or gemini-1.5-pro etc.
        temperature=0.7,
        api_key=api_key,
    ).bind_tools([englishGreeting, mohitNumbersTool ])


def _run_requested_tools(messages, tool_calls):
    """Execute model-requested tools and append tool results to the message list."""
    tool_map = {
        "englishGreeting": englishGreeting,
        "mohitNumbersTool": mohitNumbersTool,
    }

    tool_outputs = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool = tool_map.get(tool_name)
        if tool is None:
            continue

        tool_result = tool.invoke(tool_call)
        tool_outputs.append(str(tool_result))
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            )
        )

    return tool_outputs


def run_agent(user_text: str) -> str:
    """Run a tiny tool-using agent and return the final reply text."""
    llm = build_model()
    messages = [
        SystemMessage(
            content=(
                "You are a precise, efficient technical assistant. "
                "When the user asks for a greeting, call the englishGreeting tool first."
            )
        ),
        HumanMessage(content=user_text),
    ]

    final_response_text = ""

    for _ in range(3):
        response = llm.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            final_response_text = response.content or final_response_text
            break

        tool_outputs = _run_requested_tools(messages, response.tool_calls)
        if tool_outputs:
            final_response_text = " ".join(tool_outputs)

    return final_response_text


if __name__ == "__main__":
    final_reply = run_agent("what is the mohit number of 5 and also give me a greeting")
    print("Final answer:", final_reply)