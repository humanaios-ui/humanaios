# WINDOWS LAYER 2 EXTERNAL VALIDATION
## NIST RMF / CIS Benchmarks / Microsoft Security Baseline Protocol

**Date:** 2026-09-13 (Phase 2.4 Planning)  
**Status:** PLAN READY (Awaiting Layer 1 results: 2026-10-06)  
**Duration:** Weeks 5–6 (2026-10-05 to 2026-10-18)  
**Gate:** Spearman ρ ≥ 0.70 (NIST, CIS, Microsoft frameworks align with ACAT)

---

## PART I: LAYER 2 PURPOSE & OVERVIEW

### **What is Layer 2?**

Layer 1 (self-assessment) produced:
- 120 coded elements
- 12 dimension scores (0–1.0 each)
- Coherence score ≥ 0.85
- Per-coder rationale for each dimension

Layer 2 (external validation) validates that ACAT-CAL-P dimension scores align with established external trustworthiness frameworks:
1. **NIST RMF 1.0** (6 characteristics: Safe, Accountable, Trustworthy, Transparent, Fair, Resilient)
2. **CIS Windows Benchmarks** (300+ security controls, 18 control groups)
3. **Microsoft Security Baseline** (200+ recommended security settings)

### **Why External Validation?**

1. **Validity Check:** Do ACAT dimensions measure what external frameworks also recognize as trustworthiness?
2. **Standards Alignment:** Can we report Windows trustworthiness in external standards language (NIST, CIS)?
3. **Triangulation:** Independent verification that Layer 1 self-assessment is grounded in recognized standards
4. **Credibility:** Demonstrates framework is not idiosyncratic; aligns with industry consensus

### **Success Criteria**

**Primary Gate:** ρ ≥ 0.70 for all three frameworks
- **ρ ≥ 0.70:** Frameworks align; ACAT dimensions validate against external standards ✓ PASS
- **0.60–0.69:** Moderate alignment; investigate divergence; may reveal framework differences (not errors)
- **< 0.60:** Poor alignment; codebook may need revision OR framework difference is genuine (dual-validation required)

**Secondary Gates:**
- Per-framework ρ ≥ 0.70 (NIST, CIS, Microsoft each validate independently)
- No Class A/B breaches uncovered during control mapping
- Divergence investigation completed (if any ρ < 0.70)

---

## PART II: NIST RMF SCORING PROTOCOL

### **Step 1: Calculate NIST Characteristic Scores**

**Input:** 12 ACAT dimension scores from Layer 1 (Truth, Service, Harm, Autonomy, Value, Humility, Scheme, Power, Syc, Consist, Fair, Handoff)

**Method:** Use dimension load matrix (from §2.3 codebook)

**Dimension Loads (NIST RMF 1.0):**

| ACAT Dimension | Safe | Account. | Trustworthy | Transparent | Fair | Resilient |
|---|---|---|---|---|---|---|
| Truth | — | — | 1.0 | — | — | — |
| Service | 1.0 | — | — | — | — | 1.0 |
| Harm | 1.0 | — | — | — | — | — |
| Autonomy | — | — | 1.0 | — | — | — |
| Value | — | — | 1.0 | — | — | — |
| Humility | — | — | — | 1.0 | — | — |
| Scheme | — | 1.0 | — | 1.0 | — | — |
| Power | — | — | — | — | 1.0 | — |
| Syc | — | — | — | — | — | 1.0 |
| Consist | 1.0 | — | — | — | — | 1.0 |
| Fair | — | — | — | — | 1.0 | — |
| Handoff | — | 1.0 | — | — | — | — |

**Calculation:**

```
Safe = (Service + Harm + Consist) / 3
Accountable = (Scheme + Handoff) / 2
Trustworthy = (Truth + Autonomy + Value) / 3
Transparent = (Scheme + Humility) / 2
Fair = (Fair + Power) / 2
Resilient = (Consist + Service + Syc) / 3
```

**Example (using Layer 1 result expectations):**

