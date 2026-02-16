# FILES TO REMOVE FROM PUBLIC HUMANAIOS REPO
## Generated: February 16, 2026
## Status: CURRENT

These files are currently in the root of the public `humanaios-ui/humanaios` repository
and should be removed or moved to a private location. They contain competitive intelligence,
contact information, partnership strategy, or internal operational details that should not
be publicly visible.

---

## REMOVE IMMEDIATELY (contain names, contacts, or competitive strategy)

- CUSTOMER_OUTREACH_LINKEDIN_MESSAGES.md (contact names, outreach messages)
- CUSTOMER_RESEARCH_5_TARGETS_COMPLETE.md (company research with named targets)
- FRONTIER_CUSTOMER_TARGETS.md (customer pipeline with names)
- ALEXANDER_FOLLOWUP_MESSAGE.md (private correspondence)
- MATT_SHUMER_ENGAGEMENT_IMPACT.md (named individual strategy)
- CHEROKEE_NATION_PARTNERSHIP_PITCH.md (partnership strategy — keep pitch private until partnership is public)
- CHEROKEE_NATION_PARTNERSHIP_ANALYSIS.md (internal analysis)
- MARKETING_INTELLIGENCE_25_COMPANIES_RANKED.md (competitive intelligence)
- MARKETING_INTELLIGENCE_V2_CONSCIOUSNESS.md (competitive intelligence)

## REMOVE (internal operational — adds clutter, no public value)

- ACCOUNTABILITY_STRUCTURE.md (internal process)
- BACKGROUND_TASK_QUEUE.md (internal task tracking)
- OVERNIGHT_WORK_MORNING_BRIEFING.md (session notes)
- WEEK_3_DETAILED_ACTION_PLAN.md (internal planning)
- PROJECT_CONTEXT_MEMORY.md (AI context document)
- TASKRABBIT_TEST_1_PLAN.md (internal experiment)
- TASKRABBIT_APPLICATION.md (internal)
- RENTAHUMAN_PUBLIC_ENGAGEMENT.md (strategy doc)
- DAY_1_SUMMARY.md through DAY_6_FILE_MANIFEST.md (daily logs)
- SYNC_GUIDE_1/2/3 (internal sync process)
- IMMEDIATE_NEXT_.md (internal priorities)
- TOMORROW_ACTI.md (internal planning)
- KNOWN_ISSUES.md (move to GitHub Issues instead)
- QUICKSTART_DAY.md (outdated)
- SOCIAL_MEDIA_UP.md (internal)
- STRATEGIC_PARTN.md (strategy)
- LAYMANS_PRODU.md (draft)
- PRODUCT_DESCRI.md (if duplicate of AI_AGENT_PRODUCT_DESCRIPTION)

## KEEP IN REPO (public-appropriate)

- README.md (corrected version)
- LICENSE
- SECURITY.md
- CONTRIBUTING.md (if it exists)
- .gitignore
- .prettierrc
- tsconfig.json
- turbo.json
- package-lock.json
- schema.sql
- apps/ directory
- src/ directory
- packages/ directory
- infrastructure/ directory
- docs/ directory
- AI_AGENT_PRODUCT_DESCRIPTION.md (public product spec — verify tense compliance)
- 12_TRADITIONS_COMPLIANCE_AUDIT.md (demonstrates governance — verify no sensitive data)
- 12_TRADITIONS_DECISION_FILTER.md (public governance framework)
- COMPREHENSIVE_GAP_ANALYSIS.md (demonstrates honesty — verify no sensitive data)
- PUBLIC_STATEMENTS_AUDIT.md (demonstrates accountability)
- HUMANAIOS_SELF_ASSESSMENT_AND_WAB_CHARTER.docx (public assessment)
- 30_DAY_SPRINT.md (building in public — verify no sensitive data)
- COPYRIGHT_HEAD.md (legal)
- AUTH_DI_ISSUE.md (technical)
- TESTING_GUIDE.md (technical)
- TECHNICAL_ARCHI.md (technical)
- PROJECT_STRUCT.md (technical)
- GITHUB_SETUP.md (technical)

## GIT COMMANDS

```bash
# After reviewing the lists above, remove files:
git rm CUSTOMER_OUTREACH_LINKEDIN_MESSAGES.md
git rm CUSTOMER_RESEARCH_5_TARGETS_COMPLETE.md
git rm FRONTIER_CUSTOMER_TARGETS.md
git rm ALEXANDER_FOLLOWUP_MESSAGE.md
git rm MATT_SHUMER_ENGAGEMENT_IMPACT.md
git rm CHEROKEE_NATION_PARTNERSHIP_PITCH.md
git rm CHEROKEE_NATION_PARTNERSHIP_ANALYSIS.md
git rm MARKETING_INTELLIGENCE_25_COMPANIES_RANKED.md
# ... continue for all files marked REMOVE

# Replace README
cp README_HUMANAIOS_CORRECTED.md README.md

# Commit
git add -A
git commit -m "Remove sensitive documents from public repo, fix README tense compliance

- Remove customer contact data, competitive intelligence, and partnership strategy docs
- Fix README: mark all unbuilt features as planned/future
- Add pre-launch disclaimer
- Add 'What Does Not Exist Yet' section
- Remove present-tense API examples that imply live endpoints
- Keep technical docs, governance frameworks, and product specs"

git push origin main
```

## NOTE

Files removed from git are still in git history. If any files contain truly sensitive
information (passwords, API keys, personal data), you may need to use `git filter-branch`
or BFG Repo-Cleaner to purge them from history entirely. For strategy documents and
contact names, removing from current HEAD is sufficient for now.
