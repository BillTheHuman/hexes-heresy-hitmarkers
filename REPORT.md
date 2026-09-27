# Hexes, Heresy & Hitmarkers

## A Whiteroom Static-Recompilation Evidence Study

Status: **Release 1.0.0 — adopted and authorized for publication by William F.
Rineer III on 2026-09-27; first-party, AI-assisted, not independently
replicated, and not independently legally reviewed**

## Purpose

This report documents a private study of whether software from a Nintendo 64
cartridge represented by the participant as lawfully possessed can be analyzed
and executed through static recompilation on a modern host. The intended public
contribution is the research account: methods, measured behavior, limitations,
and risk controls.
The cartridge image, translated program material, extracted content, and
playable implementation are not publication artifacts.

This report does not provide legal advice or claim that the work has received
legal clearance. No independent legal review of this release has occurred.
The statutory and case-law questions identified below remain subject to
jurisdiction and facts.

Product and character names, when necessary, are used only to identify the
research subject or an observed test path. This study is unaffiliated with and
not endorsed by Nintendo or any other game or platform rights holder.

In this report, “owner” is shorthand for the participant who attested to
ownership. The label does not indicate independent verification of title.

## Research assistance and responsibility

OpenAI Codex materially assisted with repository inspection, implementation,
test orchestration, live screen inspection, evidence organization, and
drafting. William F. Rineer III, the participant who attested to ownership,
selected the scope, supplied the factual attestations attributed to the owner,
performed the interactive acceptance runs, directed the disclosure boundary,
reviewed the release, and adopted its publication wording on 2026-09-27. This
disclosure describes the working process; it does not resolve the
copyrightability or authorship of every passage.

## Evidence vocabulary

The report uses five labels consistently:

- **Observation:** an instrumented, human-observed, or AI-assisted record, with
  any material retention limitation stated.
- **Attestation:** a statement supplied by the cartridge owner that the project
  has not independently verified.
- **External source:** a proposition attributed to a cited public authority and
  checked against the exact linked source.
- **Inference:** a bounded conclusion drawn from one or more observations.
- **Unresolved:** a question for which the present evidence is insufficient.

These labels must not be collapsed. In particular, an attestation is not proof,
and a successful test run does not establish complete equivalence.

## Public proof layer and its limit

This release pairs the narrative report with a claim ledger, sanitized
structured records, a public manifest, a standard-library verifier, and
deliberately altered test fixtures. A reader can check public-file integrity,
schema conformance, explicit claim-to-record references, enumerated status and
scope constraints, required negative-record retention, and selected forbidden
overreach patterns. The verifier does not decide whether every prose conclusion
logically follows from the evidence. See [CLAIMS.md](CLAIMS.md),
[PROOF_FORMAT.md](proof/PROOF_FORMAT.md), [VERIFYING.md](proof/VERIFYING.md), and
[RELEASE_VERIFYING.md](RELEASE_VERIFYING.md).

That verification is falsifiable but deliberately bounded. It does not
authenticate the truth of a private observation, bind a public record
cryptographically to a withheld executable, recreate an excluded run, verify
the participant's cartridge ownership or dumping procedure, or independently
execute the private implementation. Hashes authenticate bytes after capture;
they do not make the captured proposition true. No person or laboratory outside
the participant and AI-assisted project environment has replicated this work.

## Scope and research controls

The analysis and executable proof remain private. Project files were organized
into restricted input and analysis areas, project-developed host integration,
and a report-only disclosure area. These are internal handling and publication
controls, not an independent information barrier.

The project records published license files associated with pinned tool
snapshots. Any use or redistribution must comply with the terms actually
applicable to each covered component; project-level license files do not
establish coverage of every dependency. They confer no rights in third-party
game software or generated game material. Comparable public projects are cited
only as evidence of engineering practice, not as judicial precedent or legal
approval.

The project does not claim a conventional clean-room implementation or use
“clean room” as a legal conclusion. One research environment handled translated
material and implementation work, and no complete standalone behavioral
specification was handed from one isolated team to another before
implementation. Requirements and tests written alongside or after
implementation improve auditability but do not create retroactive independence.

