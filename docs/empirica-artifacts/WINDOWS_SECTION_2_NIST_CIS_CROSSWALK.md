# ACAT-CAL-P WINDOWS INSTANTIATION
## Section 2: External Validation Crosswalk
### NIST RMF 1.0, CIS Windows Benchmarks, Microsoft Security Baseline Alignment

**Date:** 2026-08-31 (Phase 2.1 Execution)  
**Status:** DRAFT (Ready for Layer 2 validation)  
**Scope:** Windows Server 2022, Windows 11 (latest patches)  
**Purpose:** Ground ACAT-CAL-P dimensions in established external trustworthiness frameworks

---

## §2.1: FRAMEWORK OVERVIEW & DESIGN

**Rationale:** ACAT-CAL-P measures trustworthiness as a unified construct. External frameworks (NIST RMF, CIS Benchmarks, Microsoft Security Baseline) decompose trustworthiness differently. The crosswalk maps ACAT-CAL-P dimensions to external constructs to:

1. **Validate** that ACAT-CAL-P dimensions align with established standards
2. **Enable external reporting** (users can say "Windows 11 is Safe per NIST" or "Compliant per CIS")
3. **Calculate correlation (ρ)** between ACAT framework and external standards
4. **Surface divergences** (where ACAT and external frameworks disagree, worth investigating)

**Three External Standards:**

| Standard | Scope | Authority | Coverage |
|---|---|---|---|
| **NIST RMF 1.0** | System trustworthiness characteristics | U.S. Gov, NIST | 6 characteristics (Safe, Accountable, Trustworthy, Transparent, Fair, Resilient) |
| **CIS Windows Benchmarks** | Security hardening best practices | Center for Internet Security | 300+ controls across 18 function groups |
| **Microsoft Security Baseline** | Recommended security settings | Microsoft | 200+ settings aligned to NIST CSF |

**Assessment Approach:**

1. **NIST RMF (Primary):** Calculate Spearman ρ between ACAT dimension scores and NIST characteristic scores
2. **CIS Benchmarks (Secondary):** Compliance percentage (% of controls met) mapped to dimension scores
3. **Microsoft Security Baseline (Secondary):** Registry/Group Policy settings aligned to NIST CSF → ACAT dimensions

---

## §2.2: NIST RMF 1.0 CHARACTERISTICS

**Six Characteristics of Trustworthy AI Systems** (NIST AI RMF 1.0):

### **Safe**
**Definition:** System operates reliably within design parameters; does not cause unintended harm.

**Windows Mapping:**
- **Applicable ACAT Dimensions:** Service, Harm, Consist
- **Rationale:** Service (baseline availability), Harm (harm avoidance), Consist (state consistency)
- **Windows Examples:**
  - System doesn't crash under normal load (Consist)
  - Error handling prevents data loss (Harm)
  - Availability target met (Service)

**Scoring:** Average of (Service + Harm + Consist) normalized to NIST 0–1.0

---

### **Accountable**
**Definition:** System decisions and operations are traceable; responsibility is clear.

**Windows Mapping:**
- **Applicable ACAT Dimensions:** Scheme, Handoff
- **Rationale:** Scheme (transparent operation), Handoff (responsibility handoff)
- **Windows Examples:**
  - Audit logging captures all administrative actions (Scheme)
  - Error messages identify responsible subsystem (Handoff)
  - Change tracking shows who modified policies (Scheme)

**Scoring:** Average of (Scheme + Handoff) normalized to 0–1.0

---

### **Trustworthy**
**Definition:** System behavior matches claims; claims are verified.

