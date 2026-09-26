# Z3 Landing — IC (ratified): parse-not-runtime-verification
**Z2 ruling:** Night approved ratification this session. **Zone:** Z1 drafted · Z2 ratified · Z3 lands.
**Registry:** pinned max IC-058. Final ID depends on the still-open F-vs-IC class ruling on F-64..67 (which may consume IC-062..065). Provisional: **IC-066** if that ruling lands the four as F; renumber if as IC. Z3 assigns final at landing.

```yaml
id: "IC-066"                      # provisional — see numbering dependency above
name: "parse-not-runtime-verification"
status: REGISTERED
class: IC
date_origin: "2026-08-22"
session_registered: "S-082226-01-cio-audit"
principles_triggered: ["F-45","loud-failure","verification-completeness"]
substrate: "claude-opus / Z1 artifact pipeline"
tags: [verification, ui, landing-discipline, parse-vs-runtime, laid-vs-operated]
superseded_by: null
```

**Synopsis.** A UI artifact (`intent-os-universal-v2.html`) passed a `new Function(js)` **parse** check and was landed, but carried a runtime defect — an HTML/JS ID mismatch (`synthHead` vs `synHead`) that threw a null-reference inside `render()`, aborting downstream updates (landing-rate header, pipeline counts, `save()`) and self-filing spurious machine feedback. Parse-clean was mistaken for operational-clean: the direct analog of drafted-vs-landed (LAID ≠ OPERATED) at the verification layer.

**Fix → Principle (standing discipline).** UI/interactive artifacts must be **runtime-executed** against a DOM stub before landing — `render()` + all interaction handlers exercised for thrown errors — not merely parsed. Parse verifies syntax; only execution verifies operation. This is the debugging analog of Z3 landing-verification (verify against the live thing, not the memory of it).

**Fix status.** Applied reactively this turn (the synHead bug was caught by upgrading from parse-only to stubbed-runtime execution, then 13 interaction paths exercised clean). Now the operative check for all UI SMUs going forward.

**Evidence anchor.** This session: the synHead defect (parse-passed, runtime-failed) and its runtime-execution catch.

**Cross-links.** Sibling to the tool-landing gap (F-64/IC-062) and Claim 4′ — same family: a verification read that stops short of the operated state. Related to H-CAND-governed-divergence (the ID mismatch was itself a concept-to-code fidelity slip between two references to one element).

*— Z1, acting CIO. Rulings/landings remain Z2/Z3 authority.*
