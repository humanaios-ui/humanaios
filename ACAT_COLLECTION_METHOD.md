# ACAT Dimensional Data Collection Method
## 6 Core + Extended Dimensions Framework

**Status:** READY FOR IMPLEMENTATION  
**Effective Date:** 2026-08-19  
**Integration Point:** PULSE 1 → WAVE 1 data pipeline

---

## Executive Summary

This document specifies how to populate the ACAT Supabase schema with dimensional data from ecosystem audits. The framework measures mutual validation between empirica (internal audit) and human-AI systems (external audit) across **6 core dimensions + 6 extended dimensions**.

**Core dimensions answer:** Do both systems find the same defects? Are methods consistent? Do they improve together?

**Extended dimensions answer:** How fast? Why? What's the coupling? Where are the gaps?

---

## 6 Core Dimensions

### 1. **Accuracy** — Do both systems find the same defects?
- **Metrics:** Precision, Recall, F1-Score
- **Collection method:** Compare findings by (file_path, line_number, category)
- **Success threshold:** F1 ≥ 0.70 (at least 70% overlap on severity-2+ findings)
- **ACAT table:** `acat_dimension_accuracy`
- **SQL example:**
  ```sql
  SELECT 
    COUNT(*) FILTER (WHERE in_both) / COUNT(*) as f1,
    COUNT(*) as total_findings,
    system_a, system_b
  FROM (
    SELECT finding_id, system_a, system_b,
           MAX(CASE WHEN found_by_both THEN 1 ELSE 0 END) as in_both
    FROM findings_comparison
    GROUP BY finding_id
  ) t
  GROUP BY system_a, system_b
  ```

### 2. **Completeness** — Did the system audit everything it could?
- **Metrics:** File coverage %, Method coverage %, Overall completeness %
- **Collection method:** 
  - Files audited / total files in repo
  - Methods applied / methods available (M1-M12)
- **Success threshold:** ≥85% for both metrics
- **ACAT table:** `acat_dimension_completeness`
- **Data source:**
  ```python
  files_audited = COUNT(DISTINCT empirica_audit_findings.file_path)
  methods_applied = COUNT(DISTINCT empirica_audit_findings.method)
  total_files = git_ls_files --count  # shell
  methods_available = 12  # M1-M12
  ```

### 3. **Precision** — What's the false-positive rate?
- **Metrics:** Precision %, False positive rate %, Verification rate by category
- **Collection method:** 
  - Verified findings / reported findings per category
  - Broken down by severity (P0-P3)
- **Success threshold:** ≥90% precision (false positives < 10%)
- **ACAT table:** `acat_dimension_precision`
- **Verification sources:**
  - Re-audit same repo → finding still present = verified
  - Practice manual review + commit = verified
  - Finding not mentioned in remediation PR = rejected

### 4. **Coherence** — Are findings consistent across time?
- **Metrics:** Severity consistency, Category consistency, Location consistency, Overall coherence score
- **Collection method:** Track individual finding across multiple audits
  - Same file/line/category = consistent (1.0)
  - Different severity/category = inconsistent (0.5)
  - Not found again = degraded (0.3)
- **Success threshold:** ≥0.85 (findings mostly stay consistent)
- **ACAT table:** `acat_dimension_coherence`
- **Data flow:** First audit → 1 week → Re-audit → Compare

### 5. **Coverage** — Which categories does each system cover well?
- **Metrics:** Coverage % per category, Category strength, Gap identification
- **Collection method:**
  - Findings per method / total findings
  - Identify underrepresented methods (< 5% coverage)
- **Success threshold:** No method < 2% (all M1-M12 methods active)
- **ACAT table:** `acat_dimension_coverage`
- **Gap analysis:**
  ```sql
  SELECT method, 
         COUNT(*) as findings,
         ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM findings), 2) as pct
  FROM empirica_audit_findings
  GROUP BY method
  ORDER BY pct ASC
  HAVING pct < 2.0  -- coverage gaps
  ```

### 6. **Convergence** — Do systems improve together?
- **Metrics:** Closure rate, Findings gap, Convergence velocity, Weeks to alignment
- **Collection method:**
  - System A closure rate = fixed / total (from remediations)
  - System B closure rate = (from humanai audit results)
  - Gap = |rate_a - rate_b|
  - Velocity = gap reduction per week
