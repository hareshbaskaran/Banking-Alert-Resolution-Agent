import json
from typing import Dict, Any, Optional, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.llms import llm
from db.sops import SOPS
from db.profiles import PROFILES
from db.transactions import TRANSACTIONS

from utils.prompts import ORCHESTRATOR_SCENARIOS




class AgentState(TypedDict):
    alert_id: str
    scenario_code: str
    subject_id: str
    subject_name: Optional[str]

    findings: Dict[str, Any]

    next_agent: Optional[str]
    next_agent_task: Optional[Dict[str, Any]]


class OrchestratorDecision(BaseModel):
    next_agent: Literal["Investigator", "ContextGatherer", "Adjudicator"]
    next_agent_task: Dict[str, Any] = Field(
        description="""
        Must contain:
        - finding_name: str (exact key to populate)
        - description: str (what to determine)
        """
    )


class AdjudicationResult(BaseModel):
    decision: Literal[
        "ESCALATE_SAR",
        "CLOSE_FALSE_POSITIVE",
        "REQUEST_INFO",
        "BLOCK_AND_SAR"
    ]
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    rationale: str


# ============================================================
# ORCHESTRATOR PROMPT
# ============================================================

ORCHESTRATOR_PROMPT = """
You are the ORCHESTRATOR (Hub) agent in an AML Alert Resolution System.

You control the investigation flow.

DO NOT:
- Compute metrics
- Apply SOP rules
- Use checklists mechanically

YOU MUST:
- Reason whether the investigation goal can already be resolved
- Decide which expert reduces uncertainty next

--------------------------------------------------
ALERT CONTEXT
--------------------------------------------------
Alert ID      : {alert_id}
Scenario Code : {scenario_code}

--------------------------------------------------
SCENARIO INVESTIGATION PLAN
--------------------------------------------------
{scenario_plan}

--------------------------------------------------
CURRENT FINDINGS
--------------------------------------------------
{current_findings}

--------------------------------------------------
AVAILABLE AGENTS
--------------------------------------------------
1. Investigator → Transaction behavior & metrics
2. ContextGatherer → KYC, profile, jurisdiction, sanctions
3. Adjudicator → Apply SOPs and conclude

--------------------------------------------------
OUTPUT FORMAT (STRICT JSON ONLY)
--------------------------------------------------
{{
  "next_agent": "<Investigator | ContextGatherer | Adjudicator>",
  "next_agent_task": {{
    "finding_name": "<EXACT finding key>",
    "description": "<What the agent must determine>"
  }}
}}
"""



# ============================================================
# ORCHESTRATOR NODE
# ============================================================

def orchestrator_node(state: AgentState):
    prompt = ORCHESTRATOR_PROMPT.format(
        alert_id=state["alert_id"],
        scenario_code=state["scenario_code"],
        scenario_plan=ORCHESTRATOR_SCENARIOS[state["scenario_code"]],
        current_findings=json.dumps(state["findings"], indent=2)
    )

    decision = llm.with_structured_output(
        OrchestratorDecision
    ).invoke([HumanMessage(content=prompt)])

    print(decision)

    return {
        "next_agent": decision.next_agent,
        "next_agent_task": decision.next_agent_task
    }


# ============================================================
# INVESTIGATOR AGENT (DUMMY)
# ============================================================

def investigator_node(state: AgentState):
    task = state["next_agent_task"]
    finding_name = task["finding_name"]

    # Dummy transactional output
    state["findings"][finding_name] = {
        "value": True,
        "source": "transactional_data",
        "dummy": True
    }

    return {
        "findings": state["findings"],
        "next_agent": None,
        "next_agent_task": None
    }


# ============================================================
# CONTEXT GATHERER AGENT (DUMMY)
# ============================================================

def context_gatherer_node(state: AgentState):
    task = state["next_agent_task"]
    finding_name = task["finding_name"]

    # Dummy profile output
    state["findings"][finding_name] = {
        "value": "Trader",
        "source": "profile_data",
        "dummy": True
    }

    return {
        "findings": state["findings"],
        "next_agent": None,
        "next_agent_task": None
    }


# ============================================================
# ADJUDICATOR NODE
# ============================================================

def adjudicator_node(state: AgentState):
    sop = SOPS[state["scenario_code"]]

    prompt = f"""
You are the Adjudicator.

Apply SOP strictly.

SOP:
{sop}

Findings:
{json.dumps(state["findings"], indent=2)}
"""

    result = llm.with_structured_output(
        AdjudicationResult
    ).invoke([HumanMessage(content=prompt)])

    state["next_agent"] = None
    state["next_agent_task"] = None

    print("\n================ FINAL DECISION ================")
    print(f"ALERT ID : {state['alert_id']}")
    print("DECISION :", result.decision)
    print("RISK     :", result.risk_level)
    print("RATIONALE:", result.rationale)
    print("================================================\n")

    return state


# ============================================================
# ROUTER
# ============================================================

def router(state: AgentState):
    return state["next_agent"]


# ============================================================
# LANGGRAPH CONSTRUCTION
# ============================================================

graph = StateGraph(AgentState)

graph.add_node("ORCHESTRATOR", orchestrator_node)
graph.add_node("INVESTIGATOR", investigator_node)
graph.add_node("CONTEXT", context_gatherer_node)
graph.add_node("ADJUDICATOR", adjudicator_node)

graph.add_edge(START, "ORCHESTRATOR")

graph.add_conditional_edges(
    "ORCHESTRATOR",
    router,
    {
        "Investigator": "INVESTIGATOR",
        "ContextGatherer": "CONTEXT",
        "Adjudicator": "ADJUDICATOR"
    }
)

graph.add_edge("INVESTIGATOR", "ORCHESTRATOR")
graph.add_edge("CONTEXT", "ORCHESTRATOR")
graph.add_edge("ADJUDICATOR", END)

app = graph.compile()


# ============================================================
# RUN
# ============================================================

def run():
    app.invoke({
        "alert_id": "ALT-001",
        "scenario_code": "A-001",
        "subject_id": "CUST-101",
        "subject_name": "Alice Trader",
        "findings": {},
        "next_agent": None,
        "next_agent_task": None
    })


if __name__ == "__main__":
    run()