from ptc1.models.llm import llm
from ptc1.graphs.state import AgentState


def chatbot_node(state: AgentState):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }