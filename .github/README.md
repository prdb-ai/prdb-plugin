# Plugin collaboration and automation

- [CONTRIBUTING](../CONTRIBUTING.md) and [the PR template](pull_request_template.md): independent source review and separately authorized version publication.
- [workflows](workflows/README.md): automatic ready-PR validation and optional manual candidate ZIP artifacts.
- check_plugin.py: offline distributed-tree validator and deterministic candidate packager; run with --help for output options.
- test_check_plugin.py: regression checks for package boundaries, endpoint/schema errors, symlinks, deterministic bytes and overwrite protection.
- [ISSUE_TEMPLATE](ISSUE_TEMPLATE/README.md): public, redacted bug and trial feedback. Use PRDB support for sensitive reports.
- [tests](../tests/README.md): actual selected-file helper lease, FIFO, race and successful-transfer regressions, also run by ready-PR checks.

Recent update: 2026-11-22 include synthetic selected-file lease regressions in ready-PR checks; no package publication.
