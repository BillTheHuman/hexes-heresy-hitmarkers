#!/usr/bin/env python3
"""Tests for the complete-publication release verifier."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT))

from verify_release import MANIFEST_NAME, POLICY, SCHEMA, ReleaseVerificationError, verify


class ReleaseVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="whiteroom-release-verify-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "release"
        self.root.mkdir()
        self.write("README.md", b"# Public report\n")
        self.write("proof/claims.json", b'{"claims":[]}\n')
        self.regenerate_manifest()

    def write(self, relative: str, data: bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def regenerate_manifest(self) -> None:
        mime_by_suffix = {
            ".cff": "application/yaml",
            ".json": "application/json",
            ".md": "text/markdown",
        }
        entries = []
        for path in sorted(
            item for item in self.root.rglob("*") if item.is_file() and item.name != MANIFEST_NAME
        ):
            data = path.read_bytes()
            relative = path.relative_to(self.root).as_posix()
            entries.append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                    "mime": mime_by_suffix.get(path.suffix, "application/octet-stream"),
                }
            )
        self.write(
            MANIFEST_NAME,
            (json.dumps({"schema": SCHEMA, "policy": POLICY, "files": entries}, indent=2, sort_keys=True) + "\n").encode(),
        )

    def assert_invalid(self, fragment: str) -> None:
        with self.assertRaises(ReleaseVerificationError) as caught:
            verify(self.root)
        self.assertIn(fragment, str(caught.exception))

    def test_valid_release(self) -> None:
        result = verify(self.root)
        self.assertEqual(result["file_count"], 3)
        self.assertEqual(result["payload_file_count"], 2)

    def test_accepts_citation_cff_with_yaml_mime(self) -> None:
        self.write(
            "CITATION.cff",
            b'cff-version: 1.2.0\nmessage: "Please cite this release."\n',
        )
        self.regenerate_manifest()

        manifest = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        citation_entry = next(
            entry for entry in manifest["files"] if entry["path"] == "CITATION.cff"
        )
        self.assertEqual(citation_entry["mime"], "application/yaml")
        result = verify(self.root)
        self.assertEqual(result["file_count"], 4)
        self.assertEqual(result["payload_file_count"], 3)

    def test_rejects_citation_cff_with_non_yaml_mime(self) -> None:
        self.write(
            "CITATION.cff",
            b'cff-version: 1.2.0\nmessage: "Please cite this release."\n',
        )
        self.regenerate_manifest()
        manifest = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        citation_entry = next(
            entry for entry in manifest["files"] if entry["path"] == "CITATION.cff"
        )
        citation_entry["mime"] = "text/markdown"
        self.write(MANIFEST_NAME, (json.dumps(manifest) + "\n").encode())

        self.assert_invalid("does not match")

    def test_rejects_content_tampering(self) -> None:
        self.write("README.md", b"changed\n")
        self.assert_invalid("size mismatch")

    def test_rejects_extra_and_missing_files(self) -> None:
        self.write("extra.txt", b"extra\n")
        self.assert_invalid("inventory differs")
        (self.root / "extra.txt").unlink()
        (self.root / "README.md").unlink()
        self.assert_invalid("inventory differs")

    def test_rejects_symlink_and_hidden_entry(self) -> None:
        outside = Path(self.temporary.name) / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        (self.root / "linked.txt").symlink_to(outside)
        self.assert_invalid("symlinks")
        (self.root / "linked.txt").unlink()
        self.write(".hidden", b"hidden\n")
        self.assert_invalid("hidden")

    def test_rejects_path_traversal_and_absolute_path(self) -> None:
        manifest = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        for unsafe in ("../outside.txt", "/outside.txt", "proof/../README.md"):
            with self.subTest(path=unsafe):
                changed = json.loads(json.dumps(manifest))
                changed["files"][0]["path"] = unsafe
                self.write(MANIFEST_NAME, (json.dumps(changed) + "\n").encode())
                expected = "absolute" if unsafe.startswith("/") else "traversal"
                self.assert_invalid(expected)

    def test_rejects_duplicate_manifest_key(self) -> None:
        self.write(
            MANIFEST_NAME,
            b'{"schema":"whiteroom-publication-release/v1","schema":"duplicate","policy":"mapped-allowlist-utf8-text-only","files":[]}\n',
        )
        self.assert_invalid("duplicate key")

    def test_rejects_wrong_schema_policy_and_digest(self) -> None:
        original = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        cases = (("schema", "other", "schema"), ("policy", "other", "policy"))
        for key, value, expected in cases:
            with self.subTest(key=key):
                changed = json.loads(json.dumps(original))
                changed[key] = value
                self.write(MANIFEST_NAME, (json.dumps(changed) + "\n").encode())
                self.assert_invalid(expected)
        changed = json.loads(json.dumps(original))
        changed["files"][0]["sha256"] = "a" * 64
        self.write(MANIFEST_NAME, (json.dumps(changed) + "\n").encode())
        self.assert_invalid("SHA-256 mismatch")

    def test_rejects_unsorted_and_duplicate_paths(self) -> None:
        manifest = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        manifest["files"].reverse()
        self.write(MANIFEST_NAME, (json.dumps(manifest) + "\n").encode())
        self.assert_invalid("path-sorted")
        self.regenerate_manifest()
        manifest = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        manifest["files"].append(dict(manifest["files"][0]))
        manifest["files"].sort(key=lambda entry: entry["path"])
        self.write(MANIFEST_NAME, (json.dumps(manifest) + "\n").encode())
        self.assert_invalid("duplicate paths")

    def test_rejects_nonallowlisted_file_type(self) -> None:
        self.write("payload.bin", b"plain-looking bytes\n")
        self.regenerate_manifest()
        self.assert_invalid("file type is not allowlisted")

    def test_rejects_invalid_utf8_and_nul(self) -> None:
        self.write("README.md", b"\xff\xfe\n")
        self.regenerate_manifest()
        self.assert_invalid("not valid UTF-8")
        self.write("README.md", b"text\x00data\n")
        self.regenerate_manifest()
        self.assert_invalid("NUL-containing")

    def test_rejects_disguised_binary_content(self) -> None:
        self.write("README.md", b"%PDF-1.7\n")
        self.regenerate_manifest()
        self.assert_invalid("binary content")

    def test_rejects_mime_mismatch(self) -> None:
        manifest = json.loads((self.root / MANIFEST_NAME).read_text(encoding="utf-8"))
        manifest["files"][0]["mime"] = "application/octet-stream"
        self.write(MANIFEST_NAME, (json.dumps(manifest) + "\n").encode())
        self.assert_invalid("does not match")


if __name__ == "__main__":
    unittest.main()
