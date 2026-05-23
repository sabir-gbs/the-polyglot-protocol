# Install And Version Commands

Use these commands to verify local toolchains before installing or upgrading.
Check official sources before pinning new versions.

| Area | Verify command | Install/update source |
|---|---|---|
| Python | `python --version` | python.org, distro packages, `uv`, or `pyenv` |
| TypeScript/JavaScript | `node --version && npm --version` | nodejs.org and npm registry |
| Bash | `bash --version` | OS package manager |
| C | `cc --version` | OS package manager or compiler vendor |
| C++ | `c++ --version` | OS package manager or compiler vendor |
| C#/.NET | `dotnet --info` | Microsoft .NET release metadata |
| CSS/HTML | browser and build-tool versions | project browser matrix |
| Dart | `dart --version` | dart.dev or Flutter SDK |
| Go | `go version` | go.dev downloads |
| Java | `java -version` | Adoptium, Oracle, SDKMAN, or distro packages |
| Kotlin | `kotlin -version` or Gradle plugin version | JetBrains releases |
| Lua | `lua -v` | lua.org or host application runtime |
| PHP | `php -v && composer --version` | php.net and Composer |
| R | `R --version` | CRAN or distro packages |
| Ruby | `ruby -v && bundle --version` | ruby-lang.org, ruby-install, rbenv, or asdf |
| Rust | `rustc --version && cargo --version` | rustup stable channel |
| Shopify Liquid | `shopify version` | Shopify CLI docs |
| SQL | database client version, such as `psql --version` | database vendor |
| Swift | `swift --version` | swift.org or Xcode |
| Zig | `zig version` | ziglang.org downloads |

## Update Rules

- Prefer stable production releases.
- Do not install globally inside a project unless the tool is intentionally
  system-level.
- Keep lockfiles and project metadata aligned with runtime versions.
- Record version evidence in workflow audits.
