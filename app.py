import streamlit as st
from agent import ask_agent
from tools.issue_detection import generate_issue_report
from tools.action_tools import create_escalation

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None
# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="ParcelPilot AI Copilot",
    page_icon="📦",
    layout="centered"
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("ParcelPilot AI Copilot")
st.caption(
    "AI-powered customer support investigation"
)

st.divider()

# ---------------------------------------------------------
# OPERATIONS DASHBOARD
# ---------------------------------------------------------

st.header("🚨 Operations Dashboard")

if st.button("Run Issue Detection"):

    report = generate_issue_report()

    # -----------------------------
    # Urgent Tickets
    # -----------------------------

    st.subheader("Urgent Tickets")

    if not report["urgent_tickets"]:
        st.success("No urgent tickets detected.")

    else:

        for ticket in report["urgent_tickets"]:

             with st.container(border=True):

                st.markdown(
                    f"### {ticket['priority']} — {ticket['ticket_id']}"
                )

                st.write(
                    f"**Account:** {ticket['account_id']}"
                )

                st.write(
                    f"**Issue:** {ticket['subject']}"
                )

    # -----------------------------
    # Recurring Issues
    # -----------------------------

    st.subheader("Recurring Issues")

    for issue, count in report["recurring_issues"].items():

         st.write(
            f"**{issue.title()}:** {count} ticket(s)"
        )
    st.divider()


# ---------------------------------------------------------
# CHATBOT
# ---------------------------------------------------------

st.header("💬 Support Assistant")


st.write(
    "Ask about orders, accounts, tickets, policies, "
    "cancellations, service credits, or product issues."
)

question = st.chat_input("Ask ParcelPilot Support...")

# ---------------------------------------------------------
# HANDLE CHAT
# ---------------------------------------------------------

if question:

    # User message
    with st.chat_message("user"):
        st.write(question)

    # -------------------------------------------------
    # HANDLE CONFIRMATION
    # -------------------------------------------------

    if (question.strip().lower() in ["yes", "y", "confirm"]
        and st.session_state.pending_action
    ):

        pending = st.session_state.pending_action

        escalation = create_escalation(
            account_id=pending["account_id"],
            ticket_id=pending["ticket_id"],
            reason=pending["reason"],
            priority=pending["priority"]
        )

        result = {
            "answer": f"""
    ### Escalation Created Successfully

    **Escalation ID:** {escalation['escalation_id']}

    **Ticket:** {escalation['ticket_id']}

    **Priority:** {escalation['priority']}

    **Status:** {escalation['status']}
    """,
            "tools_used": ["create_escalation"]
        }

        # Clear pending action
        st.session_state.pending_action = None

    else:

        # Normal agent request
        with st.spinner("Investigating..."):
            result = ask_agent(question)

    # -------------------------------------------------
    # DISPLAY ASSISTANT RESPONSE
    # -------------------------------------------------

    with st.chat_message("assistant"):

        if isinstance(result, dict):

            answer = result.get("answer")

            if answer:
                st.markdown(answer)

            # -----------------------------------------
            # TOOLS USED
            # -----------------------------------------

            tools_used = result.get("tools_used", [])

            if tools_used:

                st.write("🔧 **Tools used**")

                for tool in tools_used:
                    st.write(f"✓ `{tool}`")

            # -----------------------------------------
            # PENDING ACTION
            # -----------------------------------------

            pending_action = result.get("pending_action")

            if pending_action:

                # Save the action for the next message
                st.session_state.pending_action = pending_action

                st.warning(
                    "⚠️ Confirmation required before creating this action."
                )

                st.write("### Proposed Action")

                st.write(
                    f"**Ticket:** {pending_action.get('ticket_id')}"
                )

                st.write(
                    f"**Priority:** {pending_action.get('priority')}"
                )

                st.write(
                    f"**Reason:** {pending_action.get('reason')}"
                )

                st.info(
                    "Reply **yes** to confirm the escalation."
                )

        else:

            st.markdown(str(result))