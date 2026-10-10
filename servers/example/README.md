# buvis-mcp-example

An executable reference for a buvis MCP server. Its `echo` tool returns the supplied
text without side effects or external services. This is a development example.

From the workspace root:

```sh
uv run --locked --package buvis-mcp-example buvis-mcp-example
```

The process waits for MCP messages on stdin and writes protocol responses to stdout.
Diagnostic logs go to stderr. `python -m buvis_mcp_example` is also supported after
installation. See the root README for MCP host configuration.
