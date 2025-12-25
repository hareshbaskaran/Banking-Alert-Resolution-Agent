
from app.db.sops import SOPS
from langchain_core.messages import HumanMessage
from app.models.parser import AdjudicationResult
from app.models.agent import AgentState
from utils.llms import llm
import json


def adjudicator_node(state: AgentState):
    sop = SOPS[state["scenario_code"]]

    flat_findings = {
        k: v["value"] if isinstance(v, dict) else v
        for k, v in state["findings"].items()
    }

    prompt = f"""
You are the Adjudicator.

Apply SOP strictly. Do not infer beyond rules.

SOP:
{sop}

Findings:
{json.dumps(flat_findings, indent=2)}
"""

    result = llm.with_structured_output(
        AdjudicationResult
    ).invoke([HumanMessage(content=prompt)])

    print("\n================ FINAL DECISION ================")
    print(f"ALERT ID : {state['alert_id']}")
    print("DECISION :", result.decision)
    print("RISK     :", result.risk_level)
    print("RATIONALE:", result.rationale)
    print("================================================\n")

    state["next_agent"] = None
    state["next_agent_task"] = None
    return state
