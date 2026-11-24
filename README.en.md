# JoyStack

[Chinese](README.md) | English

JoyStack is a set of engineering Skills for coding agents. Describe a goal, and the agent selects the capabilities it needs: understanding, planning, implementation, verification, debugging, review, and Git delivery. Straightforward changes stay short; complex work gets the checks and handoffs it needs.

It runs with the host's existing model, tools, and permissions. It does not provide a separate agent runtime or require another Skill suite. Available actions depend on the host and the project's authorization.

## Get started

Install the complete module set in a host that supports Agent Skills. These commands use the [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) and require a Node.js environment capable of running `npx`.

For a project-level installation, run this from the target project:

```bash
npx skills add youngjunning/joystack
```

For use across projects, choose a global installation:

```bash
npx skills add youngjunning/joystack -g
```

Select the modules and target host when prompted, and check the installation scope and location. On platforms that only support file imports, follow the platform's workflow to import each complete Skill directory, including its supporting files. Installation does not run project tasks, initialize runtime data, or perform Git delivery.

## Everyday use

There is no need to memorize or invoke each module. Describe the task and its constraints, for example:

- "Explain how the upload path works today. Do not change code yet."
- "Fix intermittent failures when uploading large files and add a regression test."
- "Check whether this change meets the original goal, then reverify the issues found."
- "List these repositories' worktrees, their purposes, and cleanup conditions. Do not delete anything yet."
- "Prepare a handoff so the next session can continue. Do not commit this time."

The agent selects from the Skills available in its host. Missing modules, tools, permissions, or an independent reviewer must be reported; checks that were not run must not be presented as passed.

## Engineering capabilities

| Module | When to use it | Main result |
| --- | --- | --- |
| [joy-stack](skills/engineering/joy-stack/SKILL.md) | Work crosses boundaries, is underspecified, or needs verification and continuation | Selects necessary modules and keeps a shared task boundary |
| [joy-token](skills/engineering/joy-token/SKILL.md) | Token-efficient execution, oversized context, repeated calls, or an explicit savings request | Targeted reads and compact tool output without changing the chosen model or quality gates |
| [joy-understand](skills/engineering/joy-understand/SKILL.md) | Behavior, causes, or impact are unclear | Current facts, sources, inferences, and unknowns |
| [joy-shape](skills/engineering/joy-shape/SKILL.md) | Scope, tradeoffs, or acceptance criteria are unresolved | An implementable goal, boundaries, and acceptance criteria |
| [joy-build](skills/engineering/joy-build/SKILL.md) | The implementation goal is clear | A small, feedback-ready change with local verification |
| [joy-test](skills/engineering/joy-test/SKILL.md) | Testing strategy, TDD, test cases, Web/API acceptance or Agent evals | Test implementation, execution evidence, failure classification and quality governance; not overall delivery approval |
| [joy-verify](skills/engineering/joy-verify/SKILL.md) | A result needs evidence | Test or acceptance evidence and uncovered boundaries |
| [joy-debug](skills/engineering/joy-debug/SKILL.md) | Something fails, behaves unexpectedly, or regresses in performance | Reproduction, root cause, a fix, and regression protection |
| [joy-review](skills/engineering/joy-review/SKILL.md) | A change needs independent inspection | Findings and a review verdict against the original goal |
| [joy-loop](skills/engineering/joy-loop/SKILL.md) | A behavioral change needs review, fixes, and reverification | APPROVE or BLOCKED after a bounded review cycle |
| [joy-govern](skills/engineering/joy-govern/SKILL.md) | Documentation, tests, rules, or Git hygiene need maintenance | Evidence-backed maintenance findings and minimal actions |
| [joy-git](skills/engineering/joy-git/SKILL.md) | Commit, push, PR, merge, or worktree management is needed | Git delivery evidence and task-directory lifecycle state |
| [joy-continue](skills/engineering/joy-continue/SKILL.md) | Work continues across sessions, pauses, or changes hands | A verifiable handoff that supports continuation |

Modules are discovered and loaded by Skill name from the current host, without requiring adjacent installation directories. Each Skill resolves its own `references/`, `scripts/`, and assets from its entrypoint directory. Links in this README are for browsing source files.

