# PRDB reading

`SKILL.md` guides catalog matching, owner PDFs, exact anchors, comments, private reviews, long-page reading, page images and complete source checks. Public reviews require exact-body owner confirmation in PRDB.

[scripts](scripts/README.md) contains the optional OS picker and explicitly granted-file helper. Browser imports support one PDF or selected exports. Remote MCP does not automatically see local folders or attachments; report the actual uploaded result.

The unpublished selected-file helper now uses a bounded regular-file lease read, rejects observed replacements/type/permission/size changes, and closes its descriptor before parsing or transport. Public v0.2.0 remains unchanged.

Recent update: 2026-11-21 unpublished lease-file acquisition and synthetic regression coverage.
