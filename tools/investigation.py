from data_lookup import get_order, get_account
from document_search import search_documents


def investigate_cancellation(order_id):

    # 1. Find order
    order = get_order(order_id)

    if order is None:
        return {
            "success": False,
            "error": f"Order {order_id} was not found."
        }

    # 2. Find account
    account = get_account(order["account_id"])

    if account is None:
        return {
            "success": False,
            "error": f"Account {order['account_id']} was not found."
        }

    # 3. Find relevant documents
    documents = search_documents(
        "cancellation fee booked pickup",
        account_id=order["account_id"]
    )

    # 4. Return investigation package
    return {
        "success": True,
        "order": order,
        "account": account,
        "documents": documents
    }


if __name__ == "__main__":

    result = investigate_cancellation("ORD-1001")

    print("\nINVESTIGATION RESULT")
    print("=" * 70)

    if not result["success"]:
        print(result["error"])

    else:

        order = result["order"]
        account = result["account"]

        print("Order:", order["order_id"])
        print("Account:", account["account_name"])
        print("Status:", order["status"])

        print("\nDocuments found:")

        for document in result["documents"]:
            print(
                "-",
                document["file_name"],
                "| Authority:",
                document["authority"],
                "| Score:",
                document["score"]
            )