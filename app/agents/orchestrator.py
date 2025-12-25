from langchain_core.messages import HumanMessage
import json

from app.models.agent import AgentState
from app.models.parser import OrchestratorDecision
from app.utils.llms import llm
from app.utils.prompts import ORCHESTRATOR_SCENARIOS, ORCHESTRATOR_PROMPT


def orchestrator_node(state: AgentState):
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

    res = {
        "next_agent": decision.next_agent,
        "next_agent_task": decision.next_agent_task
    }

    print("\n================ Orchestrator RESULT ================ \n")
    print(f"Orchestrator Agent Prompt: \n\n {prompt}")
    print(f"----------------------------------------------------- \n")
    print(f"Orchestrator Agent Routing : \n\n {json.dumps({'next_agent': res['next_agent'], 'next_agent_task': res['next_agent_task']}, indent=2)}")
    print(f"Orchestrator Agent Result: \n\n {json.dumps(res, indent=2)}")

    return res
