# Language Guidance Scoring Rubric

Use this rubric to score any individualized language file. Score each criterion
from `0` to `10`; final target is `100/100`.

## Criteria

1. Language selection clarity
2. Project discovery and structure clarity
3. Runtime, package, and toolchain clarity
4. Style, naming, documentation, comments, and best-practice example clarity
5. Testing, red-green-refactor, refactoring playbook, and verification clarity
6. Security, privacy, and compliance clarity
7. Algorithmic complexity and performance clarity
8. Architecture, queues, concurrency, CPU, and GPU clarity
9. Release, migration, rollback, and operability clarity
10. Dependency, configuration, resource, and packaging clarity

## Scoring Rules

- `100/100`: ready for code generation with minimal guesswork.
- `90-99`: usable but one or more senior decisions are implicit.
- `70-89`: partial guidance; code generation will require assumptions.
- Below `70`: not acceptable for autonomous code generation.
- Criterion 4 includes the plain-language comment rule in
  `docs/language-guidelines.md`. Comments that restate the code, narrate edits,
  hype the result, or pad with filler lower that score.

Record concrete gaps and fixes in the workflow audit before editing code.
