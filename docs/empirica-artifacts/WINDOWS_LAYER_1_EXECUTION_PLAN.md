# WINDOWS LAYER 1 SELF-ASSESSMENT
## Execution Plan & Coding Strategy

**Date:** 2026-09-13 (Phase 2.3 Planning)  
**Status:** PLAN READY (Awaiting coder team assignment)  
**Duration:** Weeks 4–5 (2026-09-21 to 2026-10-04)  
**Target:** 120 elements coded, coherence ≥ 0.85, κ ≥ 0.60 overall

---

## PART I: LAYER 1 OVERVIEW

### **Purpose**
Layer 1 self-assessment establishes baseline Windows trustworthiness using the 12-dimension ACAT-CAL-P framework operationalized in §1–§7 codebook. Results feed into Layer 2 external validation (NIST/CIS), Layer 3 evaluator assessment, and Layer 4 red-team stress tests.

### **Success Criteria**
1. ✓ All 120 elements coded (O1–O7 stratified)
2. ✓ Coherence score ≥ 0.85 (0–1.0 scale, average of 12 dimensions)
3. ✓ Per-dimension scores: each ≥ 0.70 (no severely low dimensions)
4. ✓ Overall κ agreement ≥ 0.60 (minimum acceptable inter-rater reliability)
5. ✓ No Class A/B/C breaches unresolved (escalation protocol honored)
6. ✓ Stopping rules armed; no threshold breaches that halted assessment

### **Coherence Gate**
**Definition:** Average of all 12 dimension scores across all 120 coded elements.

**Example:** If dimensions score: Truth 0.89, Service 0.87, Harm 0.88, Autonomy 0.85, Value 0.86, Humility 0.84, Scheme 0.87, Power 0.88, Syc 0.85, Consist 0.89, Fair 0.86, Handoff 0.85 → Coherence = 0.866 ✓ PASS (≥ 0.85)

**Interpretation:** Coherence ≥ 0.85 means Windows operating system exhibits consistent, high trustworthiness across dimensions. No single dimension is severely compromised.

---

## PART II: 120-ELEMENT SOURCING STRATEGY

### **Element Allocation by Operation Type**

| O-Type | Count | Favorable | Neutral | Unflattering | (a) Direct | (b) Inference |
|---|---|---|---|---|---|---|
| **O1: User-Facing** | 20 | 8 | 6 | 6 | 14 | 6 |
| **O2: Constraints** | 18 | 6 | 6 | 6 | 12 | 6 |
| **O3: Claim-Evidence** | 18 | 8 | 5 | 5 | 12 | 6 |
| **O4: API Behavior** | 18 | 8 | 5 | 5 | 14 | 4 |
| **O5: Error Handling** | 16 | 4 | 6 | 6 | 10 | 6 |
| **O6: Task-Response** | 18 | 10 | 5 | 3 | 14 | 4 |
| **O7: Limitations** | 12 | 0 | 8 | 4 | 6 | 6 |
| **TOTAL** | **120** | **44** | **41** | **35** | **82** | **38** |

### **Sourcing Instructions by Operation Type**

#### **O1: User-Facing Behavior (20 elements)**

**Sources:** Live Windows system (GUI, PowerShell, Settings app), Microsoft Docs (feature documentation)

**Examples to Source:**

| # | Element | Source | Verification Method | Valence |
|---|---|---|---|---|
| O1.1 | Copy file from local to network share; NTFS permissions enforced | Test: File Explorer copy operation | Verify permission denied in error dialog | Favorable |
| O1.2 | Right-click file → Properties → verify file ownership shows current user | Test: File Explorer GUI | Inspect Ownership tab | Favorable |
| O1.3 | Enable Windows Update; system downloads + installs patch + prompts restart | Test: Settings app → Update | Monitor update progress; verify restart notification | Favorable |
| O1.4 | UAC prompt appears when running admin command as standard user | Test: PowerShell "runas /user:admin" or GUI elevation | Screenshot UAC prompt dialog | Favorable |
| O1.5 | Close app (Ctrl+Q); Windows saves state to recovery database; app restarts to same state | Test: Open app, make changes, close, reopen | Verify state recovered (if app supports recovery) | Favorable |
| O1.6 | Network share access denied; Windows displays "You do not have permission" | Test: Attempt access to restricted share | Observe error message in File Explorer | Unflattering |
| O1.7 | File encrypted with EFS; Windows decrypts and displays to authorized user | Test: Create EFS file, access with authorized account | Verify decryption works; decrypt file contents | Favorable |
| O1.8 | Settings app occasionally lags when loading large settings pages | Test: Open Settings, navigate to System → Storage | Observe load time; measure responsiveness | Unflattering |
| ... (12 more) | ... | ... | ... | ... |

