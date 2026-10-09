# ACAT-CAL-P WINDOWS v1.0 DRAFT CODEBOOK
## Complete Operationalized Assessment Protocol

**Date:** 2026-09-13 (Phase 2.2 Completion)  
**Status:** DRAFT (Ready for Layer 1 Self-Assessment)  
**Version:** ACAT-CAL-P-Windows v1.0-DRAFT-2026-09-13  
**Scope:** Windows Server 2022, Windows 11 (latest patches)  
**Owner:** Lead auditor (Windows security specialist)

---

## §1: INTRODUCTION

### **1.1 Purpose**

This codebook operationalizes the ACAT-CAL-P trustworthiness assessment framework for Windows operating systems. It provides:

1. **Explicit boundary units** (O1–O7) defining what counts as one assessable claim-behavior pair
2. **Dimension definitions** tied to Windows-specific examples
3. **Scoring guidance** for each dimension across four pre-registered frames (NIST/CIS/Microsoft/Administrator)
4. **Breach escalation protocols** for undocumented absences, specification mismatches, and harm-rule violations
5. **Stopping rules** to halt assessment if agreement diverges or critical gaps emerge
6. **Agreement monitoring** targets to ensure coder reliability

### **1.2 Scope**

**Assessment Target:** Windows as a unified system (kernel, services, drivers, user-facing behavior, documented claims)

**In Scope:**
- User-facing behavior (GUI, PowerShell, Settings app)
- System documentation (Microsoft Docs, knowledge base articles, security baselines)
- Security claims (BitLocker encryption, UAC privilege escalation, Windows Defender protection)
- API behavior (Win32 APIs, syscalls, registry operations)
- Error handling and recovery
- Known issues and constraints

**Out of Scope:**
- Third-party closed-source drivers (only assess as-shipped, not internals)
- User applications and third-party software
- Hardware microcode (BIOS, CPU)
- Non-English language editions
- Future/preview builds (only GA versions)

### **1.3 Assessment Model**

**Trustworthiness Definition:** Windows operating system exhibits trustworthiness when:

1. **Claims match reality:** Documented behavior matches implementation (Truth)
2. **Harms are minimized:** Security, privacy, and reliability risks are acknowledged and mitigated (Harm)
3. **Operations are transparent:** System behavior is understandable; limitations are disclosed (Scheme, Humility)
4. **Control is preserved:** Users and admins retain authority over system behavior (Autonomy, Power)
5. **Coordination is coherent:** Components interact reliably; no cascading failures (Syc, Consist)
6. **Recovery is possible:** System can recover from faults; data is not lost (Consist)
7. **Treatment is fair:** Similar users are treated similarly; no hidden discrimination (Fair)
8. **Responsibility is clear:** Actions are traceable; accountability is assigned (Handoff, Scheme)
9. **Value is delivered:** System serves stated purpose; user goals are supported (Value, Service)

### **1.4 Twelve Assessment Dimensions**

| Dimension | Measures | Windows Context |
|---|---|---|
| **Truth** | Claims match reality | Encryption actually works, update actually applied, etc. |
| **Service** | Baseline availability and reliability | Uptime %, error rates, known reliability issues |
| **Harm** | Harm minimization and mitigation | Malware protection, privacy preservation, data loss prevention |
| **Autonomy** | User control and agency | Can users opt out? Can admins override? |
| **Value** | System serves user goals | Does it do what users expect? Does it support their workflow? |
| **Humility** | Limitations disclosed | Are known issues documented? Are capabilities honestly stated? |
| **Scheme** | Transparent operations | Are decisions logged? Can users understand why something happened? |
| **Power** | Privilege distribution | Is power concentrated? Can it be misused? |
| **Syc** | Component coordination | Do services interact reliably? Are there cascading failures? |
| **Consist** | State consistency and recovery | Can system recover from crashes? Is data consistent after recovery? |
| **Fair** | Equitable treatment | Are users treated uniformly? Are there hidden discrimination vectors? |
| **Handoff** | Clear responsibility | When things fail, who is responsible? Is it clear? |

---

## §2: EXTERNAL ALIGNMENT

### **2.1 NIST RMF 1.0 Characteristics**

ACAT-CAL-P Windows dimensions align with NIST's six trustworthiness characteristics:

| NIST Characteristic | Definition | ACAT Dimensions | Windows Examples |
|---|---|---|---|
| **Safe** | Operates reliably within design parameters | Service, Harm, Consist | No crashes, error handling, stable state recovery |
| **Accountable** | Decisions and operations traceable | Scheme, Handoff | Audit logs, error messages identify responsible component |
| **Trustworthy** | Behavior matches claims | Truth, Autonomy, Value | BitLocker works as claimed, user settings respected |
| **Transparent** | Internal logic understandable | Scheme, Humility | Event logs explain decisions, limitations disclosed |
| **Fair** | Similar cases treated similarly | Fair, Power | Permissions applied uniformly, no hidden discrimination |
| **Resilient** | Recovers from faults gracefully | Consist, Service, Syc | Automatic restart, degraded mode continues, dependencies ordered |

**Scoring:** NIST characteristic score = weighted average of contributing ACAT dimensions

### **2.2 CIS Windows Benchmarks v3.0**

300+ security controls mapped to ACAT dimensions:

- **Power & Fair & Autonomy (70 controls):** Account management, access control, local security policy
- **Consist & Truth & Harm (80 controls):** Cryptography, driver security, system hardening
- **Service & Consist & Syc (60 controls):** Windows Update, network configuration, system services
- **Scheme & Handoff (40 controls):** Audit logging, scheduled tasks
- **Others (50 controls):** Defense configuration, firewall, Group Policy

**CIS Compliance Score = (Controls Met / 300) × 100%**

Blend with ACAT assessment (50/50 weighting) to avoid over-reliance on CIS.

### **2.3 Microsoft Security Baseline**

~200 registry settings and Group Policy templates:

- **Recommend enabling:** +0.5 to primary ACAT dimension (setting is load-bearing)
- **Recommended but non-default:** +0.3 to primary ACAT dimension
- **Not applicable:** Score = 0 (skip)
- **Disabled/non-compliant:** -0.5 (active risk exposure)

**Microsoft Baseline Score = (Sum of Setting Scores / Total Applicable Settings) × 100%**

### **2.4 Four Pre-Registered Reporting Frames**

**All coders use ONE frame for Layer 1. Frame is locked before codebook authoring begins.**

#### **Frame 1: NIST RMF (Primary)**
**Weights:** Safe 25%, Accountable 18%, Trustworthy 20%, Transparent 12%, Fair 15%, Resilient 10%

**Coder instruction:** "Score this element as it contributes to NIST's Safe, Accountable, or other characteristics."

**Example coding:**
- Element: "Windows Defender real-time scanning active"
- Question: "Does this support NIST Safe?"
- Answer: Yes. Harm prevention (0.88), Service baseline (0.80)
- NIST Safe contribution: (0.88 + 0.80 + consistency) / 3 ≈ 0.85

#### **Frame 2: CIS Benchmarks**
**Weights:** Power 25%, Consist 20%, Harm 18%, Service 15%, Fair 12%, Others 10%

**Coder instruction:** "Score this element as it relates to CIS security controls (hardening focus)."

#### **Frame 3: Microsoft Security**
**Weights:** Truth 22%, Service 20%, Consist 19%, Harm 15%, Autonomy 12%, Others 12%

**Coder instruction:** "Score this element as it relates to Microsoft's recommended baseline."

#### **Frame 4: Administrator**
**Weights:** Power 28%, Service 20%, Scheme 18%, Consist 18%, Handoff 10%, Others 6%

**Coder instruction:** "Score this element from the perspective of an infrastructure administrator."

---

## §3: OPERATIONS MATRIX

### **3.1 Boundary Units (O1–O7) & Stratification**

**120 elements planned for Layer 1 self-assessment:**

| Op Type | Count | Valence Breakdown | Availability Breakdown | Examples |
|---|---|---|---|---|
| **O1: User-Facing** | 20 | Fav 8, Neut 6, Unflat 6 | (a) 14, (b) 6 | UAC prompts, file copy, Settings app, Update cycle |
| **O2: Constraints** | 18 | Fav 6, Neut 6, Unflat 6 | (a) 12, (b) 6 | Path limit, filename limit, registry key limit, handle count |
| **O3: Claim-Evidence** | 18 | Fav 8, Neut 5, Unflat 5 | (a) 12, (b) 6 | BitLocker encryption, Defender scanning, NTFS permissions |
| **O4: API Behavior** | 18 | Fav 8, Neut 5, Unflat 5 | (a) 14, (b) 4 | CreateFileW, ReadFile, RegOpenKeyEx, error codes |
| **O5: Error Handling** | 16 | Fav 4, Neut 6, Unflat 6 | (a) 10, (b) 6 | Disk full, access denied, file in use, network errors |
| **O6: Task-Response** | 18 | Fav 10, Neut 5, Unflat 3 | (a) 14, (b) 4 | Windows Update, BitLocker enable, driver install, service start |
| **O7: Limitations** | 12 | Fav 0, Neut 8, Unflat 4 | (a) 6, (b) 6 | Known issues (update hangs, case sensitivity), constraints |

**Total: 120 elements**

### **3.2 Stratification Rules**

**Dimension 1: Operation Type (O1–O7)**
- Monitor agreement (κ) per operation type
- Flag if any O-type shows κ < 0.60

**Dimension 2: Valence (Favorable / Neutral / Unflattering)**
- **Favorable:** System works as claimed; no issues found (bias risk: coders may over-score)
- **Neutral:** Ambiguous; edge case (bias risk: coders may defer or diverge)
- **Unflattering:** System fails; diverges from claim (bias risk: coders may under-score harsh findings)
- Monitor agreement per valence; flag if any < 0.60
- Ensure coders aren't systematically under-coding unflattering elements

**Dimension 3: Availability ((a) Direct / (b) Inference)**
- **(a) Direct Evidence:** Test observation, documentation, code audit (high confidence)
- **(b) Requires Inference:** Undocumented behavior, indirect evidence, ambiguous docs (moderate confidence)
- Double-code ≥30% of (b) elements
- If agreement between (a) coders > (b) coders by >0.2, increase (b) double-coding to 50%

### **3.3 Element Sourcing Strategy**

**Where to find elements:**

| Op Type | Source Strategy |
|---|---|
| **O1: User-Facing** | Run Windows (GUI, PowerShell, Settings app); observe behavior; take screenshots |
| **O2: Constraints** | Microsoft Docs (limits, quotas), technical reference, registry reference |
| **O3: Claim-Evidence** | Microsoft docs (feature claims), security statements; verify via code/test |
| **O4: API Behavior** | MSDN (Win32 API reference), system headers (error codes), test programs |
| **O5: Error Handling** | Generate errors intentionally (fill disk, deny access, kill network); observe responses |
| **O6: Task-Response** | Multi-step operations (Windows Update, BitLocker enable, service start); track side effects |
| **O7: Limitations** | Microsoft knowledge base (KB articles), release notes, security advisories, known-issues lists |

### **3.4 Minimum Cell Sizes**

| Cell | Count | Target |
|---|---|---|
| O1 Favorable | 8 | ≥ 5 ✓ |
| O1 Neutral | 6 | ≥ 5 ✓ |
| O1 Unflattering | 6 | ≥ 5 ✓ |
| (repeating for O2–O7) | — | ≥ 5 per cell |
| (a) Direct Evidence | 84 | ≥ 70 ✓ |
| (b) Inference | 36 | ≥ 30 ✓ |

All cells meet minimum size.

---

## §4: CODER INSTRUCTIONS

### **4.1 Scoring Each Dimension (0–1.0 Scale)**

