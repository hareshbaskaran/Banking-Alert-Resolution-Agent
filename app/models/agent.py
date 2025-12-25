from typing import Dict, Any, Optional
from typing_extensions import TypedDict

class AgentState(TypedDict):
    alert_id: str
    scenario_code: str
    subject_id: str
    subject_name: Optional[str]

    findings: Dict[str, Any]

    next_agent: Optional[str]
    next_agent_task: Optional[Dict[str, Any]]