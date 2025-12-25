from app.models.agent import AgentState
from app.utils.tools import (
    rfi_tool,
    ivr_tool, ## IVR TOOL NOT NEEDED FOR EITHER OF DECISIONS CURRENTLY
    sar_preparer_tool,
    alert_closure_tool
)

def aem_node(state: AgentState):
    """
    Action Executor Module (AEM) Node.
    Executes actions based on adjudication results.

    Args:
        state (AgentState): Current state of the agent including adjudication results.
    Returns:
        AgentState: Updated state after executing the action.
    """

    ## 1. Get Adjudication Result
    adjudication = state.get("adjudication")

    if adjudication is None:
        raise RuntimeError("AEM invoked without adjudication result")

    ## 2. Parse Decision to State Memory
    decision = adjudication["decision"]
    rationale = adjudication.get("rationale", "")

    alert_id = state["alert_id"]
    subject_name = state.get("subject_name", "Unknown Customer")

    ## 3. Execute Action Based on Decision
    if decision == "REQUEST_INFO":
        rfi_tool(customer_name=subject_name)


    elif decision == "ESCALATE_SAR":
        sar_preparer_tool(
            alert_id=alert_id,
            rationale=rationale
        )

    elif decision == "BLOCK_AND_SAR":
        sar_preparer_tool(
            alert_id=alert_id,
            rationale=rationale
        )

    elif decision == "CLOSE_FALSE_POSITIVE":
        alert_closure_tool(alert_id=alert_id)

    else:
        raise ValueError(f"Unsupported adjudication decision: {decision}")

    return state
