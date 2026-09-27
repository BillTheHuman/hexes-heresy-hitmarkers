#!/usr/bin/env python3
"""Verify the Whiteroom public proof capsule using only the Python standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


MANIFEST_NAME = "manifest.json"
FORMAT_MANIFEST = "whiteroom-proof-manifest-v1"
FORMAT_CLAIMS = "whiteroom-claims-v1"
FORMAT_EVIDENCE = "whiteroom-evidence-v1"
PACKAGE_NAME = "whiteroom-public-proof-capsule"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^(?:claim|evidence)-[a-z0-9]+(?:-[a-z0-9]+)*$")
DISPLAY_ID_RE = re.compile(r"^C-[0-9]{3}$")
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
PATH_PART_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
LONG_HEX_RE = re.compile(r"(?i)(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
LONG_BASE64_RE = re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{120,}={0,2}(?![A-Za-z0-9+/])")
LOCAL_PATH_RE = re.compile(r"(?i)(?:/(?:home|users|run/media|mnt)/|[A-Z]:\\\\Users\\\\)")

ALLOWED_STATUSES = ("observed", "attested", "inference", "unresolved")
ALLOWED_SCOPES = (
    "exact_run",
    "exercised_path",
    "examined_configuration",
    "participant_report",
    "unresolved_question",
)
ALLOWED_SOURCE_TYPES = (
    "instrumented_record",
    "inspection_record",
    "participant_attestation",
    "ai_live_observation",
    "process_record",
    "analytical_synthesis",
    "unresolved_record",
)
ALLOWED_RECORD_KINDS = (
    "positive_run",
    "negative_run",
    "inspection",
    "attestation",
    "observation",
    "unresolved_event",
)
ALLOWED_FACT_UNITS = ("boolean", "count", "label", "status")
ALLOWED_ROLES = ("claims", "documentation", "evidence", "schema", "test", "verifier")

STATUS_SOURCE_RULES = {
    "observed": {
        "instrumented_record",
        "inspection_record",
        "ai_live_observation",
        "process_record",
    },
    "attested": {"participant_attestation"},
    "inference": {"analytical_synthesis"},
    "unresolved": {"unresolved_record"},
}
STATUS_KIND_RULES = {
    "observed": {"direct_observation", "adverse_observation"},
    "attested": {"participant_attestation"},
    "inference": {"bounded_inference"},
    "unresolved": {"unresolved_question"},
}
STATUS_SCOPE_RULES = {
    "observed": {"exact_run", "exercised_path", "examined_configuration"},
    "attested": {"participant_report"},
    "inference": {"exercised_path", "examined_configuration"},
    "unresolved": {"unresolved_question"},
}
OVERREACH_PATTERNS = {
    "fully playable": re.compile(r"\bfully[ -]playable\b", re.IGNORECASE),
    "complete fidelity": re.compile(r"\bcomplete[ -]fidelity\b", re.IGNORECASE),
    "defect-free": re.compile(r"\bdefect[ -]free\b", re.IGNORECASE),
    "legal port": re.compile(r"\blegal[ -]port\b", re.IGNORECASE),
    "legal clearance": re.compile(r"\blegally[ -]clear(?:ed|ance)\b", re.IGNORECASE),
    "no emulation": re.compile(r"\bno[ -]emulation\b", re.IGNORECASE),
    "clean-room conclusion": re.compile(r"\bclean[ -]room(?:ed)?\b", re.IGNORECASE),
    "independent reproduction": re.compile(
        r"\bindependent(?:ly)?[ -](?:reproduced|replicated|reproduction|replication)\b",
        re.IGNORECASE,
    ),
    "one-to-one translation": re.compile(r"\bone[ -]to[ -]one[ -]translat(?:ed|ion)\b", re.IGNORECASE),
    "mapped-entry one-for-one translation": re.compile(
        r"\bmapped entries\b[^.]{0,100}\b(?:translated|generated)\b[^.]{0,40}\bone[ -](?:to|for)[ -]one\b",
        re.IGNORECASE,
    ),
}


class VerificationError(Exception):
    """A deterministic package-verification failure."""


def fail(message: str) -> None:
    raise VerificationError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    require(not missing and not extra, f"{context}: keys differ; missing={missing}, extra={extra}")


def require_string(value: Any, context: str, *, nonempty: bool = True, max_length: int = 4000) -> str:
    require(isinstance(value, str), f"{context}: expected string")
    require(len(value) <= max_length, f"{context}: string is too long")
    if nonempty:
        require(bool(value.strip()), f"{context}: string must not be blank")
    require("\x00" not in value, f"{context}: NUL is forbidden")
    return value


def require_string_list(
    value: Any,
    context: str,
    *,
    nonempty: bool = True,
    sorted_unique: bool = False,
) -> list[str]:
    require(isinstance(value, list), f"{context}: expected list")
    if nonempty:
        require(bool(value), f"{context}: list must not be empty")
    result = [require_string(item, f"{context}[{index}]") for index, item in enumerate(value)]
    require(len(result) == len(set(result)), f"{context}: duplicate values are forbidden")
    if sorted_unique:
        require(result == sorted(result), f"{context}: values must be sorted")
    return result


def reject_constant(value: str) -> None:
    fail(f"JSON constant {value!r} is forbidden")


def reject_float(value: str) -> None:
    fail(f"JSON floating-point value {value!r} is forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"JSON object contains duplicate key {key!r}")
        result[key] = value
    return result


def load_json_bytes(data: bytes, context: str) -> Any:
    require(not data.startswith(b"\xef\xbb\xbf"), f"{context}: UTF-8 BOM is forbidden")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{context}: not valid UTF-8: {exc}")
    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=reject_float,
        )
    except VerificationError:
        raise
    except json.JSONDecodeError as exc:
        fail(f"{context}: invalid JSON: {exc}")


def safe_relative_path(raw: Any, context: str) -> str:
    path = require_string(raw, context, max_length=240)
    require("\\" not in path, f"{context}: backslashes are forbidden")
    pure = PurePosixPath(path)
    require(not pure.is_absolute(), f"{context}: absolute path is forbidden")
    require(path == pure.as_posix(), f"{context}: path is not canonical POSIX form")
    require(bool(pure.parts), f"{context}: empty path is forbidden")
    require(all(part not in ("", ".", "..") for part in pure.parts), f"{context}: traversal is forbidden")
    require(all(PATH_PART_RE.fullmatch(part) for part in pure.parts), f"{context}: unsafe path component")
    require(path != MANIFEST_NAME, f"{context}: manifest cannot hash itself")
    return path


def open_regular_nofollow(path: Path, context: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        fail(f"{context}: cannot open regular no-follow file: {exc}")
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode), f"{context}: not a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            f"{context}: file changed while being read",
        )
        data = b"".join(chunks)
        require(len(data) == before.st_size, f"{context}: short read")
        return data
    finally:
        os.close(descriptor)


def inventory(root: Path) -> set[str]:
    try:
        root_stat = root.lstat()
    except OSError as exc:
        fail(f"package root cannot be inspected: {exc}")
    require(stat.S_ISDIR(root_stat.st_mode), "package root must be a real directory, not a symlink")
    found: set[str] = set()
    stack: list[tuple[Path, PurePosixPath]] = [(root, PurePosixPath("."))]
    while stack:
        directory, relative_directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as exc:
            fail(f"cannot scan {relative_directory.as_posix()}: {exc}")
        for entry in entries:
            relative = (
                PurePosixPath(entry.name)
                if relative_directory.as_posix() == "."
                else relative_directory / entry.name
            )
            display = relative.as_posix()
            try:
                entry_stat = entry.stat(follow_symlinks=False)
            except OSError as exc:
                fail(f"cannot inspect {display}: {exc}")
            require(not stat.S_ISLNK(entry_stat.st_mode), f"{display}: symlinks are forbidden")
            if stat.S_ISDIR(entry_stat.st_mode):
                stack.append((Path(entry.path), relative))
            elif stat.S_ISREG(entry_stat.st_mode):
                found.add(display)
            else:
                fail(f"{display}: only regular files and directories are allowed")
    return found


def validate_manifest(value: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(isinstance(value, dict), "manifest: expected object")
    exact_keys(
        value,
        {"format", "package", "version", "hash_algorithm", "files", "policy"},
        "manifest",
    )
    require(value["format"] == FORMAT_MANIFEST, "manifest.format: unsupported value")
    require(value["package"] == PACKAGE_NAME, "manifest.package: unsupported value")
    require(value["version"] == 1, "manifest.version: expected integer 1")
    require(value["hash_algorithm"] == "sha256", "manifest.hash_algorithm: expected sha256")
    files = value["files"]
    require(isinstance(files, list) and files, "manifest.files: expected nonempty list")
    paths: list[str] = []
    for index, entry in enumerate(files):
        context = f"manifest.files[{index}]"
        require(isinstance(entry, dict), f"{context}: expected object")
        exact_keys(entry, {"path", "role", "size", "sha256"}, context)
        path = safe_relative_path(entry["path"], f"{context}.path")
        paths.append(path)
        require(entry["role"] in ALLOWED_ROLES, f"{context}.role: unsupported role")
        require(type(entry["size"]) is int and entry["size"] >= 0, f"{context}.size: expected nonnegative integer")
        require(isinstance(entry["sha256"], str) and HASH_RE.fullmatch(entry["sha256"]), f"{context}.sha256: invalid digest")
        suffix = PurePosixPath(path).suffix
        require(suffix in {".json", ".md", ".py"}, f"{context}.path: unsupported public file type")
        role = entry["role"]
        if role == "evidence":
            require(path.startswith("evidence/") and suffix == ".json", f"{context}: evidence role/path mismatch")
        elif role == "claims":
            require(path == "claims.json", f"{context}: claims role/path mismatch")
        elif role == "verifier":
            require(path == "verify.py", f"{context}: verifier role/path mismatch")
        elif role == "test":
            require(path.startswith("tests/") and suffix == ".py", f"{context}: test role/path mismatch")
        elif role == "schema":
            require(path.startswith("schema/") and suffix == ".json", f"{context}: schema role/path mismatch")
        elif role == "documentation":
            require(suffix == ".md", f"{context}: documentation must be Markdown")
    require(paths == sorted(paths), "manifest.files: entries must be path-sorted")
    require(len(paths) == len(set(paths)), "manifest.files: duplicate path")
    required_core = {
        "PROOF_FORMAT.md",
        "VERIFYING.md",
        "claims.json",
        "schema/claims.schema.json",
        "schema/evidence.schema.json",
        "schema/manifest.schema.json",
        "tests/test_verifier.py",
        "verify.py",
    }
    require(required_core.issubset(paths), f"manifest.files: missing core files {sorted(required_core - set(paths))}")

    policy = value["policy"]
    require(isinstance(policy, dict), "manifest.policy: expected object")
    exact_keys(
        policy,
        {
            "claims_file",
            "evidence_directory",
            "required_claim_ids",
            "required_evidence_ids",
            "required_negative_evidence_ids",
            "allowed_statuses",
            "allow_symlinks",
        },
        "manifest.policy",
    )
    require(policy["claims_file"] == "claims.json", "manifest.policy.claims_file: expected claims.json")
    require(policy["evidence_directory"] == "evidence", "manifest.policy.evidence_directory: expected evidence")
    for key in ("required_claim_ids", "required_evidence_ids", "required_negative_evidence_ids"):
        values = require_string_list(policy[key], f"manifest.policy.{key}", sorted_unique=True)
        require(all(ID_RE.fullmatch(item) for item in values), f"manifest.policy.{key}: invalid identifier")
    statuses = require_string_list(policy["allowed_statuses"], "manifest.policy.allowed_statuses", sorted_unique=True)
    require(statuses == sorted(ALLOWED_STATUSES), "manifest.policy.allowed_statuses: status vocabulary changed")
    require(policy["allow_symlinks"] is False, "manifest.policy.allow_symlinks: must be false")
    return files, policy


def scan_public_text(path: str, data: bytes) -> None:
    require(b"\x00" not in data, f"{path}: NUL byte is forbidden")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path}: not valid UTF-8: {exc}")
    require(not LOCAL_PATH_RE.search(text), f"{path}: apparent absolute local path is forbidden")
    require(not LONG_BASE64_RE.search(text), f"{path}: long encoded-looking string is forbidden")
    if path != MANIFEST_NAME:
        require(not LONG_HEX_RE.search(text), f"{path}: standalone SHA-256-length value is forbidden")


def validate_evidence(value: Any, path: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{path}: expected object")
    exact_keys(value, {"format", "evidence"}, path)
    require(value["format"] == FORMAT_EVIDENCE, f"{path}.format: unsupported value")
    evidence = value["evidence"]
    require(isinstance(evidence, dict), f"{path}.evidence: expected object")
    exact_keys(
        evidence,
        {
            "id",
            "status",
            "source_type",
            "scope",
            "record_kind",
            "summary",
            "facts",
            "retention",
            "limitations",
        },
        f"{path}.evidence",
    )
    identifier = require_string(evidence["id"], f"{path}.evidence.id")
    require(ID_RE.fullmatch(identifier) is not None and identifier.startswith("evidence-"), f"{path}.evidence.id: invalid")
    require(path == f"evidence/{identifier}.json", f"{path}: filename must match evidence id")
    status = evidence["status"]
    source_type = evidence["source_type"]
    scope = evidence["scope"]
    record_kind = evidence["record_kind"]
    require(status in ALLOWED_STATUSES, f"{path}.evidence.status: unsupported value")
    require(source_type in ALLOWED_SOURCE_TYPES, f"{path}.evidence.source_type: unsupported value")
    require(source_type in STATUS_SOURCE_RULES[status], f"{path}: status/source_type mismatch")
    require(scope in ALLOWED_SCOPES, f"{path}.evidence.scope: unsupported value")
    require(record_kind in ALLOWED_RECORD_KINDS, f"{path}.evidence.record_kind: unsupported value")
    if status == "attested":
        require(scope == "participant_report" and record_kind == "attestation", f"{path}: invalid attestation semantics")
    if status == "inference":
        require(record_kind == "observation", f"{path}: inference records must use observation kind")
    if status == "unresolved":
        require(scope == "unresolved_question" and record_kind == "unresolved_event", f"{path}: invalid unresolved semantics")
    if record_kind == "negative_run":
        require(status == "observed" and scope == "unresolved_question", f"{path}: negative run must be an observed unresolved-question record")
    require_string(evidence["summary"], f"{path}.evidence.summary", max_length=1200)
    facts = evidence["facts"]
    require(isinstance(facts, list) and facts, f"{path}.evidence.facts: expected nonempty list")
    names: list[str] = []
    for index, fact in enumerate(facts):
        context = f"{path}.evidence.facts[{index}]"
        require(isinstance(fact, dict), f"{context}: expected object")
        exact_keys(fact, {"name", "value", "unit"}, context)
        name = require_string(fact["name"], f"{context}.name")
        require(NAME_RE.fullmatch(name) is not None, f"{context}.name: invalid")
        names.append(name)
        unit = fact["unit"]
        require(unit in ALLOWED_FACT_UNITS, f"{context}.unit: unsupported value")
        item = fact["value"]
        require(type(item) in (bool, int, str), f"{context}.value: only bool, int, or string is allowed")
        if type(item) is int:
            require(0 <= item <= 2**63 - 1, f"{context}.value: integer outside allowed range")
        elif type(item) is str:
            require_string(item, f"{context}.value", max_length=300)
        if unit == "boolean":
            require(type(item) is bool, f"{context}: boolean unit requires bool value")
        elif unit == "count":
            require(type(item) is int, f"{context}: count unit requires int value")
        else:
            require(type(item) is str, f"{context}: label/status unit requires string value")
    require(len(names) == len(set(names)), f"{path}.evidence.facts: duplicate names")
    retention = evidence["retention"]
    require(isinstance(retention, dict), f"{path}.evidence.retention: expected object")
    exact_keys(retention, {"public_record", "underlying_material_public", "limitation"}, f"{path}.evidence.retention")
    require(retention["public_record"] in {"sanitized_summary", "sanitized_transcription"}, f"{path}.evidence.retention.public_record: unsupported value")
    require(retention["underlying_material_public"] is False, f"{path}: underlying private material must not be marked public")
    require_string(retention["limitation"], f"{path}.evidence.retention.limitation", max_length=900)
    require_string_list(evidence["limitations"], f"{path}.evidence.limitations")
    return evidence


def validate_claims(value: Any, evidence_by_id: dict[str, dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    require(isinstance(value, dict), "claims.json: expected object")
    exact_keys(value, {"format", "disclosure", "claims"}, "claims.json")
    require(value["format"] == FORMAT_CLAIMS, "claims.json.format: unsupported value")
    require_string(value["disclosure"], "claims.json.disclosure", max_length=1600)
    claims = value["claims"]
    require(isinstance(claims, list) and claims, "claims.json.claims: expected nonempty list")
    claim_ids: list[str] = []
    referenced: set[str] = set()
    negative_references: set[str] = set()
    for index, claim in enumerate(claims):
        context = f"claims.json.claims[{index}]"
        require(isinstance(claim, dict), f"{context}: expected object")
        exact_keys(
            claim,
            {
                "id",
                "display_id",
                "status",
                "claim_kind",
                "scope",
                "statement",
                "evidence_refs",
                "failure_criteria",
                "limitations",
            },
            context,
        )
        identifier = require_string(claim["id"], f"{context}.id")
        require(ID_RE.fullmatch(identifier) is not None and identifier.startswith("claim-"), f"{context}.id: invalid")
        claim_ids.append(identifier)
        display_id = require_string(claim["display_id"], f"{context}.display_id")
        require(DISPLAY_ID_RE.fullmatch(display_id) is not None, f"{context}.display_id: invalid")
        status = claim["status"]
        scope = claim["scope"]
        claim_kind = claim["claim_kind"]
        require(status in ALLOWED_STATUSES, f"{context}.status: unsupported value")
        require(claim_kind in STATUS_KIND_RULES[status], f"{context}: status/claim_kind mismatch")
        require(scope in STATUS_SCOPE_RULES[status], f"{context}: status/scope mismatch")
        statement = require_string(claim["statement"], f"{context}.statement", max_length=1200)
        for label, pattern in OVERREACH_PATTERNS.items():
            require(not pattern.search(statement), f"{context}.statement: forbidden overreach phrase ({label})")
        refs = require_string_list(claim["evidence_refs"], f"{context}.evidence_refs", sorted_unique=True)
        require(all(ref in evidence_by_id for ref in refs), f"{context}.evidence_refs: unknown evidence id")
        referenced.update(refs)
        ref_records = [evidence_by_id[ref] for ref in refs]
        if status == "observed":
            require(all(item["status"] == "observed" for item in ref_records), f"{context}: observed claim requires only observed evidence")
            require(all(item["record_kind"] not in {"negative_run", "unresolved_event"} for item in ref_records), f"{context}: adverse or unresolved record cannot support positive observed claim")
        elif status == "attested":
            require(all(item["status"] == "attested" for item in ref_records), f"{context}: attested claim requires only attested evidence")
        elif status == "inference":
            require(all(item["status"] in {"observed", "attested"} for item in ref_records), f"{context}: inference basis must be observation or attestation")
            require(any(item["status"] == "observed" for item in ref_records), f"{context}: inference requires observed evidence")
            require(all(item["record_kind"] not in {"negative_run", "unresolved_event"} for item in ref_records), f"{context}: unresolved evidence cannot support affirmative inference")
        elif status == "unresolved":
            require(all(item["record_kind"] in {"negative_run", "unresolved_event"} for item in ref_records), f"{context}: unresolved claim requires negative-run or unresolved-event evidence")
            require(any(item["record_kind"] in {"negative_run", "unresolved_event"} for item in ref_records), f"{context}: unresolved claim lacks an adverse basis")
            negative_references.update(item["id"] for item in ref_records if item["record_kind"] == "negative_run")
        require(all(item["scope"] == scope for item in ref_records), f"{context}: claim scope exceeds or differs from evidence scope")
        require_string_list(claim["failure_criteria"], f"{context}.failure_criteria")
        require_string_list(claim["limitations"], f"{context}.limitations")
    require(claim_ids == sorted(claim_ids), "claims.json.claims: claims must be id-sorted")
    require(len(claim_ids) == len(set(claim_ids)), "claims.json.claims: duplicate id")
    display_ids = [claim["display_id"] for claim in claims]
    require(len(display_ids) == len(set(display_ids)), "claims.json.claims: duplicate display_id")
    expected_display_ids = {f"C-{index:03d}" for index in range(1, len(claims) + 1)}
    require(set(display_ids) == expected_display_ids, "claims.json.claims: display ids must form a complete C-001 sequence")
    required_claims = set(policy["required_claim_ids"])
    require(set(claim_ids) == required_claims, "claims.json: claim ids differ from manifest policy")
    require(referenced == set(evidence_by_id), f"claims.json: unreferenced evidence ids {sorted(set(evidence_by_id) - referenced)}")
    required_negative = set(policy["required_negative_evidence_ids"])
    actual_negative = {item["id"] for item in evidence_by_id.values() if item["record_kind"] == "negative_run"}
    require(actual_negative == required_negative, "negative-run inventory differs from manifest policy")
    require(actual_negative.issubset(negative_references), "a required negative run is not preserved by an unresolved claim")
    return claims


def verify(root: Path) -> dict[str, Any]:
    actual_inventory = inventory(root)
    require(MANIFEST_NAME in actual_inventory, "manifest.json is missing")
    manifest_bytes = open_regular_nofollow(root / MANIFEST_NAME, MANIFEST_NAME)
    scan_public_text(MANIFEST_NAME, manifest_bytes)
    manifest = load_json_bytes(manifest_bytes, MANIFEST_NAME)
    file_entries, policy = validate_manifest(manifest)
    expected_inventory = {MANIFEST_NAME, *(entry["path"] for entry in file_entries)}
    extra = sorted(actual_inventory - expected_inventory)
    missing = sorted(expected_inventory - actual_inventory)
    require(not extra and not missing, f"file inventory differs; missing={missing}, extra={extra}")

    bytes_by_path: dict[str, bytes] = {}
    for entry in file_entries:
        path = entry["path"]
        data = open_regular_nofollow(root / PurePosixPath(path), path)
        require(len(data) == entry["size"], f"{path}: size mismatch")
        digest = hashlib.sha256(data).hexdigest()
        require(digest == entry["sha256"], f"{path}: SHA-256 mismatch")
        scan_public_text(path, data)
        bytes_by_path[path] = data

    evidence_entries = [entry for entry in file_entries if entry["role"] == "evidence"]
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for entry in evidence_entries:
        path = entry["path"]
        evidence = validate_evidence(load_json_bytes(bytes_by_path[path], path), path)
        require(evidence["id"] not in evidence_by_id, f"{path}: duplicate evidence id")
        evidence_by_id[evidence["id"]] = evidence
    require(set(evidence_by_id) == set(policy["required_evidence_ids"]), "evidence ids differ from manifest policy")
    claims = validate_claims(load_json_bytes(bytes_by_path["claims.json"], "claims.json"), evidence_by_id, policy)
    return {
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "file_count": len(actual_inventory),
        "evidence_count": len(evidence_by_id),
        "claim_count": len(claims),
        "evidence_statuses": dict(sorted(Counter(item["status"] for item in evidence_by_id.values()).items())),
        "claim_statuses": dict(sorted(Counter(item["status"] for item in claims).items())),
        "negative_evidence_ids": sorted(
            item["id"] for item in evidence_by_id.values() if item["record_kind"] == "negative_run"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).absolute().parent,
        help="proof-capsule root (defaults to this script's directory)",
    )
    parser.add_argument("--json", action="store_true", help="emit the successful result as JSON")
    args = parser.parse_args(argv)
    try:
        result = verify(args.root)
    except VerificationError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"valid": True, **result}, sort_keys=True, separators=(",", ":")))
    else:
        print("VALID: Whiteroom public proof capsule")
        print(f"Manifest SHA-256: {result['manifest_sha256']}")
        print(f"Files: {result['file_count']}; evidence records: {result['evidence_count']}; claims: {result['claim_count']}")
        print(f"Evidence statuses: {result['evidence_statuses']}")
        print(f"Claim statuses: {result['claim_statuses']}")
        print(f"Preserved negative runs: {result['negative_evidence_ids']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
