from app.utils.tools import get_profile_by_customer
from app.models.agent import AgentState
from app.models.parser import FindingResult
from app.utils.llms import llm

from langchain_core.messages import HumanMessage
import json

def context_gatherer_node(state: AgentState):
    """
    Context Gatherer Node.
    Analyzes customer profile/KYC data to compute specific findings.

    Args:
        state (AgentState): Current state of the agent including next agent task.
    Returns:    
        dict: Updated findings along with next agent and task set to None.
    
    attributes:
        findings (dict): Updated findings with the new computed finding.
        next_agent (None): Set to None after task completion.
        next_agent_task (None): Set to None after task completion.
    """

    task = state["next_agent_task"]
    finding_name = task["finding_name"]

    profile = get_profile_by_customer(state["subject_id"])

    prompt = f"""
You are a Context Gatherer Agent.

ROLE:
Analyze CUSTOMER PROFILE / KYC data only.

OBJECTIVE:
Compute finding: {finding_name}

PROFILE DATA:
{json.dumps(profile, indent=2)}

Return a structured result.
"""


    try:
        result = llm.with_structured_output(
        FindingResult
    ).invoke([HumanMessage(content=prompt)])
        state["findings"][finding_name] = result.model_dump()
    except Exception as e:
        raise RuntimeError(
            f"Failed to load finding '{finding_name}'. "
            f"LLM failed to Structure or result invalid. Error: {e}"
        )

    return {
        "findings": state["findings"],
        "next_agent": None,
        "next_agent_task": None
    }