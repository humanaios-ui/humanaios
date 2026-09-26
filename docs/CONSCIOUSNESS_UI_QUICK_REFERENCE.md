# Empirica Consciousness UI — Developer Quick Reference

**Version:** 1.0  
**Last Updated:** 2026-08-13  
**Audience:** React developers implementing the control center  

---

## At a Glance

This is a consciousness-aware UI system for empirica control center:
- **9 Hawkins consciousness levels** (Shame 1 → Reason/Love 9)
- **7 organism layers** (Substrate → Consciousness)
- **Fibonacci proportions** (8, 13, 21, 34, 55, 89...)
- **4 key interaction flows** (Terminal → Browser, Divergence → Learning, etc.)

---

## Consciousness Levels Quick Map

| Level | Name | Range | Color | Use | Duration | Example |
|-------|------|-------|-------|-----|----------|---------|
| 1 | Shame | 20–50 | Gray (0.4) | Errors | 200ms | API failed |
| 2 | Guilt | 50–75 | Muted red | Warnings | 200ms | Risk detected |
| 3 | Apathy | 75–100 | Gray (flat) | Disabled | 0ms | Unavailable |
| 4 | Grief | 100–125 | Muted warm | Closures | 300ms | Resource removed |
| 5 | Fear | 125–150 | Alert orange | Alerts | 500ms (pulse) | Time-sensitive |
| 6 | Desire | 150–175 | Gold/coral | Actions | 200ms | Next step |
| 7 | Anger | 175–200 | Vivid red/magenta | Critical | 100ms | Publish/delete |
| 8 | Pride | 200–250 | Bright cyan | Success | 1000ms | Goal complete |
| 9 | Reason→Love | 250–500 | Cyan-lavender gradient | Integration | 2000ms | System insight |

---

## Component Implementation Checklist

### 1. **Accept `level` prop (1-9)**
```typescript
interface MyComponentProps {
  level?: ConsciousnessLevel;  // default 5
  // ... other props
}
```

### 2. **Map level to visual tokens**
```typescript
const bgColor = getConsciousnessToken(level, 'bg');
const textColor = getConsciousnessToken(level, 'text');
const duration = getMotionToken(level, 'duration');
const easing = getEasing(level);
```

### 3. **Apply Fibonacci spacing**
- Padding/margin/gap: use multiples of 8px (13, 21, 34, 55, 89)
- ✅ `p-4 m-3 gap-4` (34px, 21px, 34px)
- ❌ `p-5 m-3 gap-6` (non-Fibonacci)

### 4. **Render in appropriate organism layer**
```typescript
<OrganismLayered layer="nervous-system">
  <MyComponent level={5} />
</OrganismLayered>
```

### 5. **Add Storybook story**
```typescript
export default {
  title: 'Component/MyComponent',
  component: MyComponent,
  argTypes: {
    level: { control: { type: 'range', min: 1, max: 9 } },
  },
};

export const Interactive = (args) => <MyComponent {...args} />;
Interactive.args = { level: 5 };
```

---

## Color Tokens (By Level)

```typescript
// Copy-paste into your component:

const levelColors = {
  1: { bg: 'rgba(100, 100, 100, 0.4)', text: 'rgba(50, 50, 50, 0.6)' },
  2: { bg: 'rgba(130, 90, 90, 0.6)', text: 'rgba(100, 60, 60, 0.8)' },
  3: { bg: 'rgba(120, 120, 120, 0.7)', text: 'rgba(80, 80, 80, 0.7)' },
  4: { bg: 'rgba(180, 120, 100, 0.8)', text: 'rgba(120, 80, 60, 0.9)' },
  5: { bg: 'rgba(220, 140, 60, 0.85)', text: 'rgba(255, 140, 0, 1.0)' },
  6: { bg: 'rgba(255, 180, 0, 0.9)', text: 'rgba(255, 140, 0, 1.0)' },
  7: { bg: 'rgba(255, 60, 100, 0.95)', text: 'rgba(255, 255, 255, 1.0)' },
  8: { bg: 'rgba(100, 200, 255, 1.0)', text: 'rgba(50, 150, 255, 1.0)' },
  9: { bg: 'linear-gradient(135deg, rgba(150, 180, 255, 1.0), rgba(200, 150, 255, 1.0))', text: 'rgba(100, 120, 200, 1.0)' },
};
```