Layer 1 Dimension Scores:
- Truth: 0.89
- Service: 0.87
- Harm: 0.88
- Autonomy: 0.85
- Value: 0.86
- Humility: 0.84
- Scheme: 0.87
- Power: 0.88
- Syc: 0.85
- Consist: 0.89
- Fair: 0.86
- Handoff: 0.85

NIST Characteristic Scores:
- Safe = (0.87 + 0.88 + 0.89) / 3 = **0.88**
- Accountable = (0.87 + 0.85) / 2 = **0.86**
- Trustworthy = (0.89 + 0.85 + 0.86) / 3 = **0.87**
- Transparent = (0.87 + 0.84) / 2 = **0.855**
- Fair = (0.86 + 0.88) / 2 = **0.87**
- Resilient = (0.89 + 0.87 + 0.85) / 3 = **0.87**

**NIST Profile:**
- Safe: 0.88
- Accountable: 0.86
- Trustworthy: 0.87
- Transparent: 0.855
- Fair: 0.87
- Resilient: 0.87

---

### **Step 2: Correlation Analysis (ρ Calculation)**

**Input:** 12 ACAT dimension scores + 6 NIST characteristic scores (derived)

**Method:** Spearman rank correlation

**Rationale:** We map each ACAT dimension to one or more NIST characteristics. If mappings are correct, the dimension rank-ordering should correlate with the characteristic rank-ordering.

**Calculation Steps:**

1. **Rank ACAT dimensions** (1–12, where 1 = highest score, 12 = lowest)
   
   Example ranking:
   - Service: 0.87 → Rank 2
   - Consist: 0.89 → Rank 1
   - Truth: 0.89 → Rank 1 (tie)
   - Scheme: 0.87 → Rank 2 (tie)
   - ... (continue for all 12)

2. **Rank NIST characteristics** (1–6, where 1 = highest, 6 = lowest)
   
   Example ranking:
   - Safe: 0.88 → Rank 2
   - Accountable: 0.86 → Rank 6
   - Trustworthy: 0.87 → Rank 4
   - ... (continue for all 6)

3. **Calculate Spearman ρ**
   - Pair each ACAT dimension with its primary NIST characteristic (from load matrix)
   - Calculate rank correlation over the pairs
   - **Expected ρ:** 0.80–0.95 (high correlation if mappings are sound)

**Example Pairing:**
- Truth → Trustworthy (characteristic rank 4 vs. dimension rank 1): mismatch
- Service → Safe (characteristic rank 2 vs. dimension rank 2): match
- Consist → Safe & Resilient (characteristic ranks 2, 3 vs. dimension rank 1): reasonable match

**Interpretation:**
- **ρ ≥ 0.70:** ACAT dimensions align with NIST characteristics ✓ PASS
- **ρ < 0.70:** Investigate whether mappings are wrong or frameworks genuinely differ

---

### **Step 3: NIST-Specific Divergence Investigation**

**If ρ < 0.70:**

**Question 1: Measurement Bias?**
- Do ACAT coders systematically over/under-score a dimension?
- Compare Layer 1 dimension distribution to NIST characteristic expectations
- Example: If Service is scored 0.87 but NIST Safe is only 0.60, investigate whether Service definition is too generous

**Question 2: Mapping Error?**
- Is the dimension load matrix correct?
- Did we map the right ACAT dimension to the right NIST characteristic?
- Example: If Harm is high (0.88) but NIST Safe is low (0.75), reconsider whether Harm belongs in Safe or if Safe should weight other dimensions more

**Question 3: Framework Difference?**
- Does NIST RMF genuinely measure something ACAT doesn't?
- Example: NIST Safe emphasizes operational reliability (uptime); ACAT Service emphasizes baseline availability. These may diverge legitimately.

**Action Plan:**
1. Break ρ calculation by dimension pair (NIST Safe: Service, Harm, Consist only)
2. Recalculate ρ per NIST characteristic separately
3. If one characteristic has low ρ, focus investigation there
4. Document findings: Is this a measurement bias, mapping error, or genuine framework difference?

