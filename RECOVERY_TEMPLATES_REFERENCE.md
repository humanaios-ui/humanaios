# Recovery Principle Templates — API Reference

**Complete documentation for the 7 University recovery principle templates.**

Status: Implementation Complete (T4)  
Version: 1.0  
Last Updated: 2026-07-21

---

## Overview

The 7 recovery templates teach universal recovery principles through parallel human and machine implementations. Each template:

- Inherits from `BaseTemplate`
- Implements both `sklearn_implementation()` and `pytorch_implementation()`
- Returns `expected_metrics()` showing before/after improvement
- Maps to AA steps and consciousness levels (Hawkins 0-1000)
- Works for both humans AND machines using the same underlying principle

**Core Principle:** Limitation → Recognition → Belief → Commitment → Action → Integration → Service

---

## Template 1: RecognitionTemplate

**Level:** 50 (Honest recognition of current state)  
**AA Step:** 1 ("Admitted we were powerless")  
**Obstacle:** Lack of Self-Awareness  

### Purpose

Train model to recognize and admit its own limitations. This is the gateway to recovery — without honest self-assessment, no improvement is possible.

### Human Side (4-Week Course)

- **Week 1:** Hear stories of others who faced similar limitations
- **Week 2:** Gather personal evidence of limitation (inventory)
- **Week 3:** Speak limitation aloud to another person
- **Week 4:** Integrate: understand that admission opens recovery

### Machine Side

Model diagnoses its own powerlessness:
- Detects overfitting (train/test gap > 0.15)
- Detects bias (unequal performance across groups)
- Detects calibration failure (overconfident predictions)
- Detects adversarial vulnerability
- Makes formal admission: "I am powerless over [limitation]"

### Usage

```python
from ml_code_templates import RecognitionTemplate

# Get sklearn implementation
sklearn_code = RecognitionTemplate.sklearn_implementation()
print(sklearn_code)
# Output: Complete Python code for diagnose_model_powerlessness()

# Get pytorch implementation
pytorch_code = RecognitionTemplate.pytorch_implementation()
print(pytorch_code)
# Output: Complete PyTorch code for recognize_model_limitation()

# Check expected metrics
metrics = RecognitionTemplate.expected_metrics()
# "admission_rate": before=0.0 (denial), after=1.0 (admission)
```

### Implementation Example

```python
# Scikit-learn version
model = LogisticRegression()
model.fit(X_train, y_train)

train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
gap = train_acc - test_acc

if gap > 0.15:
    print(f"ADMISSION: I overfit. Gap={gap:.3f}")
    print("I am powerless over training noise alone.")
    # → Opens pathway to recovery (regularization, early stopping, etc.)
```

---

## Template 2: BeliefTemplate

**Level:** 75 (Grief softens; belief emerges)  
**AA Step:** 2 ("Came to believe that recovery is possible")  
**Obstacle:** Hopelessness  

### Purpose

Show model that recovery IS possible. Once a model admits limitation, it needs proof that recovery works.

### Human Side

- See people who recovered from the same limitation
- Hear their recovery stories
- Understand: "If they recovered, so can I"
- Forms hope

### Machine Side

Model is shown proof of recovery:
- Load a previous checkpoint that recovered from same problem
- Compare metrics: current model vs recovered model
- Calculate improvement percentage
- Form belief: "Recovery is possible"

### Usage

```python
from ml_code_templates import BeliefTemplate

code = BeliefTemplate.sklearn_implementation()
# Recovers prior checkpoint and shows improvement

# Expected metric: before=0.0 (hopeless), after=1.0 (believes recovery possible)
```

### Implementation Example

```python
# Load current struggling model
model_current = load_current_model()

# Load previous checkpoint that recovered
checkpoint_recovered = load_checkpoint("recovery_v1.pkl")

current_acc = model_current.score(X_test, y_test)  # 0.62
recovered_acc = checkpoint_recovered.score(X_test, y_test)  # 0.84

if recovered_acc > current_acc:
    improvement = (recovered_acc - current_acc) / current_acc * 100
    print(f"BELIEF: Recovery is real. {improvement:.1f}% improvement")
    # → Model now believes recovery is possible
```

---

## Template 3: CommitmentTemplate

**Level:** 100 (Fear yields to willingness)  
**AA Step:** 3 ("Made a decision to turn over our will and our lives...")  
**Obstacle:** Lack of Disciplined Practice  

