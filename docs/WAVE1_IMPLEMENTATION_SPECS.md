---
doc_id: EMPIRICA-EVAL-001
title: Wave 1 Ranked Opportunities - Implementation Specifications
revision: 1
status: approved
owner: empirica-foundation-evaluator
approved_by: carly
approved_date: 2026-08-21
review_due: 2026-09-21
canonical: true
retention: permanent
---

# Wave 1 Implementation Specifications

**Resource Allocation:** 15-25 hours, 105-110k tokens  
**Timeline:** Weeks 1-2 (2026-08-26 start)  
**Target:** Deploy 3 highest-ROI opportunities (Test Coverage Dashboard, Utility Module Library, CI/CD Consolidation)

---

## Opportunity 1: Utility Module Library (ROI 2.14)

**Category:** Code Reuse | **IMPACT:** 0.88 | **FEASIBILITY:** 0.95 | **STRATEGIC_FIT:** 0.90 | **COST:** 35k tokens

### Implementation Steps
1. Extract emailService.js as npm module (async queue, retry logic, templates)
2. Extract tokenService.js as npm module (JWT, refresh logic, validation)
3. Create schema migration system (Flyway/Liquibase style)
4. Publish to org npm registry (scoped @humanaios/*)
5. Update all service dependencies to use published modules

### Dependencies
- Org npm registry access
- SemVer discipline
- Test coverage for utilities

### Risk Analysis
- Breaking changes in utilities affect all consumers
- Mitigation: Semantic versioning, feature flags, gradual rollout
- Rollback: Revert to inline copies

### Success Metrics
- 3+ services adopt modules
- 50% code duplication reduced
- <10ms module startup time

---

## Opportunity 2: CI/CD Workflow Consolidation (ROI 2.03)

**Category:** CI/CD | **IMPACT:** 0.95 | **FEASIBILITY:** 0.90 | **STRATEGIC_FIT:** 0.95 | **COST:** 40k tokens

### Implementation Steps
1. Audit all 35 workflows, classify by pattern (test, deploy, notify, security)
2. Extract 8-12 canonical workflow templates
3. Create `workflows/templates/` directory structure
4. Update all repos to call templates instead of inline steps
5. Document pattern matching guide for new workflows

### Dependencies
- GitHub Actions permissions
- Org-level workflow access
- Template repository setup

### Risk Analysis
- Dependency on reusable workflow syntax
- Mitigation: Verify org permissions, test in staging
- Rollback: Restore individual workflows from git history

### Success Metrics
- 35 → 12 unique workflows
- <2min per-repo update time
- Zero CI failures in rollout

---

## Opportunity 3: API Documentation Generator (ROI 2.03)

**Category:** Developer Experience | **IMPACT:** 0.70 | **FEASIBILITY:** 0.92 | **STRATEGIC_FIT:** 0.75 | **COST:** 30k tokens

### Implementation Steps
1. Auto-generate API docs from code (OpenAPI/Swagger)
2. Create interactive explorer
3. Implement changelog tracking
4. Deploy to docs site
5. Integrate with CI/CD pipeline

### Dependencies
- OpenAPI/Swagger tooling
- Docs site infrastructure
- CI/CD pipeline access

### Risk Analysis
- Low risk (read-only documentation)
- Mitigation: Test in staging first
- Rollback: Remove from CI, restore manual docs

### Success Metrics
- 100% API endpoints documented
- <1s interactive explorer load time
- Zero documentation debt

---

## Wave 1 Success Criteria

✅ All 3 opportunities implemented  
✅ Tests passing  
✅ Documentation updated  
✅ Team trained  
✅ Monitoring in place  

---

## Next Wave Trigger

Wave 1 completion unlocks Wave 2 (Observability Stack, Behavioral Compliance, Secrets Management).

**Decision:** Local-machine-optimizer approves Wave 1 + provides deployment timeline.
