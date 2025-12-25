from pydantic import BaseModel, Field
from typing import Literal, Optional


class AlertInput(BaseModel):
    """
    Canonical Alert Input Model.
    This is the ONLY entry point into the agentic system.
    """
    alert_id: str
    scenario_code: str
    subject_id: str

    class Config:
        extra = "allow"   
