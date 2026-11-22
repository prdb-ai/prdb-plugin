"""Granted-file lease regressions use synthetic files and no real transport."""

import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HELPER = (
    Path(__file__).resolve().parents[1]
    / "plugins/prdb/skills/prdb-reading/scripts/selected_files.py"
)
spec = importlib.util.spec_from_file_location("selected_files_under_test", HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class Response:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit):
        return b'{"document":{"id":"synthetic-document"}}'


class LeaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="prdb-lease-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.pdf = b"%PDF-1.7\nsynthetic selected bytes\n%%EOF\n"
        (self.root / "paper.pdf").write_bytes(self.pdf)
        self.lease = self.root / "lease.json"
        self.ticket = {
            "sha256": hashlib.sha256(self.pdf).hexdigest(),
            "handle": "synthetic-handle",
            "transfer_url": "https://prdb.ai/api/v1/reading-transfer/synthetic-handle/direct",
            "transfer_lease": "synthetic-private-lease",
        }
        self.write_lease()
        self.transport = patch.object(helper.urllib.request, "build_opener")
        self.opener = self.transport.start()
        self.addCleanup(self.transport.stop)
        self.opener.return_value.open.return_value = Response()

    def write_lease(self):
        self.lease.write_text(json.dumps(self.ticket))
        self.lease.chmod(0o600)

    def upload(self):
        return helper.upload(self.root, "paper.pdf", self.lease)

    def refused(self, action):
        with self.assertRaisesRegex(ValueError, "(?i)lease"):
            action()
        self.opener.assert_not_called()

    def test_regular_private_lease_retains_exact_pdf_and_authorization(self):
        self.assertEqual(self.upload(), {"document": {"id": "synthetic-document"}})
        call = self.opener.return_value.open.call_args
        request = call.args[0]
        self.assertEqual(request.full_url, self.ticket["transfer_url"])
        self.assertEqual(request.get_header("Authorization"), "Bearer synthetic-private-lease")
        self.assertIn(self.pdf, request.data)
        self.assertEqual(call.kwargs["timeout"], 60)
        self.assertEqual(self.opener.return_value.open.call_count, 1)

    def test_fifo_is_rejected_in_owned_bounded_child_without_opening_or_network(self):
        fifo = self.root / "lease.fifo"
        os.mkfifo(fifo, 0o600)
        fifo.chmod(0o600)
        self.assertTrue(stat.S_ISFIFO(fifo.lstat().st_mode))
        self.assertEqual(stat.S_IMODE(fifo.lstat().st_mode), 0o600)
        code = """import importlib.util,sys
from unittest.mock import patch
s=importlib.util.spec_from_file_location('helper',sys.argv[1])
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
with patch.object(m.urllib.request,'build_opener',side_effect=AssertionError('No network')):
 print('Lease call entered',flush=True)
 try:m.upload(sys.argv[2],'paper.pdf',sys.argv[3])
 except ValueError as e:
  if 'lease' not in str(e).lower():raise
 else:raise AssertionError('FIFO lease accepted')
print('Synthetic FIFO refused before transport')
"""
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-B", "-c", code, str(HELPER), str(self.root), str(fifo)],
                capture_output=True,
                timeout=3,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            self.assertEqual(error.stdout, b"Lease call entered\n", "No function-entry proof")
            self.fail("FIFO validation blocked after function entry; owned child was terminated")
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(
            result.stdout, b"Lease call entered\nSynthetic FIFO refused before transport\n"
        )
        self.opener.assert_not_called()

    def test_directory_is_refused_before_pdf_or_transport(self):
        self.lease.unlink()
        self.lease.mkdir(mode=0o600)
        self.refused(self.upload)

    def test_symlink_is_refused(self):
        target = self.root / "target.json"
        self.lease.rename(target)
        self.lease.symlink_to(target)
        self.refused(self.upload)

    def test_permissions_are_not_relaxed(self):
        self.lease.chmod(0o644)
        self.refused(self.upload)

    def test_oversize_lease_is_not_parsed(self):
        self.lease.write_bytes(b"x" * 10001)
        self.refused(self.upload)

    def test_replacement_between_metadata_check_and_open_is_refused(self):
        original = helper.os.open
        original_path_open = Path.open
        replacement = self.root / "replacement.json"
        replacement.write_bytes(self.lease.read_bytes())
        replacement.chmod(0o600)

        changed = []

        def replace(path):
            if os.fspath(path) == str(self.lease):
                os.replace(replacement, self.lease)
                changed.append(True)

        def descriptor_open(path, flags, *args, **kwargs):
            replace(path)
            return original(path, flags, *args, **kwargs)

        def path_open(path, *args, **kwargs):
            replace(path)
            return original_path_open(path, *args, **kwargs)

        with patch.object(helper.os, "open", side_effect=descriptor_open), patch.object(
            Path, "open", path_open
        ):
            try:
                self.refused(self.upload)
            finally:
                self.assertEqual(changed, [True], "Replacement must actually precede the lease read")

    def test_permission_change_after_open_is_refused_and_descriptor_closed(self):
        original = helper.os.open
        original_path_open = Path.open
        opened = []
        changed = []

        def mutate(path):
            if os.fspath(path) == str(self.lease):
                self.lease.chmod(0o644)
                changed.append(True)

        def change(path, flags, *args, **kwargs):
            fd = original(path, flags, *args, **kwargs)
            if os.fspath(path) == str(self.lease):
                opened.append(fd)
                mutate(path)
            return fd

        def path_open(path, *args, **kwargs):
            stream = original_path_open(path, *args, **kwargs)
            if path == self.lease:
                opened.append(stream.fileno())
                mutate(path)
            return stream

        with patch.object(helper.os, "open", side_effect=change), patch.object(
            Path, "open", path_open
        ):
            try:
                self.refused(self.upload)
            finally:
                self.assertEqual(changed, [True], "Permissions must actually change after open")
        self.assertEqual(len(opened), 1)
        with self.assertRaises(OSError):
            os.fstat(opened[0])

    def test_changed_selected_pdf_still_cannot_consume_a_lease(self):
        (self.root / "paper.pdf").write_bytes(self.pdf + b"changed")
        with self.assertRaisesRegex(ValueError, "PDF changed"):
            self.upload()
        self.opener.assert_not_called()

    def test_symlink_replacement_before_open_is_refused(self):
        original = helper.os.open
        target = self.root / "replacement.json"
        self.lease.rename(target)
        self.write_lease()
        changed = []

        def change(path, flags, *args, **kwargs):
            if os.fspath(path) == str(self.lease):
                self.lease.unlink()
                self.lease.symlink_to(target)
                changed.append(True)
            return original(path, flags, *args, **kwargs)

        with patch.object(helper.os, "open", side_effect=change):
            self.refused(self.upload)
        self.assertEqual(changed, [True])

    def test_changes_during_read_are_refused_and_descriptor_closed(self):
        for mutation in ("grow", "shrink", "replace"):
            with self.subTest(mutation=mutation):
                self.write_lease()
                original = helper.os.read
                observed = []

                def read(fd, limit):
                    data = original(fd, limit)
                    observed.append((fd, limit))
                    if mutation == "grow":
                        self.lease.write_bytes(data + b" ")
                    elif mutation == "shrink":
                        self.lease.write_bytes(data[:-1])
                    else:
                        target = self.root / "new-inode.json"
                        target.write_bytes(data)
                        target.chmod(0o600)
                        os.replace(target, self.lease)
                    return data

                with patch.object(helper.os, "read", side_effect=read):
                    self.refused(self.upload)
                self.assertEqual(len(observed), 1)
                self.assertEqual(observed[0][1], 10001)
                with self.assertRaises(OSError):
                    os.fstat(observed[0][0])

    def test_exact_size_limit_remains_usable(self):
        data = self.lease.read_bytes()
        self.lease.write_bytes(data + b" " * (10000 - len(data)))
        self.assertEqual(self.lease.stat().st_size, 10000)
        self.assertEqual(self.upload()["document"]["id"], "synthetic-document")

    def test_malformed_json_closes_descriptor_without_transport(self):
        self.lease.write_bytes(b"{")
        original = helper.os.open
        opened = []

        def record(*args, **kwargs):
            fd = original(*args, **kwargs)
            opened.append(fd)
            return fd

        with patch.object(helper.os, "open", side_effect=record):
            with self.assertRaises(json.JSONDecodeError):
                self.upload()
        self.assertEqual(len(opened), 1)
        with self.assertRaises(OSError):
            os.fstat(opened[0])
        self.opener.assert_not_called()


if __name__ == "__main__":
    unittest.main()
