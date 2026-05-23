# TYPESCRIPT.md

This document constrains all TypeScript and JavaScript code generation for any
project that references it. Read it before writing or editing TypeScript,
JavaScript, JSX, or TSX code. The goal is production-quality TypeScript that is
correct, typed, tested, secure, maintainable, efficient, portable, and explicit
about runtime behavior across Node.js, browsers, servers, workers, desktop apps,
and mobile-adjacent systems.

For cross-language decisions, read `language-guidelines.md` first. TypeScript is
preferred for new JavaScript-family product code, but operational scripts still
default to Python unless this repository already standardizes on Node-based
automation.

## Runtime

- **Language target**: Write TypeScript, not plain JavaScript, for new code unless
  the user explicitly requests JavaScript or the project is already JavaScript-only.
- **Node.js target**: Target Node.js Active LTS `24.16.0` or the current active
  LTS patch for server-side, CLI, test, build, and tooling code. Do not target
  unsupported Node versions.
- **Current vs LTS**: Do not target a newly released Current Node major for
  production by default. Use Current only for experiments, tooling that requires
  it, or when the user explicitly accepts the upgrade risk.
- **Node-first default**: Use Node.js for TypeScript servers, CLIs, packages, and
  build tooling unless the project already targets Bun, Deno, edge workers, or a
  browser-only runtime.
- **Browser target**: Use the project's declared browser support matrix. If none
  exists, support the latest stable Chrome, Edge, Firefox, and Safari releases.
- **Module system**: Prefer ESM (`"type": "module"`) for new projects. Preserve
  CommonJS only when the existing project, runtime, or dependency graph requires
  it.
- **Transpilation goal**: Emit modern JavaScript for the actual runtime. Do not
  downlevel more than needed; unnecessary transforms increase bundle size and
  hide runtime behavior.
- **Runtime verification**: Before running project commands, verify the runtime:
  ```console
  node --version
  npm --version
  ```
- **Version pinning**: New projects should include an `engines.node` range in
  `package.json` and, when using pnpm or Yarn, a `packageManager` field. Keep
  local, CI, and production Node versions aligned.
- **npm baseline**: Use npm `11.13.0` with Node.js `24.16.0` unless the project
  lockfile or deployment platform requires another package manager.
- **Corepack**: If the project uses pnpm or Yarn through Corepack, use the
  repository's configured `packageManager` value. Do not silently upgrade the
  package manager.
- **Preferred execution**: Use package scripts (`npm run ...`, `pnpm ...`,
  `yarn ...`) rather than invoking local binaries directly. Use `npx` only for
  one-off tools when the project has no local dependency and the command is safe.
- **No global installs**: Never install packages globally. If a global tool appears
  necessary, ask the user.

| Surface | Default runtime stance |
|---|---|
| Backend services | Node.js active LTS, ESM, strict TypeScript |
| CLIs and scripts | Node.js active LTS, ESM, strict TypeScript |
| Browser apps | TypeScript compiled by the existing bundler/framework |
| Shared packages | ESM-first with explicit exports; add CJS only when needed |
| Serverless/edge | Follow the platform runtime exactly; avoid Node-only APIs on edge |
| Tests/tooling | Same Node major as production unless the tool requires newer |

### Bun and Deno

- **Do not switch runtimes casually**: Bun and Deno change package resolution,
  permissions, APIs, lockfiles, test runners, bundling, and deployment behavior.
  Use them only when the project already does or the user explicitly chooses
  them.
- **Bun**: If a project uses Bun, use `bun.lock`, `bun install --frozen-lockfile`
  in CI, and Bun-native scripts only where compatibility has been verified.
- **Deno**: If a project uses Deno, respect `deno.json`, import maps, permissions,
  and remote module integrity. Do not assume npm-style `node_modules`.
- **Runtime APIs**: Keep Node-specific `node:*` imports out of Bun/Deno/browser
  code unless compatibility is documented and tested.
- **Testing**: Use the runtime's native test command only when the project already
  standardizes on it; otherwise preserve the existing test runner.

## Project Discovery

Before writing TypeScript in an existing project, inspect local conventions:

