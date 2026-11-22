# PRDB public plugin roadmap

## Released baseline

Public trial 0.2.0 supports ordinary remote MCP/OAuth, Library/community actions, selected PDF transfer, checked annotations and private reviews. Existing fixed versions and Release assets remain unchanged. Production registration availability is controlled by the website, not this package. The plugin has not been submitted to the public directory.

## Current delivery: lease acquisition and maintained regressions

The optional selected-file helper now acquires a bounded regular mode-0600 lease through a no-follow/nonblocking descriptor, checks the initial/opened/final descriptor and final path identity, and requires the actual checked length before JSON parsing or transport. The selected PDF root/bytes/SHA, endpoint/redirect/lease policy and this public helper's existing metadata extraction remain unchanged. Thirteen synthetic helper regressions passed on the reviewed source, including valid exact-byte upload, bounded FIFO entry/cleanup, replacement, permission/size/path changes and descriptor closure.

This source is integrated with the earlier independent maintainer workflow. Ready-PR checks now run the helper regressions as well as package validation and packaging boundaries. Combined-tree local validation passed: distributed package validation, seven packaging regressions, thirteen helper regressions and actionlint. Exact-head automatic CI remains a separate gate; no future CI result is claimed here. No version bump, fixed-tag/Release replacement, directory submission or installed-client change is performed. Fresh-machine/human acceptance remains separate.

## Earlier delivery: independent maintainer workflow

Implemented for review: task-branch instructions, Claude entry, source handoff template, automatic ready-PR package validation/helper syntax and validator tests. Optional manual candidate packaging produces only an Actions artifact; no new version is published. Local validation passed: actionlint, package validation, seven packaging regressions, patch whitespace and English-copy/local-link/README coverage. Actual PR execution and owner merge are tracked in the PR.

## Remaining acceptance and next work

- A fresh ordinary profile/device: installation, browser consent, connection identity/revocation and actual chosen file transfer.
- Complete real PDF highlight/comment/private-review round trip and accurate source anchors; real export/batch and annotated files require their own acceptance.
- Review changed server contracts before a future client version; do not overwrite this distributed package from private authoring templates automatically.
- Public-directory publisher verification/submission and additional clients are separate future decisions. No directory acceptance is claimed.

## Delivery log

- 2026-10-21: independent public-client workflow prepared; package validation and seven regressions passed locally; source/PR execution evidence belongs to the review. This batch does not modify the installable payload, version tags or Release assets.

- 2026-11-22: lease-file hardening and thirteen synthetic helper regressions integrated with the existing independent PR workflow; exact-head CI and source merge precede any separately authorized future package version.
