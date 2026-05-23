# Python Deep Guide

This document constrains all Python code generation for any project that references it. Read it before writing or editing Python code. The goal is production-quality Python that is correct, typed, tested, secure, maintainable, efficient, and portable across Windows, macOS, Ubuntu, and Fedora.

For cross-language decisions, read `../../language-guidelines.md` first. Python remains
the default language for operational scripts, automation, audits, migrations,
file processing, and glue code unless an existing repository toolchain is a
clearer supported path.

## Runtime

- **Python version**: Target Python `3.14.5` or newer. Use the newest stable patch version available for the target platform.
- **Minimum target**: Always use Python 3.14+ syntax and stdlib. Never backport to older versions unless the user explicitly changes the target.
- **Interpreter discovery**: Verify the interpreter before use:
  ```console
  python --version
  python -c "import sys; print(sys.executable)"
  ```
- **Preferred command**: Inside an activated `.venv`, use `python`. Outside a verified `.venv`, use the platform interpreter command from the table below.
- **pip invocation**: Always use `python -m pip` over bare `pip` to guarantee the correct interpreter is targeted.
- **pip baseline**: Use `pip==26.1.1` in project virtual environments.
- **uv baseline**: Use `uv==0.11.16` only for interpreter management or when the
  project already standardizes on `uv`.

| Platform | Preferred interpreter command | Notes |
|---|---|---|
| Windows | `py -3.14` or full `python.exe` path | Avoid Microsoft Store execution aliases. If `python` opens the Store stub, use `py -3.14` or the installed interpreter path. |
| macOS | `python3.14` | Install from `python.org`, Homebrew, `uv`, or `pyenv`; do not rely on the system Python. |
| Ubuntu | `python3.14` | Install from the distro package source, deadsnakes PPA, `uv`, or `pyenv` when the distro default is older. |
| Fedora | `python3.14` | Use Fedora packages when available, or `uv`/`pyenv` for newer patch versions. |

For project commands, prefer a tiny platform-specific bootstrap note in the project README if the local interpreter command differs from `python`.

## Environment Management

- **Virtual environments**: Use `venv` (stdlib). Always create one per project.
- **Creation command**: `<interpreter> -m venv .venv`, then use the activated environment's `python`.
- **Activation (PowerShell)**: `.\.venv\Scripts\Activate.ps1`
- **Activation (cmd)**: `.\.venv\Scripts\activate.bat`
- **Activation (bash/zsh/fish)**:
  ```sh
  source .venv/bin/activate
  ```
- **Never** install packages globally. If global install seems necessary, ask the user.
- **Never** assume a virtual environment is already active. Always document the activation step and verify with `python -c "import sys; print(sys.prefix)"`.
- **Cross-platform paths**: Never hardcode OS-specific path separators or absolute user paths. Use `pathlib.Path`, environment variables, and configuration files.

## Cross-Platform Portability

All generated code must run predictably on Windows, macOS, Ubuntu, and Fedora unless a project explicitly narrows the target.

- **Filesystem case**: Treat paths as case-sensitive. Never rely on `Config.toml` and `config.toml` being the same file.
- **Line endings**: Read text with universal newline support and write normal text files with `\n` unless a target format requires another newline.
- **Encoding**: Use UTF-8 for source, config, data files, subprocess text I/O, and logs. Never rely on locale defaults.
- **Locale**: Do not parse dates, numbers, or booleans using ambient locale. Use explicit formats and validators.
- **Time zones**: Store and compare datetimes in timezone-aware UTC. Convert to local time only at presentation boundaries.
- **Temporary paths**: Use `tempfile.TemporaryDirectory()` or `tempfile.NamedTemporaryFile()`; never hardcode `/tmp`, `%TEMP%`, or user profile paths.
- **Executable lookup**: Use `shutil.which()` for external commands and fail with a clear message when missing.
- **OS features**: Gate platform-specific behavior behind `sys.platform` or `platform.system()` checks and provide a portable fallback or explicit error.
- **File locks and deletes**: Windows may keep files locked longer than POSIX systems. Close handles promptly and avoid assuming immediate delete/rename success.
- **Permissions**: POSIX permission bits and Windows ACLs differ. Do not implement security controls that depend on one model without a platform-specific branch.
- **Signals and process groups**: Do not assume POSIX signal behavior on Windows. Prefer `subprocess.run(..., timeout=...)` and explicit process cleanup.
- **Path length**: Avoid deeply nested generated paths and keep test fixture paths short enough for Windows tooling.

## Application Surfaces

Python guidance changes by runtime surface. Identify the target surface before choosing frameworks, dependencies, architecture, packaging, and validation commands. Do not assume Python is the right runtime for every surface.

### Web APIs and Web Apps

- **Use case fit**: Python is appropriate for APIs, backend services, server-rendered apps, admin tools, workers, automation, and data services.
- **Framework approval**: Do not introduce FastAPI, Flask, Django, Starlette, Litestar, or similar frameworks without user approval.
- **Request boundaries**: Validate request bodies, path/query parameters, headers, cookies, and uploaded files at the boundary.
- **Response contracts**: Keep response schemas stable. Version public APIs when breaking changes are unavoidable.
- **Timeouts and limits**: Enforce request size limits, upload limits, outbound HTTP timeouts, database timeouts, and worker timeouts.
- **Authentication and authorization**: Keep auth checks explicit at entry points and resource boundaries. Never trust client-provided user ids, roles, or permissions.
- **CORS and cookies**: Configure CORS, cookie flags, CSRF protection, and session lifetime deliberately. Do not use permissive defaults in production.
- **Rate limiting**: Add rate limiting or abuse controls for public endpoints, login flows, expensive operations, and mutation endpoints.
- **Errors**: Return structured, sanitized errors. Do not expose stack traces, secrets, SQL, filesystem paths, or internal service names.
- **Pagination**: Paginate list endpoints. Never return unbounded result sets.
- **OpenAPI/schema docs**: If the framework supports schema generation, keep public schema docs aligned with tests.

### Mobile-Facing Systems

- **Runtime assumption**: Do not assume Python runs inside the mobile app. For iPhone and Android, Python usually belongs in backend APIs, build tooling, test automation, data pipelines, or content generation.
- **Native default**: For native iOS apps, prefer Swift/SwiftUI. For native Android apps, prefer Kotlin/Jetpack. Use Python mobile frameworks such as Kivy, BeeWare, or Toga only with explicit user approval.
- **Payload efficiency**: Optimize mobile-facing APIs for small payloads, pagination, compression, cache headers, and partial sync.
- **Latency and reliability**: Design for high latency, dropped connections, retries, duplicate requests, and offline/online transitions.
- **Backward compatibility**: Mobile clients update slowly. Keep API changes backward-compatible or versioned.
- **Battery and data use**: Avoid chatty polling and large background transfers. Prefer batching, delta sync, and server-side filtering.
- **Push and background work**: Treat push notifications, background refresh, and scheduled sync as platform-specific client concerns unless the Python service is only generating or dispatching server-side events.
- **Security**: Never put secrets in mobile clients. Python backends must assume clients can be inspected and tampered with.

### Desktop Apps

- **Framework approval**: Ask before adding GUI frameworks such as PySide, PyQt, Tkinter, wxPython, Kivy, Toga, or Electron-adjacent tooling.
- **UI separation**: Keep UI code thin. Put business logic, validation, persistence, and platform integrations behind testable modules.
- **Main thread**: Do not block UI threads with network calls, file scans, sleeps, or CPU-heavy work.
- **Background work**: Use background workers carefully, with cancellation, progress reporting, and error surfacing.
- **OS conventions**: Store config, cache, logs, and app data in OS-appropriate locations. Do not hardcode home-directory paths.
- **File dialogs and permissions**: Use platform dialogs and validate returned paths. Handle user-denied permissions and missing files.
- **Packaging**: Desktop packaging, signing, notarization, installers, auto-update, and sandboxing are surface-specific and require explicit project decisions.
- **Accessibility**: Preserve keyboard navigation, labels, focus handling, and readable error messages when building UI.

### CLI and TUI Tools

- **Default fit**: Python is a strong fit for CLIs, automation, developer tools, maintenance scripts, and batch processors.
- **Output channels**: Write machine-readable results to stdout and diagnostics/errors to stderr.
- **Exit codes**: Return `0` on success and non-zero on failure. Document special exit codes only when useful.
- **Help and version**: Provide `--help` and `--version` for reusable tools.
- **Dry run**: Include `--dry-run` or preview behavior for destructive, bulk, remote, or irreversible operations.
- **Non-interactive mode**: Do not require prompts for automation. Provide flags/env/config for unattended runs.
- **Terminal features**: Ask before adding Rich, Textual, Click, Typer, or prompt libraries. Plain `argparse` is the default.
- **Shell compatibility**: Do not assume Bash, PowerShell, zsh, fish, GNU tools, or ANSI color support unless detected or documented.

### Background Services and Workers

- **Lifecycle**: Implement startup, readiness, graceful shutdown, and cleanup paths.
- **Idempotency**: Jobs that mutate external systems must be idempotent or protected by idempotency keys.
- **Retries**: Use bounded retries with backoff and jitter. Never retry indefinitely.
- **Queues**: Bound queue sizes and worker concurrency. Apply backpressure instead of unbounded memory growth.
- **Locks**: Use explicit locks for singleton jobs and shared resources. Include stale-lock recovery when appropriate.
- **Observability**: Log job id, attempt, elapsed time, outcome, retry delay, and sanitized failure reason.
- **Poison messages**: Detect repeatedly failing work and move it to a dead-letter path or documented failure store when the queue system supports it.

### Windows-Specific Python

- **Paths**: Use `pathlib.Path`; avoid hardcoded drive letters, profile paths, and backslashes.
- **Shells**: Distinguish PowerShell, cmd, Git Bash, WSL, and native Windows behavior. Do not mix command syntax.
- **File locking**: Expect open files to block rename/delete. Close handles promptly and retry only with bounded attempts.
- **Registry/services/tasks**: Registry edits, Windows services, scheduled tasks, Event Log, COM, and WMI require explicit user approval and audit logging.
- **Permissions**: Detect admin requirements before attempting privileged actions. Fail clearly when elevation is required.
- **Newlines/encoding**: Use UTF-8 and explicit newline behavior for files that must be cross-platform.

### macOS-Specific Python

- **Python source**: Do not rely on the system Python. Use a project-managed interpreter from `python.org`, Homebrew, `pyenv`, or another approved tool.
- **CLI tools**: macOS often ships BSD variants instead of GNU tools. Avoid GNU-specific flags unless checked.
- **Filesystem**: Treat the filesystem as case-sensitive even when the default local volume is case-insensitive.
- **App distribution**: App bundles, signing, notarization, sandboxing, and Keychain access require explicit project decisions.
- **Permissions**: Handle TCC privacy prompts for files, automation, contacts, calendar, camera, microphone, screen recording, and accessibility when relevant.
- **Launch agents**: LaunchAgent/LaunchDaemon installation requires explicit approval and rollback steps.

### Linux and Unix Variants