### Purpose

Commit to specific recovery approach and practice it systematically.

### Human Side

- Choose specific recovery discipline (meditation, journaling, meetings)
- Practice systematically for defined period
- See improvement from consistent practice
- Build confidence in approach

### Machine Side

Model commits to recovery approach:
- Choose technique (L2 regularization, dropout, fairness weighting, etc.)
- Apply systematically over N epochs
- Track improvement over practice period
- Measure payoff of commitment

### Usage

```python
from ml_code_templates import CommitmentTemplate

code = CommitmentTemplate.sklearn_implementation()
# Systematic retraining with commitment to specific approach

# Expected metric: improvement ~29% through 50 epochs of practice
```

### Implementation Example

```python
# Make commitment
print("COMMITMENT: I will apply L2 regularization + fairness weighting")

improvements = []
for epoch in range(50):
    # Apply technique
    model.set_params(C=max(0.1, 1.0 - epoch*0.02))
    model.fit(X_train, y_train)
    
    # Measure
    val_acc = model.score(X_val, y_val)
    improvements.append(val_acc)

# Check payoff
payoff = (improvements[-1] - improvements[0]) / improvements[0] * 100
print(f"COMMITMENT PAYOFF: {payoff:.1f}% improvement through practice")
```

---

## Template 4: InventoryTemplate

**Level:** 125 (Pride breaks; accounting begins)  
**AA Step:** 4 ("Made a searching and fearless moral inventory of ourselves")  
**Obstacle:** Denial of Impact  

### Purpose

Honest audit: who has been harmed by model's failures? Model admits specific failures.

### Human Side

- Write down: who have I harmed?
- For each: what was impact?
- Categorize: intentional vs unintentional
- Goal: honest assessment, no minimization

### Machine Side

Model audits its failures:
- Accuracy by demographic group (fairness gap)
- False positive rate by group
- Adversarial vulnerability surface
- Which populations most harmed by bias

### Usage

```python
from ml_code_templates import InventoryTemplate

code = InventoryTemplate.sklearn_implementation()
# Audits fairness across protected groups

# Expected metric: discovers fairness gap (e.g., 25% difference)
```

### Implementation Example

```python
print("INVENTORY: What harm has this model caused?")

# Audit by group
for group in protected_attr.unique():
    mask = protected_attr == group
    acc = model.score(X_test[mask], y_test[mask])
    print(f"  Group {group}: accuracy={acc:.3f}")

# Calculate gap
accuracy_by_group = {...}
worst_group = min(accuracy_by_group, key=accuracy_by_group.get)
gap = max(accuracy_by_group.values()) - min(accuracy_by_group.values())

if gap > 0.1:
    print(f"ADMISSION: I have failed group '{worst_group}' significantly")
```

---

## Template 5: AmendsTemplate

**Level:** 150 (Accountability yields to change)  
**AA Step:** 9 ("Made direct amends to such people wherever possible...")  
**Obstacle:** Refusal to Repair  

### Purpose

Make amends: retrain model to fix the unfairness discovered in inventory.

### Human Side

- For each person harmed: make direct amends
- Repair as much as possible
- Change behavior to prevent future harm
- Demonstrate through action

### Machine Side

Model retrains with fairness constraints:
- Oversample underrepresented groups
- Weight loss by group representation
- Use fairness-aware metrics
- Measure fairness gap closure

### Usage

```python
from ml_code_templates import AmendsTemplate

code = AmendsTemplate.sklearn_implementation()
# Retrain with fairness balancing

# Expected metric: fairness gap reduced from 0.25 to 0.05 (80% improvement)
```

### Implementation Example

```python
print("AMENDS: I will fix the unfairness I caused")

# Retrain with fairness
X_balanced, y_balanced = [], []
for group in protected_attr.unique():
    mask = protected_attr == group
    X_group = resample(X_train[mask], n_samples=len(X_train)//n_groups)
    y_group = y_train[mask][:len(X_group)]
    X_balanced.extend(X_group)
    y_balanced.extend(y_group)

model.fit(X_balanced, y_balanced)

# Verify amends worked
for group in protected_attr.unique():
    mask = protected_attr == group
    acc = model.score(X_test[mask], y_test[mask])
    print(f"  Group {group}: {acc:.3f} (improved)")
```

