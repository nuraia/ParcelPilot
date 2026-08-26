import pandas as pd

file_path = "data/ParcelPilot_Assessment_Data.xlsx"

def get_order(order_id):

    orders = pd.read_excel(
        file_path, 
        sheet_name="orders"
    )

    result = orders[
        orders["order_id"].astype(str).str.upper() == order_id.upper()
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()

def get_account(account_id):

    accounts = pd.read_excel(
        file_path,
        sheet_name="accounts"
    )

    result = accounts[
        accounts["account_id"].astype(str).str.upper() == account_id.upper()
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()

def get_ticket(ticket_id):

    tickets = pd.read_excel(
        file_path,
        sheet_name="tickets"
    )

    result = tickets[
        tickets["ticket_id"].astype(str).str.upper() == ticket_id.upper()
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()

def investigate_order(order_id):

    order = get_order(order_id)
    if order is None:
        return {
            "found": False,
            "message": f"Order with ID '{order_id}' not found."
        }

    account = get_account(order["account_id"])

    if account is None:
        return {
            "found": False,
            "order": order,
            "message": (
                f"Order {order_id} found, but associated account with ID '{order['account_id']}' not found."
            )
        }

    return {
        "found": True,
        "order": order,
        "account": account
    }

if __name__ == "__main__":

    result = investigate_order("ORD-1001")

    print("\nINVESTIGATION RESULT:")
    print(result)
    # order = get_order("ORD-9999")
    # print("\nORDER:")
    # print(order)

    # account = get_account("ACCT-001")
    # print("\nACCOUNT:")
    # print(account)

    # ticket = get_ticket("TKT-501")
    # print("\nTICKET:")
    # print(ticket)
