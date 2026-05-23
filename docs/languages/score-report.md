# Language Guidance Score Report

## Current Status

Score: `100/100`

## Validation Command

```sh
python scripts/validate-workspace.py
python scripts/validate-language-guidance.py
```

## Coverage

- Individualized language files: `22/22`
- Human-readable language README files: `22/22`
- Operational language governance files: `11/11`
- Required language sections: present
- Test-first red-green-refactor sections: present
- Refactoring playbook sections: present
- Senior decision labels: present
- Final senior guardrail labels: present
- LLM coding guardrails: present
- Filename policy: kebab-case, no dates
- Workspace validation: present
- One-line installer: present

## Notes

This report is valid when the workspace validator returns `workspace validation:
PASS` and the language validator returns `language guidance validation: PASS`.
Update this file whenever required sections, labels, or language files change.
