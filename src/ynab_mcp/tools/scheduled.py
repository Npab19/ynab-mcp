from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_scheduled_transactions(
    budget_id: str = "last-used",
    last_knowledge_of_server: int | None = None,
) -> dict:
    """List all scheduled (recurring/future) transactions.

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params = {}
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server
    return await ynab.get(
        f"/budgets/{budget_id}/scheduled_transactions", params=params or None
    )


@mcp.tool()
async def get_scheduled_transaction(
    scheduled_transaction_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single scheduled transaction by ID.

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        scheduled_transaction_id: The scheduled transaction ID.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(
        f"/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}"
    )


@mcp.tool()
async def create_scheduled_transaction(
    account_id: str,
    date: str,
    budget_id: str = "last-used",
    amount: int | None = None,
    payee_id: str | None = None,
    payee_name: str | None = None,
    category_id: str | None = None,
    memo: str | None = None,
    flag_color: str | None = None,
    frequency: str | None = None,
) -> dict:
    """Create a scheduled (future/recurring) transaction.

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        account_id: The account ID (UUID).
        date: The scheduled date in ISO format (e.g. 2024-06-01). Must be a future date, no more than 5 years out.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        amount: Amount in milliunits. Negative for outflow, positive for inflow.
        payee_id: The payee ID (UUID).
        payee_name: Payee name. Used to resolve/create payee if payee_id is null.
        category_id: The category ID (UUID). Split scheduled transactions are not supported.
        memo: Memo (max 500 characters).
        flag_color: Flag color: 'red', 'orange', 'yellow', 'green', 'blue', 'purple', or null.
        frequency: Recurrence frequency. One of: never, daily, weekly, everyOtherWeek, twiceAMonth, every4Weeks, monthly, everyOtherMonth, every3Months, every4Months, twiceAYear, yearly, everyOtherYear.
    """
    txn: dict = {
        "account_id": account_id,
        "date": date,
    }
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
    if flag_color is not None:
        txn["flag_color"] = flag_color
    if frequency is not None:
        txn["frequency"] = frequency

    return await ynab.post(
        f"/budgets/{budget_id}/scheduled_transactions",
        json_body={"scheduled_transaction": txn},
    )


@mcp.tool()
async def update_scheduled_transaction(
    scheduled_transaction_id: str,
    budget_id: str = "last-used",
    account_id: str | None = None,
    date: str | None = None,
    amount: int | None = None,
    payee_id: str | None = None,
    payee_name: str | None = None,
    category_id: str | None = None,
    memo: str | None = None,
    flag_color: str | None = None,
    frequency: str | None = None,
) -> dict:
    """Update a scheduled transaction.

    Only provide the fields you want to change. All amounts in milliunits.

    Args:
        scheduled_transaction_id: The scheduled transaction ID to update.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        account_id: New account ID (UUID).
        date: New scheduled date in ISO format.
        amount: New amount in milliunits.
        payee_id: New payee ID (UUID).
        payee_name: New payee name.
        category_id: New category ID (UUID).
        memo: New memo (max 500 characters).
        flag_color: Flag color: 'red', 'orange', 'yellow', 'green', 'blue', 'purple', or null.
        frequency: New recurrence frequency.
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
    if flag_color is not None:
        txn["flag_color"] = flag_color
    if frequency is not None:
        txn["frequency"] = frequency

    return await ynab.put(
        f"/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}",
        json_body={"scheduled_transaction": txn},
    )


@mcp.tool()
async def delete_scheduled_transaction(
    scheduled_transaction_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Delete a scheduled transaction.

    Args:
        scheduled_transaction_id: The scheduled transaction ID to delete.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.delete(
        f"/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}"
    )