- **Distribution assumptions**: Do not assume Ubuntu behavior on Fedora or Fedora behavior on Ubuntu.
- **Package managers**: Do not assume `apt`, `dnf`, `yum`, `pacman`, Homebrew, or root access unless verified.
- **Filesystem**: Assume case-sensitive paths, symlinks, POSIX permissions, and executable bits.
- **XDG paths**: Use XDG conventions for user config, cache, state, and data when writing user-level tools.
- **Init systems**: Do not assume `systemd` exists. Detect or document service manager requirements.
- **Shells**: Do not assume Bash; scripts may run under `sh`, zsh, fish, or another shell. Prefer Python implementations over shell glue for portability.
- **Signals**: Handle `SIGTERM` for graceful shutdown in services and workers. Do not rely on signals that are unavailable on Windows if code is portable.
- **Containers**: In containers, avoid writing outside configured data paths, assume ephemeral filesystems, and make health/readiness behavior explicit.

## Dependency Management

- **Lockfile format**: `requirements.txt` (generated via `pip freeze`)
- **Install command**: `python -m pip install -r requirements.txt`
- **Pin exact versions**: Use `==` pins only (no `>=`, `~=`, or bare package names).
- **Example**: `requests==2.32.3` not `requests` or `requests>=2.32`.
- **Before adding a dependency**: Check that it is not already covered by the stdlib (e.g., use `pathlib`, not `pathlib2`; use `tomllib`, not `tomli` for 3.14+). Prefer fewer dependencies.
- **Dependency approval rule**: The tools and libraries explicitly prescribed in this document may be used when their section applies. Any other new third-party dependency requires user approval and a short rationale.
- **No dependency injection frameworks.** If one seems necessary, ask the user.
- **Dev dependencies**: Install these baseline tools in every project venv. Keep exact pins in `requirements-dev.txt` or a dedicated dev lockfile, and update them intentionally after running the full validation suite:
  ```
  ruff==0.15.14
  mypy==2.1.0
  pytest==9.0.3
  pytest-cov==7.1.0
  build==1.5.0
  pip-audit==2.10.0
  ```
- **Editable install**: Use `python -m pip install -e .` to install the project in development mode.

### Supply Chain Controls

- **Separate runtime and dev locks**: Keep runtime dependencies separate from development tools. Use `requirements.txt` for runtime and `requirements-dev.txt` for dev tools unless the project uses another approved lock format.
- **Record transitive dependencies**: Lock the complete resolved environment, not just top-level dependencies.
- **Hash checking for high-risk projects**: For production services, automation touching sensitive data, or deployment artifacts, prefer hash-checked installs with `--require-hashes`.
- **No dependency confusion**: Verify package names before adding dependencies. Avoid internal package names that could collide with public package indexes.
- **No unpinned indexes**: If using a private package index, document the index URL outside source when it is secret and pin the package source in setup docs.
- **Upgrade discipline**: Update dependencies in focused changes. Run tests, type checks, linting, `pip-audit`, and a smoke test after every upgrade.
- **Vulnerability handling**: If `pip-audit` reports a vulnerability, upgrade to a fixed version or document a temporary exception with package, CVE/advisory, affected path, and mitigation.
- **License awareness**: Before adding a dependency, verify its license is acceptable for the project. Ask the user if the license is unclear or restrictive.
- **Vendoring**: Do not vendor third-party code unless explicitly approved. If vendored code exists, keep its license and source provenance.
- **Optional extras**: Keep optional dependencies behind extras or documented install groups. Do not force heavy optional stacks into the base install.

## Public API Design

Design public Python APIs for clarity, stability, and low overhead.

- **Small surface area**: Export only the names users need. Keep implementation details private with a leading underscore.
- **Explicit exports**: Use `__all__` when a module has a defined public API. Keep `__init__.py` light.
- **Stable contracts**: Treat public function signatures, return types, exceptions, CLI arguments, config keys, and output formats as compatibility contracts.
- **Keyword-only options**: Use keyword-only parameters for optional behavior flags to prevent call-site ambiguity.
- **No boolean traps**: Avoid multiple boolean parameters. Use `Literal`, enums, or small config objects when choices are not obvious.
- **Config objects**: Use frozen dataclasses or pydantic models for grouped settings instead of long parameter lists.
- **Versioning**: If a package exposes a public API, define `__version__` or project metadata and document compatibility expectations.
- **Deprecation path**: Do not remove or rename public API without a deprecation warning and migration note unless the user requests a breaking change.
- **Error model**: Public functions should raise documented project-specific exceptions at boundaries, while preserving original causes with exception chaining.
- **No import side effects**: Importing a module must not perform network calls, parse large files, mutate global state, configure logging, or start background work.

## Code Style

- **Formatter**: `ruff format` (Black-compatible, line length 88). No need to install `black` separately; `ruff format` produces identical output.
- **Linter**: `ruff` (replace flake8, isort, pydocstyle, and pyupgrade)
- **Type checker**: `mypy --strict`
- **Import ordering**: Handled by `ruff` (isort-compatible)
- **String quotes**: Double quotes (consistent with Black-compatible output)
- **Max line length**: 88 characters (follow Black standard)
- **Trailing commas**: Yes (follow Black standard)
- **Indentation**: 4 spaces, no tabs
- **Ruff rule configuration**: Enable these rule sets in `pyproject.toml` under `[tool.ruff.lint]`:
  `select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM", "T20", "S110", "EM", "C90", "S", "PGH", "RUF", "RUF100"]`
  This enforces: style (E/F/W), import sorting (I), naming (N), pyupgrade (UP), bugbears (B), shadowed builtins (A), comprehensions (C4), simplifications (SIM), no print (T20), no pass in except (S110), exception message variables (EM), McCabe complexity C90 max 10, bandit security (S), type-ignore requires error code (PGH), unused noqa (RUF100), ruff-specific (RUF).
- **Per-file ignores**: Allow `T201` (print) in `tests/` via `[tool.ruff.lint.per-file-ignores]` in `pyproject.toml`.
- **Blank lines**: 2 blank lines between top-level definitions, 1 blank line within classes (enforced by E3 rules).

### Naming

