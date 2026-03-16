# Import all tool modules so their @mcp.tool() decorators register with the server.
from ynab_mcp.tools import (  # noqa: F401
    accounts,
    budgets,
    categories,
    months,
    payees,
    scheduled,
    transactions,
    user,
)
