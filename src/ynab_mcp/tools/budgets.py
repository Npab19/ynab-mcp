from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_budgets(include_accounts: bool = False) -> dict:
    """List all budgets the user has access to.

    Returns budget names, IDs, and summary information.
    Use the returned budget ID (or 'last-used') in other tools.

    Args:
        include_accounts: Whether to include the list of accounts for each budget.
    """
    params = {}
    if include_accounts:
        params["include_accounts"] = "true"
    return await ynab.get("/budgets", params=params or None)


@mcp.tool()
async def get_budget(
    budget_id: str = "last-used",
    last_knowledge_of_server: int | None = None,
) -> dict:
    """Get a single budget with all related entities (full budget export).

    This is a large response. Use last_knowledge_of_server for delta sync.

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params = {}
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server
    return await ynab.get(f"/budgets/{budget_id}", params=params or None)


@mcp.tool()
async def get_budget_settings(budget_id: str = "last-used") -> dict:
    """Get settings for a budget including date format and currency format.

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(f"/budgets/{budget_id}/settings")
