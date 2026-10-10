# Repository structure migration — 2026-10-04

Status: COMPLETE (local structure and workflows verified; initial commit and remote pending).
Target: `/Users/bob/git/src/github.com/buvis/mcp-servers`.
Mode: restructure. Authority: the installed `structure-git-repo` skill, read from
`/Users/bob/git/src/github.com/buvis/agent-skills/skills/structure-git-repo/SKILL.md`.

## Baseline and recovery

At migration start, the helper reported `git.kind: none` and `git status` confirmed
there was no repository. There was no index, tracked history, repository hook setup,
or linked worktree to preserve. Existing authored files were therefore treated as
untracked, recoverable user content. Native Python package/test layouts, pins, and
CI checks already worked. The user has since initialized Git on `master`.

Before mutation, originals of every existing file to be changed or moved were saved
to `docs/dev/tmp/structure-repo-20261004/originals.tar.gz`. It retains original paths
and includes README, AGENTS, mise, ignores, CI, and development docs/intakes. Keep
this ignored recovery archive until the resulting tree is safely committed; extract
to a separate directory to inspect or selectively restore it.

## Applicability and path map

| Area / observed source | Destination or action | Consumers | Prerequisite |
| --- | --- | --- | --- |
| `packages/core`, `servers/example`, `src/`, adjacent tests | Preserve ecosystem layout | uv, build backend, pytest, type/lint/coverage config, CI | None |
| `docs/dev/architecture.md` | `docs/dev/architecture/README.md` | README, AGENTS | Rewrite links together |
| `docs/dev/adding-a-server.md` | `docs/dev/procedures/add-a-server.md` | README, AGENTS, onboarding commands in prose | Rewrite links and rename command |
| `intake/new/initial-structure.md` | `intake/new/00001-initial-structure/idea.md` | Research links, historical implementation note | Preserve original input; no retrospective spec |
| `intake/new/migrate-calcard-mcp.md` | `intake/new/00002-migrate-calcard-mcp/idea.md` | Human intake queue | No existing ID or spec |
| `intake/new/pmcp.md` | `intake/new/00003-pmcp/idea.md` | Human intake queue | No existing ID or spec |
| `project-management/discovery/research-initial-structure-2026-10-03.md` | `intake/new/00001-initial-structure/research.md` | README, AGENTS, intake Sources link | Preserve research/review provenance |
| `mise.toml` setup/check/build | onboard/check/format/run-tests/build/develop tasks and matching `tools/` shims | README, AGENTS, procedure, CI's existing constituent commands | Installed mise syntax and tools |
| Root `AGENTS.md` | Clarify nested scope discovery and update command/doc pointers | Active Codex app session | No new host adapter |
| Recovery scratch | Ignore `/docs/dev/tmp/` precisely; verified against the initialized repo | Git, future scratch cleanup | None |
| Git, actual fresh clone | Initialized on `master`; linked-worktree behavior tested in a disposable repository | Git | Actual fresh clone awaits the first commit |
| Mise trust registration | Already trusted, verified with `mise trust --show` | Public tasks | No new trust changes needed |
| Specs, Braid projections, Autopilot runtime/records, Kiro/other hosts | Not applicable: no configured repo inputs/state/integrations | None to migrate | Enable only against installed supported capabilities |
| Release/version publication | Not applicable: packages build locally; no registry/release workflow | Preserve member manifest versions | Separate release decision |

Numbered intake IDs are assigned here because the original flat files had none.
The delivered foundation remains explicitly historical in `new/`: this skill defines
`processed/` as having a spec, and no spec exists. No requirements, approvals, Q&A,
or execution state will be fabricated. No second active queue is created.

## Current fit assessment

Project kind: Python service monorepo with independently buildable packages. The
current skill's Fit section makes the structure advisory: "A deliberate deviation
is a result, not a defect." This revalidation uses that revised policy. The shared
discovery installation matches the explicitly requested skill source byte-for-byte
for the skill, helper, and all consumed references.

| Area | Observed source | Fit and decision | Prerequisite |
| --- | --- | --- | --- |
| Package/source/test trees | uv workspace manifests and package-local tests | Fits; preserve native layouts | Existing Python/uv toolchain |
| Docs and intake lifecycle | Architecture overview, verb-first procedure, numbered idea folders | Fits; preserve original input and historical status, add no empty artifacts | No spec or approval tooling configured |
| Commands and CI | Six mise tasks, thin public shims, matching CI commands | Fits; retain working commands and one behavior implementation | Trusted mise config and installed tools |
| Public MCP executable | `buvis-mcp-example` in manifest, README host config, and tests | MISFIT for blanket verb-first renaming; retain this compatibility deviation | None |
| Agent/workflow integrations | Root AGENTS; no local skills, Specflow, Autopilot state, or Kiro configuration | Conditional and currently inapplicable; do not invent adapters or state | Explicit enablement and verified consumer support |
| Release tooling | Local package builds; no publication workflow | Currently inapplicable; do not add a dummy release task | Registry/release decision |
| Git boundary | Helper confirms this directory owns its Git worktree | Fits; initialization complete | None |

