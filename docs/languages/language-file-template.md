# Language File Template

Use this template for every future `docs/languages/*.md` file. Keep filenames
kebab-case and do not include dates.

## Required Sections

1. `# Language Name`
2. Runtime, standard, package, or platform section
3. `## Tooling`
4. `## Generation Rules`
5. `## Source Documentation And Comments`
6. `## Test-First Red Green Refactor`
7. `## Refactoring Playbook`
8. `## Best Practice Examples`
9. `## Project Discovery And Structure`
10. `## Design Patterns And Architecture`
11. `## Algorithmic Complexity And Dynamic Programming`
12. `## Senior Architecture Decisions`
13. `## Concurrency Parallelism And Hardware Acceleration`
14. `## Senior Decision Checklist`
15. `## Final Senior Guardrails`
16. `## LLM Coding Guardrails`

## Writing Rules

- Keep sections concise and action-oriented.
- Prefer language-native tooling and patterns.
- State when the language should not be used for a task.
- Include performance, security, testing, and rollback concerns.
- Require red-green-refactor for bug fixes and behavior changes.
- Include the 10 standard refactoring playbook items.
- Include concise language-specific bad/good examples.
- Avoid generic advice that could apply to any language without adjustment.
