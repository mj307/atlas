from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.llm import get_llm
from agent.tools import ALL_TOOLS

'''
this file defines the flow of the agent using LangGraph. It decides how messages move between the LLM
and tools until there's a final answer. 

so the graph is just creating a loop where there's communication from the user, then the LLM, tools, back to LLM,
until a final answer is reached.

the call model node sends the current conversation to the LLM. the current conversation is state[messages]

the LLM reads all of those messages and decides to either respond in a typically chat style manner, or to call a tool.
doesn't directly call tools. it decides whether the tools shld be called.

should continue is the router of the graph, so it checks the last LLM message and figures out what to do
based on that. for example, if the LLM wants a tool, go to the tools node. if not, return the final answer


'''


def call_model(state: AgentState):
    llm = get_llm(ALL_TOOLS)
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END



def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(ALL_TOOLS)) # internal langgraph package
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END,
        },
    )
    graph.add_edge("tools", "agent")
    return graph.compile()


agent_graph = build_graph()