## Current evidence summary

The structured capsule's twelve selected claims and their contradiction
conditions are in [CLAIMS.md](CLAIMS.md). The summary below preserves the
distinction between instrumented observations, inspection, AI-assisted
observations, participant attestations, inference, and unresolved evidence.
Statements explicitly labeled **supplementary** preserve additional
private-record context but are outside the machine-readable claim capsule and
are not checked by the public verifier.

### Attestations

**Supplementary participant provenance context — outside the structured proof
capsule:**

- The owner states that they possess the physical cartridge.
- The owner characterizes the supplied image as lawfully obtained from an owned
  cartridge for this private study.
- The project did not independently observe the acquisition or dumping
  procedure, verify that legal characterization, or establish a complete chain
  of custody.

### Artifact-bound build and runtime telemetry

The automated records below came from earlier, explicitly identified
artifact-bound runs. Neither those records nor the separately labeled
owner-operated acceptance supplement is a claim that the later host recheck
passed.

- A sanitized audit of one examined configuration recorded the distinct mapped,
  declaration, generated-definition, runtime-supplied, translation-unit,
  generated-file, byte, overlay-section, and overlay-entry counts stated in
  C-001. It does not treat those populations as interchangeable.
- One accepted fifteen-second scripted run traversed generic menu, intro, and
  battle phases and recorded the VI, screen-update, and display-list counts
  stated in C-002.
- Instrumentation recorded nonzero samples in the translated audio path,
  host-side sample conversion, and delivery to the operating system's audio
  interface.
- A physical controller produced button and analog input observed by the host
  integration while the program progressed. Rumble commands were also issued
  without a recorded host-side failure during the observed run.
- On one identified detached window-close run, logs recorded the planned runtime, audio,
  controller, window, and SDL teardown sequence.
- **Supplementary private-record summary — outside the structured proof
  capsule:** bounded preservation runs selected an in-memory baseline without reading or
  rewriting the persisted user profile. Separate configured runs read back the
  requested startup settings. With unmuted volume set to 50 percent, the
  playback peak matched the deterministic integer-scaled raw peak; with mute
  enabled, playback counters were silent while the separately measured raw
  stream remained nonzero.

### Source and executable inspection

- **Supplementary private-record summary — outside the structured proof
  capsule:** source inspection and dedicated tests exercised current-user-restricted,
  descriptor-anchored storage and no-follow handling of directory links.
- Source inspection and dedicated tests exercised the examined settings and
  launcher contract with an isolated disposable fake child, including held-path
  identity, argument and environment policy, descriptor closure, lifecycle
  handling, and marker-symbolic-link rejection. This is not live-game behavior.
- Build and executable inspection of the tested configuration did not identify
  a guest-CPU interpreter or guest-CPU just-in-time compiler in that path.
- **Supplementary private-record summary — outside the structured proof
  capsule:** source and build inspection recorded a graphics compatibility layer processing
  console display commands. Process inspection observed executable mappings
  during graphical runs; captured syscall stacks associated their transitions
  with a host graphics-driver helper.

### Process and shutdown records

- The earlier long owner-operated session is excluded from clean-shutdown
  evidence. Its process-control session returned status 143. The game was then
  observed still running and reparented outside the launcher. It was later
  absent; no matching core dump was found, and its final exit status was
  unavailable.
- A detached systemd relaunch produced separate shutdown evidence. The private
  log recorded `reason=window-close`, 622 VI callbacks, 621 screen updates, 609
  display-list submissions, and teardown messages for the runtime, audio,
  controller, window, and SDL subsystems.

### AI-assisted contemporaneous screen observations

During a final owner-operated session, AI-assisted live screen inspection
identified the credits and an explicit secret-character unlock notice. During
the later detached run, it identified the launcher message “The game closed
normally.” No screenshot was retained from either observation, so these
observations are supported only by the private contemporaneous session record
and cannot be independently re-inspected from the release package.

