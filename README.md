# buvis MCP servers

Python monorepo for buvis MCP servers, built on the **official MCP Python SDK v2**.
The workspace uses Python 3.12+, uv, one lockfile, and separately buildable packages.
The current lock selects `mcp==2.3.0`.

| Location | Purpose |
| --- | --- |
| `packages/core` | `buvis-mcp-core`: shared stdio startup and logging policy |
| `servers/example` | `buvis-mcp-example`: executable reference with an `echo` tool |
| `docs/dev` | Architecture, contributor guidance, research, and intake |

## Development

Tools are managed with [mise](https://mise.jdx.dev/). From this directory:

```sh
mise trust
mise run onboard
mise run check
mise run build
```

`onboard` installs any missing pinned mise tools and runs
`uv sync --locked --all-packages` with mise's selected Python. `check` runs Black,
isort, Ruff, Pyright, Bandit, and pytest with coverage. CI uses those same constituent commands and also builds
and tests installed wheels. A plain `uv sync` targets the non-package root;
use `--all-packages` to install all members, or `--package NAME` for one server.

| Task | Purpose |
| --- | --- |
| `onboard` | Install/repair tools and workspace dependencies |
| `onboard --sync` | Check installed prerequisites; there are no local integrations to refresh |
| `check` | Run the read-only source checks and tests |
| `format` | Apply isort and Black |
| `run-tests` | Run pytest, forwarding paths and selectors |
| `build` | Build every workspace distribution |
| `develop` | Run the reference server on stdio |

Each task has an executable `./tools/<task>` shim that works from another directory.
For bare interactive commands, activate mise in your shell (`eval "$(mise activate bash)"`,
or your shell's equivalent); it adds this checkout's `tools/` to PATH. Hooks and CI
should use explicit paths or `mise run`. Tasks never install tools implicitly;
`onboard --sync` does not install packages, contact the network, or alter hooks/config.
No Git hooks are installed because there are no local projections or links to refresh.
Mise tool resolution defaults to offline so this also holds before the task starts.
Full onboarding enables downloads explicitly for missing runtimes; explicit runtime
updates use `MISE_OFFLINE=false mise upgrade`. This setting does not restrict uv's
normal dependency downloads.

Run selected tests or the reference server:

```sh
./tools/run-tests servers/example/tests -k echo
./tools/develop
```

It waits for MCP input on stdin. To connect an MCP host, replace both absolute
paths below (`mise which uv` locates the executable):

```json
{
  "mcpServers": {
    "buvis-example": {
      "command": "/absolute/path/to/uv",
      "args": [
        "run", "--directory", "/absolute/path/to/mcp-servers",
        "--locked", "--package", "buvis-mcp-example", "buvis-mcp-example"
      ]
    }
  }
}
```

## Packages and changes

- [Architecture](docs/dev/architecture/README.md) describes boundaries and shared-core scope.
- [Adding a server](docs/dev/procedures/add-a-server.md) covers dependencies, entry points,
  testing, and distribution.
- [Research](docs/dev/project-management/intake/new/00001-initial-structure/research.md)
  records verified SDK APIs, sources, and the rationale for this foundation.
- [Structure review](docs/dev/project-management/reviews/20261004-structure-repo.md)
  records the `structure-git-repo` fit assessment, deliberate deviations, and checks.

Build wheels and source distributions with `uv build --all-packages --no-sources`.
CI installs the wheels into a clean environment and runs tests outside the workspace
to catch missing files and dependencies hidden by editable installs.

The calcard migration and proxy server remain separate intakes. No packages have
been published; install the core and a server together from local wheels until a
package registry is chosen.
