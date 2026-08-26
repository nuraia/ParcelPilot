from tools.data_lookup import (
    get_order,
    get_account,
    get_ticket
)

from tools.document_search import search_documents
from tools.decision_engine import decide_cancellation


def investigate_cancellation(order_id):

    # 1. Get order
    order = get_order(order_id)

    if not order:
        return {
            "success": False,
            "answer": f"Order {order_id} was not found."
        }

    # 2. Get account
    account = get_account(order["account_id"])

    if not account:
        return {
            "success": False,
            "answer": f"Account {order['account_id']} was not found."
        }

    # 3. Search relevant documents
    documents = search_documents(
        f"{account['account_name']} cancellation"
    )

    # 4. Apply business rules
    decision = decide_cancellation(
        order,
        account,
        documents
    )

    return {
        "success": True,
        "type": "cancellation",
        "order": order,
        "account": account,
        "documents": documents,
        "decision": decision
    }


def answer_question(question):

    question_lower = question.lower()

    # ==========================================
    # ESCALATION REQUEST
    # ==========================================

    if "escalate" in question_lower:

        ticket_id = None

        for word in question.upper().replace("?", "").split():

            if word.startswith("TKT-"):
                ticket_id = word.strip(".,!?")

        if not ticket_id:

            return {
                "answer": "Please provide a ticket ID, for example TKT-501.",
                "tools_used": []
            }

        ticket = get_ticket(ticket_id)

        if not ticket:

            return {
                "answer": f"Ticket {ticket_id} was not found.",
                "tools_used": ["get_ticket"]
            }

        return {
            "answer": (
                f"I found ticket {ticket_id}.\n\n"
                f"**Subject:** {ticket['subject']}\n"
                f"**Reason:** {ticket['description']}\n\n"
                "I recommend creating a P1 escalation because "
                "this appears to affect the customer's shipment creation.\n\n"
                "**No escalation has been created yet.** "
                "Please confirm if you want me to create it."
            ),
            "tools_used": ["get_ticket"],
            "pending_action": {
                "account_id": ticket["account_id"],
                "ticket_id": ticket_id,
                "reason": ticket["subject"],
                "priority": "P1"
            }
        }
    
    # ==========================================
    # CANCELLATION REQUEST
    # ==========================================

    if "cancel" in question_lower:

        # Find an order ID such as ORD-1001
        order_id = None

        for word in question.upper().replace("?", "").split():

            if word.startswith("ORD-"):
                order_id = word.strip(".,!?")

        if not order_id:

            return {
                "answer": "Please provide an order ID, for example ORD-1001.",
                "tools_used": []
            }

        # Run investigation
        result = investigate_cancellation(order_id)

        if not result["success"]:

            return {
                "answer": result["answer"],
                "tools_used": ["get_order"]
            }

        decision = result["decision"]

        answer = f"""
### Cancellation Decision

**Order:** {order_id}

**Customer:** {result['account']['account_name']}

**Status:** {result['order']['status']}

**Decision:** {decision['decision'].upper()}

**Cancellation fee:** INR {decision['fee_inr']}

### Why?

{decision['reason']}

### Source Authority

**Authority:** {decision['authority']}

**Source:** {decision['source']}

The customer-specific agreement takes precedence over
the general ParcelPilot cancellation SOP when the two
conflict.
"""

        return {
            "answer": answer,
            "tools_used": [
                "get_order",
                "get_account",
                "search_documents",
                "decide_cancellation"
            ],
            "action_available": decision["decision"] == "allowed",
            "order_id": order_id,
            "account_id": result["account"]["account_id"]
        }

    # ==========================================
    # TICKET REQUEST
    # ==========================================

    if "ticket" in question_lower:

        ticket_id = None

        for word in question.upper().replace("?", "").split():

            if word.startswith("TKT-"):
                ticket_id = word.strip(".,!?")

        if not ticket_id:

            return {
                "answer": "Please provide a ticket ID, for example TKT-501.",
                "tools_used": []
            }

        ticket = get_ticket(ticket_id)

        if not ticket:

            return {
                "answer": f"Ticket {ticket_id} was not found.",
                "tools_used": ["get_ticket"]
            }

        answer = f"""
### Ticket Investigation

**Ticket:** {ticket_id}

**Subject:** {ticket['subject']}

**Status:** {ticket['status']}

**Description:** {ticket['description']}

**Channel:** {ticket['channel']}

**Assigned to:** {ticket['assigned_to']}
"""

        return {
            "answer": answer,
            "tools_used": ["get_ticket"]
        }

    # ==========================================
    # DOCUMENT SEARCH
    # ==========================================

    documents = search_documents(question)

    if documents:

        best = documents[0]

        answer = f"""
### Relevant Information

**Source:** {best['file_name']}

**Authority:** {best['authority']}

**Status:** {best['status']}

{best['text'][:1500]}
"""

        return {
            "answer": answer,
            "tools_used": ["search_documents"]
        }

    # ==========================================
    # FALLBACK
    # ==========================================

    return {
        "answer": (
            "I could not confidently answer this question "
            "from the supplied ParcelPilot data. "
            "Please provide an order ID, ticket ID, or more details."
        ),
        "tools_used": []
    }

def prepare_escalation(account_id, ticket_id, reason, priority):

    return {
        "ready": True,
        "account_id": account_id,
        "ticket_id": ticket_id,
        "reason": reason,
        "priority": priority,
        "message": (
            f"I can create a {priority} escalation for ticket "
            f"{ticket_id} because: {reason}. "
            "Would you like me to create it?"
        )
    }

def ask_agent(question):
    """
    Main function used by the Streamlit application.
    """
    return answer_question(question)


# ==========================================
# COMMAND LINE TEST
# ==========================================

if __name__ == "__main__":

    pending_action = None

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        # Handle confirmation
        if pending_action:

            if question.lower().strip() in ["yes", "y", "confirm"]:

                from tools.action_tools import create_escalation

                result = create_escalation(
                    pending_action["account_id"],
                    pending_action["ticket_id"],
                    pending_action["reason"],
                    pending_action["priority"]
                )

                print("\nParcelPilot AI:")
                print("Escalation created successfully.")
                print(f"Escalation ID: {result['escalation_id']}")

                pending_action = None
                continue

            elif question.lower().strip() in ["no", "n", "cancel"]:

                print("\nParcelPilot AI:")
                print("No action was taken.")

                pending_action = None
                continue

        result = ask_agent(question)

        if result.get("pending_action"):
            pending_action = result["pending_action"]

        print("\nParcelPilot AI:")
        print(result["answer"])

        print("\nTools used:")

        for tool in result["tools_used"]:
            print(f"✓ {tool}")