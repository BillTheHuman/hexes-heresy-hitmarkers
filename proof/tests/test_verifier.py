#!/usr/bin/env python3
"""Adversarial tests for the public proof-capsule verifier."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
TRUSTED_VERIFIER = SOURCE_ROOT / "verify.py"


class VerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="whiteroom-public-proof-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "capsule"
        shutil.copytree(SOURCE_ROOT, self.root, symlinks=True)

    def run_verifier(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TRUSTED_VERIFIER), "--root", str(self.root), "--json"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )

    def assert_valid(self) -> subprocess.CompletedProcess[str]:
        result = self.run_verifier()
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        return result

    def assert_invalid(self, fragment: str) -> subprocess.CompletedProcess[str]:
        result = self.run_verifier()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(fragment, result.stderr)
        return result

    def load_json(self, relative: str) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def write_json(self, relative: str, value: dict) -> None:
        (self.root / relative).write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def refresh_manifest_entry(self, relative: str) -> None:
        data = (self.root / relative).read_bytes()
        manifest = self.load_json("manifest.json")
        entry = next(item for item in manifest["files"] if item["path"] == relative)
        entry["size"] = len(data)
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        self.write_json("manifest.json", manifest)

    def mutate_claim(self, claim_id: str, callback) -> None:
        claims = self.load_json("claims.json")
        claim = next(item for item in claims["claims"] if item["id"] == claim_id)
        callback(claim)
        self.write_json("claims.json", claims)
        self.refresh_manifest_entry("claims.json")

    def test_01_valid_baseline(self) -> None:
        result = self.assert_valid()
        payload = json.loads(result.stdout)
        self.assertEqual(payload["claim_count"], 12)
        self.assertEqual(payload["evidence_count"], 12)
        self.assertEqual(payload["negative_evidence_ids"], ["evidence-graphical-recheck-negative"])

    def test_02_rejects_content_tampering(self) -> None:
        path = self.root / "VERIFYING.md"
        path.write_text(path.read_text(encoding="utf-8") + "\ntampered\n", encoding="utf-8")
        self.assert_invalid("size mismatch")

    def test_03_rejects_extra_file(self) -> None:
        (self.root / "unexpected.txt").write_text("extra", encoding="utf-8")
        self.assert_invalid("file inventory differs")

    def test_04_rejects_missing_file(self) -> None:
        (self.root / "PROOF_FORMAT.md").unlink()
        self.assert_invalid("file inventory differs")

    def test_05_rejects_manifest_path_traversal(self) -> None:
        manifest = self.load_json("manifest.json")
        manifest["files"][0]["path"] = "evidence/../escape.json"
        self.write_json("manifest.json", manifest)
        self.assert_invalid("traversal is forbidden")

    def test_06_rejects_manifest_absolute_path(self) -> None:
        manifest = self.load_json("manifest.json")
        manifest["files"][0]["path"] = "/escape.json"
        self.write_json("manifest.json", manifest)
        self.assert_invalid("absolute path is forbidden")

    def test_07_rejects_symlink_file(self) -> None:
        target = self.root.parent / "outside-claims.json"
        shutil.copy2(self.root / "claims.json", target)
        (self.root / "claims.json").unlink()
        os.symlink(target, self.root / "claims.json")
        self.assert_invalid("symlinks are forbidden")

    def test_08_rejects_symlink_directory(self) -> None:
        target = self.root.parent / "outside-evidence"
        shutil.copytree(self.root / "evidence", target)
        shutil.rmtree(self.root / "evidence")
        os.symlink(target, self.root / "evidence", target_is_directory=True)
        self.assert_invalid("symlinks are forbidden")

    def test_09_rejects_unknown_evidence_reference(self) -> None:
        self.mutate_claim(
            "claim-audio-path-observation",
            lambda claim: claim.__setitem__("evidence_refs", ["evidence-not-present"]),
        )
        self.assert_invalid("unknown evidence id")

    def test_10_rejects_attestation_status_inflation(self) -> None:
        def inflate(claim: dict) -> None:
            claim["status"] = "observed"
            claim["claim_kind"] = "direct_observation"
            claim["scope"] = "exercised_path"

        self.mutate_claim("claim-owner-acceptance-attestation", inflate)
        self.assert_invalid("observed claim requires only observed evidence")

    def test_11_rejects_claim_scope_widening(self) -> None:
        self.mutate_claim(
            "claim-native-path-bounded-inference",
            lambda claim: claim.__setitem__("scope", "exercised_path"),
        )
        self.assert_invalid("claim scope exceeds or differs from evidence scope")

    def test_12_rejects_categorical_claim_overreach(self) -> None:
        self.mutate_claim(
            "claim-graphical-scripted-run-observation",
            lambda claim: claim.__setitem__("statement", "The private implementation is fully playable."),
        )
        self.assert_invalid("forbidden overreach phrase")

    def test_12b_rejects_mapped_entry_translation_overreach(self) -> None:
        self.mutate_claim(
            "claim-build-inventory-observation",
            lambda claim: claim.__setitem__(
                "statement",
                "All mapped entries were translated one for one.",
            ),
        )
        self.assert_invalid("forbidden overreach phrase")

    def test_13_requires_failure_criteria(self) -> None:
        self.mutate_claim(
            "claim-controller-path-observation",
            lambda claim: claim.__setitem__("failure_criteria", []),
        )
        self.assert_invalid("failure_criteria: list must not be empty")

    def test_14_rejects_missing_evidence_file(self) -> None:
        (self.root / "evidence" / "evidence-audio-path.json").unlink()
        self.assert_invalid("file inventory differs")

    def test_15_rejects_negative_run_relabeling(self) -> None:
        relative = "evidence/evidence-graphical-recheck-negative.json"
        record = self.load_json(relative)
        record["evidence"]["record_kind"] = "observation"
        record["evidence"]["scope"] = "exercised_path"
        self.write_json(relative, record)
        self.refresh_manifest_entry(relative)
        manifest = self.load_json("manifest.json")
        manifest["policy"]["required_negative_evidence_ids"] = []
        self.write_json("manifest.json", manifest)
        self.assert_invalid("required_negative_evidence_ids: list must not be empty")

    def test_16_rejects_unreferenced_negative_run(self) -> None:
        self.mutate_claim(
            "claim-graphical-recheck-unresolved",
            lambda claim: claim.__setitem__("evidence_refs", ["evidence-shutdown-ambiguity"]),
        )
        self.assert_invalid("unreferenced evidence ids")

    def test_17_rejects_duplicate_json_key(self) -> None:
        path = self.root / "claims.json"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            '  "format": "whiteroom-claims-v1",',
            '  "format": "whiteroom-claims-v1",\n  "format": "whiteroom-claims-v1",',
            1,
        )
        path.write_text(text, encoding="utf-8")
        self.refresh_manifest_entry("claims.json")
        self.assert_invalid("duplicate key")

    def test_18_rejects_absolute_local_path_leak(self) -> None:
        path = self.root / "VERIFYING.md"
        leaked_path = "/" + "home/example/private"
        path.write_text(
            path.read_text(encoding="utf-8") + f"\nAccidental path: {leaked_path}\n",
            encoding="utf-8",
        )
        self.refresh_manifest_entry("VERIFYING.md")
        self.assert_invalid("absolute local path is forbidden")

    def test_19_rejects_missing_required_evidence_field(self) -> None:
        relative = "evidence/evidence-audio-path.json"
        record = self.load_json(relative)
        del record["evidence"]["summary"]
        self.write_json(relative, record)
        self.refresh_manifest_entry(relative)
        self.assert_invalid("keys differ")

    def test_20_rejects_invalid_evidence_value_type(self) -> None:
        relative = "evidence/evidence-controller-path.json"
        record = self.load_json(relative)
        record["evidence"]["facts"][0]["value"] = ["not", "scalar"]
        self.write_json(relative, record)
        self.refresh_manifest_entry(relative)
        self.assert_invalid("only bool, int, or string is allowed")

    def test_21_rejects_invalid_status_enum(self) -> None:
        relative = "evidence/evidence-audio-path.json"
        record = self.load_json(relative)
        record["evidence"]["status"] = "confirmed"
        self.write_json(relative, record)
        self.refresh_manifest_entry(relative)
        self.assert_invalid("unsupported value")


if __name__ == "__main__":
    unittest.main(verbosity=2)