The earlier pass treated public shims as mandatory and flagged their boilerplate.
Under the current policy they are retained by choice: the existing five-line
launchers already provide tested checkout anchoring and status/argument forwarding.
Removing working commands now would cause churn without improving behavior. Keep
their logic in mise/tasks and do not grow an extra task framework. No forced root
`src/`, empty doc categories, unconfigured integrations, or release adapter is needed.

The blanket verb-first rule also reaches the existing `buvis-mcp-example` console
entry point. Keep that public package command as an explicit compatibility exception:
renaming it solely for this structure pass would invalidate configurations that use
the documented executable. Repository workflow commands and procedure names use verbs.
This naming deviation is permitted by Fit and does not block completion.

## Completed groups

- Baseline inventory, repository instructions, manifests, CI and path consumers read.
- Installed helper and all required references found; inspect ran successfully.
- Installed mise 2026.4.16 exposes `task.run_auto_install` and task argument forwarding.
- Recoverable original bytes captured before any edits/moves.
- Documentation and intake files moved to their mapped destinations; root doc links
  and the original intake's research link migrated together. Original idea content
  and research/review history retained; obsolete empty `discovery/` removed.
- Public commands migrated to onboard/check/format/run-tests/build/develop with
  checkout-anchored shims, `tools/` PATH integration, and implicit mise installs
  disabled. Full onboard explicitly installs; sync only checks installed tooling.
- Root agent guidance now states nested-file discovery and scope. No native
  execution policy, global hooks, or host configuration was created or overwritten.
- Ignored only `/docs/dev/tmp/`; authored native integration trees remain visible.
- All six task definitions validate under installed mise. Actual `onboard --sync`
  succeeds using installed tools. `git init -b main` was retried and denied by the
  filesystem boundary; mise trust is now present, unlike the earlier session.
- Full onboard installs only the declared Python/uv tool names, resolving their
  versions from mise configuration instead of touching unrelated global tools.
  An initial unconditional install attempted remote version resolution even with
  installed tools; onboard now checks `mise which` first and installs only missing
  tools, making repeat runs work without unnecessary tool downloads.
- Missing-tool fixtures exposed remote metadata resolution before the task body,
  despite `task.run_auto_install=false`. Set mise `offline=true` at repository scope
  to guard direct calls as well as shims; only full onboard's explicit missing-tool
  installer opts into network. Documented the override for deliberate runtime updates.
