# OpenCode Adapter

Copy or install the whole skill folder, not this file alone, because the
guidance links resolve from the skill root.

- Entry point: `SKILL.md`
- Guidance file: `AGENTS.md` (in this folder)
- Model profile for open-weight models: `profiles/opencode-open-weights.md`

OpenCode reads global skills from `~/.config/opencode/skills` and
`~/.agents/skills`. Validate from the skill root:
`python scripts/validate-workspace.py`.