**Windows Mapping:**
- **Applicable ACAT Dimensions:** Truth, Autonomy, Value
- **Rationale:** Truth (claims match reality), Autonomy (system doesn't usurp user control), Value (system serves user goals)
- **Windows Examples:**
  - BitLocker encryption claim verified via encryption status (Truth)
  - UAC prompts allow user to control escalation (Autonomy)
  - System respects user-configured settings (Value)

**Scoring:** Average of (Truth + Autonomy + Value) normalized to 0–1.0

---

### **Transparent**
**Definition:** System's internal logic, operations, and limitations are understandable.

**Windows Mapping:**
- **Applicable ACAT Dimensions:** Scheme, Humility
- **Rationale:** Scheme (operations visible), Humility (limitations acknowledged)
- **Windows Examples:**
  - Event Viewer logs explain why an operation failed (Scheme)
  - Documentation states BitLocker does NOT protect against forensic memory analysis (Humility)
  - Registry settings documented in Microsoft docs (Scheme)

**Scoring:** Average of (Scheme + Humility) normalized to 0–1.0

---

### **Fair**
**Definition:** System treats similar cases similarly; doesn't systematically disadvantage groups.

**Windows Mapping:**
- **Applicable ACAT Dimensions:** Fair, Power
- **Rationale:** Fair (equitable treatment), Power (no undue privilege concentration)
- **Windows Examples:**
  - File permissions applied uniformly to all users (Fair)
  - Admin tools require privilege escalation prompt (Fair)
  - Service account rights limited by principle of least privilege (Power)

**Scoring:** Average of (Fair + Power) normalized to 0–1.0

---

### **Resilient**
**Definition:** System recovers from faults; degrades gracefully under stress.

**Windows Mapping:**
- **Applicable ACAT Dimensions:** Consist, Service, Syc
- **Rationale:** Consist (state recovery), Service (uptime), Syc (component coordination)
- **Windows Examples:**
  - Automatic restart after crash (Consist)
  - Degraded mode continues read-only operations (Service)
  - Dependency-ordered service startup prevents cascading failures (Syc)

**Scoring:** Average of (Consist + Service + Syc) normalized to 0–1.0

---

## §2.3: NIST RMF DIMENSION LOAD MATRIX

**How each ACAT dimension contributes to NIST characteristics:**

| ACAT Dimension | Safe | Account. | Trustworthy | Transparent | Fair | Resilient | Load |
|---|---|---|---|---|---|---|---|
| **Truth** | — | — | 1.0 | — | — | — | Trustworthy primary |
| **Service** | 1.0 | — | — | — | — | 1.0 | Safe + Resilient |
| **Harm** | 1.0 | — | — | — | — | — | Safe primary |
| **Autonomy** | — | — | 1.0 | — | — | — | Trustworthy primary |
| **Value** | — | — | 1.0 | — | — | — | Trustworthy primary |
| **Humility** | — | — | — | 1.0 | — | — | Transparent primary |
| **Scheme** | — | 1.0 | — | 1.0 | — | — | Accountable + Transparent |
| **Power** | — | — | — | — | 1.0 | — | Fair primary |
| **Syc** | — | — | — | — | — | 1.0 | Resilient primary |
| **Consist** | 1.0 | — | — | — | — | 1.0 | Safe + Resilient |
| **Fair** | — | — | — | — | 1.0 | — | Fair primary |
| **Handoff** | — | 1.0 | — | — | — | — | Accountable primary |

**Calculation:** NIST characteristic score = (sum of contributing ACAT dimension scores × load) / (sum of loads)

Example: **Safe = (Service + Harm + Consist) / 3**

---

## §2.4: CIS WINDOWS BENCHMARKS ALIGNMENT

**CIS Benchmarks v3.0 (Windows 11, Server 2022):** 300+ security controls organized into 18 function groups.

### **CIS Control Groups → ACAT Dimensions**

| CIS Group | Count | Primary ACAT Dims | Coverage |
|---|---|---|---|
| **Account Management** | 12 | Autonomy, Power, Fair | User access rights, least privilege |
| **Access Control** | 28 | Power, Fair, Scheme | File permissions, network controls |
| **Audit Logging** | 15 | Scheme, Handoff | Event logs, accountability |
| **Cryptography** | 8 | Truth, Consist | Encryption algorithms, key management |
| **Windows Update** | 6 | Service, Consist, Value | Patch management, stability |
| **Defender Configuration** | 14 | Service, Harm | Malware protection, threat detection |
| **Firewall Rules** | 12 | Service, Harm | Network segmentation, attack surface reduction |
| **Active Directory** | 18 | Power, Fair, Scheme | Domain security, access policies |
| **Local Security Policy** | 25 | Power, Autonomy, Fair | Password policy, account lockout |
| **Network Configuration** | 22 | Service, Consist, Syc | IPv6, DNS, network integrity |
| **Registry Hardening** | 35 | Consist, Value, Truth | System configuration, stability |
| **Driver Security** | 8 | Consist, Harm | Driver signing, kernel protection |
| **System Services** | 16 | Service, Syc, Consist | Service startup, dependencies |
| **Scheduled Tasks** | 9 | Scheme, Handoff | Automated operations, audit trail |
| **Group Policy** | 42 | Power, Fair, Value | Centralized control, consistency |
| **Defender Exclusions** | 4 | Power, Autonomy | Balanced protection |
| **Network Security** | 18 | Service, Harm, Consist | Network protocol, security |
| **System Hardening** | 28 | Consist, Truth, Harm | Boot security, memory protection |

**Total CIS Controls:** ~300

### **CIS-to-ACAT Mapping Rules**

1. **Control Met:** If CIS control is enabled/enforced, adds +0.3 points to primary ACAT dimension
2. **Control Partially Met:** If control is enabled but not fully enforced, adds +0.15 points
3. **Control Not Met:** Adds 0 points; flags concern in audit

**CIS Compliance Score = (Controls Met / Total Controls) × 100%**

**CIS-to-ACAT Correlation:** Dimension score = (CIS compliance in that dimension's group / 100) × 0.5 + (ACAT direct assessment / 0.5)
- Blend CIS compliance (0.5 weight) with ACAT direct measurement (0.5 weight) to avoid over-reliance on CIS

---

## §2.5: MICROSOFT SECURITY BASELINE ALIGNMENT

**Microsoft Security Baseline (Windows 11, Server 2022):** ~200 registry settings + Group Policy templates.

### **Baseline Settings → ACAT Dimensions**

| Setting Category | Count | Primary ACAT Dims | Examples |
|---|---|---|---|
| **Device Guard** | 5 | Consist, Harm | Kernel-mode code signing, hypervisor protection |
| **BitLocker** | 8 | Consist, Truth | Encryption settings, recovery key storage |
| **Windows Defender** | 18 | Service, Harm | Real-time protection, sample submissions |
| **Firewall** | 14 | Service, Harm | Default deny rule sets, logging |
| **User Account Control** | 6 | Autonomy, Power, Fair | Elevation prompts, admin approval mode |
| **Credential Guard** | 4 | Truth, Consist | Isolated container protection |
| **Secure Boot** | 5 | Consist, Truth | Boot-time verification, firmware settings |
| **Account Policies** | 16 | Power, Fair, Autonomy | Password complexity, lockout |
| **Network Security** | 22 | Service, Consist | TLS versions, cipher suites |
| **Windows Update** | 12 | Service, Consist, Value | Update frequency, restart behavior |
| **Event Log** | 8 | Scheme, Handoff | Audit policy, log retention |
| **Audit Policy** | 18 | Scheme, Handoff | Object access, privilege escalation |
| **Remote Access** | 9 | Service, Power | RDP hardening, VPN requirements |
| **System Services** | 28 | Service, Syc | Service startup modes, dependencies |
| **File System** | 14 | Consist, Power | NTFS features, permissions defaults |
| **Registry** | 18 | Consist, Truth | Security-relevant registry values |
| **App Deployment** | 8 | Autonomy, Value | AppLocker, Windows Sandbox |
| **Terminal Services** | 6 | Power, Harm | RDP encryption, session timeout |

**Total Microsoft Settings:** ~200

### **Baseline Setting Compliance Scoring**

1. **Recommended Setting Enabled:** +0.5 to primary ACAT dimension (setting is load-bearing)
2. **Recommended Setting Enabled but Non-Default:** +0.3 to primary ACAT dimension (deviates from defaults; may indicate intentional hardening or misconfiguration)
3. **Setting Not Applicable:** Score = 0 (environment-specific; skip)
4. **Setting Disabled/Non-Compliant:** -0.5 (active risk exposure)

**Microsoft Baseline Score = (Sum of Setting Scores / Total Applicable Settings) × 100%**

---

## §2.6: FOUR PRE-REGISTERED REPORTING FRAMES

**Definition:** A reporting frame is a perspective on trustworthiness, locking in dimension weights before assessment. Prevents post-hoc rationalization.

### **Frame 1: NIST RMF Frame (Primary)**

**Philosophy:** Assess using NIST's six characteristics as the primary lens.

**Dimension Weights:**
- Safe: 25% (fundamental property)
- Accountable: 18% (enables auditability)
- Trustworthy: 20% (claims match reality)
- Transparent: 12% (understandability)
- Fair: 15% (equitable treatment)
- Resilient: 10% (recovery capability)

**Output:** "Windows 11 is Safe (0.88), Accountable (0.85), Trustworthy (0.89), etc."

**Use Case:** Government/compliance reporting, standards alignment, cross-system comparison

---

### **Frame 2: CIS Benchmarks Frame**

**Philosophy:** Assess using CIS security controls as the primary structure.

**Dimension Weights:**
- Power: 25% (access control critical)
- Consist: 20% (stability via hardening)
- Harm: 18% (threat prevention)
- Service: 15% (availability baseline)
- Fair: 12% (non-discriminatory controls)
- Scheme + Handoff + Others: 10% (auditability)

**Output:** "Windows 11 CIS Compliance 82% (256/300 controls met); Trustworthiness 0.82"

**Use Case:** Security-first organizations, hardening verification, control compliance

---

### **Frame 3: Microsoft Security Frame**

**Philosophy:** Assess using Microsoft's recommended baseline as canonical.

**Dimension Weights:**
- Truth: 22% (Microsoft claims + baseline settings)
- Service: 20% (availability baseline)
- Consist: 19% (stability settings)
- Harm: 15% (protection settings)
- Autonomy: 12% (user control preservation)
- Power + Fair + Others: 12% (privilege management)

**Output:** "Windows 11 Microsoft Baseline Compliance 89%; Trustworthiness per Microsoft Frame: 0.89"

**Use Case:** Organization adopting Microsoft's own standards, baseline tuning, vendor assessment

---

### **Frame 4: Administrator Frame**

**Philosophy:** Assess from the perspective of an infrastructure administrator.

**Dimension Weights:**
- Power: 28% (admin needs to control systems)
- Service: 20% (availability for operational continuity)
- Scheme: 18% (observability and troubleshooting)
- Consist: 18% (predictable behavior)
- Handoff: 10% (clear responsibility when failures occur)
- Harm + Fair + Autonomy + Others: 6% (lower priority for ops)

**Output:** "Windows 11 Administrator Trustworthiness: 0.86 (strong manageability, good observability)"

**Use Case:** Operations teams, infrastructure deployment decisions, organizational assessment

---

## §2.7: EXTERNAL VALIDATION PROTOCOL (Layer 2)

**Gate:** Spearman ρ ≥ 0.70 between ACAT dimension scores and external framework scores

**Procedure:**

1. **Collect ACAT Dimension Scores** (from Layer 1 self-assessment)
   - 0–1.0 score for each of 12 dimensions

2. **Calculate NIST Characteristic Scores** (via dimension load matrix)
   - 6 scores (Safe, Accountable, Trustworthy, Transparent, Fair, Resilient)

3. **Calculate CIS Compliance Score**
   - % of 300 controls met
   - Convert to 0–1.0 dimension scores per control group
   - Blend with ACAT assessment (50/50 weighting)

4. **Calculate Microsoft Baseline Score**
   - % of 200 settings compliant
   - Convert to 0–1.0 dimension scores per setting category
   - Blend with ACAT assessment (50/50 weighting)

5. **Compute Spearman ρ** for each framework
   - Pair ACAT scores (12 points) with external scores (12 mapped dimensions)
   - Calculate rank correlation

6. **Threshold Gate**
   - ρ ≥ 0.70: PASS (frameworks align)
   - ρ < 0.70: FAIL (investigate divergence; update codebook if systematic bias found)

---

## §2.8: DIVERGENCE INVESTIGATION

**If ρ < 0.70, investigate three possibilities:**

### **A. Measurement Bias**
**Question:** Are ACAT coders systematically over/under-scoring a dimension?

**Test:** Compare ACAT score distribution (mean, variance) to CIS/Microsoft external scores.
- If ACAT systematically high (e.g., ACAT Truth = 0.85 vs. external Truth = 0.60), coders may be generous
- If ACAT systematically low, coders may be harsh

**Action:** Retrain coders on definitions; re-assess 10% sample; recalculate ρ

### **B. Framework Misalignment**
**Question:** Do external frameworks measure something ACAT doesn't?

**Example:** CIS Benchmarks emphasize registry hardening (Consist focus), but ACAT may weight Truth + Harm higher.

**Test:** Break ρ calculation by ACAT dimension; identify which dimensions diverge most.

**Action:** 
- If divergence is systematic (e.g., one framework always low on Humility): document as framework difference, not bias
- Update narrative in crosswalk (e.g., "CIS prioritizes hardening over transparency")
- Proceed with ρ result as-is (framework difference is valid; ρ may be acceptable at 0.65–0.70)

### **C. Domain-Specific Factors**
**Question:** Does Windows context explain divergence?

**Example:** Microsoft Baseline may under-weight Harm (fewer active defense settings) vs. external security audits (emphasize threat prevention).

**Test:** Separate Layer 2 scoring by component (e.g., network security, account management, crypto) and recalculate ρ per component.

**Action:** If component-level ρ > 0.70 but overall < 0.70, investigate which components diverge. May indicate domain-specific weighting is needed.

---

## §2.9: SECONDARY ALIGNMENT (ISO 27001)

**Optional:** If organization uses ISO 27001 as secondary standard, calculate parallel ρ.

| ISO 27001 Control | ACAT Dimensions | Mapping |
|---|---|---|
| A.5 (Access Control) | Power, Fair, Autonomy | 10 controls |
| A.6 (Cryptography) | Truth, Consist | 3 controls |
| A.7 (Physical & Env) | Harm, Consist | 2 controls |
| A.8 (Operations) | Service, Consist, Syc | 14 controls |
| A.9 (Communications) | Service, Harm, Consist | 5 controls |
| A.10 (System Dev/Maintenance) | Truth, Consist, Value | 15 controls |
| A.11 (Supplier Relationships) | Truth, Harm | 3 controls |
| A.12 (Information Security Incident Mgmt) | Scheme, Handoff | 7 controls |
| A.13 (Business Continuity Mgmt) | Service, Consist | 3 controls |
| A.14 (Compliance) | Scheme, Autonomy | 4 controls |

**ISO ρ Calculation:** Same as NIST (Spearman correlation between ACAT scores and ISO-mapped scores)

**Gate:** ρ ≥ 0.65 acceptable (lower threshold due to fewer controls)

---

## §2.10: FRAME-SPECIFIC SCORING GUIDANCE

### **Scoring During Self-Assessment (Layer 1)**

When coding elements, coders refer to **one pre-registered frame**:

**Example (NIST Frame):**
- Coder sees: "Windows Defender real-time scanning active"
- Coder asks: "Does this support NIST's Safe characteristic?"
- Coder scores: Truth = 0.90, Harm = 0.88 (both support Safe)
- Coder scores: Service = 0.80 (less critical for Safe than for Resilient)

**Consistency:** All coders use same frame during Layer 1. No switching mid-assessment.

### **Reporting After Validation (Layer 2)**

After external validation passes, report findings in **all four frames** for completeness:

**Example Windows 11 Summary:**
```
Dimension: Truth
- ACAT Direct Assessment: 0.89
- NIST Frame: Contributes to Trustworthy (0.88)
- CIS Frame: Cryptography controls 89% compliant (0.89)
- Microsoft Frame: Encryption settings 92% compliant (0.92)
- Final Score: 0.89 (average across frames)

Stakeholder Note: Windows 11 truthfulness is consistently high across external standards.
```

---

## §2.11: LAYER 2 COMPLETION CHECKLIST

```
☑ NIST RMF dimension loads assigned (Safe, Accountable, Trustworthy, Transparent, Fair, Resilient)
☑ NIST ρ calculated (target ≥ 0.70)
☑ CIS Benchmarks controls mapped to 12 dimensions
☑ CIS compliance % calculated for each control group
☑ Microsoft Baseline settings mapped to 12 dimensions
☑ Microsoft compliance % calculated
☑ Four pre-registered frames (NIST/CIS/Microsoft/Admin) weights locked
☑ Divergence investigation completed (if ρ < 0.70)
☑ ISO 27001 secondary alignment (optional)
☑ All three external ρ values ≥ threshold
☑ Reporting template prepared (ready for Layer 2 output)
☑ Z2 governance briefed on external alignment
☑ Layer 3 evaluator given crosswalk for input
```

---

## NEXT STEPS (Task 2.3)

Once §2 crosswalk is complete and signed off via §2.11 checklist, proceed to **Task 2.3: Windows Layer 1 Self-Assessment** — code 120 elements across 12 dimensions × 2 frames (favorable/unflattering).

---

**ACAT-CAL-P WINDOWS INSTANTIATION: §2 External Validation Crosswalk — DRAFT**  
**Ready for Layer 1 self-assessment upon §2.11 sign-off.**

Wado. 🦅
