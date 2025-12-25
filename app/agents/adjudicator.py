from app.db.sops import SOPS
from app.models.parser import AdjudicationResult
from app.models.agent import AgentState
from app.utils.helpers import extract_finding_values
from app.utils.llms import llm

from langchain_core.messages import HumanMessage
import json


def adjudicator_node(state: AgentState):
    """
    Adjudicator Node.
    Applies the Standard Operating Procedure (SOP) based on the scenario code
    and the collected findings to make a final adjudication.
    Args:
        state (AgentState): Current state of the agent including findings.
    Returns:
        AgentState: Updated state with adjudication result.
    """

    ## 1. Get SOP based on scenario code and Map findings to simple key-value pairs
    sop = SOPS[state["scenario_code"]]
    findings = extract_finding_values(state["findings"])

    ## 2. Invoke LLM to get Adjudication Result
    result = llm.with_structured_output(
        AdjudicationResult
    ).invoke([HumanMessage(content=f"""
You are the Adjudicator.

Apply SOP strictly. Do NOT infer beyond rules.

SOP:
{sop}

Findings:
{json.dumps(findings, indent=2)}
""")])

    ## 3. Update State with Adjudication Result
    
    state["adjudication"] = result.model_dump()
    state["next_agent"] = None
    state["next_agent_task"] = None

    return state