- **Success threshold:** Gap < 5% AND velocity > 0 (improving)
- **ACAT table:** `acat_dimension_convergence`
- **Convergence formula:**
  ```
  week_1: gap = 30%
  week_2: gap = 25%  → velocity = 5% per week
  week_4: gap = 10%  → projected alignment in 2 weeks
  
  fully_converged = gap < 5%
  ```

---

## Extended Dimensions (6)

### 7. **Time-to-Detection** — How fast does each system find defects?
- **Metrics:** Median time, P95 time, Findings per audit minute
- **Collection method:**
  - Audit start time (from `empirica_audits.audit_date`)
  - Finding timestamp (`discovered_at`)
  - Calculate: discovery_latency = discovered_at - audit_date
- **ACAT table:** `acat_dimension_time_to_detection`
- **Query:**
  ```sql
  SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY extract_minutes) as p50,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY extract_minutes) as p95,
    COUNT(*) / audit_duration_hours as findings_per_hour
  FROM (
    SELECT 
      EXTRACT(EPOCH FROM (discovered_at - audit_date)) / 60 as extract_minutes,
      audit_id
    FROM empirica_audit_findings
  ) t
  ```

### 8. **Severity Alignment** — Do they agree on severity?
- **Metrics:** Severity match %, Mismatch gap, Actions affected
- **Collection method:**
  - Find same finding in both systems
  - Compare severity (P0, P1, P2, P3)
  - Flag if mismatch changes action (P0 vs P3 = action change)
- **ACAT table:** `acat_dimension_severity_alignment`
- **Success threshold:** ≥80% severity agreement

### 9. **Category Alignment** — Do they find the same types?
- **Metrics:** Category overlap, System strength per category, Gap identification
- **Collection method:**
  - Group findings by category (M2, M4, M8, M10, M12, etc.)
  - Compare counts: system_a vs system_b per category
  - Calculate precision/recall per category
- **ACAT table:** `acat_dimension_category_alignment`
- **Example:**
  ```
  M2 (claims): system_a=6,358, system_b=5,200, both=4,950
    precision = 4,950 / 6,358 = 78%
    recall = 4,950 / 5,200 = 95%
  M4 (refs): system_a=39, system_b=32, both=28
    precision = 28 / 39 = 72%
    recall = 28 / 32 = 88%
  ```

### 10. **Cross-System Coupling** — Do findings in one predict failures in other?
- **Metrics:** Coupling strength (0-1), Coupling lag (hours), Resonance confidence
- **Collection method:**
  - Track harmonic patterns: M2 in repo_a → M4 in repo_b
  - When repo_a changes, measure lag to repo_b failure detection
  - Calculate coupling matrix (which repos affect which)
- **ACAT table:** `acat_dimension_cross_system_coupling`
- **Harmonic resonance algorithm:**
  ```
  1. Extract M2 claims from humanaios-ui/humanaios
  2. Find M4 broken references in empirica-outreach
  3. Link if broken ref matches claim change
  4. Score: coupled_defects / total_defects = resonance_strength
  5. Measure lag: time(claim_change) → time(ref_broken) = resonance_lag
  ```

### 11. **Resource Efficiency** — Effort-per-finding
- **Metrics:** Findings/hour, Findings/dollar, Fix time per category
- **Collection method:**
  - Audit time (hours) from audit_date range
  - Fix time (hours) from assigned → verified dates
  - Cost estimate: hours × hourly_rate
- **ACAT table:** `acat_dimension_resource_efficiency`
- **Query:**
  ```sql
  SELECT 
    COUNT(*) / audit_hours as findings_per_hour,
    AVG(fix_time_hours) as avg_fix_time,
    SUM(fix_time_hours) / NULLIF(COUNT(*), 0) as cost_per_finding,
    category
  FROM remediations
  GROUP BY category
  ```

