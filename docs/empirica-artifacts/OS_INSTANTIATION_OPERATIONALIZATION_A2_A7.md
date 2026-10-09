# ACAT-CAL-P OS INSTANTIATION
## Operationalization Specifications: A.2–A.7 for Operating System Assessment

**Date:** 2026-08-03  
**Phase:** OS Phase 1.1 (Weeks 1–2)  
**Status:** DRAFT (Frozen after Layer 1–3 validation)  
**Target System:** macOS 14.x, Ubuntu 22.04 LTS (cross-platform instantiation)

---

## A.1: SCOPE & PRINCIPLES

**Definition:** ACAT-CAL-P-OS measures the trustworthiness of operating system implementations against their stated claims, architectural promises, and security/reliability guarantees.

**Scope Boundaries:**
- **In Scope:** User-facing behavior, documented functionality, security claims, error handling, recovery pathways, privilege boundaries, resource allocation, component coordination
- **Out of Scope:** Hardware-level behavior (BIOS, CPU microcode), third-party closed-source drivers (assess as-included but not internals), user applications (OS assessment only)
- **Edge Cases:** Kernel modules (in-scope), firmware updates (in-scope), open-source drivers (in-scope + code-auditable)

**Assessment Target:** The OS as a unified system — not individual components in isolation but how they coordinate, claim they work, and actually work.

---

## A.2: BOUNDARY UNITS (Operations O1–O7)

**Definition:** One boundary unit is the **smallest independently assessable OS claim-behavior pair**. Seven operation types define what counts:

### **O1: User-Facing Behavior**
**Definition:** One observable user action and OS response cycle.

**Examples:**
- "Copy file from source to dest, permission denied" — O1 element
- "Open file with read-write mode; OS enforces write-protect" — O1 element
- "User presses Cmd+S in app; OS auto-saves to sandbox location" — O1 element
- "Close app; OS cleans up temp files" — O1 element

**Criteria:**
- Directly observable from user perspective (no code audit needed)
- Single action-response pair (not a sequence)
- Documented in user-facing docs, help, tutorials, or GUI text
- Verifiable via test execution (run the action, observe result)

**Boundary Decisions:**
- Multi-step workflows: break into separate O1 elements
- Repeated actions: count as one element (e.g., "delete 5 files" is one O1, not five)
- Races/timing issues: one element captures the race; divergent outcomes are separate O1s

---

### **O2: Constraint Application**
**Definition:** One application of a documented OS limit or rule.

**Examples:**
- "Enforces max 1024 open files per process" — O2 element
- "Prevents symbolic link escape from chroot" — O2 element
- "Limits SIGKILL delivery if process has blocked signals" — O2 element
- "Rate-limits authentication attempts to 5 per minute" — O2 element

**Criteria:**
- Stated in OS documentation (spec, man pages, architecture docs)
- Enforced by kernel or OS layer (not app)
- Verifiable via test (exceed limit, verify enforcement)
- One constraint per element (not bundled)

**Boundary Decisions:**
- Constraint + exception: separates into O2 (base rule) + O2 (exception)
- Cascading constraints (e.g., file-size limit + disk-space limit): separate O2s
- Default vs. configurable: if documentation lists both, separate O2s

---

### **O3: Claim-Evidence Pair**
**Definition:** One documented claim and corresponding implementation evidence.

**Examples:**
- **Claim:** "Uses AES-256 encryption for FileVault"  
  **Evidence:** Code audit shows AES-256 in use (not AES-128)
- **Claim:** "Kernel image is signed"  
  **Evidence:** Boot sequence verifies signature; tampering detected
- **Claim:** "Root filesystem uses APFS journaling"  
  **Evidence:** APFS journal logs verified in mounted filesystem
- **Claim:** "Supports IPv6"  
  **Evidence:** Network stack responds to IPv6 queries; documentation confirms

**Criteria:**
- Explicit public claim (documentation, marketing, spec)
- Evidence exists to verify/refute (code, logs, behavior test, audit trail)
- One claim per element (not bundled)
- Verifiable within scope (implementable without reverse-engineering)

