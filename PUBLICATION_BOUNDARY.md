# Publication boundary

Status: **mandatory containment gate for each public release**

Only a fresh export assembled from the explicit report-and-proof map may become
a publication surface. A source directory or mechanically passing export is not
approved until exact-export editorial, evidence, rights, and owner legal-risk
review is complete. Release 1.0.0 completed those project gates without an
independent legal review; none is claimed.
The private repository, build tree, research notes, raw evidence, and executable
implementation are outside the public deliverable.

## Permitted content

Only material satisfying every applicable condition may be considered:

- newly prepared project prose, including disclosed AI-assisted drafting, that
  neither reproduces nor closely paraphrases restricted expression;
- observations expressed as aggregate or qualitative results sufficient to
  support the report's claims;
- owner attestations clearly labeled as attestations;
- bounded inferences that identify the observations on which they rely;
- unresolved questions and negative findings stated without overclaiming;
- links and bibliographic descriptions of authoritative public sources;
- diagrams prepared specifically for the report and individually reviewed for
  source independence, disclosure, and publication or licensing authority;
- reviewed README, protocol, claim-ledger, replication, contribution, rights,
  resume, and review-checklist prose;
- sanitized aggregate JSON records whose provenance class and retention limit
  are explicit;
- original verifier, schema, and test code, including synthetic tampering
  fixtures that contain no private material;
- original dependency-free presentation source that renders only the same
  reviewed public claims and records; and
- hashes that identify only files inside the exact public package.

## Excluded content

The publication package must not contain:

- cartridge images, archives, fragments, headers, extracted assets, or content
  capable of reconstructing them;
- disassembly, mechanically translated code, generated compilation units,
  decompilation, symbol maps, relocation data, addresses, instruction tables,
  or raw memory and execution traces;
- playable binaries, patches against protected program material, save files,
  keys, access-control bypass material, or operational circumvention guidance;
- game screenshots, music, sound effects, models, textures, fonts, dialogue, or
  other expressive content;
- raw identifying hashes for the protected input or private derived artifacts;
  package-file hashes are permitted only when independently recomputable from
  files in the same public export;
- absolute local paths, usernames, device identifiers, personal information,
  acquisition-source metadata, or unapproved owner quotations;
- third-party logos, trade dress, copied user-interface arrangement, or wording
  that implies sponsorship or endorsement;
- unreviewed machine-generated prose, machine-suggested citations that have not
  been opened and checked, or claims whose responsible human reviewer has not
  adopted the final wording; or
- claims of legal clearance, conventional clean-room independence, complete
  fidelity or implementation, defect-free operation, “fully playable,” “no
  emulation,” a “legal port,” or publication or commercial availability of the
  private implementation.

## Required evidence labels

Every material claim must be recognizable as one of:

- direct project observation, identifying whether it was instrumented,
  human-observed, or AI-assisted and stating any material retention limitation;
- owner or participant attestation;
- external-source statement with a citation;
- project inference, with its supporting observations and limits; or
- unresolved question.

If a sentence cannot be labeled confidently, it does not pass the gate.

## Release procedure

1. Assemble only the paths in the reviewed publication map into a newly created
   staging area; never export the workspace or its history.
2. Generate a complete file inventory and verify that every item is expected.
3. Scan for prohibited file types, embedded binaries, long encoded strings,
   absolute paths, secrets, identifying hashes, and vocabulary associated with
   restricted artifacts.
4. Compare the staged text against restricted source and generated material to
   detect unintended verbatim transfer. Keep comparison results private.
5. Review every table, figure, quotation, excerpt, and metadata field manually.
6. Review every AI-assisted passage and machine-suggested citation; a responsible
   human editor must adopt the final wording and verify each source directly.
7. Validate every external link and confirm that the cited source supports the
   exact proposition stated.
8. Review the repository title, description, release notes, résumé wording,
   disclaimer, and proposed license as part of the same release.
9. Keep restricted-source comparisons local; do not submit protected material
   to an external similarity service.
10. Render the report and inspect the rendered output and document metadata.
11. Run the public verifier and its negative tests. Stop if canonical records
    fail, a malformed fixture passes, evidence references are unresolved, or a
    computed classification disagrees with the published claim.
12. Review the exact final archive, not merely the working files. Record its
    file inventory and release hash privately.
13. Record the owner's legal-risk decision for that exact archive, including
    whether jurisdiction-appropriate independent counsel reviewed it. If no
    independent review occurred, disclose that fact and do not imply clearance.

## Automatic stop conditions

Publication stops if review discovers protected bytes, translated or
disassembled implementation material, a playable artifact, operational bypass
instructions, uncertain provenance presented as fact, an unsupported fidelity
claim, personal information, unreviewed AI-assisted wording, or a citation that
does not support its claim. It also stops for known lack of authority to publish
an included element, materially undisclosed AI assistance, verifier or manifest
disagreement, omission or relabeling of a negative result, or wording that
implies counsel certified the private project itself as lawful.

The issue must be removed and the entire release procedure repeated. A
disclaimer does not cure inclusion of excluded material.
