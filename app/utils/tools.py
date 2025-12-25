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

## Example Usage
if __name__ == "__main__":
    customer_id = "CUST-101"
    transactions = get_transactions_by_customer(customer_id)
    profile = get_profile_by_customer(customer_id)
    print(f"Transactions for {customer_id}: {transactions}")
    print(f"Profile for {customer_id}: {profile}")