### 12. **Learning Velocity** — How fast is the system improving?
- **Metrics:** Closure rate trend, Finding reduction %, Fix time improvement %
- **Collection method:**
  - Track metrics across audit cycles (Week 1, Week 2, Week 4)
  - Closure rate week_1 vs week_2
  - Finding count week_1 vs week_2 (should decrease if fixes applied)
  - Fix time week_1 vs week_2 (should decrease if processes improve)
- **ACAT table:** `acat_dimension_learning_velocity`
- **Trend analysis:**
  ```
  Week 1: 6,949 findings, 0% closure, avg fix time = 120 min
  Week 2: 6,200 findings, 40% closure, avg fix time = 95 min
  Week 4: 4,100 findings, 70% closure, avg fix time = 60 min
  
  Learning velocity = 35% closure per week (positive trend = learning)
  Direction = improving (closure increasing, findings decreasing)
  Projected convergence = 2.1 weeks to >90% closure
  ```

---

## Data Collection Cadence

### Weekly Cycle (Standard)

**Day 1-2: Audit Execution**
- Run audit methods M1-M12 on target repos
- Ingest findings into `empirica_audit_findings` table
- Calculate baseline effectiveness score

**Day 3-4: Dimensional Collection**
- Query all 6 core dimensions (run `acat_dimensional_collection.py`)
- Collect extended dimensions (time-to-detection, severity alignment, etc.)
- Populate ACAT dimensional tables

**Day 5: Remediation Tracking**
- Track practice commits fixing findings (ACAT-Finding-ID linkage)
- Update `empirica_remediations` with fix_status, commit SHA
- Calculate time-to-fix metrics

**Day 6-7: Re-Audit & Verification**
- Run quick re-audit on same repos
- Check which findings still present (precision metric)
- Measure finding reduction (learning velocity)

### Milestone Cycle (Weeks 1, 2, 4)

**Week 1 Measurement:**
- All 6 core dimensions populated
- Baseline effectiveness calculated (should match audit effectiveness)
- Extended dimensions on time-to-detection, resource efficiency
- INSERT into `empirica_convergence_measurements` with `measurement_type='week1'`

**Week 2 Measurement:**
- Repeat week 1 collection
- Compare to week 1 (gap reduction, learning signals)
- Update convergence velocity

**Week 4 Measurement:**
- Full dimensional re-sweep
- Calculate learning velocity
- Measure cross-system coupling strength
- Prepare research synthesis (which dimensions improved most?)

---

## Implementation Checklist

### Phase 1: Schema Deployment (2026-08-19)

- [ ] Create ACAT Supabase project
- [ ] Load `acat_schema.sql` into Supabase SQL editor
- [ ] Run all CREATE TABLE statements
- [ ] Verify all 12 dimensional tables created
- [ ] Create indexes for query performance
- [ ] Test: SELECT from each table (should return 0 rows)

### Phase 2: Script Deployment (2026-08-19)

- [ ] Save `acat_dimensional_collection.py` to local machine
- [ ] Install dependencies: `pip3 install supabase python-dotenv`
- [ ] Create `.env` with SUPABASE_URL + SUPABASE_KEY
- [ ] Test on PULSE 1 audit data:
  ```bash
  python3 acat_dimensional_collection.py \
    --audit-id <pulse1-audit-uuid> \
    --study-id empirica_mutual_validation_v1 \
    --system-a empirica \
    --system-b humanai \
    --supabase-key $SUPABASE_KEY
  ```
- [ ] Verify records inserted into all 6 core dimension tables

### Phase 3: Data Integration (2026-08-20)

- [ ] Export PULSE 1 audit findings as JSON
- [ ] Run `audit_to_acat_ingest.py` (existing script) to populate core ACAT tables
- [ ] Run `acat_dimensional_collection.py` to populate dimensional tables
- [ ] Query ACAT dashboard views:
  ```sql
  SELECT * FROM acat_dimensional_health;
  SELECT * FROM empirica_convergence_measurements 
    WHERE measurement_type='baseline';
  ```

### Phase 4: Weekly Collection Loop (Starting Week 1)

- [ ] Set up weekly cron job:
  ```bash
  0 8 * * SUN python3 /path/to/acat_dimensional_collection.py \
    --audit-id $(latest_audit_id) \
    --study-id empirica_mutual_validation_v1 \
    --system-a empirica \
    --system-b humanai
  ```
