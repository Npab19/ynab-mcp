"""Shared application instances — imported by both server.py and all tool modules."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ynab_mcp.client import YNABClient

# Initialize FastMCP server.
# stateless_http: don't keep sessions in memory, so clients keep working after
# the container restarts instead of getting 404 "Session not found".
mcp = FastMCP("YNAB Budget Assistant", host="0.0.0.0", port=8000, stateless_http=True)

# Initialize YNAB client (reads YNAB_API_KEY from environment)
ynab = YNABClient()
