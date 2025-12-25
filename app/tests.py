from app.graph import workflow
from app.models.input import AlertInput

TEST_CASES = [

        # ======================================================
        # TEST CASE 1 — A-001 : Velocity Spike (Layering)
        # ======================================================
        # WHY THIS CASE:
        # - Customer is a Trader with legitimate wholesale activity
        # - High transaction velocity is EXPECTED for this profile
        #
        # EXPECTED BEHAVIOR:
        # - Investigator finds no prior velocity spike
        # - ContextGatherer confirms business justification
        # - SOP resolves as FALSE POSITIVE
        #
        # EXPECTED ACTION:
        # - Alert Closure
        #
        {
            "alert_id": "ALT-001-A",
            "scenario_code": "A-001",
            "subject_id": "CUST-101",
            "expected_action": "ALERT_CLOSURE"
        },

        # ======================================================
        # TEST CASE 2 — A-002 : Below-Threshold Structuring
        # ======================================================
        # WHY THIS CASE:
        # - Cash business deposits just below reporting thresholds
        # - Deposits span multiple geographies
        #
        # EXPECTED BEHAVIOR:
        # - Investigator computes aggregate cash > threshold
        # - Geographic diversity is detected
        # - SOP triggers escalation for SAR
        #
        # EXPECTED ACTION:
        # - SAR Preparation
        #
        {
            "alert_id": "ALT-002-A",
            "scenario_code": "A-002",
            "subject_id": "CUST-102",
            "expected_action": "SAR_PREPARATION"
        },

        # ======================================================
        # TEST CASE 3 — A-003 : KYC Inconsistency
        # ======================================================
        # WHY THIS CASE:
        # - Teacher sends large wire to Precious Metals merchant
        # - Clear mismatch between occupation and transaction type
        #
        # EXPECTED BEHAVIOR:
        # - ContextGatherer identifies occupation = Teacher
        # - SOP mandates escalation
        #
        # EXPECTED ACTION:
        # - SAR Preparation
        #
        {
            "alert_id": "ALT-003-A",
            "scenario_code": "A-003",
            "subject_id": "CUST-103",
            "expected_action": "SAR_PREPARATION"
        },

        # ======================================================
        # TEST CASE 4 — A-004 : Sanctions / High-Risk Jurisdiction
        # ======================================================
        # WHY THIS CASE:
        # - High-risk industry (Jeweler)
        # - BUT no sanctions flag and no sanctioned counterparty
        #
        # EXPECTED BEHAVIOR:
        # - ContextGatherer confirms no sanctions exposure
        # - Investigator finds no high-risk jurisdiction hit
        # - SOP resolves as FALSE POSITIVE
        #
        # EXPECTED ACTION:
        # - Alert Closure
        #
        {
            "alert_id": "ALT-004-B",
            "scenario_code": "A-004",
            "subject_id": "CUST-104",
            "expected_action": "ALERT_CLOSURE"
        },

        # ======================================================
        # TEST CASE 5 — A-005 : Dormant Account Activation
        # ======================================================
        # WHY THIS CASE:
        # - Student account (low inherent risk)
        # - No large inbound wire
        # - No international ATM withdrawal
        #
        # EXPECTED BEHAVIOR:
        # - ContextGatherer confirms Low KYC risk
        # - Investigator finds no suspicious withdrawal
        # - SOP requests clarification instead of escalation
        #
        # EXPECTED ACTION:
        # - RFI (Request For Information)
        #
        {
            "alert_id": "ALT-005-B",
            "scenario_code": "A-005",
            "subject_id": "CUST-105",
            "expected_action": "RFI"
        },
    ]


def run_all_tests():
    """Run all predefined test cases through the workflow."""
    
    for idx, test in enumerate(TEST_CASES):
        alert = AlertInput(**test)

        print(f"\n\n===================== TEST CASE {idx+1} =====================")
        print(f"NEW ALERT : {alert.alert_id}")
        print(f"SCENARIO  : {alert.scenario_code}")
        print(f"SUBJECT   : {alert.subject_id}")

        if alert.expected_action:
            print("\n--- EXPECTED ACTION -----------------------------")
            print("EXPECTED ACTION :", alert.expected_action)
            print("------------------------------------------------\n")

        workflow.invoke({
            "alert_id": alert.alert_id,
            "scenario_code": alert.scenario_code,
            "subject_id": alert.subject_id,
            "findings": {},
            "next_agent": None,
            "next_agent_task": None,
            "adjudication": None
        })