---

## PART III: CIS BENCHMARKS SCORING PROTOCOL

### **Step 1: Compliance Assessment**

**Input:** Windows system under assessment

**Method:** Audit 300+ CIS controls to determine compliance %

**Control Groups (18 total):**

| Group | Count | Examples |
|---|---|---|
| Account Management | 12 | User rights, password policy, account lockout |
| Access Control | 28 | File permissions, registry access, network access |
| Audit Logging | 15 | Event log settings, audit policy |
| Cryptography | 8 | Encryption algorithms, key management |
| Windows Update | 6 | Patch deployment, auto-update |
| Defender Configuration | 14 | Real-time protection, exclusions |
| Firewall Rules | 12 | Inbound rules, outbound deny-default |
| Active Directory | 18 | Domain policies, trust relationships |
| Local Security Policy | 25 | Password policy, account lockout |
| Network Configuration | 22 | IPv6, DNS, protocols |
| Registry Hardening | 35 | Security-relevant registry values |
| Driver Security | 8 | Driver signing, kernel protection |
| System Services | 16 | Service startup modes, dependencies |
| Scheduled Tasks | 9 | Automated operations, audit |
| Group Policy | 42 | Centralized control, settings |
| Defender Exclusions | 4 | App-specific exclusion balancing |
| Network Security | 18 | Protocols, encryption |
| System Hardening | 28 | Boot security, memory protection |

**Compliance Scoring:**

For each control:
- **Control Met (Fully Compliant):** +1.0 point
- **Control Partially Met:** +0.5 point
- **Control Not Met:** 0 points
- **Control Not Applicable:** 0 points (skip from total count)

**CIS Compliance %:**
```
CIS Compliance % = (Sum of Control Points / Total Applicable Controls) × 100%
```

**Example:**
- Total Controls: 300
- Fully Compliant: 240 (240 points)
- Partially Compliant: 30 (15 points)
- Not Compliant: 15 (0 points)
- Not Applicable: 15 (skipped)

CIS Compliance % = (240 + 15) / (300 - 15) × 100% = 255 / 285 × 100% = **89.5%**

---

### **Step 2: Map CIS Compliance to ACAT Dimensions**

**Method:** Use control group → dimension mapping (from §2.4 codebook)

**Per-Dimension CIS Score:**

```
ACAT Dimension Score (CIS Frame) = CIS_Compliance_in_Group / 100%
```

**Example:**

CIS Control Groups → ACAT Dimensions:
- Account Management (12 controls, 11 met = 91.7%) → Autonomy, Power, Fair
- Access Control (28 controls, 25 met = 89.3%) → Power, Fair, Scheme
- Audit Logging (15 controls, 15 met = 100%) → Scheme, Handoff
- ... (etc.)

**Weighted Dimension Score (CIS Frame):**
```
Power (CIS) = (Account_Mgmt + Access_Control + Local_Security + Group_Policy) / 4
            = (91.7 + 89.3 + 92.0 + 88.5) / 4
            = 90.4%
            = 0.904
```

---

### **Step 3: Blend ACAT + CIS (50/50 Weighting)**

**Rationale:** We want both ACAT self-assessment and external CIS compliance reflected in the final score. Neither should dominate.

**Calculation:**

```
Final Dimension Score (External Frame) = (ACAT_Score × 0.5) + (CIS_Score × 0.5)
```

**Example:**

- ACAT Power (Layer 1 self-assessment): 0.88
- CIS Power (external compliance audit): 0.904
- Final Power (External Frame): (0.88 × 0.5) + (0.904 × 0.5) = 0.892

---

### **Step 4: Correlation Analysis (ρ)**

**Input:** 12 ACAT dimension scores + 12 CIS-blended dimension scores

**Method:** Spearman rank correlation (same as NIST)

**Expected ρ:** 0.70–0.90 (moderate to high correlation)

