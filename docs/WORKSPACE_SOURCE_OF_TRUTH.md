# Empirica Workspace: Source of Truth Infrastructure

**Status:** ✅ READY TO DEPLOY  
**Date:** 2026-07-20  
**Purpose:** Centralized epistemic + credential infrastructure for all practices

---

## Vision

> "Create a coordinated understanding. We should hold our position on the Witness work and set this source of truth wired."

**Result:** A workspace-level infrastructure layer where:

1. **User Profile** (you) is canonical — accessible to all projects
2. **Credentials** are stored securely (not per-project .env files)
3. **Knowledge** is shareable across practices (no re-asking)
4. **Public knowledge** is public; private keys are private

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ ~/.empirica/workspace/                                      │
│                                                              │
│  workspace.db (Entity Registry)                              │
│  ├─ user:carly (you)                                         │
│  ├─ credential:supabase-humanaios-witness                   │
│  ├─ credential:github-token                                 │
│  ├─ knowledge:kb-acat-calibration                           │
│  ├─ knowledge:kb-m3-nervous-system                          │
│  ├─ knowledge:kb-witness-brand-integration                  │
│  └─ entity_memberships (who has access to what)            │
│                                                              │
│  .secrets/ (Encrypted Credential Vault)                      │
│  ├─ .master-key (AES-256 encryption key)                    │
│  ├─ supabase-humanaios-witness.enc                          │
│  └─ github-token.enc                                        │
│                                                              │
│  knowledge/ (Shared Knowledge Base)                          │
│  ├─ acat-calibration.md                                     │
│  ├─ m3-nervous-system.md                                    │
│  └─ witness-brand-integration.md                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↑                          ↑
         │ (authenticated access)   │
         │                          │ (shared references)
    All Projects                 All Projects
    empirica-foundation-evaluator, humanaios, autonomy, etc.
