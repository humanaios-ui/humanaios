# Credentials Management Protocol

**Authority:** Admiral (Carly R. Anderson)  
**Primary Location:** `~/.empirica/credentials.yaml`  
**Tracking Location:** This document (audit trail + request log)  
**Last Updated:** 2026-07-29

---

## Primary Credentials File

**Path:** `~/.empirica/credentials.yaml`

### Current Credentials (Active)

| Service | Type | Key/Token | Practice | Issued | Expires | Status |
|---------|------|-----------|----------|--------|---------|--------|
| **Cortex** | API Key | ctx_empirica_adm_933f7b9dea79f8bcfe308e7253a62078 | empirica-foundation (system) | 2026-07-01 | 2027-01-01 | ✅ Active |
| **Ntfy** | Token | tk_7b7flkwu4i689hf1hn7bigbmcvx3i | empirica-foundation (system) | 2026-07-01 | 2027-01-01 | ✅ Active |
| **Slack** | Token | xapp-1-A0BEC6SSFJS-11490327748514-... | empirica-foundation (system) | 2026-07-01 | 2027-01-01 | ✅ Active |
| **ACAT** | API Key (humanaios) | sk-acat-4dcf5d02510423072f0efcc8928ee486... | humanaios | 2026-07-29 | 2026-10-28 | ✅ Active |
| **ACAT** | API Key (autonomy) | sk-acat-5a15ec9d9ea38dfe7260528dc83547b7c... | autonomy | 2026-07-29 | 2026-10-28 | ✅ Active |

---

## Credential Request Log

### Format for Tracking

When a practice requests credentials, log it here with:
- **Date Requested:** YYYY-MM-DD
- **Requested By:** Practice name (contact)
- **Credential Type:** API key, token, bearer token, etc.
- **Use Case:** What the practice needs it for
- **Issued:** Date issued (or approved)
- **Expiration:** Date credential expires
- **Scope:** Which systems/endpoints can be accessed
- **Rotation:** When next renewal is scheduled
- **Status:** active, expired, revoked, pending

### Active Request Log

#### 1. humanaios ACAT Integration

| Field | Value |
|-------|-------|
| **Date Requested** | 2026-07-25 |
| **Requested By** | humanaios (practice lead) |
| **Credential Type** | API Key |
| **Use Case** | Phase 1 ACAT behavioral assessment pilot (10 assessments) |
| **Issued** | 2026-07-29 |
| **Key** | sk-acat-4dcf5d02510423072f0efcc8928ee486... |
| **Endpoint** | https://api.humanaios.ai/api/v1/acat/assess |
| **Expiration** | 2026-10-28 (90 days) |
| **Scope** | Read: assessment templates, Write: assessment scores + metadata |
| **Rotation** | Quarterly (next: 2026-10-28) |
| **Status** | ✅ Active |
| **Notes** | TLS 1.3, bearer token auth, Phase 1 integration LIVE |

#### 2. autonomy ACAT Integration

| Field | Value |
|-------|-------|
| **Date Requested** | 2026-07-25 |
| **Requested By** | autonomy (Track A owner) |
| **Credential Type** | API Key |
| **Use Case** | Phase 2 gates design validation (mock sessions for testing A.0.1-A.0.3) |
| **Issued** | 2026-07-29 |
| **Key** | sk-acat-5a15ec9d9ea38dfe7260528dc83547b7c... |
| **Endpoint** | https://api.humanaios.ai/api/v1/acat/assess |
| **Expiration** | 2026-10-28 (90 days) |
| **Scope** | Read: assessment templates, Write: mock assessment scores (test data only) |
| **Rotation** | Quarterly (next: 2026-10-28) |
| **Status** | ✅ Active |
| **Notes** | Separate key from humanaios (scope isolation), test data only, Phase 2 gates |

#### 3. mesh-support Infrastructure Access