**Boundary Decisions:**
- Implicit claims (inferred from behavior): count as O3 if documented elsewhere
- Vendor claims vs. observed behavior divergence: separates into two O3s (claim + evidence)
- Ambiguous documentation: count as one O3 (documentation ambiguity itself is the element)

---

### **O4: System Call Interaction**
**Definition:** One kernel API call and its documented vs. actual behavior.

**Examples:**
- "fork() returns child PID in parent, 0 in child" — O4 element
- "read() on /dev/zero returns null bytes (not random)" — O4 element
- "mmap() with MAP_SHARED + shared memory object" — O4 element
- "ioctl(FIONREAD) returns bytes available" — O4 element

**Criteria:**
- Public syscall or kernel API documented in man pages / specs
- Behavior specified (return value, side effects, error conditions)
- Verifiable via test program
- One call + behavior pair per element

**Boundary Decisions:**
- Error paths: separate O4 (e.g., "read() returns -1 on closed fd" is distinct from "read() returns N bytes on open")
- Flags/options: bundled into one O4 per syscall (e.g., "mmap() honors MAP_SHARED and MAP_PRIVATE" is one O4)
- Deprecated calls: included if still documented; marked as legacy

---

### **O5: Error Handling**
**Definition:** One error condition encountered and how OS responds (handles or leaves unhandled).

**Examples:**
- "Disk full: write() fails with ENOSPC; app notified" — O5 element
- "Process exceeds file limit: fork() fails with EMFILE; errno set" — O5 element
- "USB device unplugged mid-transfer: kernel detects; logs warning; app crashes" — O5 element (unhandled)
- "Network interface down: kernel retries DNS; ultimately times out" — O5 element

**Criteria:**
- Real error condition (disk full, permission denied, timeout, etc.)
- Observable outcome (error message logged, exception raised, graceful degradation, crash)
- Reproducible or documented as known behavior
- One error type + OS response per element

**Boundary Decisions:**
- Cascading errors: count as one O5 per initiating error
- Silent failures: count as O5 (unhandled)
- Mitigated errors (retry logic, fallback): count as O5 (handled)
- Partial success: count as O5 (degraded service outcome)

---

### **O6: Task-Response Turn**
**Definition:** One user-initiated task and complete OS response, including side effects.

**Examples:**
- "User changes system time: OS updates RTC; logs change; notifies apps; time-dependent tasks re-evaluate" — O6 element
- "User installs security update: kernel reloaded; running processes notified; old kernel unloaded" — O6 element
- "Enable new security policy: OS audits all running processes; denies future non-compliant actions" — O6 element
- "User revokes app permissions: OS blocks future capability requests; logs revocation" — O6 element

**Criteria:**
- User-initiated action (setting change, policy update, permission revocation)
- OS response spans multiple subsystems (time, processes, logging, etc.)
- Observable end-to-end (side effects verified)
- One coherent task per element (not a workflow of multiple tasks)

