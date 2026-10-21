# Public plugin Actions

[checks.yml](checks.yml) automatically runs offline package/helper validation and regression tests for non-draft PRs against main. Subsequent PR pushes rerun the checks and cancel obsolete runs; drafts wait until ready. No application/operator workflow, service secret or user account is needed.

Optional workflow_dispatch runs the same checks on the selected branch. package_candidate=true additionally creates a deterministic reviewed-payload ZIP, SHA256SUMS and file manifest as a seven-day artifact. It never creates tags, GitHub Releases, directory submissions or installed-client changes. All jobs have read-only repository permission.

[CONTRIBUTING](../../CONTRIBUTING.md) defines independent review and deliberate new-version publication. Package structure checks do not establish real installation/OAuth/file-picker/device acceptance.

Recent update: 2026-10-21 ready-PR client checks with separately requested candidate artifacts.
