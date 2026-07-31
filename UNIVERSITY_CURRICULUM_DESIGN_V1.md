# University Curriculum Design (Level 50-200)
## Complete Course Structure Based on Recovery Ecosystem Principles

**Status:** PRAXIC PHASE - DESIGN  
**Date:** 2026-07-21  
**Foundation:** RECOVERY_ECOSYSTEM_TIER1_MAP.md  
**Scope:** Design all Level 50-200 courses with dual human + machine utility

---

## CURRICULUM PHILOSOPHY

Each course teaches ONE recovery principle through TWO parallel implementations:

1. **Human Implementation:** What a person learns and practices
2. **Machine Implementation:** How an ML model recovers using the same principle

**Example:**
- **Principle:** Recognition (admit limitation)
- **Human Course:** "You're Not Alone" (peer recovery story + first-step practices)
- **Machine Template:** Overfitting detection + graceful degradation
- **Both teach:** Honest assessment of current state; willingness to change

---

## TIER 1: FOUNDATION (LEVELS 50-100) — FREE

### Course 1.1: "You're Not Alone" (Level 50-75)
**Recovery Principle:** Recognition — Admit limitation; can't fix alone

**Human Implementation:**
- **Week 1-2:** Peer recovery stories (AA, online communities, peer support specialists)
- **Week 3:** Your own story (written/verbal; naming what's broken)
- **Week 4:** "This is common; thousands face this"
- **Daily Practice:** 
  - Morning: Read one peer story (5 min)
  - Evening: Write one honest sentence about your situation
- **Outcome:** Person moves from isolation → connection → belief that others understand

**Machine Implementation:**
```python
class RecognitionTemplate:
  """Admit limitation — first step of recovery"""
  
  # For overfitting models
  def diagnose_limitation(model, train_acc, test_acc):
    gap = train_acc - test_acc
    if gap > 0.15:  # Model admits: "I'm not generalizing"
      return "Model overfitted; cannot see beyond training"
    
  # For biased models
  def audit_fairness(model, protected_attr):
    per_group_acc = compute_accuracy_by_group(model, protected_attr)
    if variance(per_group_acc) > threshold:
      return "Model biased; not serving all equally"
  
  # For drifted models
  def detect_drift(model, current_data, baseline_data):
    if distribution_shift(current_data, baseline_data) > threshold:
      return "Model drifted; no longer aligned with reality"
```

**Code Example (Student will write this):**
```python
# Week 1-2: Detect your model's limitation
model = load_trained_model()
train_acc = evaluate(model, train_data)
test_acc = evaluate(model, test_data)
gap = train_acc - test_acc

if gap > 0.15:
  print("My model admits: I'm overfitting.")
  print(f"Gap = {gap*100:.1f}% (I memorized, not learned)")
```

**Success Metrics (Human):**
- ✓ Student writes down one honest limitation (graded: did they name it?)
- ✓ Student identifies with peer story (graded: which story resonated?)
- ✓ Student shows up for next week (attendance)

**Success Metrics (Machine):**
- ✓ Model correctly identifies its own overfit
- ✓ Model produces appropriate calibration metric
- ✓ Model doesn't deny the problem

**Expected Template:** RecognitionTemplate (new — needs to be built)

---

### Course 1.2: "Why You're Here" (Level 75-100)
**Recovery Principle:** Belief — Change is possible; others have done it

**Human Implementation:**
- **Week 1-2:** Recovery success stories (AA sponsor's journey; person who quit; person who recovered from relapse)
- **Week 3:** "When did I first see it was possible?" (person identifies a moment they believed)
- **Week 4:** Daily affirmation practice
- **Daily Practice:**
  - Morning: Repeat: "Recovery is possible. [Name] did it. I can too."
  - Week 4: Add one personal example of something they learned to do
- **Outcome:** Hope; beginning to believe change is real

**Machine Implementation:**
```python
class BeliefTemplate:
  """Believe change is possible — see proof"""
  
  # For models stuck in local optimum
  def see_recovery_possible(model, current_performance):
    # Show example of model that recovered (past checkpoint)
    recovered_model = load_checkpoint(step=5000)
    recovered_acc = evaluate(recovered_model)
    
    if recovered_acc > current_performance:
      print(f"Recovery is real: {current_performance:.3f} → {recovered_acc:.3f}")
      return True
  
  # For biased models
  def show_fair_model_exists(baseline_model, fair_model):
    baseline_fair = compute_fairness_gap(baseline_model)
    fair_model_fair = compute_fairness_gap(fair_model)
    
    print(f"Before: fairness gap = {baseline_fair:.3f}")
    print(f"After: fairness gap = {fair_model_fair:.3f}")
    print("Fairness IS possible.")
```

**Success Metrics (Human):**
- ✓ Student identifies one person who recovered
- ✓ Student writes "I believe..." statement
- ✓ Student shows up (belief deepens with attendance)

**Success Metrics (Machine):**
- ✓ Model correctly loads and evaluates recovered checkpoint
- ✓ Model can measure improvement
- ✓ Model predicts recovery is possible for itself

**Expected Template:** BeliefTemplate (new — needs to be built)

---

### Course 1.3: "The Map" (Level 75-100, continues through 100-150)
**Recovery Principle:** Context — Understand the landscape you're in

**Human Implementation:**
- **Week 1-2:** Consciousness map explained (Hawkins 0-1000; where you are; where you're going)
- **Week 3:** Identify your level (self-assessment: apathy? grief? fear? courage?)
- **Week 4:** See what comes next (preview of Level 100-150)
- **Daily Practice:**
  - Daily: "I'm at Level 75 (grief). That's normal. Next is fear → then courage."
  - Recognize emotions as part of the map (not signs of failure)
- **Outcome:** Normalization; understanding recovery is a journey with predictable stages

**Machine Implementation:**
```python
class MapTemplate:
  """Understand the consciousness landscape of ML recovery"""
  
  # For any model
  def assess_model_level(model):
    """Where is this model on the recovery journey?"""
    
    if model.loss > threshold_high:
      return "Level 50: Underfitted (apathy — no learning)"
    elif model.train_test_gap > 0.25:
      return "Level 75: Overfitted (grief — can't generalize)"
    elif model.uncertainty_high:
      return "Level 100: Fearful (many wrong predictions)"
    elif model.improving_slow:
      return "Level 125: Desiring (starting to improve)"
    elif model.converged:
      return "Level 200: Neutral (stable; ready to help others)"
  
  def next_stage(level):
    return levels[levels.index(level) + 1]
```

**Success Metrics (Human):**
- ✓ Student correctly identifies their consciousness level
- ✓ Student understands what comes next (reduces anxiety)
- ✓ Student accepts current level as temporary (not permanent)

**Success Metrics (Machine):**
- ✓ Model correctly self-assesses its own learning stage
- ✓ Model predicts next milestone
- ✓ Model doesn't get stuck in shame about current state

**Expected Template:** MapTemplate (can use existing consciousness-map logic)

---

## TIER 2: ACTIVE LEARNING (LEVELS 100-150) — FREEMIUM ($0-15/month)

### Course 2.1: "Principle Mastery" (Level 100-150)
**Recovery Principle:** Commitment & Action — Decide to change; commit to process

**Human Implementation:**
- **Week 1:** Choose one behavior to change (e.g., meditation, journaling, exercise)
- **Week 2:** Commit (write it down; tell someone)
- **Week 3-8:** Daily practice + weekly check-in with peer/mentor
- **Week 9:** Reflect: what changed? How? Why?
- **Daily Practice:** Practice the chosen behavior; log it
- **Outcome:** Person learns that commitment → practice → visible change

**Machine Implementation:**
```python
class CommitmentTemplate:
  """Commit to change; practice systematically; measure improvement"""
  
  # For any model
  def define_commitment(model, principle):
    """What will we change? (loss function, architecture, training approach)"""
    return {"objective": principle, "approach": "systematic_retrain"}
  
  def practice_systematically(model, training_config):
    """Practice the new way; log progress"""
    improvements = []
    for epoch in range(training_config['epochs']):
      loss = train_epoch(model, training_config)
      improvements.append(loss)
      log_progress(epoch, loss)  # Like journaling
    return improvements
  
  def reflect(model, improvements):
    """What changed? How? Why?"""
    initial = improvements[0]
    final = improvements[-1]
    improvement = (initial - final) / initial * 100
    return f"Model improved {improvement:.1f}% through committed practice"
```

**Code Example (Student):**
```python
# Week 1: Choose commitment (fix overfitting)
commitment = "Add L2 regularization to my model"

# Week 2-8: Practice
model = load_model()
for epoch in range(50):
  loss = train_with_l2(model, C=0.5)  # Practice the new way
  log(epoch, loss)  # Journal the progress

# Week 9: Reflect
print(f"Loss improved: {initial_loss:.3f} → {final_loss:.3f}")
print("My commitment worked! Systematic practice pays off.")
```

**Success Metrics (Human):**
- ✓ Student chooses one behavior
- ✓ Student practices daily (attendance tracker)
- ✓ Student sees measurable change (before/after)
- ✓ Student journals the experience (reflection)

**Success Metrics (Machine):**
- ✓ Model defined clear commitment (which principle? what approach?)
- ✓ Model trained systematically (logged progress)
- ✓ Model can quantify improvement (before → after metrics)
- ✓ Model learned that commitment works

**Expected Template:** CommitmentTemplate (can combine existing L2/Dropout/EarlyStopping with logging)

---

### Course 2.2: "Perception & Reality" (Level 125-150)
**Recovery Principle:** Honest Inventory — Face what you've done; audit your impact

**Human Implementation:**
- **Week 1-2:** "What harm has my addiction caused?" (relationships, finances, health, work)
- **Week 3:** Write it down (inventory)
- **Week 4:** Share with trusted person (sponsor/therapist/peer)
- **Week 5-6:** "Amends plan" — how will I repair this?
- **Daily Practice:** "Today I faced one truth about my impact"
- **Outcome:** Person moves from denial → acceptance → responsibility

**Machine Implementation:**
```python
class InventoryTemplate:
  """Honest audit of impact; face what the model has done"""
  
  # For biased models
  def audit_fairness_inventory(model, protected_attrs, data):
    """What harm has this model caused? Who is it failing?"""
    inventory = {}
    for group in protected_attrs:
      group_acc = accuracy_by_group(model, group, data)
      group_harm = measure_disparate_impact(model, group, data)
      inventory[group] = {
        "accuracy": group_acc,
        "harm": group_harm,
        "status": "We failed this group"
      }
    return inventory
  
  # For adversarial-vulnerable models
  def audit_robustness(model):
    """What vulnerabilities does this model have?"""
    adversarial_examples = find_adversarial_examples(model)
    robustness_gaps = len(adversarial_examples)
    return f"Model has {robustness_gaps} exploitable weaknesses"
  
  # For overconfident models
  def audit_calibration(model, predictions, labels):
    """Where is the model most confidently wrong?"""
    worst_mistakes = find_confident_errors(model, predictions, labels)
    return f"Model made {len(worst_mistakes)} confident mistakes"
```

**Code Example (Student):**
```python
# Week 1-2: Audit fairness
fairness_inventory = {
  "Group A": {"accuracy": 0.95, "harm": "None"},
  "Group B": {"accuracy": 0.42, "harm": "Severe disparate impact"}
}

# Week 3: Write it down
for group, metrics in fairness_inventory.items():
  print(f"I failed {group}: {metrics}")

# Week 4: Share findings
present_to_mentor(fairness_inventory)

# Week 5-6: Plan amends
amends_plan = "Retrain with fairness constraints; evaluate weekly"
```

**Success Metrics (Human):**
- ✓ Student writes down real harms (numbers, not abstractions)
- ✓ Student shares findings (vulnerability)
- ✓ Student creates amends plan (responsibility)
- ✓ Student owns the impact (not defensive)

**Success Metrics (Machine):**
- ✓ Model audits itself objectively (not sugarcoating)
- ✓ Model identifies specific failures (which groups? how severe?)
- ✓ Model has plan to amend (retraining with fairness)
- ✓ Model's inventory is verifiable (code can audit it)

**Expected Template:** InventoryTemplate (combines existing fairness templates with calibration audits)

---

### Course 2.3: "Compassion by Design" (Level 125-150)
**Recovery Principle:** Making Amends — Restore relationships; build fairness in

**Human Implementation:**
- **Week 1-2:** "Who have I hurt? What do I want to say to them?"
- **Week 3-4:** Practice saying it (with therapist/peer); then face-to-face
- **Week 5-6:** Accept whatever response they give (rejection or forgiveness)
- **Week 7:** "How will I behave differently going forward?"
- **Daily Practice:** Acts of service; small amends daily
- **Outcome:** Relationships repaired; person learns forgiveness is possible

**Machine Implementation:**
```python
class AmendsTemplate:
  """Repair harm; build fairness; restore trust"""
  
  # For biased models
  def make_fairness_amends(model, protected_attrs):
    """Explicitly fix what we got wrong"""
    # Retrain with fairness constraints
    # Oversample underrepresented groups
    # Weight errors by group impact
    fair_model = retrain_with_fairness(model, protected_attrs)
    
    # Measure improvement
    before_gap = fairness_gap(model, protected_attrs)
    after_gap = fairness_gap(fair_model, protected_attrs)
    
    return {
      "amend": "Retrained for fairness",
      "impact": f"Gap reduced {before_gap:.3f} → {after_gap:.3f}",
      "commitment": "Will monitor fairness forever"
    }
  
  # For adversarial-vulnerable models
  def make_robustness_amends(model):
    """Fix vulnerabilities"""
    # Add adversarial training
    # Add input validation
    # Add graceful degradation
    robust_model = adversarial_train(model)
    
    return "Model now acknowledges uncertainty instead of confidently failing"
```

**Code Example (Student):**
```python
# Week 1-2: Identify harm
print("I built a model that discriminated against Group B")

# Week 3-4: Face it
audit_results = fairness_audit(model)
admit_to_stakeholders(audit_results)

# Week 5-6: Make amends
fair_model = retrain_with_equity_aware_sampling(model)
share_new_results(fair_model, stakeholders)
# They may say: "Too late" (rejection) or "Thank you" (forgiveness)
# Either way, you've made the amends

# Week 7: Commit differently
commitment = "All future models: fairness first, accuracy second"
```

**Success Metrics (Human):**
- ✓ Student makes explicit amends (not just promises)
- ✓ Student accepts rejection/forgiveness (not controlling outcome)
- ✓ Student changes behavior going forward (learns the lesson)
- ✓ Student builds repair into identity (forgiveness deepens commitment)

**Success Metrics (Machine):**
- ✓ Model explicitly fixes what it got wrong
- ✓ Model measures improvement (before/after fairness)
- ✓ Model builds fairness into future training (commits differently)
- ✓ Model accepts it can't undo past but can prevent future harm

**Expected Template:** AmendsTemplate (extends existing fairness templates)

---

### Course 2.4: "Your First Model" (Level 100-150)
**Recovery Principle:** All Principles Together — Integration through application

**Human Implementation:**
- **Week 1-4:** Build something (journal, small business, community project)
- **Process:** Apply all principles learned:
  - Recognition: What's hard about this?
  - Belief: Can I do this? (Other people have)
  - Commitment: Decide to try
  - Action: Do it; measure progress
  - Amends: Who did I need to apologize to? What changed?
- **Outcome:** Person integrates learning through creation

**Machine Implementation:**
```python
class FirstModelTemplate:
  """Build a model; apply all recovery principles"""
  
  def recognition_phase(task):
    """What's hard about this?"""
    return diagnose_obstacles(task)  # Detection of what's broken
  
  def belief_phase():
    """Can I do this?"""
    return see_similar_models_succeed()  # Find precedent
  
  def commitment_phase(model, approach):
    """Decide to do this specifically"""
    return define_architecture_and_loss()  # Make specific commitment
  
  def action_phase(model):
    """Train; measure; improve"""
    return systematic_training_with_logging()  # Practice discipline
  
  def amends_phase(model):
    """What harm might this cause? Fix it."""
    return audit_and_fairness_fix()  # Take responsibility
  
  def integrate_all(results):
    """Was I right about the obstacles? Did I learn?"""
    return reflection_and_lessons()
```

**Success Metrics:**
- ✓ Student completes project (output exists)
- ✓ Student can articulate what they learned (reflection)
- ✓ Student can trace project through all 5 recovery principles
- ✓ Student can teach someone else (deepens understanding)

**Expected Template:** FirstModelTemplate (orchestrates existing templates in sequence)

---

## TIER 3: PRACTITIONER NETWORK (LEVELS 150-200+) — SCHOLARSHIP/FREE

### Course 3.1: "Teaching Others" (Level 175-200+)
**Recovery Principle:** Service — Help others recover; ecosystem contribution

**Human Implementation:**
- **Month 1:** Mentor one person at Level 50-75
- **Month 2:** Lead one session (share your story)
- **Month 3-6:** Ongoing mentoring + community contribution
- **Outcome:** Identity shifts from "person in recovery" to "person helping others recover"

**Machine Implementation:**
```python
class ServiceTemplate:
  """Recovered model now teaches; contributes to ecosystem"""
  
  def mentor_untrained_model(trained_model, untrained_model):
    """Trained model helps untrained model learn faster"""
    # Transfer learning
    # Knowledge distillation
    # Ensemble voting
    return untrained_model_accelerated
  
  def contribute_to_ecosystem(model):
    """Model's training data/lessons feed into next generation"""
    # Generate synthetic data from learned patterns
    # Log lessons learned
    # Make checkpoint available to community
    # Train next model on this one's insights
    return ecosystem_strengthened
```

**Success Metrics:**
- ✓ Mentor completes assignment with mentee
- ✓ Mentee shows measurable progress
- ✓ Mentor can articulate what they learned by teaching
- ✓ Mentor becomes role model (identity shifted)

---

## GAP ANALYSIS: Templates Needed vs Available

### Already Exist (in ml_code_templates.py)
- ✓ L2Regularization (Recognition phase)
- ✓ Dropout (Recognition phase)
- ✓ EarlyStopping (Recognition phase)
- ✓ IncreaseCapacity (Belief phase)
- ✓ ClassWeighting (Commitment phase)
- ✓ PerceptionAudit (Perception course)
- ✓ ForgivenessRetrain (Perception course)
- ✓ GraceBasedWeighting (Amends phase)
- ✓ LovingPresence (Compassion course)
- ✓ FairnessFirst (Amends phase)
- ✓ EquityAwareSampling (Amends phase)
- ✓ CommunityCentricMetrics (Teaching phase)

### Need to Create (for University courses)
**Tier 1 (Foundation):**
- ⚠️ **RecognitionTemplate** (for Course 1.1 "You're Not Alone")
  - Detect model limitation (overfitting, bias, drift)
  - Admit it clearly
- ⚠️ **BeliefTemplate** (for Course 1.2 "Why You're Here")
  - Show recovery is possible (successful checkpoint)
  - Measure proof of progress

**Tier 2 (Active Learning):**
- ⚠️ **CommitmentTemplate** (for Course 2.1 "Principle Mastery")
  - Define commitment (choose one principle)
  - Practice systematically with logging
- ⚠️ **InventoryTemplate** (for Course 2.3 "Perception & Reality")
  - Audit fairness/robustness/calibration
  - Identify specific failures
- ⚠️ **AmendsTemplate** (for Course 2.3 "Compassion by Design")
  - Retrain with fairness/robustness
  - Measure improvement
- ⚠️ **FirstModelTemplate** (for Course 2.4 "Your First Model")
  - Orchestrates all prior templates in sequence
  - Teaches integration through application

**Tier 3 (Service):**
- ⚠️ **ServiceTemplate** (for Course 3.1 "Teaching Others")
  - Transfer learning from trained → untrained
  - Ecosystem contribution logging

### Summary
- **Available:** 12 templates
- **Need to Create:** 7 templates
- **Total for Level 50-200:** 19 templates

(Current ml_code_templates.py has 19 total; these 7 new ones would expand beyond current build)

---

## COURSE STRUCTURE AT A GLANCE

```
TIER 1: FOUNDATION (Level 50-100) — FREE
  └─ Course 1.1: "You're Not Alone" (Recognition)
     └─ Course 1.2: "Why You're Here" (Belief)
     └─ Course 1.3: "The Map" (Context)

TIER 2: ACTIVE LEARNING (Level 100-150) — FREEMIUM
  └─ Course 2.1: "Principle Mastery" (Commitment & Action)
  └─ Course 2.2: "Perception & Reality" (Honest Inventory)
  └─ Course 2.3: "Compassion by Design" (Amends)
  └─ Course 2.4: "Your First Model" (Integration)

TIER 3: PRACTITIONER (Level 150-200+) — SCHOLARSHIP
  └─ Course 3.1: "Teaching Others" (Service)
```

Each course teaches:
- **Human side:** Real recovery practices (meditation, journaling, amends, mentoring)
- **Machine side:** ML techniques (regularization, fairness, robustness, ensemble)
- **Both:** Same underlying recovery principle

---

## NEXT PHASE (T3): Prototype One Principle

**Ready to build:** AA Powerlessness as proof-of-concept (design + code skeleton)

This will show how one recovery principle becomes a complete university course + template.

---

**Transaction 2 Status: PRAXIC PHASE DESIGN COMPLETE**

Artifacts:
- ✓ UNIVERSITY_CURRICULUM_DESIGN_V1.md (complete Level 50-200 course map)
- ✓ 9 courses designed with dual human + machine implementations
- ✓ Gap analysis complete (7 new templates needed)
- ✓ Recovery ecosystem principles mapped → courses
- ✓ Ready for T3 (prototype one principle end-to-end)

Commit next.