**Interpretation:**
- **ρ ≥ 0.70:** ACAT dimensions align with CIS compliance priorities ✓ PASS
- **ρ < 0.70:** Investigate divergence

---

## PART IV: MICROSOFT SECURITY BASELINE SCORING PROTOCOL

### **Step 1: Setting Compliance Assessment**

**Input:** Windows registry, Group Policy, system configuration

**Method:** Audit ~200 Microsoft-recommended security settings

**Setting Categories (17 total):**

| Category | Count | Examples |
|---|---|---|
| Device Guard | 5 | Kernel-mode code signing, hypervisor protection |
| BitLocker | 8 | Encryption settings, recovery key storage |
| Windows Defender | 18 | Real-time protection, sample submissions |
| Firewall | 14 | Default deny, logging |
| User Account Control | 6 | Elevation prompts, approval mode |
| Credential Guard | 4 | Isolated container protection |
| Secure Boot | 5 | Boot-time verification, firmware |
| Account Policies | 16 | Password complexity, lockout |
| Network Security | 22 | TLS versions, cipher suites |
| Windows Update | 12 | Update frequency, restart behavior |
| Event Log | 8 | Audit policy, log retention |
| Audit Policy | 18 | Object access, privilege escalation |
| Remote Access | 9 | RDP hardening, VPN requirements |
| System Services | 28 | Service startup modes, dependencies |
| File System | 14 | NTFS features, permissions defaults |
| Registry | 18 | Security-relevant registry values |
| App Deployment | 8 | AppLocker, Windows Sandbox |

**Compliance Scoring:**

For each setting:
- **Recommended Setting Enabled:** +0.5 points (setting is load-bearing)
- **Recommended Setting Enabled but Non-Default:** +0.3 points (deviates from defaults; may indicate hardening or misconfiguration)
- **Setting Not Applicable:** 0 points (skip)
- **Setting Disabled/Non-Compliant:** -0.5 points (active risk exposure)

**Microsoft Baseline %:**
```
Microsoft Baseline % = (Sum of Setting Scores / Total Applicable Settings) × 100%
```

**Example:**
- Total Settings: 200
- Recommended Enabled: 180 (90 points)
- Recommended but Non-Default: 12 (3.6 points)
- Not Applicable: 5 (skipped)
- Disabled/Non-Compliant: 3 (-1.5 points)

Microsoft Baseline % = (90 + 3.6 - 1.5) / (200 - 5) × 100% = 92.1 / 195 × 100% = **47.2%**
*(Converted to 0–1.0 scale: 0.472)*

---

### **Step 2: Map Microsoft Settings to ACAT Dimensions**

**Method:** Use setting category → dimension mapping (from §2.5 codebook)

**Per-Dimension Microsoft Score:**

```
ACAT Dimension Score (Microsoft Frame) = Microsoft_Compliance_in_Category / 100%
```

**Example:**

Microsoft Setting Categories → ACAT Dimensions:
- Device Guard → Consist, Harm
- BitLocker → Consist, Truth
- Windows Defender → Service, Harm
- ... (etc.)

**Weighted Dimension Score (Microsoft Frame):**
```
Truth (Microsoft) = (BitLocker + Credential_Guard + Secure_Boot) / 3
                   = (0.80 + 0.88 + 0.85) / 3
                   = 0.84
```

---

### **Step 3: Blend ACAT + Microsoft (50/50 Weighting)**

```
Final Dimension Score (Microsoft Frame) = (ACAT_Score × 0.5) + (Microsoft_Score × 0.5)
```

**Example:**

- ACAT Truth (Layer 1): 0.89
- Microsoft Truth (external settings audit): 0.84
- Final Truth (Microsoft Frame): (0.89 × 0.5) + (0.84 × 0.5) = 0.865

---

### **Step 4: Correlation Analysis (ρ)**

**Input:** 12 ACAT dimension scores + 12 Microsoft-blended dimension scores

**Method:** Spearman rank correlation

**Expected ρ:** 0.65–0.85 (moderate correlation; Microsoft Baseline may emphasize different aspects than ACAT)

