def can_access_account(user, account_id):
    """
    Check whether the current user can access an account.

    Internal support users can access all accounts.

    Customer users can only access their own account.
    """

    if user["role"] == "internal_support":
        return True

    if user["role"] == "customer":
        return user.get("account_id") == account_id

    return False

def require_account_access(user, account_id):
    """
    Raise an error if the user is not authorized
    to access the requested account.
    """

    if not can_access_account(user, account_id):

        raise PermissionError(
            f"User is not authorized to access account {account_id}."
        )