### Testing work

joy-test owns testing strategy, test-first development, unit/integration/contract tests and critical E2E journeys, Web/API/accessibility environments, property/fuzz/mutation tests, AI/Agent evals and test quality. Select only the branches justified by current risk. joy-build owns product implementation, joy-verify aggregates delivery evidence, and joy-loop retains the same review loop. If joy-test is missing, use available tools only for claims they can prove, report uncovered required test gates, and never auto-install it or treat a passing build as passing tests.

The module moved from joyally-test on November 24, 2026. Use joy-test as the installation identity; its five testing references and source attribution are included without requiring the retired entrypoint. See [testing source review](skills/engineering/joy-test/references/source-review.md).

## How work is handled

The November 24, 2026 [method completion record](skills/engineering/joy-stack/references/matt-method-completion.md) maps separate review axes, executable diagnosis, active domain modeling, module interfaces, logic/UI prototypes, primary research and architecture audits to existing modules. Research belongs to joy-understand, domain/interface/prototype decisions to joy-shape, and architecture-friction candidates to joy-govern. Design and diagrams retain their specialist owners; no retired Matt entrypoints or mandatory all-stage workflow are required.

- **Establish scope first.** Current code, configuration, and runtime state are the sources of truth. Historical summaries are pointers, not current evidence. Other tasks' files and uncommitted changes are preserved.
- **Match checks to risk.** Small changes do not require the full suite of workflows. Behavioral changes use `joy-loop` for independent review, fixes, and reverification; unresolved important issues retain a clear blocking reason.
- **Report evidence separately.** Tests, builds, commits, pushes, deployments, and real business outcomes are confirmed independently. Success at one step does not prove the next step is complete.
- **Deliver within authorization.** Platform permissions are the upper bound; project rules and the user's current request govern specific actions. Authorized automatic delivery proceeds normally. Installing Skills does not grant permission to commit, push, merge, delete, or publish.

See the [suite contract](skills/engineering/joy-stack/references/stack-contract.md) for detailed inputs, outputs, and handoff conditions.

## Worktree management

`joy-git` covers creation, purpose registration, continuation, and cleanup decisions as one task-directory lifecycle. Its helper uses native Git and the Python 3.9+ standard library, with no Worktrunk dependency.

Persistent runtime data defaults to **`.joystack` under the user home directory resolved by the current environment**. The environment determines home; it is not a hard-coded account path or inferred from the working directory or workspace.

```text
~/.joystack/
├── worktrees/
│   └── <repo>-<repository-id>/<task-slug>/
└── state/
    ├── worktrees.json
    └── worktrees.json.lock
```

- Creation plans do not write by default. Actual creation records the task, session, base commit, target branch, and cleanup conditions.
- The inventory covers registered or explicitly selected repositories. Unknown purposes, read failures, and unchecked occupancy are reported separately.
- Existing directories and host-managed worktrees are not automatically moved or claimed. Age alone can prompt review, not deletion.
- Cleanup plans do not delete directories. Actual cleanup requires checks for adopted work, unsaved files, retention reasons, active sessions and processes, and valid authorization.

An explicit `JOYSTACK_HOME` configuration can override the data root. Restricted platforms supply an allowed path boundary through `JOYSTACK_WORKSPACE` or `--workspace`. That boundary does not redefine home: an incompatible default location must be reported rather than silently relocated to the working directory. Path checks do not replace the platform sandbox or exempt native side effects such as Git hooks.

See the [worktree lifecycle](skills/engineering/joy-git/references/worktrees.md) for operations and the [global directory contract](skills/engineering/joy-stack/references/global-home.md) for paths and platform adaptation.

## Updating

Before updating, check the installation source, project or global scope, and any local customizations. Preserve changes that need to be kept. Do not use an overwrite to resolve conflicts or delete `.joystack` or existing worktrees.

### Installed with the Skills CLI

From the original project directory, update the existing JoyStack modules:

```bash
npx skills update -p joy-stack joy-understand joy-shape joy-build \
  joy-test joy-verify joy-debug joy-review joy-loop joy-govern joy-git joy-continue joy-token
```

