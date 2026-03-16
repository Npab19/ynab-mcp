from __future__ import annotations

import logging
import os
import sys

import uvicorn

# Configure logging to stderr (stdout is reserved for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("ynab_mcp")

# Import shared instances
from ynab_mcp.app import mcp  # noqa: E402
from ynab_mcp.auth import BearerTokenMiddleware  # noqa: E402

# Import all tool modules to register them with the MCP server
import ynab_mcp.tools  # noqa: E402, F401


def main() -> None:
    """Run the MCP server."""
    logger.info("Starting YNAB MCP server")

    token = os.environ.get("MCP_BEARER_TOKEN", "")
    if not token:
        raise RuntimeError("MCP_BEARER_TOKEN environment variable is required")

    starlette_app = mcp.streamable_http_app()
    protected_app = BearerTokenMiddleware(starlette_app, token=token)

    uvicorn.run(protected_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
