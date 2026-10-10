# Architecture

## Workspace

The root is a non-distributable uv project. `packages/*` holds shared libraries;
`servers/*` holds separately buildable server distributions. Every member has a
`pyproject.toml`, a `src/` package, a package README, and adjacent tests.

The root source mapping resolves `buvis-mcp-core` to the editable workspace member.
Every consumer must also declare core in its own runtime dependencies. One lockfile
and development environment keep versions aligned, but do not isolate dependencies:
an undeclared import can work accidentally in development. CI therefore tests
installed wheels in a clean environment outside the checkout.

Each distribution owns its version. Servers read their version from installed
distribution metadata, so MCP discovery and wheel metadata agree. The coordinating
root version is not a release train. Core and example start at 0.1.0; no publication
or release automation is implied.

## Dependency direction

`server -> buvis-mcp-core -> official mcp SDK`

Servers also declare `mcp` directly because they import SDK APIs. Core must not
depend on any server. A server owns domain integrations and credentials, tool
registration, validation, and its SDK lifespan. Shared code moves into core when
there is a concrete reusable policy or behavior.

Core currently exports only `run_stdio(server_factory, *, log_level=logging.INFO)`.
It replaces root log handlers with stderr logging **before** constructing the
server, then calls the SDK's stdio runner. This is a process-entry-point API, not
an embedding API. Importing core has no logging side effects. For embedding and
in-memory tests, call the server factory directly. Custom loggers with their own
handlers remain the server author's responsibility.

The SDK owns schemas, protocol negotiation, request validation, tool errors,
concurrency, and transport lifecycle. There is no local server framework or SDK
compatibility shim. HTTP, authentication, secret stores, proxy routing, and metrics
belong to concrete future server requirements.

## Compatibility and verification

Runtime packages require `mcp>=2.3,<3`; `uv.lock` currently selects 2.3.0, and normal
development/CI commands use `--locked`. SDK upgrades are explicit lockfile changes
with protocol tests. The separate `fastmcp` distribution is not used.

CI covers Python 3.12–3.14 on Linux and 3.12 on macOS. Tests check server identity,
tool schemas and annotations, Unicode/empty input, errors, stderr routing, both
installed entry points, and process shutdown. SDK clients exercise real protocol
messages; handlers are not replaced with mocks. Coverage includes subprocesses.

Production code is checked with strict Pyright and Bandit; Black/isort/Ruff enforce
formatting and lint. CI's GitHub Actions are pinned by commit with read-only
permissions. The initial scope does not claim Windows support.
