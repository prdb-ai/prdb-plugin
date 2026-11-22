# Plugin repository workflow

This repository independently owns the publicly distributed PRDB plugin. Its PR checks and candidate packaging do not depend on an application or operator commit. Read AGENTS.md and START_HERE.md before work.

## Source review

Use a codex/<task> branch, scoped local tests and the PR template. Preserve dirty work and report the exact SHA, behavior/compatibility changes and outstanding human acceptance. Owner-authorized commit/push/PR hands source to the maintainer; merging or publishing requires its own applicable authorization. Actual GitHub permissions apply: application developer Write does not imply plugin publishing rights.

A ready PR automatically validates the manifest, marketplace, production MCP endpoint/scopes, reviewed file allowlist and helper syntax, then runs the validator's regression tests. Drafts wait until ready. A new commit cancels an obsolete run of the same PR. Read-only CI has no service credentials or Release-write permission.

Private authoring templates and this distributed tree have different purposes. Transfer a reviewed client change deliberately, inspect the transformed files and validate the public package; neither an application merge nor a deployment silently copies or publishes plugin files.

## Candidate and version publication

An explicitly requested checks.yml workflow_dispatch with package_candidate=true validates the current branch and creates a deterministic ZIP, file manifest and SHA256SUMS as a short-lived Actions artifact. The ZIP contains only the reviewed plugins/prdb payload. This is a candidate: it creates no tag, Release or marketplace listing and does not modify installed clients.

For an owner-authorized public version:

1. Review endpoint/scopes, helper behavior, server compatibility and release notes. New scopes require actual owner consent; old connections do not expand automatically.
2. Change package version/release notes in a reviewed source batch. Preserve the prdb@prdb identity. Never replace existing fixed tags, ZIPs, manifests or checksums merely to update links.
3. Validate candidate contents/hashes and perform the applicable new-profile installation, browser OAuth, selected PDF, exact highlight/comment and private review checks. State any unaccepted client/device path.
4. After explicit version-publication authorization, publish the exact accepted bytes as a new version and update public quickstart/download links in the reviewed release batch. Hosted application deployment and public plugin publication remain independent.

Public code is copyright-reserved; LICENSE-NOTICE.md governs distribution. Use SECURITY.md for sensitive reports and keep private material out of issues/artifacts.

Updated: 2026-10-21. Independent client review, validation and candidate packaging workflow.
