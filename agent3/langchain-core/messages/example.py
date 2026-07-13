"""Tiny agent example that shows how LangChain messages become conversation state.

The goal here is not to build a production agent. The goal is to make the role of
each message type obvious:

- `SystemMessage` defines the agent behavior.
- `HumanMessage` stores the user's input.
- `AIMessage` stores the agent's reply.
- `ToolMessage` stores a tool result that the agent can read later.
"""

from dataclasses import dataclass, field

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


def add_numbers_tool(expression: str) -> str:
    """Very small tool used by the demo agent."""
    numbers = [int(part) for part in expression.split() if part.isdigit()]
    total = sum(numbers)
    return f"sum={total} from numbers={numbers}"


@dataclass
class TinyAgent:
    """A minimal agent that keeps the full conversation in `messages`."""

    messages: list = field(default_factory=list)
    tool_call_id: int = 0

    def __post_init__(self) -> None:
        self.messages.append(
            SystemMessage(
                content=(
                    "You are a tiny teaching agent. Keep replies short and explain "
                    "which message types were used when a tool is involved."
                )
            )
        )

    def ask(self, user_text: str) -> AIMessage:
        """Add user input, optionally call a tool, then append the assistant reply."""
        self.messages.append(HumanMessage(content=user_text))

        if "sum" in user_text.lower() or "+" in user_text:
            self.tool_call_id += 1
            tool_result = add_numbers_tool(user_text)
            self.messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=f"tool_call_{self.tool_call_id}",
                )
            )
            reply = (
                "I used a ToolMessage to store the calculation result, then I used it "
                "to create this AIMessage reply."
            )
        else:
            reply = (
                "I only needed the existing messages, so I responded directly with an AIMessage."
            )

        ai_message = AIMessage(content=reply)
        self.messages.append(ai_message)
        return ai_message

    def print_transcript(self) -> None:
        """Show how the conversation is stored."""
        print("Conversation transcript:")
        for index, message in enumerate(self.messages, start=1):
            print(f"{index}. {message.__class__.__name__}: {message.content}")


def main() -> None:
    agent = TinyAgent()

    print("First turn: no tool needed")
    print(agent.ask("Explain how messages work in an agent." ).content)

    print("\nSecond turn: tool used")
    print(agent.ask("Please sum 3 7 10 for me.").content)

    print()
    agent.print_transcript()


if __name__ == "__main__":
    main()