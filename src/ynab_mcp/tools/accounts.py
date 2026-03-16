from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def list_accounts(
    budget_id: str = "last-used",
    last_knowledge_of_server: int | None = None,
) -> dict:
    """List all accounts for a budget.

    Args:
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
        last_knowledge_of_server: If provided, only entities changed since this value will be included.
    """
    params = {}
    if last_knowledge_of_server is not None:
        params["last_knowledge_of_server"] = last_knowledge_of_server
    return await ynab.get(f"/budgets/{budget_id}/accounts", params=params or None)


@mcp.tool()
async def get_account(
    account_id: str,
    budget_id: str = "last-used",
) -> dict:
    """Get a single account by ID.

    Args:
        account_id: The account ID (UUID).
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.get(f"/budgets/{budget_id}/accounts/{account_id}")


@mcp.tool()
async def create_account(
    name: str,
    type: str,
    balance: int,
    budget_id: str = "last-used",
) -> dict:
    """Create a new account in a budget.

    Args:
        name: The account name.
        type: The account type. One of: checking, savings, cash, creditCard, lineOfCredit, otherAsset, otherLiability, mortgage, autoLoan, studentLoan, personalLoan, medicalDebt, otherDebt.
        balance: The starting balance in milliunits (1 dollar = 1000 milliunits).
        budget_id: The budget ID. Use 'last-used' for the most recently used budget.
    """
    return await ynab.post(
        f"/budgets/{budget_id}/accounts",
        json_body={"account": {"name": name, "type": type, "balance": balance}},
    )
