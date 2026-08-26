def decide_cancellation(order, account, documents):

    status = str(order.get("status", "")).upper()
    account_id = account.get("account_id")

    # ------------------------------------------------
    # Check customer-specific agreement first
    # ------------------------------------------------

    for doc in documents:

        if(
            doc.get("authority") == "customer_agreement"
            and doc.get("account_id") == account_id
            and doc.get("status") == "active"
        ):
            text = doc.get("text", "").lower()

            # Northstar-style agreement:
            # BOOKED before pickup = no cancellation fee
            if(
                "booked shipment before pickup with no cancellation fee"
                in text
                and status == "BOOKED"
            ):
                return {
                    "decision": "allowed",
                    "fee_inr": 0,
                    "reason": "Customer agreement overrides the default cancellation fee.",
                    "authority": "customer_agreement",
                    "source": doc["file_name"]
                }


    # ------------------------------------------------
    # Default SOP
    # ------------------------------------------------

    if status == "DRAFT":
        return {
            "decision": "allowed",
            "fee_inr": 0,
            "reason": "Draft shipments may be cancelled without a fee.",
            "authority": "current_sop"
        }

    if status == "BOOKED":
        return {
            "decision": "needs_time_check",
            "reason":  "Booked shipments have different fees depending on when cancellation was requested.",
            "authority": "current_sop"
        }

    if status == "PICKED_UP":
        return {
            "decision": "not_allowed",
            "fee_inr": None,
            "reason": "Picked-up shipments cannot be cancelled. Use the return-to-origin workflow.",
            "authority": "current_sop"
        }

    if status == "DELIVERED":
        return {
            "decision": "not_allowed",
            "fee_inr": None,
            "reason": "Delivered shipments cannot be cancelled.",
            "authority": "current_sop"
        }

    return {
        "decision": "needs_human_review",
        "reason": "The order status does not match a known cancellation rule.",
        "authority": "unknown"
    }