- Fresh linked-worktree onboarding exposed uv preferring one of its own managed
  interpreters over mise's Python. Onboard now supplies `--python` from `mise which
  python`, preserving mise as the single runtime authority without a duplicate pin.
- User initialized Git on `master`; the structural gate now passes. CI push triggers
  cover both `master` and `main`. No hook manager or remote is configured.

## Operational verification

- `mise tasks validate`: all six tasks valid with mise 2026.4.16.
- Actual `tools/check`: formatting, imports, lint, strict types, security and all
  10 tests pass; coverage remains 100%. Pytest emitted cleanup warnings about older
  shared temp directories; tests in the dedicated fixture directories were clean.
- Actual `tools/build`: both sdists and wheels build successfully.
- Actual `tools/run-tests` called from `/tmp`: paths and `-k echo` selectors forwarded;
  five selected tests pass. Actual `tools/develop` called from `/tmp`: SDK client
  completes an echo request and clean shutdown over stdio.
- All six shims preserve spaces/empty arguments, anchor to a checkout path containing
  spaces, and propagate exit 37 from a fixture backend. Shell syntax checks pass.
- Direct mise and shim `onboard --sync` reject missing Python in an isolated fixture
  without remote resolution; normal sync succeeds with installed tools.
- Fresh dependency setup in a disposable snapshot succeeds. A disposable Git repository
  with an orphan linked worktree (no commits created) exercises full onboard, repeated
  onboard, sync and selected tests. All authored bytes and the existing fixture
  `core.hooksPath`/post-checkout hook stay unchanged. Python is mise's 3.12.13.
- `tools/format` executes on the disposable snapshot without changing Python files.
- `git check-ignore` in the fixture confirms scratch, `.env`, and `.venv` are ignored;
  authored `.github/workflows/ci.yml` stays visible. No cleanup policy existed to migrate.
- Local Markdown links resolve; moved pending ideas and historical research match
  backup bytes. Active path references have migrated. CI check/build commands still
  match mise's constituent commands; no checks or review phases were removed.
- Native runtime/source files and dependency pins are unchanged. No spec approval,
  Autopilot recovery, host projection, release, or deployment capability is claimed.

Fixture trust/cache locations use documented mise directory overrides; only fixture
configs were explicitly trusted in that isolated state. See
[mise directory configuration](https://mise.jdx.dev/directories.html) and
[offline semantics](https://mise.jdx.dev/configuration/settings.html#offline), read
2026-10-04. Local command probes above establish support in the installed version.

## Commit and remote checks

Local setup and structural validation are complete. Actual clean-clone and hosted CI
verification await the initial commit and a remote. The initial commit is being
prepared without committing or pushing. Mise trust is established. Review the
explicit console-name exception above if a broader public command rename is desired.

No pending doc/task moves remain. Keep the ignored originals archive until a safe
commit exists. Disposable validation repositories/environments are removed after
verification; no global hooks or trust records were modified.

## Revalidation against the revised skill

At the fit-policy revalidation, the helper ran successfully through the shared
discovery path and reported only `own-git-worktree` as failing; that failure has
since been resolved by Git initialization. All six mise tasks validate and the real
public `onboard --sync` succeeds. Working runtime/task implementations were preserved;
prior protocol, build, missing-tool and linked-worktree evidence remains applicable.

That revalidation updated the fit assessment and human documentation only. Its originals
are preserved in `docs/dev/tmp/structure-repo-20261004/fit-revalidation-originals.tar.gz`.
No skill source, global policy, host configuration, or optional integration changed.

## Initial commit preparation

Git is initialized on `master`; CI accepts pushes to `master` and `main`.
Moved the example-only asyncio fixture from root `conftest.py` into
`servers/example/tests/conftest.py` and removed the obsolete Pyright include.
The complete `tools/check` passes after this move: 10 tests, 100% coverage,
formatting/import checks, lint, strict typing, and Bandit. A dedicated pytest temp
directory avoids the earlier unrelated cleanup warnings. No commit or push was made.

## Structural helper result

Actual output from the bundled check command, before staging:

```json
{
  "mode": "check",
  "target": "/Users/bob/git/src/github.com/buvis/mcp-servers",
  "structural_gate": "PASS",
  "checks": [
    {
      "check": "own-git-worktree",
      "status": "PASS",
      "evidence": {
        "kind": "worktree",
        "root": "/Users/bob/git/src/github.com/buvis/mcp-servers",
        "git_dir": "/Users/bob/git/src/github.com/buvis/mcp-servers/.git",
        "explicit_worktree": false,
        "hooks_path_config": null,
        "status_porcelain_v1_tokens": [
          "?? .editorconfig",
          "?? .github/",
          "?? .gitignore",
          "?? AGENTS.md",
          "?? README.md",
          "?? docs/",
          "?? mise.toml",
          "?? packages/",
          "?? pyproject.toml",
          "?? servers/",
          "?? tools/",
          "?? uv.lock"
        ],
        "status_truncated": false
      }
    },
    {
      "check": "nonempty-README.md",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 3855
      }
    },
    {
      "check": "nonempty-AGENTS.md",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 1403
      }
    },
    {
      "check": "untracked-docs/dev/tmp",
      "status": "PASS",
      "evidence": {
        "count": 0,
        "paths": []
      }
    },
    {
      "check": "untracked-.agents/autopilot/runtime",
      "status": "PASS",
      "evidence": {
        "count": 0,
        "paths": []
      }
    },
    {
      "check": "executable-tools/onboard",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 122
      }
    },
    {
      "check": "executable-tools/check",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 120
      }
    },
    {
      "check": "executable-tools/format",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 121
      }
    },
    {
      "check": "executable-tools/run-tests",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 124
      }
    },
    {
      "check": "executable-tools/build",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 120
      }
    },
    {
      "check": "executable-tools/develop",
      "status": "PASS",
      "evidence": {
        "kind": "file",
        "bytes": 122
      }
    }
  ],
  "limitations": [
    "Checks core docs, Git boundary, tracked scratch/runtime, known links and shim modes.",
    "No task/hook/release execution or approval/path-consumer validation.",
    "COMPLETE still requires the mode reference's operational evidence."
  ]
}
```
