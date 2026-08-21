# Workflow Template Matching Guide

Map existing 102 workflows to 12 canonical templates for consolidation.

## Template Mapping Reference

### Template 01: CI - Test & Lint
**Maps to:** `ci.yml`, `test.yml`, `lint.yml`, `npm-publish.yml` (test phase)
**Used by:** humanaios, website, empirica-foundation
**Consolidation:** Merge project-specific CI workflows into this universal template

### Template 02: Security - Scan & Audit
**Maps to:** `security-scan.yml`, `semgrep-review.yml`, `secret-scan.yml`, `codeql.yml`
**Used by:** All projects (outreach: 35+ instances)
**Consolidation:** Replace per-project security workflows with this canonical template

### Template 03: Compliance - Policy & Standards
**Maps to:** `behavioral-compliance.yml`, `document-control.yml`, `findings-registry-gate.yml`, `state-validate.yml`
**Used by:** outreach, operations (35+ instances)
**Consolidation:** Unify compliance checking across all projects

### Template 04: Build & Deploy
**Maps to:** `build.yml`, `deploy-*.yml`, `release.yml`, `pages.yml`
**Used by:** All projects needing CI/CD
**Consolidation:** Replace inline deploy steps with template + config

### Template 05: Data - Pipeline & Sync
**Maps to:** `intake-pipeline.yml`, `mesh-sync-batch.yml`, `registry-mirror-sync.yml`, `smag-capture.yml`, `smag-consolidate.yml`, `weekly-funding-rescore.yml`, `weekly-profile-sync.yml`
**Used by:** All projects with data workflows (15+ instances)
**Consolidation:** Separate data pipelines into this standard template

### Template 06: Monitoring - Health & Alerts
**Maps to:** `drift-monitor.yml`, `daily-deadline-alerts.yml`, `agent-api-monitor.yml`, `haios-corpus-integrity.yml`, `haios-harmonizer-pulse.yml`, `haios-standing-audit.yml`, `haios-system-audit.yml`
**Used by:** outreach, operations (12+ instances)
**Consolidation:** Unify monitoring & alerting patterns

### Template 07: Documentation - Generate & Deploy
**Maps to:** `jekyll-gh-pages.yml`, and documentation-related workflows
**Used by:** humanaios-internal, website
**Consolidation:** Standardize docs generation & deployment

### Template 08: Release - Publish & Tag
**Maps to:** `release.yml`, `npm-publish.yml` (publish phase), `release-to-zenodo.yml`
**Used by:** Projects needing release automation
**Consolidation:** Unified release process across all projects

### Template 09: Audit - Code Quality & Coverage
**Maps to:** `sonarcloud-baseline-auto.yml`, `sonarqube.yml`, `sonarqube-issues.yml`, `scorecard.yml`
**Used by:** All projects (outreach: 3 instances)
**Consolidation:** Single quality audit template per project

### Template 10: Scheduled - Maintenance & Cleanup
**Maps to:** `scheduled-audit.yml`, `Refresh.yml`, `Import.yml`, `refresh.yml`, `cleanup.yml` patterns
**Used by:** All projects (7+ instances)
**Consolidation:** Standard maintenance schedule

### Template 11: Integration - End-to-End Tests
**Maps to:** `integration.yml`, `e2e.yml`, `acat-bot-test.yml`, `acat_pipeline_trigger.yml`, `acat-pipeline-trigger.yml`
**Used by:** humanaios, outreach, website (5+ instances)
**Consolidation:** Unified E2E testing pattern

### Template 12: Notifications - Status & Reports
**Maps to:** `announce-findings.yml`, `auto-request-copilot-review.yml`, `agent-principle-compliance-check.yml`, `ledger-capture.yml`
**Used by:** All projects for notifications (8+ instances)
**Consolidation:** Central notification pattern

## Migration Strategy

### Phase 1: Project Mapping (Done)
- [x] Analyze 102 existing workflows
- [x] Classify into 12 template families
- [x] Document mapping relationships

### Phase 2: Template Adoption (Next)
- [ ] Create reusable workflow references in `.github/workflows/templates/`
- [ ] Update each project to call templates instead of inline workflows
- [ ] Test in non-critical repos first (website, humanaios-internal)
- [ ] Migrate critical projects (outreach, operations, evaluator)

### Phase 3: Consolidation (Follow-up)
- [ ] Delete replaced inline workflows
- [ ] Archive old workflow history in git
- [ ] Document per-project customization (if any)
- [ ] Update CI/CD documentation

## Per-Project Migration Order

1. **Low Risk** (can migrate immediately): humanaios, website, humanaios-internal
2. **Medium Risk** (test first): grok-crossref, lasting-light-ai
3. **High Risk** (careful rollout): empirica-outreach, humanaios/operations
4. **Critical** (last): empirica-foundation-evaluator

## Expected Outcomes

- **Workflow Count:** 102 → 12 canonical templates
- **Code Duplication:** 50%+ reduction
- **Maintenance:** Centralized, consistent patterns
- **Update Velocity:** Change once, propagate to all projects
- **Monitoring:** Unified health/alert patterns

## Configuration Pattern

Each project customizes templates via:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    uses: humanaios/.github/workflows/01-ci-test.yml@main
    with:
      node-version: '18'
      coverage-threshold: 80
```

See `TEMPLATES_README.md` for full configuration reference.
