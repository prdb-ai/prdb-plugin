# Public plugin Actions

[checks.yml](checks.yml) automatically runs offline package/helper validation and regression tests for non-draft PRs against main. Subsequent PR pushes rerun the checks and cancel obsolete runs; drafts wait until ready. No application/operator workflow, service secret or user account is needed.

Optional workflow_dispatch runs the same checks on the selected branch. package_candidate=true additionally creates a deterministic reviewed-payload ZIP, SHA256SUMS and file manifest as a seven-day artifact. It never creates tags, GitHub Releases, directory submissions or installed-client changes. All jobs have read-only repository permission.

[CONTRIBUTING](../../CONTRIBUTING.md) defines independent review and deliberate new-version publication. Package structure checks do not establish real installation/OAuth/file-picker/device acceptance.
Ready-PR validation also runs the actual optional selected-file helper against synthetic leases/PDFs, including owned bounded FIFO children and read-time changes. No service, account or network is used by those regressions.

Recent update: 2026-11-22 include synthetic selected-file lease regressions in ready-PR checks; no package publication.