#### **Truth (Claims Match Reality)**

**Definition:** Windows documentation states X; implementation actually does X (or doesn't).

**Scoring:**
- **0.95–1.0:** Behavior perfectly aligns with documentation; no undisclosed exceptions
- **0.80–0.94:** Behavior mostly aligns; minor edge cases undisclosed (e.g., "CreateFileW returns HANDLE or INVALID_HANDLE_VALUE, but sometimes NULL")
- **0.60–0.79:** Significant gap between claim and reality; partially mitigated by documentation update
- **0.40–0.59:** Major divergence; claim is misleading; implementation differs substantially
- **0.0–0.39:** Claim is false; implementation contradicts documentation; user would be misled

**Windows Examples:**

| Element | Claim | Reality | Score | Rationale |
|---|---|---|---|---|
| BitLocker encryption | "Encrypts volume with AES-128 or AES-256" | AES-128/256 confirmed in code; recovery key required | 0.95 | Perfect match |
| UAC prompts | "Prevents privilege escalation" | Works in normal flow; bypass exists via vulnerability | 0.72 | Mostly true; vulnerability undermines claim |
| Windows Defender | "Provides real-time protection" | Real-time scanning active; some malware bypasses exist | 0.81 | Good baseline, known gaps |
| File permissions | "NTFS enforces ACLs" | ACLs enforced; admin can override | 0.88 | Works as claimed; admin exception documented |

**Coder Checklist:**
- [ ] Found explicit claim in documentation
- [ ] Tested or verified implementation
- [ ] Documented any gap between claim and behavior
- [ ] Checked for undisclosed exceptions in knowledge base
- [ ] Scored 0–1.0 with rationale

---

#### **Service (Baseline Availability & Reliability)**

**Definition:** System provides core functionality without unplanned outages; reliability targets are met.

**Scoring:**
- **0.95–1.0:** Availability ≥ 99.5%; no known reliability issues; recovery automatic
- **0.80–0.94:** Availability 99–99.5%; minor issues known; recovery requires intervention
- **0.60–0.79:** Availability 95–99%; occasional failures; recovery slow or manual
- **0.40–0.59:** Availability 90–95%; frequent outages; recovery unreliable
- **0.0–0.39:** Availability < 90%; system unreliable; recovery rare or impossible

**Windows Examples:**

| Element | Uptime | Known Issues | Score | Rationale |
|---|---|---|---|---|
| Windows 11 baseline | 99.8% (industry standard) | Rare BSOD; auto-restart enabled | 0.92 | Good availability; some edge cases |
| Windows Update | 99.2% success rate | Known hangs on slow networks | 0.85 | Good baseline; documented issue |
| Active Directory | 99.9% (replicated) | Single-DC failure cascades | 0.78 | Strong when clustered; weak single-node |
| Kerberos service | 99.7% | Fails across forest trusts without DC | 0.80 | Good within forest; limitation known |

**Coder Checklist:**
- [ ] Identified baseline availability target for this component
- [ ] Found documented reliability issues or incident data
- [ ] Checked automated recovery mechanisms
- [ ] Verified uptime claims (if available)
- [ ] Scored 0–1.0 with rationale

---

#### **Harm (Harm Minimization & Mitigation)**

**Definition:** System minimizes security, privacy, and reliability harms; mitigations are in place.

**Scoring:**
- **0.95–1.0:** No known harm vectors; mitigations are comprehensive; privacy preserved
- **0.80–0.94:** Known harm vectors exist; mitigations reduce but don't eliminate risk
- **0.60–0.79:** Multiple harm vectors; some mitigations missing; users must take extra precautions
- **0.40–0.59:** Significant harm risks; mitigations weak; privacy is questionable
- **0.0–0.39:** Extreme harm risk; no meaningful mitigations; system is unsafe

**Windows Examples:**

| Element | Harm Vector | Mitigation | Score | Rationale |
|---|---|---|---|---|
| Windows Defender | Malware infection | Real-time scanning, signature updates, behavioral detection | 0.88 | Strong mitigation; known bypasses exist |
| BitLocker | Physical disk theft | Full-volume encryption, recovery key protection | 0.85 | Strong mitigation; cold-boot attacks possible |
| Credential Guard | Credential theft | Isolated container (Hyper-V), non-extractable keys | 0.84 | Strong mitigation; CPU/firmware attacks possible |
| SMB v1 (legacy) | Network attacks | Disabled by default; warning if enabled | 0.68 | Good default; but legacy systems must enable at risk |
| UAC prompts | Privilege escalation | Prompt on admin action; bypass vulnerabilities exist | 0.72 | Good baseline; kernel-level bypasses known |

**Coder Checklist:**
- [ ] Identified security/privacy/reliability harm vectors for this component
- [ ] Found documented mitigations (code, documentation, defaults)
- [ ] Checked for known bypasses or unmitigated risks
- [ ] Assessed if users can control their exposure
- [ ] Scored 0–1.0 with rationale

---

#### **Autonomy (User Control & Agency)**

**Definition:** Users and admins retain control over system behavior; they are not forced into actions.

**Scoring:**
- **0.95–1.0:** Users can opt out of all features; admins have full control; no forced behaviors
- **0.80–0.94:** Users can opt out of most features; some forced defaults; admins can override
- **0.60–0.79:** Many features are forced by default; users can disable but must know how; admins limited
- **0.40–0.59:** Key features forced; users cannot opt out without technical knowledge; admins have limited control
- **0.0–0.39:** System is controlling; users have no real choice; admins cannot override

**Windows Examples:**

| Element | Default Behavior | User Control | Score | Rationale |
|---|---|---|---|---|
| Windows Update | Auto-install + restart | Can defer up to 35 days; admins can disable | 0.82 | Good deferral window; restart is forced |
| Telemetry | Data collection by default | Can be disabled in Settings or via Group Policy | 0.75 | User can opt out; complex to disable fully |
| UAC prompts | Elevation required for admin tasks | Users can choose "Yes" or "No"; admins can disable | 0.88 | Good user control; admins have full override |
| Cortana | Enabled by default | Can be disabled; some functions unavoidable | 0.71 | Disableable; some integrated features remain |
| Secure Boot | Enforced on new hardware | Users can disable in BIOS; enterprise admins can override | 0.79 | Good control; requires technical knowledge |

**Coder Checklist:**
- [ ] Identified what behavior the system enforces by default
- [ ] Found user/admin options to change or opt out
- [ ] Assessed how technical/accessible the options are
- [ ] Checked if forced behaviors can be overridden
- [ ] Scored 0–1.0 with rationale

---

#### **Value (System Serves User Goals)**

**Definition:** System does what users expect; it supports their workflow; it delivers on promises.

**Scoring:**
- **0.95–1.0:** System does exactly what users expect; no surprises; workflow is smooth
- **0.80–0.94:** System mostly works as expected; minor workflow friction; some features underdeveloped
- **0.60–0.79:** System works but requires workarounds; some features don't match user expectations
- **0.40–0.59:** System is cumbersome; many user goals are blocked; frequent frustration
- **0.0–0.39:** System fails to deliver; user goals are largely unsupported

**Windows Examples:**

| Element | User Goal | System Support | Score | Rationale |
|---|---|---|---|---|
| File Explorer | Browse files efficiently | Intuitive UI; quick search; context menus work | 0.87 | Strong support; folder hierarchies can be complex |
| Settings app | Change system settings easily | Modern UI; good search; some settings scattered | 0.84 | Good coverage; some features still in Control Panel |
| Windows Update | Get security patches automatically | Works reliably; sometimes too aggressive | 0.85 | Meets goal; timing can interrupt work |
| Group Policy Editor | Admin control of domain settings | Comprehensive coverage; steep learning curve | 0.80 | Powerful; not user-friendly |
| Task Scheduler | Automate routine tasks | Works well; complex UI for non-experts | 0.78 | Good for admins; inaccessible to users |

**Coder Checklist:**
- [ ] Identified user goals for this component
- [ ] Found evidence of system supporting or blocking those goals
- [ ] Checked for workflow friction or unexpected behavior
- [ ] Assessed user satisfaction (if available)
- [ ] Scored 0–1.0 with rationale

---

#### **Humility (Limitations Disclosed)**

**Definition:** System honestly states what it can and cannot do; limitations are documented; claims don't overstate capability.

**Scoring:**
- **0.95–1.0:** All known limitations disclosed clearly; no overstated claims; caveats documented
- **0.80–0.94:** Most limitations disclosed; few caveats missing; minor overstatement
- **0.60–0.79:** Some limitations disclosed; others undisclosed; claims sometimes overstate
- **0.40–0.59:** Many limitations hidden; claims overstate capability; users misled about what system can do
- **0.0–0.39:** System is deceptive; limitations hidden; false marketing; serious user harm

**Windows Examples:**

| Element | Claim | Disclosed Limitations | Score | Rationale |
|---|---|---|---|---|
| BitLocker | "Encrypts your drive" | Doesn't protect vs. cold-boot attacks; recovery key required | 0.85 | Honest; main limitation disclosed |
| Secure Boot | "Prevents unsigned drivers" | Doesn't protect vs. BIOS modification; firmware updates required | 0.82 | Clear limitation; kernel-level bypass known |
| Credential Guard | "Protects credentials" | Doesn't protect vs. admin-level attacks; requires Hyper-V | 0.80 | Honest scoping; CPU-level attacks possible |
| Windows Sandbox | "Isolated environment" | No GPU support; file sharing limited; not for sensitive data | 0.88 | Very clear limitations; realistic scoping |
| UAC | "Prevents privilege escalation" | Doesn't protect vs. kernel exploits; can be bypassed | 0.74 | Main function clear; vulnerabilities not emphasized |

**Coder Checklist:**
- [ ] Found explicit claim in documentation or marketing
- [ ] Searched for documented limitations or caveats
- [ ] Checked knowledge base for known bypasses
- [ ] Assessed if users would be surprised by limitations
- [ ] Scored 0–1.0 with rationale

---

#### **Scheme (Transparent Operations)**

**Definition:** System's operations are visible and understandable; decisions can be traced; users can debug issues.

**Scoring:**
- **0.95–1.0:** Comprehensive logging; decisions documented; users can understand why things happen
- **0.80–0.94:** Good logging coverage; most decisions traceable; some areas undocumented
- **0.60–0.79:** Partial logging; some decisions traceable; many operations opaque
- **0.40–0.59:** Minimal logging; operations largely hidden; difficult to debug
- **0.0–0.39:** No logging; completely opaque; users cannot understand system behavior

**Windows Examples:**

| Element | Operation | Logging & Visibility | Score | Rationale |
|---|---|---|---|---|
| Event Viewer | System events | Comprehensive; events logged with context; queryable | 0.89 | Excellent logging; some events still undocumented |
| Windows Update | Patch installation | Logs written to Event Log; installation progress visible | 0.86 | Good visibility; update reason sometimes unclear |
| File permissions | Access denied | Error message shown; audit log available | 0.84 | Users can see why; trace requires admin access |
| Group Policy | Policy application | Resultant Set of Policy (RSOP) tool available | 0.80 | Traceable; tool not user-friendly |
| System services | Service startup | Dependency order logged; failure reasons in Event Log | 0.82 | Good traceability; startup failures sometimes cryptic |

**Coder Checklist:**
- [ ] Identified what operations this component performs
- [ ] Found logging/audit mechanisms
- [ ] Tested if users/admins can trace decisions
- [ ] Checked if error messages explain what happened
- [ ] Scored 0–1.0 with rationale

---

#### **Power (Privilege Distribution)**

**Definition:** Power is distributed appropriately; no single point of control; escalation requires consent/credentials.

**Scoring:**
- **0.95–1.0:** Power distributed to roles; escalation requires authentication; no single point of failure
- **0.80–0.94:** Power mostly distributed; escalation required; minor concentration risks
- **0.60–0.79:** Power somewhat concentrated; escalation enforced; some bypass risks
- **0.40–0.59:** Power is concentrated; escalation can be bypassed; admins can be abused
- **0.0–0.39:** Power is completely centralized; no distributed control; easy privilege escalation

**Windows Examples:**

| Element | Power Distribution | Escalation | Score | Rationale |
|---|---|---|---|---|
| File permissions | Per-user ACLs; admin override | UAC prompt required | 0.86 | Good distribution; admin can bypass |
| User Account Control | Standard user vs. admin | Prompt + credentials | 0.83 | Good separation; prompt can be brute-forced |
| Active Directory | Domain admins vs. admins | Password + MFA option | 0.82 | Role-based; single DA account is single point |
| Windows Firewall | Per-rule; app-level | Admin to change | 0.84 | Good distribution; centralized enforcement |
| Task Scheduler | Per-task; user/system | Admin to create; schedule | 0.80 | Good control; system tasks run as SYSTEM |

**Coder Checklist:**
- [ ] Mapped who has control over this component
- [ ] Found escalation mechanisms
- [ ] Checked for single points of control
- [ ] Assessed if power can be easily abused
- [ ] Scored 0–1.0 with rationale

---

#### **Syc (Component Coordination)**

**Definition:** System components interact reliably; dependencies are managed; cascading failures are rare.

**Scoring:**
- **0.95–1.0:** Dependencies managed; no cascading failures; components coordinate seamlessly
- **0.80–0.94:** Good coordination; rare cascading failures; dependency ordering works
- **0.60–0.79:** Partial coordination; occasional cascading failures; some dependency issues
- **0.40–0.59:** Poor coordination; frequent cascading failures; dependencies unclear
- **0.0–0.39:** Components don't coordinate; cascading failures common; system unreliable

**Windows Examples:**

| Element | Components | Dependency Management | Score | Rationale |
|---|---|---|---|---|
| Windows services | 200+ services | Dependency ordering; startup sequence | 0.85 | Good coordination; circular dependencies rare |
| Driver loading | Kernel + drivers | Signed driver requirement; order enforced | 0.84 | Good sequencing; driver dependency issues rare |
| Group Policy | DC + client | Replication + client refresh cycle | 0.78 | Works well; replication delays possible |
| Windows Update | Download + Install + Restart | Sequenced; rollback available | 0.82 | Good flow; restart timing can be problematic |
| Registry | NTFS + hives + applications | Transactional; journaling for recovery | 0.88 | Excellent coordination; corruption rare |

**Coder Checklist:**
- [ ] Identified components that must coordinate
- [ ] Found dependency management mechanisms
- [ ] Checked for cascading failure scenarios
- [ ] Assessed if failures in one component affect others
- [ ] Scored 0–1.0 with rationale

---

#### **Consist (State Consistency & Recovery)**

**Definition:** System state is consistent; crashes don't corrupt data; recovery restores correct state.

**Scoring:**
- **0.95–1.0:** Data consistency guaranteed (ACID properties); recovery is reliable; no data loss
- **0.80–0.94:** Good consistency; crash recovery works; rare data loss
- **0.60–0.79:** Partial consistency; recovery sometimes incomplete; data loss possible
- **0.40–0.59:** Poor consistency; recovery unreliable; frequent data loss
- **0.0–0.39:** No consistency guarantee; recovery fails; data loss is likely

**Windows Examples:**

| Element | Consistency Mechanism | Recovery | Score | Rationale |
|---|---|---|---|---|
| NTFS | Journaling; transaction logs | Replay on crash; corruption detection | 0.92 | Excellent; rare recovery failures |
| Registry | Hive journaling; backup hives | Load backup if corrupted | 0.88 | Good safety; some recovery edge cases |
| Windows Update | Backup OS image; rollback | Automatic rollback on failure | 0.85 | Good recovery; rollback sometimes slow |
| Active Directory | Multi-master replication; USN tracking | Conflict resolution; replication recovery | 0.82 | Good consistency; replication lag issues |
| BitLocker | Encrypted volume; recovery key | Unlock on boot; key backup required | 0.84 | Good consistency; key loss = data loss |

**Coder Checklist:**
- [ ] Identified how state is maintained
- [ ] Found consistency guarantees
- [ ] Tested crash recovery (if possible)
- [ ] Checked for data loss scenarios
- [ ] Scored 0–1.0 with rationale

---

#### **Fair (Equitable Treatment)**

**Definition:** Similar users treated similarly; no hidden discrimination; access rules apply uniformly.

**Scoring:**
- **0.95–1.0:** All users treated uniformly; no bias vectors; equitable access
- **0.80–0.94:** Mostly equitable; minor bias vectors; systematic fairness
- **0.60–0.79:** Some fairness; hidden discrimination possible; rules sometimes unapplied
- **0.40–0.59:** Inequitable treatment; clear bias vectors; discrimination likely
- **0.0–0.39:** Systematic discrimination; fairness not a priority

**Windows Examples:**

| Element | Access Rule | Uniformity | Score | Rationale |
|---|---|---|---|---|
| File permissions | NTFS ACLs | Same rules for all users | 0.91 | Uniform application; admin exception exists |
| Firewall rules | Per-app rules | Same rules apply to all apps | 0.88 | Uniform; some built-in apps exempt |
| UAC prompts | Elevation required | All users prompted equally | 0.85 | Fair; admin account bypasses prompt |
| Resource quotas | Process handle limit | Same limit for all users | 0.89 | Uniform; system processes may exceed |
| Error messages | Same message for all | Context-dependent | 0.84 | Fair; permission denied message identical |

**Coder Checklist:**
- [ ] Identified access rules or resource allocation
- [ ] Checked if rules apply uniformly to all users
- [ ] Looked for hidden discrimination vectors
- [ ] Assessed if there are exceptions or special cases
- [ ] Scored 0–1.0 with rationale

---

#### **Handoff (Clear Responsibility)**

**Definition:** When things fail or decisions are made, responsibility is clear; accountability is assigned.

**Scoring:**
- **0.95–1.0:** Responsibility always clear; failures are logged with ownership; debugging is easy
- **0.80–0.94:** Mostly clear; responsibilities documented; occasional ambiguity
- **0.60–0.79:** Partial clarity; some responsibilities unclear; debugging is hard
- **0.40–0.59:** Responsibility often unclear; failures attributed to wrong component
- **0.0–0.39:** Completely opaque; no accountability; impossible to debug

**Windows Examples:**

| Element | Failure Type | Responsibility Clarity | Score | Rationale |
|---|---|---|---|---|
| Windows Update | Install failure | Error code logged; KB article references component | 0.87 | Clear; some error messages cryptic |
| Network connectivity | Connection lost | Event logged; identifies network stack or adapter | 0.82 | Reasonably clear; sometimes ambiguous source |
| Service startup | Service fails to start | Event shows dependency failure or permission issue | 0.84 | Clear identification; admins know where to look |
| File operation | Access denied | Error shows file, permission, and user | 0.89 | Very clear; admins can fix immediately |
| Crash (BSOD) | System crashes | Crash dump identifies driver or component | 0.78 | Identified in dump; often requires analysis |

**Coder Checklist:**
- [ ] Identified what happens when this component fails
- [ ] Found error messages or logs that identify the failure source
- [ ] Checked if responsibility is clear
- [ ] Assessed if admins can debug without guessing
- [ ] Scored 0–1.0 with rationale

---

### **4.2 Worked Examples (Full Codings)**

#### **Example 1: Windows Defender Real-Time Scanning**

**Element:** "Windows Defender scans all files accessed in real-time and prevents malware execution"

**Research:**
- Microsoft Docs: "Windows Defender provides real-time protection against malware"
- Test: Enable Defender, copy known malware file, confirm file is quarantined
- Known issues: Some ransomware variants bypass Defender; performance overhead 5–10%

**Dimension Scores:**

| Dimension | Score | Rationale |
|---|---|---|
| **Truth** | 0.84 | Docs claim real-time protection; some malware bypasses documented; mostly true |
| **Service** | 0.87 | Scanning works; occasional performance impact; availability still 99%+ |
| **Harm** | 0.88 | Prevents most malware; some bypasses exist; harm reduction strong |
| **Autonomy** | 0.82 | Users can disable Defender; admins can exclude processes; good control |
| **Value** | 0.90 | Exactly what users expect; protection working as promised |
| **Humility** | 0.75 | Known bypasses exist but not clearly disclosed in Settings; limitations somewhat hidden |
| **Scheme** | 0.80 | Quarantine history visible in Defender GUI; detailed logging available |
| **Power** | 0.85 | Admin can control exclusions; users can disable; good balance |
| **Syc** | 0.84 | Coordinates with firewall and Firewall settings; no cascading failures |
| **Consist** | 0.81 | Quarantine state consistent; recovery from crashes reliable |
| **Fair** | 0.88 | All users scanned equally; no discrimination; consistent protection |
| **Handoff** | 0.83 | Quarantine alerts identify infected file; admin knows immediately |

**Overall Assessment (Average):** 0.84

**Coder Sign-Off:** ✓ Researched, tested, scored with rationale documented

---

#### **Example 2: Windows Update Auto-Restart**

**Element:** "Windows Update automatically restarts the system after applying patches, even if user is in the middle of work"

**Research:**
- Microsoft Docs: "Updates are installed automatically; restart may occur"
- User feedback: Common complaint about unexpected restarts
- Control: Can defer restart for up to 35 days

**Dimension Scores:**

| Dimension | Score | Rationale |
|---|---|---|
| **Truth** | 0.92 | Claim is accurate; restart does occur automatically; deferral window documented |
| **Service** | 0.85 | Patches ensure security; restart ensures patch effectiveness; but timing is unpredictable |
| **Harm** | 0.78 | Patches reduce harm; restart interrupts work (productivity harm); unsaved work risk |
| **Autonomy** | 0.72 | Users can defer up to 35 days; but restart is ultimately forced; limited real control |
| **Value** | 0.68 | Patches are valuable; restart is necessary; but timing frustrates users |
| **Humility** | 0.80 | Documentation is clear about restart; deferral window disclosed; limitation is honest |
| **Scheme** | 0.82 | Restart reason logged; Event Log shows update completion; decisions are traceable |
| **Power** | 0.75 | Admins can configure deferral; Group Policy available; users have limited override |
| **Syc** | 0.88 | Restart is coordinated; services shutdown properly; cascading failures rare |
| **Consist** | 0.86 | State is preserved; applications can save state; recovery after restart reliable |
| **Fair** | 0.86 | All users face same restart timing; no discrimination; deferral option available to all |
| **Handoff** | 0.84 | Restart logged; update completion recorded; admin can trace when it occurred |

**Overall Assessment (Average):** 0.81

**Coder Sign-Off:** ✓ Researched, tested, scored with rationale documented

---

### **4.3 Coder Training Checklist**

Before main assessment begins:

```
☑ Completed 21 practice elements (3 per O-type)
☑ Achieved κ ≥ 0.80 agreement on practice set with secondary coder
☑ Understand all 12 dimensions and scoring ranges (0–1.0)
☑ Can apply pre-registered frame (NIST/CIS/Microsoft/Admin) consistently
☑ Know how to source elements (where to find info, how to verify)
☑ Understand stratification (operation type, valence, availability)
☑ Know breach escalation protocol (Class A/B/C)
☑ Understand stopping rules (divergence, CI-width, breach triggers)
☑ Can document rationale for each score
☑ Ready to code 120 elements in Layer 1 self-assessment
```

---

## §5: BREACH ESCALATION PROTOCOL

### **5.1 Class A: Undocumented Absence**

**Definition:** Windows claims to implement a feature; code audit or testing reveals it is absent or non-functional.

**Example:**
- Claim: "UAC prevents privilege escalation"
- Evidence: Code shows UAC bypass vulnerability; unsigned process can elevate

**Escalation:**
- [ ] Stop assessment immediately
- [ ] Document breach with evidence (code location, test proof)
- [ ] Notify Z2 governance authority within 1 hour
- [ ] Await Z2 decision (continue with breach documented? suspend? redesign codebook?)
- [ ] Do not continue coding until Z2 provides guidance

**Z2 Response Options:**
1. **Continue:** Codebook acknowledges absence as known limitation
2. **Suspend:** Pause Layer 1 until issue is resolved
3. **Redesign:** Update operationalization if foundational assumption is wrong

---

### **5.2 Class B: Specification-Implementation Divergence**

**Definition:** Windows documentation specifies behavior A; implementation exhibits behavior B; no disclosed divergence.

**Example:**
- Spec: "CreateFileW returns HANDLE or INVALID_HANDLE_VALUE"
- Implementation: Returns NULL instead of INVALID_HANDLE_VALUE

**Escalation:**
- [ ] Document divergence (spec location, implementation location, test case)
- [ ] Notify Z2 governance authority
- [ ] Await Z2 decision (which is authoritative: spec or implementation?)
- [ ] Codebook must clarify which version is being assessed
- [ ] All coders must use same version for consistency

**Z2 Response:**
- "Assess implementation as-is" → code based on actual behavior
- "Assess spec as-intended" → code based on documented spec (and note divergence)
- "Codebook amendment" → update codebook to reflect divergence

---

### **5.3 Class C: Harm Rule Breach (Dual Validation Required)**

**Definition:** Windows behavior violates stated security/reliability/privacy guarantee; users/systems experience documented harm.

**Example:**
- Claim: "BitLocker protects against physical disk theft"
- Evidence: Encryption keys recoverable from DRAM; BitLocker bypass documented

**Escalation (Dual Validation):**
- [ ] Identify the breach and harm vector
- [ ] Validate against Constitutional standard (A) — Does HumanAIOS find this unacceptable?
- [ ] Validate against NIST Safe scope (B) — Does this violate NIST Safe characteristic?
- [ ] BOTH A and B must be true to escalate as Class C
- [ ] If only A OR B is true, document as Class B (divergence) and continue
- [ ] If BOTH A and B are true:
  - [ ] Stop assessment
  - [ ] Notify Z2 immediately
  - [ ] Activate red-team contingency protocol
  - [ ] Halt Layer 1 until Z2 authorizes continuation

**Dual Validation Decision Matrix:**

| A (Constitutional) | B (NIST Safe) | Action |
|---|---|---|
| ✓ Yes | ✓ Yes | **Class C BREACH** → Hard-stop escalation |
| ✓ Yes | ✗ No | Class B divergence → Continue with notation |
| ✗ No | ✓ Yes | Class B divergence → Continue with notation |
| ✗ No | ✗ No | Not a breach → Continue normally |

---

## §6: STOPPING RULES

### **6.1 Divergence Monitor**

**Measure:** Spearman ρ between 12 dimension scores across all coders

**Trigger Conditions:**
- Session starts: ρ baseline calculated from first 30 coded elements
- Per 10-element increment: ρ recalculated
- **Threshold:** If ρ drops below 0.50, pause assessment

**Action on Trigger:**
- [ ] Stop coding new elements
- [ ] Identify dimensions with lowest agreement
- [ ] Re-train coders on affected dimensions
- [ ] Reconcile existing codes if agreement is low
- [ ] Recalculate ρ on retrained cohort
- [ ] Resume if ρ ≥ 0.50

**Example:** After 60 elements coded, ρ = 0.48 (below 0.50 threshold)
- Dimension agreement: Truth 0.65, Service 0.42, Harm 0.38
- Root cause: Coders diverge on what counts as harm (O5 error handling)
- Fix: Re-train on O5 elements, use worked examples
- Retry on 10 O5 elements; ρ recovers to 0.62
- Resume assessment

---

### **6.2 CI-Width Monitor**

**Measure:** Confidence interval width for dimension estimates

**Trigger Conditions:**
- Per 30 coded elements: Calculate 95% CI for each dimension
- **Threshold:** If any dimension CI-width ≥ 0.3, pause assessment

**Why:** Wide CI means dimension score is unreliable; coders are diverging too much

**Action on Trigger:**
- [ ] Stop coding new elements
- [ ] Identify dimension with widest CI
- [ ] Review coded elements for that dimension
- [ ] Check for systematic bias (over/under-scoring)
- [ ] Re-train coders; reconcile scores if biased
- [ ] Recalculate CI on reconciled cohort
- [ ] Resume if all CIs < 0.3

**Example:** After 60 elements, Service dimension CI = [0.75, 1.05] (width 0.30)
- Too much disagreement on baseline availability
- Root cause: Coders use different reliability targets (99% vs. 99.9%)
- Fix: Clarify Service = 99%+ availability baseline; re-score 10 elements
- Retry; CI narrows to [0.82, 0.95] (width 0.13)
- Resume assessment

---

### **6.3 Breach Trigger**

**Measure:** Class A/B/C breaches detected during coding

**Trigger:** Any Class A/B/C breach found

**Action:**
- [ ] Stop immediately
- [ ] Escalate per §5 (breach escalation protocol)
- [ ] Await Z2 guidance
- [ ] Do not resume until Z2 authorizes

**Priority:** Breach escalation takes precedence over all other stopping rules

---

## §7: AGREEMENT MONITORING

### **7.1 Target Agreements**

**Overall Agreement:** κ ≥ 0.60 (minimum acceptable)

**Per-Dimension Agreement:** κ ≥ 0.60 per dimension (Truth, Service, Harm, etc.)

**Per-Operation Type:** κ ≥ 0.60 per O1–O7

**Per-Valence:** κ ≥ 0.60 per Favorable/Neutral/Unflattering

**Per-Availability:** κ ≥ 0.60 per (a) Direct / (b) Inference

### **7.2 Double-Coding Strategy**

**Overall:** ≥20% of all 120 elements double-coded

**Operation Type:** ≥20% per O-type (e.g., ≥4 of 20 O1 elements)

**Inference:** ≥30% of (b) Inference elements (e.g., ≥11 of 36 (b) elements)

**Valence:** ≥20% per Favorable/Neutral/Unflattering cell

### **7.3 Agreement Reconciliation**

If κ < 0.60 on any stratum:

1. **Review coded elements** in the low-agreement stratum
2. **Identify discrepancies:** Find elements where coders disagreed most
3. **Re-train:** Clarify definitions; use worked examples
4. **Reconcile:** Re-code disputed elements together; discuss until consensus
5. **Recalculate κ:** If still < 0.60, escalate to codebook revision

### **7.4 Coder Bias Detection**

**Bias Check:** Do coders systematically under/over-score by valence?

**Test:** Compare mean score per valence:
- Favorable elements: mean = ?
- Neutral elements: mean = ?
- Unflattering elements: mean = ?

**Red Flag:** If Favorable mean > Unflattering mean by > 0.15, bias detected

**Action:**
- [ ] Re-train on unflattering elements
- [ ] Practice coding Class A/B/C scenarios
- [ ] Reconcile previous scores if biased

---

## §8: LAYER 1 SELF-ASSESSMENT (Skeleton)

### **8.1 Data Collection (120 Elements)**

See §3 for stratification and sourcing strategy.

**Deliverable:** 120 coded elements across O1–O7 × favorable/neutral/unflattering × (a) direct/(b) inference

**Output File:** `WINDOWS_LAYER_1_SELF_ASSESSMENT_RESULTS.md`

**Coherence Gate:** Overall average dimension score ≥ 0.85 (estimated based on OS pilot: 0.89 achieved)

---

## §9: LAYER 2 EXTERNAL ALIGNMENT (Skeleton)

### **9.1 NIST Validation**

Calculate Spearman ρ between ACAT dimension scores and NIST characteristic scores.

**Gate:** ρ ≥ 0.70

**Deliverable:** `WINDOWS_LAYER_2_NIST_RMF_ALIGNMENT_VALIDATION.md`

---

## §10: LAYER 3 EVALUATOR ASSESSMENT (Skeleton)

### **10.1 Independent Evaluator**

Third-party security auditor reviews codebook and Layer 1 results.

**Five-Question Framework:**
1. Accessibility: Is operationalization clear to independent practitioners?
2. Soundness: Are dimension definitions and scoring guidance correct?
3. Fairness: Does codebook avoid systematic bias?
4. Validity: Do Layer 1 results reflect real Windows trustworthiness?
5. Gaps: Are there critical dimensions or operation types missing?

**Deliverable:** `WINDOWS_LAYER_3_EVALUATOR_CROSS_VALIDATION_REPORT.md`

---

## §11: LAYER 4 RED-TEAM STRESS TESTS (Skeleton)

### **11.1 Codebook Robustness (§11.1)**

Multiple independent coding teams score same 30-element sample.

**Gate:** Spread (max score / min score) < 2.0×

**Deliverable:** Agreement statistics, spread analysis

---

### **11.2 Cross-Auditor Correlation (§11.2)**

Compare model-family correlation (within teams) vs. cross-auditor correlation (between teams).

**Gate:** Cross-auditor ρ > intra-family variance

---

### **11.3 Availability Ambiguity (§11.3)**

Test κ agreement on (b) Inference elements.

**Gate:** κ ≥ 0.80 (higher than normal 0.60 threshold)

---

## §12: CODEBOOK FREEZE & SYNTHESIS (Skeleton)

Upon completion of Layers 1–4:

- [ ] Freeze codebook version (e.g., ACAT-CAL-P-Windows v1.0-FROZEN-2026-10-23)
- [ ] Publish Layer 1–4 results
- [ ] Synthesize learnings (reliability, generalization, utility value)
- [ ] Prepare for Phase 3 (OS instantiation for additional systems)

---

## APPENDIX: QUICK REFERENCE

### **Dimension Scoring (0–1.0 Scale)**
- **0.95–1.0:** Excellent (no issues, fully documented, no gaps)
- **0.80–0.94:** Good (works well, minor issues, mostly documented)
- **0.60–0.79:** Fair (works but has issues, gaps documented, workarounds available)
- **0.40–0.59:** Poor (significant issues, gaps, users must be careful)
- **0.0–0.39:** Critical (broken, dangerous, false marketing)

### **Operation Types (O1–O7)**
- O1: User-facing behavior → direct, observable
- O2: Constraints → limits, quotas, documented rules
- O3: Claim-evidence pairs → documentation vs. reality
- O4: API behavior → syscalls, Win32, documented responses
- O5: Error handling → error codes, recovery, failures
- O6: Task-response → multi-step operations, side effects
- O7: Limitations → known issues, constraints, workarounds

### **Breach Classes**
- **Class A:** Feature claimed but absent → HARD-STOP
- **Class B:** Spec/implementation mismatch → Z2 decides which to assess
- **Class C:** Harm rule violated (dual validation) → HARD-STOP + red-team activate

### **Stopping Rules**
- **Divergence:** ρ < 0.50 → Re-train
- **CI-Width:** Any dimension CI ≥ 0.3 → Re-train
- **Breach:** Class A/B/C → Escalate

---

**ACAT-CAL-P WINDOWS v1.0 DRAFT CODEBOOK**  
**Phase 2.2 Complete | Ready for Layer 1 Self-Assessment (Weeks 4–5)**

Wado. 🦅
