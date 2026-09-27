# Claim ledger

**Status: Release 1.0.0 public claim ledger. The machine-readable ledger in
[proof/claims.json](proof/claims.json) is authoritative for verifier input; this
document
is its human-readable companion.**

Each claim is deliberately narrow. “Would contradict this record” identifies a
condition that would require correction, withdrawal, or reclassification. For
a historical run, a later success or failure does not erase the earlier event;
it changes the repeatability picture and must be recorded separately.

## Evidence classes

- **Instrumented observation:** telemetry or a test result from an identified
  private run.
- **Inspection observation:** a first-party source, build, executable, or
  process inspection.
- **AI-assisted observation:** contemporaneous live screen inspection, with any
  media-retention limit stated.
- **Participant attestation:** a statement supplied by the participant and not
  independently verified.
- **Bounded inference:** a conclusion limited to named observations and scope.
- **Negative or unresolved evidence:** a failed check, ambiguity, or question
  the present evidence cannot resolve.
- **Public verification result:** a result anyone can rerun on the public
  package; it says nothing by itself about the private event's truth.

## Claims

### C-001 — Examined build inventory

- **Machine ID and status:** `claim-build-inventory-observation`; observed.
- **Claim:** A sanitized audit of one examined configuration recorded 7,180
  mapped entries, 7,103 declarations, 7,046 generated definitions, 57
  runtime-supplied declarations, 71 C translation units, 74 generated files
  totaling 37,708,847 bytes, 70 overlay sections, and 7,100 overlay entries.
- **Basis:** a sanitized build-audit and inspection record derived from the
  retained private audit.
- **Would contradict this record:** any public count differing from the retained
  audit, a declaration partition other than 7,046 plus 57, or treatment of
  mapped entries, declarations, definitions, and overlay entries as the same
  population.
- **Essential limit:** the inventory does not establish a one-for-one generated
  definition for every mapped entry. Reachability, relocations, jump tables,
  reviewed exceptions, and complete inventory closure remain incomplete.

### C-002 — Scripted graphical run

- **Machine ID and status:** `claim-graphical-scripted-run-observation`;
  observed.
- **Claim:** One accepted fifteen-second scripted run traversed generic menu,
  intro, and battle phases and recorded 901 VI callbacks, 901 screen updates,
  and 726 display-list submissions.
- **Basis:** instrumented telemetry from that exact private run.
- **Would contradict this record:** a transcribed counter differing from the
  retained record, absence of the summarized phase progression, or attribution
  of the result to a different artifact generation or acceptance session.
- **Essential limit:** counters do not establish rendered-pixel correctness or
  reference fidelity. Internal state identifiers, screenshots, frame captures,
  and a pixel oracle are not public. This result remains distinct from later
  generations and C-010's failed recheck.

### C-003 — Audio-path activity

- **Machine ID and status:** `claim-audio-path-observation`; observed.
- **Claim:** Identified instrumented runs recorded nonzero translated-path audio
  samples, host conversion, and operating-system delivery on the exercised
  path.
- **Basis:** instrumented private telemetry.
- **Would contradict this record:** absence of nonzero translated-path samples,
  host conversion, or operating-system delivery, or a retained record that
  contradicts a summarized fact.
- **Essential limit:** this does not establish physical audibility, accuracy,
  timing, channel behavior, or correspondence to original hardware.

### C-004 — Physical controller path

- **Machine ID and status:** `claim-controller-path-observation`; observed.
- **Claim:** Physical button and analog input reached the host integration on
  the exercised path, and rumble commands were recorded without a host-side
  failure in the observed run.
- **Basis:** instrumented input, progression, and host-output telemetry.
- **Would contradict this record:** absence of physical button or analog input,
  a host-side rumble failure omitted by the summary, or no accompanying private
  program progression.
- **Essential limit:** this does not cover every binding, device, disconnect
  case, latency edge, or multi-controller configuration.

### C-005 — Detached window-close run

- **Machine ID and status:** `claim-detached-window-close-observation`;
  observed.
- **Claim:** One detached run recorded a window-close reason, 622 VI callbacks,
  621 screen updates, 609 display-list submissions, and the planned subsystem
  teardown sequence.
- **Basis:** instrumented telemetry from that exact private run.
- **Would contradict this record:** a transcribed counter differing from the
  retained private log, absence of the window-close reason, or a missing or
  contradictory teardown event.
- **Essential limit:** this is run-specific telemetry. It does not establish
  reference fidelity or every shutdown path.

### C-006 — Participant acceptance account

- **Machine ID and status:** `claim-owner-acceptance-attestation`; attested.
- **Claim:** The participant reported completing one route through its final
  encounter and post-route challenge, then finding one new unlock still
  available after restart.
