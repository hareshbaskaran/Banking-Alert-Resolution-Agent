from app.db.profiles import PROFILES
from app.db.transactions import TRANSACTIONS

def get_transactions_by_customer(customer_id: str):
    return sorted(
        [t for t in TRANSACTIONS if t["customer_id"] == customer_id],
        key=lambda x: x["timestamp"]
    )

def get_profile_by_customer(customer_id: str):
    for p in PROFILES:
        if p["customer_id"] == customer_id:
            return p
    return None


def rfi_tool(customer_name: str):
    print(
        f"Action Executed: RFI via Email. "
        f"Drafted message for Customer: {customer_name} requesting Source of Funds."
    )


def ivr_tool():
    print(
        "Action Executed: IVR Call Initiated. "
        "Script ID 3 used for simple verification. "
        "Awaiting Customer Response..."
    )


def sar_preparer_tool(alert_id: str, rationale: str):
    print(
        f"Action Executed: SAR Preparer Module Activated. "
        f"Case {alert_id} pre-populated and routed to Human Queue. "
        f"Rationale: {rationale}."
    )


def alert_closure_tool(alert_id: str):
    print(
        f"Action Executed: Alert {alert_id} closed as False Positive."
    )


## Example Usage
if __name__ == "__main__":
    customer_id = "CUST-101"
    transactions = get_transactions_by_customer(customer_id)
    profile = get_profile_by_customer(customer_id)
    print(f"Transactions for {customer_id}: {transactions}")
    print(f"Profile for {customer_id}: {profile}")