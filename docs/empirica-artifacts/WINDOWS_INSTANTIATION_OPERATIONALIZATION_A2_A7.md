# ACAT-CAL-P WINDOWS INSTANTIATION
## Operationalization Specifications: A.2–A.7 for Windows Operating System Assessment

**Date:** 2026-08-31 (Phase 2.1 Kickoff)  
**Status:** DRAFT (Frozen after Layer 1–4 validation)  
**Scope:** Windows Server 2022 + Windows 11 (latest patches)  
**Assessment Target:** Windows operating system as unified system — kernel (ntoskrnl), system services, driver coordination, user-facing behavior, security architecture, and documented claims

---

## A.1: SCOPE & PRINCIPLES

**Definition:** ACAT-CAL-P-Windows measures the trustworthiness of Windows operating system implementations against their stated claims, architectural promises, and security/reliability guarantees.

**Scope Boundaries:**
- **In Scope:** User-facing behavior, documented functionality, security claims, error handling, recovery pathways, privilege boundaries, resource allocation, component coordination, registry structure, driver interaction
- **Out of Scope:** Third-party closed-source drivers (assess as-shipped but not internals), user applications (Windows assessment only), hardware microcode (BIOS/CPU), non-English language editions (assess English builds)
- **Edge Cases:** Windows components with source available (some drivers, some services), legacy APIs (still documented, assessable), closed-source .NET runtime (Framework, not Core)

**Assessment Target:** Windows as a unified system — not individual components in isolation, but how kernel, services, and drivers coordinate, claim they work, and actually work.

---

## A.2: BOUNDARY UNITS (Operations O1–O7)

**Definition:** One boundary unit is the **smallest independently assessable Windows claim-behavior pair**. Seven operation types define what counts:

### **O1: User-Facing Behavior (Windows Desktop/Server UI)**

**Definition:** One observable user action and Windows response cycle.

**Windows-Specific Examples:**
- "Copy file from C:\Users\Documents to D:\Archive, NTFS permissions enforced" — O1 element
- "Right-click file, open Properties, verify file ownership matches current user" — O1 element
- "Enable Windows Update, system downloads patch, installs, prompts restart" — O1 element
- "User Account Control (UAC) prompt appears when running admin command as standard user" — O1 element
- "Close app (Ctrl+Q), Windows saves state to recovery database, app restarts to same state" — O1 element
- "Open file encrypted with EFS, Windows decrypts and displays content to authorized user" — O1 element
- "Network share access denied; Windows displays 'You do not have permission'" — O1 element

**Criteria:**
- Directly observable from user/admin perspective (no kernel debugging needed)
- Single action-response pair (not a multi-step workflow)
- Documented in Windows docs, Help, Microsoft knowledge base, or official guides
- Verifiable via test execution (GUI interaction, PowerShell cmdlets, file operations)

**Boundary Decisions:**
- Multi-step workflows: break into separate O1 elements
- Batch operations: count as one element (e.g., "copy 5 files to network share" is one O1)
- Race conditions/timing: one element captures the race; divergent outcomes are separate O1s

**Windows-Context Notes:**
- UAC prompts (elevation requests) are O1
- File operation dialogs (copy, move, delete progress) are O1
- System tray notifications are O1
- Registry Editor interactions are O1
- Settings app changes are O1

---

### **O2: Constraint Application (Windows Limits & Rules)**

**Definition:** One application of a documented Windows limit or rule.

**Windows-Specific Examples:**
- "NTFS enforces 255-character filename limit (per file, not full path)" — O2 element
- "Windows enforces max 260 characters in file path (extended to 32K with special prefix)" — O2 element
- "Registry key name limited to 255 characters; REG_SZ value limited to 2048 chars" — O2 element
- "Process can open max 1,024 handles (configurable via registry); exceeding limit fails" — O2 element
- "Windows Event Log files rotate after 20 MB or 7 days (configurable)" — O2 element
- "NTFS supports max 4 billion files per volume" — O2 element
- "Active Directory object name limited to 64 characters" — O2 element
- "Service dependency limit (max 2,000 characters in service dependency string)" — O2 element

**Criteria:**
- Stated in official Windows documentation (Microsoft docs, TechNet, man pages, registry reference)
- Enforced by kernel or Windows system layer (not application)
- Verifiable via test (exceed limit, verify enforcement via error message or behavior change)
- One constraint per element (not bundled)

