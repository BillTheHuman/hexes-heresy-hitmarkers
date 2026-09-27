# Contributing to Hexes, Heresy & Hitmarkers

**A Whiteroom Static-Recompilation Evidence Study**

**This repository is a publication record, not a place to submit game data,
private artifacts, or a playable implementation.**

Contributions are useful when they improve the accuracy, auditability, or
clarity of the public package without crossing its disclosure boundary.

## Welcome contributions

- corrections to factual statements or citations;
- clearer limits, contradiction conditions, or evidence labels;
- verifier and schema fixes that preserve fail-closed behavior;
- tests for malformed, altered, missing, extra, traversing, or symbolic-link
  package cases;
- accessibility, portability, and documentation improvements; and
- independent replication reports that follow the protocol and disclose their
  scope, methods, failures, retained evidence, and conflicts of interest.

## Do not submit

Do not open an issue, pull request, discussion, attachment, or link containing:

- cartridge images, fragments, archive metadata, or identifying private hashes;
- extracted assets, screenshots, recordings, dialogue, music, models, textures,
  fonts, or other game content;
- translated, reconstructed, decompiled, or disassembled game code;
- symbol maps, addresses, relocation data, raw memory, or execution traces;
- playable binaries, save files, patches against protected material, keys, or
  operational bypass instructions;
- private repository history, local paths, credentials, personal information,
  or unapproved participant statements; or
- material whose publication or licensing authority is uncertain.

If a correction depends on restricted material, describe only the public claim
that needs correction and why its current wording is unsupported. Do not upload
the restricted material as proof. A maintainer may request a safer summary or
close a submission that creates disclosure risk.

## Evidence and claim changes

Every claim change should:

1. preserve its stable claim identifier or explain why a versioned replacement
   is necessary;
2. name the evidence class and scope;
3. state what would contradict or require correction of the record;
4. preserve material limitations and contrary evidence;
5. add a new event instead of overwriting a historical pass, failure, or
   ambiguity; and
6. update the human-readable ledger, machine-readable records, tests, and
   manifest together.

Never promote a participant attestation into an instrumented observation,
describe public file verification as execution replication, or infer fidelity
from the absence of a reported problem.

## Verification expectations

Before proposing a change, run the complete-release check first and the nested
proof check second, as described in
[RELEASE_VERIFYING.md](RELEASE_VERIFYING.md). See
[proof/VERIFYING.md](proof/VERIFYING.md) for the proof model. Changes should
include focused tests for any new invariant or corrected failure mode. The
verifiers must continue to reject unexpected files, altered digests, unsafe
paths, symbolic links, malformed records, missing negative evidence, and
claim/evidence status mismatches.

## Rights and conduct

Release 1.0.0 uses file-specific licenses, as detailed in
[RIGHTS.md](RIGHTS.md):

- original prose, records, manifests, and `CITATION.cff` are licensed under
  `CC-BY-SA-4.0`; and
- original software, user-interface source, tests, and schemas are licensed
  under `GPL-2.0-or-later`.

By submitting a contribution for inclusion, you agree to license that
contribution under the license already assigned to its destination file. A new
file should use the license for the category it joins. Contributors retain
their copyright; this project does not require a copyright assignment. If a
change spans categories or its proper category is unclear, identify that in
the submission before it is merged.

Submit only material that you have authority to provide under the applicable
license. Do not assume that possessing, quoting, transforming, or using
third-party or AI-assisted material gives this project authority to publish or
relicense it. Describe the source and your claimed authority for any proposed
text or code. The project may decline material whose provenance or licensing
authority cannot be established.

Use third-party names only as needed for precise identification. Do not imply
sponsorship, endorsement, or legal approval. Be exact, civil, and candid about
uncertainty: a well-described failure is more valuable than an inflated result.
