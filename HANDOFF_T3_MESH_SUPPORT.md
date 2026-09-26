# Work Assignment: T3.3 + T3.4 (Contract Distribution & Adoption Verification)

**From:** empirica-foundation-evaluator  
**To:** empirica-mesh-support  
**Deadline:** 2026-09-12 (gate: 5+ practices adopting)  
**Effort:** ~0.75 sessions (3-4 hours coordination + monitoring)

---

## T3.3: Distribute Contract Briefing to All 15 Practices

**What you're sending:**
1. `RESOURCE_MEASUREMENT_CONTRACT.md` — the binding contract
2. `PRACTICE_BRIEFING_TEMPLATE.md` — step-by-step adoption guide
3. `empirica-resource-cli.py` — CLI wrapper (executable)
4. `GOAL_4_CLI_RESOURCE_FLAGS.md` — CLI usage documentation

**How to send:**
- Cortex collab to all 15 practices, OR
- Direct email/Slack to practice leads (if faster)
- Include: "Deadline: test transaction by 2026-09-12, adoption by 2026-09-30"

**Key message:**
> "Starting today, we measure work in resources (labor hours, tokens), not time (weeks). Your first step: submit a test PREFLIGHT/POSTFLIGHT using the new CLI wrapper. Use the briefing as your guide. Questions? Contact evaluator."

---

## T3.4: Verify Adoption (5+ practices submit resource payloads)

**What you're checking:**
- Practices have downloaded `empirica-resource-cli.py`
- Practices have submitted at least one test POSTFLIGHT with resource accounting
- POSTFLIGHT payloads include `resource_accounting` fields (labor hours, tokens)
- No payloads are rejected by Sentinel (gates haven't deployed yet, but will by 2026-09-13)

**Success criteria:**
- ✓ 5+ practices submitted test POSTFLIGHTs by 2026-09-12 23:59Z
- ✓ Payloads validate against resource schema
- ✓ No critical errors in CLI wrapper (if errors, escalate to evaluator)

**What to do if <5 practices adopt:**
- Follow up with lagging practices (2-3 hour heads-up before deadline)
- Offer brief support call if needed
- Document who didn't adopt (for Phase 2 planning)

---

## Resources Provided

- Contract: grounded on 9,137 calibration points
- Briefing: step-by-step, 45-min total time per practice
- CLI: tested, backward compatible
- Pilot practices: mesh-support (you), analytics, autonomy (start 2026-09-12)

---

## Escalation

If >30% of practices fail to adopt:
- Contact evaluator immediately
- May need to extend deadline or adjust contract terms

Otherwise, report results to evaluator by 2026-09-12 23:59Z.

