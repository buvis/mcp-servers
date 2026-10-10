# Adding a server

1. Create `servers/<name>/pyproject.toml` with a unique distribution name, version,
   description, README, Python requirement, and build backend. Follow the example's
   `src/<import_name>/` layout and include `py.typed`.
2. Declare `buvis-mcp-core>=0.1,<0.2`, `mcp>=2.3,<3`, and every other direct runtime
   dependency. The root `tool.uv.sources` mapping supplies core locally. Do not add
   a dependency to the root merely to make a server's imports work.
3. Provide `create_server()` returning a fresh `mcp.server.MCPServer`. Use installed
   distribution metadata for its version. Register domain tools directly with the
   SDK; use typed arguments, return values, docstrings, and accurate annotations.
4. Define a console script pointing to `<import_name>.__main__:main`. Its `main()`
   calls `run_stdio(create_server)`; guard module execution with `__name__`.
   Keep stdout for MCP. Configure secrets explicitly at startup and fail promptly
   when required values are missing. The SDK v2 does not implicitly load `.env`.
5. Put tests alongside the member. Use `Client(create_server())` for contract tests
   and `Client(StdioServerParameters(...))` for installed process checks. Add new
   import packages to root coverage, isort source paths, and Ruff first-party names.
6. Run `uv lock`, `mise run onboard`, `mise run check`, and `mise run build`. The
   workspace glob automatically includes the new member. Review `uv.lock` with
   dependency changes; do not update it incidentally during unrelated work.

Use SDK lifespan hooks for shared connections and close them on shutdown. Do not
construct a global server at import time. Production servers should declare only
their own integration dependencies; tests may use root development dependencies.

## Focused work

```sh
uv run --locked --package buvis-mcp-example buvis-mcp-example
./tools/run-tests servers/example/tests
uv build --package buvis-mcp-example --no-sources
```

`--no-sources` checks builds against standard packaging metadata. The workspace
source mapping is a development convenience and is not embedded in wheel metadata.

## Installing distributions

Build core and the selected server, then install both wheels together into a clean
virtual environment. Install the test dependencies and run tests from outside the
checkout using pytest's configured importlib mode. CI demonstrates the exact
commands. This detects missing package files and accidental reliance on editable
workspace paths. For each new server, keep this check restricted to that server
and its shared libraries so sibling dependencies cannot mask mistakes.

Until core is published, installing a server by its PyPI name alone cannot resolve
the internal dependency. Future publication must make the required core version
available first. Release policy and registry selection are separate work.
