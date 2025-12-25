from langchain_core.messages import HumanMessage
import json

from app.models.agent import AgentState
from app.models.parser import OrchestratorDecision
from app.utils.llms import llm
from app.models.prompts import ORCHESTRATOR_SCENARIOS, ORCHESTRATOR_PROMPT


def orchestrator_node(state: AgentState):
    """
    Orchestrator Node.
    Determines the next agent and task based on the current state.
    
    - Hub for routing between different agents.
    - Routing decisions are based on findings and scenario plan.
    - Uses MetaPrompts of different scenarios for decision making.
    - Returns the next agent and task to be executed.

    Args:
        state (AgentState): Current state of the agent including findings and scenario code.

    Returns:    
        dict: Next agent and task to be executed.
    
    attributes:
        next_agent (str): The identifier of the next agent to be invoked.
        next_agent_task (dict): The task details for the next agent.    
    """

    ## 1. Invoke LLM to determine next agent and task based on provided scenario plan and findings

    prompt = ORCHESTRATOR_PROMPT.format(
        alert_id=state["alert_id"],
        scenario_code=state["scenario_code"],
        scenario_plan=ORCHESTRATOR_SCENARIOS[state["scenario_code"]],
        current_findings=json.dumps(state["findings"], indent=2)
    )

    try:
        decision = llm.with_structured_output(
        OrchestratorDecision
    ).invoke([HumanMessage(content=prompt)])
    except Exception as e:
        raise RuntimeError(
            f"LLM failed to Structure or result invalid. Error: {e}"
        )

    ## 2. Return Next Agent and Task

    return {
        "next_agent": decision.next_agent,
        "next_agent_task": decision.next_agent_task
    }
