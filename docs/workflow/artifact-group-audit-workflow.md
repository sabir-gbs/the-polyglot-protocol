# Artifact Group Audit Workflow

## Purpose

This document defines the standard audit workflow for every add, change, and
update request that produces artifacts. Work is split into artifact groups, and
each group passes an independent dual-auditor gate before the next group starts.

It extends `dev-workflow.md`. It does not replace the audit loops defined there.

## Scope And Precedence

- Applies to code, guidance files, scripts, and documentation produced by a
  request. A request with one group runs the gate once.
- Passing this gate lets work move to the next group. It is not a completion
  claim.
- The following remain in force and are not weakened by this gate:
  - Planning Audit Loop, Coding Audit Loop, and Guidance-File Audit Loop in
    `dev-workflow.md`
  - Post-Codegen Protocol Audit in `dev-workflow.md`, which still targets
    `10/10` per criterion for the whole affected codebase
  - language-specific audits such as the Python Ten-Round Audit
- When a stricter rule applies to the completion claim, the stricter rule wins.
- Keep all existing content. If rules overlap, follow the guidance priority in
  `dev-workflow.md`.

## Roles

Roles are defined by capability and permission. Which model fills a role comes
from the selected profile (see `role-resolution.md`), never from this document.

| Role | Must be able to | May touch | Count |
|---|---|---|---|
| Orchestrator | Plan long-horizon work, use tools, dispatch roles, apply fixes | Read and write; the only role that edits | 1 |
| Auditor A, Auditor B | Read many files, score ten criteria, verify facts on the web with cited sources, emit the output contract | Read-only; web allowed; no edits; no spawning | 2 |
| Worker | Read, list, grep, and copy text verbatim | Read only; no web | up to 8 |

The orchestrator is the session the user is already in. Every other role is a
command dispatched through a harness.

Rules:

- Auditors are read-only and never edit files.
- Auditors run in parallel and must not see each other's output.
- Only the orchestrator fixes findings.
- **Independence.** Auditor A and Auditor B come from different model families.
- **Capability check.** Before dispatch, confirm each model can do what its role
  needs. A model that cannot is a blocker. Do not substitute a different model
  or self-audit silently.
- **Read-only is verified.** Snapshot the tree before and after each auditor or
  worker run. Any change invalidates that run, whatever the harness claims.
- **Degraded mode.** If two families are not available, two different models from
  one family are allowed. Record `degraded independence` in the audit log. The
  pass bar rises to `90` and the deterministic checks must pass. Running the same
  model twice is a blocker.

## Artifact Group

An artifact group is a set of related files that can be reviewed as one unit,
such as one language guidance file with its readme, or one script with its
tests. Build each group as:

- the files in the group
- an audit prompt that names the criteria set, the output contract below, and
  the files to read

## Procedure

Run these steps for each artifact group.

1. **Prep.** The orchestrator dispatches up to 8 workers to read,
   list, and grep the group's files. This builds the file inventory and
   surfaces obvious defects before audit.
2. **Audit.** Auditor A and Auditor B run in parallel against the same
   files and the same audit prompt. Each scores 10 criteria out of 100.
3. **Check.** One worker greps each auditor's verdict lines and severity
   tags and copies them verbatim into the audit log. It does not summarize or
   interpret them.
4. **Score.** The orchestrator re-adds each auditor's criterion scores and
   takes the mean of the two totals by running:

   ```sh
   python scripts/score-audit-gate.py <auditor-a-output> <auditor-b-output> \
     [--lock resolved-roles.json | --independence full|degraded]
   ```

   The script ignores each advertised `TOTAL`, reports any discrepancy, rejects
   malformed contract lines and mismatched criterion names, and exits `0` when
   the gate passes, `1` when it fails, and `2` when an input is invalid. Record
   its output in the audit log.

   With neither `--lock` nor `--independence` the scorer assumes `full` and uses
   `85`, so in degraded mode always pass `--independence degraded` or `--lock`.
   The lock file wins, and a conflicting `--independence` exits `2`.
5. **Gate.** In `full` independence the group passes when the mean is `85` or
   more. In `degraded` independence the mean must be `90` or more. In both modes
   neither auditor may raise a `CRITICAL` finding.
6. **Fix or stop.**
   - Pass: record the result, start the next group, and queue the group for
     maintainer review.
   - Fail in gate round 1 or 2: the orchestrator fixes every finding,
     including non-`CRITICAL` ones, then repeats from step 1 as gate round + 1.
   - Fail after gate round 3: stop. Report findings and scores to the
     maintainer. Do not start another gate round without instruction.

Gate rounds are counted per artifact group and are separate from the planning,
coding, and guidance-file audit rounds in `dev-workflow.md`.

## Auditor Output Contract

Auditors must emit greppable lines so the check step can copy them verbatim:

```text
VERDICT <criterion name>: <score>/10
TOTAL: <sum>/100
FINDING <CRITICAL|MAJOR|MINOR> <file>:<line> <one-line summary>
```

- One `VERDICT` line per criterion, ten in total.
- `TOTAL` is advisory. The orchestrator uses its own re-added total. If the two
  differ, record the discrepancy and use the re-added value.
- `CRITICAL` means the artifact is unsafe, incorrect, or misleading enough that
  it must not be accepted: security or data-loss risk, a violation of
  `docs/languages/do-not-generate-policy.md`, fabricated evidence, or a false
  completion claim.
- `MAJOR` and `MINOR` do not block the gate but must still be fixed in the fix
  step.
- An auditor output is invalid if it has anything other than ten `VERDICT`
  lines, a score outside `0` to `10`, a contract line that is malformed,
  indented or decorated (bulleted, quoted or bold) instead of starting at
  column 0, or criterion names that differ from the other auditor's. The scorer
  exits `2` for each. Re-dispatch that auditor once without counting a gate
  round and record the invalid output. If the second output is also invalid,
  record a blocker and stop the gate for that group.

## Criteria By Artifact Type

Use the existing ten-criterion set that matches the group. Do not invent new
criteria.

| Artifact group | Criteria source |
|---|---|
| Plans and implementation or execution plans | Planning Audit Criteria in `dev-workflow.md` |
| Generated code and language guidance | `docs/languages/scoring-rubric.md` |
| Workflow or guidance files (`AGENTS.md`, `SKILL.md`, workflow docs) | Guidance-File Audit Criteria in `dev-workflow.md` |
| Python code | Production Audit Workflow criteria in `docs/languages/python/python.md` |

## Audit Log Requirements

Record each round in `docs/workflow/<request-slug>-audits.md`:

- group name and round number
- files audited
- each auditor's criterion scores and the orchestrator's re-added totals
- the mean score and the gate decision
- every finding with severity, copied verbatim
- fixes applied between rounds
- any unavailable model, skipped step, or `N/A` with evidence
- the independence mode (`full` or `degraded`) and the lock file or profile that
  produced the role mapping

## N/A And Blocker Rules

- Never fabricate an auditor result, score, or severity tag.
- If an auditor model is unavailable, record `status`, `reason`, `evidence`, and
  `follow-up requirement if scope changes`. If a second model from another
  family is available the gate continues; if only one family is available it
  continues in degraded independence. Only the absence of two different
  qualified models stops the gate for that group.
- If a group fails after round 3, the blocker is the failed gate itself.
  Report it. Do not lower the threshold to pass.
