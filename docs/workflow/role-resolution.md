# Role Resolution

How the audit gate's four roles are filled by models, and how harnesses are
treated. The role contract itself lives in `artifact-group-audit-workflow.md`.
The design rationale is in `model-agnostic-roles-design.md`.

## Status

The profile format and the harness reference below are in force. The automatic
resolver (`scripts/resolve-roles.py`), the dispatcher
(`scripts/dispatch-role.py`), and the qualification fixture are a later plan and
are not implemented yet. Until they exist, role-to-model mapping comes from the
selected profile's `fallback` block.

## Profile Selection

1. A project profile at `.polyglot/profile.md`, if present.
2. Otherwise a named profile in `profiles/`.
3. Otherwise `profiles/default.md`.

A profile is Markdown with one ` ```json ` block. Required keys: `name`,
`harnesses`, `constraints`, `pins`, `fallback`, `verified_on`, `sources`.
`scripts/validate-workspace.py` validates the shipped files in `profiles/` and
warns when `verified_on` is older than 30 days. A project profile at
`.polyglot/profile.md` is not validated yet.

## Harness Classes

| Class | Definition | Can fill |
|---|---|---|
| Dispatchable | Runs headless with a prompt and a model, and prints the final answer | Any role |
| Session-only | Interactive or GUI only | Orchestrator only |

A user whose only harness is session-only runs the other roles sequentially in
the same session with fresh context, and the gate is always degraded.

## Model Sources Are Not Harnesses

Ollama, OpenRouter, and vendor APIs are model sources. They are reached through
a harness that supports them. A model runner with no agent loop and no file
tools cannot fill an auditor role by itself.

## Capability Contract

Each capability is tested, never assumed.

| Capability | Required for |
|---|---|
| Run headless with a prompt file | Auditor, Worker |
| Select a model per invocation | Auditor A and B from different models in one harness |
| Print the final answer to stdout | Auditor, Worker |
| Enforce read-only | Preferred; always backed by the snapshot check |
| Web tool | Auditor |
| Parallel fan-out | Worker |

A harness that cannot select a model per invocation is `fixed-model per
configuration`: it can fill one role, not several with different models.

A harness is `multi-family` when it exposes models from more than one family and
`single-family` otherwise. A multi-family harness can satisfy the independence
rule alone. A single-family harness needs a second harness, or the gate runs in
degraded independence.

## Read-Only Is Verified

Before each auditor or worker run, snapshot the tree (for example
`git status --short` plus a hash of every modified and untracked file). After
the run, compare. Any change invalidates that run: record the changed paths and
re-dispatch once. This works for every harness, including unknown ones.

## Unknown Harnesses

Add one command template to the profile's `harnesses` block with `{model}` and
`{prompt_file}` placeholders. It must run headless and print the final answer to
stdout. Everything else is probed.

Placeholders in command templates: `{model}` and `{prompt_file}` are required;
`{output_file}` is a path the harness should write its final answer to when its
CLI supports that; `{agent}` is the harness agent configured for the role, taken
from the harness entry's `agents` map.

## Observed Harnesses

Observed on 2026-10-11 from each tool's own `--help` or official documentation.
Re-probe before relying on a row.

| Harness | Headless | Model per run | Read-only mechanism observed | Notes |
|---|---|---|---|---|
| Codex | `exec` | `-m` | `--sandbox read-only` (OS level) | |
| Claude Code | `-p` | `--model` | `--allowedTools`, `--disallowedTools` | |
| OpenCode | `run` | `-m provider/model` | per-agent `permission` config | Scripted auditors need `mode: "all"`: with `mode: "subagent"`, `opencode run --agent` silently falls back to the default agent and loses its read-only permissions. Subagent depth defaults to 1 |
| Grok | `-p/--single`, `--prompt-file` | `-m` | `--allowedTools`, `--disallowed-tools` | Single family |
| Gemini CLI | `-p` | `-m` | `--approval-mode`, `--sandbox` | |
| Cursor Agent | `-p` | `--model` | `--mode plan` (planning, no edits) | |
| Pi | `-p` | `--model` | `--tools` allowlist | |
| Crush | `run` | `-m provider/model` | none observed | Relies on the snapshot check |
| Copilot | `-p` | `--model` | `--deny-tool` / `--allow-tool` rules | No OS-level read-only observed |
| ZCode | `-p` | none; session level | `--mode plan`, `--disallowed-tools` | `-p` defaults to `yolo`; fixed model per configuration |
| Antigravity (`agy`) | `-p` | `--model <slug>` | none documented | Default mode pauses for review; headless needs `permissions.allow` or `--dangerously-skip-permissions`. From documentation, not probed |
| Ollama | none | n/a | n/a | Model runner, not a harness |

## Safest Invocation

Record the least-permissive invocation observed for each role, not just any
working one. For example, launch a ZCode auditor with `--mode plan` and write
tools disallowed rather than the `-p` default.
