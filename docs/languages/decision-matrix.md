# Language Decision Matrix

Use this matrix before choosing a language for new code.

## Default Choice

Use Python for operational scripts, automation, audits, migrations, file
processing, and glue code unless the repository already has a better native
script runner.

## Platform-Native Choices

| Task | Preferred choice |
|---|---|
| WordPress plugin or theme behavior | PHP |
| Shopify storefront theme | Shopify Liquid, HTML, CSS, JavaScript |
| Browser application | TypeScript, HTML, CSS |
| Node.js service or package | TypeScript |
| iOS or macOS app | Swift |
| Android app | Kotlin |
| Database schema/query/migration | SQL |
| Systems or embedded code | Rust, C, C++, or Zig based on repo |
| .NET app or service | C# |
| JVM service | Java or Kotlin based on repo |
| Data analysis | R when repo is R; otherwise Python unless requested |
| Thin local shell glue | Bash |

## Decision Rules

- Existing repo language and framework win over personal preference.
- Do not introduce a second runtime for small tasks.
- Do not use compiled languages for simple operational glue.
- Do not use Bash for complex parsing, retries, queues, or cross-platform logic.
- Verify current stable versions before installing or pinning toolchains.
