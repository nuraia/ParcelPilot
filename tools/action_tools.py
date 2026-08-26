from datetime import datetime

ESCALATIONS = []

def create_escalation(
    account_id,
    ticket_id,
    reason,
    priority
):
     """
    Create a support escalation.

    This is a mocked state-changing action for the assessment.
    """

     escalation = {
        "escalation_id": f"ESC-{len(ESCALATIONS) + 1:04d}",
        "account_id": account_id,
        "ticket_id": ticket_id,
        "reason": reason,
        "priority": priority,
        "created_at": datetime.now(),
        "status": "open"
     }

     ESCALATIONS.append(escalation)

     return escalation