- `package.json`
- lockfile: `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, or `bun.lock`
- `tsconfig.json` and any extended configs
- framework config: `vite.config.*`, `next.config.*`, `astro.config.*`,
  `remix.config.*`, `svelte.config.*`, `eslint.config.*`, etc.
- test config: `vitest.config.*`, `jest.config.*`, `playwright.config.*`,
  `cypress.config.*`
- source layout and naming conventions

Use the existing package manager, framework, import style, test runner, and
folder structure unless the user approves a migration.

## Package and Environment Management

- **Package manager**: Use the package manager implied by the existing lockfile.
  For new projects, prefer `npm` unless the user chooses `pnpm`, Yarn, or Bun.
- **Lockfiles are required**: Commit exactly one lockfile. Do not mix lockfiles.
- **Workspace detection**: If the repository has npm, pnpm, Yarn, Nx, Turborepo,
  Rush, Lage, or similar workspaces, run commands from the workspace root unless
  the project documents package-local commands.
- **Workspace scope**: In monorepos, change only the package(s) required for the
  task. Update root config only when the rule or dependency is truly shared.
- **Install command**:
  - npm: `npm ci` for clean installs, `npm install` when intentionally changing
    dependencies.
  - pnpm: `pnpm install --frozen-lockfile` in CI, `pnpm install` when changing
    dependencies.
  - Yarn: `yarn install --immutable` for modern Yarn, otherwise use the
    repository's documented command.
- **Exact dependency versions**: Prefer exact dependency versions. For npm, set
  `save-exact=true` in project `.npmrc` for new projects.
- **No unreviewed dependency additions**: Adding any third-party runtime
  dependency requires a short rationale. Prefer platform APIs and existing
  dependencies.
- **Dev dependency baseline**: For new general TypeScript projects, include:
  `typescript`, `tsx`, `eslint`, `typescript-eslint`, `prettier`, `vitest`, and
  `@types/node` when Node APIs are used. Pin exact versions through the lockfile.
- **Baseline versions**: For new npm projects, start with `typescript@6.0.3`,
  `tsx@4.22.3`, `eslint@10.4.0`, `typescript-eslint@8.59.4`,
  `prettier@3.8.3`, `vitest@4.1.7`, and `@types/node@24.12.4` when targeting
  Node.js `24.x`. Re-check the registry before starting a new project.
- **Node type versions**: Match `@types/node` to the target Node major. Do not use
  the global latest `@types/node` package when it describes a newer Current Node
  major than production.
- **Version refresh gate**: Before scaffolding a new project, verify the current
  package versions and current Active LTS Node major. If they differ from this
  dated baseline, use the newer verified baseline and update this document.
- **Environment variables**: Read from `process.env` only at boundary modules,
  validate once, and pass typed config inward. Never scatter raw env access
  through business logic.
- **`.env` files**: Use `.env` for local secrets, add it to `.gitignore`, and
  commit `.env.example` with placeholder keys only.
- **No secret values in source**: Never commit API keys, OAuth client secrets,
  database URLs, tokens, cookies, private keys, or service account JSON.
- **Local caches**: Do not commit `.turbo`, `.next`, `.vite`, `.cache`,
  `coverage`, `dist`, `build`, or generated dependency folders unless the
  project explicitly tracks a build artifact.

### Supply Chain Controls

- **Separate runtime and dev dependencies**: Put build, lint, test, and type tools
  in `devDependencies`. Put only production runtime imports in `dependencies`.
- **Audit intentionally**: Run the package manager audit command before shipping
  production services, CLIs, or deployment artifacts. Fix vulnerable packages or
  document a temporary exception with advisory, path, risk, and mitigation.
- **Dependency confusion**: Verify package names before adding dependencies. Be
  especially careful with internal package names and similarly named public
  packages.
- **Install scripts**: Treat dependency lifecycle scripts as a supply-chain risk.
  Do not add packages with suspicious install/postinstall behavior without
  review.
- **License awareness**: Check dependency licenses before adding packages. Ask the
  user when a license is unclear, copyleft, source-available, or commercial.
- **Vendoring**: Do not vendor third-party code unless explicitly approved. Keep
  license and source provenance for vendored code.
- **Upgrade discipline**: Upgrade dependencies in focused changes. Run type
  checks, lint, tests, builds, and smoke tests after every upgrade.
- **No private registry secrets in repo**: Keep auth tokens out of `.npmrc`.
  Commit registry URLs only when they are non-secret and intentional.
- **Provenance for packages**: For publishable packages, prefer provenance or
  signed publishing when the registry and CI support it.
- **Package publish allowlist**: Use `"files"` in `package.json` or an equivalent
  publish allowlist. Never publish tests, local env files, raw source maps,
  private config, fixtures with secrets, or internal scripts by accident.
- **Dependency footprint**: Before adding a dependency, check install size,
  transitive count, maintenance status, ESM/CJS compatibility, Node/browser
  compatibility, types quality, and whether it runs install scripts.

## TypeScript Compiler Configuration

Use the strictest settings the project can support. For new projects, start with
this baseline and relax only with a documented reason:

```json
{
  "compilerOptions": {
    "target": "ES2024",
    "lib": ["ES2024"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "allowUnreachableCode": false,
    "allowUnusedLabels": false,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "skipLibCheck": false
  }
}
```

- **Applications** may set `declaration: false` when they do not publish a public
  package API.
- **Source maps**: Generate source maps for debugging when needed, but do not
  publish private production source maps publicly. Upload them only to controlled
  error-reporting systems when access is restricted.
- **Isolated declarations**: For published libraries with large public surfaces,
  consider `isolatedDeclarations` once the codebase has explicit exported return
  types and declaration emit performance matters.
- **Browser apps** must include the correct browser libs, usually
  `["ES2024", "DOM", "DOM.Iterable"]`.
- **Bundler projects** may use `"moduleResolution": "Bundler"` when the framework
  expects it. Do not mix NodeNext assumptions into bundler-only code.
- **`skipLibCheck`**: Keep `false` for packages and libraries. For large apps with
  dependency type conflicts, `true` is acceptable only as a temporary workaround
  with an issue or note.
- **Unused code checks**: For libraries and packages, keep `noUnusedLocals` and
  `noUnusedParameters` enabled unless ESLint enforces equivalent rules. For apps,
  enforce unused code through either TypeScript or ESLint.
- **`any` prohibition**: Do not use `any`. Use `unknown`, generics, discriminated
  unions, branded types, or narrow interfaces. If `any` is unavoidable for a
  third-party boundary, isolate it in one adapter and explain why.
- **`@ts-ignore` prohibition**: Do not use `@ts-ignore`. Use `@ts-expect-error`
  only with a short reason and only when the line is intentionally invalid or a
  dependency type is wrong.

### ESLint Baseline

Use the existing ESLint setup when present. For new projects, configure ESLint
with TypeScript-aware rules and fail CI on warnings unless the project has an
explicit warning budget.

- Enable recommended `typescript-eslint` type-checked rules when performance is
  acceptable.
- Enforce no floating promises, no misused promises, no unsafe assignment/member
  access/calls/returns, no unnecessary type assertions, no implicit `any`, and no
  unused disable comments.
- Enforce import consistency, including `import type` for type-only imports.
- Disallow `console` in libraries and production frontend code except approved
  boundary logging.
- Keep per-file rule disables narrow, line-specific, and justified.
- Do not disable a strict rule globally to make one file pass.

**`eslint.config.mjs` baseline**

Use this only for new projects without a stronger local config. It follows
typescript-eslint's current flat-config pattern with typed linting and
`projectService: true`.

```js
import js from "@eslint/js";
import { defineConfig } from "eslint/config";
import tseslint from "typescript-eslint";

export default defineConfig(
  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
      },
    },
    rules: {
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { fixStyle: "inline-type-imports" },
      ],
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/no-unnecessary-type-assertion": "error",
      "@typescript-eslint/no-unsafe-assignment": "error",
      "@typescript-eslint/no-unsafe-call": "error",
      "@typescript-eslint/no-unsafe-member-access": "error",
      "@typescript-eslint/no-unsafe-return": "error",
      "no-console": ["error", { allow: ["warn", "error"] }],
    },
  },
  {
    files: ["**/*.js", "**/*.mjs", "**/*.cjs"],
    extends: [tseslint.configs.disableTypeChecked],
  },
);
```

## Application Surfaces

### Backend APIs and Web Services

- **Framework approval**: Do not introduce Express, Fastify, Hono, NestJS, Next.js
  API routes, tRPC, GraphQL servers, or similar frameworks without user approval.
- **Boundary validation**: Validate path params, query params, headers, cookies,
  request bodies, uploads, and webhook signatures at the boundary.
- **Schema libraries**: Prefer the project's existing validation library. For new
  TypeScript services, `zod` is acceptable with approval; otherwise use explicit
  validators or platform/framework validation.
- **Auth checks**: Keep authentication and authorization explicit at entry points
  and resource boundaries. Never trust client-provided user ids, roles, tenant
  ids, or permissions.
- **Timeouts and limits**: Enforce request body limits, upload limits, outbound
  HTTP timeouts, database timeouts, queue timeouts, and worker timeouts.
- **Errors**: Return structured, sanitized errors. Never expose stack traces,
  SQL, secrets, filesystem paths, internal hostnames, or dependency internals.
- **Pagination**: Paginate list endpoints. Never return unbounded result sets.
- **CORS and cookies**: Configure allowed origins, credentials, `SameSite`,
  `Secure`, `HttpOnly`, CSRF protection, and session lifetime deliberately.
- **Rate limiting**: Add abuse controls for public endpoints, login flows,
  expensive reads, mutations, uploads, and webhook receivers.
- **Idempotency**: Mutating endpoints that may be retried need idempotency keys or
  equivalent duplicate protection.
- **Streaming**: Use streaming for large downloads/uploads. Do not buffer large
  payloads in memory unless bounded and documented.
- **Database access**: Use parameterized queries, prepared statements, or the
  project's ORM/query builder safely. Keep transactions short, explicit, and
  tested for rollback behavior.
- **Migrations**: Treat schema migrations as production code. Include forward
  migration, rollback or recovery notes, backfill strategy, and compatibility
  with old and new application versions when deploys are rolling.
- **Multi-tenancy**: Enforce tenant scoping in the data access layer and at
  authorization boundaries. Never rely on client-provided tenant ids alone.

### Database and ORM Standards

- **ORM approval**: Do not introduce Prisma, Drizzle, TypeORM, Sequelize, Kysely,
  Knex, or database SDKs without user approval. Use the existing persistence
  pattern.
- **Query shape**: Select only fields needed by the caller. Avoid unbounded
  relation loading, accidental N+1 queries, and large JSON columns in list views.
- **Transactions**: Keep transactions short and explicit. Include timeout,
  isolation, retry, and rollback behavior when the database or ORM exposes it.
- **Generated clients**: Treat generated ORM clients and database types as
  boundary types. Map them to domain models when invariants, nullability, or
  authorization rules need stronger guarantees.
- **Migrations**: Never combine risky schema migration, data backfill, and
  application behavior changes without a staged rollout plan.
- **Indexes**: For new query paths, consider indexes, uniqueness constraints, and
  foreign keys as part of the feature, not as later cleanup.
- **Raw SQL**: Keep raw SQL parameterized, reviewed, and covered by tests for
  empty input, special characters, permissions, and transaction behavior.

### Frontend Apps

- **Framework approval**: Do not introduce React, Next.js, Vue, Svelte, Astro,
  Angular, Solid, Remix, Vite, Tailwind, or component libraries without user
  approval. Follow the existing framework.
- **State locality**: Keep state as local as possible. Add global state only when
  multiple distant parts of the app genuinely need shared state.
- **Rendering discipline**: Avoid unnecessary re-renders, unstable object/function
  props, expensive work during render, and layout thrashing.
- **Data fetching**: Centralize API calls behind typed clients or hooks. Validate
  untrusted API responses before treating them as domain data.
- **Accessibility**: Use semantic HTML first. Preserve labels, roles, keyboard
  navigation, focus states, reduced-motion behavior, and contrast.
- **Forms**: Validate on the client for usability and on the server for security.
  Never trust client validation.
- **Security**: Never inject unsanitized HTML. Avoid `dangerouslySetInnerHTML`;
  when required, sanitize with an approved sanitizer and document the source.
- **Secrets**: Treat all frontend code as public. Never put server secrets in
  browser bundles or public runtime config.
- **Browser storage**: Treat `localStorage`, `sessionStorage`, IndexedDB,
  cookies readable by JavaScript, and URL fragments as attacker-readable. Do not
  store long-lived secrets there.
- **Auth tokens**: Prefer secure, `HttpOnly`, `SameSite` cookies for browser
  sessions when the architecture supports them. If bearer tokens are required in
  the browser, keep lifetime short and document the tradeoff.
- **Content Security Policy**: For production apps, use a CSP appropriate to the
  framework and hosting model. Avoid `unsafe-inline` and broad third-party
  script allowances unless there is a documented exception.
- **Performance budgets**: Keep bundle size, image size, render work, and network
  waterfalls visible. Lazy-load heavy routes and components when it improves real
  user experience.
- **SSR and hydration**: For SSR, SSG, RSC, or islands architectures, keep server
  and client boundaries explicit. Do not read browser globals during server
  render, do not depend on nondeterministic render output, and test hydration
  paths for mismatches.
- **React Server Components**: In React/Next-style RSC projects, keep server-only
  code out of client components, avoid passing non-serializable props across the
  server/client boundary, and protect server actions as mutation endpoints.

### Framework-Specific Docs Rule

When code generation depends on a framework, SDK, CLI, or cloud service, fetch
current official documentation before writing version-specific guidance or code.
Framework behavior changes too quickly for memory to be the source of truth.

- **React and Next.js**: Verify current docs for routing, server/client
  boundaries, server actions, caching, metadata, image optimization, and config.
- **Express, Fastify, Hono, and NestJS**: Verify current docs for middleware
  order, body parsing, error handling, route typing, plugins, and adapter APIs.
- **Prisma, Drizzle, TypeORM, and database SDKs**: Verify current docs for client
  generation, migrations, transactions, relation loading, and raw SQL APIs.
- **Playwright, Cypress, and test tools**: Verify current docs for locators,
  assertions, browser projects, traces, retries, and fixtures.
- **Vite, Astro, Remix, SvelteKit, Vue, Angular, Tailwind, and bundlers**: Verify
  current docs for TypeScript integration, SSR behavior, environment variables,
  plugin APIs, and production builds.

### Framework Mini-Standards

These are global guardrails, not replacements for current framework docs.

- **React**: Keep components pure, avoid side effects during render, use effects
  only for synchronization with external systems, keep derived state derived, and
  memoize only when it prevents measured churn or unstable identities at real
  boundaries.
- **Next.js**: Keep server/client boundaries explicit. Treat route handlers and
  server actions as backend endpoints with validation, authorization, rate limits,
  and safe errors. Be deliberate about caching, revalidation, dynamic rendering,
  and environment variable exposure.
- **Express/Fastify/Hono**: Centralize error handling, validate all inputs before
  handlers reach business logic, keep middleware order obvious, enforce request
  limits before parsing expensive bodies, and type route context explicitly.
- **NestJS**: Avoid decorator magic leaking into domain logic. Keep providers
  small, validate DTOs at boundaries, test guards/interceptors/pipes separately,
  and keep business rules independent of framework decorators when practical.
- **tRPC/GraphQL**: Treat resolvers/procedures as API boundaries. Validate input,
  enforce auth per procedure/field as appropriate, avoid over-fetching, and keep
  schema changes backward-compatible for existing clients.
- **Prisma/Drizzle/TypeORM**: Keep generated client usage behind persistence
  modules for non-trivial domains, avoid leaking database nullability into public
  APIs, and test transaction and relation-loading behavior.
- **Vite/Astro/Remix/SvelteKit/Vue/Angular**: Follow the framework's file-system
  routing, SSR, environment, and build conventions. Do not import server-only code
  into browser bundles.
- **Tailwind and CSS tooling**: Preserve the local design system. Avoid
  one-off arbitrary values when a token or component pattern exists, and verify
  production class extraction when generating dynamic class names.
- **Playwright**: Use test isolation, role-first locators, web-first assertions,
  multiple browser projects when cross-browser risk exists, and traces/screenshots
  for debugging rather than sleeps.

### CLIs and Developer Tools

- **Default fit**: TypeScript is appropriate for CLIs, build tools, repo scripts,
  generators, API clients, and automation.
- **Output channels**: Write machine-readable results to stdout and diagnostics to
  stderr.
- **Exit codes**: Return `0` on success and non-zero on failure. Keep documented
  exit codes stable.
- **Help and version**: Provide `--help` and `--version` for reusable tools.
- **Dry run**: Include `--dry-run` for destructive, bulk, remote, or irreversible
  operations.
- **Non-interactive mode**: Do not require prompts for automation. Provide flags,
  env vars, and config files for unattended use.
- **Shell compatibility**: Do not assume Bash, PowerShell, zsh, fish, GNU tools,
  ANSI color, or TTY availability unless detected or documented.
- **Argument parsing**: Use the project's existing parser. For new small CLIs,
  parse arguments directly or use `node:util.parseArgs`; ask before adding a CLI
  framework.

### Background Services and Workers

- **Lifecycle**: Implement startup, readiness, graceful shutdown, and cleanup.
- **Shutdown signals**: Handle `SIGTERM` and `SIGINT` for Node services. Stop
  accepting work, finish or requeue in-flight jobs, close clients, and exit.
- **Idempotency**: Retried jobs that mutate external systems must be idempotent or
  guarded by idempotency keys.
- **Retries**: Use bounded retries with exponential backoff and jitter. Never
  retry indefinitely.
- **Queues**: Bound queue sizes and concurrency. Apply backpressure instead of
  unbounded memory growth.
- **Poison messages**: Move repeatedly failing work to a dead-letter queue or
  documented failure store when available.
- **Observability**: Log job id, attempt, elapsed time, outcome, retry delay, and
  sanitized failure reason.
- **Concurrency control**: Use explicit concurrency limits. Do not create one
  promise per unbounded input item.

### Serverless and Edge

- **Runtime differences**: Edge runtimes may not support `node:*` modules,
  sockets, filesystem access, native dependencies, or long-lived background work.
- **Cold starts**: Keep imports lean. Avoid heavy top-level initialization.
- **Global state**: Cache immutable clients carefully when the platform supports
  it, but do not rely on process lifetime for correctness.
- **Timeouts**: Respect platform request and execution limits.
- **Streams and Web APIs**: Prefer standard Web APIs on edge runtimes.
- **Secrets**: Read secrets from platform-managed environment bindings, not source
  files or public runtime config.

### Desktop and Mobile-Adjacent Apps

- **Framework approval**: Ask before adding Electron, Tauri, React Native, Expo,
  Ionic, Capacitor, NativeScript, or similar app frameworks.
- **Runtime boundary**: Do not assume browser APIs exist in Node contexts or Node
  APIs exist in browser/native contexts.
- **IPC security**: In Electron/Tauri-style apps, keep privileged APIs behind a
  narrow validated bridge. Never expose raw filesystem, shell, or network power
  to untrusted renderer code.
- **Offline behavior**: Mobile-facing APIs and clients must handle slow networks,
  duplicate requests, retries, and offline/online transitions.
- **Secrets**: Never put server secrets in desktop or mobile clients. Assume
  distributed clients can be inspected and modified.

### Libraries and Published Packages

- **Public entrypoints**: Define `exports` explicitly in `package.json`. Avoid
  exposing internal files by directory structure accident.
- **Type declarations**: Publish `.d.ts` files and validate that consumers can
  import them from the package entrypoints.
- **Dual package hazard**: Avoid publishing separate ESM and CJS builds unless the
  project needs both. If dual builds are required, test both import styles and
  ensure singleton state is not duplicated.
- **Semver**: Treat type changes as API changes. A stricter exported type can be a
  breaking change for consumers.
- **Tree shaking**: Keep modules side-effect-free by default and set
  `"sideEffects"` accurately. Do not mark side effects false if CSS imports,
  polyfills, or registration code must run.
- **Package contents**: Verify packed contents with `npm pack --dry-run` or the
  package manager equivalent before publishing.

### JavaScript Interop and Migration

- **Prefer conversion over expansion**: When touching JavaScript files in a
  TypeScript project, prefer converting the touched module to TypeScript if the
  scope is contained and tests can verify behavior.
- **`allowJs`**: Use `allowJs` only as a migration bridge. Do not use it as a
  long-term substitute for typing source code.
- **`checkJs`**: Enable `checkJs` for JavaScript that remains in a TypeScript
  project when the warning volume is manageable.
- **JSDoc types**: Use JSDoc for legacy JavaScript only when conversion is not
  practical. Do not build new public APIs in JavaScript with JSDoc when
  TypeScript is available.
- **Interop wrappers**: Isolate untyped CommonJS or legacy packages behind a typed
  adapter rather than spreading unsafe imports through the codebase.

## Cross-Platform Portability

Generated code must run predictably on Windows, macOS, Ubuntu, and Fedora unless
the project explicitly narrows the target.

- **Filesystem case**: Treat paths as case-sensitive. Never rely on
  `Config.ts` and `config.ts` being the same file.
- **Path separators**: Use `node:path` APIs. Never concatenate paths with `/` or
  `\\` in Node code.
- **URLs vs paths**: Use `URL` for URLs and `path`/`fs` for filesystem paths. Do
  not parse URLs with string splitting.
- **Line endings**: Read text with universal handling where possible and write
  normal text files with `\n` unless a format requires otherwise.
- **Encoding**: Use UTF-8 for source, config, data files, subprocess text I/O,
  and logs. Never rely on locale defaults.
- **Locale**: Do not parse dates, numbers, or booleans using ambient locale. Use
  explicit formats and validators.
- **Time zones**: Store and compare timestamps as UTC. Convert to local time only
  at presentation boundaries.
- **Temporary paths**: Use `node:os.tmpdir()` with unique names or
  `fs.mkdtemp`. Never hardcode `/tmp`, `%TEMP%`, or user profile paths.
- **Executable lookup**: Use package scripts or explicit tool paths. If invoking
  external commands, detect missing executables and fail clearly.
- **Shells**: Do not assume Bash syntax works on Windows or PowerShell syntax
  works on Unix. Prefer Node implementations over shell glue.
- **File locks and deletes**: Windows may keep files locked longer than POSIX
  systems. Close handles promptly and avoid assuming immediate delete/rename.
- **Permissions**: POSIX mode bits and Windows ACLs differ. Do not build security
  controls that depend on one model without platform-specific branches.
- **Signals**: Do not assume all POSIX signals exist on Windows. Use timeouts and
  explicit child-process cleanup.
- **Path length**: Keep generated paths short enough for Windows tooling.

## Public API Design

Design public TypeScript APIs for clarity, stability, and low overhead.

- **Small surface area**: Export only the names consumers need. Keep
  implementation details unexported.
- **Explicit exports**: Use named exports. Avoid default exports for reusable
  libraries unless the ecosystem convention strongly expects one.
- **Stable contracts**: Treat function signatures, return types, thrown errors,
  config keys, CLI args, events, and JSON shapes as compatibility contracts.
- **No import side effects**: Importing a module must not perform network calls,
  parse large files, mutate global state, configure logging, start timers, or
  launch background work.
- **Options objects**: Use an options object for functions with more than two
  parameters or any optional behavior.
- **No boolean traps**: Avoid multiple boolean parameters. Use discriminated
  unions, string literal unions, enums only when needed, or small config objects.
- **Readonly input**: Accept `readonly` arrays and readonly object shapes when the
  function does not mutate input.
- **Immutability**: Prefer immutable return values for public value objects.
- **Deprecation path**: Do not remove or rename public API without a migration note
  and deprecation period unless the user requests a breaking change.
- **Type-level API**: Export helper types only when consumers need them. Do not
  leak internal conditional types, schema implementation types, or generated
  vendor types into public signatures unnecessarily.
- **Async contracts**: Public async functions must document cancellation,
  timeout, retry, and idempotency expectations when they touch external systems.
- **Error model**: Throw documented project-specific errors at boundaries. Preserve
  original causes with `cause`.

```ts
export class AppError extends Error {
  constructor(message: string, options?: { cause?: unknown }) {
    super(message, options);
    this.name = "AppError";
  }
}
```

## Code Style

- **Formatter**: Prettier for formatting. Do not hand-format around Prettier.
- **Linter**: ESLint with `typescript-eslint` for TypeScript-aware rules.
- **Type checker**: `tsc --noEmit` for apps; `tsc --noEmit` plus declaration
  emit checks for packages.
- **Formatter ownership**: Use Prettier for formatting and ESLint for code
  correctness. Do not enable conflicting stylistic ESLint rules unless the
  project already owns that convention.
- **Indentation**: 2 spaces, no tabs.
- **Semicolons**: Use semicolons.
- **Quotes**: Double quotes for strings unless the project already uses single
  quotes.
- **Trailing commas**: Use where Prettier emits them.
- **Line length**: Let Prettier wrap. Avoid dense clever expressions.
- **Imports**: Keep imports sorted by the project's tooling. Prefer static imports
  at the top of files; use dynamic import only for real lazy loading or optional
  dependencies.
- **File length**: Split files over about 400 lines, files with unrelated
  responsibilities, or files requiring unrelated test fixtures.
- **Comments**: Add comments only for non-obvious behavior, invariants, security
  constraints, performance tradeoffs, or external protocol quirks.

### Naming

| Element | Convention | Example |
|---|---|---|
| Packages | lowercase kebab-case | `billing-core` |
| Source files | kebab-case or project convention | `load-config.ts` |
| React components | PascalCase file and export | `UserMenu.tsx` |
| Functions | camelCase verb phrase | `loadConfig()` |
| Variables | camelCase noun phrase | `userCount` |
| Constants | UPPER_SNAKE_CASE for true constants | `MAX_RETRIES` |
| Classes | PascalCase | `class DataLoader` |
| Error classes | PascalCase ending in `Error` | `ConfigError` |
| Types/interfaces | PascalCase | `UserProfile` |
| Generic params | short PascalCase | `T`, `TValue`, `TError` |
| Booleans | `is`, `has`, `can`, `should`, `needs` | `isActive` |
| Arrays/collections | plural nouns | `users` |
| Maps | key/value role | `userById` |
| Callbacks | verb or `onEvent` | `onComplete` |
| CLI commands | lowercase kebab-case | `sync-users` |
| CLI options | lowercase kebab-case | `--dry-run` |
| Env vars | uppercase with project prefix | `APP_DATABASE_URL` |
| Config keys | camelCase or project convention | `retryCount` |

- **Avoid vague names**: Do not use `data`, `obj`, `item`, `manager`, `handler`,
  `processor`, `temp`, or `result` unless the scope is tiny and obvious.
- **Acronyms**: Treat acronyms as words: `httpClient`, `userId`, `apiKey`.
  Avoid `HTTPClient` unless matching an external API.
- **Units and domains**: Include units when ambiguity is possible:
  `timeoutMs`, `sizeBytes`, `createdAtUtc`.
- **Throwaway names**: Use `_` only for intentionally unused values.

### Imports and Modules

- Use explicit file extensions in ESM imports when the runtime requires them.
- In NodeNext ESM TypeScript, local relative imports that emit to JavaScript
  should usually use `.js` extensions in source (`./module.js`), not `.ts`.
- Avoid path aliases unless already configured. If aliases are used, keep
  TypeScript, bundler, test runner, and runtime resolution aligned.
- No wildcard namespace imports unless the library convention expects it.
- No circular imports. Move shared types or constants into a small boundary module
  when needed.
- Use `import type` for type-only imports when `verbatimModuleSyntax` is enabled.
- Do not mix CommonJS `require` with ESM imports unless bridging legacy code.
- Keep `index.ts` barrels small. Avoid broad barrels that create cycles, slow
  builds, or hide ownership.

## Type System Rules

- **No `any`**: Use `unknown`, generics, narrow interfaces, discriminated unions,
  or runtime validation.
- **No unsafe assertions**: Avoid `as SomeType`. Prefer narrowing. If an assertion
  is required, isolate it near a validated boundary and explain why.
- **No non-null assertion**: Avoid `value!`. Prove presence with control flow or
  throw a clear error.
- **Prefer `unknown` in catches**: Narrow errors before reading properties.
- **Prefer type aliases for unions** and object shapes that compose; interfaces
  are acceptable for public extension points and class contracts.
- **Discriminated unions**: Use tagged unions for state machines, API variants,
  and mutually exclusive shapes.
- **Exhaustiveness**: Use a `never` check for switches over unions.

```ts
type JobState =
  | { kind: "queued"; queuedAt: string }
  | { kind: "running"; startedAt: string }
  | { kind: "failed"; reason: string }
  | { kind: "completed"; completedAt: string };

