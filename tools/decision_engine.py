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


def decide_service_credit(order, account, documents):
    """
    Determine service-credit eligibility using the current SOP
    and customer-specific agreement.
    """

    from datetime import datetime

    if not order:
        return {
            "decision": "needs_verification",
            "reason": "Order information is unavailable."
        }

    shipment_fee = order.get("shipment_fee_inr")
    carrier_fault = order.get("carrier_fault")
    customer_fault = order.get("customer_fault")

    pickup_window_end = order.get("pickup_window_end")
    pickup_actual_at = order.get("pickup_actual_at")

    if not pickup_window_end:
        return {
            "decision": "needs_verification",
            "reason": "Pickup window information is unavailable."
        }

    try:
        window_end = datetime.fromisoformat(str(pickup_window_end))
    except Exception:
        return {
            "decision": "needs_verification",
            "reason": "Pickup window data could not be interpreted."
        }

    # Dataset snapshot time from README
    snapshot_time = datetime(2026, 8, 16, 11, 0)

    # If the shipment was picked up, use actual pickup time.
    # If it has not been picked up, use the dataset snapshot time.
    if pickup_actual_at and str(pickup_actual_at).lower() != "nan":
        try:
            actual_pickup = datetime.fromisoformat(str(pickup_actual_at))
        except Exception:
            return {
                "decision": "needs_verification",
                "reason": "Pickup timing data could not be interpreted."
            }
    else:
        actual_pickup = snapshot_time

    delay_hours = (
        actual_pickup - window_end
    ).total_seconds() / 3600

    # Carrier fault must be confirmed
    if carrier_fault is not True:
        return {
            "decision": "needs_verification",
            "reason": "Carrier fault must be confirmed before granting a service credit."
        }

    # Customer fault makes the order ineligible
    if customer_fault is True:
        return {
            "decision": "not_eligible",
            "credit_inr": 0,
            "reason": "The order has a customer-caused issue."
        }

    # Check for customer-specific agreement
    account_id = order.get("account_id")

    customer_agreement = None

    for document in documents:
        if (
            document.get("authority") == "customer_agreement"
            and document.get("account_id") == account_id
        ):
            customer_agreement = document
            break

    # LumenWorks-specific rule
    if account_id == "ACCT-002":

        if delay_hours <= 4:
            return {
                "decision": "not_eligible",
                "credit_inr": 0,
                "reason": (
                    f"Pickup is only {delay_hours:.1f} hours past the "
                    "scheduled pickup window. LumenWorks requires more "
                    "than 4 hours."
                ),
                "authority": "customer_agreement",
                "source": "06_LumenWorks_Service_Agreement.pdf"
            }

        return {
            "decision": "eligible",
            "credit_inr": 300,
            "reason": (
                f"Pickup is {delay_hours:.1f} hours past the scheduled "
                "window, carrier fault is confirmed, and there is no "
                "customer-caused issue. LumenWorks receives a fixed "
                "INR 300 credit after more than 4 hours."
            ),
            "authority": "customer_agreement",
            "source": "06_LumenWorks_Service_Agreement.pdf"
        }

    # Default SOP
    if delay_hours <= 2:
        return {
            "decision": "not_eligible",
            "credit_inr": 0,
            "reason": (
                f"Pickup is only {delay_hours:.1f} hours past the "
                "scheduled window. The default threshold is more than 2 hours."
            ),
            "authority": "current_sop",
            "source": "03_Cancellation_and_Service_Credit_SOP_v4.pdf"
        }

    credit = min(500, shipment_fee * 0.10)

    return {
        "decision": "eligible",
        "credit_inr": credit,
        "reason": (
            f"Pickup is {delay_hours:.1f} hours past the scheduled window, "
            "carrier fault is confirmed, and there is no customer-caused issue."
        ),
        "authority": "current_sop",
        "source": "03_Cancellation_and_Service_Credit_SOP_v4.pdf"
    }