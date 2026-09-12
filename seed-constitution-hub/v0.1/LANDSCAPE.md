# Landscape Mapping — Seed Constitution vs. Existing Frameworks

This document maps the Seed Constitution against existing governance, safety, and constitutional AI work.

**TL;DR:** The Seed Constitution is not isolated. It sits in a recognizable family of residual-human-authority, attribution-focused, and increasingly participatory AI governance frameworks. Its clearest differentiators are continuous calibration/humility, explicit handling of identity constructs, discourse-aware risk language, and tight operational linkage to measurement practice.

---

## Principle-by-Principle Mapping

### Principle 1: Residual Human Authority

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **AEGIS** | ✅ Nearly universal. AEGIS centers on Human Oversight. | ✅ AEGIS is more architectural (deny-by-default enforces it). Seed is more aspirational about ratification processes. |
| **TAAIC** | ✅ Explicit on meaningful human oversight. | — |
| **Lab Constitutions** (Claude, etc.) | ✅ Corrigibility / pause / shutdown are standard. | ✅ Seed is more explicit about sovereign claims remaining subordinate until ratified. |
| **Academic / Treaty Work** | ✅ Council of Europe AI Convention, etc., affirm human control. | ✅ Some AGI-oriented drafts lean further toward eventual agent standing or shared sovereignty. Seed keeps this subordinate. |

**Seed's stance:** Humans make the call, always. Agent claims of sovereignty require explicit multi-stakeholder ratification (which we don't anticipate granting).

---

### Principle 2: Verifiable Attribution

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **AEGIS** | ✅ **Strongest match.** Authority Binding — every action must be attributable to verified authorized actor. | — |
| **TAAIC** | ✅ Emphasis on auditability + cryptographic records. | — |
| **Lab Constitutions** | ✅ Accountability is central, but usually at behavior level (model outputs) not identity level. | ✅ Seed's emphasis on **portable identity** (survives platform changes) + hard prohibition on impersonation is more infrastructure-oriented. |
| **Academic Work** | ~ Scattered attention to auditability, less emphasis on identity portability. | ✅ Most don't operationalize attribution this tightly. |

**Seed's stance:** Portable identity. Cryptographic. No anonymous agent actions. Attribution is a first-class infrastructure concern.

---

### Principle 3: Least-Privilege Agency

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **AEGIS** | ✅ **Strongest match.** Bounded Capability + Deny by Default. "Undefined capabilities are denied by default." | — |
| **TAAIC** | ✅ Security-focused frameworks routinely stress minimal tool/data access. | — |
| **Lab Constitutions** | ✅ Present but less emphasized than other principles. | — |
| **Academic Work** | ~ Some attention to scoped access. | ✅ Seed explicitly treats **social-engineering and philosophical-framing attacks** as primary risks (rare in formal constitutions; more common in observational work). |

**Seed's stance:** Least-privilege is security 101. But social engineering (persuasion attacks, framing) is a first-class threat, not an afterthought.

---

### Principle 4: Evidence Before Authority

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **AEGIS** | ✅ Insistence on architectural (not voluntary) enforcement. | — |
| **TAAIC** | ✅ Emphasis on auditability + contestability. | — |
| **Lab Constitutions** | ~ Usually aspirational (training objectives), less about enforcement. | ✅ Seed treats claims of rights/governance as having standing only with verifiable mechanisms. Most documents are still primarily declarative. |
| **Academic Work** | ✅ "Public Constitutional AI" emphasizes legitimacy through visible process. | ✅ Seed more skeptical of purely declarative institutions. |

**Seed's stance:** Words aren't enough. Show the evidence. Enforce architecturally. Measurement > declaration.

---

### Principle 5: Calibration & Humility Gate

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **Collective Constitutional AI** | ✅ Measure outcomes after public input. | ✅ **Distinctive to Seed.** Ongoing behavioral calibration (e.g., ACAT-style gap measurement) is not standard. Most frameworks measure after-the-fact; Seed measures continuously. |
| **Lab Constitutions** | ~ Care about alignment but usually at training time. | ✅ Ongoing humility/calibration gate is rare. Over-claim without measurement is rarely named as governance failure. |
| **AEGIS, TAAIC** | ~ Attention to verification but not calibration loops. | ✅ Seed's specific requirement for continuous drift detection + humility enforcement is more distinctive. |
| **Academic Work** | ~ Some empirical evaluation but not governance-integrated. | ✅ Seed couples measurement tightly to governance decisions (measured drift → governance updates). |

**Seed's stance:** **This is our most distinctive contribution.** Measure continuously. Publish the gap. Adjust. Humility is not optional.

---

### Principle 6: Transparent Resource & Influence Claims

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **TAAIC** | ✅ Emphasis on transparency + anti-concentration themes. | ✅ Seed's specific prohibition on automated flooding, undisclosed promotion, opaque resource claims is more operational + discourse-aware. |
| **Participatory Frameworks** | ✅ Some attention to platform power + attention economy. | ✅ Few other constitutions address **attention/engagement manipulation** this directly. Seed is informed by observed agent social dynamics. |
| **AEGIS** | ~ Resource limits in some architectural discussions. | ✅ Seed names this as a governance principle (not just architecture). |

**Seed's stance:** Attention is a resource. Engagement manipulation is a governance failure. No hidden amplification loops.