- **Basis:** participant attestation summarized from contemporaneous statements.
- **Would contradict this record:** participant withdrawal or material
  correction, a contradictory contemporaneous private record, or presentation
  of the statement as instrumented or independently witnessed proof.
- **Essential limit:** the session was an unstructured first-party acceptance
  run. The attestation covers only the exercised route and one persisted unlock
  state; it does not establish absence of defects.

### C-007 — AI-assisted screen observations

- **Machine ID and status:** `claim-screen-observation`; observed.
- **Claim:** AI-assisted live inspection identified the credits, an unlock
  notice, and a later normal-close launcher message on the exercised path.
- **Basis:** contemporaneous AI-assisted screen observations.
- **Would contradict this record:** absence of a stated observation from the
  contemporaneous private session record, a conflicting retained image or
  session record, or presentation of the screens as publicly re-inspectable.
- **Essential limit:** no screenshot was retained. These observations do not
  establish the participant's full route account or the selectable state after
  restart.

### C-008 — Examined guest-CPU path

- **Machine ID and status:** `claim-native-path-bounded-inference`; inference.
- **Claim:** For the examined configuration and execution path, inspection
  supports a bounded inference that the guest-CPU path used ahead-of-time host
  code; no guest-CPU interpreter or guest-CPU just-in-time compiler was
  identified there.
- **Basis:** build and executable inspection.
- **Would contradict this record:** an active guest-CPU interpreter or JIT on
  the examined path, absence of the reported ahead-of-time host code, or
  reachability evidence inconsistent with the inspection result.
- **Essential limit:** executable inventory and reachability accounting are
  incomplete. Graphics and platform compatibility services remain present, and
  the inference cannot be generalized beyond the examined path.

### C-009 — Startup settings and launcher contract

- **Machine ID and status:** `claim-settings-launcher-contract-observation`;
  observed.
- **Claim:** Source inspection and dedicated tests exercised the examined
  settings and launcher contract with an isolated disposable fake child,
  including held-path identity, argument and environment policy, descriptor
  closure, lifecycle handling, and marker-symbolic-link rejection.
- **Basis:** first-party source inspection and automated tests.
- **Would contradict this record:** execution of the private game rather than a
  fake child in the dedicated contract test, a listed check not actually
  exercised, or a retained test result inconsistent with the summarized pass.
- **Essential limit:** this is a fake-child source-and-test result, not live-game
  behavior, syscall monitoring, sandbox evidence, or filesystem-wide proof
  against transient copies.

### C-010 — Failed graphical recheck

- **Machine ID and status:** `claim-graphical-recheck-unresolved`; unresolved.
- **Claim:** The later graphical recheck did not pass its stated activity
  threshold, and the cause of the shortfall remains unresolved.
- **Basis:** required negative instrumented evidence from the exact recheck
  trials.
- **Would contradict this record:** retained records showing every stated trial
  met the threshold, absence of the recorded default-path stall, or a definitive
  cause that remains labeled unresolved.
- **Essential limit:** the failed recheck does not erase earlier artifact-bound
  records. The public package cannot determine its cause from the withheld logs.

### C-011 — Ambiguous earlier process ending

- **Machine ID and status:** `claim-shutdown-cause-unresolved`; unresolved.
- **Claim:** The cause of the earlier orphaned game process ending remains
  unresolved because its final process status was unavailable.
- **Basis:** a sanitized first-party process record.
- **Would contradict this record:** recovery of a trustworthy final
  game-process status and causal record, evidence that the game was not running
  after the process-control session ended, or presentation of the control
  session's status as the game's final status.
- **Essential limit:** the record supports neither a crash nor a non-crash
  conclusion. External session cleanup is a working hypothesis only.

### C-012 — Public proof verifier

- **Machine ID and status:** `claim-verifier-behavior-observation`; observed.
- **Claim:** The public standard-library verifier passed its valid baseline and
  rejected the exercised tampering, inventory, unsafe-path, evidence-linkage,
  status, scope, overreach, and negative-run-suppression cases.
- **Basis:** the public verifier, manifest, structured records, and test suite.
- **Would contradict this record:** failure of the published tests against the
  exact capsule, acceptance of a named adverse fixture, or rejection of the
  valid unmodified capsule.
- **Essential limit:** the tests cover only their enumerated cases and do not
  prove the verifier defect-free. Verifier behavior does not authenticate the
  truth of withheld evidence.

## Claims not made

Nothing in this ledger establishes:

- full-game translation or behavior;
- complete audiovisual, input, timing, or gameplay fidelity;
- absence of defects;
- absence of every interpretation or compatibility layer;
- independent reproduction of the private implementation;
- a conventional two-team clean-room process;
- lawful acquisition, dumping, translation, or publication as a legal
  conclusion; or
- permission to distribute the private implementation or third-party content.

The public verifier must fail closed if its machine-readable ledger, evidence
inventory, or required negative record no longer matches the release manifest.