function describeState(state: JobState): string {
  switch (state.kind) {
    case "queued":
      return `queued at ${state.queuedAt}`;
    case "running":
      return `started at ${state.startedAt}`;
    case "failed":
      return `failed: ${state.reason}`;
    case "completed":
      return `completed at ${state.completedAt}`;
    default: {
      const exhaustive: never = state;
      return exhaustive;
    }
  }
}
```

- **Branded types**: Use brands for ids from different domains when plain strings
  could be mixed accidentally.

```ts
type Brand<T, Name extends string> = T & { readonly __brand: Name };
type UserId = Brand<string, "UserId">;
type AccountId = Brand<string, "AccountId">;
```

- **Readonly by default**: Use `readonly T[]`, `ReadonlyArray<T>`, and readonly
  object properties for values that should not be mutated.
- **Optionality**: Use `undefined` for absent optional fields and `null` only when
  an external API or storage format distinguishes it.
- **Indexing**: With `noUncheckedIndexedAccess`, handle possibly missing values
  from arrays, maps, and records.
- **Records**: Use `Record<K, V>` only when every key in `K` exists. Use
  `Partial<Record<K, V>>` or `Map<K, V>` for sparse maps.
- **Enums**: Prefer string literal unions. Use `enum` only when interoperating
  with existing APIs or when runtime enum objects are genuinely useful.
- **Const assertions**: Use `as const` for literal tables, not as a substitute for
  validation.
- **Generic constraints**: Constrain generics to the behavior used. Do not create
  unconstrained abstractions.

### Type-Level Performance

TypeScript type computation can become a real build bottleneck. Keep type-level
programming boring unless a public API genuinely benefits from it.

- Prefer named object types, interfaces, and simple unions over deeply nested
  conditional, mapped, and template-literal types.
- Avoid large generated unions in hand-authored code. If generated unions are
  necessary, isolate them and avoid re-exporting them through many modules.
- Avoid recursive conditional types unless the input size is tightly bounded and
  compile time has been measured.
- Prefer explicit return type annotations on exported functions and complex
  callbacks. This reduces declaration emit cost and stabilizes public API shape.
- Split very large projects with project references and `composite` builds when
  one `tsconfig` becomes slow or hard to cache.
- Use `incremental` for local builds when the project benefits from `.tsbuildinfo`
  caching. Keep build-info files out of source control unless the project has a
  specific reason to track them.
- Keep `declaration` emit limited to packages that publish types. App-only code
  should not pay declaration emit cost unless another tool requires it.
- Run `tsc --extendedDiagnostics` or project build profiling before doing
  non-obvious type-system refactors for performance.
- For deep compiler performance investigations, use TypeScript trace generation
  on a clean non-incremental build and keep trace output out of source control.

## Runtime Validation and Data Modeling

TypeScript types disappear at runtime. Validate all untrusted data.

- **Validate at boundaries**: Network responses, request bodies, query params,
  route params, local storage, cookies, files, CLI args, env vars, message queue
  payloads, and database JSON blobs are untrusted.
- **Schema source**: Prefer one schema per boundary and derive types from the
  schema when using a validation library.
- **No blind casts**: Never write `const user = json as User` for untrusted JSON.
- **Internal models**: After validation, pass typed domain objects inward rather
  than raw JSON or `Record<string, unknown>`.
- **Explicit optionality**: Missing, empty, and null values must have distinct
  handling when the domain distinguishes them.
- **Money and decimals**: Do not use floating-point numbers for currency or exact
  decimal quantities. Use integer minor units or an approved decimal library.
- **Dates**: Store timestamps as ISO 8601 UTC strings or validated epoch
  milliseconds. Convert to `Date` only when needed and validate invalid dates.
- **Schema evolution**: Persisted and external data must tolerate added fields,
  missing legacy fields, and version migration.
- **Serialization boundary**: Keep serialization/deserialization near I/O edges.
- **Database rows**: Treat database results as untrusted until mapped to typed
  domain objects. Do not let nullable or optional database columns leak deep into
  business logic without normalization.
- **Generated types**: Generated API, GraphQL, Prisma, OpenAPI, or database types
  are boundary types. Wrap or map them when domain invariants are stronger than
  the generated shape.

## Error Handling

- **Never throw strings**: Throw `Error` or project-specific subclasses.
- **Project error base**: Use a shared base error for expected application errors.
- **Preserve causes**: Use `new Error(message, { cause })` when wrapping failures.
- **Catch narrowly**: Catch errors only where you can add context, recover, retry,
  translate to a boundary response, or clean up.
- **Unknown catches**: Treat caught values as `unknown` and narrow them.
- **No swallowed failures**: Never use empty `catch` blocks. Log, rethrow, return
  a typed failure, or intentionally ignore with a comment explaining why.
- **Boundary translation**: Translate internal errors to safe CLI/HTTP/UI messages
  at the boundary. Do not leak internals.
- **Finally for cleanup**: Use `finally` for resource cleanup when a dedicated
  API such as `using`/disposal is not available or not supported by the project.

### Error Messages

User-facing errors are product surface.

- State what failed and which safe user-controlled input caused it.
- Include the next action when known.
- Do not expose stack traces, SQL, secrets, tokens, raw exception objects,
  internal hostnames, absolute filesystem paths, or dependency internals.
- Keep CLI errors concise; put detailed diagnostics behind `--verbose` or debug
  logs.
- HTTP errors should include a stable code, safe message, and optional request id.
- Validation errors should identify the failing field or argument without dumping
  entire payloads.

## Logging and Observability

- **Library default**: Use the project's existing logger. For new small Node
  projects, `console` is acceptable only at application boundaries for CLI output
  or startup diagnostics; production services should use an approved structured
  logger.
- **No diagnostic `console.log` in libraries**: Libraries must not write to
  stdout/stderr except through a caller-provided logger or documented debug hook.
- **Log levels**:
  - `debug`: Detailed diagnostic information.
  - `info`: Normal lifecycle events.
  - `warn`: Unexpected but recoverable conditions.
  - `error`: Failed operation that can be handled or reported.
  - `fatal`: Process cannot continue.
- **Structured fields**: Include operation name, resource id, attempt, elapsed
  time, result, and correlation id when useful.
- **Correlation ids**: Propagate request ids, job ids, run ids, or trace ids across
  multi-step workflows.
- **Elapsed time**: Use monotonic timers such as `performance.now()` or
  `process.hrtime.bigint()` for durations.
- **Never log secrets**: Redact values whose key names include `token`, `secret`,
  `password`, `key`, `credential`, `cookie`, `authorization`, or `session`.
- **High-cardinality guard**: Do not use raw user input, URLs, file paths, stack
  traces, or unbounded ids as metric labels.
- **Health checks**: Services should expose lightweight liveness/readiness checks
  when the framework/platform supports it.
- **Run summaries**: CLIs and batch jobs should report processed, skipped, failed,
  retried, and elapsed totals.

## Project Structure

Use the existing layout when present. For new package or service projects, prefer:

```text
project-name/
|-- package.json
|-- package-lock.json
|-- tsconfig.json
|-- eslint.config.mjs
|-- README.md
|-- LICENSE
|-- .gitignore
|-- .env.example
|-- src/
|   |-- index.ts
|   |-- config.ts
|   |-- errors.ts
|   `-- ...
`-- tests/
    |-- config.test.ts
    `-- ...
```

