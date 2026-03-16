from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_transactions(
    budget_id: str = "last-used",
    account_id: str | None = None,
    category_id: str | None = None,
    payee_id: str | None = None,
    since_date: str | None = None,
    type: str | None = None,
    last_knowledge_of_server: int | None = None,
) -> dict:
    """List transactions for a budget, optionally filtered by account, category, or payee.

    Provide at most one of account_id, category_id, or payee_id to filter.
    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        account_id: Filter by account ID. Returns only transactions for this account.
        category_id: Filter by category ID. Returns only transactions for this category.
        payee_id: Filter by payee ID. Returns only transactions for this payee.
        since_date: Only transactions on or after this date (ISO format, e.g. 2024-01-01).
        type: Filter by type: 'uncategorized' or 'unapproved'.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params: dict = {}
    if since_date is not None:
        params["since_date"] = since_date
    if type is not None:
        params["type"] = type
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server

    if account_id is not None:
        path = f"/budgets/{budget_id}/accounts/{account_id}/transactions"
    elif category_id is not None:
        path = f"/budgets/{budget_id}/categories/{category_id}/transactions"
    elif payee_id is not None:
        path = f"/budgets/{budget_id}/payees/{payee_id}/transactions"
    else:
        path = f"/budgets/{budget_id}/transactions"

    return await ynab.get(path, params=params or None)


@mcp.tool()
async def get_transaction(
    transaction_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single transaction by ID.

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        transaction_id: The transaction ID.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(f"/budgets/{budget_id}/transactions/{transaction_id}")


@mcp.tool()
async def create_transaction(
    account_id: str,
    date: str,
    amount: int,
    budget_id: str = "last-used",
    payee_id: str | None = None,
    payee_name: str | None = None,
    category_id: str | None = None,
    memo: str | None = None,
    cleared: str | None = None,
    approved: bool | None = None,
    flag_color: str | None = None,
    import_id: str | None = None,
    subtransactions: list[dict] | None = None,
) -> dict:
    """Create a single transaction.

    All amounts are in milliunits (1 dollar = 1000 milliunits).
    Scheduled transactions (future dates) cannot be created here — use create_scheduled_transaction.

    Args:
        account_id: The account ID (UUID).
        date: Transaction date in ISO format (e.g. 2024-01-15). Must not be a future date.
        amount: Amount in milliunits. Negative for outflow, positive for inflow.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        payee_id: The payee ID (UUID). Optional.
        payee_name: Payee name. Used to resolve/create payee if payee_id is null.
        category_id: The category ID (UUID). Set to null and provide subtransactions for a split.
        memo: Transaction memo (max 500 characters).
        cleared: Cleared status: 'cleared', 'uncleared', or 'reconciled'.
        approved: Whether the transaction is approved. Defaults to unapproved.
        flag_color: Flag color: 'red', 'orange', 'yellow', 'green', 'blue', 'purple', or null.
        import_id: Import ID for deduplication (max 36 characters).
        subtransactions: List of subtransactions for splits. Each needs 'amount' (int) and optionally 'payee_id', 'payee_name', 'category_id', 'memo'.
    """
    txn: dict = {
        "account_id": account_id,
        "date": date,
        "amount": amount,
    }
    if payee_id is not None:
        txn["payee_id"] = payee_id
    if payee_name is not None:
        txn["payee_name"] = payee_name
    if category_id is not None:
        txn["category_id"] = category_id
    if memo is not None:
        txn["memo"] = memo
    if cleared is not None:
        txn["cleared"] = cleared
    if approved is not None:
        txn["approved"] = approved
    if flag_color is not None:
        txn["flag_color"] = flag_color
    if import_id is not None:
        txn["import_id"] = import_id
    if subtransactions is not None:
        txn["subtransactions"] = subtransactions

    return await ynab.post(
        f"/budgets/{budget_id}/transactions",
        json_body={"transaction": txn},
    )


@mcp.tool()
async def create_transactions(
    transactions: list[dict],
    budget_id: str = "last-used",
) -> dict:
    """Create multiple transactions in a single request.

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        transactions: List of transaction objects. Each needs 'account_id', 'date', 'amount' at minimum. Optional: 'payee_id', 'payee_name', 'category_id', 'memo', 'cleared', 'approved', 'flag_color', 'import_id'.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.post(
        f"/budgets/{budget_id}/transactions",
        json_body={"transactions": transactions},
    )


@mcp.tool()
async def update_transaction(
    transaction_id: str,
    budget_id: str = "last-used",
    account_id: str | None = None,
    date: str | None = None,
    amount: int | None = None,
    payee_id: str | None = None,
    payee_name: str | None = None,
    category_id: str | None = None,
    memo: str | None = None,
    cleared: str | None = None,
    approved: bool | None = None,
    flag_color: str | None = None,
) -> dict:
    """Update an existing transaction.

    Only provide the fields you want to change. All amounts in milliunits.

    Args:
        transaction_id: The transaction ID to update.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        account_id: New account ID (UUID).
        date: New date in ISO format (e.g. 2024-01-15).
        amount: New amount in milliunits.
        payee_id: New payee ID (UUID).
        payee_name: New payee name.
        category_id: New category ID (UUID).
        memo: New memo (max 500 characters).
        cleared: New cleared status: 'cleared', 'uncleared', or 'reconciled'.
        approved: Whether the transaction is approved.
        flag_color: Flag color: 'red', 'orange', 'yellow', 'green', 'blue', 'purple', or null.
    """
    txn: dict = {}
    if account_id is not None:
        txn["account_id"] = account_id
    if date is not None:
        txn["date"] = date
    if amount is not None:
        txn["amount"] = amount
    if payee_id is not None:
        txn["payee_id"] = payee_id
    if payee_name is not None:
        txn["payee_name"] = payee_name
    if category_id is not None:
        txn["category_id"] = category_id
    if memo is not None:
        txn["memo"] = memo
    if cleared is not None:
        txn["cleared"] = cleared
    if approved is not None:
        txn["approved"] = approved
    if flag_color is not None:
        txn["flag_color"] = flag_color

    return await ynab.put(
        f"/budgets/{budget_id}/transactions/{transaction_id}",
        json_body={"transaction": txn},
    )


@mcp.tool()
async def update_transactions(
    transactions: list[dict],
    budget_id: str = "last-used",
) -> dict:
    """Update multiple transactions by ID or import_id.

    Each transaction must have either an 'id' or 'import_id' for lookup.
    Do not specify both. Updating an import_id on an existing transaction is not allowed.

    Args:
        transactions: List of transaction objects. Each needs 'id' or 'import_id' for lookup, plus fields to update.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.patch(
        f"/budgets/{budget_id}/transactions",
        json_body={"transactions": transactions},
    )


@mcp.tool()
async def delete_transaction(
    transaction_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Delete a transaction.

    Args:
        transaction_id: The transaction ID to delete.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.delete(f"/budgets/{budget_id}/transactions/{transaction_id}")


@mcp.tool()
async def import_transactions(
    budget_id: str = "last-used",
) -> dict:
    """Import transactions from all linked accounts.

    This triggers an import from linked financial institutions, equivalent to
    clicking 'Import' in the YNAB web app. Returns the IDs of imported transactions.

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.post(f"/budgets/{budget_id}/transactions/import")
