from __future__ import annotations

import logging
import sys

# Configure logging to stderr (stdout is reserved for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("ynab_mcp")

# Import shared instances
from ynab_mcp.app import mcp  # noqa: E402

# Import all tool modules to register them with the MCP server
import ynab_mcp.tools  # noqa: E402, F401


def main() -> None:
    """Run the MCP server."""
    logger.info("Starting YNAB MCP server")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