| Field | Value |
|-------|-------|
| **Date Requested** | TBD |
| **Requested By** | mesh-support (infrastructure lead) |
| **Credential Type** | TBD |
| **Use Case** | TBD |
| **Issued** | TBD |
| **Expiration** | TBD |
| **Status** | ⏳ Pending |

---

## Credential Rotation Schedule

### Quarterly Rotation (90 days)

| Credential | Issued | Expires | Rotation Date | Owner | Notes |
|------------|--------|---------|---------------|-------|-------|
| ACAT (humanaios) | 2026-07-29 | 2026-10-28 | 2026-10-28 | Admiral | Issue replacement key 1 week before expiration |
| ACAT (autonomy) | 2026-07-29 | 2026-10-28 | 2026-10-28 | Admiral | Issue replacement key 1 week before expiration |

### Annual Rotation (System Credentials)

| Credential | Issued | Expires | Rotation Date | Owner | Notes |
|------------|--------|---------|---------------|-------|-------|
| Cortex | 2026-07-01 | 2027-01-01 | 2026-12-15 | Admiral | Issue replacement 2 weeks before expiration |
| Ntfy | 2026-07-01 | 2027-01-01 | 2026-12-15 | Admiral | Issue replacement 2 weeks before expiration |
| Slack | 2026-07-01 | 2027-01-01 | 2026-12-15 | Admiral | Issue replacement 2 weeks before expiration |

---

## How to Update Credentials

### Step 1: Edit the Credentials File

```bash
# Open credentials file in your editor
open ~/.empirica/credentials.yaml

# OR from command line:
nano ~/.empirica/credentials.yaml
```

### Step 2: Add New Credential

```yaml
# Add to the appropriate section
practice_name:
  api_key: "new-key-value"
  endpoint: "https://api.example.com/endpoint"
  expiration: "YYYY-MM-DD"
  rotation_schedule: "quarterly/annually"
```

### Step 3: Log the Request

Add entry to the "Credential Request Log" section above with all relevant details.

### Step 4: Commit & Track

```bash
# DON'T commit credentials file itself!
# Instead, create a record in THIS document
# Then commit the MARKDOWN file (not the .yaml)
```

---

## Security Best Practices

### DO
- ✅ Store credentials in `~/.empirica/credentials.yaml` (local, not in git)
- ✅ Rotate credentials on schedule (quarterly for ACAT, annually for system)
- ✅ Use separate keys per practice/scope (humanaios ≠ autonomy)
- ✅ Track all requests in this document
- ✅ Set expiration dates (never "no expiration")
- ✅ Review credentials monthly for unused/stale keys
- ✅ Revoke immediately if compromised

### DON'T
- ❌ Commit credentials to git (ever)
- ❌ Share credentials in Slack, email, or logs
- ❌ Use same key across multiple practices (scope isolation)
- ❌ Issue credentials without documented request
- ❌ Forget to update expiration dates
- ❌ Leave credentials unchanged for >1 year

---

## Practice Credential Requests — Template

**When a practice requests credentials, use this template:**

```
# Credential Request: [Practice Name] — [Use Case]

**Date Requested:** YYYY-MM-DD  
**Requested By:** [Practice Lead Name] ([practice-name])  
**Credential Type:** [API key / token / bearer token / etc.]  
**Use Case:** [Specific purpose — what will this access?]  
**Scope Needed:** [Read/Write/Admin — which operations?]  
**Duration:** [How long is this credential needed?]  
**Justification:** [Why this credential, why this practice?]  

**Approval:** Admiral ([date])  
**Issued:** [date]  
**Expiration:** [date]  

**Notes:** [Any special constraints or monitoring needs]
```

---

## Access Control by Practice

### humanaios
- ✅ ACAT API key (humanaios_key)
- ✅ Endpoint: https://api.humanaios.ai/api/v1/acat/assess
- ✅ Scope: Read assessment templates, Write scores + metadata
- ✅ Phase 1 integration LIVE
- ❌ NO access to: Cortex (system), Ntfy (system), Slack (system)

