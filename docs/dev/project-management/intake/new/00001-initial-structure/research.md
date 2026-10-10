# Initial structure research

Research date: 2026-10-03. Scope: official Python SDK v2, a reusable core, packaging,
and verification for the new buvis MCP monorepo.

## Findings

The official `mcp` package has a stable 2.3.0 release dated October 2, 2026, published
from `modelcontextprotocol/python-sdk`. It requires Python 3.10 or newer. This
workspace targets 3.12+, matching the existing calcard project's baseline.
[PyPI release and provenance](https://pypi.org/project/mcp/2.3.0/)

SDK v2's high-level API is `from mcp.server import MCPServer`; the old
`mcp.server.fastmcp` module is removed. Python model fields use snake_case, including
`structured_content` and `is_error`. SDK v2 no longer loads `.env` implicitly.
The external `fastmcp` package is a different dependency and is not selected here.
[Official migration guide](https://py.sdk.modelcontextprotocol.io/migration/)

The SDK offers in-memory `Client(server)` tests and stdio subprocess clients via
`StdioServerParameters`. Entering/exiting the client manages connection lifetime.
The subprocess transport filters inherited environment variables. Tests here pass
only additional coverage configuration, rather than copying the parent environment.
[Official testing guide](https://py.sdk.modelcontextprotocol.io/get-started/testing/),
[client transports](https://py.sdk.modelcontextprotocol.io/client/transports/)

uv workspaces give members individual manifests and one shared lockfile. Sources
declared at the root apply to members; consumers must still declare dependencies.
Workspace installs are editable, and Python does not enforce member dependency
isolation. A non-package coordinating root is supported.
[uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/),
[project configuration](https://docs.astral.sh/uv/concepts/projects/config/)

`--locked` verifies that the lockfile still matches manifests, while `--frozen`
skips freshness validation. `uv build --no-sources` checks ordinary packaging
metadata without relying on development source overrides.
[Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/),
[building and publishing](https://docs.astral.sh/uv/guides/publish/)

## Decisions

- Use `mcp>=2.3,<3` in runtime metadata and lock 2.3.0 for reproducible development.
  This preserves standard version resolution for independently installed wheels.
- Put reusable libraries under `packages/` and independent servers under `servers/`.
  Use Hatchling and `src/` layouts; the existing calcard package uses that backend.
- Keep core limited to a stdio runner with stderr logging established before the
  server factory executes. Use SDK APIs directly for domain behavior and lifespans.
- Include one deterministic echo server to exercise the package boundary and serve
  as a copyable reference. Do not build calcard migration or proxy features here.
- Test behavior in memory, over real stdio, and from independently installed wheels.
  The last check addresses a documented limitation of workspace dependency isolation.
- Keep root tooling and checks centralized; use mise for runtimes and uv for Python
  dependencies. Pin GitHub Actions commits and scope CI permissions to read-only.

These are local design choices informed by the sources above, not MCP requirements.

## Evidence and limitations

The research agent ran 20 targeted searches and fetched five primary-source pages;
implementation follow-up inspected the installed 2.3.0 wheel's API signatures and
startup logging, then exercised the actual SDK. Current documentation can evolve;
the lockfile and executable tests record the version verified here.

The initial study does not choose a registry, release automation, HTTP deployment,
or authentication policy. Calcard currently depends on external FastMCP 3; its
migration needs its own compatibility review and cannot be treated as a folder move.

CI action references were verified against the official
[checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) and
[setup-uv v10.2.0](https://github.com/astral-sh/setup-uv/releases/tag/v10.2.0) releases.

## Verification and skeptical review

This section records the 2026-10-03 review. Git initialization and mise trust were
subsequently completed; the [structure migration report](../../../reviews/20261004-structure-repo.md)
contains the current setup status. Hosted CI still awaits a remote and push.

Local validation on macOS: 10 tests pass with 100% line/branch coverage, including
subprocesses. Clean wheel installs also pass all 10 tests on Python 3.12.13,
3.13.14, and 3.14.6. Both distributions build as sdist and wheel with `--no-sources`.
Black, isort, Ruff, strict Pyright, Bandit, and lockfile freshness checks pass.

The review found seven doubts: two fixed, three verified and dismissed, and two
remaining environment limitations.

| Doubt | Disposition and evidence |
| --- | --- |
| Editable installs may hide missing files or dependencies; the least certain integration point | Verified: clean wheel environments passed; wheel metadata declares core/SDK dependencies and includes `py.typed`. |
| Coverage may miss child processes or startup/shutdown paths | Verified: explicit coverage environment forwarding measures both entry points; the report shows 100% including the main guard. |
| A shared runner with one server might be unnecessary abstraction | Verified: the intake requires a reusable core; the regression test demonstrated that logging must be configured before SDK construction. The factory owns only this process policy. |
| The runtime docstring duplicated package guidance | Fixed: shortened it; usage detail remains in package/architecture documentation. Generated lock data and package metadata account for much of the remaining foundation size. |
| The unknown-tool test verified SDK behavior without a local contract | Fixed: removed it and exercised the example's missing/wrong-type argument contract instead. |
| Git and mise setup are incomplete | Known: `.git` and mise's global trust store are outside this session's writable scope. `git init -b main` and `mise trust` must run locally. |
| Hosted CI has not actually run | Known: there is no Git repository or remote yet. Workflow YAML and command parity with mise were checked; Linux execution awaits a push. |

A second pass reviewed both fixes, reran checks and tests, and found no new issue.
The startup logging regression, independent package builds, and isolated installs
support retaining the current small core and direct SDK API approach.
