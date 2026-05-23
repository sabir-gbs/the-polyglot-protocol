# Language Guidance Index

Use this directory for language-specific code generation rules. Start with
`../../language-guidelines.md` for language selection and default-script policy,
then open the relevant language file before generating code.

## Default Rule

Python is the default for operational scripts, automation, audits, migrations,
file processing, and glue code. Existing project language and platform-native
code still win for product surfaces such as WordPress PHP, Shopify Liquid,
Android Kotlin, iOS Swift, database SQL, and frontend HTML/CSS.

## Human-Readable READMEs

Each individualized language guide has a matching README folder, such as
`python/readme.md`, `typescript/readme.md`, or `rust/readme.md`. These summarize
quality, completeness, and accuracy decisions for humans. The matching top-level
language `.md` file remains the enforceable agent guidance.

## Language Files

- [Decision Matrix](decision-matrix.md)
- [Do Not Generate Policy](do-not-generate-policy.md)
- [Examples](examples.md)
- [Install And Version Commands](install-version-commands.md)
- [Language File Template](language-file-template.md)
- [Maintenance Policy](maintenance-policy.md)
- [Pre-Codegen Checklist](pre-codegen-checklist.md)
- [Scoring Rubric](scoring-rubric.md)
- [Score Report](score-report.md)
- [Top LLM Coding Nuances](top-llm-coding-nuances.md)
- [Bash](bash.md)
- [Bash README](bash/readme.md)
- [C](c.md)
- [C README](c/readme.md)
- [C#](c-sharp.md)
- [C# README](c-sharp/readme.md)
- [C++](cpp.md)
- [C++ README](cpp/readme.md)
- [CSS](css.md)
- [CSS README](css/readme.md)
- [Dart](dart.md)
- [Dart README](dart/readme.md)
- [Go](go.md)
- [Go README](go/readme.md)
- [HTML](html.md)
- [HTML README](html/readme.md)
- [Java](java.md)
- [Java README](java/readme.md)
- [JavaScript](javascript.md)
- [JavaScript README](javascript/readme.md)
- [Kotlin](kotlin.md)
- [Kotlin README](kotlin/readme.md)
- [Lua](lua.md)
- [Lua README](lua/readme.md)
- [PHP](php.md)
- [PHP README](php/readme.md)
- [Python](python.md)
- [Python README](python/readme.md)
- [R](r.md)
- [R README](r/readme.md)
- [Ruby](ruby.md)
- [Ruby README](ruby/readme.md)
- [Rust](rust.md)
- [Rust README](rust/readme.md)
- [Shopify Liquid](shopify-liquid.md)
- [Shopify Liquid README](shopify-liquid/readme.md)
- [SQL](sql.md)
- [SQL README](sql/readme.md)
- [Swift](swift.md)
- [Swift README](swift/readme.md)
- [TypeScript](typescript.md)
- [TypeScript README](typescript/readme.md)
- [Zig](zig.md)
- [Zig README](zig/readme.md)