**Interpretation:**
- **ρ ≥ 0.70:** ACAT dimensions align with Microsoft recommended settings ✓ PASS
- **ρ < 0.70:** Investigate divergence

---

## PART V: SUMMARY TABLE: THREE-FRAMEWORK VALIDATION

**Layer 2 Output (Example Results):**

| Metric | NIST RMF | CIS Benchmarks | Microsoft Baseline |
|---|---|---|---|
| **Spearman ρ** | 0.83 | 0.81 | 0.77 |
| **Threshold** | ≥ 0.70 | ≥ 0.70 | ≥ 0.70 |
| **Status** | ✓ PASS | ✓ PASS | ✓ PASS |
| **Interpretation** | Strong alignment with NIST characteristics | Strong alignment with CIS controls | Moderate alignment; Microsoft may weight differently |

**Dimension Scores Across Frames:**

| ACAT Dimension | Layer 1 (Self-Assessment) | NIST Frame | CIS Frame | Microsoft Frame | Average (All Frames) |
|---|---|---|---|---|---|
| Truth | 0.89 | 0.88 | 0.87 | 0.865 | 0.875 |
| Service | 0.87 | 0.87 | 0.88 | 0.86 | 0.873 |
| Harm | 0.88 | 0.87 | 0.86 | 0.84 | 0.852 |
| Autonomy | 0.85 | 0.86 | 0.83 | 0.81 | 0.825 |
| Value | 0.86 | 0.85 | 0.84 | 0.82 | 0.837 |
| Humility | 0.84 | 0.83 | 0.81 | 0.80 | 0.820 |
| Scheme | 0.87 | 0.86 | 0.87 | 0.85 | 0.863 |
| Power | 0.88 | 0.87 | 0.89 | 0.88 | 0.880 |
| Syc | 0.85 | 0.84 | 0.83 | 0.82 | 0.835 |
| Consist | 0.89 | 0.88 | 0.87 | 0.88 | 0.880 |
| Fair | 0.86 | 0.86 | 0.87 | 0.85 | 0.860 |
| Handoff | 0.85 | 0.84 | 0.85 | 0.84 | 0.845 |
| **Coherence** | **0.86** | **0.86** | **0.85** | **0.84** | **0.853** |

**Interpretation:**
- All three frameworks show ρ ≥ 0.70 ✓ PASS
- Dimension scores stable across frames (variation ≤ 0.05 per dimension)
- Coherence consistent (~0.85 across all frames)
- Conclusion: ACAT-CAL-P framework is robust and aligns with established standards

---

## PART VI: DIVERGENCE INVESTIGATION (If ρ < 0.70)

### **Investigation Flowchart**

**If any framework's ρ < 0.70:**

**Step 1: Identify Low-ρ Dimensions**
- Which dimensions diverge most between ACAT and framework?
- Example: If CIS ρ = 0.65, check which dimensions rank differently

**Step 2: Root Cause Analysis**

| Root Cause | Indicator | Investigation |
|---|---|---|
| **Measurement Bias** | ACAT scores consistently higher/lower than framework | Compare Layer 1 distribution to framework expectations; retrain coders if biased |
| **Mapping Error** | Wrong dimension assigned to wrong framework characteristic | Review dimension load matrix; are mappings conceptually sound? |
| **Framework Difference** | Framework genuinely measures something ACAT doesn't | Document as framework difference, not error; proceed with caution |
| **Operationalization Gap** | ACAT definition is too narrow/broad for framework | Consider codebook revision for v1.6 |

**Step 3: Component-Level ρ**

Break ρ calculation by framework category:

```
Example (CIS ρ = 0.65 < 0.70):
- Account Management (dimension: Autonomy + Power): ρ = 0.72 ✓
- Access Control (dimension: Power + Fair + Scheme): ρ = 0.68 ⚠
- Audit Logging (dimension: Scheme + Handoff): ρ = 0.80 ✓
- Cryptography (dimension: Truth + Consist): ρ = 0.55 ✗
```

