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
```
## 2. Create a virtual environment
```bash
python3 -m venv .venv
```

macOS / Linux
```bash
source .venv/bin/activate
```

Windows
```bash
.venv\Scripts\activate
```
## 3. Install dependencies
```bash
pip install -r requirements.txt
```
## 4. Configure the LLM
The project can use a local Ollama model to avoid dependency on paid API
quotas.
Make sure Ollama is running and the required model is available.
## 5. Build the document index
The PDF ingestion script extracts text from the documents in data/ and
creates:
```bash
data/document_index.json
```
Run:
```bash
python ingestion/build_index.py
```
## 6. Run the Streamlit application
```bash
streamlit run app.py
```
The application will open in the browser.
