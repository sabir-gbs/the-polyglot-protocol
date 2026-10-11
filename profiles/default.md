# Default Profile

The default stack: Claude Code as the orchestrator session, with Codex and a
second Claude model as independent auditors. Model identifiers live only in
this file.

```json
{
  "name": "default",
  "harnesses": {
    "claude-code": {
      "command": "claude -p --model {model} --disallowedTools Edit Write NotebookEdit Bash < {prompt_file}",
      "roles": ["orchestrator", "auditor_b", "worker"]
    },
    "codex": {
      "command": "codex exec --sandbox read-only --skip-git-repo-check -m {model} --output-last-message {output_file} \"$(cat {prompt_file})\"",
      "roles": ["auditor_a"]
    }
  },
  "constraints": {
    "allowed_providers": [],
    "max_cost_per_mtok": null,
    "licence_policy": "any",
    "local_only": false
  },
  "pins": {},
  "fallback": {
    "orchestrator": {"harness": "claude-code", "model": "claude-sonnet-5-5"},
    "auditor_a": {"harness": "codex", "model": "gpt-6.1-sol"},
    "auditor_b": {"harness": "claude-code", "model": "claude-opus-5-5"},
    "worker": {"harness": "claude-code", "model": "claude-haiku-5-5"}
  },
  "verified_on": "2026-10-11",
  "sources": [
    "https://platform.claude.com/docs/en/about-claude/models/overview",
    "codex exec -m gpt-6.1-sol answered on the reference machine on 2026-10-11"
  ]
}
```

Auditor A and Auditor B come from different families (OpenAI and Anthropic), so
this profile runs the gate in `full` independence.

Command placeholders: `{model}` is the model identifier from `fallback` or
`pins`, `{prompt_file}` is the path of the file holding the role prompt, and
`{output_file}` is the path where the harness writes its final answer (used by
Codex through `--output-last-message`; Claude Code prints the answer to stdout).
