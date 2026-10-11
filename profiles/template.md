# Profile Template

Copy this file to `.polyglot/profile.md` in your project, or into `profiles/`,
and fill it in. Every key is required.

```json
{
  "name": "my-profile",
  "harnesses": {
    "my-harness": {
      "command": "my-tool run --model {model} --prompt-file {prompt_file}",
      "roles": ["orchestrator", "auditor_a", "auditor_b", "worker"]
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
    "orchestrator": {"harness": "my-harness", "model": "orchestrator-model-id"},
    "auditor_a": {"harness": "my-harness", "model": "first-auditor-model-id"},
    "auditor_b": {"harness": "my-harness", "model": "second-auditor-model-id"},
    "worker": {"harness": "my-harness", "model": "worker-model-id"}
  },
  "verified_on": "2026-10-11",
  "sources": ["https://example.org/where-you-confirmed-these-models"]
}
```

Rules: use two different model families for `auditor_a` and `auditor_b` when you
can. If you cannot, use two different models from one family and the gate runs
in degraded independence. Never use the same model for both auditors.