### autonomy
- ✅ ACAT API key (autonomy_key) — test data only
- ✅ Endpoint: https://api.humanaios.ai/api/v1/acat/assess
- ✅ Scope: Read assessment templates, Write mock scores
- ✅ Phase 2 gates design validation
- ❌ NO access to: Cortex (system), Ntfy (system), Slack (system), humanaios_key

### mesh-support
- ⏳ Pending credential request
- ✅ Access TBD (infrastructure needs)
- ❌ NO access to: ACAT keys (unless explicitly approved)

### evaluator (this seat)
- ✅ Cortex (system orchestration)
- ✅ Ntfy (listener topic: empirica-foundation-orchestration-events-carly)
- ✅ Slack (notifications)
- ✅ ACAT API keys (both — for coordination + verification)
- ✅ Full access for oversight

---

## Credential Distribution

### How to Share Credentials with a Practice

1. **Approved by Admiral?** → Get approval first
2. **Request logged?** → Add entry to "Credential Request Log" above
3. **Key generated?** → Create new key (never reuse)
4. **Scope isolated?** → Separate keys per practice
5. **Expiration set?** → Always set, never "no expiration"
6. **Distribution method?** → Use secure channel (never Slack/email)
   - Best: Cortex collab message (encrypted mesh transport)
   - Acceptable: Direct conversation, verbal confirmation
   - Never: Unencrypted email, Slack, git commit
7. **Logged in THIS document?** → Add request entry
8. **Confirmation receipt?** → Practice confirms receipt + acknowledgment

---

## Monthly Credential Audit

**Run this audit on the 1st of each month:**

| Item | Check | Status |
|------|-------|--------|
| Active credentials still needed? | Review all keys in use | ⏳ Due: 2026-08-01 |
| Any expiring soon? | Check dates vs. today | ⏳ Due: 2026-08-01 |
| Any stale/unused? | Verify each key is actively used | ⏳ Due: 2026-08-01 |
| Rotation on schedule? | Verify quarterly/annual cycle | ⏳ Due: 2026-08-01 |
| All requests logged? | Ensure this document is current | ⏳ Due: 2026-08-01 |

---

## Credential Revocation Protocol

**If a credential is compromised or no longer needed:**

1. Revoke the key immediately (don't wait for rotation cycle)
2. Log revocation in this document with date + reason
3. Notify the practice (via Cortex collab)
4. Issue replacement key if still needed
5. Commit update to THIS document (not the credentials file)

**Example:**
```
#### REVOKED: autonomy ACAT Key (OLD)

| Field | Value |
|-------|-------|
| **Date Revoked** | 2026-08-15 |
| **Reason** | Leaked in git commit (accidental) |
| **Replacement Issued** | 2026-08-15 |
| **New Key** | sk-acat-[newkey...]... |
| **Status** | ✅ Revoked, Replacement Active |
```

---

## Summary

**You now have:**
1. ✅ Primary credentials file location: `~/.empirica/credentials.yaml`
2. ✅ Tracking document: This file (centralized audit trail)
3. ✅ Request log: All credential requests documented
4. ✅ Rotation schedule: Quarterly (ACAT), Annual (system)
5. ✅ Access control matrix: Per-practice authorization
6. ✅ Distribution protocol: Secure credential sharing method
7. ✅ Monthly audit checklist: Compliance verification

**To add credentials to a practice:**
1. Admiral approves request
2. Generate new key (don't reuse)
3. Log request in this document (with expiration)
4. Share via secure channel (Cortex collab, not email/Slack)
5. Practice confirms receipt
6. Commit THIS document (markdown audit trail, not the credentials file)

---

**Authority:** Admiral (Carly R. Anderson)  
**Last Reviewed:** 2026-07-29  
**Next Review:** 2026-08-01 (monthly audit)  
**Rotation Alert:** 2026-10-15 (ACAT keys due 2026-10-28)