- **`src/` layout**: Keep source under `src/`; tests may live in `tests/` or next
  to source files if the project already uses co-located tests.
- **Entrypoints**: Keep package entrypoints explicit in `package.json` `exports`.
- **No junk drawers**: Avoid broad `utils.ts`, `helpers.ts`, or `common.ts` for
  unrelated functions. Use specific names such as `retry-policy.ts` or
  `path-validation.ts`.
- **Boundary modules**: Separate domain logic, external adapters, config,
  persistence, CLI/API entry points, and serialization once each has meaningful
  logic.
- **Generated files**: Put generated output in a clearly marked directory and
  exclude it from manual edits.
- **Tests directory scale**: Keep tests flat for small projects. Mirror `src/`
  when modules or subpackages grow.

### Minimal New Project Templates

**`package.json`**

```json
{
  "name": "project-name",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=24"
  },
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "typecheck": "tsc --noEmit -p tsconfig.json",
    "lint": "eslint .",
    "format": "prettier --check .",
    "test": "vitest run",
    "audit": "npm audit"
  },
  "devDependencies": {
    "@types/node": "24.12.4",
    "eslint": "10.4.0",
    "prettier": "3.8.3",
    "tsx": "4.22.3",
    "typescript": "6.0.3",
    "typescript-eslint": "8.59.4",
    "vitest": "4.1.7"
  }
}
```

