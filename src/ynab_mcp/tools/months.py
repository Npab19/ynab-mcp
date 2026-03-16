from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_months(
    budget_id: str = "last-used",
    last_knowledge_of_server: int | None = None,
) -> dict:
    """List all budget months with summary information.

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params = {}
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server
    return await ynab.get(f"/budgets/{budget_id}/months", params=params or None)


@mcp.tool()
async def get_month(
    month: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single budget month with category details.

    Includes Ready to Assign, Age of Money, and all category balances.
    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        month: The budget month in ISO format (e.g. 2016-12-01) or 'current'.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(f"/budgets/{budget_id}/months/{month}")