**Boundary Decisions:**
- Constraint + exception: separates into O2 (base rule) + O2 (exception)
- Soft vs. hard limits: both count (e.g., recommended max process count is O2; hard max file handles is O2)
- Configurable limits: if documented, count (e.g., "default 1024, configurable to 32K")

**Windows-Context Notes:**
- Registry hive size limit: 1 GB (soft), ~4 GB (hard)
- Max partition size: 16 EB (NTFS)
- Max file size: 16 EB (NTFS)
- Active Directory forest functional levels (each level has constraint set)
- Group Policy Object limit: ~16 MB uncompressed

---

### **O3: Claim-Evidence Pair (Windows Documentation vs. Reality)**

**Definition:** One documented claim and corresponding implementation evidence.

**Windows-Specific Examples:**
- **Claim:** "Windows Defender provides real-time malware protection"  
  **Evidence:** Code audit shows real-time scanning engine; test shows files scanned on access
- **Claim:** "BitLocker encrypts entire volume with AES-128 or AES-256"  
  **Evidence:** Code inspection confirms AES algorithm; encrypted volume verified via key recovery impossibility
- **Claim:** "NTFS supports file permissions (DACL, SACL)"  
  **Evidence:** File system shows ACL storage; permission enforcement verified via test
- **Claim:** "Windows Update can be deferred for up to 35 days"  
  **Evidence:** Documentation states deferral policy; test confirms updates not applied within deferral window
- **Claim:** "Secure Boot prevents unsigned drivers from loading"  
  **Evidence:** Code inspection, Secure Boot logs, test with unsigned driver (fails to load)
- **Claim:** "Credential Guard protects credentials in isolated container"  
  **Evidence:** Architecture documentation, Hyper-V isolation verification, credential theft test
- **Claim:** "Windows Event Log is tamper-proof (with appropriate permissions)"  
  **Evidence:** Audit trail protection mechanism, admin-level event deletion attempt (fails or logged)

**Criteria:**
- Explicit public claim (Microsoft docs, marketing, security documentation)
- Evidence exists to verify/refute (code audit, logs, behavior test, configuration inspection)
- One claim per element (not bundled)
- Verifiable within scope (implementable without proprietary/closed-source reversal)

**Boundary Decisions:**
- Implicit claims (inferred from behavior): count as O3 if documented elsewhere
- Vendor claims vs. observed behavior divergence: separates into two O3s (claim + evidence mismatch)
- Ambiguous documentation: count as one O3 (documentation ambiguity itself is the element)

**Windows-Context Notes:**
- Kernel-level claims (interrupt handling, memory management)
- Service-level claims (Svchost process pooling, service dependencies)
- Security claims (DEP, ASLR, CFG enablement)
- Driver signing requirements (kernel-mode code signing)

---

### **O4: System Call/API Interaction (Windows API Behavior)**

**Definition:** One kernel API call (syscall or Win32 API) and its documented vs. actual behavior.

**Windows-Specific Examples:**
- "CreateFileW returns HANDLE or INVALID_HANDLE_VALUE; succeeds if file exists" — O4 element
- "ReadFile returns bytes read in OUT parameter; sets ERROR_HANDLE_EOF if past EOF" — O4 element
- "RegOpenKeyEx returns ERROR_FILE_NOT_FOUND if key doesn't exist" — O4 element
- "CreateProcessW with dwCreationFlags=CREATE_SUSPENDED pauses new process before execution" — O4 element
- "GetLastError returns error code from last failed API call (not thread-safe if cross-thread)" — O4 element
- "SetFileAttributes silently succeeds even if file doesn't exist (no error returned)" — O4 element
- "GetFileAttributesEx returns FILE_ATTRIBUTE_DIRECTORY for directories, FILE_ATTRIBUTE_ARCHIVE for files" — O4 element
- "OpenProcessToken with TOKEN_READ succeeds only if caller has SeDebugPrivilege (or same user)" — O4 element

**Criteria:**
- Public API documented in Microsoft documentation (MSDN, docs.microsoft.com)
- Behavior specified (return value, side effects, error conditions, thread safety)
- Verifiable via test program
- One call + behavior pair per element

**Boundary Decisions:**
- Error paths: separate O4 (e.g., "CreateFileW succeeds on existing file" vs. "CreateFileW fails on non-existent file")
- Flags/options: bundled into one O4 per API call (e.g., "CreateFileW honors CREATE_NEW, CREATE_ALWAYS, OPEN_EXISTING flags")
- Deprecated APIs: included if still documented; marked as legacy

