from langchain_core.messages import HumanMessage
import json

from app.models.agent import AgentState
from app.models.parser import FindingResult
from app.utils.tools import get_transactions_by_customer
from app.utils.llms import llm



def investigator_node(state: AgentState):
    """
    AML Investigator Node.
    Analyzes transaction data to compute specific findings.
    Args:
        state (AgentState): Current state of the agent including next agent task.
    Returns:    
        dict: Updated findings along with next agent and task set to None.
    
    attributes:
        findings (dict): Updated findings with the new computed finding.
        next_agent (None): Set to None after task completion.
        next_agent_task (None): Set to None after task completion.
    """

    ## 1. Get Task Details
    task = state["next_agent_task"]
    finding_name = task["finding_name"]

    ## 2. Get Transaction Details for all the accounts the customer hold, Sorted by Timestamps
    transactions = get_transactions_by_customer(state["subject_id"])

    ## 3. Invoke LLM to compute the findings and update state
    prompt = f"""
You are an AML Investigator Agent.

ROLE:
Analyze TRANSACTION DATA only.

OBJECTIVE:
Compute finding: {finding_name}

TRANSACTION DATA:
{json.dumps(transactions, indent=2)}

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

    ## 4. Return Updated State with Findings
    return {
        "findings": state["findings"],
        "next_agent": None,
        "next_agent_task": None
    }

