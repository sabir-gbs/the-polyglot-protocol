# Model-Agnostic Roles Design

Status: **design approved by the maintainer section by section; awaiting review
of this written spec. No implementation has started.**

## Purpose

The Polyglot Protocol exists so users can produce, revise, and optimize
codebases regardless of which AI model they use. The default workflow is Claude
Code and Codex with Sonnet, Opus, Haiku, and gpt-6.1-sol. A user on OpenCode
with open-weight models such as DeepSeek, Kimi, or GLM, or on any other harness,
must get the same quality process from the best available mix of models.

Today `artifact-group-audit-workflow.md` hardcodes one model stack as the
definition of its roles. This design makes the roles and rules fixed and the
role-to-model mapping computed at run time.

## Non-Goals

- Ranking models for general use. The protocol only selects models for its own
  four roles.
- Replacing the Planning, Coding, Guidance-File, or Post-Codegen audits. The
  gate stays additive, as in `artifact-group-audit-workflow.md`.
- Supporting a harness that cannot run headless as a dispatched role. Such a
  harness can only be the orchestrator session (see Harness Classes).

## Decisions Already Made

| Question | Decision |
|---|---|
| How are roles mapped to models? | Roles and capability requirements live in the protocol. Model names never appear in core docs. |
| Static list or dynamic? | **Dynamic.** Models are discovered, filtered, qualified by test, ranked, and locked at run time. |
| What if only one model family is available? | **Degraded mode**, clearly labeled, with a higher pass bar. Not a blocker. |
| Where do profiles live? | A `profiles/` directory, with a per-project override. Profiles hold constraints, pins, and the offline fallback, not the list of record. |
| What counts as a harness? | A program that runs an agent loop with file access and can be driven headless. Model sources (Ollama, OpenRouter, vendor APIs) plug in through harnesses. |
| Degraded pass bar | Mean of `90` or more, no `CRITICAL`. |

## Role Contract

Four roles, defined by capability and permission. This table is the only place
the roles are defined.

| Role | Must be able to | May touch | Count |
|---|---|---|---|
| Orchestrator | Plan long-horizon work, use tools, dispatch roles, apply fixes | Read and write. The only role that edits | 1 |
| Auditor A, Auditor B | Read many files, score ten criteria, verify facts on the web with cited sources, emit the output contract | Read-only. Web allowed. No edits. No spawning | 2 |
| Worker | Read, list, grep, and copy text verbatim | Read only. No web | up to 8 |

The orchestrator is the session the user is already in. Every other role is a
command dispatched through a harness.

### Rules

1. **Independence.** Auditor A and Auditor B come from different model families.
2. **Capability check.** Before dispatch, each model is confirmed able to do what
   its role needs. A model that cannot is a blocker, never a silent
   substitution.
3. **Read-only is verified.** The tree is snapshotted before and after each
   auditor or worker run. Any change invalidates that run, whatever the harness
   claims.
4. **Degraded mode.** If two families are not available, two different models
   from one family are allowed. The audit log records `degraded independence`,
   the pass bar rises to `90`, and the deterministic checks must pass. Running
   the same model twice is a blocker.

## Resolution Pipeline

A deterministic script (`scripts/resolve-roles.py`) performs resolution. A model
never chooses its own role, so no model can favor itself.

