# OpenCode Open-Weight Profile

An example fallback for users running OpenCode with open-weight models. The
resolver replaces it when discovery works. Almost every benchmark figure behind
these choices is vendor-reported; only the DeepSWE leaderboard is independent.

Licence notes: Kimi K3, GLM-5.3, and MiniMax-M3 carry licences with revenue or
commercial-use conditions. Set `licence_policy` to `permissive` or
`commercial-ok` if that matters to you.

```json
{
  "name": "opencode-open-weights",
  "harnesses": {
    "opencode": {
      "command": "opencode run --agent {agent} --model {model} --format json \"$(cat {prompt_file})\"",
      "roles": ["orchestrator", "auditor_a", "auditor_b", "worker"]
    }
  },
  "constraints": {
    "allowed_providers": ["opencode-go", "opencode", "openrouter", "ollama"],
    "max_cost_per_mtok": null,
    "licence_policy": "any",
    "local_only": false
  },
  "pins": {},
  "fallback": {
    "orchestrator": {"harness": "opencode", "model": "opencode-go/glm-5.3"},
    "auditor_a": {"harness": "opencode", "model": "opencode-go/kimi-k3"},
    "auditor_b": {"harness": "opencode", "model": "opencode-go/deepseek-v4.1-flash"},
    "worker": {"harness": "opencode", "model": "opencode-go/mimo-v2.6-flash"}
  },
  "verified_on": "2026-10-11",
  "sources": [
    "https://opencode.ai/docs/agents/",
    "https://opencode.ai/docs/go/",
    "https://models.dev/api.json",
    "https://deepswe.datacurve.ai/"
  ]
}
```

Scripted auditors must use agents with `mode: "all"`, not `subagent`, or
`opencode run --agent` silently falls back to the default agent and loses its
read-only permissions. Auditor A and Auditor B come from different families
(Moonshot and DeepSeek), so this profile runs in `full` independence.
