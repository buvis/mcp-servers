"""Construct an isolated reference server using the official SDK."""

from importlib.metadata import version

from mcp.server import MCPServer
from mcp.types import ToolAnnotations


def create_server() -> MCPServer[None]:
    """Return a new server without starting a transport."""
    server: MCPServer[None] = MCPServer(
        "buvis-mcp-example",
        version=version("buvis-mcp-example"),
        instructions="A development example. Use echo to check the MCP connection.",
    )
    server.add_tool(
        echo,
        annotations=ToolAnnotations(
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=False,
        ),
    )
    return server


def echo(text: str) -> str:
    """Return the supplied text unchanged."""
    return text
