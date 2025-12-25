from langgraph.graph import StateGraph, START, END
from app.agents.orchestrator import orchestrator_node
from app.agents.investigation import investigator_node
from app.agents.context_gatherer import context_gatherer_node
from app.agents.adjudicator import adjudicator_node
from app.agents.action_executor import aem_node

from app.models.agent import AgentState


def router(state: AgentState):
    return state["next_agent"]


exec_graph = StateGraph(AgentState)
exec_graph.add_node("ORCHESTRATOR", orchestrator_node)
exec_graph.add_node("INVESTIGATOR", investigator_node)
exec_graph.add_node("CONTEXT", context_gatherer_node)
exec_graph.add_node("ADJUDICATOR", adjudicator_node)
exec_graph.add_node("AEM", aem_node)
exec_graph.add_edge(START, "ORCHESTRATOR")

exec_graph.add_conditional_edges(
    "ORCHESTRATOR",
    router,
    {
        "Investigator": "INVESTIGATOR",
        "ContextGatherer": "CONTEXT",
        "Adjudicator": "ADJUDICATOR"
    }
)

exec_graph.add_edge("INVESTIGATOR", "ORCHESTRATOR")
exec_graph.add_edge("CONTEXT", "ORCHESTRATOR")
exec_graph.add_edge("ADJUDICATOR", "AEM")
exec_graph.add_edge("AEM", END)

workflow = exec_graph.compile()