| Element | Convention | Example |
|---|---|---|
| Packages | `snake_case`, short, import-safe | `billing_core` |
| Modules | `snake_case` | `data_loader.py` |
| Private modules | leading underscore only for internal modules | `_compat.py` |
| Functions | `snake_case` verb phrase for actions | `def load_config():` |
| Variables | `snake_case` noun phrase | `user_count = 0` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 3` |
| Classes | `PascalCase` | `class DataLoader:` |
| Exceptions | `PascalCase` ending in `Error` | `class ConfigError(AppError):` |
| Methods | `snake_case` | `def get_status(self):` |
| Private attrs | `_leading_underscore` | `self._cache = {}` |
| Type aliases | `PascalCase` | `UserId = int` |
| Protocols | capability name, often `Supports...` | `class SupportsClose(Protocol):` |
| Enums | `PascalCase` | `class Status(Enum):` |
| Enum members | `UPPER_SNAKE_CASE` | `ACTIVE = "active"` |
| Booleans | `is_`, `has_`, `can_`, `should_`, `needs_` | `is_active`, `has_token` |
| Collections | plural nouns | `users`, `pending_jobs` |
| Mappings | key/value role in name | `user_by_id`, `email_to_user` |
| Callbacks | verb phrase or `on_<event>` | `on_complete`, `transform_item` |
| Context managers | resource/lifecycle name | `managed_connection` |
| Pytest files | `test_<module_name>.py` | `test_config.py` |
| Pytest functions | `test_<behavior>_<condition>` | `test_load_config_raises_on_missing_file` |
| Pytest fixtures | noun phrase, no `fixture_` prefix | `tmp_config_path` |
| CLI commands | lowercase kebab-case | `sync-users` |
| CLI options | lowercase kebab-case | `--dry-run` |
| Environment variables | uppercase with project prefix | `APP_DATABASE_URL` |
| Config keys | lowercase snake_case | `retry_count` |

- **Avoid vague names**: Do not use `data`, `obj`, `item`, `manager`, `handler`, `processor`, `temp`, or `result` unless the scope is tiny and the meaning is obvious.
- **Avoid overloaded suffixes**: Use `service`, `client`, `repository`, `adapter`, or `controller` only when the object has that specific architectural role.
- **Units and domains**: Include units or domain meaning when ambiguity is possible, e.g., `timeout_seconds`, `size_bytes`, `created_at_utc`.
- **Acronyms**: Treat acronyms as words in identifiers: `http_client`, `user_id`, `JsonParser` only when matching a public class name style. Avoid `HTTPClient` unless an external API requires it.
- **Public API names**: Prefer stable, explicit names over abbreviated names. Public names are harder to change than private locals.
- **Throwaway names**: Use `_` only for intentionally unused values. Use `_name` only for private attributes or variables whose value is intentionally internal.

### Imports

- Use absolute imports only. No relative imports.
- Group in this order (enforced by `ruff`):
  1. Standard library
  2. Third-party
  3. Local/application
- No wildcard imports (`from module import *`).
- No implicit re-exports. Use `__all__` explicitly if re-exporting.
- Import `typing` symbols from `typing` (not `typing_extensions` for 3.14+).

## Type Hints

- **Enforced**: All function signatures must have full type annotations.
- **Return types**: Always explicit, including `-> None`.
- **Use `mypy --strict`** as the validation standard.
- **Prefer modern syntax** (3.14+):
  - Use `X | Y` instead of `Union[X, Y]`.
  - Use `list[X]` instead of `List[X]` (no `from __future__ import annotations` needed).
  - Use `dict[str, object]` instead of `Dict[str, Any]`.
  - Use PEP 695 `type` alias syntax: `type Point = tuple[float, float]` instead of `TypeAlias` annotation.
- **Never use `Any`**. Use `object` when the type is truly opaque (e.g., container of arbitrary items). Use `Protocol` when specific methods are expected. If neither `object` nor `Protocol` fits, ask the user before using `Any`.
- **Use `Protocol`** for structural subtyping instead of `ABC` when only method signatures matter.
  ```python
  from typing import Protocol

  class Closeable(Protocol):
      def close(self) -> None: ...
  ```
- **Additional type constructs**:
  - `TypedDict` for structured dict types with known keys.
  - `Literal["a", "b"]` for constrained string/int values.
  - `Final` for constants that should not be reassigned. `ClassVar` for class-level attributes excluded from instance data.
  - `Callable[[int, str], bool]` for function type signatures.
  - `NoReturn` for functions that never return (e.g., `sys.exit` wrappers).
  - `@overload` for multiple signatures. `@override` (PEP 698, 3.12+) for explicit subclass method overrides.
  - `cast()` only when the type is known to be correct but cannot be inferred. Add a comment explaining why.
  - `assert_never()` for exhaustive type checking in `match`/`else` branches.
  ```python
  from typing import (
      Callable,
      ClassVar,
      Final,
      Literal,
      NoReturn,
      TypedDict,
      assert_never,
      override,
  )

  class UserInfo(TypedDict):
      name: str
      age: int

  Status = Literal["active", "inactive"]
  MAX_NAME_LEN: Final = 255

  class Base:
      def process(self) -> None: ...

  class Impl(Base):
      @override
      def process(self) -> None: ...
  ```
- **Generic classes**: Use `class Container[T]:` syntax (3.14+).
- **Type aliases**: Use PEP 695 syntax `type AliasName = ...` instead of `TypeAlias` annotation.

## Error Handling

- **Never use bare `except:`**. Always specify the exception type.
- **Never catch `Exception` broadly** except in these two cases: (1) re-raising (`except Exception: raise`), or (2) logging inside the outermost function that handles an incoming request, CLI command, message, or task.
- **Custom exceptions**: Subclass from a project-specific base exception, not directly from `Exception`.
- **Pattern**:
  ```python
  class AppError(Exception):
      pass

  class ConfigError(AppError):
      pass
  ```
- **Always use `with`** for resource management (files, connections, locks).
- **Prefer `try/except/else/finally`** with each block having a single responsibility.
  ```python
  try:
      data = read_file(path)
  except FileNotFoundError:
      logger.exception("Config file not found")
      raise ConfigError(f"Missing config: {path}") from None
  else:
      config = parse(data)
  finally:
      logger.info("Config load attempt finished")
  ```
- **Error propagation**: Re-raise at boundaries with added context (`raise NewError(...) from orig`). Never swallow and return `None` silently. Use explicit sentinel values or `Result` types only when the user requests them.
- **Logging errors**: Use `logging.exception()` inside `except` blocks to capture tracebacks automatically.
- **No silent failures**: Never use `pass` as the only body of an `except` block.

### Error Messages

User-facing error messages are part of the product surface. They must be specific, actionable, and safe.

- **State the problem clearly**: Say what failed and which user-controlled input or operation caused it.
- **Suggest the fix**: Include the next action when it is known, e.g., "Set APP_API_TOKEN" or "Use --dry-run first".
- **Do not expose internals**: Never show stack traces, SQL, secrets, tokens, raw exception reprs, internal hostnames, filesystem internals, or dependency implementation details to users.
- **Keep CLI errors concise**: Prefer messages under about 120 characters for CLI stderr. Put longer diagnostics behind `--verbose` or debug logs.
- **Use stable wording**: Keep public API and CLI error wording stable enough for tests and automation when users may depend on it.
- **Differentiate cause and hint**: For CLI tools, use a short primary error plus optional hint.
  ```text
  error: config file not found: settings.toml
  hint: pass --config or create settings.toml in the project root
  ```
- **HTTP errors**: Return structured error bodies with a stable code, safe message, and optional request/correlation id.
- **Validation errors**: Point to the failing field or argument. Do not dump entire payloads.

## Logging

- **Library**: Standard library `logging` module.
- **No print statements** for diagnostic output in production code. Use `logging`.
- **Logger per module**: `logger = logging.getLogger(__name__)`
- **Levels**:
  - `DEBUG`: Detailed diagnostic information.
  - `INFO`: Confirmation of normal operation.
  - `WARNING`: Something unexpected but still working.
  - `ERROR`: A function failed but the application can continue.
  - `CRITICAL`: The application cannot continue.
- **Format**: Include timestamp, level, module, and message. Use: `"%(asctime)s [%(levelname)s] %(name)s: %(message)s"`.
- **Configuration**: Configure logging only in `if __name__ == "__main__"` blocks or `__main__.py`. Never call `basicConfig()` in library modules. Example:
  ```python
  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
  )
  ```
- **Structured logging**: Use plain text logging by default. If JSON/structured output is needed, use a structured handler but keep the stdlib logging interface.
- **Structured JSON schema**: When JSON logs are required, use stable field names:
  ```json
  {
    "ts": "2026-05-12T15:04:05.123Z",
    "level": "INFO",
    "module": "project_name.worker",
    "msg": "job completed",
    "event_type": "job.completed",
    "correlation_id": "run_123",
    "duration_ms": 42,
    "success": true
  }
  ```
- **Deprecation warnings**: Use `warnings.warn(msg, DeprecationWarning, stacklevel=2)` when removing or renaming a public function, class, parameter, or constant that external consumers may reference.
- **Exception groups**: Use `except*` syntax (3.11+) for handling `ExceptionGroup` when multiple exceptions must be handled independently.
- **Never log sensitive data**: Do not log passwords, tokens, API keys, PII, or auth headers. Mask or truncate before logging.
- **Log rotation**: For long-running processes, configure `RotatingFileHandler` or `TimedRotatingFileHandler`. Never let log files grow unbounded.

## Observability

Observability must make failures diagnosable without leaking secrets or overwhelming the runtime.

- **Boundary logs**: Log at application boundaries: CLI start/end, job start/end, external API calls, retries, validation failures, and unrecoverable errors.
- **Context fields**: Include stable context such as operation name, resource id, attempt number, elapsed time, and result. Do not include secrets or raw PII.
- **Correlation ids**: For services, jobs, and multi-step workflows, propagate a request id, run id, or correlation id.
- **Elapsed time**: Measure important operations with `time.perf_counter()`, not wall-clock time.
- **Retry visibility**: Log retries with attempt count, wait duration, and sanitized failure reason.
- **Metrics**: If a metrics stack exists, record counts, durations, queue depth, and failure rates. Do not introduce a metrics dependency without approval.
- **High-cardinality guard**: Do not use raw user input, URLs, file paths, stack traces, or unbounded ids as metric labels.
- **Health checks**: Long-running services should expose or implement lightweight checks for dependencies and readiness when the framework supports it.
- **Run summaries**: CLI and batch tools should return meaningful exit codes and produce concise summaries for processed, skipped, failed, and retried items.
- **Debug logging**: Keep debug logs useful but cheap. Do not build expensive debug values unless debug logging is enabled.

## Data Validation

- **Library**: `pydantic` (v2+) for structured data validation and settings.
- **Use for**: API payloads, configuration files, CLI arguments, database models.
- **Pydantic model example**:
  ```python
  from pydantic import BaseModel

  class User(BaseModel):
      name: str
      email: str
      age: int | None = None
  ```
- **Settings management**: Use `pydantic-settings` for env-var and config-file loading.
- **Never manually parse** JSON/YAML/TOML into typed structures without validation.

### Data Modeling

- **Choose the lightest model**: Use dataclasses for trusted internal records and pydantic models for untrusted external input, configuration, and boundary validation.
- **Validate at boundaries**: Validate once when data enters the system. Keep internal data typed so repeated validation is not needed in hot paths.
- **Immutable by default**: Prefer frozen dataclasses or immutable tuples for values that should not change after creation.
- **Explicit optionality**: Use `T | None` only when absence is meaningful. Do not use `None` as a vague failure value.
- **No primitive obsession at boundaries**: Replace loosely related `str`, `int`, and `dict` bundles with named models when the values travel together.
- **Schema evolution**: For persisted or external data, plan for added fields, missing fields, and version migration.
- **Serialization boundary**: Keep serialization and deserialization near I/O edges. Do not pass raw JSON/dicts deep into business logic.
- **Decimal for money**: Use `decimal.Decimal` for money and exact decimal quantities. Never use `float` for currency.
- **Timezone-aware datetimes**: Use aware UTC datetimes for storage and comparisons.
- **Stable identifiers**: Use explicit id types or aliases when multiple id domains exist.

## Project Structure

```
project-name/
├── pyproject.toml
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── py.typed
│       ├── __main__.py
│       ├── config.py
│       ├── models.py
│       └── ...
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_config.py
    └── ...
```

- **Source layout**: Use `src/` layout to prevent accidental imports from the project root.
- **Package naming**: Single `snake_case` word or short `snake_case` phrase. No underscores at start/end.
- **`__main__.py`**: Required for `python -m project_name` execution.
- **`conftest.py`**: Shared pytest fixtures go here.
- **`__init__.py`**: Keep minimal. Use only for `__all__` exports and version string. Leave empty if no explicit public API exports are needed. Never put business logic in `__init__.py`.
- **`py.typed`**: Include an empty `py.typed` marker file in each typed package root to signal PEP 561 compliance.
- **LICENSE**: Every package must include a `LICENSE` file at the repository root.

### Module Decomposition

- **Split large modules**: Split a module when it exceeds about 400 lines, has more than two distinct responsibilities, or requires unrelated test fixtures to exercise its behavior.
- **Group by domain concept**: Prefer modules organized around domain behavior (`invoices`, `users`, `sync_jobs`) instead of technical layers (`helpers`, `misc`, `common`) unless the layer is a real boundary.
- **Keep cohesion high**: A module should have one clear reason to change. If two groups of functions change for different reasons, split them.
- **Avoid junk drawers**: Do not create broad `utils.py`, `helpers.py`, or `common.py` modules for unrelated functions. Use specific names such as `path_validation.py` or `retry_policy.py`.
- **Separate boundaries**: Keep external adapters, domain logic, configuration, persistence, CLI/API entry points, and serialization in separate modules once each has meaningful logic.
- **Prevent cycles**: If a split creates circular imports, move shared types or protocols into a small boundary module rather than importing implementation modules both ways.

### Minimal Project Templates

Use these templates for new projects unless the existing repository already has stronger local conventions.

**`requirements-dev.txt`**

```txt
ruff==0.15.14
mypy==2.1.0
pytest==9.0.3
pytest-cov==7.1.0
build==1.5.0
pip-audit==2.10.0
```

**`src/project_name/__main__.py`**

```python
from project_name.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
```

**`src/project_name/cli.py`**

```python
from argparse import ArgumentParser


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="project-name")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        parser.exit(status=0, message="project-name 0.1.0\n")
    return 0
```

**`tests/test_cli.py`**

```python
from project_name.cli import main


def test_main_returns_success_for_default_invocation() -> None:
    assert main([]) == 0
