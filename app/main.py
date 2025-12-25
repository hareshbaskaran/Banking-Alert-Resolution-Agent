from app.tests import run_all_tests
from app.graph import workflow
from app.models.input import AlertInput


def run_single_from_cli():
    """
    CLI-driven single alert execution.

    This simulates a real analyst intake screen:
    - Explicit prompts
    - No silent input modification
    - Strict Pydantic validation
    """

    print("\nEnter Alert Details")
    print("-------------------")

    alert_id = input("Enter Alert ID (e.g., ALT-001-A): ")
    scenario_code = input("Enter Scenario Code (e.g., A-001): ")
    subject_id = input("Enter Subject ID (e.g., CUST-101): ")

    # Pydantic validation happens here
    alert = AlertInput(
        alert_id=alert_id,
        scenario_code=scenario_code,
        subject_id=subject_id
    )

    print("\n--- VALIDATED INPUT -----------------------------")
    print(f"Alert ID  : {alert.alert_id}")
    print(f"Scenario  : {alert.scenario_code}")
    print(f"Subject   : {alert.subject_id}")
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


def main():
    print("\nAgentic AML Alert Resolution System")
    print("----------------------------------")
    print("1. Run all predefined test cases")
    print("2. Run a single alert (manual input)")
    print("----------------------------------")

    choice = input("Select option (1 or 2): ")

    if choice == "1":
        run_all_tests()
    elif choice == "2":
        run_single_from_cli()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
