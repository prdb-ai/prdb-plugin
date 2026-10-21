"""Exercise public-package boundaries without accounts or client settings."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from check_plugin import PACKAGE_FILES, build_candidate, validate

ROOT = Path(__file__).resolve().parents[1]


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        shutil.copytree(ROOT / "plugins", self.root / "plugins")
        shutil.copytree(ROOT / ".agents", self.root / ".agents")

    def mutate(self, name, transform):
        path = self.root / name
        data = json.loads(path.read_text())
        transform(data)
        path.write_text(json.dumps(data))

    def test_valid_payload_and_deterministic_candidate(self):
        self.assertEqual(validate(self.root), "0.2.0")
        first = build_candidate(self.root, self.base / "first", "a" * 40)
        second = build_candidate(self.root, self.base / "second", "a" * 40)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as zf:
            self.assertEqual(set(zf.namelist()), {"prdb/" + name for name in PACKAGE_FILES})
            for name in PACKAGE_FILES:
                self.assertEqual(zf.read("prdb/" + name), (self.root / "plugins/prdb" / name).read_bytes())
        record = json.loads((first.parent / "manifest.json").read_text())
        self.assertEqual(record["source_sha"], "a" * 40)
        for name, digest in record["files"].items():
            self.assertEqual(digest, hashlib.sha256((self.root / "plugins/prdb" / name).read_bytes()).hexdigest())
        for line in (first.parent / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            self.assertEqual(digest, hashlib.sha256((first.parent / name).read_bytes()).hexdigest())

    def test_unreviewed_endpoint_rejected(self):
        self.mutate("plugins/prdb/.mcp.json", lambda d: d["mcpServers"]["prdb-reading"].update(url="https://example.com/mcp"))
        with self.assertRaisesRegex(ValueError, "endpoint"):
            validate(self.root)

    def test_embedded_credentials_rejected(self):
        self.mutate("plugins/prdb/.mcp.json", lambda d: d["mcpServers"]["prdb-reading"].update(headers={"Authorization": "synthetic"}))
        with self.assertRaisesRegex(ValueError, "credentials"):
            validate(self.root)

    def test_unreviewed_file_rejected(self):
        (self.root / "plugins/prdb/private.key").write_text("synthetic sentinel")
        with self.assertRaisesRegex(ValueError, "allowlist"):
            validate(self.root)

    def test_symlink_rejected(self):
        target = self.root / "plugins/prdb/README.md"
        target.unlink()
        target.symlink_to(ROOT / "README.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate(self.root)

    def test_version_and_marketplace_mismatch_rejected(self):
        self.mutate("plugins/prdb/.codex-plugin/plugin.json", lambda d: d.update(version="../../invalid"))
        with self.assertRaisesRegex(ValueError, "version"):
            validate(self.root)
        self.mutate("plugins/prdb/.codex-plugin/plugin.json", lambda d: d.update(version="0.2.0"))
        self.mutate(".agents/plugins/marketplace.json", lambda d: d["plugins"][0]["source"].update(path="../private"))
        with self.assertRaisesRegex(ValueError, "source"):
            validate(self.root)

    def test_existing_candidate_is_never_overwritten(self):
        output = self.base / "existing"
        output.mkdir()
        sentinel = output / "keep"
        sentinel.write_text("original")
        with self.assertRaises(FileExistsError):
            build_candidate(self.root, output, "a" * 40)
        self.assertEqual(sentinel.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