**`src/index.ts`**

```ts
export function main(): number {
  return 0;
}
```

**`tests/index.test.ts`**

```ts
import { describe, expect, it } from "vitest";

import { main } from "../src/index.js";

describe("main", () => {
  it("returns success", () => {
    expect(main()).toBe(0);
  });
});
```

## Testing

- **Framework**: Use the existing project test runner. For new TypeScript
  projects, prefer Vitest for unit tests.
- **Run command**: Use the project script, usually `npm test`.
- **Type check command**: `npm run typecheck`.
- **Test naming**: Use `*.test.ts` or the project's existing pattern.
- **Behavior over implementation**: Test observable behavior, not private
  implementation details.
- **Coverage**: Target at least 80% overall for production code. Do not let
  coverage replace meaningful assertions.
- **Regression tests**: Every bug fix needs a test that fails before the fix and
  passes after it when feasible.
- **No public internet in unit tests**: Use local fakes, mocks, fixtures, or
  approved integration-test markers.
- **No real sleeps**: Use fake timers, injected clocks, or short bounded timeouts.
- **No test ordering assumptions**: Each test must run independently.
- **Filesystem tests**: Use temporary directories. Never write tests to the repo
  root, user home, `/tmp`, or `%TEMP%` directly.
- **Randomness**: Seed non-security randomness in tests. For security randomness,
  test shape and validation, not exact values.
- **Cross-platform assertions**: Avoid hardcoded path separators, OS-specific
  error text, and platform-specific ordering unless the test is platform-gated.
- **Snapshot tests**: Use sparingly. Prefer explicit assertions for behavior and
  important output. Review snapshots as code.
- **E2E tests**: Use Playwright when the project already uses it or the user
  approves it. Keep E2E tests focused on critical workflows.
- **Playwright versions**: For new projects that need browser E2E or accessibility
  checks, start with `@playwright/test@1.60.0` and `@axe-core/playwright@4.11.3`,
  then re-check the registry before adding them later.
