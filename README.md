# ParcelPilot AI Copilot

An AI-powered customer support copilot for ParcelPilot's logistics operations.

The system investigates customer questions using structured order/account data,
company policies, customer-specific agreements, and operational tools. It can
make policy-based decisions, investigate tickets, detect recurring issues, and
create escalations only after confirmation.

---

## Features

- Order and account lookup
- Customer-specific policy investigation
- Document search across current policies, SOPs, and agreements
- Cancellation decision engine
- Service-credit decision engine
- Ticket investigation
- P1/P2 escalation workflow with confirmation
- Proactive issue detection
- Streamlit-based support UI
- Source and authority tracking for decisions

---

# Setup

## Requirements

- Python 3.10+
- pip
- Git
- Streamlit
- An LLM provider or local Ollama model

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ParcelPilot
