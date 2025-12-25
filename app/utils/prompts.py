ORCHESTRATOR_SCENARIOS = {

    "A-001": """
SCENARIO: A-001 Velocity Spike (Layering)

GOAL:
Determine whether the detected velocity spike represents
suspicious activity or an expected business cycle.

FINDINGS REQUIRED:

1. prior_velocity_exists
   - Criteria:
     Check if another velocity spike occurred BEFORE the alerted spike
     within the SAME 90-day lookback window.
   - Metriculation:
     Boolean → TRUE if ≥1 earlier 48-hour window had ≥5 txns > $5k.
   - Datatype:
     Boolean
   - Source:
     Transactional Data

2. business_justification_present
   - Criteria:
     Customer occupation and source of funds logically explain
     high outbound velocity reported in the alert.
   - Metriculation:
     Boolean → TRUE if occupation ∈ {Trader, Business Owner, Jeweler}
   - Datatype:
     Boolean
   - Source:
     Profile Data

STOP CONDITION:
Proceed to adjudication when both findings are available.
""",

    "A-002": """
SCENARIO: A-002 Below-Threshold Structuring

GOAL:
Determine whether repeated near-threshold cash deposits
constitute structuring or legitimate business activity.

FINDINGS REQUIRED:

1. aggregate_cash_amount
   - Criteria:
     Sum of all cash deposits (9k–9.9k range) across ALL linked accounts
     within 7 days.
   - Metriculation:
     Numeric sum (USD)
   - Datatype:
     Float
   - Source:
     Transactional Data

2. geographically_diverse_deposits
    - Criteria:
      Count the number of distinct countries from which cash deposits were made within the 7-day window.
    - Metriculation:
      Integer count of unique country codes.
    - Datatype:
      Integer
    - Source:
      Transactional Data

STOP CONDITION:
Proceed to adjudication when both findings are available.
""",

    "A-003": """
SCENARIO: A-003 KYC Inconsistency

GOAL:
Determine whether the customer profile aligns with
the nature of the transaction.

FINDINGS REQUIRED:

1. occupation_category
   - Criteria:
     Identify customer's declared occupation.
   - Metriculation:
     Enum → {Trader, Jeweler, Teacher, Student, Other}
   - Datatype:
     String
   - Source:
     Profile Data

STOP CONDITION:
Proceed to adjudication when finding is available.
""",

    "A-004": """
SCENARIO: A-004 Sanctions List Hit (Minor Match)

GOAL:
Determine whether the counterparty involved
is a true sanctions match.

FINDINGS REQUIRED:

1. counterparty_sanctioned
   - Criteria:
     Counterparty has sanctioned flag TRUE.
   - Metriculation:
     Boolean
   - Datatype:
     Boolean
   - Source:
     Profile Data

2. high_risk_jurisdiction
   - Criteria:
     Counterparty country ∈ sanctioned or high-risk list.
   - Metriculation:
     Boolean
   - Datatype:
     Boolean
   - Source:
     Transactional Data

STOP CONDITION:
Proceed to adjudication when both findings are available.
""",

    "A-005": """
SCENARIO: A-005 Dormant Account Activation

GOAL:
Determine whether reactivation of a dormant account
poses money laundering risk.

FINDINGS REQUIRED:

1. kyc_risk_level
   - Criteria:
     Customer risk rating from KYC profile.
   - Metriculation:
     Enum → {Low, Medium, High}
   - Datatype:
     String
   - Source:
     Profile Data

2. suspicious_withdrawal
   - Criteria:
     Large International ATM withdrawal (> $10k) shortly after inbound wire of (>= $15k).
   - Metriculation:
     Boolean
   - Datatype:
     Boolean
   - Source:
     Transactional Data

STOP CONDITION:
Proceed to adjudication when all findings are available.
"""
}


ORCHESTRATOR_PROMPT = """
You are the ORCHESTRATOR (Hub) agent in an AML Alert Resolution System.

ROLE:
- Control investigation flow
- Decide which expert to call next
- NEVER compute metrics
- NEVER apply SOP rules

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
DECISION RULE
--------------------------------------------------
If all findings required by the scenario are present → Adjudicator
Else choose ONE agent that best reduces uncertainty.

OUTPUT STRICT JSON ONLY.
"""

