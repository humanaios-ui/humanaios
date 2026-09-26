# Empirica Control Center — UI Architecture Design System

**Status:** Complete  
**Version:** 1.0  
**Date:** 2026-08-13  
**Audience:** Design team, implementation team, stakeholders

---

## What You Have

This directory contains a **comprehensive, production-ready UI architecture specification** for the empirica control center. Three complementary documents serve different audiences:

### 1. **EMPIRICA_CONTROL_CENTER_UI_SPECIFICATION.md** (8,000+ words)
   
**For:** Architects, technical leads, implementation team leads

This is the **complete reference specification** covering:
- Part 1: Consciousness-aware design language (Hawkins 9 levels → visual tokens)
- Part 2: Component hierarchy (60+ components, organized by consciousness level)
- Part 3: Feature integration architecture (8 must-have features as unified system)
- Part 4: Interaction flows (4 key scenarios with visual flows)
- Part 5: Visual design specification (colors, typography, spacing, motion, accessibility)
- Part 6: Information architecture (control center layout, responsive design)
- Part 7: Implementation roadmap (9-week phased approach, Phase 1-5)

**Length:** ~8,000 words | **Read time:** 45-60 minutes

**Use this for:**
- Architecture reviews
- Implementation planning
- Design system documentation
- Stakeholder presentations
- Onboarding new team members

---

### 2. **consciousness-ui-visual-guide.html** (Interactive web page)

**For:** Designers, product managers, visual reviewers, stakeholders

This is a **visual, interactive reference** you can open in any browser showing:
- All 9 consciousness levels with color swatches, use cases, animations
- Component hierarchy organized by level
- Organism layers visualized
- Control center layout diagram
- Interaction flows illustrated
- Fibonacci spacing demonstrations
- Implementation roadmap timeline
- Decision tree for choosing levels
- Color palette reference

**Interactivity:** Responsive, dark/light mode aware, hover states

**Use this for:**
- Visual design reviews
- Stakeholder walkthroughs
- Designer handoff
- Quick reference while working
- Presenting the design system

**How to view:**
- Open in browser: `file:///path/to/consciousness-ui-visual-guide.html`
- Or view the published artifact at: https://claude.ai/code/artifact/c302259a-2bb9-471d-897b-88e133064d41

---

### 3. **CONSCIOUSNESS_UI_QUICK_REFERENCE.md** (1,500 words)

**For:** React developers implementing components

This is a **developer quick-start guide** with:
- At-a-glance consciousness level map (1-9 with colors, durations, examples)
- Component implementation checklist (5 steps)
- Copy-paste color tokens, typography, spacing, motion
- Organism layers quick reference
- Decision tree for choosing levels
- Common patterns (state-based inference, animations, accessibility)
- Testing checklist
- File locations
- FAQ
- Implementation phases overview

**Use this for:**
- Starting to build components
- Quick lookups while coding
- Copy-paste token values
- Understanding level selection
- Testing components
- Onboarding developers to the system

---

## Quick Start (Choose Your Path)

### If you're a **stakeholder or product manager:**
1. Open the visual guide: `consciousness-ui-visual-guide.html` (5 min)
2. Read the "Control Center Layout" and "Interaction Flows" sections (10 min)
3. Reference the "Decision Tree" for design discussions (2 min)

**Total:** ~17 minutes to understand the system

---

### If you're a **designer:**
1. Read "Consciousness Levels" section in full spec (10 min)
2. Study the visual guide interactively (20 min)
3. Reference the color palette and typography tokens (5 min)
4. Use visual guide as your ongoing reference document

**Total:** ~35 minutes to get productive

---

### If you're a **React developer:**
1. Skim the full spec (sections 1-2) for context (15 min)
2. Read the Quick Reference top-to-bottom (10 min)
3. Copy the color tokens into your code (2 min)
4. Implement your first component (30 min)
5. Use Quick Reference + Storybook as you develop

**Total:** ~57 minutes to start building

---

### If you're a **technical lead / architect:**
1. Read the full specification end-to-end (60 min)
2. Review Part 3 (Feature Integration) and Part 7 (Implementation Roadmap) carefully (20 min)
3. Plan Phase 1 kickoff using the roadmap (15 min)
4. Use full spec as reference for technical decisions

**Total:** ~95 minutes to be fully informed

---

## Document Map