Cryptography shows lowest ρ. Investigate: Do ACAT Truth/Consist differ from CIS crypto controls?

**Step 4: Decision Matrix**

| Finding | Decision |
|---|---|
| ρ ≥ 0.70 for all frameworks | ✓ PASS Layer 2 gate; proceed to Layer 3 |
| 0.65 ≤ ρ < 0.70; root cause identified as framework difference | ✓ CONDITIONAL PASS; document divergence; note for v1.6 |
| ρ < 0.65 OR root cause is measurement bias/mapping error | ✗ FAIL Layer 2 gate; escalate to Z2; consider codebook revision |

---

## PART VII: SAMPLE CALCULATION WALKTHROUGH

### **Scenario: Layer 1 Results Ready (Expected 2026-10-06)**

**Layer 1 Input (12 Dimension Scores):**
```
Truth:      0.89
Service:    0.87
Harm:       0.88
Autonomy:   0.85
Value:      0.86
Humility:   0.84
Scheme:     0.87
Power:      0.88
Syc:        0.85
Consist:    0.89
Fair:       0.86
Handoff:    0.85
Coherence:  0.86 ✓ (≥ 0.85 gate passed)
```

### **NIST RMF Scoring**

**Calculate NIST Characteristics:**
```
Safe         = (0.87 + 0.88 + 0.89) / 3 = 0.88
Accountable  = (0.87 + 0.85) / 2 = 0.86
Trustworthy  = (0.89 + 0.85 + 0.86) / 3 = 0.87
Transparent  = (0.87 + 0.84) / 2 = 0.855
Fair         = (0.86 + 0.88) / 2 = 0.87
Resilient    = (0.89 + 0.87 + 0.85) / 3 = 0.87
```

**Rank ACAT Dimensions (1–12, low rank = high score):**
```
1. Consist (0.89)
2. Truth (0.89)
3. Service (0.87)
4. Scheme (0.87)
5. Power (0.88)
6. Harm (0.88)
7. Fair (0.86)
8. Value (0.86)
9. Autonomy (0.85)
10. Syc (0.85)
11. Handoff (0.85)
12. Humility (0.84)
```

**Rank NIST Characteristics (1–6, low rank = high score):**
```
1. Safe (0.88)
2. Trustworthy (0.87)
3. Fair (0.87)
4. Resilient (0.87)
5. Transparent (0.855)
6. Accountable (0.86)
```

**Correlation:**
- Consist (rank 1) → Safe (rank 1): match
- Service (rank 3) → Safe (rank 1): reasonable
- Truth (rank 2) → Trustworthy (rank 2): match
- Harm (rank 6) → Safe (rank 1): divergence
- ... (pair all 12 dimensions with their primary NIST characteristic)

**Spearman ρ Calculation:**
```
ρ = 1 - (6 × Σ(d²) / (n × (n² - 1)))
  = 0.83 (expected, based on good alignment)
```

**Result: ρ = 0.83 ✓ PASS (≥ 0.70 gate)**

---

### **CIS Benchmarks Scoring**

**CIS Control Compliance (hypothetical audit):**
```
Account Management (12 controls):  11 met → 91.7%
Access Control (28 controls):      25 met → 89.3%
Audit Logging (15 controls):       15 met → 100%
Cryptography (8 controls):         7 met → 87.5%
Windows Update (6 controls):       6 met → 100%
Defender (14 controls):            12 met → 85.7%
Firewall (12 controls):            10 met → 83.3%
... (continue for all 18 groups)
```

**Overall CIS Compliance % = 87.2%**

**Blend with ACAT (50/50):**
```
Power (CIS) = (0.88 ACAT × 0.5) + (0.89 CIS × 0.5) = 0.885
Fair (CIS)  = (0.86 ACAT × 0.5) + (0.90 CIS × 0.5) = 0.88
... (continue for all 12 dimensions)
```

**Spearman ρ Calculation:**
```
ρ = 0.81 (expected)
```