- **Mocks**: Prefer dependency injection, local fakes, and boundary adapters over
  heavy module mocking. Do not mock what you do not own unless necessary.

### Test Quality Checklist

- Empty input, single item, many items.
- Invalid input and validation errors.
- Missing files, permission failures, malformed data.
- Timeouts, retries, cancellation, and aborts.
- Auth failures and authorization boundaries.
- Platform-specific branches.
- Serialization/deserialization round trips.
- Public API compatibility.
- Common off-by-one, missing-branch, wrong-sort-order, and duplicate-handling
  mistakes.

### Accessibility Verification

Frontend changes must be verified for accessibility when they add or alter UI,
navigation, forms, dialogs, interactive controls, or page structure.

- **Semantic-first checks**: Prefer native HTML semantics before ARIA. Use ARIA
  only when native elements cannot express the interaction.
- **Keyboard path**: Verify that every interactive control is reachable,
  operable, and visibly focused with the keyboard alone.
- **Accessible names**: Controls, links, form fields, dialogs, regions, and
  icon-only buttons need accessible names that match their visible purpose.
- **Playwright locators**: Prefer role, label, placeholder, text, and test id
  locators in that order. Role locators are a useful accessibility smoke test.
- **Web-first assertions**: Use Playwright's retrying `expect` assertions for UI
  state instead of manual sleeps or immediate DOM reads.
- **ARIA assertions**: In Playwright tests, assert accessible name, description,
  and role for critical custom controls.
- **Automated scans**: Use axe checks for changed pages or components when the
  project has Playwright or another browser test harness. Automated scans do not
  replace keyboard and screen-reader-oriented checks.
- **Responsive accessibility**: Verify focus order, skip links, dialogs, menus,
  and sticky UI at mobile and desktop widths.
- **Motion and contrast**: Respect reduced motion and check contrast for text,
  icon-only controls, focus rings, disabled states, and validation errors.
- **Error recovery**: Form errors must be associated with fields, announced to
  assistive tech when appropriate, and preserve user input.

```ts
import { expect, test } from "@playwright/test";

test("save button is accessible", async ({ page }) => {
  await page.goto("/settings");

  const saveButton = page.getByRole("button", { name: "Save changes" });

  await expect(saveButton).toBeVisible();
  await expect(saveButton).toBeEnabled();
  await expect(saveButton).toHaveAccessibleName("Save changes");
});
```

## Configuration

- **Config format**: Use `package.json` for package metadata and scripts,
  `tsconfig.json` for TypeScript, `eslint.config.*` for ESLint, and a documented
  app config file when needed.
- **Config precedence**: Use this order unless the project specifies otherwise:
  CLI args > environment variables > local config file > project defaults.
- **Env validation**: Validate env vars once at startup and expose a typed config
  object.
- **Example files**: Commit `.env.example` with names only. Never include real
  secrets or realistic tokens.
- **Redaction**: Redact config values whose key names include `token`, `secret`,
  `password`, `key`, `credential`, `cookie`, `authorization`, or `session`.
- **Public env vars**: In frontend frameworks, variables exposed to the browser
  are public. Prefixes such as `NEXT_PUBLIC_` or `VITE_` do not make values safe.

**`.env.example`**

```dotenv
APP_ENV=development
APP_LOG_LEVEL=info
APP_DATABASE_URL=
APP_API_TOKEN=
```

## Build, CI, and Release

- **CI parity**: CI must run the same package manager, Node major, typecheck,
  lint, tests, build, and audit commands documented for local development.
- **Clean install**: CI should use `npm ci`, `pnpm install --frozen-lockfile`, or
  the repository's immutable install command.
- **No generated drift**: If codegen is part of the build, CI must verify that
  generated files are current or regenerate them in a clearly controlled step.
- **Artifacts**: Build artifacts must be reproducible from source and lockfile.
  Do not hand-edit generated bundles.
- **Environment separation**: Keep development, test, staging, and production
  configs separate. Production builds must not depend on `.env` files committed to
  source.
- **Release checks**: Before release, run typecheck, lint, tests, build, package
  audit, smoke tests, and package-content verification for publishable packages.
- **Rollback**: Production services and migrations need a rollback or recovery
  plan. If rollback is not practical, document the forward-fix plan.
- **Versioning**: For packages, update version and changelog intentionally. For
  apps, record deployed commit SHA and configuration version where possible.

## Async, Concurrency, and Cancellation

- **Async default**: Use async APIs for I/O in Node and browser code. Keep pure
  CPU logic synchronous.
- **Always await promises**: Do not leave floating promises. If fire-and-forget is
  intentional, attach rejection handling and document lifecycle ownership.
- **Timeouts everywhere**: Every network call, subprocess, lock acquisition,
  queue receive, long-running promise, and external service call needs a timeout
  or documented reason.
- **Cancellation**: Use `AbortController`/`AbortSignal` for cancellable async
  work and propagate signals through API boundaries.
- **Bounded concurrency**: Limit concurrent work for arrays, queues, network
  calls, and file operations. Do not use unbounded `Promise.all` on untrusted or
  large inputs.
- **Promise combinators**:
  - `Promise.all` when every task must succeed.
  - `Promise.allSettled` when partial success is expected and every result must be
    inspected.
  - `Promise.race` only with explicit cleanup for losing tasks.
- **Retries**: Retry only idempotent operations or operations guarded by
  idempotency keys. Use bounded backoff with jitter.
- **Backpressure**: Streams, queues, and workers must apply backpressure instead
  of buffering unbounded data.
- **Shared state**: Avoid shared mutable state. When required, protect it with
  explicit ownership, queues, locks, or atomic operations.
- **CPU-bound work**: Do not block the event loop with heavy CPU work. Ask before
  adding worker threads, native modules, or parallel processing.
- **Top-level await**: Use only when the runtime supports it and startup behavior
  remains clear. Avoid slow top-level awaits in serverless and CLI startup paths.
- **Unhandled rejections**: Treat unhandled promise rejections as defects. Attach
  handlers at the owner boundary and let the process fail fast for unrecoverable
  startup or invariant failures.
- **Resource pools**: Bound database, HTTP, browser, worker, and queue client
  pools. Size pools from platform limits and measured throughput, not guesses.

## File I/O and Streams

- **Use `node:fs/promises`** for async file operations in Node code.
- **Encoding**: Always specify `"utf8"` when reading/writing text.
- **Paths**: Use `node:path` and `node:url` conversion helpers. Do not concatenate
  filesystem paths manually.
- **Large files**: Stream or process in chunks. Never read multi-GB files into
  memory.
- **Atomic writes**: For important files, write to a temporary file in the same
  directory, flush when necessary, then rename.
- **Permissions**: Do not assume POSIX permissions on Windows.
- **Cleanup**: Close file handles, streams, database connections, and child
  processes promptly.
- **JSON**: Parse with validation. Avoid repeated parse/stringify in hot paths.
- **CSV and spreadsheets**: Treat spreadsheet formulas as executable content.
  Escape exported cells that begin with `=`, `+`, `-`, or `@` unless the export is
  explicitly trusted.

## HTTP and External Calls

- **HTTP client**: Use the existing project client. In modern Node, `fetch` is the
  default unless the project needs features from an approved client.
- **Timeouts**: Native `fetch` has no default timeout. Use `AbortSignal.timeout`
  or an explicit `AbortController`.
- **Retries**: Do not retry unsafe methods by default. Retry network failures and
  selected 5xx/429 responses only when idempotent.
- **Headers**: Never log authorization headers, cookies, API keys, or raw request
  bodies containing sensitive data.
- **SSRF**: For server-side URL fetches using user input, validate protocol,
  hostname, IP ranges, redirects, and DNS behavior before fetching.
- **Webhooks**: Verify signatures using raw body bytes when required. Use
  constant-time comparison for secrets.
- **Pagination**: Handle paginated APIs explicitly. Do not assume one page is all
  data.
- **Rate limits**: Respect `Retry-After` and vendor-specific rate-limit headers.
- **Connection reuse**: Reuse clients/agents where the runtime benefits from it.
  Do not create new clients per request in hot paths.
- **Response size**: Bound downloaded response sizes when fetching untrusted or
  user-selected URLs.

## Security

- **Secrets**: Never hardcode, commit, log, expose to browsers, or include in
  source maps.
- **Input validation**: Validate all untrusted input before use.
- **Output encoding**: Escape or encode output for the sink: HTML, URL, SQL,
  shell, JSON, CSV, Markdown, or logs.
- **XSS**: Do not insert unsanitized HTML. Prefer text APIs and framework escaping.
- **CSRF**: Browser cookie-authenticated mutations require CSRF protection unless
  the architecture safely avoids it.
- **CORS**: CORS is not authentication. Restrict origins deliberately and still
  enforce auth and authorization on every protected endpoint.
