# Research and publication protocol

**Status: descriptive protocol for the public release, not a recipe for
reconstructing the private implementation.**

This document explains how the project separated private technical work from a
publicly auditable report. It intentionally omits protected inputs, translated
material, operational circumvention details, and private implementation paths.

## 1. Scope and participant representations

The participant defined a narrow research question: could program behavior from
an owned-cartridge input, as represented by the participant, be translated
ahead of time and exercised on a modern Linux host?

The participant attested to owning the physical cartridge and characterized
the supplied image as lawfully obtained. The project did not independently
witness the dumping procedure, verify title, determine whether an access
control was involved, or establish a complete chain of custody. Those facts
remain attestations and unresolved legal-risk inputs, not findings.

## 2. Private input handling

The private environment recorded input identity, version, region, and byte
ordering without changing the source. Identity values, acquisition metadata,
and the input itself remain outside the public package. The public record says
what kinds of checks occurred without exposing values that would identify or
facilitate reconstruction of protected material.

## 3. Pinned technical workflow

The study used pinned public tool snapshots and project-developed host
integration. Private records associated generated compilation units, build
outputs, and runtime results with identified artifacts. Public sources describe
the relevant tools, but availability or licensing of a tool does not grant
rights in the game software or its derived material.

The private analysis included executable-region identification, translation,
host-service integration, and inspection of runtime boundaries. Disassembly,
mechanically translated code, symbol and address data, extracted content, and
raw traces remain restricted.

## 4. Behavioral requirements and implementation

Project-written behavioral requirements described expected interfaces, state
changes, tests, and constraints. They were written and normalized during and
after implementation. They were not a complete specification prepared in
advance by an isolated team.

Accordingly, this project does not claim conventional two-team clean-room
independence. Organizational separation inside one research environment and a
publication boundary improve auditability; they do not retroactively create an
independent specification handoff.

## 5. Measurement classes

The project kept evidence classes distinct:

- build and automated-test records;
- instrumented runtime telemetry;
- source, executable, and process inspection;
- participant-operated acceptance and participant statements;
- AI-assisted contemporaneous screen observations;
- negative runs and unresolved events; and
- bounded inferences drawn from named records.

No class silently substitutes for another. For example, nonzero audio-path
telemetry does not establish that a person heard accurate sound; a participant
statement does not become instrumented proof; and a screen observation without
retained media cannot be re-inspected from this release.

## 6. Bounded runtime exercises

Private scenarios exercised startup, menu and gameplay progression, graphics,
audio, physical-controller input, persistence context, and cooperative
shutdown. Each public claim is limited to the configuration and path actually
described.

The owner-operated acceptance route was unstructured. It produced useful
first-party evidence but was not a reference-oracle comparison, exhaustive test
plan, or defect-free certification. One earlier process-control session ended
while the game process remained outside its launcher. The game's final status
was unavailable, so the project records neither a crash nor a non-crash
finding. External session cleanup remains a hypothesis only.

## 7. Negative-result retention

A later graphical recheck failed its defined activity threshold. One display
path did not reach the expected callback, while adjacent trials on another path
produced activity below the threshold. The cause remains unresolved.

The negative record is a required member of the public evidence inventory. A
future pass must be added as a new event; it must not overwrite, relabel, or
silently remove the failed historical recheck.

## 8. Sanitization into public records

The publication layer reduces private evidence to the minimum facts needed to
support or limit a claim. Each structured record identifies its evidence class,
scope, retained facts, public-retention status, and limitations. Stable public
record identifiers replace private paths and protected-artifact identities.

Sanitization necessarily weakens independent auditability. The public record
can be checked for consistency with itself, but a reader cannot compare it with
the withheld raw evidence. This is disclosed as a limitation rather than
treated as proof.

## 9. Claim derivation

The human-readable ledger in [CLAIMS.md](CLAIMS.md) and machine-readable ledger
in [proof/claims.json](proof/claims.json) state:

- the claim and its scope;
- the evidence class and supporting public record;
- conditions that would contradict or force correction of the record; and
- limits on the inference permitted.

Positive historical observations, participant attestations, bounded
inferences, failed checks, and unresolved events retain separate statuses.

## 10. Public verification

Verification has two layers. The outer standard-library verifier checks the
complete export against its release manifest: exact inventory, regular-file and
symbolic-link policy, path safety, sizes, and digests. The nested proof verifier
then checks JSON structure, identifier uniqueness, evidence-to-claim
relationships, status/scope consistency, required negative evidence, and
selected overclaim language.

From the exported repository root, run complete-release integrity first, then
proof-capsule semantics:

```sh
python3 verify_release.py
PYTHONDONTWRITEBYTECODE=1 python3 release_tests/test_release_verifier.py
python3 proof/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 proof/tests/test_verifier.py
```

See [RELEASE_VERIFYING.md](RELEASE_VERIFYING.md) for the two-layer sequence and
[proof/VERIFYING.md](proof/VERIFYING.md) for the proof model. Passing both means
that the exported bytes match the outer manifest and that the nested records
satisfy their encoded rules. It does not prove the underlying private events,
legal provenance, fidelity, or independent replication.

## 11. Release preparation

The public package must be created from an explicit allowlist into a fresh
staging directory. Reviewers must inspect the exact staged bytes, not merely
the working tree. They must confirm that:

- excluded material is absent;
- every material statement has the right evidence label;
- every citation supports the nearby wording;
- the human-readable and structured claim ledgers agree;
- the verifier and tests pass on the exact export;
- the manifest covers exactly the expected files;
- AI-assisted language has been reviewed and adopted by a responsible human;
- rights and licensing decisions are stated accurately; and
- legal-risk review and upload are separately recorded decisions.

[REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) is the sign-off record. Mechanical
success does not authorize publication on its own.

## 12. Amendment protocol

Corrections and new results should be additive and versioned. A later result
must not rewrite history by erasing a failure, promoting an attestation to an
observation, or expanding a path-bounded result into a general claim. Any
change to claims, evidence, verifier rules, rights language, or scope requires a
new exact-export review and regenerated manifest.
