# Selected-file helper regressions

Run `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` from the repository root with POSIX Python 3, matching the optional helper's supported runtime. Tests import the actual helper and use only synthetic PDFs, leases and a mocked HTTP transport. No account, provider, real PDF or credential is used.

The unpublished lease-acquisition correction rejects FIFOs and other nonregular files before reading, enforces mode 0600 and the 10,000-byte limit, opens without following links or blocking on a FIFO race, and verifies the opened descriptor and observed path metadata. Controls cover replacement, permission and size changes, descriptor closure, malformed JSON and successful exact-byte upload. The FIFO regression owns a bounded child and proves function entry before classifying a timeout.

These source regressions do not modify the immutable public v0.2.0 tag or release assets, establish native-client acceptance, or publish a new package. The existing PDF metadata behavior of this public source remains separate from the application helper's newer metadata extraction.

Updated: 2026-11-21 UTC. Add synthetic lease-file type, race and successful-transfer controls.