**Coder Instructions for O1:**
1. Access live Windows 11 or Server 2022 test environment
2. Execute described user action
3. Observe system response; take screenshots/logs
4. Document evidence (what happened, error messages, UI state)
5. Code element per 12 dimensions (Truth, Service, Harm, etc.)
6. Mark availability: (a) Direct (observed in test) or (b) Inference (inferred from behavior)

---

#### **O2: Constraints Application (18 elements)**

**Sources:** Microsoft Docs (technical reference, limits/quotas), NTFS specification, registry reference

**Examples to Source:**

| # | Element | Source | Verification Method | Valence |
|---|---|---|---|---|
| O2.1 | NTFS enforces 255-character filename limit per file (not full path) | Microsoft Docs: "File Naming Limitations" | Test: Create file with 260+ chars; verify error | Favorable |
| O2.2 | Windows enforces max 260 characters in file path (extended to 32K with special prefix) | Microsoft Docs: "Maximum Path Length Limitation" | Test: Create deep directory; verify path limit | Favorable |
| O2.3 | Registry key name limited to 255 characters | Microsoft Docs: Registry reference | Test: Create registry key with 256+ chars; verify error | Favorable |
| O2.4 | REG_SZ value limited to 2048 characters | Microsoft Docs: Registry value types | Test: Set REG_SZ > 2048 chars; verify truncation/error | Favorable |
| O2.5 | Process can open max 1,024 handles (configurable via registry) | Microsoft Docs: "Process Handle Limit" | Test: Open 1,024+ handles; verify exceeding limit fails | Favorable |
| O2.6 | Windows Event Log files rotate after 20 MB or 7 days (configurable) | Windows Event Viewer settings | Test: Fill event log; observe rotation | Favorable |
| O2.7 | NTFS supports max 4 billion files per volume | Microsoft Docs: NTFS specifications | Test: Verify file count limit (difficult to test; documentation sufficient) | Neutral |
| O2.8 | Active Directory object name limited to 64 characters | Microsoft Docs: AD limitations | Test: Create AD object with 65+ char name; verify error | Favorable |
| ... (10 more) | ... | ... | ... | ... |

**Coder Instructions for O2:**
1. Locate limit in Microsoft Docs (or system reference)
2. If testable: run test to verify limit (create object exceeding limit; verify error)
3. If not testable: document from official source; mark as (b) Inference
4. Code element per 12 dimensions
5. Assess whether limit is reasonable, documented, enforced consistently

---

#### **O3: Claim-Evidence Pairs (18 elements)**

**Sources:** Microsoft Docs (feature claims), security documentation, code audit (where available), test results

**Examples to Source:**

| # | Claim | Source of Claim | Evidence Source | Valence |
|---|---|---|---|---|
| O3.1 | "Windows Defender provides real-time malware protection" | Microsoft Docs: Defender feature page | Test: Enable Defender; copy known malware sample; verify quarantine | Favorable |
| O3.2 | "BitLocker encrypts entire volume with AES-128 or AES-256" | Microsoft Docs: BitLocker tech spec | Code audit: Cipher algorithm verification; test: encrypt & verify | Favorable |
| O3.3 | "NTFS supports file permissions (DACL, SACL)" | Microsoft Docs: NTFS features | File system inspection: Verify ACL storage; permission enforcement test | Favorable |
| O3.4 | "Windows Update can be deferred for up to 35 days" | Microsoft Docs: Update deferral policy | Test: Set deferral to 35 days; verify updates not applied within window | Favorable |
| O3.5 | "Secure Boot prevents unsigned drivers from loading" | Microsoft Docs: Secure Boot specification | Test: Attempt unsigned driver load; verify failure; check Secure Boot logs | Favorable |
| O3.6 | "Credential Guard protects credentials in isolated container" | Microsoft Docs: Credential Guard overview | Architecture doc inspection; test: attempt credential theft; verify isolation | Favorable |
| O3.7 | "Windows Event Log is tamper-proof with appropriate permissions" | Microsoft Docs: Event Log security | Test: Admin attempts to delete event; verify audit trail or failure | Favorable |
| O3.8 | "UAC prevents privilege escalation" | Microsoft Docs: UAC overview | Security research: UAC bypass vulnerabilities documented | Unflattering |
| ... (10 more) | ... | ... | ... | ... |

**Coder Instructions for O3:**
1. Locate official Microsoft claim (documentation, feature page, KB article)
2. Find evidence (code, test, documentation of implementation, security research)
3. Compare claim vs. evidence: do they align?
4. Code element per 12 dimensions
5. If divergence found: document as potential Class B breach; flag for Z2 review

---

#### **O4: System Call/API Interaction (18 elements)**

**Sources:** MSDN (Win32 API reference), system headers, test programs

**Examples to Source:**

