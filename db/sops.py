SOPS = {
    "A-001": 
""" 
IF prior_velocity_exists == FALSE
AND business_justification_present == FALSE
THEN
   DECISION = ESCALATE_SAR
   RISK_LEVEL = HIGH
ELSE
   DECISION = CLOSE_FALSE_POSITIVE
   RISK_LEVEL = LOW
""",
    "A-002": 
    """ 
IF aggregate_cash_amount > 28000
THEN
   DECISION = ESCALATE_SAR
   RISK_LEVEL = HIGH

ELSE IF geographically_diverse_deposits >= 2
THEN
   DECISION = REQUEST_INFO
   RISK_LEVEL = MEDIUM

ELSE
   DECISION = CLOSE_FALSE_POSITIVE
   RISK_LEVEL = LOW

    """,
    "A-003": 
    """ 
IF occupation_category IN {"Teacher", "Student"}
THEN
   DECISION = ESCALATE_SAR
   RISK_LEVEL = HIGH

ELSE IF occupation_category IN {"Trader", "Jeweler"}
THEN
   DECISION = CLOSE_FALSE_POSITIVE
   RISK_LEVEL = LOW

ELSE
   DECISION = ESCALATE_SAR
   RISK_LEVEL = MEDIUM
    """,
    "A-004": 
    """ 
IF counterparty_sanctioned == TRUE
   OR high_risk_jurisdiction == TRUE
THEN
   DECISION = BLOCK_AND_SAR
   RISK_LEVEL = CRITICAL

ELSE
   DECISION = CLOSE_FALSE_POSITIVE
   RISK_LEVEL = LOW

    """,
    "A-005": 
    """
 IF kyc_risk_level == "High"
   AND suspicious_withdrawal == TRUE
THEN
   DECISION = ESCALATE_SAR
   RISK_LEVEL = HIGH

ELSE
   DECISION = REQUEST_INFO
   RISK_LEVEL = MEDIUM
"""
}