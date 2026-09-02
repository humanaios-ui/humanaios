---
doc_id: HAIOS-TEST-009
title: Bio Systems Mapping V1
revision: 1
status: draft
owner: "@carly"
created_date: 2026-09-02
review_due: 2026-12-01
canonical: true
retention: permanent
---
# BIO_SYSTEMS_MAPPING_V1.md

**Status:** DRAFT — research artifact, not registry-touching
**Scope:** Functional component inventory, Western biomedicine vs. Eastern (TCM Zang-Fu) systems
**Purpose:** Feeds Phase 4 (translation into programming framework)

---

## 1. Schema (applied to every component)

Function | Inputs | Outputs | Regulation/feedback | Failure mode | Interdependencies

---

## 2. Strong / Partial Matches (Zang, primary organs)

| Component | Western | Eastern (Zang) | Tier | Note |
|---|---|---|---|---|
| Circulation | Heart, vasculature | Xin (Heart) | Strong | Eastern adds Shen (mind) — scope overhang |
| Respiration | Lungs | Fei (Lung) | Strong | Eastern adds Wei Qi (defense) — scope overhang |
| Digestion | Stomach, pancreas, small intestine | Pi/Wei (Spleen/Stomach) | Strong | Eastern adds hematopoiesis, muscle tone, hemostasis |
| Blood storage | Coagulation factor synthesis, blood volume buffering | Gan (Liver) | Partial | Functionally adjacent, not identical |

## 3. Composite Mappings (one Eastern node = several Western modules)

| Eastern node | Maps onto (Western) | Note |
|---|---|---|
| Shen (Kidney) | Renal, gonadal/HPG axis, skeletal/marrow, aging trajectory | "Root of Yin-Yang for the whole body" — no single Western owner |
| Pi (Spleen) hematopoiesis claim | Bone marrow, coagulation, partly hepatic | Overlaps with Kidney's marrow claim — TCM tolerates redundant ownership; Western assigns single-owner systems |

## 4. Cross-Cutting Regulators (not components — middleware-shaped)

| Eastern concept | Behavior | Closest Western analog |
|---|---|---|
| Gan-Qi (free flow of Qi) | Attaches to every organ's regulation, not owned inputs/outputs | Sympathetic tone + cortisol stress response + smooth muscle tone (distributed, not unified) |
| Wei Qi (defensive Qi) | Surface/skin defense, tied to Lung | Innate immunity, skin barrier |

## 5. Distributed-Function Finding (the big one)

Western **unified systems** that have **no single Eastern counterpart** — instead parceled across multiple Zang:

| Western system | Distributed across (Eastern) |
|---|---|
| Nervous system (CNS/PNS/ANS) | Wu Shen (Five Spirits): Shen–Heart (consciousness), Hun–Liver (emotional/ethereal), Po–Lung (corporeal/reflexive), Yi–Spleen (thought/intellect), Zhi–Kidney (willpower). No coordinating node except loosely Heart-as-"emperor." |
| Endocrine system | No standalone concept. Folded into Kidney (reproductive/growth), Spleen (metabolic), San Jiao (fluid/hormonal passage, loosely) |
| Musculoskeletal system | Spleen (muscle/flesh), Liver (tendons/sinews), Kidney (bone/marrow) |
| Integumentary system | Lung (skin/body hair via Wei Qi), Kidney (head hair via Jing), Heart (complexion) |
| Reproductive system | Kidney (Jing/essence) — already flagged under Kidney composite |

**Architecture implication:** these aren't matching failures — they're a structural difference in how the two systems partition responsibility. Western = single-owner modules. Eastern = shared/broadcast responsibility across multiple nodes. A framework modeled on Western anatomy wants strict interfaces; one modeled on TCM wants a pub/sub or shared-state model.

## 6. Six Fu (Bowels) — paired, mostly follow their Zang

| Fu | Paired Zang | Western match | Orphan element |
|---|---|---|---|
| Small intestine | Heart | Nutrient absorption — good match | Heart-pairing (no Western diagnostic link) |
| Large intestine | Lung | Elimination — good match | Lung-pairing (no Western diagnostic link) |
| Gallbladder | Liver | Bile storage — good match | Governs "decisiveness/courage" (psychological trait, orphan) |
| Bladder | Kidney | Water storage/excretion — good match | — |
| Stomach | Spleen | Covered above | — |
| San Jiao (Triple Burner) | — (no Zang pair) | **No anatomical correlate at all** | Full orphan — see §7 |

## 7. Categorical Orphans (not organs — substances, networks, or meta-frameworks)

| Concept | Type | Western status |
|---|---|---|
| San Jiao (Triple Burner) | Three body-cavity functional zones governing overall fluid passage | No confirmed correlate; loosely echoes whole-body fluid-compartment coordination |
| Jing-Luo (meridians/channels) | Connectivity network, not a component | Unconfirmed anatomical correlate (fascial plane / peripheral nerve theories exist, contested) — this is a **topology**, not a node |
| Qi | Unified energetic/functional substance circulating system-wide | No single-concept Western analog — Western splits this into many discrete things (ATP/metabolic energy, nerve signaling, autonomic tone) |
| Jinye (body fluids) | Unified fluid category (sweat, saliva, synovial, etc. as Yin manifestations) | Western treats each fluid as a separate discrete system, not one category |
| Wu Xing (Five Element correspondence) | Meta-framework organizing all Zang-Fu into a fixed 5-node graph with generative (Sheng) and control (Ke) cycles | No equivalent — Western feedback loops are modeled ad hoc per pathway, not under one universal topology |

---

## 8. Key Findings for Phase 4

1. **Three different code shapes required, not one:** clean interface (Heart/Lung), composite (Kidney/Spleen), cross-cutting middleware (Liver-Qi, Wei Qi).
2. **Ownership model differs by tradition:** Western = single-owner modules; Eastern = shared/redundant ownership, esp. for nervous-system-equivalent and hematopoiesis.
3. **The meridian network (Jing-Luo) isn't a module — it's the graph itself.** Any framework needs a connectivity layer separate from the component list.
4. **Wu Xing (Five Element) cycle is effectively a pre-built topology** — 5 nodes, generative cycle, control cycle. This is the most directly reusable piece for Phase 4: it's already close to pseudocode for inter-module message passing / regulation calls.
5. **Qi and Jinye are the hardest translation targets** — categorical substances with no single Western unit. They'll likely need to be modeled as a resource/state layer threaded through every component rather than as components themselves.

---
Draft — Phase 1/2 inventory complete for primary Zang-Fu, Six Fu, and categorical orphans.