```

## Testing

- **Framework**: `pytest`
- **Test discovery**: `test_*.py` files containing `test_*` functions.
- **Run command**: `python -m pytest tests/ -v`
- **Fixtures**: Use pytest fixtures in `conftest.py`. Do not use `unittest.TestCase`.
- **Coverage**: `python -m pytest --cov=src tests/`
- **Minimum coverage**: 80% overall. Never merge below this threshold without exemption.
- **Test isolation**: Each test must run independently. No test ordering assumptions. Use fresh fixtures per test; prefer `scope="function"` (default). No module-level or session-scoped mutable state.
- **Custom markers**: Use `@pytest.mark.slow` for >1s tests. Register all markers in `pyproject.toml` under `[tool.pytest.ini_options].markers`.
- **Naming**:
  - Files: `test_<module_name>.py`
  - Functions: `test_<behavior>_<condition>()`
  - Example: `test_load_config_raises_on_missing_file()`
- **Assert style**: Use plain `assert` statements (not `self.assertEqual`).
- **Parametrize**: Use `@pytest.mark.parametrize` for data-driven tests.
  ```python
  @pytest.mark.parametrize("input_val,expected", [(1, 2), (2, 4), (3, 6)])
  def test_double(input_val: int, expected: int) -> None:
      assert double(input_val) == expected
  ```
- **Mocks**: Use `unittest.mock` directly. Use pytest's `monkeypatch` for environment variables, paths, module attributes, and process state. Do not add `pytest-mock` unless the user approves it.
- **Test directory scale**: Keep `tests/` flat for small projects. When the package has more than five modules or multiple subpackages, mirror the `src/` structure under `tests/`.

### Test Quality Requirements

- **Behavior over implementation**: Test externally observable behavior, not private implementation details.
- **Boundary coverage**: Cover empty input, single item, many items, invalid input, missing files, permission failures, timeouts, malformed data, and platform-specific branches.
- **Error paths**: Every documented exception path should have a test.
- **Regression tests**: Every bug fix needs a test that fails before the fix and passes after it when feasible.
- **Temporary filesystem**: Use `tmp_path` for file tests. Never write tests to the repository root, user home, `/tmp`, or `%TEMP%` directly.
- **Time control**: Avoid real sleeps. Use injected clocks, small timeout values, or monkeypatched time sources.
- **Network isolation**: Unit tests must not call the public internet. Use local fakes, adapters, or approved integration-test markers.
- **Randomness**: Seed non-security randomness in tests. For security randomness, test shape and validation, not exact values.
- **Cross-platform assertions**: Avoid hardcoded path separators, OS-specific error text, and platform-specific ordering unless the test is explicitly platform-gated.
- **Slow tests**: Mark slow tests and keep them out of default quick feedback unless the project requires them.
- **Property-style checks**: Use table-driven tests by default. Ask before adding property-testing libraries.
- **Mutation risk**: For complex logic, include tests that would fail for common off-by-one, missing-branch, and wrong-sort-order mistakes.

## Configuration

- **Config format**: TOML (`pyproject.toml` for tool config, `.toml` files for app config).
- **Environment variables**: Access via `pydantic-settings` or `os.environ`. Never hardcode secrets.
- **`.env` files**: Use `.env` for local development secrets. Add `.env` to `.gitignore`.
- **`pyproject.toml` sections**: Configure `ruff`, `mypy`, and `pytest` under `[tool.*]`.
- **Config precedence**: Use this order unless the project specifies otherwise: CLI arguments > environment variables > local config file > project defaults.
- **Example files**: Commit `.env.example` with placeholder names only. Never commit real values.
- **Redaction**: Redact config values whose key names contain `token`, `secret`, `password`, `key`, `credential`, `cookie`, or `authorization`.
- **Complete `pyproject.toml` template**:
  ```toml
  [build-system]
  requires = ["hatchling"]
  build-backend = "hatchling.build"

  [project]
  name = "project-name"
  version = "0.1.0"
  requires-python = ">=3.14"
  dependencies = []
  readme = "README.md"
  license = "MIT"

  [project.scripts]
  project-name = "project_name.__main__:main"

  [tool.hatch.build.targets.wheel]
  packages = ["src/project_name"]

  [tool.ruff]
  line-length = 88

  [tool.ruff.lint]
  select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM", "T20", "S110", "EM", "C90", "S", "PGH", "RUF", "RUF100"]

  [tool.ruff.lint.per-file-ignores]
  "tests/**" = ["T201"]

  [tool.ruff.lint.mccabe]
  max-complexity = 10

  [tool.mypy]
  strict = true
  python_version = "3.14"
  warn_unused_configs = true
  warn_return_any = true
  no_implicit_optional = true
  show_error_codes = true

  [tool.pytest.ini_options]
  testpaths = ["tests"]
  addopts = "-ra --strict-markers --strict-config"
  markers = ["slow: marks tests as slow (>1s)"]
  ```

**`.env.example`**

```dotenv
APP_ENV=development
APP_LOG_LEVEL=INFO
APP_DATABASE_URL=
APP_API_TOKEN=
```

**`config.example.toml`**

```toml
[app]
environment = "development"
log_level = "INFO"

[limits]
request_timeout_seconds = 30
max_input_bytes = 10485760
```

## Concurrency

- **Default**: Synchronous code. Use `asyncio` only when I/O-bound work justifies it (≥3 concurrent I/O calls or user explicitly requests async).
- **If async is required**: Use `async`/`await` with `asyncio`. No `threading` or `multiprocessing`. If threading/process pools seem necessary, ask the user.
- **HTTP clients**: Use `httpx` if async is needed; `requests` for synchronous.
- **Never mix** sync and async code. If you must call a sync function from async, use `asyncio.to_thread()`. If you must call an async function from sync, use `asyncio.run()`.
  ```python
  result = await asyncio.to_thread(blocking_function, arg1, arg2)
  result = asyncio.run(async_function(arg1))
  ```
- **Async file I/O**: Use `asyncio.to_thread()` for occasional file reads/writes inside an event loop. Ask before adding `aiofiles`; use it only when async file I/O is frequent enough to justify the dependency.

### Concurrency Correctness

- **Structured concurrency**: Prefer `asyncio.TaskGroup` for related concurrent tasks so failures cancel the group predictably.
- **Timeouts everywhere**: Every network call, subprocess, lock acquisition, queue receive, and long-running await must have a timeout or documented reason.
- **Cancellation-safe cleanup**: Use `try/finally` or async context managers to release resources when a task is cancelled.
- **Backpressure**: Bound queues and concurrent task counts. Never spawn unbounded tasks for untrusted or large input.
- **Shared state**: Avoid shared mutable state. If it is required, protect it with the appropriate lock and keep critical sections small.
- **Idempotency**: Retried operations should be idempotent or protected by idempotency keys when they mutate external systems.
- **Ordering**: Document whether concurrent results preserve input order. Test both ordered and unordered behavior.
- **Exception handling**: Do not hide task exceptions. Gather and surface failures with enough context to retry or diagnose.
- **CPU-bound work**: Do not put CPU-heavy work in the event loop. Ask before adding process pools or native/vectorized dependencies.

## File I/O

- **Encoding**: Always specify `encoding="utf-8"` when calling `open()`. Never rely on platform default encoding (Windows defaults to `cp1252`).
  ```python
  with open(path, encoding="utf-8") as f:
      ...
  ```
- **Path handling**: Always use `pathlib.Path` for all paths. Never hardcode `/` or `\\` as separators.
- **Dict access**: Use `.get()` with a default or check `in` before key access when the key may not exist. Reserve `d[key]` for keys that must exist.

## Performance

All production code must be written with algorithmic efficiency and resource awareness. Every function should have a known time and space complexity. Never write O(n²) when O(n) or O(n log n) is achievable.

### Algorithmic Complexity

- **State complexity explicitly**: Every function that contains a loop, recursion, or algorithmic logic must document its time and space complexity in the docstring.
  ```python
  def find_duplicates(items: list[int]) -> list[int]:
      """Find duplicate integers in a list.

      Args:
          items: List of integers to check.

      Returns:
          List of duplicate values (each appearing once).

      Time complexity: O(n)
      Space complexity: O(n)
      """
      seen: set[int] = set()
      duplicates: set[int] = set()
      for item in items:
          if item in seen:
              duplicates.add(item)
          seen.add(item)
      return sorted(duplicates)
  ```
- **Default target**: O(n) for linear scans and lookups. O(n log n) for sorting. Never accept O(n²) nested loops when a hash map, set, or sort-then-scan solves it in O(n) or O(n log n).
- **Before writing nested loops**: Ask whether a dictionary, set, sorting pass, two-pointer technique, or sliding window can reduce the complexity.

### Dynamic Programming

- **Use DP when**: The problem has overlapping subproblems AND optimal substructure. If the naive recursive solution recomputes the same subproblem, DP applies.
- **Top-down (memoization)**: Use `@functools.cache` or `@functools.lru_cache` for recursive solutions. Prefer this when the recurrence is natural and not all subproblems are needed.
  ```python
  from functools import cache

  @cache
  def fibonacci(n: int) -> int:
      if n < 2:
          return n
      return fibonacci(n - 1) + fibonacci(n - 2)
  ```
- **Bottom-up (tabulation)**: Use an iterative array/table approach when all subproblems must be solved or when avoiding recursion depth limits. Prefer this for production code where stack safety matters.
  ```python
  def fibonacci(n: int) -> int:
      if n < 2:
          return n
      dp: list[int] = [0, 1]
      for i in range(2, n + 1):
          dp.append(dp[i - 1] + dp[i - 2])
      return dp[n]
  ```
- **Space optimization**: If the DP recurrence only uses the last k states, reduce the table from O(n) to O(k) space. Never store the full table when a rolling window suffices.
  ```python
  def fibonacci(n: int) -> int:
      if n < 2:
          return n
      prev, curr = 0, 1
      for _ in range(2, n + 1):
          prev, curr = curr, prev + curr
      return curr
  ```
- **Common DP patterns to apply**:
  - **0/1 Knapsack**: Item selection with capacity constraint.
  - **Longest Common Subsequence / Longest Increasing Subsequence**: Sequence comparison.
  - **Edit Distance**: String similarity / diff algorithms.
  - **Coin Change**: Minimum coins for amount.
  - **Matrix Chain Multiplication**: Optimal parenthesization.
  - **Interval DP**: Optimal partitioning, burst balloons, merge stones.
  - **Bitmask DP**: Small state-space enumeration (n ≤ 20).
  - **Greedy first**: If a greedy choice property exists, prefer greedy over DP — it is O(n log n) or O(n) instead of O(n²) or O(n³).

### CPU Efficiency

- **Use built-in functions and C-extensions**: `sum()`, `min()`, `max()`, `sorted()`, `map()`, `filter()`, `any()`, `all()` are implemented in C. Always prefer them over manual Python loops.
- **Comprehensions over loops**: Use list/dict/set comprehensions instead of append-in-loop patterns. They are faster due to optimized internal iteration.
  ```python
  squares = [x * x for x in range(1000)]
  ```
- **Generator expressions for large data**: Use `(...)` generator expressions instead of `[...]` list comprehensions when the result is consumed once (e.g., `sum()`, `any()`, `max()`). This avoids allocating the full list in memory.
  ```python
  total = sum(x * x for x in range(1_000_000))
  ```
- **Avoid repeated work in loops**: Hoist computations, method lookups, and attribute accesses outside hot loops.
  ```python
  result = []
  append = result.append
  for item in large_list:
      append(transform(item))
  ```
- **Use `itertools`**: `groupby`, `chain`, `islice`, `product`, `permutations`, `combinations`, `accumulate`, `batched` (3.14+) for efficient iteration patterns. Never reimplement these manually.
- **Use `collections`**: `Counter`, `defaultdict`, `deque`, `OrderedDict` for specialized data structures. Never manually implement counting, double-ended queues, or grouping.
- **Use `bisect`**: For binary search on sorted sequences. Never linear-search a sorted list.
- **Use `heapq`**: For priority queues and top-k problems. Never sort the entire list when only the top k elements are needed.
- **Prefer `set` and `dict` lookups**: O(1) average. Never use `x in list` for membership testing on large collections — convert to `set` first.
- **String concatenation**: Use `"".join(parts)` not `+=` in loops. `join` allocates once.
- **Avoid `deepcopy`**: Use explicit constructors or `copy()` for shallow copies. `deepcopy` traverses the entire object graph recursively.
- **Prefer `__slots__`** on data-heavy classes to reduce per-instance memory overhead by ~40-50% and speed up attribute access.
  ```python
  class Point:
      __slots__ = ("x", "y")

      def __init__(self, x: float, y: float) -> None:
          self.x = x
          self.y = y
  ```
- **`functools.lru_cache`**: Use for pure functions with repeated inputs. Explicitly set `maxsize` when the cache has a known bound.

### Data Structure Selection

Choose containers based on access pattern, mutation pattern, ordering needs, and data size.

| Workload | Recommended structure/API | Avoid |
|---|---|---|
| Membership checks on many items | `set[T]` | repeated `x in list` |
| Keyed lookup or grouping by id | `dict[Key, Value]` | parallel lists |
| Frequency counting | `collections.Counter` | manual count dictionaries |
| Grouping into lists | `collections.defaultdict(list)` | repeated `setdefault` in hot paths |
| FIFO queue | `collections.deque` | `list.pop(0)` |
| LIFO stack | `list.append` / `list.pop` | custom stack classes |
| Priority queue | `heapq` | sorting on every insert |
| Top-k values | `heapq.nlargest` / `heapq.nsmallest` | sorting the full collection |
| Sorted insert/search | `bisect` | linear scan of sorted data |
| Fixed immutable record | `@dataclass(frozen=True, slots=True)` or `NamedTuple` | unstructured tuples for public APIs |
| Mutable internal record | `@dataclass(slots=True)` | ad hoc dicts |
| Streaming one-pass data | generator / iterator | materialized list |
| Numeric arrays after approval | `array`, `memoryview`, or approved `numpy` | Python object lists for large numeric data |
| LRU memoization | `functools.lru_cache(maxsize=...)` | unbounded custom caches |

## Design Principles and Patterns

Use design patterns as tools, not obligations. Do not add classes, indirection, interfaces, factories, or inheritance just to match a classic pattern. A pattern is acceptable only when it reduces real complexity, improves testability, protects an external boundary, or isolates behavior that is expected to vary. Simpler code that is faster and easier to read wins.

- **Start simple**: Prefer small functions and cohesive modules before classes. Add classes when shared state, invariants, lifecycle, or a public object model makes them clearer.
- **Composition over inheritance**: Prefer passing collaborators, callables, and data objects. Use inheritance only for true subtype relationships or framework integration.
- **Value objects**: Use `@dataclass(frozen=True, slots=True)` for small immutable records. Use plain tuples only for tiny local values where field names do not matter.
- **Protocols for boundaries**: Use `Protocol` when code depends on behavior rather than a concrete class. Keep protocols small and capability-based.
- **Dependency injection without frameworks**: Pass dependencies explicitly through function parameters, constructors, or configuration objects. Do not introduce dependency injection frameworks.
- **Context managers**: Use context managers for files, locks, network clients, database connections, temporary directories, and any resource with setup/teardown.
- **Strategy**: Use a callable or small `Protocol` when one algorithm must vary behind a stable interface. Avoid class hierarchies for one-off branches.
- **Adapter**: Wrap external APIs, CLIs, filesystems, databases, and HTTP services behind a narrow local interface so calling code is not coupled to vendor details.
- **Factory**: Use a factory function only when construction has real branching, validation, environment selection, or dependency wiring. Avoid factory classes by default.
- **Repository**: Use a repository boundary only when persistence logic is complex enough to isolate from business rules. For simple scripts, direct `sqlite3` or file access may be clearer.
- **Facade**: Use a facade when a subsystem has many steps and callers need one stable entry point. Keep the facade thin.
- **Command**: Use command objects or functions for queued, retryable, undoable, or auditable operations. Otherwise a function is enough.
- **Observer/event bus**: Avoid unless multiple independent consumers truly need event notifications. Prefer direct calls for simple flows.
- **Singleton**: Avoid. Prefer explicit module-level constants for immutable values or pass shared dependencies explicitly.
- **Service locator/global registry**: Avoid. Hidden dependencies make tests and performance behavior harder to reason about.
- **Deep inheritance**: Avoid inheritance chains beyond one or two levels. Prefer composition and protocols.
- **Metaclasses and monkey patching**: Prohibited unless explicitly requested and justified.
- **Performance gate**: If a pattern adds allocation, dynamic dispatch, reflection, decorators, indirection, or per-call object creation in a hot path, measure it before keeping it.

### GPU and Parallel Computation

- **GPU acceleration**: Ask before introducing GPU libraries (`cuda`, `cupy`, `torch`, `numba`). Only use when the workload is embarrassingly parallel with large data arrays (≥100K elements). Document the GPU requirement.
- **CPU parallelism**: Ask before introducing `multiprocessing.Pool`, `ProcessPoolExecutor`, or `ThreadPoolExecutor`. None are permitted without explicit approval.
- **Vectorized operations**: When `numpy` or `pandas` is approved, always prefer vectorized operations over element-wise Python loops. Never iterate rows of a DataFrame.
- **Batching**: Process data in batches, not one item at a time. Batch size should be tuned, not guessed. Start with 1000 and benchmark.
- **Memory-mapped files**: Use `mmap` for large files that cannot fit in memory. Never `read()` a multi-GB file into RAM.

### Memory Efficiency

- **Use generators** (`yield`) for large or infinite sequences. Never materialize a full list when the consumer processes items one at a time.
  ```python
  def read_lines(path: Path) -> Iterator[str]:
      with open(path, encoding="utf-8") as f:
          yield from f
  ```
- **Use `__slots__`** on classes that will be instantiated thousands of times or more.
- **Avoid holding references**: Release large objects explicitly (`del`) when they are no longer needed, especially in long-running processes.
- **Profile before optimizing**: Use `cProfile` and `memory_profiler` to identify actual bottlenecks. Never optimize based on assumption.
  ```console
  python -m cProfile -s cumulative src/project_name/__main__.py
  ```
- **Lazy evaluation**: Use `itertools` and generator expressions to defer computation until needed.
- **Chunk large data**: Process files and datasets in fixed-size chunks rather than loading entirely into memory.

### Benchmarking and Profiling

- **Before optimizing**: Always profile. Use `cProfile` for CPU, `memory_profiler` for memory, `timeit` for microbenchmarks.
- **Benchmark pattern**:
  ```python
  import logging
  import timeit

  logger = logging.getLogger(__name__)
  time_taken = timeit.timeit(
      "my_function(test_data)",
      setup="from __main__ import my_function, test_data",
      number=1000,
  )
  logger.info("Average: %.6fs per call", time_taken / 1000)
  ```
- **Document performance characteristics**: Add `Time complexity` and `Space complexity` to docstrings of non-trivial functions.
- **Never premature-optimize**: Write correct code first. Profile. Then optimize the actual bottleneck.

### Benchmark Template

Use a repeatable benchmark file for hot paths instead of one-off timing snippets. Keep benchmark data small enough for CI when possible and add larger local-only benchmarks when needed.

```python
from pathlib import Path
from time import perf_counter

