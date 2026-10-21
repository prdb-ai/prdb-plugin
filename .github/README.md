# Plugin collaboration and automation

- [CONTRIBUTING](../CONTRIBUTING.md) and [the PR template](pull_request_template.md): independent source review and separately authorized version publication.
- [workflows](workflows/README.md): automatic ready-PR validation and optional manual candidate ZIP artifacts.
- check_plugin.py: offline distributed-tree validator and deterministic candidate packager; run with --help for output options.
- test_check_plugin.py: regression checks for package boundaries, endpoint/schema errors, symlinks, deterministic bytes and overwrite protection.
- [ISSUE_TEMPLATE](ISSUE_TEMPLATE/README.md): public, redacted bug and trial feedback. Use PRDB support for sensitive reports.

Recent update: 2026-10-21 independent plugin PR checks and candidate-only packaging.
