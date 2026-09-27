# Verifying the Hexes, Heresy & Hitmarkers proof capsule

## Requirements

- Python 3.10 or newer
- no third-party packages
- a filesystem that reports symbolic links and regular-file types normally

Run from the capsule root:

```sh
python3 verify.py
```

This command verifies only the `proof/` capsule. To verify the complete GitHub
release, follow [`../RELEASE_VERIFYING.md`](../RELEASE_VERIFYING.md) and use a
downloaded source archive for the exact release. The complete-release verifier
deliberately rejects an ordinary clone's `.git` directory as an unexpected
hidden entry.

For machine-readable output:

```sh
python3 verify.py --json
```

The verifier exits with status zero only after all inventory, digest, schema,
status, scope, reference, falsifiability, and negative-run rules pass. It prints
the exact manifest digest on success. Record that digest separately when
identifying a release.

To verify a copied capsule from elsewhere without executing its copied
verifier, invoke a trusted local copy and name the other root:

```sh
python3 verify.py --root path/to/copied-capsule
```

This protects against the obvious mistake of trusting a verifier that an
untrusted package changed along with its data. A high-assurance reviewer should
also inspect `verify.py`, run the tests, and compare the verifier itself to a
separately recorded manifest commitment.

## Test suite

Run the test file directly so Python does not create bytecode-cache files in
the strict package inventory:

```sh
python3 tests/test_verifier.py
```

The 22-case suite copies the complete capsule to temporary directories and
checks the valid baseline plus failures for content tampering, unexpected and
missing files, path traversal, absolute paths, symlinks, missing evidence,
unknown references, status inflation, scope widening, categorical claim
overreach, duplicate JSON keys, required-field, value-type, and enum violations,
and suppression or relabeling of the required negative run. Tests that target
semantics update the altered file's manifest size and digest first,
demonstrating that content hashing alone does not enforce the evidence model.

If another tool has created `__pycache__` below the capsule, verification will
reject it as an unexpected file. Remove only that generated cache after
confirming its exact path, or test a fresh archive. Strict inventory is a
feature: nothing is silently ignored.

## Reading a successful result

Success means the package is internally intact and conforms to its declared
proof format. It does not authenticate the withheld private logs, validate the
participant's attestations, establish that an AI-assisted live observation was
correct, reproduce private execution, or provide legal advice.

The release has not been independently replicated or independently reviewed by
legal counsel. Verification does not supply legal clearance.

The public records are nevertheless falsifiable. Each claim lists concrete
conditions that would contradict or resolve it, and the required adverse run is
preserved rather than removed from the evidence set. See `PROOF_FORMAT.md` for
the exact schema and epistemic boundary.
