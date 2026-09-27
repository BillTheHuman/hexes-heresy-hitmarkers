#!/usr/bin/env python3
"""Verify the complete exported Whiteroom publication inventory and digests."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from typing import Any


MANIFEST_NAME = "release-manifest.json"
SCHEMA = "whiteroom-publication-release/v1"
POLICY = "mapped-allowlist-utf8-text-only"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
PATH_PART_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MIME_BY_SUFFIX = {
    ".cff": "application/yaml",
    ".css": "text/css",
    ".html": "text/html",
    ".js": "text/javascript",
    ".json": "application/json",
    ".md": "text/markdown",
    ".py": "text/x-python",
    ".txt": "text/plain",
    ".yaml": "application/yaml",
    ".yml": "application/yaml",
}
BINARY_PREFIXES = {
    b"\x7fELF": "ELF executable",
    b"MZ": "PE/DOS executable",
    b"PK\x03\x04": "ZIP archive",
    b"PK\x05\x06": "ZIP archive",
    b"PK\x07\x08": "ZIP archive",
    b"\x1f\x8b": "gzip archive",
    b"BZh": "bzip2 archive",
    b"\xfd7zXZ\x00": "xz archive",
    b"7z\xbc\xaf\x27\x1c": "7-Zip archive",
    b"Rar!\x1a\x07": "RAR archive",
    b"%PDF-": "PDF document",
    b"\x89PNG\r\n\x1a\n": "PNG image",
    b"\xff\xd8\xff": "JPEG image",
    b"GIF87a": "GIF image",
    b"GIF89a": "GIF image",
    b"OggS": "Ogg media",
    b"fLaC": "FLAC audio",
    b"ID3": "MP3 audio",
    b"RIFF": "RIFF media",
    b"\x00asm": "WebAssembly binary",
}
MACH_O_MAGICS = {
    b"\xfe\xed\xfa\xce",
    b"\xce\xfa\xed\xfe",
    b"\xfe\xed\xfa\xcf",
    b"\xcf\xfa\xed\xfe",
    b"\xca\xfe\xba\xbe",
    b"\xbe\xba\xfe\xca",
}


class ReleaseVerificationError(ValueError):
    """The exported release failed an integrity check."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseVerificationError(message)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"manifest contains duplicate key {key!r}")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    raise ReleaseVerificationError(f"manifest contains non-finite number {value!r}")


def _load_manifest(data: bytes) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), "manifest UTF-8 BOM is forbidden")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReleaseVerificationError("manifest is not valid UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
            parse_float=lambda raw: (_ for _ in ()).throw(
                ReleaseVerificationError(f"manifest floating-point number is forbidden: {raw}")
            ),
        )
    except ReleaseVerificationError:
        raise
    except json.JSONDecodeError as error:
        raise ReleaseVerificationError(f"manifest is invalid JSON: {error}") from error
    require(isinstance(value, dict), "manifest must be a JSON object")
    require(set(value) == {"schema", "policy", "files"}, "manifest keys differ")
    require(value["schema"] == SCHEMA, "manifest schema is unsupported")
    require(value["policy"] == POLICY, "manifest policy is unsupported")
    require(isinstance(value["files"], list) and value["files"], "manifest files must be nonempty")
    return value


def _safe_path(raw: Any, context: str) -> str:
    require(isinstance(raw, str) and raw, f"{context}: path must be a nonempty string")
    require("\\" not in raw, f"{context}: backslashes are forbidden")
    path = PurePosixPath(raw)
    require(not path.is_absolute(), f"{context}: absolute path is forbidden")
    require(raw == path.as_posix(), f"{context}: path is not canonical")
    require(all(part not in {"", ".", ".."} for part in path.parts), f"{context}: traversal is forbidden")
    require(all(not part.startswith(".") for part in path.parts), f"{context}: hidden path is forbidden")
    require(all(PATH_PART_RE.fullmatch(part) for part in path.parts), f"{context}: unsafe path component")
    require(raw != MANIFEST_NAME, f"{context}: manifest cannot inventory itself")
    return raw


