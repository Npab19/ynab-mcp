from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_categories(
    budget_id: str = "last-used",
    last_knowledge_of_server: int | None = None,
) -> dict:
    """List all categories grouped by category group.

    Amounts (budgeted, activity, balance) are for the current budget month (UTC).
    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params = {}
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server
    return await ynab.get(f"/budgets/{budget_id}/categories", params=params or None)


@mcp.tool()
async def get_category(
    category_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single category. Amounts are for the current budget month (UTC).

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        category_id: The category ID.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(f"/budgets/{budget_id}/categories/{category_id}")


@mcp.tool()
async def update_category(
    category_id: str,
    budget_id: str = "last-used",
    name: str | None = None,
    note: str | None = None,
    category_group_id: str | None = None,
    goal_target: int | None = None,
) -> dict:
    """Update a category's name, note, group, or goal target.

    Args:
        category_id: The category ID.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        name: New category name.
        note: New category note.
        category_group_id: Move category to a different group (UUID).
        goal_target: Goal target amount in milliunits. Only works if category already has a goal.
    """
    category: dict = {}
    if name is not None:
        category["name"] = name
    if note is not None:
        category["note"] = note
    if category_group_id is not None:
        category["category_group_id"] = category_group_id
    if goal_target is not None:
        category["goal_target"] = goal_target
    return await ynab.patch(
        f"/budgets/{budget_id}/categories/{category_id}",
        json_body={"category": category},
    )


@mcp.tool()
async def get_month_category(
    month: str,
    category_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single category for a specific budget month.

    All amounts are in milliunits (1 dollar = 1000 milliunits).

    Args:
        month: The budget month in ISO format (e.g. 2016-12-01) or 'current'.
        category_id: The category ID.
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(
        f"/budgets/{budget_id}/months/{month}/categories/{category_id}"
    )


@mcp.tool()
async def update_month_category(
    month: str,
    category_id: str,
    budgeted: int,
    budget_id: str = "last-used",
) -> dict:
    """Update the budgeted amount for a category in a specific month.

    Only the budgeted amount can be updated.

    Args:
        month: The budget month in ISO format (e.g. 2016-12-01) or 'current'.
        category_id: The category ID.
        budgeted: The budgeted amount in milliunits (1 dollar = 1000 milliunits).
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.patch(
        f"/budgets/{budget_id}/months/{month}/categories/{category_id}",
        json_body={"category": {"budgeted": budgeted}},
    )
