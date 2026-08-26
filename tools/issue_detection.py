import pandas as pd 
from pathlib import Path
from collections import Counter

FILE_PATH = Path("data/ParcelPilot_Assessment_Data.xlsx")

def load_tickets():
    return pd.read_excel(
        FILE_PATH,
        sheet_name="tickets"
    )

def detect_urgent_tickets():
    tickets = load_tickets()

    urgent = []

    for _, ticket in tickets.iterrows():

        text = (
            str(ticket["subject"]) + " " +
            str(ticket["description"])
        ).lower()

        priority = None

        if any(word in text for word in [
            "outage",
            "http 500",
            "every user",
            "all users",
            "all shipment"
        ]):
            priority = "P1"

        elif any(word in text for word in [
            "fails",
            "failure",
            "error",
            "cannot"
        ]):
            priority = "P2"

        if priority:

            urgent.append({
                "ticket_id": ticket["ticket_id"],
                "account_id": ticket["account_id"],
                "subject": ticket["subject"],
                "priority": priority,
                "status": ticket["status"]
            })
    return urgent

def detect_recurring_issues():
    tickets = load_tickets()

    subjects = []

    for _, ticket in tickets.iterrows():
        subject = str(ticket["subject"]).lower()

        if "shipment" in subject:
            subjects.append("shipment issue")

        elif "upload" in subject:
            subjects.append("upload issue")

        elif "billing" in subject:
            subjects.append("billing issue")

        else: 
            subjects.append("other")

    counts = Counter(subjects)

    return counts

def generate_issue_report():

    urgent = detect_urgent_tickets()
    recurring = detect_recurring_issues()

    return {
        "urgent_tickets": urgent,
        "recurring_issues": dict(recurring)
    }

if __name__ == "__main__":

    report = generate_issue_report()

    print("\n" + "=" * 60)
    print("PARCELPILOT PROACTIVE ISSUE DETECTION")
    print("=" * 60)

    print("\nURGENT TICKETS")
    print("-" * 60)

    for ticket in report["urgent_tickets"]:
        print(
            f"{ticket['priority']} | "
            f"{ticket['ticket_id']} | "
            f"{ticket['account_id']} | "
            f"{ticket['subject']}"
        )

    print("\nRECURRING ISSUE PATTERNS")
    print("-" * 60)

    for issue, count in report["recurring_issues"].items():
         print(f"{issue}: {count}")
