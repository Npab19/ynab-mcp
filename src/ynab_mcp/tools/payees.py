from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_payees(
    budget_id: str = "last-used",
    last_knowledge_of_server: int | None = None,
) -> dict:
    """List all payees for a budget.

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params = {}
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server
    return await ynab.get(f"/budgets/{budget_id}/payees", params=params or None)


@mcp.tool()
async def get_payee(
    payee_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single payee by ID.

    Args:
        payee_id: The payee ID.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(f"/budgets/{budget_id}/payees/{payee_id}")


@mcp.tool()
async def update_payee(
    payee_id: str,
    name: str,
    budget_id: str = "last-used",
) -> dict:
    """Update a payee's name.

    Args:
        payee_id: The payee ID.
        name: The new payee name (max 500 characters).
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.patch(
        f"/budgets/{budget_id}/payees/{payee_id}",
        json_body={"payee": {"name": name}},
    )
