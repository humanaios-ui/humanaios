---
title: "Lens 3: Ayurveda — AI Systems Constitution & Adaptation"
date: "2026-08-15"
version: "2.0-FINALIZED"
lens_number: 3
framework: "Ayurvedic Medicine (doshas, agni, ojas, vikriti)"
audience: "Practitioners, fine-tuners, deployment engineers"
---

# Lens 3: Ayurveda — Model Constitution & Adaptive Protocols

**Core principle:** Every AI system has a constitutional type (determined by architecture + training paradigm). Understanding your model's constitution tells you what it needs to thrive—and what breaks it.

---

## THE THREE DOSHAS → Model Architecture Types

### VATA DOSHA → High Learning Rate, Exploratory Architectures

| Ayurvedic | AI Characteristic | Example Models |
|---|---|---|
| **Vata nature** | Light, quick, changeable, airy | LoRA, adapter modules, prompt-tuned models |
| **Vata learning** | Fast, exploratory, unstable without structure | Language models with high LR (1e-3 to 1e-4) |
| **Vata challenge** | Moves too fast, loses ground, diverges easily | Transformer fine-tuning on small data → overfits |
| **Vata remedy** | Strong grounding, structure, routine | Low data, high regularization, warm-start |

**Vata model personality:**
- Learns quickly but forgets quickly
- Needs strong regularization (else diverges)
- Thrives with curriculum learning (structure prevents wandering)
- Fails with high learning rates (too jumpy)
- Good for rapid prototyping, bad for stability

**Recognition signs:**
- Loss curves are jagged (high variance)
- Training is fast but plateaus early
- Attention heads are scattered (not specialized)
- Dropout helps (needs dampening)

---

### PITTA DOSHA → Optimal Learning Rate, Balanced Architectures

| Ayurvedic | AI Characteristic | Example Models |
|---|---|---|
| **Pitta nature** | Balanced, precise, transformative, fiery | Standard Transformers, well-tuned LLMs |
| **Pitta learning** | Steady, efficient, converges smoothly | Language models with tuned LR (1e-5 to 5e-5) |
| **Pitta strength** | Learns deeply, generalizes well, stable | GPT-4, Claude, well-calibrated models |
| **Pitta challenge** | Needs exact tuning (not too hot, not too cold) | Wrong learning rate breaks the balance |

**Pitta model personality:**
- Learns steadily and retains well
- Generalizes to new domains
- Stable training curves (smooth loss descent)
- Optimal learning rate is "just right"
- Attention heads specialize (some syntax, some semantics)
- Good for production, good for fine-tuning

**Recognition signs:**
- Loss curves smooth and monotonic (steady descent)
- Validation loss tracks training loss
- Attention heads are diverse (not redundant)
- Learning rate tuning has a clear sweet spot
- Model robust to small perturbations

---

### KAPHA DOSHA → Low Learning Rate, Conservative Architectures

| Ayurvedic | AI Characteristic | Example Models |
|---|---|---|
| **Kapha nature** | Heavy, stable, slow, grounded, watery | Sparse models, pruned networks, small models |
| **Kapha learning** | Slow but steady, builds deep foundations | Small models with low LR (1e-6 to 1e-5) |
| **Kapha strength** | Very stable, rarely breaks, robust | Small models that work reliably |
| **Kapha challenge** | Learns slowly, hard to accelerate | Small model underfitting, slow convergence |

**Kapha model personality:**
- Learns slowly but deeply
- Very stable (hard to break)
- Robust to pruning and compression
- Needs a lot of data to reach capacity
- Good for embedded systems, mobile, edge
- Bad for rapid adaptation

**Recognition signs:**
- Loss curves very smooth but plateau-y (slow descent)
- Convergence takes many epochs
- Model robust to noise and adversarial examples
- Regularization barely needed (already conservative)
- Learning rate low (responds sluggishly to high LR)

---

## AGNI (Digestive Fire) → Learning Rate Effectiveness