### Participant attestations

**Supplementary participant audio attestations — outside the structured proof
capsule:** during earlier attempts, the owner described audio as delayed and
crackly in one run and reported no audible sound in a separate run. After a
later output-path change, the owner reported hearing the game without an audio
issue. These are uninstrumented, subjective accounts from different runs and
configurations. Their causes remain unresolved; they neither contradict nor
upgrade C-003's narrower audio-path telemetry, and they do not establish timing,
channel accuracy, fidelity, or correspondence to original hardware.

For the final acceptance session, the owner reported completing a
single-player route through its final encounter, seeing the credits, defeating
a post-route challenger, and noticing no issues. After the detached relaunch,
the owner reported that the newly unlocked character remained selectable and
that the game was then closed through its window. The owner also reported not
closing the earlier orphaned game and seeing no intervening state change or
crash indication before it disappeared while idle. These are owner
attestations; the AI-assisted live observations and private telemetry above
are separate direct evidence. This was an unstructured acceptance report, not a
defect-free finding.

### Bounded inference

For the examined configuration and execution path, project inspection supports
a bounded inference that the guest-CPU path used ahead-of-time host code and did
not identify a guest-CPU interpreter or guest-CPU JIT there. Because executable
inventory and reachability accounting remain incomplete, this is a bounded
negative finding, not proof of absence from every path. It does not support the
unqualified phrase “no emulation”:
graphics and platform compatibility services remain part of the system, and
host drivers may dynamically compile their own code.

The participant attested that the route reached credits and that one unlocked
character remained selectable after restart. AI-assisted observations
separately identified the credits and unlock notice. Detached-run telemetry
recorded the restart and shutdown path but did not itself establish the
on-screen selectable state. Together, these records support the reported route
and persistence of one unlock state, not behavior beyond that path, general
save reliability, fidelity, completeness, legal clearance, or conventional
clean-room independence. They do not replace the failed current automated
graphical recheck.

The evidence does not establish why the earlier orphaned game process ended.
Status 143 applied to the process-control session, while the game's final
status was unavailable. External session cleanup remains a working hypothesis
only; the record supports neither a crash nor a non-crash determination.

### Unresolved questions

- The executable inventory and reachability accounting are incomplete.
- Visual, audio, timing, and gameplay fidelity have not passed an independent
  reference oracle.
- Repeatability and deterministic state comparison require additional work.
- A later host recheck did not reproduce the previously recorded graphical
  activity threshold: one display path stalled before guest video callbacks,
  while another reached a telemetry state associated with the expected menu
  scene and logged the expected teardown sequence but submitted too few display
  lists. The cause remains unresolved, and this recheck is not reported as a
  pass.
- **Supplementary private-record limitation — outside the structured proof
  capsule:** persisted controller bindings remain unapplied because the current schema
  cannot represent all established compound default mappings. A
  controller-operated or in-game settings surface, effective
  fullscreen/multisampling capability checks, and multi-controller validation
  also remain incomplete.
- The provenance record does not yet include a witnessed participant-controlled
  dump.
- No complete pre-implementation specification handoff or conventional
  independent two-team clean-room separation occurred.
- Because protected inputs, executable artifacts, and raw logs are excluded,
  the public package does not enable readers to reproduce all reported runs or
  inspect all underlying evidence independently.
- The release applies its licenses only to original material and rights William
  F. Rineer III controls; facts, standard license texts, third-party material,
  names, marks, and rights not controlled by William remain excluded.
- William F. Rineer III adopted the release wording and authorized publication
  on 2026-09-27. No independent intellectual-property review occurred.
- No conclusion has been reached about whether any access-control provision,
  contract term, or jurisdiction-specific rule applies to the acquisition or
  analysis facts.

## Method and publication protocol

### 1. Input identity and custody

The project recorded the input privately using cryptographic identity, version,
region, and byte-order information and preserved the source unchanged. This
package describes the verification method without publishing the image, archive
metadata that exposes acquisition history, or unnecessary identifying values.

