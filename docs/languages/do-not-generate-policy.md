# Do Not Generate Policy

These are hard stops for code generation.

## Hard Stops

- Do not invent APIs, flags, package names, configuration keys, or cloud
  services.
- Do not add infrastructure without evidence that simpler supported paths fail.
- Do not create unbounded queues, retries, thread pools, caches, or memory
  growth.
- Do not store secrets, tokens, credentials, or private keys in source.
- Do not write destructive scripts without dry-run, confirmation bypass, and
  rollback notes.
- Do not add dependencies without justification, exact versions, license review,
  and vulnerability consideration.
- Do not ignore tests, type checks, linting, or security checks when they exist.
- Do not hide errors with broad catches, silent retries, or swallowed failures.
- Do not use preview, nightly, beta, or deprecated runtimes for production
  unless explicitly approved.

## Required Response To A Hard Stop

Pause implementation, document the blocker in the workflow audit, and choose the
shortest reliable supported alternative. Ask the user only when the safe path
cannot be inferred.
