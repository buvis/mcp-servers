"""Process entry-point policy for stdio MCP servers."""

import logging
import sys
from collections.abc import Callable

from mcp.server import MCPServer


def run_stdio[StateT](
    server_factory: Callable[[], MCPServer[StateT]], *, log_level: int = logging.INFO
) -> None:
    """Own process logging and run a new server; call outside an event loop."""
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
        force=True,
    )
    server_factory().run(transport="stdio")
