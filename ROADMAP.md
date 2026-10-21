# PRDB public plugin roadmap

## Released baseline

Public trial 0.2.0 supports ordinary remote MCP/OAuth, Library/community actions, selected PDF transfer, checked annotations and private reviews. Existing fixed versions and Release assets remain unchanged. Production registration availability is controlled by the website, not this package. The plugin has not been submitted to the public directory.

## Current delivery: independent maintainer workflow

Implemented for review: task-branch instructions, Claude entry, source handoff template, automatic ready-PR package validation/helper syntax and validator tests. Optional manual candidate packaging produces only an Actions artifact; no new version is published. Local validation passed: actionlint, package validation, seven packaging regressions, patch whitespace and English-copy/local-link/README coverage. Actual PR execution and owner merge are tracked in the PR.

## Remaining acceptance and next work

- A fresh ordinary profile/device: installation, browser consent, connection identity/revocation and actual chosen file transfer.
- Complete real PDF highlight/comment/private-review round trip and accurate source anchors; real export/batch and annotated files require their own acceptance.
- Review changed server contracts before a future client version; do not overwrite this distributed package from private authoring templates automatically.
- Public-directory publisher verification/submission and additional clients are separate future decisions. No directory acceptance is claimed.

## Delivery log

- 2026-10-21: independent public-client workflow prepared; package validation and seven regressions passed locally; source/PR execution evidence belongs to the review. This batch does not modify the installable payload, version tags or Release assets.
