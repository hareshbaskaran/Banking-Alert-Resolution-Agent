from langchain_core.messages import HumanMessage
import json

from app.models.agent import AgentState
from app.models.parser import FindingResult
from app.utils.tools import get_transactions_by_customer
from app.utils.llms import llm



def investigator_node(state: AgentState):
    task = state["next_agent_task"]
    finding_name = task["finding_name"]

    transactions = get_transactions_by_customer(state["subject_id"])

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

    res = {
        "findings": state["findings"],
        "next_agent": None,
        "next_agent_task": None
    }
    print("\n================ INVESTIGATOR RESULT ================ \n")
    print(f"Investigator Agent Prompt: \n\n {prompt}")
    print(f"----------------------------------------------------- \n")
    print(f"Investigator Agent Routing : \n\n {json.dumps({'next_agent': res['next_agent'], 'next_agent_task': res['next_agent_task']}, indent=2)}")
    print(f"Investigator Agent Result: \n\n {json.dumps(res, indent=2)}")

    return res