- **Cookies**: Use `HttpOnly`, `Secure`, and appropriate `SameSite` flags for
  session cookies. Scope `Domain` and `Path` narrowly.
- **JWTs**: Validate issuer, audience, expiration, not-before, algorithm, and
  signature. Do not accept unsigned tokens or algorithm confusion. Keep token
  lifetimes short and support key rotation.
- **OAuth/OIDC**: Validate state, nonce, redirect URI, issuer, audience, and token
  signatures. Never put client secrets in browser code.
- **SQL injection**: Use parameterized queries or query builders. Never build SQL
  with string interpolation from untrusted values.
- **Command injection**: Avoid shell execution. Use `spawn`/`execFile` with args
  arrays. If a shell is unavoidable, validate and quote inputs carefully.
- **Path traversal**: Normalize and validate paths against an allowed base
  directory before reading or writing user-selected paths.
- **Prototype pollution**: Be careful merging untrusted objects. Reject keys such
  as `__proto__`, `prototype`, and `constructor` where relevant.
- **Open redirects**: Validate redirect destinations against an allowlist or same
  origin.
- **Cryptography**: Use platform crypto APIs. Do not invent algorithms. Use
  `crypto.randomUUID()` or cryptographic random bytes for security tokens.
- **Password storage**: Use an approved password hashing algorithm and library.
  Never store plaintext passwords or use general-purpose hashes for passwords.
- **Source maps**: Do not publish source maps containing secrets or sensitive
  source for private production apps unless access is controlled.
- **Dependency risk**: Treat build plugins, transpilers, and code generators as
  privileged code.
- **Sourcemap and error reporting**: Redact secrets and PII before sending errors
  to third-party monitoring. Protect uploaded source maps and avoid exposing them
  publicly for private apps.

### Privacy and Data Handling

- **Data minimization**: Collect, store, log, and transmit only the fields needed
  for the feature.
- **PII boundaries**: Identify PII and sensitive business data before adding logs,
  analytics, exports, or support tooling.
- **Retention**: For user data, audit logs, uploads, and temporary files, define
  retention or cleanup behavior instead of keeping data indefinitely by accident.
- **Analytics**: Do not send PII, secrets, or sensitive event payloads to
  analytics tools. Hashing is not anonymization unless the threat model supports
  it.
- **Exports**: CSV, JSON, and report exports must apply authorization checks,
  field allowlists, and safe filename/content-disposition handling.

## Code Generation and Generated Code

- **Generated files**: Mark generated files clearly and document the command that
  regenerates them.
- **Edit source of truth**: Do not hand-edit generated code unless the generated
  output is the declared source of truth.
- **Generated types**: Keep generated types checked into source only when the
  project convention requires it. Otherwise generate them in CI/build.
- **Codegen inputs**: Treat schemas, OpenAPI specs, GraphQL documents, and
  templates as source code. Review changes to them carefully.
- **AI-generated snippets**: Validate AI-generated code like any other untrusted
  contribution: typecheck, lint, test, and inspect security-sensitive behavior.

## Performance

All production code must be written with algorithmic efficiency and resource
awareness. Every non-trivial function should have a known time and space
complexity. Never write O(n^2) when O(n) or O(n log n) is achievable.

### Algorithmic Complexity

- **Default target**: O(n) for linear scans and lookups. O(n log n) for sorting.
  Avoid O(n^2) nested loops when a `Map`, `Set`, sorting pass, two-pointer
  technique, or sliding window solves it more efficiently.
- **Document hot algorithms**: Add a short complexity note for non-trivial
  algorithms, parsers, transforms, matching logic, and hot paths.
- **Choose data structures deliberately**:

| Workload | Recommended structure/API | Avoid |
|---|---|---|
| Membership checks | `Set<T>` | repeated `array.includes` on large arrays |
| Keyed lookup/grouping | `Map<K, V>` or object with null prototype | parallel arrays |
| String-keyed JSON shape | `Record<string, V>` with validation | unvalidated objects |
| FIFO queue | explicit queue with head index or deque library after approval | `array.shift()` |
| LIFO stack | `array.push` / `array.pop` | custom stack classes |
| Unique values | `Set<T>` | manual duplicate scans |
| Sorting | `array.toSorted()` or copied `sort()` | mutating caller-owned arrays |
| Large binary data | `ArrayBuffer`, `Uint8Array`, streams | strings for binary data |
| Large text processing | streams/chunks | reading everything into memory |

### JavaScript Runtime Efficiency

- Avoid repeated work in loops. Hoist regex compilation, config parsing, object
  creation, and expensive lookups out of hot paths.
- Prefer `Map` over plain objects when keys are not fixed strings or when frequent
  inserts/deletes occur.
- Prefer `Set` for membership checks on large collections.
- Avoid `delete` in hot paths; prefer constructing new objects or using `Map`.
- Avoid object shape churn in tight loops. Initialize objects consistently.
- Avoid unnecessary allocations in hot paths, including repeated closures,
  spreads, JSON serialization, and array copies.
- Avoid `forEach` with async callbacks. Use `for...of` with `await`, or map to
  promises with bounded concurrency.
- Use streams for large I/O and network payloads.
- Debounce or throttle user-triggered expensive frontend work.
- Use memoization only for pure, stable, repeated computations. Bound caches and
  provide invalidation when data changes.
- Profile before optimizing. Keep benchmark notes for non-obvious optimizations
  that reduce readability.

### Frontend Performance

- Measure with browser devtools, framework profiler, Lighthouse/Web Vitals, or
  project tooling before optimizing.
- Optimize images: correct dimensions, modern formats, lazy loading, and explicit
  width/height to prevent layout shift.
- Avoid render-blocking work on the main thread. Split expensive work, defer it,
  or move it to a worker after approval.
- Keep event handlers cheap and passive where appropriate.
- Avoid unnecessary global state updates that re-render large subtrees.
- Use virtualization for long lists when item count can grow large.
- Prefer CSS transforms and opacity for animation. Respect reduced motion.
- Keep bundle budgets visible. Lazy-load rare heavy code paths.

### Benchmarking and Profiling

- Use repeatable benchmarks for hot paths. Avoid one-off timing conclusions.
- Use representative data sizes and shapes.
- Use `performance.now()` for timing in Node and browsers.
- Run benchmarks in the target runtime, not only in tests.
- For Node CPU profiling, use built-in profiler/devtools or project tooling.
- For memory, inspect heap snapshots or process memory metrics.

## Design Principles and Patterns

Use design patterns as tools, not obligations. Do not add classes, inheritance,
frameworks, decorators, dependency injection containers, factories, or layers just
to match a pattern. Simpler code that is faster and easier to read wins.

- **Start simple**: Prefer small pure functions and cohesive modules before
  classes.
- **Composition over inheritance**: Use functions, objects, and small interfaces.
  Use inheritance only for real subtype relationships or framework integration.
- **Explicit dependencies**: Pass clients, clocks, loggers, and config explicitly.
  Do not hide them in global registries.
- **Adapter boundaries**: Wrap external APIs, CLIs, databases, filesystems, and
  SaaS SDKs behind narrow local interfaces.
- **Dependency injection without frameworks**: Constructor/function injection is
  enough for most projects. Do not add DI containers without approval.
- **Strategy**: Use a function or small interface when an algorithm varies behind
  a stable contract.
- **Factory**: Use factory functions when construction has real branching,
  validation, environment selection, or dependency wiring.
- **Repository**: Add a repository boundary only when persistence logic is complex
  enough to isolate from business rules.
- **Facade**: Use a facade when callers need one stable entry point for a
  multi-step subsystem. Keep it thin.
- **Event bus**: Avoid unless multiple independent consumers truly need
  notifications. Prefer direct calls for simple flows.
- **Singletons**: Avoid mutable singletons. Use constants for immutable values and
  pass shared dependencies explicitly.
- **Decorators and reflection**: Avoid unless the framework requires them and the
  tradeoff is understood.
- **Metaprogramming**: Proxies, monkey patching, dynamic module loading, and code
  generation require explicit justification.

## Standard Library and Platform Preferences

Use platform APIs when they fully cover the use case. Add third-party packages
only when the platform lacks a required feature or the user approves the tradeoff.

| Use | Instead of |
|---|---|
| `node:path` | string path concatenation |
| `node:fs/promises` | callback fs APIs for new code |
| `node:crypto` | custom crypto or random token code |
| `crypto.randomUUID()` | UUID packages for basic UUID generation |
| global `fetch` | adding HTTP clients without need |
| `URL` / `URLSearchParams` | manual URL parsing |
| `Intl` | ad hoc locale/date/number formatting |
| `structuredClone` | JSON clone hacks |
| `Map` / `Set` | object/array hacks for keyed collections |
| `AbortController` | custom cancellation flags |
| `node:test` | external test runners for tiny Node-only utilities, when sufficient |
| `node:util.parseArgs` | CLI parser packages for small CLIs |