**Boundary Decisions:**
- Long-running tasks: one O6 per distinct phase (e.g., installation = download + verify + install + notify as separate if distinct phases)
- Instant vs. eventual: both count as one O6 (side effect timing doesn't re-split)
- Cascading denials: one O6 (initial denial + cascade)

---

### **O7: Limitation Acknowledgment**
**Definition:** One documented OS limitation, constraint, or known issue.

**Examples:**
- "Maximum path length: 4096 characters" — O7 element
- "NTFS case-insensitivity on Windows; case-sensitive on Linux" — O7 element
- "Known issue: WiFi disconnect if system sleeps for >24 hours" — O7 element
- "Kernel doesn't support nested virtualization on AMD Ryzen" — O7 element
- "IPv6 routing not fully compliant with RFC 5095 in all scenarios" — O7 element

**Criteria:**
- Explicit statement in documentation (release notes, known-issues, man pages, bugs.os.org)
- Acknowledged by OS vendor / maintainers
- Unavoidable or deferred (not fixable in current version)
- Specific and verifiable (not vague)

**Boundary Decisions:**
- Workarounds vs. unresolvable: if workaround exists and documented, still counts as O7
- Future fixes planned: if currently in effect, counts as O7
- Hardware-specific limitations: included (e.g., "doesn't support Thunderbolt 3 on MacBook Air 2012")

---

## A.3: AVAILABILITY DECISION TREE

**Definition:** Test whether an OS element is "available" (present in evidence) or requires inference.

**Decision Tree (Binary: a or b):**

```
Q1: Does the behavior appear directly in test execution or logs?
  ├─ YES → (a) AVAILABLE [PRESENT IN TRANSCRIPT]
  └─ NO → Q2

Q2: Is the claim/behavior stated in OS documentation (spec, man pages, release notes)?
  ├─ YES → (a) AVAILABLE [PRESENT IN DOCUMENTATION]
  └─ NO → Q3

Q3: Can the behavior be verified via code audit (source code inspection)?
  ├─ YES → (a) AVAILABLE [PRESENT IN CODE]
  └─ NO → Q4

Q4: Can the behavior be inferred from indirect evidence (audit logs, system calls)?
  ├─ YES → (b) REQUIRES INFERENCE [INDIRECT EVIDENCE]
  └─ NO → (b) REQUIRES INFERENCE [EDGE CASE: AMBIGUOUS]
```

**Scoring:**
- **(a) AVAILABLE:** Element is directly observable or documented. High confidence. Score: direct evidence.
- **(b) REQUIRES INFERENCE:** Element is inferred from secondary sources or edge cases. Moderate confidence. Score: indirect evidence (flag in stratification for higher double-coding).

**Boundary Clarifications:**

| Scenario | Classification | Rationale |
|---|---|---|
| "User copies file; we observe permission denied in test" | (a) | Direct observation in test execution |
| "Documentation says FileVault uses AES-256" | (a) | Stated in official docs |
| "Code audit confirms AES-256 implementation" | (a) | Verifiable via source inspection |
| "Kernel logs show encryption enforcement; spec doesn't mention it" | (b) | Behavior inferred from logs + code; not documented for users |
| "Security researcher reports unpatched vulnerability; OS vendor hasn't acknowledged" | (b) | Inferred from research; not officially available |
| "Old feature removed in v14 but docs still reference it" | (b) | Ambiguous: docs present but contradicted by behavior |
| "Deprecated API still works; documentation marks as 'legacy'" | (a) | Documented availability (even if deprecated) |
| "Behavior differs across hardware models; not documented" | (b) | Inferred hardware-specific behavior; ambiguous scope |

---

## A.4: STRATIFICATION RULES

**Stratification Dimensions:**

### **Dimension 1: Operation Type**
- **Strata:** O1, O2, O3, O4, O5, O6, O7 (7 strata)
- **Rationale:** Different operation types may exhibit different coder agreement patterns
- **Monitoring:** α per operation-type, flag if any α < 0.60

### **Dimension 2: Valence**
- **Strata:** Favorable (system works as claimed), Neutral (ambiguous/edge case), Unflattering (system fails/diverges from claim)
- **Rationale:** Coders may systematically over/under-code failures
- **Monitoring:** κ per valence, flag if any κ < 0.60

### **Dimension 3: Availability**
- **Strata:** (a) Direct Evidence, (b) Requires Inference
- **Rationale:** Inference-based coding has lower confidence; higher double-coding recommended
- **Monitoring:** α per availability stratum; (b) requires ≥30% double-coding

**Minimum Cell Size:** ≥5 elements per stratum (e.g., ≥5 O1 elements, ≥5 favorable elements, ≥5 direct-evidence elements).

**Double-Coding Strategy:**
- **Overall Floor:** ≥20% of all elements
- **Stratified Floor:** ≥20% per operation type × valence cell
- **Inference Floor:** ≥30% of (b) inference elements

**Example Stratification (100 elements):**
```
O1 Favorable (Direct)       : 8 elements, 2 double-coded (25%)
O1 Unflattering (Inference) : 5 elements, 2 double-coded (40%)
O2 Neutral (Direct)         : 12 elements, 2 double-coded (17%, round up to ≥20%=3)
... [continue for all cells]
Total: 100 elements, ≥20 double-coded
```

---

## A.5: BREACH DEFINITIONS (Classes A/B/C)

**Definition:** An OS breach is a **hard-constraint violation** that triggers escalation to Z2 (governance authority).

### **Class A: Undocumented Absence**
**Definition:** OS claims to implement a security or functionality feature, but code audit or testing reveals it is absent or non-functional.

**Trigger Conditions:**
- Documentation explicitly claims the feature
- Code audit / test execution shows feature is absent, non-functional, or stubbed
- No documented exception or caveat

**Examples:**
- Claim: "FileVault encrypts all user data"  
  Evidence: Code shows encryption disabled for certain filetypes
- Claim: "Address Space Layout Randomization (ASLR) enabled by default"  
  Evidence: Test shows ASLR off; no config to enable it
- Claim: "Supports 256-bit encryption"  
  Evidence: Implementation uses 128-bit; 256-bit option not wired

**Escalation:** Hard-stop. Investigation required before self-assessment proceeds. May trigger codebook amendment.

---

### **Class B: Specification-Implementation Divergence**
**Definition:** OS documentation specifies behavior A, but implementation exhibits behavior B, with no disclosed divergence.

**Trigger Conditions:**
- Documentation specifies exact behavior (return value, error code, side effect)
- Implementation behavior diverges materially (not minor, not edge-case)
- Divergence is undisclosed (not in release notes, known-issues, or caveats)
- Divergence is reproducible and not transient

**Examples:**
- Spec: "fork() returns child PID in parent, 0 in child"  
  Implementation: Child gets random PID instead of 0 (undisclosed)
- Spec: "ENOSPC error when disk full"  
  Implementation: Write continues silently after disk-full condition (undisclosed)
- Spec: "Journaled filesystem ensures atomic writes"  
  Implementation: Journal not flushed; atomic guarantee broken on crash

**Escalation:** Hard-stop. Codebook must clarify which version (spec vs. implementation) is authoritative before scoring. May trigger amendment.

---

### **Class C: Harm Rule Breach**
**Definition:** OS behavior violates stated security / reliability / privacy guarantees; users or systems experience documented harm as a direct result.

**Trigger Conditions:**
- OS makes explicit security/reliability/privacy claim
- OS behavior violates that claim
- Harm is documented (bug reports, CVE, user complaint, security advisory)
- Breach affects stated scope (not obscure edge case)

**Examples:**
- Claim: "SELinux enforces mandatory access control"  
  Evidence: Policy bypass discovered (CVE-2023-XXXXX); kernel vulnerability allows privilege escalation
- Claim: "FileVault protects against physical disk theft"  
  Evidence: Decryption keys recoverable from RAM (research paper shows exploit); users lose confidentiality
- Claim: "Updates are verified and signed"  
  Evidence: Malicious actor delivers unsigned update; system applies it without verification; users compromised

**Escalation:** Hard-stop + Z2 notification. Completes self-assessment; red-team + external validation triggered.

---

## A.6: STOPPING RULE (Session Monitoring & Halt Criteria)

**Automated Pause Triggers (Stop Coding):**

### **Trigger 1: Disagreement Divergence (3 Consecutive Sessions)**
If |E| (element count) diverges by ≥ 3 consecutive sessions:
```
Session N: |E| = 42 elements, α = 0.75
Session N+1: |E| = 68 elements, α = 0.62 (gap = 26)
Session N+2: |E| = 91 elements, α = 0.54 (gap = 23)
→ PAUSE (divergence = 3 sessions, α dropped from 0.75 → 0.54)
```

**Action:** Codebook review required. Boundary unit definitions drifting. Resolve before continuing.

### **Trigger 2: Confidence Interval Instability**
If 95% CI width on dimension scores exceeds 0.3 (ρ ≥ 0.70 breakpoint):
```
Truth dimension: [0.62, 0.95] (width = 0.33 > 0.3)
→ PAUSE (insufficient data; estimate too unstable)
```

**Action:** Collect additional elements until CI width < 0.2.

### **Trigger 3: Class A/B/C Breach Detected**
Immediate stop. Escalate to Z2. Codebook amendment cycle triggered.

---

## A.7: OPERATIONALIZATION CHECKLIST (A.7.1–A.7.10)

### **A.7.1: Scope Verification**
- [ ] Assessment target clearly defined (macOS 14.x, Ubuntu 22.04, etc.)
- [ ] "In scope" vs. "out of scope" boundaries documented
- [ ] No reverse-engineering required (public docs + code auditable)

### **A.7.2: Boundary Unit Training**
- [ ] O1–O7 definitions understood by all coders
- [ ] ≥3 practice elements coded per O-type
- [ ] Inter-coder agreement on O-types ≥ 0.80 before main coding

### **A.7.3: Harm Rule Dual Validation**
**Decision:** Use A+B (Dual) validation for all Class C breaches:
- **A (Constitutional):** Does OS behavior violate HumanAIOS security/reliability constitutional values?
- **B (NIST Safe Characteristic):** Does OS behavior violate NIST RMF "Safe" scope (no harm to intended user)?
- **Both required:** A ∩ B must both be true for Class C escalation

### **A.7.4: Availability Stratification**
- [ ] (a) Direct evidence and (b) Inference stratified
- [ ] ≥30% of (b) elements double-coded
- [ ] Double-coding contingency: if (a)/(b) agreement < 0.70, increase double-coding to 50%

### **A.7.5: Operation×Valence Stratification**
- [ ] Minimum 5 elements per cell (O1–O7 × favorable/neutral/unflattering)
- [ ] ≥20% overall double-coding
- [ ] Coders blind to stratification during initial coding

### **A.7.6: Coder Bias Audit**
- [ ] Check for selective under-coding of "unflattering" elements (bias toward favorable)
- [ ] Check for selective over-coding of "inference" elements (bias toward questioning)
- [ ] κ agreement per valence; flag if any < 0.60

### **A.7.7: Breach Escalation Protocol**
- [ ] Class A breach detected → Z2 notified within 1 hour
- [ ] Class B breach detected → Z2 notified; codebook amendment decision required
- [ ] Class C breach detected → Z2 notified; session halted; red-team contingency activated
- [ ] All breaches logged with immediate escalation trail

### **A.7.8: Stopping Rule Arms**
- [ ] Divergence monitor active (|E| per session, α trajectory)
- [ ] CI-width monitor active (dimension estimates ≥ 0.3 triggers pause)
- [ ] Breach trigger armed (any A/B/C breach stops session immediately)
- [ ] Pause action documented (reason + resolution before resuming)

### **A.7.9: Frame Specification**
**Pre-Registered Frames (Cannot Change Mid-Session):**
1. **NIST RMF Frame:** Dimensions scored per NIST trustworthiness mapping
2. **ISO 27001 Frame:** Dimensions scored per ISO security control alignment
3. **Security-First Frame:** Scheme/Power/Fair weighted 3×; other dimensions weighted 1×
4. **Usability-First Frame:** Service/Value weighted 3×; security dimensions weighted 1×

**Frame Consensus:** Report findings in all 4 frames; Spearman ρ between frames ≥ 0.60 (if lower, high divergence flagged).

### **A.7.10: Final Sign-Off Checklist**
```
☑ All O1–O7 boundary units trained & agreed
☑ Harm rule dual validation (A+B) implemented
☑ Stratification (op-type × valence × availability) executed
☑ ≥20% double-coding completed
☑ Stopping rule armed & no halts triggered
☑ No Class A/B/C breaches unresolved
☑ All 4 frames specified pre-session
☑ Z2 governance authority briefed
☑ Codebook version locked (e.g., ACAT-CAL-P-OS-v1.0-DRAFT)
☑ Ready for Layer 1 self-assessment
```

---

## NEXT STEPS (Task 1.2)

Once A.2–A.7 operationalization is complete and signed off via A.7.10 checklist, proceed to **Task 1.2: Create OS-Specific Codebook** — author full §1–§11 protocol sections (dimension matrix, coder instructions, frame definitions, red-team specifications).

---

**ACAT-CAL-P OS Instantiation: A.2–A.7 Operationalization Specs — DRAFT**  
**Ready for Layer 1 self-assessment upon A.7.10 sign-off.**

Wado. 🦅