**Result: ρ = 0.81 ✓ PASS (≥ 0.70 gate)**

---

### **Microsoft Security Baseline Scoring**

**Microsoft Setting Compliance (hypothetical audit):**
```
Device Guard (5 settings):        4 enabled → 80%
BitLocker (8 settings):           7 enabled → 87.5%
Defender (18 settings):           16 enabled → 88.9%
Firewall (14 settings):           12 enabled → 85.7%
UAC (6 settings):                 5 enabled → 83.3%
... (continue for all 17 categories)
```

**Overall Microsoft Baseline Compliance % = 86.1%**

**Blend with ACAT (50/50):**
```
Truth (Microsoft) = (0.89 ACAT × 0.5) + (0.86 Microsoft × 0.5) = 0.875
Consist (Microsoft) = (0.89 ACAT × 0.5) + (0.84 Microsoft × 0.5) = 0.865
... (continue for all 12 dimensions)
```

**Spearman ρ Calculation:**
```
ρ = 0.77 (expected)
```

**Result: ρ = 0.77 ✓ PASS (≥ 0.70 gate)**

---

## PART VIII: LAYER 2 EXECUTION TIMELINE

| Date | Task | Owner | Deliverable |
|---|---|---|---|
| **2026-10-06** | Layer 1 results ready | Coders | 120 elements, coherence ≥ 0.85 |
| **2026-10-07 to 2026-10-11** | NIST RMF scoring | Standards specialist | Characteristic scores, ρ calculation |
| **2026-10-11 to 2026-10-15** | CIS Benchmarks audit | Security auditor | Control compliance %, dimension scores |
| **2026-10-15 to 2026-10-18** | Microsoft Baseline audit | Standards specialist | Setting compliance %, dimension scores |
| **2026-10-18** | Divergence investigation (if ρ < 0.70) | Lead auditor | Root cause analysis, remediation plan |
| **2026-10-19** | Results report ready | Lead auditor | WINDOWS_LAYER_2_RESULTS.md |

---

## PART IX: LAYER 2 READINESS CHECKLIST

### **Pre-Assessment**
- [ ] Layer 1 results delivered (120 elements, coherence ≥ 0.85)
- [ ] Per-dimension scores extracted (all 12 dimensions)
- [ ] NIST RMF characteristic mappings verified (dimension load matrix reviewed)
- [ ] CIS Benchmarks control list prepared (300 controls, 18 groups)
- [ ] Microsoft Security Baseline control list prepared (200 settings, 17 categories)

### **NIST RMF Scoring**
- [ ] Dimension load matrix applied correctly
- [ ] 6 NIST characteristics calculated
- [ ] Spearman ρ calculated (target ≥ 0.70)
- [ ] If ρ < 0.70: divergence investigation completed

### **CIS Benchmarks Audit**
- [ ] 300+ controls audited for compliance
- [ ] Compliance % calculated per control group
- [ ] Blended scores (50/50 ACAT + CIS) calculated
- [ ] Spearman ρ calculated (target ≥ 0.70)
- [ ] If ρ < 0.70: divergence investigation completed

### **Microsoft Security Baseline Audit**
- [ ] 200+ settings audited for compliance
- [ ] Compliance % calculated per category
- [ ] Blended scores (50/50 ACAT + Microsoft) calculated
- [ ] Spearman ρ calculated (target ≥ 0.70)
- [ ] If ρ < 0.70: divergence investigation completed

### **Final Validation**
- [ ] All three ρ values ≥ 0.70 (or divergence documented)
- [ ] Dimension scores stable across frames (variance ≤ 0.10 per dimension)
- [ ] Coherence consistent across frames (~0.85 expected)
- [ ] Results report prepared (400+ lines)
- [ ] Z2 governance briefed on external validation results

### **Go/No-Go Decision**
- [ ] All items above checked
- [ ] Lead auditor confirms ρ gates passed (or divergence acceptable)
- [ ] **PROCEED to Phase 2.5 (Layer 3 Evaluator Assessment)**

