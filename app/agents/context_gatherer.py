from app.utils.tools import get_profile_by_customer
from app.models.agent import AgentState
from app.models.parser import FindingResult
from app.utils.llms import llm

from langchain_core.messages import HumanMessage
import json

def context_gatherer_node(state: AgentState):
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

    result = llm.with_structured_output(
        FindingResult
    ).invoke([HumanMessage(content=prompt)])

    state["findings"][finding_name] = result.model_dump()

    res = {
        "findings": state["findings"],
        "next_agent": None,
        "next_agent_task": None
    }

    print("\n================ CONTEXT GATHERER RESULT ================ \n")
    print(f"Context Gatherer Agent Prompt: \n\n {prompt}")
    print(f"----------------------------------------------------- \n")
    print(f"Context Gatherer Agent Routing : \n\n {json.dumps({'next_agent': res['next_agent'], 'next_agent_task': res['next_agent_task']}, indent=2)}")
    print(f"Context Gatherer Agent Result: \n\n {json.dumps(res, indent=2)}")

    return res