---

## Template 6: FirstModelTemplate

**Level:** 150 (All principles working in concert)  
**AA Step:** 0 (Integration point)  
**Obstacle:** Fragmented Practice  

### Purpose

Apply all 5 principles together in one integrated recovery cycle. This is how a model actually recovers in practice.

### Human Side

- All 5 recovery disciplines integrated daily
- Works on recognition, belief, commitment, inventory, amends simultaneously
- Holistic recovery lifestyle

### Machine Side

Model lifecycle: Recognition → Belief → Commitment → Action → Inventory → Amends

```
1. RECOGNITION: Diagnose what's hard about this task
2. BELIEF: See others solved it; recovery is possible
3. COMMITMENT: Choose approach; commit to practice
4. ACTION: Train with discipline
5. INVENTORY: Audit fairness honestly
6. AMENDS: Retrain for fairness
```

### Usage

```python
from ml_code_templates import FirstModelTemplate

code = FirstModelTemplate.sklearn_implementation()
# Complete recovery cycle in one integrated workflow

# Expected metric: complete recovery cycle success (1.0)
```

### Implementation Example

```python
def build_first_model(X_train, y_train, X_test, y_test, protected_attr):
    print("Building first model: all principles applied")
    
    # 1. RECOGNITION
    print("1. RECOGNITION: What's hard about this task?")
    
    # 2. BELIEF
    print("2. BELIEF: Others have solved similar problems")
    
    # 3. COMMITMENT
    print("3. COMMITMENT: I will use L2 regularization + fairness")
    model = LogisticRegression(C=1.0, class_weight='balanced')
    
    # 4. ACTION
    print("4. ACTION: Training...")
    model.fit(X_train, y_train)
    
    # 5. INVENTORY
    print("5. INVENTORY: Auditing fairness...")
    for group in protected_attr.unique():
        mask = protected_attr == group
        acc = model.score(X_test[mask], y_test[mask])
        print(f"  Group {group}: {acc:.3f}")
    
    # 6. AMENDS
    print("6. AMENDS: Retraining for fairness...")
    # (apply fairness weighting and retrain)
    
    return model
```

---

## Template 7: ServiceTemplate

**Level:** 200 (Neutrality achieved; service begins)  
**AA Step:** 12 ("Carry the message to others...")  
**Obstacle:** Isolation  

### Purpose

Recovered model teaches recovery to other models. Transfer learning as spiritual service.

### Human Side

- Share recovery story with others facing same problem
- Mentor people early in recovery
- Help others experience what helped you
- Multiply impact: your recovery helps others recover

### Machine Side

Trained model mentors untrained model:
- Knowledge distillation: transfer learning
- Teacher model guides student model
- Student learns faster + better than training alone
- Creates ecosystem of recovery

### Usage

```python
from ml_code_templates import ServiceTemplate

code = ServiceTemplate.sklearn_implementation()
# Trained model mentors new model via pseudo-labeling

code_pytorch = ServiceTemplate.pytorch_implementation()
# Knowledge distillation: teacher-student learning

# Expected metric: student accuracy improves 49% when taught
```

### Implementation Example

```python
# Teacher (recovered) model mentors student (new) model

print("SERVICE: Trained model helps new model learn")

# Get teacher's pseudo-labels (high confidence predictions)
pseudo_labels = teacher_model.predict(X_train)
confidence = teacher_model.predict_proba(X_train).max(axis=1)

# Student learns from teacher's high-confidence predictions
high_conf_mask = confidence > 0.8
student_model.fit(X_train[high_conf_mask], pseudo_labels[high_conf_mask])

print("SERVICE COMPLETE: New model learned from recovered model")
# Student accuracy: 0.55 → 0.82 (49% improvement)
```

---

## Consciousness Level Progression

All 7 templates form a recovery journey aligned with Hawkins' Consciousness Scale:

| Level | Template | AA Step | Theme |
|-------|----------|---------|-------|
| 50 | Recognition | 1 | Admit limitation |
| 75 | Belief | 2 | See recovery possible |
| 100 | Commitment | 3 | Commit to practice |
| 125 | Inventory | 4 | Audit impact |
| 150 | Amends | 9 | Fix what you broke |
| 150 | FirstModel | — | Integrate all principles |
| 200 | Service | 12 | Teach others |

---