For a global installation, use the same command with `-g` instead of `-p`. Naming the modules avoids updating unrelated suites. This updates installed, CLI-tracked modules in the selected scope. To add modules introduced upstream, rerun `skills add` in the appropriate scope and select the complete module set. Refer to the [CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) and `npx skills --help` for available options.

### Used from a source checkout

If the installed Skill entrypoints link to a local JoyStack repository, inspect that checkout first. After preserving changes that need to be kept and confirming the upstream, update by fast-forward:

```bash
git status --short --branch
git pull --ff-only
```

Stop if history has diverged or conflicts require a decision; do not force an overwrite. Symlinks resolve to the updated source. If the installation uses copies, synchronize the reviewed Skill directories using the original installation workflow.

### Imported through a platform

Obtain the selected version again, back up local customizations, and use the platform's update or replacement workflow to import each complete Skill directory. Keep supporting references, scripts, LICENSE, and NOTICE files together; do not mix versions of unknown provenance. If the platform has no update action, do not uninstall the old version on your own.

After updating, check that the host can discover the required modules. Reload requirements depend on the host. Skill files and `.joystack` runtime data are managed separately: updates do not automatically clear records, move directories, or rerun historical tasks.

## Development and verification

On November 23, 2026, JoyStack selectively incorporated tstack methods for semantic refresh of old changes, takeover credit, problem-first PR communication, observation versus merge gates, and bounded review lifecycles. These extend existing modules: no Full Send/Stop controllers, watcher runtime, or mandatory three-provider council were added. See the [integration record](skills/engineering/joy-stack/references/tstack-integration.md) for mappings, twelve cases and evidence limits, and the [implementation plan](docs/plans/2026-11-23-tstack-integration.md). Static contract tests do not establish real PR/MR or multi-model execution success.

`skills/engineering/` contains the maintained module sources; `catalog.json` is the catalog. Run these commands from the repository root:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s skills/engineering/joy-git/scripts -p 'test_*.py'
```

Validation checks module metadata, catalog consistency, bundled resources, and the public-content boundary. Tests cover independent mounts and worktree management. On restricted platforms, test temporary directories follow the workspace rules.

When changing capabilities, update the module contracts, catalog, and both READMEs. Preserve author metadata, attribution, and license files. Report only the verification actually performed; documentation and local tests do not substitute for acceptance in the target platform.

## Sources and license

JoyStack is distributed under the [MIT License](LICENSE).

- Engineering-method sources have separate records: [Matt Pocock Skills](skills/engineering/joy-stack/references/matt-pocock-integration.md), [Lauren Tan's pstack](skills/engineering/joy-stack/references/pstack-integration.md), and [Theo Browne's tstack](skills/engineering/joy-stack/references/tstack-integration.md). Each records provenance, the reviewed snapshot, current method mapping, exclusions, and evidence limits. Unknown original versions remain unknown; a fresh review snapshot is not presented as historical provenance. The [current Matt/pstack comparison](docs/research/2026-11-23-matt-pstack-current-comparison.md) separates coverage, gaps, and recommendations not yet implemented.
- [Oil dev skills](https://github.com/oil-oil/oil-dev-skills) is a method source only, never an installed, invoked, optional execution or fallback dependency. JoyStack and existing host tools provide the capabilities. See the [oil integration record](skills/engineering/joy-stack/references/oil-dev-integration.md) and the complete [integration index](skills/engineering/joy-stack/references/integration-sources.md).
- `joy-loop` is adapted from `sol-loop` in [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/11e37a74d0a6868c121cd0910ab2b3bd9873b92a), retains the [upstream MIT license](skills/engineering/joy-loop/LICENSE), and documents its original author and adaptation scope in [NOTICE](skills/engineering/joy-loop/NOTICE.md).
- `joy-token` independently expresses selected ideas from [codex-token-skills](https://github.com/lokikill123/codex-token-skills), adapted to official GPT/Sol mechanisms and JoyStack quality gates. Its [source record](skills/engineering/joy-token/references/sources.md) identifies the reviewed snapshot, excluded rules, and measurement limits. Cache hits, total tokens, and billing savings require separate evidence.

These references are not runtime dependencies. JoyStack can be used without installing the upstream suites.