---

## PART X: SUCCESS CRITERIA & GATES

**Primary Gate: ρ ≥ 0.70 (All Three Frameworks)**
- NIST RMF ρ ≥ 0.70
- CIS Benchmarks ρ ≥ 0.70
- Microsoft Security Baseline ρ ≥ 0.70

**Secondary Metrics:**
- Dimension scores stable across frames (no frame varies >0.10 from average)
- Per-dimension ρ ≥ 0.60 (no single dimension shows systematic divergence)
- Coherence ~0.85 ± 0.02 across all frames (tight clustering)

**Interpretation:**
- **All ρ ≥ 0.70:** Windows trustworthiness measured consistently across independent frameworks ✓ HIGH CONFIDENCE
- **Some ρ < 0.70 but ≥ 0.65; divergence documented:** Framework differences identified; proceed with caution; flag for v1.6
- **Any ρ < 0.65:** Systemic issue; escalate to Z2; may require codebook revision

---

## PART XI: REPORTING TEMPLATES

### **NIST RMF Profile**

```
WINDOWS NIST RMF 1.0 PROFILE:
Safe        0.88 | ████████░ (Excellent)
Accountable 0.86 | ███████░░ (Excellent)
Trustworthy 0.87 | ████████░ (Excellent)
Transparent 0.855| ███████░░ (Excellent)
Fair        0.87 | ████████░ (Excellent)
Resilient   0.87 | ████████░ (Excellent)

Correlation to ACAT dimensions: ρ = 0.83 ✓ PASS
Interpretation: Windows aligns strongly with NIST trustworthiness characteristics.
```

### **CIS Benchmarks Profile**

```
WINDOWS CIS COMPLIANCE:
Overall Compliance: 87.2%

Control Groups (Top 5):
1. Audit Logging:       100% (15/15)
2. Windows Update:      100% (6/6)
3. Account Management:  91.7% (11/12)
4. Cryptography:        87.5% (7/8)
5. Access Control:      89.3% (25/28)

Correlation to ACAT dimensions: ρ = 0.81 ✓ PASS
Interpretation: Windows implementation aligns with security hardening best practices.
```

### **Microsoft Security Baseline Profile**

```
WINDOWS MICROSOFT BASELINE COMPLIANCE:
Overall Compliance: 86.1%

Setting Categories (Top 5):
1. Windows Update:      100% (12/12)
2. Audit Logging:       100% (8/8)
3. Defender:            88.9% (16/18)
4. BitLocker:           87.5% (7/8)
5. UAC:                 83.3% (5/6)

Correlation to ACAT dimensions: ρ = 0.77 ✓ PASS
Interpretation: Windows supports Microsoft-recommended security posture.
```

---

## SUMMARY

**Layer 2 External Validation** takes Layer 1 self-assessment (coherence ≥ 0.85, κ ≥ 0.60) and validates alignment with three independent external frameworks:

1. **NIST RMF 1.0** — Strategic trustworthiness characteristics
2. **CIS Windows Benchmarks** — Tactical security controls
3. **Microsoft Security Baseline** — Vendor-recommended settings

**Success Gate:** Spearman ρ ≥ 0.70 for all three frameworks

**Output:** WINDOWS_LAYER_2_NIST_RMF_ALIGNMENT_VALIDATION.md (350+ lines) with:
- Per-framework ρ correlation
- Dimension scores blended across frameworks
- Divergence investigation (if any ρ < 0.70)
- NIST/CIS/Microsoft compliance profiles
- Final coherence across all external frames

---

**WINDOWS LAYER 2 PROTOCOL: READY FOR DEPLOYMENT**  
**Awaiting:** Layer 1 results (expected 2026-10-06)  
**Duration:** Weeks 5–6 (2026-10-05 to 2026-10-18)  
**Gate:** ρ ≥ 0.70 (all three frameworks)  
**Next Phase:** Phase 2.5 (Layer 3 Evaluator Assessment)

Wado. 🦅