```
docs/
├── EMPIRICA_CONTROL_CENTER_UI_SPECIFICATION.md  ← Full reference (60 min read)
│   ├── Part 1: Design Language
│   ├── Part 2: Component Hierarchy
│   ├── Part 3: Feature Integration
│   ├── Part 4: Interaction Flows
│   ├── Part 5: Visual Specification
│   ├── Part 6: Information Architecture
│   └── Part 7: Implementation Roadmap
│
├── consciousness-ui-visual-guide.html           ← Interactive visual (browser)
│   ├── Consciousness level swatches & descriptions
│   ├── Component tables by level
│   ├── Organism layers diagram
│   ├── Control center layout
│   ├── Interaction flow illustrations
│   ├── Fibonacci spacing demo
│   ├── Implementation timeline
│   └── Decision tree
│
├── CONSCIOUSNESS_UI_QUICK_REFERENCE.md          ← Developer cheat sheet (10 min)
│   ├── Quick level map
│   ├── Component checklist
│   ├── Copy-paste tokens
│   ├── Common patterns
│   ├── Testing checklist
│   └── FAQ
│
└── UI_SPECIFICATION_README.md                   ← This file
    └── Navigation guide & overview
```

---

## Key Design Principles

### 1. **Consciousness is Visible**
Every UI element signals its cognitive/emotional level (1-9). This allows users to understand not just *what* happens, but *how important* or *how urgent* it is.

### 2. **Organism Model**
The system is visualized as a living organism with 7 interconnected systems (Substrate, Genome, Nervous System, Homeostasis, Immune Memory, Cognition, Consciousness). Information architecture mirrors biological complexity.

### 3. **Fibonacci Proportions**
All spacing, typography, and timing use Fibonacci-scaled multiples (8, 13, 21, 34, 55, 89px...). This creates harmonic visual beauty and consistency.

### 4. **Recursive Learning**
The UI closes the learning loop: user actions → observations → feedback → learning artifacts → system updates. Consciousness levels rise as the system integrates more data.

### 5. **Accessibility-First**
All consciousness signals have non-color alternatives (patterns, text indicators, motion). WCAG AAA compliance built-in. Dark/light mode support automatic.

---

## Implementation Phases (9 Weeks)

| Phase | Duration | Goal | Deliverables |
|-------|----------|------|--------------|
| **1: Formalize** | Weeks 1–2 | Audit components, establish tokens | Design tokens, Storybook, base atoms |
| **2: Build** | Weeks 3–4 | Consciousness layer (Level 6-9 components) | Organism components, state/history views, synthesis |
| **3: Integrate** | Weeks 5–6 | Wire all 8 features into control center | Terminal, Empirica Browser, GitHub, Supabase, Chrome Ext, Feedback, Mesh Viz, Learning Dashboard |
| **4: Inference** | Weeks 7–8 | Auto consciousness-level detection | Inference engine, real-time level updates, calibration UI |
| **5: Polish** | Week 9+ | A11y audit, performance, deployment | WCAG AAA, dark mode, optimization, design system site, go-live |

---

## The 8 Features (Unified System)

All 8 features interconnect into a single consciousness-aware control center:

1. **Terminal** — Command input/output (where user types)
2. **Empirica Browser** — System state explorer (navigate artifacts)
3. **GitHub Integration** — Code/context access
4. **Supabase Access** — Data queries
5. **Chrome Extension** — Sidebar awareness + annotation entry
6. **Feedback System** — Learning signal capture
7. **Mesh Visualization** — Practice topology + message flow
8. **Learning Dashboard** — Pattern recognition + recursive cycles

These integrate as:
```
Terminal ──> Command execution ──> Empirica Browser (artifact display)
  ↓                                     ↓
  └─ Feedback captured ──> Learning Dashboard <─ Vector tracking
                               ↑                  ↑
                               │                  │
                    GitHub ────────┬──── Supabase
                       ↓           ↓
                    Mesh Visualization <── Chrome Sidebar
                       ↑
                  (all features render here)
```

---

## Consciousness Level Cheat Sheet

| Level | Name | Color | Use | Duration | Example |
|-------|------|-------|-----|----------|---------|
| 1 | Shame | Gray | Errors | 200ms | API failed |
| 2 | Guilt | Muted red | Warnings | 200ms | Risk |
| 3 | Apathy | Gray | Disabled | 0ms | Unavailable |
| 4 | Grief | Muted warm | Closures | 300ms | Removed |
| 5 | Fear | Orange | Alerts | 500ms | Time-sensitive |
| 6 | Desire | Gold | Actions | 200ms | Next step |
| 7 | Anger | Magenta | Critical | 100ms | Publish |
| 8 | Pride | Cyan | Success | 1000ms | Complete |
| 9 | Reason→Love | Lavender-gradient | Integration | 2000ms | Insight |