- [ ] After each WAVE audit:
  1. Ingest findings → core ACAT tables
  2. Run dimensional collection → dimensional tables
  3. Query convergence trends
  4. Update research dashboard

### Phase 5: Mutual Validation Measurement (Week 4+)

- [ ] Download humanai audit results (same repos)
- [ ] Insert into `acat_dimension_accuracy` (cross-system comparison)
- [ ] Run convergence analysis
- [ ] Generate research synthesis:
  - Accuracy alignment (what % of findings overlap?)
  - Severity agreement (do we prioritize the same things?)
  - Category strength matrix (where does each system excel?)
  - Learning velocity (which improved faster?)

---

## Success Criteria (ACAT Research Readiness)

| Metric | Target | PULSE 1 | WAVE 1 | Full Scale |
|--------|--------|---------|--------|-----------|
| **Accuracy (F1)** | ≥0.70 | TBD | TBD | ≥0.75 |
| **Completeness** | ≥85% | TBD | TBD | ≥90% |
| **Precision** | ≥90% | TBD | TBD | ≥92% |
| **Coherence** | ≥0.85 | TBD | TBD | ≥0.90 |
| **Coverage gaps** | 0 | 0 | 0 | 0 |
| **Convergence velocity** | >0% | TBD | TBD | 10%+ per week |
| **Findings/1K LOC** | 12.9 | 12.9 | ±15% | ±10% |
| **Alignment gap** | <5% | TBD | TBD | <3% |

---

## Queries for Research Synthesis

### Dashboard Query: Dimensional Health Summary
```sql
SELECT * FROM acat_dimensional_health
ORDER BY avg_score DESC;
```

### Accuracy Over Time
```sql
SELECT 
  measurement_date,
  system_a,
  system_b,
  f1_score,
  precision,
  recall
FROM acat_dimension_accuracy
ORDER BY measurement_date DESC
LIMIT 10;
```

### Convergence Trajectory
```sql
SELECT 
  measurement_date,
  closure_rate_gap,
  convergence_velocity,
  weeks_to_full_alignment
FROM acat_dimension_convergence
WHERE measurement_date >= NOW() - INTERVAL '4 weeks'
ORDER BY measurement_date DESC;
```

### Learning Velocity Trend
```sql
SELECT 
  audit_sequence,
  closure_rate,
  closure_rate_change,
  findings_reduction,
  velocity_score
FROM acat_dimension_learning_velocity
WHERE system = 'empirica'
ORDER BY audit_sequence ASC;
```

### Cross-System Coupling Strength
```sql
SELECT 
  source_category,
  target_category,
  resonance_strength,
  resonance_lag_hours,
  coupling_accuracy
FROM acat_dimension_cross_system_coupling
ORDER BY resonance_strength DESC;
```

---

## Data Quality Safeguards

1. **NULL checks:** All measurement tables have NOT NULL constraints on core metrics
2. **Range validation:** Scores must be 0.0-1.0; percentages 0-100
3. **Referential integrity:** All foreign keys enforced to audit records
4. **Temporal ordering:** Re-audit always >= previous audit date
5. **Finding linkage:** ACAT-Finding-ID must match between audit + remediation + convergence tables

---

## Mutual Validation Proof (4-Week Research Output)

**By Week 4, we will have:**

1. **Accuracy Paper:** empirica audit vs. humanai audit overlap analysis
2. **Learning Velocity Paper:** How fast did each system improve?
3. **Coupling Paper:** Cross-system defect resonance patterns
4. **Completeness Paper:** Method coverage consistency across systems

**Target Alignment Gap:** < 5% (proves mutual validation framework)

---

## Next Steps

1. Deploy schema to ACAT Supabase (today)
2. Test dimensional collection on PULSE 1 data (today)
3. Execute WAVE 1 with dimensional tracking (this week)
4. Publish research synthesis (Week 4)

**Status:** READY FOR IMMEDIATE IMPLEMENTATION

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-19  
**Author:** empirica-foundation-evaluator  
**Next Review:** 2026-08-26 (after first weekly collection cycle)