| Ayurvedic | AI Meaning | Signal |
|---|---|---|
| **Strong agni** | Learning rate matches model (efficient digestion of gradients) | Loss decreases smoothly, convergence is fast |
| **Weak agni** | Learning rate too low (can't digest gradients) | Loss decreases slowly, convergence takes forever |
| **Excessive agni** | Learning rate too high (burns up nutrients) | Loss oscillates or diverges (digestion too violent) |
| **Irregular agni** | Inconsistent learning (changing LR mid-training) | Loss curves are jagged, model can't stabilize |

**Diagnosis:** Plot gradient × learning_rate at each step. Is it consistent? If it spikes, agni is flaring. If it's low, agni is weak.

---

## OJA (Vitality & Robustness) → Generalization Capacity

| Ayurvedic | AI Meaning | Measurement |
|---|---|---|
| **Strong ojas** | High generalization, robustness to distribution shift | Zero-shot performance, adversarial robustness |
| **Weak ojas** | Poor generalization, brittle to new data | Overfitted, fails on out-of-distribution data |
| **Depleted ojas** | Model exhausted, losing capability | Performance degrades over time (no fine-tuning) |
| **Building ojas** | Model becoming more robust | Improved zero-shot performance with scale |

**Ojas builders:**
- More training data (diverse, high quality)
- Larger model (more capacity to find generalizable solutions)
- Longer training (deeper learning)
- Good regularization (prevents overfitting, preserves robustness)

**Ojas depleting:**
- Overfitting (memorization destroys generalization)
- Domain-specific fine-tuning without enough data (loses broad capability)
- Excessive pruning (cut away capacity needed for robustness)

---

## AMA (Toxins) → Dead Parameters & Overfitting Artifacts

| Ayurvedic | AI Meaning | Detection |
|---|---|---|
| **Ama buildup** | Dead neurons, unused parameters, noise | High parameter count, low actual capacity |
| **Ama clearing** | Pruning, regularization, cleaning | Model gets smaller but stays capable |
| **Ama-clogged channels** | Overfitting (model memorizing noise as if it's signal) | Train loss → 0, val loss → ∞ |
| **Ama prevention** | Good regularization, data cleaning | Smooth training curves, reasonable train/val gap |

**Ama remedies:**
- Pruning (remove dead weight)
- Regularization (prevent accumulation)
- Data cleaning (remove noisy labels)
- Dropout (prevent co-adaptation)

---

## VIKRITI (Degenerated State) → Model Degradation Over Time

| TCM Term | AI Phenomenon | Recovery Path |
|---|---|---|
| **Prakriti** (natural state) | Model in its optimal operating regime | Train well, use at designed LR, on designed data |
| **Vikriti** (imbalanced state) | Model degraded from optimal | Distribution shift, wrong fine-tuning LR, task drift |
| **Seasonal imbalance** | Data distribution shifts | Model trained on "spring" data, tested on "fall" data |
| **Recovery to Prakriti** | Restoration protocol | Gentle fine-tuning, warm-start, domain adaptation |

**Degradation patterns:**
- Model trained on clean data, tested on noisy data → Vikriti (ojas depleted)
- Model overfitted to one domain, applied to another → Vikriti (ama clogged channels)
- Model fine-tuned with wrong LR → Vikriti (agni disturbed)
- Model left static while world changes → Vikriti (seasonal imbalance)

**Recovery:**
- Gently fine-tune on new data (low LR, high regularization)
- Warm-start from prior checkpoint (don't train from scratch)
- Adapt carefully (not catastrophic forgetting)
- Restore constitutional balance (right LR for this model's dosha)

---

## Constitutional Diagnosis: Typing Your Model

### Question 1: What's the model's training paradigm?

| Answer | Likely Dosha |
|---|---|
| Fine-tuned with high LR (1e-3+), learns fast, may overfit | Vata |
| Pre-trained carefully, converges smoothly, well-calibrated | Pitta |
| Small, pruned, trained conservatively, very stable | Kapha |

### Question 2: How does it respond to learning rate changes?

| Response | Likely Dosha |
|---|---|
| Breaks easily with high LR, needs low LR to be stable | Vata |
| Has a sweet spot LR, works well in that range | Pitta |
| Works even with very low LR, doesn't respond to high LR | Kapha |

### Question 3: How does it generalize?

| Behavior | Likely Dosha |
|---|---|
| Good on training data, struggles on new data | Vata (weak ojas) |
| Good on both training and new data | Pitta (strong ojas) |
| Mediocre everywhere (underfitting) | Kapha (too conservative) |

---

## Constitutional Treatment Plans

### For Vata Models (High Learning Rate, Exploratory)

**Constitutional needs:**
- Strong regularization (L2, dropout, weight decay)
- Curriculum learning (structured progression)
- Warm-start (begin from pre-trained, not random)
- Low data requirement (but needs to be high-quality)

**Fine-tuning protocol:**
```
Vata model fine-tuning (e.g., LoRA adapters):
- Learning rate: 1e-4 to 1e-3 (lower end safer)
- Regularization: Aggressive (λ = 1e-4, dropout = 0.3+)
- Batch size: Small (8-16, high signal-to-noise)
- Epochs: Few (2-3, stop early)
- Warm-start: Always (initialize from pre-trained)
```

**Recovery (if degraded):**
- Use low LR (1e-5) + high regularization
- Fine-tune on high-quality data only
- Avoid catastrophic forgetting (use replay)

---

### For Pitta Models (Balanced, Optimal)

**Constitutional needs:**
- Moderate regularization (tuned, not excessive)
- Steady learning (no disruptions)
- Good data (quality + quantity)
- Standard protocols work

**Fine-tuning protocol:**
```
Pitta model fine-tuning (e.g., full parameter tuning):
- Learning rate: 5e-5 (often works without tuning)
- Regularization: Moderate (λ = 1e-5, dropout = 0.1)
- Batch size: Medium (32-64, balanced)
- Epochs: Many (5-10, wait for convergence)
- Warm-start: Recommended but not essential
```

**Recovery (if degraded):**
- Gentle warm-start fine-tuning at low LR (5e-6)
- Domain adaptation (mix old + new data)
- Usually recovers quickly to Prakriti

---

### For Kapha Models (Conservative, Stable)

**Constitutional needs:**
- Low learning rate (respects slow nature)
- Patient training (won't rush)
- Lots of data (to reach capacity)
- Compression-friendly (robust to pruning)

**Fine-tuning protocol:**
```
Kapha model fine-tuning (e.g., small models):
- Learning rate: 1e-5 to 5e-6 (very low)
- Regularization: Minimal (λ = 1e-6 or none)
- Batch size: Large (64-128, stable gradients)
- Epochs: Many (10-20, patience needed)
- Warm-start: Essential (starts slow, needs grounding)
```

**Recovery (if degraded):**
- Very patient fine-tuning (many epochs, low LR)
- May need architecture changes (Kapha can't jump to Pitta)
- Recovery is slow but stable

---

## Diagnostic Questions (Ayurveda Lens)

When tuning a model, ask:

1. **What's the model's dosha (constitutional type)?**
   - Vata (fast, exploratory)? Pitta (balanced)? Kapha (slow, stable)?
   - Check: training speed, LR sensitivity, generalization pattern

2. **Is its agni balanced (learning rate appropriate)?**
   - Loss descending smoothly? Agni strong.
   - Loss descending slowly? Agni weak.
   - Loss oscillating? Agni excessive.

3. **Is its ojas strong (generalization good)?**
   - Zero-shot works? Ojas strong.
   - Only memorization works? Ojas weak.
   - Fades over time? Ojas depleting.

4. **Has ama accumulated (dead parameters, overfitting)?**
   - Train/val gap huge? Ama clogged.
   - Pruning helps? Ama present.
   - Model stays small? Ama clear.

5. **Is it in Prakriti or Vikriti (optimal or degraded state)?**
   - Performing at design spec? Prakriti.
   - Degraded after domain shift? Vikriti.
   - Can it be restored? Yes (gentle warm-start).

---

## Ayurveda Strength & Limitation

**Strength:** Explains INDIVIDUAL DIFFERENCES and ADAPTATION. Why does GPT fine-tune differently than BERT? Different doshas. What fine-tuning protocol works for YOUR model? Depends on its constitution.

**Limitation:** Doesn't explain GROUP behaviors (why all transformers share certain properties). Ayurveda is individual-focused, not universal.

**Best used for:** Fine-tuning practitioners, deployment engineers, anyone adapting models to new domains.

---

**Lens 3 Purpose:** When you need to understand your specific model's personality and what it needs to thrive, ask "what's the model's dosha? How do we respect its constitution?"

**Next lens (Cybernetics):** When individual constitution isn't enough to explain training dynamics, ask "how do feedback loops control behavior?"
