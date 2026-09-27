# Verifying the complete Hexes, Heresy & Hitmarkers release

Release 1.0.0 has two verification layers with different meanings.

## Use a downloaded source archive, not a Git clone

For complete-release verification, download the source archive for the exact
release from
[github.com/BillTheHuman/hexes-heresy-hitmarkers](https://github.com/BillTheHuman/hexes-heresy-hitmarkers),
extract it, and run the commands below from the extracted repository root.

Do not run the outer verifier directly in an ordinary Git clone. The outer
verifier intentionally rejects hidden or unexpected entries, including the
clone's `.git` directory, because the downloadable release is defined by an
exact file inventory. A rejection caused by `.git` does not say that the
tracked files were altered; it says that a clone is not the archive-shaped
input this check accepts.

## 1. Complete-release integrity

From the exported repository root, run:

```sh
python3 verify_release.py
```

This checks that `release-manifest.json` has the expected format, that its paths
are canonical and safe, that the export contains exactly the listed regular
files and no symbolic links or hidden entries, and that every listed byte size
and SHA-256 digest matches. It detects an added, removed, or altered report,
site, proof, or policy file.

Run its focused tests with bytecode creation disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 release_tests/test_release_verifier.py
```

## 2. Proof-capsule semantics

Then run:

```sh
python3 proof/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 proof/tests/test_verifier.py
```

The proof verifier checks the stricter claim and evidence model inside `proof/`:
status and scope compatibility, evidence references, contradiction conditions,
negative-run preservation, schema rules, and categorical-overclaim guards.

## What success means

Passing both layers establishes the exported bytes' integrity and the published
records' conformance to their encoded rules. It does not authenticate withheld
telemetry, prove a participant attestation, reproduce private execution,
establish audiovisual fidelity, or provide legal clearance. The release has
not been independently replicated and did not receive independent legal
review. A digest proves which bytes were checked, not whether an underlying
event occurred.
