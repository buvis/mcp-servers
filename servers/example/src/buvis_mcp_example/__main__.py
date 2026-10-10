"""Executable entry points for the reference MCP server."""

from buvis_mcp_core import run_stdio
from buvis_mcp_example.server import create_server


def main() -> None:
    """Start the reference server on stdio."""
    run_stdio(create_server)


if __name__ == "__main__":
    main()