1. **Discover.** Ask each available harness which models it can run (for example
   `opencode models`, `agy models`, or the harness's own list). Read capability
   metadata for each model from a public registry. The default registry is
   `models.dev`, which OpenCode also uses and which carries tool-call support,
   context size, cost, licence, `open_weights`, and release date.
2. **Filter.** Apply hard requirements per role: tool calling, minimum context,
   a web tool for auditors, an allowed provider, a licence that fits the user's
   constraints, a cost ceiling. A model whose licence is unknown is `unverified`
   and passes only when the user's licence constraint is `any`.
3. **Qualify by test.** Run each candidate against the qualification fixture
   (see below). A model that fails is excluded regardless of vendor claims.
4. **Rank** only qualified models. Prefer independent evidence over
   self-reported numbers. Assign Auditor A and Auditor B from different families
   when possible.
5. **Lock.** Write the result, with sources and timestamps, to the lock file and
   copy it into the audit log. Reuse the lock until it expires or a new model
   appears for a role.

### Principles

- **New is not better.** A model released recently with no independent evidence
  can fill the worker role or be listed as a candidate. It becomes an auditor
  only after passing the qualification probe.
- **Qualify by test, not by reputation.** The probe is the gate.
- **Always a defined answer.** If discovery fails or the machine is offline, the
  resolver uses the selected profile's fallback roles.

### Qualification Fixture

A small, versioned directory of files with known planted defects, plus a checker
script that scores a model's output.

- **Auditor probe:** the fixture contains a stale version pin, a broken path,
  and a fabricated verification claim. The auditor must report each, emit ten
  valid `VERDICT` lines, and mark an unverifiable claim `UNVERIFIED` instead of
  inventing a source. It is run twice with the files in different order to catch
  position bias.
- **Worker probe:** copy a block of text verbatim. Any difference fails.
- **Orchestrator:** no probe. It is chosen by capability filter and user pin,
  because a faithful probe of long-horizon planning would cost more than it
  proves.
- A model is re-qualified only when its identifier, harness, or the fixture
  version changes.

### Lock File

`resolved-roles.json`, written to the workflow-run directory and copied into the
audit log. Fields:

| Field | Meaning |
|---|---|
| `resolved_at` | UTC timestamp |
| `expires_at` | UTC timestamp; default 7 days after `resolved_at` |
| `independence` | `full` or `degraded` |
| `registry` | Source URL and the timestamp it was read |
| `profile` | Name of the profile applied |
| `fixture_version` | Version of the qualification fixture |
| `roles` | Map of role to `{harness, model, family, qualified, evidence}` |
| `rejected` | Models considered and excluded, with the reason |

The scorer reads `independence` from this file. There is no second source.

## Harness Adapters

### Harness Classes

| Class | Definition | Can fill |
|---|---|---|
| Dispatchable | Runs headless with a prompt and a model, and prints the final answer | Any role |
| Session-only | Interactive or GUI only | Orchestrator only |

A user whose only harness is session-only runs the other roles sequentially in
the same session with fresh context, and the gate is always in degraded mode.

### Capability Contract

The resolver tests each of these and records the result. Nothing is assumed.

| Capability | Required for |
|---|---|
| Run headless with a prompt file | Auditor, Worker |
| Select a model per invocation | Auditor A and B from different models in one harness |
| Print the final answer to stdout | Auditor, Worker |
| Enforce read-only | Preferred; always backed by the snapshot check |
| Web tool | Auditor |
| Parallel fan-out | Worker |

A harness that cannot select a model per invocation is `fixed-model per
configuration`. It can fill one role, not several with different models.

### Harness Families

A harness is `multi-family` when it exposes models from more than one family
(for example OpenCode, or Antigravity depending on plan) and `single-family`
otherwise. A multi-family harness can satisfy the independence rule alone. A
single-family harness needs a second harness, or degraded mode.

### Unknown Harnesses

A harness the protocol does not know needs one command template in the profile
with `{model}` and `{prompt_file}` placeholders. It must run headless and print
the final answer to stdout. The resolver probes everything else.

### Observed Harnesses

Observed on 2026-10-11 from each tool's own `--help` or official documentation.
Adapter files record these with a verified-on date, and the resolver re-probes
them.

| Harness | Headless | Model per run | Read-only mechanism observed | Notes |
|---|---|---|---|---|
| Codex | `exec` | `-m` | `--sandbox read-only` (OS level) | |
| Claude Code | `-p` | `--model` | `--allowedTools`, `--disallowedTools` | |
| OpenCode | `run` | `-m provider/model` | per-agent `permission` config | Scripted auditors need `mode: "all"`, not `subagent`, or `--agent` silently falls back to the default agent. Subagent depth defaults to 1. |
| Grok | `-p/--single`, `--prompt-file` | `-m` | `--allowedTools`, `--disallowed-tools` | Single family |
| Gemini CLI | `-p` | `-m` | `--approval-mode`, `--sandbox` | |
| Cursor Agent | `-p` | `--model` | `--mode plan` (planning, no edits) | |
| Pi | `-p` | `--model` | `--tools` allowlist | |
| Crush | `run` | `-m provider/model` | none observed | Relies on the snapshot check |
| Copilot | `-p` | `--model` | `--deny-tool` / `--allow-tool` permission rules | No OS-level read-only observed; backed by the snapshot check |
| ZCode | `-p` | **no flag**; session level | `--mode plan`, `--disallowed-tools` | Default `--mode` for `-p` is `yolo`. `--version` and `--help` report different version numbers. Fixed model per configuration. |
| Antigravity (`agy`) | `-p` | `--model <slug>`, `agy models` | **none documented**; `plan` mode uses read-only tools | Default mode pauses for review; headless needs `permissions.allow` rules or `--dangerously-skip-permissions` |
| Ollama | none | n/a | n/a | A model runner, not a harness |

Antigravity was verified from Google's documentation but is not installed on
the reference machine, so its row is documentation-derived, not probe-derived.

### Safest Invocation

Each adapter records the least-permissive invocation observed for each role,
not just any working one. For example, a ZCode auditor is launched with
`--mode plan` and write tools disallowed rather than the `-p` default.

## Gate And Scorer

| Mode | Pass rule | Extra requirements |
|---|---|---|
| Full independence | Mean `85` or more, no `CRITICAL` | None |
| Degraded | Mean `90` or more, no `CRITICAL` | Two different models, deterministic checks pass, `degraded independence` in the audit log |

`scripts/score-audit-gate.py` changes:

- Read `independence` from the lock file and derive the threshold.
- Reject thresholds below the floor for the mode, and above `100`.
- Reject any line starting with `VERDICT`, `TOTAL`, or `FINDING` that does not
  match the contract, instead of ignoring it.
- Require both auditors' criterion names to be identical.
- Print the mode on the `GATE:` line.

These also close the defects found by `sol-auditor` in round 1.

## Profiles

Files in `profiles/` are Markdown with a small structured header. A project may
add a file at `.polyglot/profile.md` to override or replace the default.

| Field | Meaning |
|---|---|
| `name` | Profile name |
| `harnesses` | Harness command templates and the roles each may fill |
| `constraints` | `allowed_providers`, `max_cost_per_mtok`, `licence_policy` (`any`, `permissive`, `commercial-ok`), `local_only` |
| `pins` | Optional role to model overrides, for example a fixed orchestrator |
| `fallback` | Role to `{harness, model}`, used when discovery is unavailable |
| `verified_on` | Date the fallback was last checked |
| `sources` | URLs that support the fallback choices |

Shipped profiles: `default` (Claude Code and Codex), `opencode-open-weights`,
and `template`.

### Example Fallback For Open-Weight Stacks

Verified 2026-10-11 from model cards, models.dev, and the DeepSWE leaderboard.
Almost every benchmark figure is vendor-reported; only DeepSWE is independent.
This is a fallback example, not a ranking, and the resolver replaces it when it
can.

| Role | Model | Basis |
|---|---|---|
| Orchestrator | GLM-5.3 | Independent DeepSWE 69%, 1M context |
| Auditor A | Kimi K3 | Strongest reported web and tool-use profile; independent DeepSWE 69% |
| Auditor B | DeepSeek V4.1-Flash | Different family, MIT licence, cheap; headline numbers vendor-reported |
| Worker | MiMo-V2.6-Flash, or local Qwen3.8-27B | Cheap and fast; local option is Apache-2.0 |

Licence notes: Kimi K3, GLM-5.3, and MiniMax-M3 carry licences with revenue or
commercial-use conditions. The resolver surfaces these under `licence_policy`.

## Error Handling

| Situation | Behavior |
|---|---|
| Registry unreachable | Use the profile fallback; record `registry: unavailable` in the lock |
| Model fails the probe | Exclude it, record it in `rejected`, try the next candidate |
| No qualified auditor | Blocker. Stop the gate and report. Never self-audit silently |
| Only one family qualifies | Degraded mode |
| Same model would fill both auditor roles | Blocker |
| Snapshot differs after an auditor or worker run | That run is invalid; record the changed paths; re-dispatch once |
| Harness missing or not headless | Record as session-only or unavailable; try another harness |
| Lock expired | Re-resolve; reuse qualifications still valid for the fixture version |
| Unknown licence | `unverified`; passes only under `licence_policy: any` |

## Components And Files

New:

- `scripts/resolve-roles.py`
- `scripts/dispatch-role.py` (runs a command template, snapshots the tree, captures the answer)
- `qualification/` (fixture and checker)
- `profiles/default.md`, `profiles/opencode-open-weights.md`, `profiles/template.md`
- `docs/workflow/role-resolution.md` (resolver spec, adapter format, observed-harness table)

Changed:

- `docs/workflow/artifact-group-audit-workflow.md`: capability-based roles, no model names
- `docs/workflow/dev-workflow.md`, `SKILL.md`, `readme.md`, `docs/AGENTS.md`
- `adapters/*`: collapse to a pointer at the profile for their harness
- `scripts/score-audit-gate.py` and its tests
- `scripts/validate-workspace.py`: check profile fields, and warn when a profile's `verified_on` is older than 30 days

## Testing

- **Unit tests, offline:** the scorer, the resolver against a recorded registry
  snapshot, the probe checker, and the snapshot diff logic.
- **Live probes:** run by hand against the harnesses installed on the reference
  machine and recorded in the audit log. They are not part of validation,
  because they need credentials and network.
- **Negative tests:** a model that passes a claim without evidence, a harness
  that writes a file, an expired lock, a malformed contract line.

## Risks Accepted

- Probes cost tokens whenever a new model is qualified.
- `models.dev` is a third-party registry. The lock records its source and time,
  and the profile fallback covers an outage.
- The fixture measures only what it plants. It is versioned so it can grow.
- A resolved lock is only as current as its expiry. Seven days is a default, not
  a guarantee.

## Order Of Work

1. **Foundation.** Scorer fixes and degraded mode, the role contract, and the
   profiles. Small, and it makes every later re-audit trustworthy.
2. **Round 2 of the upgrade plan.** Apply the P0 fixes from
   `polyglot-protocol-upgrade-plan.md` and re-run the gate.
3. **Dynamic layer.** Resolver, qualification fixture, and dispatcher, tested
   against the installed harnesses.

## Validation Rollback And Risk

- Validation: `python scripts/validate-workspace.py`, the unit tests, and a gate
  run per artifact group.
- Rollback: each order-of-work step is a separate commit and can be reverted
  alone.

## Refactoring Playbook

`N/A`; new components, not a refactor of existing code. The scorer changes follow
`docs/languages/python/python.md`.

## Baseline URL KPI Docker Lighthouse CloakBrowser Deployment

All `N/A`; no web surface, container, or deployment is affected.
