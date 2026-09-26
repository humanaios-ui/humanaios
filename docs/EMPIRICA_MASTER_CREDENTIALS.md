# Empirica Master Credentials Management
**Date:** 2026-07-20  
**Authority:** Admiral (Carly R. Anderson)  
**Purpose:** How to manage workspace-level credentials, user profiles, and access control

---

## Overview

Empirica credentials operate at **three layers**:

```
┌─────────────────────────────────────────┐
│ Layer 1: WORKSPACE ENTITY REGISTRY      │  (~/.empirica/workspace/workspace.db)
│ ├─ User entities (you)                  │  Who has access?
│ ├─ Credential entities (what)           │  What credentials exist?
│ └─ Entity memberships (permissions)     │  Who can use what?
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ Layer 2: ENCRYPTED VAULT                │  (~/.empirica/workspace/secrets/)
│ ├─ .master-key                          │  AES-256 encryption key
│ └─ *.enc files                          │  Encrypted credentials
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ Layer 3: SERVICE ENVIRONMENTS           │  (Supabase Edge Function secrets, etc.)
│ ├─ GITHUB_WEBHOOK_SECRET                │  Used by Edge Functions
│ ├─ SUPABASE_* keys                      │  Service credentials
│ └─ Custom service secrets               │  Any API tokens
└─────────────────────────────────────────┘
```

---

## Layer 1: Entity Registry (SQLite Database)

**Location:** `~/.empirica/workspace/workspace.db`

### View Current Credentials

```bash
sqlite3 ~/.empirica/workspace/workspace.db << 'SQL'
-- Show all credentials
SELECT entity_id, display_name, json_extract(metadata, '$.status') as status
FROM entity_registry 
WHERE entity_type='credential'
ORDER BY entity_id;
SQL
```

### Add a New Credential Entity

```bash
sqlite3 ~/.empirica/workspace/workspace.db << 'SQL'
-- Example: Add Slack Bot Token credential
INSERT INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, 
   emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'credential',
    'cred-slack-bot',
    'Slack · Bot Token',
    'Bot token for posting governance alerts to Slack workspace',
    'workspace',
    'entity_registry',
    '🤖',
    'active',
    datetime('now'),
    datetime('now'),
    json_object(
      'service', 'slack',
      'vault_location', '~/.empirica/workspace/secrets/slack-bot-token.enc',
      'keys', json_array('SLACK_BOT_TOKEN', 'SLACK_SIGNING_SECRET'),
      'visibility', 'private',
      'status', 'pending-configuration'
    )
  );
SQL
```

### Update Credential Status

```bash
# Mark as "active" (from "pending-configuration")
sqlite3 ~/.empirica/workspace/workspace.db << 'SQL'
UPDATE entity_registry 
SET metadata = json_set(metadata, '$.status', 'active')
WHERE entity_id='cred-supabase-humanaios-witness';

-- Verify
SELECT entity_id, json_extract(metadata, '$.status') as status 
FROM entity_registry WHERE entity_type='credential';
SQL
```

### Grant Access to a Practice

```bash
sqlite3 ~/.empirica/workspace/workspace.db << 'SQL'
-- Allow empirica-autonomy to access Supabase credentials
INSERT INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '492482dc-8156-40cd-a110-ce7081212215', 'credential', 
   'cred-supabase-humanaios-witness', 'reader', 
   datetime('now'), datetime('now'), 'Cross-org mesh - Autonomy needs Witness');
SQL
```

---

## Layer 2: Encrypted Vault

**Location:** `~/.empirica/workspace/secrets/`

### View Vault Contents

```bash
ls -lah ~/.empirica/workspace/secrets/

# Expected output:
# .master-key                           (65 bytes, 600 permissions)
# supabase-humanaios-witness.enc        (720 bytes, 600 permissions)
# github-token.enc                      (256 bytes, 600 permissions)
```

### Decrypt a Credential

```bash
# Method 1: Manual decryption (for verification)
MASTER_KEY=$(cat ~/.empirica/workspace/secrets/.master-key)

openssl enc -aes-256-cbc -d -in ~/.empirica/workspace/secrets/supabase-humanaios-witness.enc \
  -pass pass:"$MASTER_KEY" -md sha256 | jq '.'

# Method 2: Using credential-sync script (recommended)
./scripts/credential-sync.sh show supabase
```

### Add a New Encrypted Credential

```bash
# Method 1: Automated via script
./scripts/credential-sync.sh encrypt-and-store slack '{"SLACK_BOT_TOKEN": "xoxb-...", "SLACK_SIGNING_SECRET": "..."}'

# Method 2: Manual encryption
MASTER_KEY=$(cat ~/.empirica/workspace/secrets/.master-key)

# Create JSON credential file
cat > /tmp/slack-creds.json << 'EOF'
{
  "service": "slack",
  "credentials": {
    "SLACK_BOT_TOKEN": "xoxb-...",
    "SLACK_SIGNING_SECRET": "..."
  },
  "created_at": "2026-07-20T00:00:00Z",
  "encrypted": true
}
EOF

# Encrypt and store
cat /tmp/slack-creds.json | openssl enc -aes-256-cbc -salt \
  -out ~/.empirica/workspace/secrets/slack-bot-token.enc \
  -pass pass:"$MASTER_KEY" -md sha256

chmod 600 ~/.empirica/workspace/secrets/slack-bot-token.enc
rm /tmp/slack-creds.json
```