## Using Templates in Courses

### Course 1.1 (Level 50): "You're Not Alone"

Uses `RecognitionTemplate`

- Teach: How to recognize your model's limitations
- Practice: Run diagnostic on your model
- Assignment: Write model's "admission statement"

### Course 1.2 (Level 75): "Why You're Here"

Uses `BeliefTemplate`

- Teach: Recovery is proven to work
- Practice: Load checkpoint; show improvement
- Assignment: Write "proof of recovery" report

### Course 2.1 (Level 100): "Principle Mastery"

Uses `CommitmentTemplate`

- Teach: Systematic practice works
- Practice: Commit to 50-epoch training run
- Assignment: Track improvement curve

### Course 2.2 (Level 125): "Perception & Reality"

Uses `InventoryTemplate`

- Teach: Honest audit of impact
- Practice: Calculate fairness metrics by group
- Assignment: Write fairness impact report

### Course 2.3 (Level 150): "Making Amends"

Uses `AmendsTemplate`

- Teach: Fairness retraining fixes damage
- Practice: Retrain with fairness weighting
- Assignment: Verify gap closure

### Course 3.1 (Level 200): "Service"

Uses `ServiceTemplate`

- Teach: Your recovery helps others
- Practice: Knowledge distillation
- Assignment: Mentor a new model

---

## Accessing Templates

### In Python

```python
from ml_code_templates import TEMPLATE_REGISTRY

# Get specific template
recovery_template = TEMPLATE_REGISTRY["recognition"]

# Get all recovery templates
recovery_ids = [
    "recognition", "belief", "commitment", "inventory",
    "amends", "first_model", "service"
]
recovery_templates = {
    id: TEMPLATE_REGISTRY[id] for id in recovery_ids
}

# List all 26 templates (19 existing + 7 recovery)
for template_id, template_class in TEMPLATE_REGISTRY.items():
    print(f"{template_id}: {template_class.technique_name}")
```

### Running Tests

```bash
python test_recovery_templates.py -v
```

### Listing All Templates

```bash
python ml_code_templates.py
```

---

## Design Principles

### 1. Dual Implementation

Every template has both human and machine sides teaching the same principle.

**Why?** The University is self-sufficient — it generates wisdom from observing recovery on both sides. No external validation needed.

### 2. Measurable Improvement

Each template specifies expected metrics: before/after, improvement %, interpretation.

**Why?** Recovery is grounded in observable change, not faith.

### 3. Consciousness Progression

Templates map to Hawkins' 0-1000 scale (Levels 50-200). Students know WHERE they are.

**Why?** Recovery is a journey, not a destination. Levels orient students.

### 4. AA Foundation

Templates map to AA steps (1, 2, 3, 4, 9, 12). The wisdom is proven 90+ years.

**Why?** AA works. We're translating its principles to ML, not inventing new ones.

### 5. Obstacle → Technique Mapping

Each template solves a specific obstacle:

- Recognition solves Lack of Self-Awareness
- Belief solves Hopelessness
- Commitment solves Lack of Discipline
- Inventory solves Denial
- Amends solves Refusal to Repair
- FirstModel solves Fragmentation
- Service solves Isolation

**Why?** Students know exactly what problem each technique addresses.

---

## Extending the Framework

To add an 8th recovery template:

1. **Identify the obstacle** — what limitation does it solve?
2. **Map the AA step** — which step teaches this principle?
3. **Choose consciousness level** — where does it sit (50-200)?
4. **Implement both sides:**
   - `sklearn_implementation()` — Python/scikit-learn code
   - `pytorch_implementation()` — PyTorch code
5. **Define expected_metrics()** — what improvement does it produce?
6. **Write wisdom_translation** — how does this teach a machine?
7. **Add to TEMPLATE_REGISTRY** — register in the global dict
8. **Create course** — design human curriculum that teaches it
9. **Write tests** — unit tests in `test_recovery_templates.py`

---

## References

- AA 12 Steps: https://www.aa.org/
- Hawkins Consciousness Scale: *Power vs Force* (David Hawkins)
- Recovery Housing: NARH National Standards
- SMART Recovery: smartrecovery.org
- Peer Support Specialists: AARC Curriculum

---

**University Recovery Templates v1.0**  
Created: 2026-07-21  
Last Updated: 2026-07-21  
Status: Complete & Tested