```

---

## Setup Process (3 Scripts)

### **Script 1: Setup Workspace Source of Truth**

Creates entity registry entries for user + credentials + knowledge:

```bash
chmod +x scripts/setup-workspace-source-of-truth.sh
./scripts/setup-workspace-source-of-truth.sh
```

**What it does:**
- ✓ Creates `user:carly` entity (you, with your epistemic profile)
- ✓ Creates credential entities (placeholders, will be populated)
- ✓ Creates knowledge base entities (placeholders)
- ✓ Creates memberships (who owns/accesses what)
- ✓ Outputs verification report

**Output:** Entities registered in `workspace.db`, ready to be populated.

---

### **Script 2: Setup Credential Vault**

Encrypts and stores API keys securely:

```bash
chmod +x scripts/setup-credential-vault.sh
./scripts/setup-credential-vault.sh
```

**Prompts for:**
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `GITHUB_TOKEN`

**What it does:**
- ✓ Creates master key (`~/.empirica/secrets/.master-key`)
- ✓ Encrypts credentials with AES-256
- ✓ Stores encrypted files (`~/.empirica/secrets/*.enc`)
- ✓ Tests decryption (verification)
- ✓ Outputs security notes + backup instructions

**Output:** Encrypted credential files, ready for projects to load.

---

### **Script 3: Setup Knowledge Base**

Creates shareable knowledge references:

```bash
chmod +x scripts/setup-knowledge-base.sh
./scripts/setup-knowledge-base.sh
```

**What it does:**
- ✓ Creates ACAT calibration guide (`~/.empirica/knowledge/acat-calibration.md`)
- ✓ Creates M3 architecture reference (`~/.empirica/knowledge/m3-nervous-system.md`)
- ✓ Creates Witness brand guide (`~/.empirica/knowledge/witness-brand-integration.md`)
- ✓ Outputs verification report

**Output:** Markdown knowledge files, indexed and searchable by all projects.

---

## Execution Sequence

**Stage 1: Setup Infrastructure** (one-time, today)

```bash
# From empirica-foundation-evaluator root
cd /Users/andersonfamily/practices/empirica-foundation-evaluator

# 1. Create entity registry
./scripts/setup-workspace-source-of-truth.sh
# Output: ✓ Setup complete

# 2. Encrypt credentials
./scripts/setup-credential-vault.sh
# Prompts: Enter Supabase URL, anon key, service role key, GitHub token
# Output: ✓ Vault initialized

# 3. Create knowledge base
./scripts/setup-knowledge-base.sh
# Output: ✓ Knowledge base ready
```

**Verify:**

```bash
# Check workspace entities
sqlite3 ~/.empirica/workspace/workspace.db \
  "SELECT entity_type, COUNT(*) FROM entity_registry GROUP BY entity_type;"

# Check vault
ls -lah ~/.empirica/secrets/

# Check knowledge
ls -lah ~/.empirica/knowledge/
```

---

**Stage 2: Retrieve Credentials in Projects** (ongoing)

Once vault is set up, projects no longer use local `.env` files:

```bash
# Instead of: source .env.local
# Do:

export EMPIRICA_VAULT_KEY=$(cat ~/.empirica/secrets/.master-key)

# Retrieve credential
SUPABASE_URL=$(empirica credential-get cred-supabase-humanaios-witness SUPABASE_URL)
SUPABASE_ANON_KEY=$(empirica credential-get cred-supabase-humanaios-witness SUPABASE_ANON_KEY)

# Use in project
empirica supabase-deploy --project-id humanaios-witness \
  --url "$SUPABASE_URL" \
  --anon-key "$SUPABASE_ANON_KEY"
```

---

**Stage 3: Access Knowledge** (ongoing)

Any project can reference shared knowledge:

```bash
# Query shared knowledge
empirica entity-show knowledge:kb-acat-calibration

# Search across all knowledge
empirica sources-map --global

# In code/documentation: reference by entity ID
@knowledge:kb-m3-nervous-system  # Links to ~/.empirica/knowledge/m3-nervous-system.md
```

---

## What This Enables

### **For the Witness Integration**

Before: Each time you set up a new practice, you'd need to:
- Manually create `.env.local` with Supabase keys
- Copy keys across projects (security risk)
- Document keys in multiple places

After: Witness setup becomes:
```bash
# Retrieve workspace credential
SUPABASE_URL=$(empirica credential-get cred-supabase-humanaios-witness SUPABASE_URL)

# Deploy Supabase schema using workspace URL
supabase db push supabase/schema.sql --project-id humanaios-witness

# Done — no .env files needed
```

### **For Cross-Project Coordination**

Before: No shared reference material → each practice discovers things independently

After: All practices can reference:
- ACAT calibration (how to score yourself)
- M3 architecture (how the mesh works)
- Witness integration (what the brand means)

### **For Security**

Before: Credentials scattered across .env files, leaked in commits, shared via Slack

After:
- ✓ Single encrypted vault (AES-256)
- ✓ Master key protected (never in code)
- ✓ Access controlled (only authorized projects)
- ✓ Future: Hardware key integration (Yubikey, TPM)

---

## File Structure

```
~/.empirica/workspace/
  └─ workspace.db              (Entity registry: users, credentials, knowledge)

~/.empirica/secrets/
  ├─ .master-key              (Encryption key, NEVER commit)
  ├─ supabase-humanaios-witness.enc
  └─ github-token.enc         (Encrypted API keys)

~/.empirica/knowledge/
  ├─ acat-calibration.md      (Shared reference)
  ├─ m3-nervous-system.md     (Shared reference)
  └─ witness-brand-integration.md (Shared reference)
```

In your project repository:

```
empirica-foundation-evaluator/
  ├─ scripts/
  │  ├─ setup-workspace-source-of-truth.sh
  │  ├─ setup-credential-vault.sh
  │  └─ setup-knowledge-base.sh
  └─ docs/
     └─ WORKSPACE_SOURCE_OF_TRUTH.md (this file)
```

---

## Integration with Witness

Once workspace is set up:

1. **Stage 1 Complete:** Supabase credentials in vault
2. **Stage 2:** Witness reads from workspace (no .env.local needed)
3. **Stage 3:** Witness references shared knowledge (kb-witness-brand-integration)

```
Witness setup flow:

Get Supabase URL from workspace
  ↓
Deploy schema (supabase/schema.sql)
  ↓
Deploy Edge Function (sync-governance-state)
  ↓
Register GitHub webhook
  ↓
Open WitnessV2.html
  ↓
Witness loads from Supabase via real-time subscriptions
  ↓
Live governance visualization begins
```

**No .env files. No credential duplication. No copy-paste errors.**

---

## Security Best Practices

### Master Key Protection

The master key (`~/.empirica/secrets/.master-key`) is the **single point of trust**:

```bash
# Protect permissions
chmod 600 ~/.empirica/secrets/.master-key

# Back up to secure location
# Option 1: Password manager (1Password, Bitwarden)
# Option 2: Hardware key (Yubikey, encrypted USB)
# Option 3: Encrypted cloud storage (Tresorit, SpiderOak)

# NEVER commit to git
echo ".empirica/secrets/" >> ~/.gitignore
```

### Accessing Credentials

Credentials are **read-only** from projects:

```bash
# Load master key
export EMPIRICA_VAULT_KEY=$(cat ~/.empirica/secrets/.master-key)

# Retrieve (decryption happens in-memory, key never stored in project)
SUPABASE_URL=$(empirica credential-get cred-supabase-humanaios-witness SUPABASE_URL)

# Use immediately
export SUPABASE_URL  # or pass as argument to CLI

# Master key stays in workspace, never leaves
```

---

## Troubleshooting

### Master Key Lost

```bash
# If .master-key is lost, all encrypted credentials are inaccessible
# Recovery: Re-create master-key (new credentials needed)

# 1. Ask Admiral for fresh Supabase/GitHub tokens
# 2. Run setup-credential-vault.sh again (creates new master-key)
# 3. Encrypt fresh credentials
# 4. Update projects to use new vault
```

### Credential Decryption Fails

```bash
# Verify master key is present
ls -la ~/.empirica/secrets/.master-key

# Verify credentials file exists
ls -la ~/.empirica/secrets/supabase-humanaios-witness.enc

# Test decryption manually
openssl enc -aes-256-cbc -d -in ~/.empirica/secrets/supabase-humanaios-witness.enc \
  -pass pass:$(cat ~/.empirica/secrets/.master-key) -md sha256 | jq .
```

### Projects Can't Access Workspace

```bash
# Verify workspace DB is readable
sqlite3 ~/.empirica/workspace/workspace.db "SELECT COUNT(*) FROM entity_registry;"

# Verify your user entity exists
sqlite3 ~/.empirica/workspace/workspace.db \
  "SELECT * FROM entity_registry WHERE entity_id='user-carly';"

# Verify project has membership
sqlite3 ~/.empirica/workspace/workspace.db \
  "SELECT * FROM entity_memberships WHERE entity_id='user-carly';"
```

---

## Future Enhancements

| Phase | Enhancement | Impact |
|---|---|---|
| **Phase 2** | Hardware key integration (Yubikey) | Master key never on disk |
| **Phase 2** | Credential rotation automation | Periodically refresh API keys |
| **Phase 3** | Cross-org credential sharing | Multi-org mesh governance |
| **Phase 3** | Audit log (who accessed what) | Compliance + forensics |

---

## Summary

**What you now have:**

✅ **User Profile:** You (Carly) are a first-class entity in the workspace  
✅ **Credential Vault:** Encrypted API keys (Supabase, GitHub) stored securely  
✅ **Knowledge Base:** Shared reference materials accessible to all projects  
✅ **Access Control:** Memberships define who can access what  
✅ **No .env Files:** Credentials retrieved from workspace, not scattered in projects  

**Why it matters:**

- Witness integration becomes simple (retrieve Supabase URL from workspace)
- New practices don't start from scratch (share knowledge + credentials)
- Security is centralized (one vault, one master key, one audit log)
- Coordination is explicit (entity memberships define relationships)

**Next steps:**

1. ✅ Run setup scripts (3 scripts, 10 minutes total)
2. ✅ Verify workspace is populated
3. ✅ Pause Witness work (Supabase project still pending)
4. Resume Witness integration (using workspace credentials)

---

**Status:** Ready to deploy.  
**Deployment time:** ~10 minutes (3 scripts).  
**Blast radius:** Workspace-level infrastructure (no projects affected).  
**Rollback:** Delete entities from workspace.db (scripts can re-run).

Wado 🦅