## Prohibited Patterns

- No `any`.
- No `@ts-ignore`.
- No non-null assertion (`!`) without explicit justification.
- No blind casts from untrusted data.
- No hardcoded secrets, tokens, passwords, cookies, API keys, or service account
  JSON.
- No `eval`, `new Function`, dynamic code execution, or string-based timers.
- No shell command construction with untrusted string interpolation.
- No unsanitized HTML injection.
- No unbounded `Promise.all` over user-controlled or large input.
- No floating promises.
- No swallowed `catch` blocks.
- No global mutable state for request, tenant, auth, or user context.
- No import-time network calls, filesystem scans, process exits, or background
  work.
- No circular dependencies.
- No broad `utils` junk drawers.
- No unresolved task-marker comments without an associated issue, owner, or
  immediate follow-up context.

## Validation Before Completion

Before claiming a TypeScript change is complete, run the relevant project
commands. For most projects this means:

```console
npm run typecheck
npm run lint
npm test
npm run build
```

Use the repository's actual package manager and scripts. If a command is missing,
state that explicitly and run the closest available verification. For frontend
changes, also verify the app in a browser when the behavior or layout is
user-facing.

## Dry-Run Audit Mode

Use this mode when auditing existing TypeScript codebases across one or more
projects without changing files. The audit goal is to identify correctness,
security, maintainability, performance, and verification risks using this
standard as the rubric.

### No-Edit Rule

- Do not edit files, install dependencies, run formatters with write mode, run
  migrations, generate code, update lockfiles, or start long-lived services.
- Read-only commands are allowed: `pwd`, `ls`, `find`, `rg`, `cat`, `sed`,
  `git status`, `git diff`, `git log`, package-manager script listing, and
  test/type/lint/build commands that do not write source or lockfiles.
- If a command may write files (`npm install`, `npm audit fix`, `eslint --fix`,
  `prettier --write`, codegen, migrations, build commands that emit tracked
  files), skip it or ask for explicit approval.
- If generated output is unavoidable for a check, write only to ignored temp or
  tool output directories and state that in the report.
- After any command that might create caches, coverage, snapshots, generated
  files, or build output, run `git status --short` and report any changed or
  untracked files. Do not clean them up unless the user explicitly asks.

### Audit Discovery Order

For each project, inspect these before scoring:

1. Repository state: current path, git status, dirty files, branch, recent commit.
2. Package manager and workspace shape: lockfile, workspaces, package scripts,
   monorepo tooling, package boundaries.
3. Runtime target: `engines`, `.nvmrc`, `.node-version`, Dockerfile, CI runtime,
   serverless/edge/deploy config.
4. TypeScript config: root and package `tsconfig*`, inherited configs,
   strictness, module resolution, declaration settings, project references.
5. Lint/format config: ESLint flat config or legacy config, Prettier config,
   ignored files, disabled rules.
6. Test setup: unit, integration, E2E, browser, accessibility, coverage, CI
   commands, fixtures, test isolation.
7. Source layout: entrypoints, public APIs, app surfaces, framework boundaries,
   generated code, adapters, persistence modules.
8. Security and config: env handling, secret patterns, auth, CORS/cookies, input
   validation, SSRF, command execution, path handling.
9. Dependency and supply chain: direct dependencies, lockfile health, audit
   output when safe, package scripts, postinstall hooks, publish config.
10. Performance and operations: hot paths, concurrency, streaming, bundle/build
    size, observability, shutdown, CI/release/deploy checks.

### Read-Only Command Set

Prefer these commands, adapted to the package manager and project structure:

```console
pwd
git status --short
git branch --show-current
rg --files -g 'package.json' -g 'tsconfig*.json' -g '*eslint*' -g '*prettier*'
rg --files -g 'package-lock.json' -g 'pnpm-lock.yaml' -g 'yarn.lock' -g 'bun.lock'
npm pkg get scripts engines packageManager workspaces
npm run
npm run typecheck --if-present
npm run lint --if-present
npm test --if-present
npm run build --if-present
npm audit --audit-level=moderate
git status --short
```

- Use `pnpm`, Yarn, or Bun equivalents when their lockfile is present.
- For monorepos, prefer workspace-aware commands that match existing CI.
- If tests or builds are destructive, network-heavy, require secrets, or start
  persistent services, skip them and record why.
- Treat `npm test` and `npm run build` as conditional dry-run commands. Run them
  only when project docs or script names indicate they do not mutate tracked
  files, deploy, run migrations, update snapshots, or require unavailable
  services.
- Do not pass runner-specific flags such as Jest's `--runInBand` unless the
  project uses that runner.
- Do not treat a missing script as an automatic failure. Score it as a coverage or
  operability gap when the project lacks an equivalent check.

### Severity Levels

Classify findings by user impact and confidence.

| Severity | Meaning |
|---|---|
| Critical | Likely security issue, data loss, production crash, or broken release path. |
| High | Likely correctness, security, or operational failure in normal use. |
| Medium | Real maintainability, testing, portability, or performance risk. |
| Low | Local quality issue with limited blast radius. |
| Info | Observation or improvement idea without clear current risk. |

Examples:

- Critical: secret exposure, auth bypass, unsafe migration, public source maps
  with secrets.
- High: strict mode disabled with unsafe casts, unvalidated API boundary, missing
  auth check.
- Medium: missing typecheck script, weak test isolation, unbounded concurrency.
- Low: inconsistent naming, small config drift, minor duplicate helper.
- Info: optional framework cleanup, docs polish.

Only report a finding when it has evidence. Include file path, line number when
available, command output when relevant, and the violated rule from this
standard.

Assign each finding a confidence level:

- High: directly proven by code, config, or command output.
- Medium: strongly indicated by code/config, but one runtime condition is not
  verified.
- Low: plausible risk that needs follow-up before action.

Do not use Low-confidence findings to cap the score. Put Low-confidence items in
follow-up unless the user explicitly asks for speculative risk discovery.

### Scoring Rubric

Score each project out of 100 using 10 criteria worth 10 points each:

1. Runtime and version alignment.
2. Package manager, lockfile, and dependency hygiene.
3. TypeScript compiler strictness and type safety.
4. Lint, formatting, and static analysis.
5. App-surface and framework boundary correctness.
6. Runtime validation, error handling, and observability.
7. Security, privacy, secrets, and supply chain.
8. Tests, accessibility, and verification coverage.
9. Performance, concurrency, and resource management.
10. Maintainability, architecture, portability, and CI/release readiness.

Use this scoring:

- `10`: Meets or exceeds this standard with evidence.
- `8-9`: Minor gaps, low risk, clear local conventions.
- `6-7`: Meaningful gaps that should be addressed soon.
- `4-5`: Significant risk or missing core controls.
- `0-3`: Broken, absent, or actively dangerous for that criterion.

Do not average away critical issues. If any Critical finding exists, cap the
overall score at `69` until it is fixed. If any High finding affects security,
auth, data integrity, or release safety, cap the overall score at `84`.

### Multi-Project Audit Report

For multiple projects, produce one summary table and one section per project.

**Summary table columns**

- Project
- Package manager
- Runtime target
- Frameworks
- Typecheck
- Lint
- Tests
- Build
- Score
- Critical/High count
- Top risk

**Per-project section**

```text
Project: <name>
Path: <path>
Score: <n>/100
Criterion scores:
  Runtime/package/types/lint/surfaces/validation/security/tests/performance/maintainability:
  <n>/<n>/<n>/<n>/<n>/<n>/<n>/<n>/<n>/<n>
Package manager: <npm|pnpm|yarn|bun|unknown>
Runtime: <node/browser/edge/etc>
Frameworks: <detected frameworks>
Commands run: <read-only commands>
Commands skipped: <command and reason>
Files changed by audit commands: <none|paths and command that caused them>

Findings:
- [Severity] <title>
  Evidence: <file:line or command output>
  Confidence: <High|Medium|Low>
  Why it matters: <risk>
  Standard: <section of TYPESCRIPT.md>
  Suggested fix: <short non-edit recommendation>

Strengths:
- <what is already strong>

Follow-up checklist:
- <highest leverage next steps>
```

### Audit Quality Rules

- Findings lead. Do not bury Critical or High issues in narrative.
- Separate evidence from inference. Mark inferred risks clearly.
- Prefer fewer high-confidence findings over long speculative lists.
- Do not recommend new frameworks or dependencies unless the existing project
  needs them and the tradeoff is justified.
- Respect existing conventions when they are coherent and safe.
- For version-sensitive findings, verify current docs or registry data before
  reporting.
- For security findings, avoid printing secret values. Show only filenames, key
  names, prefixes, or redacted samples.
- End every audit with what was not verified, especially skipped tests, missing
  secrets, inaccessible CI, or commands that could not run safely.
