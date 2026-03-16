"""Shared application instances — imported by both server.py and all tool modules."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ynab_mcp.client import YNABClient

# Initialize FastMCP server
mcp = FastMCP("YNAB Budget Assistant", host="0.0.0.0", port=8000)

# Initialize YNAB client (reads YNAB_API_KEY from environment)
ynab = YNABClient()