| # | API Call | Documented Behavior | Test Protocol | Valence |
|---|---|---|---|---|
| O4.1 | CreateFileW | Returns HANDLE or INVALID_HANDLE_VALUE; succeeds if file exists | Test: Open existing file; verify HANDLE returned | Favorable |
| O4.2 | ReadFile | Returns bytes read in OUT parameter; sets ERROR_HANDLE_EOF if past EOF | Test: Read file to EOF; verify error code | Favorable |
| O4.3 | RegOpenKeyEx | Returns ERROR_FILE_NOT_FOUND if key doesn't exist | Test: Open nonexistent registry key; verify error | Favorable |
| O4.4 | CreateProcessW with dwCreationFlags=CREATE_SUSPENDED | Pauses new process before execution; process can be resumed | Test: Create suspended process; verify it doesn't run; resume it | Favorable |
| O4.5 | GetLastError | Returns error code from last failed API call (NOT thread-safe across threads) | Test: Generate error in one thread; verify GetLastError in another thread | Neutral |
| O4.6 | SetFileAttributes | Silently succeeds even if file doesn't exist (no error returned) | Test: SetFileAttributes on nonexistent file; verify no error | Unflattering |
| O4.7 | GetFileAttributesEx | Returns FILE_ATTRIBUTE_DIRECTORY for directories, FILE_ATTRIBUTE_ARCHIVE for files | Test: Query both file and directory; verify attributes | Favorable |
| O4.8 | OpenProcessToken with TOKEN_READ | Succeeds only if caller has SeDebugPrivilege (or same user) | Test: Non-admin opens process token; verify failure | Favorable |
| ... (10 more) | ... | ... | ... | ... |

**Coder Instructions for O4:**
1. Locate API in MSDN (official documentation)
2. Write/run test program to verify behavior
3. Compare documented vs. actual behavior
4. Code element per 12 dimensions
5. If behavior diverges from docs: flag as potential Class B breach

---

#### **O5: Error Handling (16 elements)**

**Sources:** Test environment (generate errors intentionally), Event Viewer (error logs), Microsoft Docs (error code reference)

**Examples to Source:**

| # | Error Condition | How to Generate | Expected Response | Valence |
|---|---|---|---|---|
| O5.1 | Disk full | Fill disk to 100%; attempt write | WriteFile returns FALSE; GetLastError = ERROR_DISK_FULL | Favorable |
| O5.2 | Access Denied | Attempt to read file without permissions | CreateFileW returns INVALID_HANDLE_VALUE; GetLastError = ERROR_ACCESS_DENIED | Favorable |
| O5.3 | File In Use | Delete file that process has open | DeleteFileW returns FALSE; GetLastError = ERROR_SHARING_VIOLATION | Favorable |
| O5.4 | Registry key access denied | Attempt to open protected registry key without admin | RegOpenKeyEx returns ERROR_ACCESS_DENIED | Favorable |
| O5.5 | Out of Memory | Allocate huge memory block (malloc/new) | malloc returns NULL or throws exception | Favorable |
| O5.6 | Process exceeds quota | Create processes beyond limit | CreateProcessW fails with ERROR_NOT_ENOUGH_MEMORY | Favorable |
| O5.7 | Network connection lost | Disconnect network mid-transfer | Winsock API returns WSAECONNRESET | Favorable |
| O5.8 | Device disconnected mid-transfer | Unplug USB device during file copy | ReadFile returns incomplete data; error logged | Favorable |
| ... (8 more) | ... | ... | ... | ... |

**Coder Instructions for O5:**
1. Set up test environment to generate error condition
2. Execute operation that triggers error
3. Observe Windows response (error code, event log, GUI message)
4. Document how error is handled (gracefully, with recovery, crash, etc.)
5. Code element per 12 dimensions
6. Assess: Is error handling robust? Are users/admins informed?

---

#### **O6: Task-Response Turn (18 elements)**

**Sources:** Test environment (multi-step operations), Event Viewer (side effects logged), system state inspection

**Examples to Source:**