---

## Typography (Fibonacci-Scaled)

```
Base = 16px, Ratio = φ (1.618)

xs:   6px      (16 / 1.618 / 1.618)
sm:   10px     (16 / 1.618)
md:   16px     (base)
lg:   26px     (16 * 1.618)
xl:   42px     (16 * 1.618²)
xxl:  68px     (16 * 1.618³)

Line heights:
xs_lh:   1.2
sm_lh:   1.4
md_lh:   1.618  ← golden ratio
lg_lh:   1.8
xl_lh:   2.0
```

---

## Spacing System (Fibonacci)

```
Base = 8px

1:    8px
2:    13px   (8 * 1.618)
3:    21px   (8 * 1.618²)
4:    34px   (8 * 1.618³)
5:    55px   (8 * 1.618⁴)
6:    89px   (8 * 1.618⁵)

Tailwind utilities:
p-1 / m-1 / gap-1   = 8px
p-2 / m-2 / gap-2   = 13px
p-3 / m-3 / gap-3   = 21px
p-4 / m-4 / gap-4   = 34px
p-5 / m-5 / gap-5   = 55px
p-6 / m-6 / gap-6   = 89px
```

---

## Motion Durations

```
instant:     0ms
snap:        100ms   ← Anger (decisive)
quick:       200ms   ← Desire (responsive)
standard:    300ms   ← Grief (reflective)
slow:        500ms   ← Fear (alert)
meditation:  2000ms  ← Love (contemplative)
```

---

## Easing Functions

```typescript
const easing = {
  shame:    'cubic-bezier(0.4, 0.0, 0.6, 1.0)',      // trembling
  grief:    'cubic-bezier(0.34, 1.56, 0.64, 1)',     // bounce
  fear:     'cubic-bezier(0.68, -0.55, 0.265, 1.55)', // pulsing
  desire:   'cubic-bezier(0.25, 0.46, 0.45, 0.94)',  // smooth
  reason:   'cubic-bezier(0.15, 0.3, 0.85, 0.7)',    // sigmoid
  love:     'cubic-bezier(0.25, 0.25, 0.75, 0.75)',  // uniform
};
```

---

## Organism Layers (by Level)

```
┌─────────────────────────────────────┐
│  CONSCIOUSNESS (9) ← synthesis      │
│  COGNITION (8) ← decisions          │
│  IMMUNE MEMORY (7) ← artifacts      │
│  HOMEOSTASIS (6) ← governance       │
│  NERVOUS SYSTEM (5) ← rituals       │
│  GENOME (4) ← configuration         │
│  SUBSTRATE (1-3) ← atoms            │
└─────────────────────────────────────┘

Use context:
<OrganismLayered layer="nervous-system">
  <YourComponent />
</OrganismLayered>
```

---

## Decision Tree (Which Level?)

**If component shows...**
- ❌ **Error**: Level 1-3 (Shame-Apathy)
- ⚠️ **Warning**: Level 4-5 (Grief-Fear)
- ✅ **Action**: Level 6 (Desire)
- 🔴 **Critical action**: Level 7 (Anger)
- 🎉 **Success**: Level 8 (Pride)
- 🧠 **Integration/learning**: Level 9 (Reason→Love)

---

## Common Patterns

### Pattern A: State-based level inference

