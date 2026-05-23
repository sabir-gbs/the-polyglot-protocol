# Security Policy

The Polyglot Protocol is documentation and validation tooling for coding agents.
Security issues are still possible if guidance accidentally recommends unsafe
behavior or if scripts mishandle local files.

## Reporting

Report security issues through the repository's GitHub security advisory flow
when available. If advisories are not enabled, open an issue that avoids
including secrets, exploit payloads, or private environment details.

## Scope

In scope:

- Unsafe guidance that could expose secrets, bypass authentication, weaken
  validation, or encourage insecure defaults
- Validator behavior that misses obvious dangerous guidance
- Accidentally committed sensitive project data

Out of scope:

- Misuse of the guidance in unrelated repositories
- Vulnerabilities in third-party coding agents
- General requests for new language coverage

## Handling Sensitive Data

Do not include API keys, tokens, passwords, private keys, customer data, or
machine-specific paths in issues, pull requests, examples, or tests.
