# Public proof-capsule format

## Purpose and epistemic limit

This directory is a report-and-proof capsule, not a playable implementation.
Its JSON records are sanitized transcriptions and summaries of a private,
first-party, AI-assisted study. They deliberately exclude protected inputs,
generated or reconstructed implementation material, executable artifacts, game
media, save data, raw traces, local paths, and identifying hashes for withheld
artifacts.

The verifier establishes four things:

1. the files named by `manifest.json` are exactly the files present;
2. each named file has the declared size and SHA-256 digest;
3. evidence and claims obey the closed schemas and status rules below; and
4. every claim resolves to evidence with a compatible status and scope,
   including preservation of every declared negative run.

It does **not** prove that a sanitized record is a truthful transcription,
authenticate the withheld telemetry, reproduce the private implementation, or
establish legal clearance, correctness, completeness, fidelity, or independent
replication. A manifest digest published through a separate trusted channel can
commit to one exact capsule, but it still cannot add facts that the capsule does
not contain.

## Common JSON rules

All JSON files use UTF-8 without a byte-order mark. The verifier rejects:

- duplicate object keys;
- floating-point values, `NaN`, and infinity;
- keys not named by the applicable schema;
- missing keys, blank required strings, or duplicate identifiers;
- noncanonical, absolute, backslash-containing, or traversing paths; and
- symbolic links, special files, unexpected files, and unsupported file types.

Integer evidence values must be between zero and the largest signed 64-bit
integer. Fact values are limited to booleans, nonnegative integers, and short
strings. No arbitrary nested fact payload is permitted.

Machine-readable Draft 2020-12 schemas for the manifest, claims, and individual
evidence records are included under `schema/`. They are useful for editors and
general JSON tooling. `verify.py` is normative for capsule acceptance because
cross-file inventory equality, digest checks, path safety, claim-to-evidence
references, exact scope matching, display-id completeness, and negative-run
preservation cannot be expressed by the three per-document schemas alone.

## Manifest schema

`manifest.json` has exactly these keys:

| Key | Type | Rule |
| --- | --- | --- |
| `format` | string | `whiteroom-proof-manifest-v1` |
| `package` | string | `whiteroom-public-proof-capsule` |
| `version` | integer | `1` |
| `hash_algorithm` | string | `sha256` |
| `files` | array | Nonempty, path-sorted file entries |
| `policy` | object | Closed policy object described below |

Each file entry has exactly `path`, `role`, `size`, and `sha256`. Roles are
`claims`, `documentation`, `evidence`, `schema`, `test`, or `verifier`.
Evidence must be a JSON file below `evidence/`; the claims role is reserved for
`claims.json`; schemas are JSON files below `schema/`; the verifier role is
reserved for `verify.py`; tests are Python files below `tests/`; and
documentation is Markdown.

The manifest does not hash itself because a self-hash has no finite fixed
construction. Instead, the verifier prints the SHA-256 digest of the exact
manifest after checking all manifest-listed content. That printed value is the
appropriate small commitment to record in a release, résumé appendix, signed
statement, or other independent channel.

The policy object has exactly these keys:

- `claims_file`: exactly `claims.json`;
- `evidence_directory`: exactly `evidence`;
- `required_claim_ids`: the sorted, complete claim-id inventory;
- `required_evidence_ids`: the sorted, complete evidence-id inventory;
- `required_negative_evidence_ids`: every and only record whose
  `record_kind` is `negative_run`;
- `allowed_statuses`: the sorted closed status vocabulary; and
- `allow_symlinks`: always `false`.

`manifest.json` plus the listed paths must equal the complete recursive file
inventory. There is no ignored-file concept.

## Evidence schema

Every `evidence/*.json` file has exactly:

```json
{
  "format": "whiteroom-evidence-v1",
  "evidence": {}
}
```

The `evidence` object has exactly these fields:

| Field | Meaning |
| --- | --- |
| `id` | Lowercase hyphenated id beginning with `evidence-`; the filename must match it |
| `status` | `observed`, `attested`, `inference`, or `unresolved` |
| `source_type` | Closed source vocabulary compatible with `status` |
| `scope` | Closed scope vocabulary used for exact claim matching |
| `record_kind` | `positive_run`, `negative_run`, `inspection`, `attestation`, `observation`, or `unresolved_event` |
| `summary` | Short project-authored description |
| `facts` | Nonempty list of typed name/value/unit triples |
| `retention` | Public-record form and the limits created by withholding raw material |
| `limitations` | Nonempty list of boundaries on the evidence |

