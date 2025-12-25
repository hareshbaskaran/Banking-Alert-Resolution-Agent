from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

class OrchestratorDecision(BaseModel):
    next_agent: Literal["Investigator", "ContextGatherer", "Adjudicator"]
    next_agent_task: Dict[str, Any] = Field(
        description="""
        Must contain:
        - finding_name: exact key to populate
        - description: what the agent must determine
        """
    ) ## exact keys induces confusion and LLMs understand with proper prompts

class FindingResult(BaseModel):
    value: Any
    explanation: str
    source: Literal["transactional_data", "profile_data"]

class AdjudicationResult(BaseModel):
    decision: Literal[
        "ESCALATE_SAR",
        "CLOSE_FALSE_POSITIVE",
        "REQUEST_INFO",
        "BLOCK_AND_SAR"
    ]
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    rationale: str



