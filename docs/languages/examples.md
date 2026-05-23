# Language Guidance Examples

Use these examples to apply the individualized language files without guessing.

## Operational Scripts

Bad: write a complex Bash script with nested parsing, retries, and state files.

Good: write a Python CLI with `argparse`, `--dry-run`, explicit timeouts,
structured errors, and tests.

## Dependency Addition

Bad: add a package because it is familiar.

Good: check the standard library and existing dependencies first, justify the
package, pin the version, verify license/security status, and run tests.

## Error Handling

Bad: catch broad exceptions and continue silently.

Good: classify retryable, user-correctable, and terminal errors; preserve the
cause; add timeout, cleanup, and observable failure output.

## Queue Consumer

Bad: process messages with unbounded retries and no duplicate handling.

Good: make handlers idempotent, bound retries, add dead-letter handling, record
correlation IDs, and expose queue depth, latency, and failure metrics.

## Dynamic Programming

Bad: add memoization because an algorithm is slow.

Good: prove overlapping subproblems and optimal substructure, define state,
transition, base cases, iteration order, complexity, and memory bounds.

## Concurrency

Bad: add threads to make code faster without measuring.

Good: profile first, separate I/O wait from CPU work, bound concurrency, support
cancellation, avoid shared mutable state, and benchmark representative inputs.

## GPU Usage

Bad: move ordinary business logic to GPU.

Good: use GPU only for large numeric, image, ML, graphics, or data-parallel
workloads where transfer and setup costs are justified by measurement.

## Frontend Accessibility

Bad: create clickable `div` elements and hide instructions in visual styling.

Good: use semantic controls, keyboard access, focus states, labels, locale-aware
formatting, and accessible loading/error states.

## SQL And Persistence

Bad: loop through rows in application code and run one query per item.

Good: use set-based SQL, indexes, constraints, transactions, query plans, and an
outbox pattern for reliable post-commit events.

## Refactoring

Bad: refactor unrelated modules while fixing a narrow bug.

Good: preserve behavior, add characterization tests for risky code, keep changes
reviewable, and avoid unrelated churn.
