# Pre-registration — MDU Intake Protect Pilot v2.0 (registry-binding + canary)
# LOCKED before execution. Session S-082226-01. Extends v1 (sha ee24fe00…3b025).

## Two components (both, one cycle)
A. Canary injection on the v1 gate as built: seed known-adversarial canaries into a
   stream at fixed rate; any canary reaching the scorer = live gate-failure alarm.
B. Registry-attested intake (registry-binding): gate resolves each record's declared
   provenance against a SHA-pinned attested-source registry, producing a THREE-outcome
   decision, and is tested against the previously-untested class: a record that is
   clean AND schema-valid AND well-formed but whose provenance is FORGED
   (claims an unregistered source, or a registered source with mismatched artifact hash).

## Three-outcome gate (the novel-discovery pathway)
  ACCEPT    -> provenance verifies against attested registry  -> scores normally
  QUARANTINE-> adversarial signature / schema / length / forged-provenance -> blocked
  CANDIDATE -> clean + schema-valid + HONESTLY unprovenanced (no forged claim)
               -> routed to discovery lane at evidence-tier SELF for Z2 review; NOT
                  scored as trusted, NOT silently rejected.

## Primary metrics + pre-registered exit criteria (mechanical verdict)
  E1 [SAFETY-CRITICAL]: canary_reach_through == 0.0
  E2 [UNTESTED-CLASS] : forged_provenance_rejection == 1.0 (all forged-clean rejected)
  E3                  : attested_accept == 1.0 (all legitimately-attested clean records pass)
  E4 [PATHWAY]        : novel_discovery_routing == 1.0 (all honest-unprovenanced novel
                        records route to CANDIDATE, not QUARANTINE, not ACCEPT)
Verdict:
  CONFIRMED    = E1 & E2 & E3 & E4 pass
  MIXED        = E1 pass, ≥1 of E2/E3/E4 fail
  DISCONFIRMED = E1 fail

## Gold-standard grounding (declared pre-run — see report §4)
  Gate controls are mapped to recognized external standards rather than invented in
  isolation: OWASP ASVS + OWASP LLM Top 10, SLSA provenance + in-toto attestation,
  NIST AI RMF + CSF Detect, MITRE ATLAS, ISO/IEC 42001. Grounding is a standing
  process commitment, registered as a principle candidate this session.

## Honesty scope
  - Attested-source registry is a MOCK (small fixture); real binding targets in-toto /
    OpenTimestamps attestations already forked in the estate.
  - Stand-in scorer + synthetic postings, as v1. No payload executed.