Each fact has exactly `name`, `value`, and `unit`. Names use lowercase
underscore form. Units have mechanical type requirements:

- `boolean` requires a JSON boolean;
- `count` requires a nonnegative JSON integer; and
- `label` and `status` require a short JSON string.

The retention object has exactly `public_record`,
`underlying_material_public`, and `limitation`. `public_record` is either
`sanitized_summary` or `sanitized_transcription`.
`underlying_material_public` must be `false`; the capsule makes no contrary
representation about its private source material.

### Evidence status semantics

`observed` means the project record attributes the result to instrumentation,
inspection, AI-assisted live observation, or a process record. It does not mean
that a public reader independently observed it.

`attested` means the participant supplied the statement and the project did not
independently establish it. Attested evidence must use source type
`participant_attestation`, scope `participant_report`, and record kind
`attestation`.

`inference` is reserved for an analytical synthesis record. The current
capsule places its bounded inference in `claims.json` and points it to observed
inspection evidence instead of creating a second evidence-layer inference.

`unresolved` is reserved for a record whose source and kind are themselves
unresolved. An observed failed run remains `observed` evidence with
`record_kind` `negative_run`; its consequence is expressed by an `unresolved`
claim.

Every negative run must have scope `unresolved_question`. The policy must name
every and only negative run, and at least one unresolved claim must reference
each one. This makes deletion, relabeling, or quiet omission of an adverse run a
verification failure.

## Claim schema

`claims.json` has exactly `format`, `disclosure`, and `claims`.
`format` is `whiteroom-claims-v1`; `disclosure` states the public evidence
limit; and `claims` is a nonempty, id-sorted list.

Each claim has exactly:

| Field | Meaning |
| --- | --- |
| `id` | Lowercase hyphenated id beginning with `claim-` |
| `display_id` | Stable short reference in the complete sequence `C-001` onward |
| `status` | Evidence label governing the claim |
| `claim_kind` | Status-compatible claim class |
| `scope` | Exact scope shared by every referenced evidence record |
| `statement` | Bounded natural-language claim |
| `evidence_refs` | Sorted, nonempty evidence-id list |
| `failure_criteria` | Nonempty list stating what would contradict or resolve the claim |
| `limitations` | Nonempty list stating what the claim does not establish |

The complete claim-id set must equal the manifest policy, and every evidence
record must be referenced by at least one claim.

### Claim status rules

| Claim status | Required kind | Permitted scope | Required evidence |
| --- | --- | --- | --- |
| `observed` | `direct_observation` or `adverse_observation` | `exact_run`, `exercised_path`, or `examined_configuration` | Only observed, non-adverse evidence |
| `attested` | `participant_attestation` | `participant_report` | Only attested evidence |
| `inference` | `bounded_inference` | `exercised_path` or `examined_configuration` | Observation or attestation, including at least one observation |
| `unresolved` | `unresolved_question` | `unresolved_question` | Only negative-run or unresolved-event records |

Every referenced evidence record must have exactly the claim's scope. This
intentionally declines implicit scope widening. The verifier also rejects a
small stop-list of categorical claim phrases associated with completeness,
fidelity, legal clearance, independent reproduction, or other conclusions the
capsule cannot establish.

Natural-language truth cannot be reduced to a schema. Human review must still
ask whether each statement accurately reflects its referenced record, whether
the failure criteria are genuinely capable of defeating it, and whether the
limitations preserve every material qualification.

## Falsifiability and challenge procedure

A critic can challenge the capsule at three distinct layers:

1. **Integrity:** edit, remove, replace, or add a file. Verification must fail.
2. **Semantics:** change a status, widen a scope, remove a failure criterion,
   disconnect evidence, suppress a negative run, or introduce a categorical
   overclaim. Verification must fail even if the attacker updates the changed
   file's manifest entry.
3. **Underlying fact:** present a trustworthy retained record or new repeat run
   that meets a listed failure criterion. That may defeat a claim even when the
   capsule remains byte-for-byte valid.

The third category is the most important. Cryptographic hashes establish
identity, not truth. The capsule is designed to make its claims finite and
challengeable while plainly acknowledging that the private implementation and
underlying raw evidence are not independently executable or inspectable here.