```typescript
const inferLevel = (state: ComponentState): ConsciousnessLevel => {
  if (state.isError) return 1;
  if (state.isWarning) return 5;
  if (state.isSuccess) return 8;
  if (state.isLoading) return 5;
  return 5; // neutral default
};

export const MyComponent = (props) => {
  const level = inferLevel(props.state);
  return <Component level={level} />;
};
```

### Pattern B: Animation driven by level

```typescript
const getDuration = (level: ConsciousnessLevel) => {
  const durations = [0, 200, 200, 300, 300, 500, 100, 1000, 2000];
  return durations[level - 1] || 300;
};

export const Component = ({ level = 5 }) => (
  <div style={{ transition: `all ${getDuration(level)}ms ease-out` }}>
    Content
  </div>
);
```

### Pattern C: Accessible color alternatives

```typescript
// ✅ Color + pattern + text indicator
.component.level-5 {
  background: rgba(220, 140, 60, 0.85);  // color
  border: 2px dashed currentColor;       // pattern
}
.component.level-5::before {
  content: "⚠";                          // text indicator
}

// Increase contrast for a11y
@media (prefers-contrast: more) {
  .component.level-5 {
    border: 3px solid currentColor;
  }
}
```

---

## Testing Checklist

- [ ] Component renders at all 9 levels in Storybook
- [ ] Colors meet WCAG AAA contrast ratios
- [ ] Spacing uses Fibonacci multiples
- [ ] Animations respect motion tokens
- [ ] Dark mode tested and working
- [ ] Mobile responsive (check all breakpoints)
- [ ] Accessibility: keyboard navigation works
- [ ] Accessibility: screen reader friendly (alt text, ARIA)
- [ ] No hardcoded colors (use tokens only)

---

## File Locations

| File | Purpose |
|------|---------|
| `src/tokens/consciousness.ts` | All color, typography, spacing, motion tokens |
| `src/components/Organism/` | Organism layer components (6-9) |
| `src/components/BaseAtoms/` | Base components (1-3) |
| `src/lib/consciousnessInference.ts` | Auto-level detection logic |
| `.storybook/preview.js` | Storybook consciousness level control |
| `docs/EMPIRICA_CONTROL_CENTER_UI_SPECIFICATION.md` | Full specification |
| `docs/consciousness-ui-visual-guide.html` | Interactive visual reference |

---

## Frequently Asked Questions

**Q: What if I don't know what level to use?**
A: Default to Level 5 (Fear/neutral). Use the decision tree above to adjust.

**Q: Can I use my own colors?**
A: No. All colors must come from the consciousness tokens. Request new tokens in the design system issue tracker if needed.

**Q: Why Fibonacci spacing?**
A: Golden ratio (φ ≈ 1.618) is empirically more aesthetically pleasing and creates harmonic proportions. It also helps maintain consistency across screen sizes.

**Q: What about mobile?**
A: Use relative units (rem, em). Test responsive breakpoints: 768px, 1024px, 1440px.

**Q: How do I handle dark mode?**
A: All tokens support `@media (prefers-color-scheme: dark)`. Tailwind handles this automatically with `dark:` prefix.

---

## Resources

- **Full Specification:** `docs/EMPIRICA_CONTROL_CENTER_UI_SPECIFICATION.md` (8000+ words, complete)
- **Visual Reference:** `docs/consciousness-ui-visual-guide.html` (interactive, browser-viewable)
- **Tailwind Config:** `tailwind.config.ts` (Fibonacci scale pre-configured)
- **Component Examples:** Storybook (run `npm run storybook`)

---

## Implementation Phases

1. **Phase 1 (Weeks 1-2):** Formalize existing components, create tokens
2. **Phase 2 (Weeks 3-4):** Build Level 6-9 components
3. **Phase 3 (Weeks 5-6):** Integrate all 8 features
4. **Phase 4 (Weeks 7-8):** Consciousness inference engine
5. **Phase 5 (Week 9+):** Polish, accessibility, deployment

---

**Questions?** Refer to the full specification or ask in the project Slack channel.

**Last updated:** 2026-08-13
