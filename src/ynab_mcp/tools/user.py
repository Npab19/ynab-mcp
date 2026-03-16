from __future__ import annotations

from ynab_mcp.app import mcp, ynab


@mcp.tool()
async def get_user() -> dict:
    """Get the authenticated user's information including user ID."""
    return await ynab.get("/user")