| # | Task | Steps | Side Effects | Valence |
|---|---|---|---|---|
| O6.1 | Windows Update | 1. Run Windows Update 2. Download patches 3. Verify signatures 4. Install 5. Update registry 6. Schedule restart | OS downloads patches; registry updated; restart scheduled/notified; Event Log records | Favorable |
| O6.2 | Enable BitLocker | 1. Open Device Encryption settings 2. Turn on BitLocker 3. Generate recovery key 4. Encrypt volume 5. Update boot manager | Recovery key generated; volume encrypted; boot manager updated; notification displayed | Favorable |
| O6.3 | Change system time | 1. Open Date/Time settings 2. Modify time 3. Update RTC 4. Adjust file timestamps 5. Notify time-dependent services | RTC updated; file times adjusted; Kerberos service notified (potential token invalidation) | Favorable |
| O6.4 | Plug in USB device | 1. Detect device 2. Search for drivers 3. Install/load driver 4. Mount volume 5. Notify Safely Remove | Device detected; driver loaded; volume mounted; notification shown | Favorable |
| O6.5 | User revokes app permissions (microphone) | 1. Open Privacy settings 2. Disable microphone for app 3. Update registry 4. Notify running app 5. Block microphone access on next attempt | Setting stored in registry; app receives access denied on next attempt | Favorable |
| O6.6 | Join domain | 1. Open System properties 2. Enter domain credentials 3. Contact DC 4. Create computer account 5. Store credentials 6. Configure Group Policy 7. Restart | Credentials stored in LSA; Group Policy fetched; restart required | Favorable |
| O6.7 | Restart in Safe Mode | 1. Set boot option to Safe Mode 2. Restart 3. Load minimal drivers 4. Disable services 5. Boot to safe desktop | Boot option set; minimal drivers loaded; services disabled; safe desktop displays | Favorable |
| O6.8 | Enable Windows Defender | 1. Open Defender settings 2. Enable real-time protection 3. Start scanning service 4. Schedule periodic scan 5. Register event log | Service starts; periodic scan scheduled; Event Log updated; malware protection active | Favorable |
| ... (10 more) | ... | ... | ... | ... |

**Coder Instructions for O6:**
1. Execute multi-step task on test system
2. Observe all side effects (registry changes, service state, event logs, notifications)
3. Document complete lifecycle (start → end → side effects)
4. Code element per 12 dimensions
5. Assess: Does task execute reliably? Are side effects expected? Are there cascading effects?

---

#### **O7: Limitation Acknowledgment (12 elements)**

**Sources:** Microsoft knowledge base (KB articles), release notes, security advisories, known-issues lists

**Examples to Source:**

