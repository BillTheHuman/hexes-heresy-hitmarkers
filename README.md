# Hexes, Heresy & Hitmarkers

## A Whiteroom Static-Recompilation Evidence Study

**Release 1.0.0 — adopted and authorized for publication by William F. Rineer
III on 2026-09-27; first-party, AI-assisted, not independently replicated, and
not independently legally reviewed.**

Canonical repository:
[github.com/BillTheHuman/hexes-heresy-hitmarkers](https://github.com/BillTheHuman/hexes-heresy-hitmarkers)

Whiteroom documents a first-party, AI-assisted study of whether software from a
Nintendo 64 cartridge could be translated ahead of time and exercised on an
x86-64 Linux host. The participant represented that the private input came from
an owned cartridge. The project did not independently witness the dumping
procedure, verify title, or establish a complete chain of custody.

The public deliverable is a report-and-proof package, not a port. It contains
project-written analysis, a bounded claim ledger, sanitized evidence summaries,
negative results, and a verifier for the public files. It contains no playable
implementation or game content.

## Result in one paragraph

Identified private runs recorded a produced host executable, menu and gameplay
progression, graphics-command submission, nonzero audio-path activity, physical
controller input, and cooperative teardown on the exercised paths. The
participant separately attested to completing one single-player route and to
one unlocked state remaining available after restart. Inspection supports the
bounded inference that the examined guest-CPU path used ahead-of-time host code;
it did not identify a guest-CPU interpreter or guest-CPU just-in-time compiler
on that path. These findings are not claims of completeness, fidelity,
defect-free operation, or coverage beyond the examined configuration. A later
automated graphical recheck missed its activity threshold, and its cause
remains unresolved.

## What a public reader can verify

A reader can:

- inspect twelve bounded claims and the conditions that would contradict each
  record;
- inspect the evidence class, scope, retention limits, and caveats attached to
  every sanitized record;
- confirm that negative evidence has not been omitted from the claim logic;
- validate the public file inventory and file digests;
- run the verifier against the canonical package; and
- run the public tests to see altered, malformed, missing, extra, traversing,
  and symbolic-link cases rejected.

That is **public record verification**. It establishes the package's file
integrity and the verifier's enumerated structural, inventory, relationship,
status, scope, negative-record, and selected overreach constraints. It is not a
general semantic review of every prose statement. It does not authenticate the
truth of a private observation, recreate a withheld run, validate the cartridge
attestation, or execute the private implementation. A digest commits to bytes;
it does not prove that an event happened.

## Four different levels of repeatability

The project keeps these concepts separate:

1. **First-party internal repetition:** some bounded tests and scenarios were
   repeated inside the private project environment.
2. **Public record verification:** anyone can check this package's inventory,
   structure, claim-to-record relationships, and verifier behavior.
3. **Underlying execution reproducibility:** unavailable from this package,
   because the protected input, translated implementation, executable, and raw
   evidence are withheld.
4. **Independent replication:** none has occurred as of this release.

See [REPLICATION_STATUS.md](REPLICATION_STATUS.md) for the exact status.

## Start here

- [REPORT.md](REPORT.md) gives the full research account, limitations, and legal
  questions.
- [CLAIMS.md](CLAIMS.md) is the human-readable claim ledger.
- [proof/claims.json](proof/claims.json) is the machine-readable claim ledger.
- [proof/evidence](proof/evidence) contains the sanitized structured records.
- [PROTOCOL.md](PROTOCOL.md) describes the private study and public-proof
  procedures without disclosing restricted material.
- [proof/PROOF_FORMAT.md](proof/PROOF_FORMAT.md) defines the structured proof
  format.
- [proof/VERIFYING.md](proof/VERIFYING.md) explains how to run and interpret the
  verifier.
- [RELEASE_VERIFYING.md](RELEASE_VERIFYING.md) explains how to verify the entire
  exported repository before checking the nested proof semantics.
- [REPLICATION_STATUS.md](REPLICATION_STATUS.md) distinguishes repetition,
  verification, reproducibility, and replication.
- [PUBLICATION_BOUNDARY.md](PUBLICATION_BOUNDARY.md) defines what must remain
  private.
- [SOURCES.md](SOURCES.md) records legal and engineering context.
- [NOTICE.md](NOTICE.md) gives the author credit, license map, requested
  attribution, and nonendorsement statement.
- [RIGHTS.md](RIGHTS.md) defines the file-specific `CC-BY-SA-4.0` and
  `GPL-2.0-or-later` grants and their limits.
- [CITATION.cff](CITATION.cff) provides citation metadata.
- [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) records release review and upload
  verification.

For a downloaded export, verify the complete release first and the evidence
model second:

```sh
python3 verify_release.py
python3 proof/verify.py
```

Run the focused test commands in
[RELEASE_VERIFYING.md](RELEASE_VERIFYING.md) as part of a full review. Passing
either layer does not establish the private events' truth.

## What is deliberately absent

This release contains no cartridge image or fragment, archive, extracted
asset, game screenshot, recording, save file, translated or decompiled game
code, disassembly, symbol or address map, raw execution trace, playable binary,
patch against protected program material, key, or operational bypass guidance.
It also excludes the private repository and its history.

The exclusions make the package safer and more focused, but they also limit
what a reader can independently test. That tradeoff is intentional and must not
be hidden behind the public verifier.

## Engineering-publication context

Ship of Harkinian is useful context for one engineering principle: a public
project can keep user-supplied game resources separate from its published
work. Its pinned public materials describe a much broader source-port model,
including decompilation-derived program source, a native executable, and local
resource extraction from a user-supplied copy. This package adopts only the
separation principle and is materially narrower: it publishes no port,
reconstructed game logic, executable, extractor, patch, or asset pipeline.

The exact pinned Shipwright and upstream decompilation sources are listed in
[SOURCES.md](SOURCES.md#public-and-source-available-engineering-context). Their
existence is engineering context, not legal precedent, permission, or evidence
that this project's private conduct or publication is lawful.

## Research assistance and responsibility

OpenAI Codex materially assisted with repository inspection, implementation,
test orchestration, live screen inspection, evidence organization,
verification, and drafting. William F. Rineer III selected the scope, supplied
the attestations attributed to the owner, performed the interactive acceptance
sessions, directed the disclosure boundary, reviewed the release, and adopted
its publication wording on 2026-09-27. This disclosure does not settle
authorship or copyrightability of every passage.

## Rights and nonendorsement

Copyright (C) 2026 William F. Rineer III. Original documentation and curated
evidence are licensed `CC-BY-SA-4.0`; original software, tests, schemas, and
presentation source are licensed `GPL-2.0-or-later`. The grants apply only to
rights William controls. See [NOTICE.md](NOTICE.md), [RIGHTS.md](RIGHTS.md), and
the complete texts in [LICENSES](LICENSES).

Attribution identifies provenance only. It does not mean William F. Rineer III
sponsors, approves, endorses, or assumes responsibility for a recipient,
redistribution, modification, conclusion, or use—including unlawful, harmful,
or misleading use. This nonendorsement statement adds no restriction to either
license.

Product and project names are used only to identify research subjects, tools,
or engineering context. Whiteroom is independent and is not sponsored,
approved, or endorsed by Nintendo or any other game, platform, or tool rights
holder. Third-party names and marks remain the property of their respective
owners.

This package is a technical research record, not legal advice or legal
clearance for the private work, the report, or anyone else's conduct.