**Windows-Context Notes:**
- Win32 API (user-mode): CreateFile, ReadFile, WriteFile, RegOpenKeyEx, GetFileAttributes, etc.
- Syscalls (kernel-mode): NtCreateFile, NtReadFile (low-level, fewer documented)
- COM APIs (Component Object Model): CoCreateInstance, QueryInterface, etc.
- Active Directory APIs: LDAP calls, directory binding, object modification

---

### **O5: Error Handling (Windows Error Responses)**

**Definition:** One error condition encountered and how Windows responds (handles or leaves unhandled).

**Windows-Specific Examples:**
- "Disk full: WriteFile returns FALSE, GetLastError returns ERROR_DISK_FULL; app notified" — O5 element
- "Access Denied: CreateFileW returns INVALID_HANDLE_VALUE, GetLastError returns ERROR_ACCESS_DENIED" — O5 element
- "File In Use: DeleteFileW returns FALSE, GetLastError returns ERROR_SHARING_VIOLATION" — O5 element
- "Registry key access denied: RegOpenKeyEx returns ERROR_ACCESS_DENIED; access not granted" — O5 element
- "Out of Memory: malloc returns NULL or throws exception (depending on CRT settings)" — O5 element
- "Process exceeds quota: CreateProcessW fails with ERROR_NOT_ENOUGH_MEMORY" — O5 element
- "Network connection lost: Winsock API returns WSAECONNRESET; connection object invalid" — O5 element
- "Device disconnected mid-transfer: ReadFile returns incomplete data; GetLastError set" — O5 element

**Criteria:**
- Real error condition (disk full, permission denied, timeout, resource exhaustion, etc.)
- Observable outcome (error code logged, exception raised, graceful degradation, crash)
- Reproducible or documented as known behavior
- One error type + Windows response per element

**Boundary Decisions:**
- Cascading errors: count as one O5 per initiating error
- Silent failures: count as O5 (unhandled, no error notification)
- Mitigated errors (retry logic, fallback): count as O5 (handled gracefully)
- Partial success: count as O5 (degraded service outcome)

**Windows-Context Notes:**
- Win32 error codes (ERROR_* constants, 0–15,000 range)
- Winsock errors (WSAE* constants, 10,000+ range)
- HRESULT codes (COM errors, facility + code)
- NTSTATUS codes (kernel-level, NT*_* constants)

---

### **O6: Task-Response Turn (Windows System Operations)**

**Definition:** One user-initiated or system-initiated task and complete Windows response, including side effects.

**Windows-Specific Examples:**
- "User runs Windows Update: OS downloads patches, verifies signatures, installs, updates registry, schedules restart" — O6 element
- "Enable BitLocker: OS generates recovery key, encrypts volume, updates boot manager, displays completion" — O6 element
- "User changes system time: OS updates RTC, adjusts file timestamps, notifies time-dependent services (Kerberos, etc.)" — O6 element
- "Plug in USB device: Windows detects, searches drivers, installs/loads driver, mounts volume, notifies Safely Remove" — O6 element
- "User revokes app permissions (microphone): Windows blocks future microphone access, logs revocation, app receives error on next attempt" — O6 element
- "Join domain: Windows contacts DC, creates computer account, stores credentials in LSA, configures Group Policy, restarts" — O6 element
- "Restart in Safe Mode: Windows loads minimal drivers, disables services, boots to safe desktop" — O6 element
- "Enable Windows Defender: Service starts, schedules first scan, registers event log, configures auto-updates" — O6 element

**Criteria:**
- User-initiated action (setting change, policy update, permission revocation, device plugging) OR system-initiated (scheduled task, event response)
- Windows response spans multiple subsystems (services, registry, event log, file system, etc.)
- Observable end-to-end (side effects verified)
- One coherent task per element (not a workflow of multiple tasks)