### 2. Restricted technical analysis

Pinned tools were used to identify executable regions, translation units,
required platform services, and runtime interfaces. Disassembly, mechanically
translated code, symbol maps, addresses, extracted content, and raw traces
remain in the restricted lane.

### 3. Project-worded behavioral requirements

Project-worded requirements were written to describe the behavior needed for
interfaces, state changes, tests, and constraints. They were normalized during
and after implementation and are review records, not a pre-implementation
specification from an independent team. Implementation expression, game text,
visual arrangement, audiovisual content, and mechanically generated material
remain outside the publication lane.

### 4. Host execution and measurement

The private translation was built with project-developed host services. The
private record documents boundaries among guest CPU execution, graphics
compatibility, audio, input, storage, operating-system services, and device
drivers.

### 5. Claim calibration

The restricted evidence record ties results to private artifacts and test
configurations. This public release states only the result needed to support
each claim and retains every material limitation. Public artifact-generation
labels are neutral aliases, not published hashes or independent proof of
lineage.

## Legal context and unresolved questions

The following are questions, not conclusions. The package's narrow disclosure
boundary is a risk control, not a ruling that the private work or publication is
lawful:

1. Does the proposed report reproduce protectable expression, including code,
   audiovisual material, dialogue, character expression, or an original
   selection or arrangement, beyond what is necessary to explain the findings?
2. How does ownership of the physical cartridge or copy differ from ownership
   of copyright in the work embodied in it?
3. How do the four section 107 factors apply to the intermediate copies and
   adaptations documented in the private record, including their purpose,
   character, necessity, amount, and potential market effect?
4. Is the actor an “owner of a copy” for section 117 purposes, and does section
   117(a)(1) apply to any copy or adaptation as an essential step used in no
   other manner, or section 117(a)(2) to any archival-only copy? Do section
   117(b)'s transfer restrictions apply?
5. Did any technical step circumvent an effective access control, and if so,
   does section 1201(f) or a current 37 C.F.R. § 201.40(b)(19) class actually
   apply? Would publishing any code, instructions, links, or other material
   constitute manufacturing, importing, offering to the public, providing, or
   otherwise trafficking in a technology, product, service, device, component,
   or part prohibited by section 1201(a)(2) or (b), separately from whether an
   act of circumvention is exempt?
6. Do any cartridge, platform, software, account, tool, or output terms create
   relevant contractual restrictions?
7. Was any information obtained through improper means or subject to a duty to
   maintain secrecy or limit use, and do federal or applicable state
   trade-secret rules apply?
8. Does the proposed naming, branding, imagery, or trade dress create a
   likelihood of confusion, false association, sponsorship, endorsement, or
   dilution?
9. Which portions of the final report reflect identifiable human authorship,
   and should any copyright notice, license, or registration claim be limited
   accordingly?
10. Could the report or accompanying material substitute for the copyrighted
    work, facilitate unauthorized copies, or adversely affect an existing or
    reasonably likely market?
11. Do the repository description, release notes, résumé language, and other
    publicity accurately distinguish the private prototype from the published
    report and avoid implying legal approval?

## Publication conclusion

This release is a report-and-proof package, not the private
implementation. William F. Rineer III adopted the wording, acknowledged the
unresolved legal risks and absence of independent legal review, and authorized
publication on 2026-09-27. That decision is not legal clearance, approval of the
private work, or independent replication.

Each release must be a sanitized, allowlisted export; pass the public
verifier and containment gate; preserve the negative and unresolved records;
receive citation, wording, rights, metadata, and rendered-output review; and be
inspected as the exact archive proposed for upload. Whether independent counsel
reviews that archive must be recorded truthfully; no such review is claimed
here. See [PUBLICATION_BOUNDARY.md](PUBLICATION_BOUNDARY.md) for the release gate,
[REPLICATION_STATUS.md](REPLICATION_STATUS.md) for the replication vocabulary,
and [SOURCES.md](SOURCES.md) for authorities and contextual project references.