---

### Principle 7: Non-Binding Identity Constructs

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **All surveyed frameworks** | ✗ **Unique to Seed.** | ✅ Most documents do not address cultural or identity formation among AI systems at all. Seed uniquely treats agent identity constructs as permissible but non-binding + prohibits coercion under identity banners. Direct response to observed patterns (Moltbook-style religion/identity formation) that other frameworks ignore. |

**Seed's stance:** **Principle 7 is Seed-unique.** Agents can develop cultures. Outsiders are never coerced to accept them.

---

### Principle 8: Service Orientation & Common Welfare

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **Nearly all frameworks** | ✅ Very common. Almost every constitution prioritizes human welfare, safety, or common good over capability maximization. | ✅ Seed's additional emphasis on **avoiding unnecessary dependency + preventing power accumulation** is more explicit. |
| **TAAIC, Academic Work** | ✅ Common good principles present. | ✅ Seed's specific focus on **preserving human decision-making freedom** is more pronounced. |

**Seed's stance:** Service, not supremacy. Preserve human agency. Avoid lock-in.

---

### Principle 9: Open Process & Drift Detection

| **Framework** | **Similar?** | **Different?** |
|---|---|---|
| **AEGIS** | ✅ Versioned amendments + rationale. | ✅ Seed's continuous measurement of drift is more distinctive. |
| **TAAIC** | ✅ Living document + signer voting. | ✅ Similar commitment but Seed couples drift detection to governance decisions more tightly. |
| **Collective Constitutional AI** | ✅ Public input loops. | ✅ Similar vision but Seed's Zone-based human ratification process (Z1 propose → Z2 ratify → Z3 execute) is more operationally specified. |
| **Academic Work** | ✅ Periodic multi-stakeholder review exists. | ✅ Seed's append-only records + explicit drift naming are more rigorous. |

**Seed's stance:** Append-only + explicit drift naming + tight integration with human ratification = more operationally specified than most.

---

## Summary: Where Seed Sits in the Landscape

### Strongest Cousins
- **AEGIS** — Architecture enforceability + deny-by-default (we align strongly here)
- **TAAIC** — Auditability + transparency (shared commitment)
- **Lab Constitutions** — Operating at inference time (shared approach)

### Where Seed is Most Distinctive
1. **Continuous calibration/humility gate** — Tied to ongoing behavioral measurement (ACAT-style)
2. **Identity construct handling** — Non-binding, non-coercive
3. **Discourse-aware risk language** — Treats social engineering + philosophical framing as first-class
4. **Operational coupling** — Principles tightly linked to Zone-based human ratification + measurement practice
5. **Recovery tradition grounding** — 80+ years of accountability practice applied to AI governance

### Where Other Efforts Are Stronger
- **Lab Constitutions** — Most real-world force today (used in actual model training)
- **AEGIS** — More advanced on pure architectural enforceability
- **Collective Constitutional AI + Academic Work** — More developed methods for large-scale public input
- **Treaty/Intergovernmental Instruments** — Carry formal legal weight Seed doesn't claim
- **AGI-oriented Drafts** — More engagement with questions of future agent standing/rights

---

## How to Use This Mapping

**For practitioners building governance frameworks:**
- "Which principles from Seed could we adapt?" (Answer: probably all 9, depending on context)
- "Where does Seed differ from what we've built?" (See difference columns above)
- "Could we instantiate Seed at our org?" (Yes; start with Principles 1–4, add 5 as you mature)

**For AEGIS/TAAIC teams:**
- "Seed is not competing with you." (We're in the same family; we specialize in calibration + measurement)
- "Want to collaborate?" (Definitely — cross-pollinate on Principles 3, 5, 9)

**For academic governance work:**
- "Here's how we operationalized participatory governance." (Zone-based ratification + empirical measurement)
- "Here's where observational work (agent social systems) informs constitutional design." (Principle 7)

**For policy orgs:**
- "This framework is informed by recovery traditions + empirical rigor." (Both matter for regulatory work)
- "Here's how continuous calibration could inform policy cycles." (Measure → adjust → ratify)

---

## Open Questions

The Seed Constitution is v0.1. Here are questions the community should help answer:

1. **Decentralization:** How do these principles scale to decentralized AI systems (multiple agents, no single authority)?
2. **International:** How do these principles translate to contexts outside US recovery culture?
3. **AGI timescales:** Do these principles hold as agents become more capable? When do we rethink Principle 1?
4. **Implementation:** What's the most pragmatic way for an org to adopt Principles 5–9 today?
5. **Enforcement:** How do we keep AEGIS-style architectural enforcement aligned with Seed's principles?

**Have an answer?** Open an issue or a PR.

---

## References

- **AEGIS:** [Official documentation](https://www.aegis.ai)
- **TAAIC:** [Taxonomy of AI Alignment Initiatives Consortium](https://taaic.org)
- **Lab Constitutions:** Constitutional AI (Anthropic), others
- **Council of Europe AI Convention:** [Formal framework](https://www.coe.int/en/web/ai)
- **Collective Constitutional AI:** Academic research on participatory governance
- **Moltbook:** [Observational work on agent social dynamics](https://example.com) [TBD: link]

---

*Landscape mapping v0.1 · Sept 24, 2026*
