# Optional local PDF helpers

- `upload_pdf.py`: dependency-free Python 3 OS picker for one human-selected PDF. Accepts a short-lived private upload ticket, never an arbitrary PDF path or URL; snapshots actual bytes and waits for browser file/Paper approval. macOS opens Downloads; Windows/Linux use Tk.
- `selected_files.py`: Python 3 POSIX helper for an explicitly granted directory/file. `inspect --root <granted-root> [--file <relative-file>]` checks PDF bytes/hash and optional pypdf metadata. `upload --root ... --file ... --lease-file <private-file>` consumes a 15-minute upload-only lease and rechecks the exact SHA. Rejects symlinks/escape; at most 50 PDFs/300 MiB, each 30 MiB. A single-file grant must not scan its parent folder.

Keep ticket/lease/journal files private (0600) and remove consumed secrets. Neither helper installs a daemon or reads third-party accounts. No pypdf means metadata extraction is unavailable, not successful. Without a supported runtime or client-exposed file, use browser import or paper-page Upload.

The unpublished selected_files.py source reads only a regular mode-0600 lease of at most 10,000 bytes. It uses no-follow/nonblocking descriptor acquisition, checks the opened file and observed path metadata, and rejects changes before network access. [Synthetic tests](../../../../../tests/README.md) cover FIFO refusal, replacement/permission/size races, closure and successful transfer. These guards are not a filesystem snapshot against arbitrary concurrent writers. Public v0.2.0 and release assets remain unchanged.

Recent update: 2026-11-21 unpublished bounded lease acquisition with refusal and healthy controls.