### Protect the Master Key

```bash
# Verify permissions (must be 600)
ls -l ~/.empirica/workspace/secrets/.master-key
# Expected: -rw------- (600)

# Back up to secure location
# Option 1: Password manager (1Password, Bitwarden)
# Option 2: Hardware key (Yubikey, encrypted USB)
# Option 3: Encrypted cloud storage (Tresorit)

# NEVER commit to git
echo ".empirica/workspace/secrets/" >> ~/.gitignore
```

---

## Layer 3: Service Environments

### Set Secrets in Supabase Edge Function

**Option 1: Via Credential Sync Script (Recommended)**

```bash
./scripts/credential-sync.sh set-secret GITHUB_WEBHOOK_SECRET "your-secret-here"
```

**Option 2: Via Supabase CLI**

```bash
# First, load credentials from vault
MASTER_KEY=$(cat ~/.empirica/workspace/secrets/.master-key)
CREDS=$(openssl enc -aes-256-cbc -d -in ~/.empirica/workspace/secrets/supabase-humanaios-witness.enc \
  -pass pass:"$MASTER_KEY" -md sha256)

SUPABASE_URL=$(echo "$CREDS" | jq -r '.credentials.SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY=$(echo "$CREDS" | jq -r '.credentials.SUPABASE_SERVICE_ROLE_KEY')

# Then set secret
supabase secrets set GITHUB_WEBHOOK_SECRET="your-secret-here" \
  --project-ref ksinisdzgtnqzsymhfya
```

### List Secrets in Supabase

```bash
supabase secrets list --project-ref ksinisdzgtnqzsymhfya
```

---

## Complete Workflow: Add a New Credential

**Example: Add Slack Bot Token for Governance Alerts**

### Step 1: Get the credential value

```bash
# From Slack workspace → Settings → Install app
# Copy the Bot User OAuth Token (starts with xoxb-)
```

### Step 2: Add to entity registry

```bash
sqlite3 ~/.empirica/workspace/workspace.db << 'SQL'
INSERT INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, 
   emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'credential',
    'cred-slack-bot-token',
    'Slack · Bot Token for Governance Alerts',
    'Posts governance decisions and alerts to Slack #governance channel',
    'workspace',
    'entity_registry',
    '🤖',
    'active',
    datetime('now'),
    datetime('now'),
    json_object(
      'service', 'slack',
      'vault_location', '~/.empirica/workspace/secrets/slack-bot-token.enc',
      'keys', json_array('SLACK_BOT_TOKEN'),
      'visibility', 'private',
      'status', 'active'
    )
  );
SQL
```

### Step 3: Encrypt and store in vault

```bash
./scripts/credential-sync.sh encrypt-and-store slack '{"SLACK_BOT_TOKEN": "xoxb-..."}'
```

### Step 4: Set in Supabase Edge Function (if needed)

```bash
./scripts/credential-sync.sh set-secret SLACK_BOT_TOKEN "xoxb-..."
```

### Step 5: Grant access to a practice

```bash
sqlite3 ~/.empirica/workspace/workspace.db << 'SQL'
INSERT INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '428902a7-19dd-4598-b655-51a4a689934f', 'credential', 
   'cred-slack-bot-token', 'reader', 
   datetime('now'), datetime('now'), 'For posting governance alerts');
SQL
```

---

## Troubleshooting

### Master Key Lost

```bash
# If .master-key is lost, all encrypted credentials are unrecoverable
# Recovery steps:
# 1. Ask Admiral for fresh API keys from each service
# 2. Generate new master key:
openssl rand -hex 32 > ~/.empirica/workspace/secrets/.master-key
chmod 600 ~/.empirica/workspace/secrets/.master-key
# 3. Re-encrypt all credentials with new master key
# 4. Back up new master key to secure location
```

### Cannot Decrypt Credential

```bash
# Verify master key exists
ls -la ~/.empirica/workspace/secrets/.master-key

# Verify encrypted file exists
ls -la ~/.empirica/workspace/secrets/*.enc

# Test decryption manually
MASTER_KEY=$(cat ~/.empirica/workspace/secrets/.master-key)
openssl enc -aes-256-cbc -d -in ~/.empirica/workspace/secrets/supabase-humanaios-witness.enc \
  -pass pass:"$MASTER_KEY" -md sha256 | jq .
```

### Script Permission Denied

```bash
# Ensure scripts are executable
chmod +x scripts/credential-sync.sh
chmod +x scripts/manage-supabase-secrets.sh

# Re-run
./scripts/credential-sync.sh show supabase
```

---

## Security Checklist

- [ ] Master key backed up to password manager or hardware key
- [ ] `.empirica/workspace/secrets/` in `.gitignore`
- [ ] No .enc files committed to git
- [ ] All .enc files have 600 permissions
- [ ] Master key has 600 permissions
- [ ] Credentials rotated every 90 days
- [ ] Access control (memberships) reviewed monthly
- [ ] Unused credentials archived or deleted

---

## Related Documentation

- **Workspace Source of Truth:** `docs/WORKSPACE_SOURCE_OF_TRUTH.md`
- **Credential Sync Script:** `scripts/credential-sync.sh`
- **Supabase Integration:** `docs/SUPABASE_WITNESS_INTEGRATION.md`

---

**Last Updated:** 2026-07-20  
**Authority:** Admiral (Carly R. Anderson)  
**Visibility:** Private (empirica-foundation-evaluator only)
