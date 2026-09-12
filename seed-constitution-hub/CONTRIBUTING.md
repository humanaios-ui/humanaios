# Contributing to the Seed Constitution

The Seed Constitution is a living document. Community questions, challenges, and proposals make it better.

---

## How to Contribute

### Option 1: Propose a Governance Decision

See [v0.1/DECISION-LOG.md](v0.1/DECISION-LOG.md) for the process.

1. **Open a GitHub issue** with label `governance-proposal`
   - Describe the decision needed
   - Explain why (grounded in evidence + Principles)
   - Suggest alternatives
   
2. **Carly reviews** (weekly)
   - Requests clarity if needed
   - Decides + logs decision
   - Responses within 1–2 weeks

3. **Community discusses**
   - Thread on the issue
   - Carly reads + considers feedback
   - Final decision is Carly's (Principle 1: Residual Human Authority)

### Option 2: Propose a Change via Pull Request

If you've thought through *exactly* what should change:

1. **Fork the repo**
2. **Create a branch:** `feature/your-proposal-name`
3. **Make changes:**
   - Edit PRINCIPLES.md, LANDSCAPE.md, etc.
   - Include rationale in commit message
   - Link to relevant GitHub issue or Substack discussion
4. **Create a PR with:**
   - Title: "Proposal: [what changes]"
   - Description: Why this change? Grounded in which Principle(s)? Evidence?
   - Link to community inbound that prompted it
5. **Carly reviews:**
   - May request changes
   - Will approve + merge OR defer to next version
   - Merged PRs create DECISION-LOG.md entries

### Option 3: Report an Issue or Bug

- **Typo or clarity issue?** Open issue with label `documentation`.
- **Principle is unclear?** Open issue with label `principle-clarification` + explain what's ambiguous.
- **Found contradictions?** Open issue with label `consistency` + show where.

### Option 4: Start a Discussion

Not a proposal, just want to discuss?

- **Comment on Substack** (The Seed Constitution publication)
- **Open GitHub Discussion** (once available)
- **Post in INTENT-OS forums** with tag `#constitution-discussion`

All discussions are monitored + feed into weekly community synthesis reports.

---

## Governance Principles for Contributors

When proposing changes, ground your proposal in the Principles:

- **Principle 1** (Residual Human Authority) — You can propose anything, but Carly decides. This is intentional.
- **Principle 4** (Evidence Before Authority) — Proposals with data > proposals without. "We should clarify Principle 5 because X orgs reported confusion" > "Principle 5 is confusing."
- **Principle 5** (Calibration) — If you've tried instantiating a Principle at your org and found a gap, that's high-value feedback.
- **Principle 9** (Open Process) — All decisions are logged + visible. You can see why something was accepted or declined.

---

## Code of Conduct

**Respectful discourse. Assume good faith. Evidence-based disagreement.**

- No personal attacks
- Disagreement is welcome; personal attacks are not
- "I think you're wrong because X" is good. "You're stupid" is not.
- If someone violates this, they'll be asked to leave. Once.

---

## v0.1 vs. v0.2 Contributions

**v0.1 is frozen as of Sept 24, 2026.** We're not making changes to it.

**v0.2 opens for PRs starting Nov 1, 2026** (after 4 weeks of community inbound synthesis).

If you want your proposal in v0.2:
- Submit a PR against `v0.2/` directory (not `v0.1/`)
- Or open an issue + wait for synthesis (Carly will incorporate top inbound themes)

---

## Recognition

Contributors who have PRs merged will be:
1. **Named** in the commit message + DECISION-LOG.md (unless you prefer anonymity)
2. **Linked** from README.md ("Contributors to v0.2")
3. **Thanked** in a Substack post ("Here's what the community shaped")

If you want to stay anonymous, say so in the PR description.

---

## Technical Setup

**To fork and develop locally:**

```bash
git clone https://github.com/humanaios/seed-constitution.git
cd seed-constitution
git checkout -b feature/your-proposal-name
# Make your changes
git commit -m "Proposal: [description]"
git push origin feature/your-proposal-name
# Open PR on GitHub
```

**Style guide:**
- Markdown formatting (standard GFM)
- 80-char line width (where possible)
- Hyperlinks to related docs (e.g., link DECISION-LOG.md entries from PRINCIPLES.md)
- No hidden references or shorthand (clarity over cleverness)

---

## Questions?

- **How do I start?** Read [README.md](README.md) + [PRINCIPLES.md](v0.1/PRINCIPLES.md).
- **Not sure if it's a PR or a discussion?** Open an issue first. Carly will guide.
- **Want to propose something big?** Email carly@humanaios.ai before opening a PR. Let's talk it through.

---

## What We're Looking For

**High-priority contributions:**
- [ ] Implementations at your org (case studies, what worked/failed)
- [ ] Comparisons with other frameworks (additions to LANDSCAPE.md)
- [ ] Clarifications to Principles (examples, FAQ)
- [ ] Integration guides (how to instantiate at different org types)
- [ ] Research (does the framework hold? measurements)

**Low-priority (but welcome):**
- [ ] Typo fixes
- [ ] Minor rewording
- [ ] Stylistic preferences

---

## Support

**Help wanted:**

1. **INTENT-OS integration** — We need someone to help design + wire the community forums
2. **Data pipeline** — Script to aggregate + classify weekly feedback (Python or your language)
3. **Translations** — Interested in translating to another language?
4. **Implementations** — Want to help an org instantiate Principles 1–5? Reach out.
5. **Academic partnerships** — Researchers interested in empirically testing the framework?

Contact Carly (carly@humanaios.ai) if you want to help with any of these.

---

*Contributing Guide v0.1 · Sept 24, 2026*