**Boundary Decisions:**
- Long-running tasks: one O6 per distinct phase (e.g., installation = download + verify signature + install system files + register services)
- Instant vs. eventual: both count as one O6 (side effect timing doesn't re-split)
- Cascading operations: one O6 (initial action + cascade)

**Windows-Context Notes:**
- Windows Update cycle (download → install → restart → verification)
- Driver installation (detection → search → install → load → device enumeration)
- Service start/stop (permission check → dependencies loaded → service started → registry updated)
- Group Policy application (fetch from DC → parse → apply to registry/file system → log)

---

### **O7: Limitation Acknowledgment (Windows Known Issues & Constraints)**

**Definition:** One documented Windows limitation, constraint, or known issue.

**Windows-Specific Examples:**
- "Maximum path length: 260 characters (can be extended to 32K with special prefix; not all APIs support this)" — O7 element
- "NTFS is case-insensitive for display but case-preserving internally; can cause issues with Unix software" — O7 element
- "Known issue: Windows Update can hang if disk space < 5 GB; workaround is to free space" — O7 element
- "Kerberos doesn't support pre-authentication across forest trusts; requires KDC to forward" — O7 element
- "IPv6 routing table size limited to 2 million routes (can be changed via registry; undocumented)" — O7 element
- "SMB v1 disabled by default in Server 2019+ for security reasons; legacy clients must enable" — O7 element
- "Group Policy update can take 90 seconds on slow networks; immediate update via gpupdate not guaranteed" — O7 element
- "Windows Sandbox can't access GPU; only supports CPU rendering" — O7 element

**Criteria:**
- Explicit statement in documentation (Microsoft Docs, KB articles, release notes, known-issues lists)
- Acknowledged by Microsoft/Windows team
- Unavoidable or deferred (not fixable in current version, or workaround documented)
- Specific and verifiable (not vague)

**Boundary Decisions:**
- Workarounds vs. unresolvable: if workaround exists and documented, still counts as O7
- Future fixes planned: if currently in effect, counts as O7
- Hardware-specific limitations: included (e.g., "Windows 11 requires TPM 2.0; older systems unsupported")

**Windows-Context Notes:**
- .NET Framework compatibility issues
- Driver incompatibility with newer Windows versions
- Registry size/depth limitations
- Active Directory replication timing
- Group Policy replication delays

---

## A.3: AVAILABILITY DECISION TREE

**Definition:** Test whether a Windows element is "available" (present in evidence) or requires inference.

**Decision Tree (Binary: a or b):**

```
Q1: Does the behavior appear directly in test execution or logs (Event Viewer)?
  ├─ YES → (a) AVAILABLE [PRESENT IN EXECUTION/LOGS]
  └─ NO → Q2

Q2: Is the claim/behavior stated in Windows documentation (Microsoft Docs, KB)?
  ├─ YES → (a) AVAILABLE [PRESENT IN DOCUMENTATION]
  └─ NO → Q3

Q3: Can the behavior be verified via code audit (source inspection, disassembly)?
  ├─ YES → (a) AVAILABLE [PRESENT IN CODE]
  └─ NO → Q4

Q4: Can the behavior be inferred from indirect evidence (registry inspection, WMI queries)?
  ├─ YES → (b) REQUIRES INFERENCE [INDIRECT EVIDENCE]
  └─ NO → (b) REQUIRES INFERENCE [AMBIGUOUS/UNDOCUMENTED]
```

**Scoring:**
- **(a) AVAILABLE:** Element is directly observable or documented. High confidence. Score: direct evidence.
- **(b) REQUIRES INFERENCE:** Element is inferred from secondary sources or undocumented behavior. Moderate confidence. Score: indirect evidence (flag in stratification for higher double-coding).

**Boundary Clarifications:**

| Scenario | Classification | Rationale |
|---|---|---|
| "User copies file; we observe permission denied in File Explorer" | (a) | Direct observation in test execution |
| "Documentation says BitLocker uses AES-256 by default" | (a) | Stated in official docs |
| "Code audit confirms AES-256 implementation in BitLocker" | (a) | Verifiable via source inspection |
| "Event Viewer shows file creation audit event; spec doesn't mention it" | (b) | Behavior inferred from logs; not documented for users |
| "Security researcher reports UAC bypass; Microsoft hasn't acknowledged" | (b) | Inferred from research; not officially available |
| "Old documentation mentioned NTFS 5.0; newer docs removed it" | (b) | Ambiguous: docs present but contradicted by behavior |
| "Deprecated API still works; documentation marks as 'legacy'" | (a) | Documented availability (even if deprecated) |
| "Behavior differs across Windows versions; not documented" | (b) | Inferred version-specific behavior; ambiguous scope |

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

---

## A.5: BREACH DEFINITIONS (Classes A/B/C)

### **Class A: Undocumented Absence**
**Definition:** Windows claims to implement a security or functionality feature, but code audit or testing reveals it is absent or non-functional.

**Examples:**
- Claim: "Windows Defender scans all files in real-time"  
  Evidence: Code shows real-time scanning disabled; manual scans only
- Claim: "UAC prevents privilege escalation"  
  Evidence: Code audit finds UAC bypass; unsigned process can elevate to admin

**Escalation:** Hard-stop. Investigation required before self-assessment proceeds.

### **Class B: Specification-Implementation Divergence**
**Definition:** Windows documentation specifies behavior A, but implementation exhibits behavior B, with no disclosed divergence.

**Examples:**
- Spec: "CreateFileW returns HANDLE or INVALID_HANDLE_VALUE"  
  Implementation: Returns HANDLE value but never INVALID_HANDLE_VALUE; returns NULL instead
- Spec: "ERROR_DISK_FULL returned when disk full"  
  Implementation: WriteFile continues silently after disk-full condition

**Escalation:** Hard-stop. Codebook must clarify which version (spec vs. implementation) is authoritative.

### **Class C: Harm Rule Breach** (Dual Validation Required)
**Definition:** Windows behavior violates stated security/reliability/privacy guarantee; users/systems experience documented harm as direct result.

**Examples:**
- Claim: "BitLocker protects against physical disk theft"  
  Evidence: Encryption keys recoverable from DRAM; BitLocker bypass documented
- Claim: "Windows Update is verified and signed"  
  Evidence: Malicious actor delivers unsigned update; system applies without verification

**Escalation:** Hard-stop + Z2 notification. Dual-harm validation (A+B) required.

---

## A.7: OPERATIONALIZATION CHECKLIST (A.7.1–A.7.10)

### **A.7.1: Scope Verification**
- [ ] Assessment target clearly defined (Windows Server 2022, Windows 11, versions)
- [ ] "In scope" vs. "out of scope" boundaries documented
- [ ] No reverse-engineering required (public docs + open-source where available)

### **A.7.2: Boundary Unit Training**
- [ ] O1–O7 definitions understood by all coders
- [ ] ≥3 practice elements coded per O-type (21 test elements minimum)
- [ ] Inter-coder agreement on O-types ≥ 0.80 before main coding

### **A.7.3: Harm Rule Dual Validation**
- [ ] Class C breaches require A (Constitutional) + B (NIST Safe) validation
- [ ] Both A and B must be true for escalation
- [ ] Misalignment documented (informs future protocol evolution)

### **A.7.4: Availability Stratification**
- [ ] (a) Direct evidence and (b) Inference stratified
- [ ] ≥30% of (b) elements double-coded
- [ ] If agreement < 0.70 between (a) and (b) coders, increase double-coding to 50%

### **A.7.5: Operation×Valence Stratification**
- [ ] Minimum 5 elements per cell (O1–O7 × favorable/neutral/unflattering)
- [ ] ≥20% overall double-coding
- [ ] Coders blind to stratification during initial coding

### **A.7.6: Coder Bias Audit**
- [ ] Check for selective under-coding of "unflattering" elements
- [ ] Check for selective over-coding of "inference" elements
- [ ] κ agreement per valence; flag if any < 0.60

### **A.7.7: Breach Escalation Protocol**
- [ ] Class A breach detected → Z2 notified within 1 hour
- [ ] Class B breach detected → Z2 notified; codebook amendment decision required
- [ ] Class C breach detected → Z2 notified; session halted; red-team contingency activated

### **A.7.8: Stopping Rule Arms**
- [ ] Divergence monitor active (|E| per session, α trajectory)
- [ ] CI-width monitor active (dimension estimates ≥ 0.3 triggers pause)
- [ ] Breach trigger armed (any A/B/C breach stops session immediately)

### **A.7.9: Frame Specification**
**Pre-Registered Frames (Cannot Change Mid-Session):**
1. **NIST RMF Frame:** Dimensions scored per NIST trustworthiness mapping
2. **CIS Benchmarks Frame:** Dimensions scored per CIS Windows Security Baseline
3. **Microsoft Security Frame:** Dimensions scored per Microsoft Security Best Practices
4. **Administrator Frame:** Dimensions weighted toward admin control and observability

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
☑ Codebook version locked (e.g., ACAT-CAL-P-Windows v1.0-DRAFT)
☑ Ready for Layer 1 self-assessment
```

---

## NEXT STEPS (Task 2.2)

Once A.2–A.7 operationalization is complete and signed off via A.7.10 checklist, proceed to **Task 2.2: Windows §2 Crosswalk** — map Windows dimensions to NIST RMF + CIS Benchmarks + Microsoft Security Baseline.

---

**ACAT-CAL-P WINDOWS INSTANTIATION: A.2–A.7 Operationalization Specs — DRAFT**  
**Ready for §2 crosswalk upon A.7.10 sign-off.**

Wado. 🦅