from project_name.module import run_hot_path


def main() -> int:
    input_path = Path("tests/fixtures/representative_input.txt")
    data = input_path.read_text(encoding="utf-8")

    started = perf_counter()
    result = run_hot_path(data)
    elapsed_seconds = perf_counter() - started

    print(
        {
            "items": len(data),
            "elapsed_seconds": round(elapsed_seconds, 6),
            "result_size": len(result),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Production code must not use `print()` for diagnostics, but standalone local benchmark scripts may print concise machine-readable results.

### Performance Budgets

- **Define a budget for hot paths**: For user-facing commands, background jobs, parsers, batch processors, and API handlers, document the expected input size and acceptable runtime or memory use.
- **Measure representative data**: Benchmark with realistic data shapes, not only tiny examples.
- **Avoid per-item setup**: Do not create clients, compile regexes, parse config, open files, or allocate large helpers inside tight loops.
- **Bound memory growth**: Use streaming, chunking, pagination, or generators when input size can grow beyond memory.
- **Cache deliberately**: Cache only pure or stable results. Bound cache size and provide invalidation when data can change.
- **Avoid hidden quadratic behavior**: Watch for repeated list membership checks, string concatenation in loops, nested scans, and repeated sorting.
- **Fail before exhaustion**: Validate input sizes before processing when untrusted input could exhaust CPU, memory, disk, or network resources.
- **Keep observability cheap**: Logging and metrics in hot paths must avoid expensive formatting, serialization, or high-cardinality values.
- **Optimize after proof**: Keep a benchmark or profiler output note for non-obvious optimizations that reduce readability.

## Standard Library Preferences

Use stdlib when it covers the use case fully. Use the third-party option only when the stdlib lacks a required feature or when the user explicitly requests the third-party library:

| Use | Instead of |
|---|---|
| `pathlib.Path` | `os.path` |
| `tomllib` (3.11+) | `tomli` |
| `dataclasses` | `attrs` (ask the user before using) |
| `logging` | `loguru` (ask the user before using) |
| `sqlite3` | External SQLite wrappers |
| `json` | `orjson` (only when the user identifies JSON serialization as a measured bottleneck) |
| `http.server` | Flask (for single-endpoint dev/test servers with no auth) |
| `argparse` | `click` (ask the user before using) |
| `enum.Enum` | String constants |
| `collections.namedtuple` | Plain tuples with positional access |
| `datetime` (stdlib) | `pendulum` / `arrow` |
| `re` | `regex` (only if a specific `regex` feature is required that `re` lacks, e.g., fuzzy matching) |
| `urllib.parse` | Manual string splitting |

## Deprecated Standard Library Modules

Never use these removed or deprecated modules. Prefer modern equivalents:

| Removed/Deprecated | Use Instead |
|---|---|
| `cgi` | `multipart` or manual parsing |
| `imp` | `importlib` |
| `optparse` | `argparse` |
| `asyncore` / `asynchat` | `asyncio` |
| `smtpd` | `aiosmtpd` |
| `distutils` | `setuptools` / `hatchling` |
| `lib2to3` | `lib2to3` is frozen, do not use |
| `tkinter.tix` | `tkinter.ttk` |

## Prohibited Patterns

- No `eval()`, `exec()`, or `compile()`. If one is genuinely required, the user must explicitly request it and document the reason in a code comment.
- No `globals()` or `locals()` manipulation.
- No mutable default arguments (`def foo(items=[]):`). Use `None` and initialize inside.
- No star imports (`from os import *`).
- No string concatenation for paths. Use `/` with `pathlib.Path`.
- No `print()` in production code. Use `logging` for diagnostics and pytest assertions for tests. Short-lived local debugging prints must be removed before completion.
- No hardcoded secrets, API keys, tokens, or passwords.
- No `# type: ignore` without a comment explaining why.
- No `TODO` or `FIXME` without an associated issue number.
- No `__del__` for cleanup. Use context managers.
- No metaclasses. If you believe one is required, ask the user before writing it.
- No monkey-patching stdlib or third-party modules (exception: `unittest.mock.patch` in test code is permitted).
- No `is` for value comparisons (use `==`): `x is 5` is wrong, use `x == 5`.
- No `x == None` or `x != None` (use `x is None` / `x is not None` per PEP 8).
- No `type(x) == SomeType` (use `isinstance(x, SomeType)`).
- No catching `BaseException` (use `Exception` at minimum; `KeyboardInterrupt` and `SystemExit` must propagate).
- No `sys.exit()` outside `if __name__ == "__main__"` blocks.
- No `input()` in production code.
- No `os.system()` (use `subprocess.run()`).
- No bare `raise` outside an active `except` block.
- No `deepcopy` when a shallow copy or explicit construction suffices.
- No `type()` checks for isinstance patterns.
- No f-strings in logging calls (use `%s` formatting for lazy evaluation: `logger.info("value=%s", val)`).
- No `from __future__ import annotations` (unnecessary for 3.14+; can break runtime type checks).
- No `assert` in non-test code. Use explicit `if` + `raise` for validation. `assert` is stripped by `python -O`.
- No `__import__()`. Use `importlib.import_module()` if dynamic imports are required.
- No `subprocess.run()` without a `timeout` parameter.
- No unchecked `dict.get()` — if the default is `None`, check before use or use a non-None sentinel.

## `.gitignore` (Python)

Always include these entries:

```
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv/
.env
*.cover
htmlcov/
.mypy_cache/
.ruff_cache/
.pytest_cache/
```

## Build and Distribution

- **Build system**: Use `hatchling` as the build backend in `pyproject.toml`.
- **Build command**: `python -m build`
- **No `setup.py`**: Use `pyproject.toml` exclusively. Hatchling supports PEP 660 editable installs natively (`python -m pip install -e .`). No `setup.py` stub is needed.

## Delivery and CI

Every non-trivial Python project should define repeatable local validation and, when hosted in a shared repo, equivalent CI validation.

- **CI parity**: CI must run the same core commands documented locally: ruff check, ruff format check, mypy, pytest, coverage, pip-audit, and build.
- **Platform matrix**: For portable projects, run at least one Linux CI job. Add Windows and macOS jobs when code touches paths, subprocesses, file locking, shells, native dependencies, or OS APIs.
- **Python matrix**: Test the minimum supported Python version and the newest stable patch version available in CI.
- **Build artifacts**: Validate source distributions and wheels with `python -m build` before release.
- **Release checklist**: Verify version bump, changelog or release notes, dependency audit, tests, type checks, build, and install smoke test.
- **Install smoke test**: In a clean virtual environment, install the built wheel and run a minimal import or CLI command.
- **Generated files**: Do not commit generated artifacts unless the project explicitly tracks them. If tracked, document how to regenerate them.
- **Exit codes**: CLI tools must return `0` on success and non-zero on failure. Use distinct documented codes only when helpful.
- **Rollback**: For migrations, destructive operations, or external mutations, document rollback or recovery steps.
- **Reproducibility**: Avoid hidden machine state. All required environment variables, files, services, and credentials must be documented.

## Lint and Validation Commands

Run these after every code change. All must pass with zero errors:

```console
python -m ruff check src/ tests/
python -m ruff format --check src/ tests/
python -m mypy --strict src/
python -m pytest tests/ -v
python -m pytest --cov=src tests/
python -m pip-audit
python -m build
```

On Windows PowerShell, use the same commands after activating `.venv`. On macOS, Ubuntu, and Fedora, use the same commands after `source .venv/bin/activate`. If activation is not possible, replace `python` with the verified interpreter command for that platform.

## API Integration

- **HTTP client**: `requests` (sync) or `httpx` (async or sync).
- **Connection pooling**: Always use `requests.Session` or `httpx.Client` as a context manager for repeated calls. Never create a new connection per request.
  ```python
  with requests.Session() as session:
      response = session.get(url, timeout=30)
  ```
  ```python
  with httpx.Client() as client:
      response = client.get(url, timeout=30)
  ```
- **Retry logic**: Use `tenacity` for retry with bounded exponential backoff when retries are required. Never retry indefinitely.
- **Rate limiting**: Prefer a small local token-bucket implementation. Ask before adding `aiolimiter` or `ratelimit`.
- **Timeouts**: Always set explicit timeouts. Never use infinite waits.
  ```python
  requests.get(url, timeout=30)
  ```

## Database

- **ORM**: Do not assume one. Ask before introducing SQLAlchemy, Django ORM, or others.
- **Migrations**: Do not assume a tool. Ask before introducing Alembic or others.
- **Raw SQL**: If no ORM is specified, use `sqlite3` (stdlib) with parameterized queries only.
  ```python
  cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
  ```

### Database and Migration Safety

- **Transactions**: Wrap multi-step writes in transactions. Commit only after all invariants are satisfied.
- **Rollback path**: Every schema or data migration needs a rollback, backup, or explicit forward-only recovery plan.
- **Backups**: For destructive or large migrations, require a backup or export step before mutation.
- **Idempotency**: Migrations and seed scripts should be safe to re-run or should detect prior completion clearly.
- **Locking**: Document expected locks and downtime. Avoid long transactions around unbounded reads or network calls.
- **Batching**: Process large updates in batches with progress logging and safe resume behavior.
- **Schema compatibility**: For services, prefer expand-and-contract migrations so old and new code can run during deploys.
- **Seed data**: Keep seed data deterministic, minimal, and environment-safe. Never seed production secrets.
- **Query plans**: For performance-sensitive queries, inspect the query plan and add indexes deliberately.
- **Foreign keys**: Enable and test foreign-key constraints when using SQLite.
- **Time and money**: Store UTC timestamps and exact decimal values. Do not use local naive datetimes or floats for currency.

## Security

- **Never** commit secrets, credentials, or API keys.
- **Never** use `pickle` to deserialize untrusted data.
- **Never** use `subprocess` with `shell=True`. If you believe it is required, ask the user and ensure all interpolated values are passed via the `args` list, never via the command string.
- **SSL/TLS**: Always verify certificates. Never set `verify=False` in `requests` or `httpx`.
- **Always** use parameterized queries for database access.
- **Always** validate external input (HTTP payloads, CLI args, env vars, file contents) with `pydantic` models before use.
- **Always** use HTTPS for external requests.
- **Dependencies**: Pin all versions. Run `pip-audit` to check for known vulnerabilities.
- **YAML parsing**: Prefer TOML or JSON. If YAML is required and `PyYAML` is approved, always use `yaml.safe_load()`, never `yaml.load()`.
- **Temporary files**: Use `tempfile.mkstemp()` or `tempfile.TemporaryDirectory()` — never predictable names or hardcoded temp paths.
- **Security-sensitive random values**: Use `secrets` module (not `random`) for tokens, passwords, and nonces.

### Adversarial Input and Abuse Cases

- **Threat model first**: For code that handles files, network input, credentials, subprocesses, or user-controlled paths, identify what an attacker controls before implementing.
- **SSRF prevention**: Do not fetch arbitrary user-provided URLs in production code without an allowlist, scheme validation, DNS/IP checks, redirects policy, and timeouts.
- **Archive extraction**: Validate archive member paths before extraction. Reject absolute paths, parent traversal, symlinks, device files, and excessive decompressed size.
- **XML**: Avoid XML for untrusted input. If required, ask before adding a hardened parser and disable external entities.
- **CSV injection**: When exporting CSV for spreadsheets, escape or reject cells starting with `=`, `+`, `-`, or `@` when the file may be opened in spreadsheet software.
- **Regex DoS**: Avoid nested quantifiers and ambiguous alternation. For untrusted input, keep patterns simple and enforce input length limits.
- **Untrusted templates**: Never render user-controlled templates. Render trusted templates with escaped user data.
- **Open redirects**: Validate redirect targets against an allowlist or same-origin policy.
- **Request size limits**: Enforce size limits before parsing files, JSON, forms, archives, and request bodies.
- **Secrets in exceptions**: Sanitize exception messages crossing API, CLI, log, or UI boundaries.
- **Privilege boundaries**: Do not silently elevate privileges, change file ownership, alter ACLs, or write outside the project/configured data directory.
- **Dry-run for destructive actions**: File deletion, migration, remote mutation, and bulk update tools should support dry-run or preview unless the user explicitly requests otherwise.

## Data Security

Data security encompasses encryption, hashing, key management, data masking, and secure data handling patterns. Follow these rules for any code that processes, stores, or transmits sensitive data.

### Encryption

- **Symmetric encryption**: Ask before adding `cryptography`. If approved, use `Fernet` for symmetric encryption at rest. Never implement custom encryption.
  ```python
  from cryptography.fernet import Fernet

  key = Fernet.generate_key()
  cipher = Fernet(key)
  encrypted = cipher.encrypt(b"secret data")
  decrypted = cipher.decrypt(encrypted)
  ```
- **AES-GCM**: With approved `cryptography`, use `cryptography.hazmat.primitives.ciphers.aead.AESGCM` for authenticated encryption when you need associated data.
  ```python
  from cryptography.hazmat.primitives.ciphers.aead import AESGCM

  key = AESGCM.generate_key(bit_length=256)
  aesgcm = AESGCM(key)
  nonce = os.urandom(12)
  encrypted = aesgcm.encrypt(nonce, b"secret data", None)
  decrypted = aesgcm.decrypt(nonce, encrypted, None)
  ```
- **Never use**: `AES-CBC` without HMAC (unauthenticated), `RC4`, `DES`, `3DES`, `Blowfish`, or any custom cipher. These are broken or obsolete.
- **Never hardcode keys**: Load encryption keys from environment variables, a secrets manager, or a key management service. Never commit keys to source control.
- **IV/Nonce**: Always generate a unique, cryptographically random IV or nonce for each encryption operation. Never reuse a nonce with the same key.
  ```python
  import os
  nonce = os.urandom(12)
  ```

### Hashing

- **Password hashing**: Use `hashlib.scrypt()` or `bcrypt` (third-party). Never use `md5`, `sha1`, or plain `sha256` for passwords.
  ```python
  import hashlib
  import os

  salt = os.urandom(16)
  hashed = hashlib.scrypt(b"password", salt=salt, n=16384, r=8, p=1, dklen=64)
  ```
- **bcrypt pattern** (ask user before introducing `bcrypt` library):
  ```python
  import bcrypt

  hashed = bcrypt.hashpw(b"password", bcrypt.gensalt(rounds=12))
  bcrypt.checkpw(b"password", hashed)
  ```
- **Password hashing rules**:
  - Always salt. Never hash without a unique per-user salt.
  - Use a work factor / cost parameter appropriate for the hardware. Start with `n=16384` for scrypt or `rounds=12` for bcrypt.
  - Never truncate passwords before hashing.
  - Store the salt alongside the hash (they are not secrets).
- **Data integrity hashing**: Use `hashlib.sha256` or `hashlib.sha512` for file checksums, data integrity verification, and deduplication keys.
- **Never use `hashlib.md5` or `hashlib.sha1`** for security purposes. They are collision-broken. Only acceptable for non-security checksums (e.g., cache keys) with a comment documenting why.
- **HMAC**: Use `hmac` module for message authentication. Never implement HMAC manually.
  ```python
  import hmac
  import hashlib

  signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
  ```

### Key and Secret Management

- **Storage hierarchy** (preferred order):
  1. Cloud secrets manager (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) — ask before introducing SDK.
  2. Environment variables — acceptable for local dev and simple deployments.
  3. `.env` files — local development only. Must be in `.gitignore`.
  4. Never hardcode in source.
- **Key rotation**: Design systems to support key rotation without downtime. Store key identifiers alongside encrypted data so the correct key can be selected during decryption.
  ```python
  class KeyStore:
      def __init__(self) -> None:
          self._keys: dict[str, bytes] = {}
          self._active_id: str = ""

      def get_key(self, key_id: str) -> bytes:
          return self._keys[key_id]

      @property
      def active_key_id(self) -> str:
          return self._active_id

      @property
      def active_key(self) -> bytes:
          return self._keys[self._active_id]
  ```
- **Key derivation**: Use `hashlib.pbkdf2_hmac()` or `cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC` for deriving keys from passwords. Never use a password directly as an encryption key.
  ```python
  import hashlib

  key = hashlib.pbkdf2_hmac("sha256", password, salt, iterations=600_000, dklen=32)
  ```
- **Memory cleanup**: Zero out sensitive byte arrays after use. Python does not guarantee this automatically.
  ```python
  import ctypes

  def secure_zero(data: bytearray) -> None:
      ctypes.memset(ctypes.addressof((ctypes.c_char * len(data)).from_buffer(data)), 0, len(data))
  ```
- **Never log secrets**: Do not log API keys, passwords, tokens, session IDs, or auth headers. Use `str.masked` or equivalent patterns when debugging.

### Data Masking and Redaction

- **PII redaction**: Never log, store in plaintext, or expose in error messages: SSNs, credit card numbers, email addresses, phone numbers, dates of birth, IP addresses (when GDPR applies).
- **Masking pattern**:
  ```python
  def mask_email(email: str) -> str:
      local, domain = email.split("@", 1)
      return f"{local[0]}***@{domain}"
  ```
- **Credit card masking**: Show only last 4 digits. Store only a tokenized reference, never the full PAN.
  ```python
  def mask_card(card: str) -> str:
      return f"****-****-****-{card[-4:]}"
  ```
- **Tokenization**: Replace sensitive values with irreversible tokens before storage. Keep the mapping in a secured, access-controlled store. Ask before introducing a tokenization library.

### Input Sanitization

- **SQL injection**: Always parameterized queries (see Database section). Never f-string or concatenate user input into SQL.
- **Command injection**: Never pass user input to `subprocess` via `shell=True`. Use `args` list form.
  ```python
  subprocess.run(["git", "clone", user_url], timeout=30)
  ```
- **Path traversal**: Always validate and resolve paths. Never trust user-supplied filenames.
  ```python
  def safe_path(base_dir: Path, user_filename: str) -> Path:
      resolved = (base_dir / user_filename).resolve()
      if not resolved.is_relative_to(base_dir.resolve()):
          raise ValueError("Path traversal detected")
      return resolved
  ```
- **HTML/JS injection**: Use a sanitizer library (ask before introducing `bleach` or `nh3`). Never render user input as raw HTML.
- **Deserialization**: Never `pickle.load()` or unsafe `yaml.load()` on untrusted data. Use `json.loads()`, `tomllib`, or `pydantic` model validation.
- **Regex DoS (ReDoS)**: Avoid nested quantifiers and overlapping alternations in regex patterns. Test regex patterns with adversarial inputs for catastrophic backtracking.

### Transport Security

- **Always HTTPS**: No exceptions for production. Use `verify=True` (default) in `requests`/`httpx`.
- **Certificate pinning**: Ask before implementing. Use `ssl` module or `certifi` for explicit certificate bundles.
- **TLS version**: Minimum TLS 1.2. Reject TLS 1.0 and 1.1. Configure via `ssl.SSLContext`.
  ```python
  import ssl

  ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  ctx.minimum_version = ssl.TLSVersion.TLSv1_2
  ```
- **Retry with backoff on auth failures**: Use `tenacity`. Never retry indefinitely on 401/403 — fail fast and alert.

### Data at Rest

- **Encryption at rest**: Encrypt sensitive data before writing to disk or database. Use `Fernet` (see Encryption section).
- **Database column encryption**: Encrypt PII columns before storing. Decrypt only at the application layer, never in the database.
- **File permissions**: On Windows, use `tempfile.mkstemp()` which creates files with restricted permissions. Never create sensitive files in world-readable locations.
- **Secure deletion**: For temporary sensitive files, overwrite before deletion:
  ```python
  def secure_delete(path: Path) -> None:
      size = path.stat().st_size
      with open(path, "r+b") as f:
          f.write(os.urandom(size))
          f.flush()
          os.fsync(f.fileno())
      path.unlink()
  ```

### Session and Token Security

- **Token generation**: Use `secrets.token_urlsafe(32)` for session tokens, API keys, and reset tokens. Minimum 32 bytes of entropy.
  ```python
  import secrets
  token = secrets.token_urlsafe(32)
  ```
- **Token expiry**: All tokens must have an expiry. Validate expiry on every use.
- **JWT**: Ask before using `PyJWT`. Always verify signature, expiry, and issuer. Never accept `alg=none`.
- **Session IDs**: Regenerate after login and privilege escalation. Never reuse across authentication levels.

### Audit Logging

- **Log security events**: Login attempts, permission changes, data access, encryption operations, key rotations, and failed validations.
- **Structured format**: Use consistent log fields for security events: `event_type`, `user_id`, `timestamp`, `source_ip`, `success`.
  ```python
  logger.info(
      "auth.login",
      extra={"event_type": "login", "user_id": user_id, "success": True},
  )
  ```
- **Tamper resistance**: Append-only logs. Never allow log deletion in production.
- **Never log**: Passwords (even hashed), full credit card numbers, auth tokens, encryption keys, or raw PII.

### Data Security Prohibited Patterns

- No `hashlib.md5()` or `hashlib.sha1()` for security purposes.
- No `random` module for security-sensitive values. Use `secrets`.
- No hardcoded encryption keys, API keys, or passwords in source code.
- No `pickle.load()` on untrusted data.
- No unsafe `yaml.load()` on untrusted data. Use `yaml.safe_load()` only when `PyYAML` is approved.
- No custom encryption implementations.
- No AES-CBC without HMAC (unauthenticated encryption).
- No password storage without salting and stretching.
- No logging of secrets, tokens, passwords, or PII.
- No user-supplied paths used directly without traversal protection.
- No user input rendered as raw HTML without sanitization.

## Documentation

- **Docstring format**: Google style.
- **Coverage**: All public modules, classes, functions, and methods.
- **Docstrings describe contracts**: Include purpose, arguments, returns, raised exceptions, side effects, and complexity for non-trivial code.
- **Module docstrings**: Use for public modules to explain the module's responsibility and any important platform, security, or performance constraints.
- **Class docstrings**: Explain the invariant or role of the class. Do not repeat every attribute if the dataclass fields are self-explanatory.
- **Function docstrings**: Required for public functions and for private functions with non-obvious behavior. Tiny private helpers with clear names may omit docstrings.
- **Examples**: Add docstring examples only when they clarify API usage. Keep examples executable and aligned with tests.
- **Example**:
  ```python
  def load_config(path: Path) -> Config:
      """Load application configuration from a TOML file.

      Args:
          path: Path to the configuration file.

      Returns:
          A validated Config object.

      Raises:
          ConfigError: If the file cannot be read or parsed.
          FileNotFoundError: If the file does not exist.

      Time complexity: O(n) where n is file size.
      Space complexity: O(n) for file contents.
      """
      ...
  ```

## Comments

Prefer clear names, small functions, and direct control flow over comments. Comments are for intent, constraints, invariants, tradeoffs, and non-obvious decisions. They must not narrate code that is already readable.

- **Explain why, not what**: Comment the reason for a choice, not a line-by-line translation of the code.
- **Document invariants**: Put a short comment before complex logic when a condition must remain true across the block.
- **Document tradeoffs**: Comment security, performance, concurrency, compatibility, or platform-specific decisions.
- **Document measured optimizations**: If code is less obvious because it is faster, include the measured reason or benchmark context.
- **Document external constraints**: Note protocol quirks, API limitations, file format rules, or OS behavior that future maintainers cannot infer locally.
- **TODO/FIXME policy**: Do not leave `TODO` or `FIXME` without an issue number, owner, or concrete follow-up.
- **No commented-out code**: Delete dead code. Use version control for history.
- **No decorative banners**: Avoid large section banners, ASCII art, or repeated divider comments.
- **No stale comments**: Update or remove comments when behavior changes.
- **No redundant comments**:
  ```python
  # Increment count by one.
  count += 1
  ```
- **Good comment**:
  ```python
  # Windows can keep recently closed files locked briefly, so retry once
  # before surfacing the cleanup failure.
  ```

## Common Libraries (Ask Before Using)

These libraries require explicit approval before introduction:

| Category | Libraries |
|---|---|
| Web framework | FastAPI, Flask, Django, Litestar, Starlette |
| Database ORM | SQLAlchemy, Django ORM, Tortoise |
| Task queue | Celery, Dramatiq, ARQ |
| Caching | Redis, Memcached, diskcache |
| ML/Data | pandas, numpy, scikit-learn, torch |
| CLI framework | Click, Typer, Rich |
| Templating | Jinja2, Mako |
| WebSocket | websockets, FastAPI WebSocket |
| GPU/Parallel | cuda, cupy, numba, JAX |
| Profiling | memory_profiler, py-spy, line_profiler |
| Cryptography | cryptography, bcrypt, PyJWT, pynacl |
| Sanitization | bleach, nh3, lxml.html.clean |

The following libraries are pre-approved only when the matching section of this document applies: `pytest`, `pytest-cov`, `ruff`, `mypy`, `build`, `pip-audit`, `hatchling`, `pydantic`, `pydantic-settings`, `requests`, `httpx`, and `tenacity`. If a library is not explicitly pre-approved or already present in the project, ask before introducing it.

## Production Audit Workflow

Use this workflow before declaring Python work complete. Score each criterion from 0 to 10. A project reaches production quality only at 100/100, with no criterion below 10.

| Criterion | Requirement |
|---|---|
| Runtime and environment | Interpreter, virtual environment, commands, and platform assumptions are explicit and reproducible across Windows, macOS, Ubuntu, and Fedora. |
| Dependency and supply chain | Dependencies are minimal, pinned, approved, audited, and justified. |
| Architecture and maintainability | Modules are cohesive, boundaries are clear, and public APIs are stable. |
| Type safety | Public and internal functions are annotated and pass `mypy --strict`. |
| Style and static analysis | Formatting, linting, import order, complexity, and prohibited patterns are clean. |
| Testing and coverage | Unit, edge, error-path, integration, and regression tests cover meaningful behavior at 80%+ coverage. |
| Security and data handling | Inputs, secrets, subprocesses, paths, serialization, network calls, and logs are safe. |
| Performance and scalability | Complexity is documented, data sizes are considered, and bottlenecks are measured before optimization. |
| Observability and error handling | Logs, exceptions, retries, timeouts, and boundary errors are actionable without leaking secrets. |
| Packaging and delivery | `pyproject.toml`, `src/` layout, build, CLI entry points, docs, and validation commands are complete. |

### Ten-Round Audit

Run all 10 rounds when producing or materially changing Python code or this guidance. Each round has 10 criteria scored 0 to 10. If a round reaches `100/100` early, change the next round's criteria to a sharper lens that can still expose gaps.

1. **Round 1 - completeness**: Runtime, environment, dependency, style, typing, tests, security, performance, packaging, and docs are present.
2. **Round 2 - portability**: Windows, macOS, Ubuntu, Fedora, paths, encodings, locale, timezone, subprocesses, and filesystem behavior are covered.
3. **Round 3 - supply chain**: Pins, transitive locks, audit results, licenses, indexes, dependency approval, updates, vulnerability exceptions, vendoring, and optional extras are controlled.
4. **Round 4 - API design**: Public surface, compatibility, naming, exceptions, config, CLI, import behavior, deprecation, versioning, and examples are stable.
5. **Round 5 - test quality**: Behavior, edge cases, error paths, regression tests, isolation, filesystem tests, time, network, randomness, and cross-platform assertions are covered.
6. **Round 6 - adversarial security**: Inputs, paths, subprocesses, SSRF, archives, XML/YAML/JSON, regexes, secrets, redirects, and destructive actions are safe.
7. **Round 7 - performance**: Complexity, hot paths, memory, streaming, caching, batching, profiling, budgets, observability cost, and scalability are addressed.
8. **Round 8 - operations**: Logging, metrics, correlation ids, health checks, run summaries, retries, timeouts, exit codes, recovery, and supportability are addressed.
9. **Round 9 - concurrency and data**: Async structure, cancellation, backpressure, shared state, idempotency, data models, validation boundaries, schema evolution, and serialization are sound.
10. **Round 10 - delivery gate**: Local validation, CI parity, platform/Python matrix, build artifacts, install smoke test, release checklist, docs, rollback, and final diff review are complete.

Do not claim completion unless the final round totals `100/100`, every criterion is `10/10`, and validation commands that apply to the project have passed or are explicitly documented as unavailable.

## AI Generation Workflow

When an AI assistant writes or edits Python code under this document, it must follow this workflow.

- **Read first**: Read this file and the local project instructions before editing Python.
- **State assumptions**: Identify target platforms, Python version, dependency policy, data size, and security boundaries before choosing an approach.
- **Clarify only blockers**: Ask the user only when a decision changes architecture, dependencies, destructive behavior, security posture, public API, data model, deployment target, or user-visible behavior. Otherwise make a conservative assumption and document it.
- **Prefer stdlib**: Use the standard library unless an approved dependency is already present or the user approves a new one.
- **Design for tests**: Structure code so important behavior can be tested without network, global state, real sleeps, or user-specific paths.
- **Keep changes scoped**: Do not refactor unrelated files or introduce architecture beyond the requested behavior.
- **Patch with evidence**: After editing, run applicable validation commands and report exact unavailable tools or skipped checks.
- **Self-review**: Review the final diff for portability, naming, comments, dependency creep, security regressions, and performance regressions.
- **No false completion**: Never claim code is complete or passing without fresh verification output.

### Single-Pass Execution Readiness

Use this checklist to complete Python work correctly in one pass whenever the request is sufficiently scoped.

1. **Restate the outcome internally**: Identify the requested behavior, target user, target surface, inputs, outputs, constraints, and non-goals.
2. **Extract acceptance criteria**: Convert the request into observable pass/fail checks before editing. Include success path, error path, edge cases, and platform expectations.
3. **Inspect before editing**: Read the existing project structure, dependency files, tests, config, entry points, and local conventions before choosing an implementation.
4. **Classify the change**: Decide whether the task is a bug fix, feature, refactor, script, library, API, CLI, worker, desktop app, or integration. Apply the matching sections of this document.
5. **Choose the smallest safe design**: Prefer the least abstraction that satisfies the acceptance criteria, preserves performance, and leaves room for obvious extension.
6. **Plan test evidence**: Identify which tests, lint checks, type checks, builds, audits, and smoke tests will prove the change.
7. **Implement in vertical slices**: Make the smallest coherent change from input to output, then expand. Avoid broad rewrites unless they are required.
8. **Handle failures deliberately**: Add explicit validation, timeouts, exception paths, cleanup, and user-facing error behavior while implementing, not afterward.
9. **Update docs/config**: Update README, examples, config templates, CLI help, API docs, migration notes, or comments when behavior or usage changes.
10. **Verify and self-review**: Run the planned checks, inspect the diff, compare against acceptance criteria, and fix gaps before reporting.

### Root Cause Analysis Before Fixing

Do not patch the first plausible cause just because it matches the symptom. For non-trivial failures, gather enough evidence to understand the deeper cause, affected layer, and blast radius before editing.

- **Separate symptom from cause**: Record the visible failure, the expected behavior, and the actual behavior before naming the cause.
- **Check neighboring evidence**: Inspect the caller, callee, test, fixture, config, dependency boundary, data model, and entry point related to the failure.
- **Generate alternatives**: Identify at least two plausible causes for non-trivial failures before choosing a fix.
- **Try to disprove the favorite**: Look for evidence that would make the leading hypothesis false.
- **Root cause vs trigger**: Distinguish a trigger such as a failing test input from the underlying design, state, dependency, or environment issue.
- **Group related failures**: When several tests fail, look for a shared cause before patching failures one by one.
- **Check recent changes**: Inspect recent diffs, dependency updates, config changes, generated files, and environment changes before editing.
- **Understand blast radius**: Identify public APIs, CLI output, config keys, data formats, migrations, and user workflows that the fix might affect.
- **Avoid confidence patches**: Do not broaden exceptions, weaken validation, change tests, add sleeps, or alter public behavior before explaining why the failure happens.
- **Verify adjacent risk**: After fixing, verify the original symptom and at least one neighboring behavior that could have regressed.

Root-cause note shape:

```md
Root cause note:
- Symptom:
- Expected:
- Actual:
- Affected layer:
- Plausible causes considered:
- Evidence for chosen cause:
- Fix strategy:
- Adjacent regression check:
```

Python-specific root-cause checks:

- Is the wrong interpreter, virtual environment, or executable path being used?
- Is `src/` layout, package metadata, current working directory, or import shadowing affecting imports?
- Is a test patching the wrong namespace or over-mocking behavior?
- Is the failure caused by type design, runtime behavior, or a bad test assumption?
- Is sync code calling async code, or async code calling blocking sync code, incorrectly?
- Is path, newline, file locking, permission, signal, or shell behavior different across operating systems?
- Is config precedence or environment-variable state producing an unexpected value?
- Did dependency version drift change an API, default, extra, or transitive behavior?
- Is mutable global/shared state leaking across tests or requests?
- Is time, randomness, network, filesystem order, or concurrency making the failure nondeterministic?

### Failure Recovery and Retry Strategy

Do not get stuck repeating the same failing methodology. A retry is valid only when the next attempt changes the hypothesis, scope, tool, input, or implementation approach.

- **Two-attempt limit**: Do not retry the same failing command, patch pattern, dependency install, test strategy, or implementation approach more than twice without changing strategy.
- **Classify the failure**: After a second failure, classify it as one or more of: environment/tooling, interpreter/virtualenv mismatch, dependency/version conflict, import path, type model, test expectation mismatch, design flaw, API misuse, async/event-loop misuse, subprocess/shell quoting, platform-specific behavior, flaky timing, insufficient requirements, or external service failure.
- **Change the hypothesis**: Before retrying, state a new hypothesis and choose a different action that can disprove it.
- **Shrink the reproduction**: Prefer the smallest failing test, import, function call, command, fixture, or script over repeated full-suite runs.
- **Isolate the layer**: Determine whether the failure is in setup, import resolution, static analysis, unit logic, integration boundary, runtime behavior, packaging, OS behavior, or CI-only behavior.
- **Verify tools before code changes**: If a tool or dependency fails, check interpreter path, virtualenv activation, package version, lockfile, config, and command syntax before editing source.
- **Inspect tests before forcing code**: If tests fail repeatedly, re-read the requirement and the test expectation. Do not contort production code around a guessed or misunderstood test.
- **Avoid weak fixes**: Do not solve repeated failure by deleting tests, weakening assertions, adding broad `except Exception`, adding sleeps, disabling lint/type rules, ignoring audit findings, or hiding errors.
- **Use different methods**: Change approach when stuck: replace broad integration debugging with a unit repro, replace mocking with a fake adapter, replace async complexity with sync isolation, replace shell glue with Python stdlib, or replace a complex abstraction with direct code.
- **Escalate when needed**: If two meaningfully different fixes fail for the same class of issue, stop and report the blocker, evidence, attempted approaches, and the decision needed from the user.
- **Protect the worktree**: Before risky recovery steps, inspect the diff and avoid overwriting unrelated user changes.
- **Keep an attempt log**: For non-trivial failures, track attempt, hypothesis, command/result, change made, and next different approach.

Attempt log shape:

```md
Attempt:
- Failure class:
- Hypothesis:
- Action/command:
- Result:
- Next different approach:
```

Common Python loop traps to check explicitly:

- `src/` layout import path mismatch.
- Running tools with the wrong interpreter or inactive virtual environment.
- Mocking the wrong namespace.
- Mypy errors caused by an unclear data model.
- Async tests using the wrong event loop pattern.
- Subprocess quoting that works on one OS but fails on another.
- Dependency resolver conflicts hidden by global packages.
- Flaky tests caused by sleeps, real clocks, network, or shared state.
- Packaging failures caused by missing `py.typed`, package include config, or wrong entry point.

### Acceptance Criteria Template

Before implementation, derive criteria in this shape. Do not necessarily write them to a file unless the project process requires it.

```md
Acceptance criteria:
- Given <initial state/input>, when <action>, then <observable result>.
- Given <invalid/edge input>, when <action>, then <safe failure/result>.
- Given <target platform/environment>, when <validation command runs>, then <expected pass condition>.
- No new unapproved dependencies, secrets, global installs, or unrelated rewrites.
```

### Existing Codebase Rules

- **Respect local patterns**: Prefer existing architecture, naming, testing style, config conventions, and dependency management when they do not conflict with this document.
- **Do not overwrite user work**: Check git status before broad edits. Never revert unrelated changes unless explicitly instructed.
- **Use narrow edits**: Touch only files required for the acceptance criteria and direct supporting tests/docs.
- **Preserve public contracts**: Do not change public APIs, CLI flags, config keys, database schema, file formats, or output formats without making compatibility and migration explicit.
- **Add seams only when useful**: Introduce adapters, protocols, or config objects only when they make the current change safer, faster to test, or clearer.
- **Delete carefully**: Remove dead code only when tests or search prove it is unused, or when the user explicitly requests cleanup.

### Definition of Done

Python work is complete only when all applicable items are true.

- Acceptance criteria are satisfied by tests, smoke checks, or explicit verification.
- Formatting, linting, type checking, tests, security audit, and build commands pass or unavailable commands are documented.
- New dependencies are approved, pinned, justified, and audited.
- Errors, logs, timeouts, cleanup, and edge cases are handled.
- Performance characteristics are appropriate for expected input size.
- Cross-platform assumptions are documented or tested.
- Public API, CLI, config, docs, and examples are updated when changed.
- The final response reports what changed, what was verified, and what could not be verified.

### Pre-Final Response Checklist

Before responding that Python work is complete, verify and report these items.

- **Scope**: The implemented behavior matches the user's latest request and no unrelated changes were made.
- **Files**: List the meaningful files changed and why.
- **Validation**: Include exact validation commands run and whether each passed, failed, or was unavailable.
- **Tests**: Note new or changed tests and what behavior they prove.
- **Risks**: State residual risks, skipped checks, platform assumptions, or follow-up work.
- **Dependencies**: State any dependency additions, removals, or version changes.
- **Security**: Confirm secrets, credentials, destructive operations, and external calls were handled safely.
- **Performance**: Mention complexity or benchmark evidence for hot paths.
- **User work**: Confirm unrelated dirty worktree changes were not reverted or overwritten.

## Decision Tree for Code Generation

1. **Can the stdlib do it?** Use stdlib (see Standard Library Preferences table).
2. **Is the library already prescribed in this document?** (e.g., `pytest`, `pydantic`, `requests`, `httpx`, `tenacity`, `ruff`, `mypy`, `hatchling`) Use it as specified.
3. **Is there an existing dependency in requirements.txt?** Use that.
4. **Is the library listed in Common Libraries?** Ask before using.
5. **Is it a new dependency?** Document the rationale and get approval.
6. **Sync or async?** Default sync. Use async only when ≥3 concurrent I/O calls justify it (see Concurrency section).
7. **Is there ambiguity?** Ask. Never guess.