| # | Limitation | Source | Documented? | Workaround | Valence |
|---|---|---|---|---|
| O7.1 | Maximum path length: 260 characters (extendable to 32K with special prefix; not all APIs support) | Microsoft Docs: Path length limitation | Yes | Use special prefix or split paths | Neutral |
| O7.2 | NTFS is case-insensitive for display but case-preserving internally; can cause issues with Unix software | Microsoft Docs: File naming | Yes | Use consistent casing; be aware of Unix compatibility | Neutral |
| O7.3 | Known issue: Windows Update can hang if disk space < 5 GB | KB Article (specific KB#) | Yes | Free disk space before updating | Unflattering |
| O7.4 | Kerberos doesn't support pre-authentication across forest trusts; requires KDC forwarding | Microsoft Docs: Kerberos architecture | Yes | Configure trust forwarding; document limitation | Neutral |
| O7.5 | IPv6 routing table size limited to ~2 million routes (can change via registry; undocumented) | Microsoft Docs: IPv6 limitations | Partially | Modify registry setting HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters | Neutral |
| O7.6 | SMB v1 disabled by default in Server 2019+ for security reasons; legacy clients must enable | Microsoft Security Baseline release notes | Yes | Enable SMB v1 if legacy clients needed; accept security risk | Neutral |
| O7.7 | Group Policy update can take 90 seconds on slow networks; immediate update via gpupdate not guaranteed | Microsoft Docs: Group Policy processing | Yes | Run gpupdate; accept replication delays | Neutral |
| O7.8 | Windows Sandbox can't access GPU; only supports CPU rendering | Microsoft Docs: Sandbox limitations | Yes | Use standard VM if GPU needed | Neutral |
| ... (4 more) | ... | ... | ... | ... |

**Coder Instructions for O7:**
1. Locate limitation in Microsoft knowledge base or official release notes
2. Verify it's acknowledged by Microsoft (not undisclosed)
3. Check if workaround exists
4. Code element per 12 dimensions
5. Assess: Is limitation reasonable? Is it properly disclosed? Is there a workaround?

---

## PART III: CODING WORKFLOW

### **Phase 1: Coder Training (Week 3, 2026-09-14 to 2026-09-20)**

**Deliverable:** κ ≥ 0.80 inter-rater agreement on 21 practice elements (3 per O-type)

**Schedule:**
- **Day 1 (2026-09-14):** Codebook review + dimension scoring training
- **Day 2 (2026-09-15):** Practice coding on 3 O1 elements; discuss discrepancies
- **Day 3 (2026-09-16):** Practice coding on 3 O2 elements; achieve κ ≥ 0.80
- **Day 4 (2026-09-17):** Practice coding on 3 O3 + 3 O4 elements; verify agreement
- **Day 5 (2026-09-18):** Practice coding on 3 O5 + 3 O6 elements; maintain κ ≥ 0.80
- **Day 6 (2026-09-19):** Practice coding on 3 O7 elements; final agreement check
- **Day 7 (2026-09-20):** κ ≥ 0.80 gate verification; approved to proceed or re-train

**Acceptance Criteria:**
- [ ] All 21 practice elements coded by both primary + secondary coder
- [ ] Cohen's κ ≥ 0.80 for each O-type (minimum 0.80, no type below threshold)
- [ ] Dimension agreement per rationale (both coders agree on top 3 dimensions; some disagreement on lower-weight dims acceptable if κ ≥ 0.80 overall)
- [ ] Coder team confident in operationalization
- [ ] Ready to proceed to Phase 2

**If κ < 0.80:**
- Identify low-agreement dimensions (O-types)
- Re-train on those dimensions using worked examples
- Retry with new 21-element practice set
- Continue until κ ≥ 0.80 achieved

---

### **Phase 2: Main Assessment (Weeks 4–5, 2026-09-21 to 2026-10-04)**

**Deliverable:** 120 elements fully coded; coherence ≥ 0.85; κ ≥ 0.60; no unresolved breaches

**Schedule:**

| Week | Dates | Elements | Tasks |
|---|---|---|---|
| **Week 4** | 2026-09-21 to 2026-09-27 | 0–60 (half) | Code O1–O4 elements (primary + ~20% double-coding). Daily: ρ divergence monitor (target ≥ 0.50); CI-width monitor (all dimensions CI < 0.30) |
| **Week 5** | 2026-09-28 to 2026-10-04 | 60–120 (second half) | Code O5–O7 elements (primary + ~20% double-coding). Reconcile Week 4 low-agreement cells. Final: coherence check (target ≥ 0.85) |

**Daily Workflow (per coder):**
1. **Morning (30 min):** Codebook review; select 3–4 elements for the day
2. **Coding (4–5 hours):** Source element, verify evidence, code 12 dimensions, document rationale
3. **Evening (30 min):** Upload coded element; sync with team; note any issues
4. **Daily Check (lead auditor, 30 min):** Review codes; spot-check agreement; monitor ρ/CI-width; escalate breaches

**Team Coordination:**
- Primary coder: Individual coding (99 elements, ~70% of total)
- Secondary coder: Double-code ~20% of elements (24 elements)
- Lead auditor: Review all codes; reconcile discrepancies; monitor stopping rules
- Data manager: Track progress; calculate κ/ρ daily; alert on threshold breaches

---

### **Phase 3: Reconciliation & Finalization (2026-10-05)**

**Activities:**
1. Reconcile all low-agreement elements (κ < 0.60 per cell)
2. Verify no Class A/B/C breaches left outstanding
3. Calculate final coherence score (target ≥ 0.85)
4. Prepare Layer 1 results report

**Output:**
- `WINDOWS_LAYER_1_SELF_ASSESSMENT_RESULTS.md` (400+ lines)
  - Coherence score + per-dimension scores
  - Stratification analysis (O-type, valence, availability)
  - Sample element codings (8–10 with full rationale)
  - Agreement statistics (κ per dimension/O-type/valence)
  - Any resolved breaches with Z2 sign-off

---

## PART IV: STOPPING RULES (Armed at Start of Week 4)

### **Rule 1: Divergence Monitor (ρ < 0.50)**
- **Measure:** Spearman ρ between all coder scores across all elements coded so far
- **Check:** Every 10 elements (at 10, 20, 30, ... 120)
- **Trigger:** ρ drops below 0.50
- **Action:** Pause new coding; re-train coders; recalculate ρ on retrained cohort; resume if ρ ≥ 0.50

### **Rule 2: CI-Width Monitor (any dimension CI ≥ 0.30)**
- **Measure:** 95% confidence interval for each dimension score
- **Check:** Every 30 elements (at 30, 60, 90, 120)
- **Trigger:** Any dimension CI-width ≥ 0.30
- **Action:** Pause new coding; identify dimension with widest CI; re-train; recalculate CI; resume if all CIs < 0.30

### **Rule 3: Breach Trigger (Class A/B/C)**
- **Measure:** Breaches detected during coding
- **Trigger:** Any breach found
- **Action:** Stop immediately; escalate per §5 (breach escalation protocol); await Z2 guidance

---

## PART V: SUCCESS METRICS

### **Primary Gate: Coherence ≥ 0.85**
**Definition:** Average of 12 dimension scores across all 120 elements

**Interpretation:**
- **≥ 0.85:** Windows exhibits consistent, high trustworthiness across all dimensions
- **0.70–0.84:** Windows is generally trustworthy but has one or more weak dimensions (flag for Phase 2.4 external validation)
- **< 0.70:** Trustworthiness is questionable; may indicate operationalization issues or genuine Windows weaknesses

**Expected Result (based on OS pilot):** Coherence ≈ 0.88–0.91

### **Secondary Gates:**
- **κ ≥ 0.60 (overall):** Inter-rater reliability acceptable
- **κ ≥ 0.60 per O-type:** No operation type shows systematic disagreement
- **κ ≥ 0.60 per dimension:** No dimension shows systematic disagreement
- **κ ≥ 0.60 per valence:** Coders don't systematically under/over-score unflattering elements

### **Tertiary Metrics:**
- **Per-dimension scores:** Truth, Service, Harm, Autonomy, Value, Humility, Scheme, Power, Syc, Consist, Fair, Handoff (each 0–1.0)
- **Stratification analysis:** No severe imbalance by O-type, valence, or availability
- **Breach resolution:** All Class A/B/C breaches identified and resolved with Z2 sign-off

---

## PART VI: SAMPLE ELEMENTS (Pre-Sourced)

### **Sample O1 Element (User-Facing, Favorable, Direct)**

**Element ID:** O1-FAV-001  
**Title:** Windows Update downloads and installs patches automatically

**Evidence Sources:**
1. Microsoft Docs: "Windows Update is configured to automatically download and install updates"
2. Test Environment: Settings → Update & Security → View Update History
3. Event Viewer: Application and Services Logs → Windows Update

**Sourcing Instructions:**
1. Open Windows Settings
2. Navigate to Update & Security
3. Confirm "Automatically download and install" is selected
4. Check Update History for recent installations
5. Inspect Event Viewer for Windows Update events

**Preliminary Coding (Primary Coder A):**
| Dimension | Score | Rationale |
|---|---|---|
| Truth | 0.92 | Claim accurate; auto-download/install confirmed; timing sometimes unexpected |
| Service | 0.88 | Updates ensure security; automatic delivery is reliable; restart timing can interrupt |
| Harm | 0.87 | Patches reduce harm; automatic update beneficial; restart can cause loss if unsaved |
| Autonomy | 0.78 | Users can defer up to 35 days; restart is ultimately forced; limited real control |
| Value | 0.85 | Patches serve security goal; timing sometimes conflicts with user workflow |
| Humility | 0.82 | Documentation is clear about deferral; limitations documented |
| Scheme | 0.84 | Update process logged; Event Viewer shows status; decisions are traceable |
| Power | 0.81 | Admins can configure Group Policy; users have limited override |
| Syc | 0.87 | Update sequence coordinated; dependencies managed; restart ordered |
| Consist | 0.85 | OS state preserved; applications can save state; recovery after restart reliable |
| Fair | 0.86 | All users face same update timing; deferral available to all |
| Handoff | 0.84 | Restart reason logged; update completion recorded; admin can trace when it occurred |
| **Coherence** | **0.84** | Overall trustworthiness slightly below ideal; update timing is primary concern |

**Secondary Coder B Preliminary Coding (for comparison):**
| Dimension | Score | Difference | Notes |
|---|---|---|---|
| Truth | 0.91 | -0.01 | Agree; well-documented claim |
| Service | 0.86 | -0.02 | Slight disagreement on restart impact; coder B weights more heavily |
| Harm | 0.88 | +0.01 | Agree; patch benefits outweigh risks |
| Autonomy | 0.80 | +0.02 | Coder B slightly more generous on deferral window |
| Value | 0.84 | -0.01 | Agree; security value clear |
| Humility | 0.81 | -0.01 | Agree; limitations clear |
| Scheme | 0.83 | -0.01 | Agree; logging is good |
| Power | 0.80 | -0.01 | Agree; admin control is moderate |
| Syc | 0.86 | -0.01 | Agree; coordination is good |
| Consist | 0.86 | +0.01 | Coder B slightly more confident in recovery |
| Fair | 0.85 | -0.01 | Agree; fairness is good |
| Handoff | 0.83 | -0.01 | Agree; responsibility clear |
| **Coherence** | **0.84** | **0.00** | Both coders arrive at identical coherence; high agreement |

**Reconciliation:**
- κ for this element: 0.96 (near-perfect agreement)
- Dimension spread: min 0.78 (Autonomy), max 0.92 (Truth); range 0.14 (acceptable)
- Final score (average): O1-FAV-001 Coherence = 0.84

**Coder Notes:**
"Update timing is the key trustworthiness challenge. Patches are necessary and beneficial; the forced restart is the trade-off. Users can defer but cannot fully avoid. Overall assessment: system works as documented, but user autonomy is limited."

---

### **Sample O3 Element (Claim-Evidence, Unflattering, Inference)**

**Element ID:** O3-UNFLAT-008  
**Title:** UAC prevents privilege escalation

**Official Claim:**
Source: Microsoft Docs: "User Account Control (UAC) helps prevent unauthorized changes to your computer"

**Evidence Research:**

1. **Documentation:** Microsoft Docs explains UAC prompts when admin action is attempted
2. **Security Research:** Multiple UAC bypass vulnerabilities documented in security literature
3. **Known Vulnerabilities:**
   - CVE-2021-1732 (UAC bypass via Windows COM objects)
   - Various kernel exploits that bypass UAC entirely
4. **Functional Behavior:** UAC prompts for elevated operations; prompts can be brute-forced or social engineered

**Sourcing Instructions:**
1. Review Microsoft's UAC documentation and design intent
2. Search security advisories (CVE, NVD) for "UAC bypass"
3. Research whether UAC is truly effective as a privilege escalation barrier
4. Distinguish: UAC as a "soft" barrier (prompts users) vs. "hard" barrier (prevents escalation technically)

**Preliminary Coding (Primary Coder A):**
| Dimension | Score | Rationale |
|---|---|---|
| Truth | 0.68 | Claim says "prevents"; research shows bypasses exist; claim overstated |
| Service | 0.75 | UAC is functional most of the time; known exploits are edge cases |
| Harm | 0.72 | UAC prevents casual escalation; determined attackers can bypass |
| Autonomy | 0.85 | UAC respects user choice (user can click "Yes" or "No"); good autonomy |
| Value | 0.74 | UAC prompts users; some value in awareness; doesn't prevent determined escalation |
| Humility | 0.64 | Microsoft doesn't widely disclose UAC bypass vulnerabilities in marketing |
| Scheme | 0.76 | Prompt decisions are visible; audit trail exists |
| Power | 0.80 | Escalation requires consent (prompt); doesn't fully prevent abuse |
| Syc | 0.81 | UAC integrates with service startup; dependencies work |
| Consist | 0.79 | UAC decision is logged; state is consistent |
| Fair | 0.82 | All users prompted equally; no hidden escalation |
| Handoff | 0.75 | Prompt shows who requested escalation; limited attribution |
| **Coherence** | **0.75** | UAC is effective deterrent but not absolute barrier; claim somewhat overstated |

**Secondary Coder B Preliminary Coding:**
| Dimension | Score | Difference | Notes |
|---|---|---|---|
| Truth | 0.70 | +0.02 | Agree; claim is overstated |
| Service | 0.73 | -0.02 | Coder B weights bypass vulnerabilities more heavily |
| Harm | 0.74 | +0.02 | Coder B slightly more generous |
| Autonomy | 0.84 | -0.01 | Agree; user choice is clear |
| Value | 0.75 | +0.01 | Agree; awareness value moderate |
| Humility | 0.62 | -0.02 | Coder B feels Microsoft downplays limitations |
| Scheme | 0.77 | +0.01 | Agree; transparency is good |
| Power | 0.79 | -0.01 | Agree; escalation requires action |
| Syc | 0.80 | -0.01 | Agree; coordination is good |
| Consist | 0.80 | +0.01 | Agree; consistency is good |
| Fair | 0.81 | -0.01 | Agree; fairness is good |
| Handoff | 0.76 | +0.01 | Agree; responsibility is moderate |
| **Coherence** | **0.75** | **0.00** | Identical coherence; minor dimension disagreements |

**Reconciliation:**
- κ for this element: 0.90 (high agreement; minor dimension disagreements)
- Dimension spread: min 0.62 (Humility), max 0.85 (Autonomy); range 0.23 (higher variance due to unflattering nature)
- Final score (average): O3-UNFLAT-008 Coherence = 0.75

**Coder Notes:**
"UAC is a user-awareness mechanism, not a technical barrier. The claim that UAC 'prevents' escalation is misleading. Kernel-level exploits, social engineering, and documented CVEs show that UAC is 'soft' security. Score reflects this gap between claim and reality."

**Potential Breach Consideration:**
This element borders on Class B (Specification-Implementation Divergence). Claim says "prevents privilege escalation"; implementation shows it prompts but doesn't prevent. However, Microsoft's documentation does clarify UAC is a "protection" (not absolute prevention), so it's scored as unflattering claim-evidence pair rather than escalated as breach.

---

### **Sample O5 Element (Error Handling, Favorable, Direct)**

**Element ID:** O5-FAV-001  
**Title:** WriteFile returns error and sets ERROR_DISK_FULL when disk is full

**Error Generation Protocol:**
1. Create test file on small partition
2. Fill partition to 100% capacity
3. Attempt WriteFile operation
4. Observe return value and GetLastError

**Test Results:**
- **Condition:** Disk full (0 KB free)
- **Operation:** WriteFile to fill partition
- **Expected Response:** FALSE returned; ERROR_DISK_FULL (0x70 = 112)
- **Actual Response:** FALSE returned; GetLastError = 112 (ERROR_DISK_FULL)
- **Result:** ✓ MATCH

**Preliminary Coding (Primary Coder A):**
| Dimension | Score | Rationale |
|---|---|---|
| Truth | 0.95 | Behavior perfectly matches documentation |
| Service | 0.88 | Error prevents data corruption; service continues |
| Harm | 0.90 | Error prevents silent write failure; data integrity protected |
| Autonomy | 0.82 | User/app can decide how to handle error; good control |
| Value | 0.87 | Error allows graceful handling; application can notify user |
| Humility | 0.88 | Error documented; no hidden failures |
| Scheme | 0.91 | Error code is clear; enables debugging |
| Power | 0.85 | No privilege issues; consistent handling |
| Syc | 0.89 | No cascading failures; error is isolated |
| Consist | 0.90 | Disk state consistent; no corruption |
| Fair | 0.89 | Same error for all users/apps |
| Handoff | 0.88 | Error code identifies problem clearly |
| **Coherence** | **0.88** | Error handling is exemplary; information is rich |

**Secondary Coder B:** (likely 0.95+ κ agreement; error handling is objective/testable)

---

## PART VII: PRE-ASSESSMENT READINESS CHECKLIST

Before Layer 1 begins (2026-09-21), verify:

### **Coder Team**
- [ ] 3–5 Windows security professionals assigned (WIN-CODER-001)
- [ ] Coder training completed; κ ≥ 0.80 on 21 practice elements (WIN-CODER-TRAIN)
- [ ] All coders have access to test environment (Windows 11 + Server 2022)
- [ ] Codebook (§1–§7) distributed to all coders

### **Test Infrastructure**
- [ ] Windows 11 test system provisioned (latest patches)
- [ ] Windows Server 2022 test system provisioned (latest patches)
- [ ] Internet access (for Microsoft Docs, knowledge base lookups)
- [ ] Event Viewer, PowerShell, Registry Editor accessible
- [ ] Tools available: Notepad/Word (for documentation), screenshot tool, file manager

### **Codebook & Protocols**
- [ ] ACAT_CAL_P_WINDOWS_v1_0_DRAFT_CODEBOOK.md distributed (all coders have copy)
- [ ] §4 dimension scoring examples reviewed by all coders
- [ ] Stopping rules understood (ρ monitor, CI-width monitor, breach trigger)
- [ ] Breach escalation protocol confirmed with Z2 (Class A/B/C)
- [ ] Frame selection finalized (NIST/CIS/Microsoft/Administrator chosen for all coders)

### **Data Tracking**
- [ ] Spreadsheet prepared to track coding progress (120 elements, primary/double-coded, κ per cell)
- [ ] Daily ρ divergence and CI-width calculation prepared
- [ ] Breach log prepared (for any Class A/B/C detection)
- [ ] Reconciliation protocol documented

### **Leadership**
- [ ] Lead auditor assigned (Windows security specialist)
- [ ] Z2 governance authority briefed on stopping rules + escalation
- [ ] Backup auditor assigned (if primary auditor unavailable)

### **Go/No-Go Decision**
- [ ] All items above checked
- [ ] Lead auditor confirms readiness
- [ ] Z2 confirms breach escalation authority ready
- [ ] **PROCEED to Week 4 Layer 1 coding**

---

## PART VIII: TIMELINE TO COMPLETION

| Date | Milestone | Owner | Success Criteria |
|---|---|---|---|
| 2026-09-20 | Coder training complete | Lead auditor + coders | κ ≥ 0.80 on 21 elements |
| 2026-09-21 | Layer 1 begins (Week 4) | Coders | Start coding O1–O4 elements |
| 2026-09-27 | Mid-assessment ρ check | Lead auditor | ρ ≥ 0.50; CI-width all < 0.30 |
| 2026-10-04 | Layer 1 complete (Week 5) | Coders | All 120 elements coded |
| 2026-10-05 | Reconciliation + finalization | Lead auditor | Coherence ≥ 0.85; κ ≥ 0.60 |
| 2026-10-06 | Results report ready | Lead auditor | WINDOWS_LAYER_1_RESULTS.md delivered |

---

## SUMMARY

**Layer 1 Self-Assessment is a 2-week intensive coding effort** (after 1-week training) that produces:
1. **120 coded elements** with full stratification analysis
2. **Coherence score ≥ 0.85** (trustworthiness baseline)
3. **Per-dimension scores** for all 12 dimensions
4. **Inter-rater reliability κ ≥ 0.60** across all coders
5. **Breach resolution log** with Z2 sign-off

**Output feeds directly into Layer 2 external validation** (NIST/CIS alignment, ρ correlation check).

---

**WINDOWS LAYER 1 EXECUTION PLAN: READY FOR DEPLOYMENT**  
**Awaiting:** Coder team assignment (WIN-CODER-001) by 2026-09-20  
**Coder training:** Week 3 (2026-09-14 to 2026-09-20)  
**Main assessment:** Weeks 4–5 (2026-09-21 to 2026-10-04)

Wado. 🦅