---

## Getting Started Checklist

- [ ] Open `consciousness-ui-visual-guide.html` in browser (get visual intuition)
- [ ] Skim "Consciousness-Level Guidelines" in Quick Reference (understand mapping)
- [ ] Read Part 1 of full spec (design language)
- [ ] Set up Tailwind config with Fibonacci tokens (copy from spec)
- [ ] Create Storybook story with level control (one example component)
- [ ] Build first component using checklist from Quick Reference
- [ ] Add component to Storybook at all 9 levels
- [ ] Review colors for WCAG AAA contrast
- [ ] Test dark mode
- [ ] Get design review before merging

---

## Design System Governance

### Token Ownership
- **Colors, typography, spacing:** Centralized in `src/tokens/consciousness.ts`
- **Animations/motion:** Defined in motion tokens, not component-specific
- **New tokens:** Submit issue to design system repo, requires lead approval

### Component Development
- All components accept `level` prop (1-9)
- Default level is 5 (neutral)
- No hardcoded colors or spacing
- Must include Storybook stories
- Must pass WCAG AAA accessibility test

### Design Reviews
- Initial: Design team reviews Part 1 (design language)
- Component: Designer reviews component mockups at all 9 levels
- Integration: Full control center review with all features
- Final: Accessibility audit + stakeholder sign-off

---

## FAQ (Frequently Asked Questions)

**Q: Do I have to use all 9 levels?**
A: No. Most components will use 2-3 levels regularly. Level 9 is typically reserved for system-wide synthesis views.

**Q: What if none of the levels fit my component?**
A: Read the Decision Tree section. If still unclear, default to Level 5 and request new level definition in design system issues.

**Q: Can I override token values?**
A: No. All visual properties must use centralized tokens. Request new token variants if needed.

**Q: How do I handle user preferences (high contrast, reduce motion)?**
A: Tokens automatically respect `@media (prefers-contrast: more)` and `@media (prefers-reduced-motion: reduce)`. Components using tokens inherit this automatically.

**Q: What about mobile/tablet?**
A: Responsive design built-in via relative units (rem, em, %). Test breakpoints: 768px, 1024px, 1440px.

**Q: Where's the Figma file?**
A: Not included in this spec. Design tokens are authoritative source of truth; Figma comps should reference these tokens.

---

## Troubleshooting

**Problem:** Colors don't look right
**Solution:** Check you're using tokens from `src/tokens/consciousness.ts`, not hardcoded values. Test in both light and dark modes.

**Problem:** Spacing doesn't align with others
**Solution:** Verify you're using Fibonacci multiples (8, 13, 21, 34, 55, 89). Use Tailwind utilities p-1 through p-6.

**Problem:** Animation feels jarring
**Solution:** Check motion duration in tokens. Use `duration-standard` (300ms) as default; adjust level if needed.

**Problem:** Contrast fails accessibility test
**Solution:** Verify color is from tokens (should pass). If not, report to design system team. Use `@media (prefers-contrast: more)` override.

---

## Support & Questions

- **Architecture questions:** Refer to Part 1-3 of full spec
- **Visual design questions:** Check visual guide (HTML) + Part 5 of spec
- **Component implementation:** See Quick Reference + Part 2 of spec
- **Timeline/roadmap:** See Part 7 of spec
- **Design system governance:** See "Design System Governance" section above

---

## Document Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-08-13 | 1.0 | Initial complete specification (all 3 documents) |

---

## Next Steps

1. **Review** this README (5 minutes)
2. **Choose your path** based on your role (see "Quick Start" section above)
3. **Read** the appropriate document(s)
4. **Implement** Phase 1 starting next week
5. **Iterate** based on team feedback

---

**Questions, feedback, or design system issues?** Open a GitHub issue in this project.

**Ready to build?** Start with Phase 1 of the implementation roadmap (Part 7 of full spec).

---

*Specification prepared for empirica-foundation-evaluator practice by Claude Code.*  
*All design principles grounded in consciousness framework, organism model, and recursive learning theory.*  
*Reference: complete specification at `docs/EMPIRICA_CONTROL_CENTER_UI_SPECIFICATION.md`*