def _inventory(root: Path) -> set[str]:
    try:
        root_stat = root.lstat()
    except OSError as error:
        raise ReleaseVerificationError(f"release root cannot be inspected: {error}") from error
    require(stat.S_ISDIR(root_stat.st_mode), "release root must be a real directory")
    found: set[str] = set()
    stack: list[tuple[Path, PurePosixPath]] = [(root, PurePosixPath("."))]
    while stack:
        directory, relative_directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as error:
            raise ReleaseVerificationError(
                f"cannot scan {relative_directory.as_posix()}: {error}"
            ) from error
        for entry in entries:
            relative = (
                PurePosixPath(entry.name)
                if relative_directory.as_posix() == "."
                else relative_directory / entry.name
            )
            display = relative.as_posix()
            require(not entry.name.startswith("."), f"{display}: hidden entries are forbidden")
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as error:
                raise ReleaseVerificationError(f"cannot inspect {display}: {error}") from error
            require(not stat.S_ISLNK(metadata.st_mode), f"{display}: symlinks are forbidden")
            if stat.S_ISDIR(metadata.st_mode):
                stack.append((Path(entry.path), relative))
            elif stat.S_ISREG(metadata.st_mode):
                found.add(display)
            else:
                raise ReleaseVerificationError(f"{display}: special files are forbidden")
    return found


def _read_regular(path: Path, context: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ReleaseVerificationError(f"{context}: cannot open regular file: {error}") from error
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


def _validate_payload_text(path: str, data: bytes) -> None:
    binary_kind = next(
        (label for prefix, label in BINARY_PREFIXES.items() if data.startswith(prefix)),
        None,
    )
    if binary_kind is None and data[:4] in MACH_O_MAGICS:
        binary_kind = "Mach-O executable"
    if binary_kind is None and len(data) >= 12 and data[4:8] == b"ftyp":
        binary_kind = "ISO base media"
    require(binary_kind is None, f"{path}: binary content ({binary_kind}) is forbidden")
    require(b"\x00" not in data, f"{path}: NUL-containing binary data is forbidden")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ReleaseVerificationError(f"{path}: payload is not valid UTF-8") from error
    require(
        all(ord(character) >= 32 or character in "\t\n\r" for character in text),
        f"{path}: control characters are forbidden",
    )


def verify(root: Path) -> dict[str, Any]:
    inventory = _inventory(root)
    require(MANIFEST_NAME in inventory, f"{MANIFEST_NAME} is missing")
    manifest_bytes = _read_regular(root / MANIFEST_NAME, MANIFEST_NAME)
    manifest = _load_manifest(manifest_bytes)
    paths: list[str] = []
    for index, entry in enumerate(manifest["files"]):
        context = f"files[{index}]"
        require(isinstance(entry, dict), f"{context}: expected object")
        require(set(entry) == {"path", "sha256", "size", "mime"}, f"{context}: keys differ")
        path = _safe_path(entry["path"], f"{context}.path")
        paths.append(path)
        require(type(entry["size"]) is int and entry["size"] >= 0, f"{context}.size: invalid")
        require(isinstance(entry["sha256"], str) and HASH_RE.fullmatch(entry["sha256"]), f"{context}.sha256: invalid")
        require(isinstance(entry["mime"], str) and entry["mime"], f"{context}.mime: invalid")
        suffix = PurePosixPath(path).suffix.lower()
        require(suffix in MIME_BY_SUFFIX, f"{context}.path: file type is not allowlisted")
        require(
            entry["mime"] == MIME_BY_SUFFIX[suffix],
            f"{context}.mime: does not match the path's allowlisted media type",
        )
    require(paths == sorted(paths), "manifest file entries are not path-sorted")
    require(len(paths) == len(set(paths)), "manifest contains duplicate paths")
    expected = {MANIFEST_NAME, *paths}
    require(
        inventory == expected,
        f"release inventory differs; missing={sorted(expected - inventory)}, extra={sorted(inventory - expected)}",
    )
    for index, entry in enumerate(manifest["files"]):
        path = entry["path"]
        data = _read_regular(root / PurePosixPath(path), path)
        require(len(data) == entry["size"], f"{path}: size mismatch")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"{path}: SHA-256 mismatch")
        _validate_payload_text(path, data)
    return {
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "file_count": len(inventory),
        "payload_file_count": len(paths),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).absolute().parent,
        help="exported release root (defaults to this script's directory)",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = verify(args.root)
    except ReleaseVerificationError as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"valid": True, **result}, sort_keys=True, separators=(",", ":")))
    else:
        print("VALID: complete Whiteroom publication export")
        print(f"Manifest SHA-256: {result['manifest_sha256']}")
        print(f"Files: {result['file_count']} ({result['payload_file_count']} payload files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
