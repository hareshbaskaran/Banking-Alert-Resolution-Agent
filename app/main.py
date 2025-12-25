from app.graph import workflow

def run():
    alerts = [
        # {
        #     "alert_id": "ALT-001",
        #     "scenario_code": "A-001",
        #     "subject_id": "CUST-101",   # Trader without prior velocity spike
        #     "subject_name": "Alice Trader"
        # },

        # {
        #     "alert_id": "ALT-002",
        #     "scenario_code": "A-002",
        #     "subject_id": "CUST-102",   # Cash business with linked accounts
        #     "subject_name": "Raj Retail"
        # },
        # {
        #     "alert_id": "ALT-003",
        #     "scenario_code": "A-003",
        #     "subject_id": "CUST-103",   # Teacher wiring to metals
        #     "subject_name": "Charlie Teach"
        # },
        # {
        #     "alert_id": "ALT-004",
        #     "scenario_code": "A-004",
        #     "subject_id": "CUST-108",   # Sanctioned counterparty
        #     "subject_name": "Unknown Entity"
        # },
        # {
        #     "alert_id": "ALT-005",
        #     "scenario_code": "A-005",
        #     "subject_id": "CUST-109",   # Dormant account reactivation
        #     "subject_name": "Elder Retiree"
        # }
    ]

    for alert in alerts:
        print("\n\n================ NEW ALERT =====================")
        workflow.invoke({
            "alert_id": alert["alert_id"],
            "scenario_code": alert["scenario_code"],
            "subject_id": alert["subject_id"],
            "subject_name": alert["subject_name"],
            "findings": {},
            "next_agent": None,
            "next_agent_task": None
        })


if __name__ == "__main__":
    run()
