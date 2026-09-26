#!/bin/bash
# Workspace Source of Truth Setup
# Purpose: Create user + credential + knowledge entities in workspace.db
# Status: Script-driven (no manual entity-create calls required)
# Date: 2026-07-20

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Empirica Workspace Source of Truth Setup                      ║"
echo "║ Creating: User Profile + Credential Vault + Knowledge Base    ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Configuration
WORKSPACE_DB="${HOME}/.empirica/workspace/workspace.db"
TIMESTAMP=$(date +%s)
CREDENTIAL_VAULT="${HOME}/.empirica/secrets"
KNOWLEDGE_BASE="${HOME}/.empirica/knowledge"

# Verify workspace exists
if [ ! -f "$WORKSPACE_DB" ]; then
    echo "❌ Error: workspace.db not found at $WORKSPACE_DB"
    exit 1
fi

echo "✓ Workspace found: $WORKSPACE_DB"

# Create vault directories
mkdir -p "$CREDENTIAL_VAULT"
mkdir -p "$KNOWLEDGE_BASE"
echo "✓ Vault directories created: $CREDENTIAL_VAULT"

# ─────────────────────────────────────────────────────────────────
# STEP 1: Create User Entity (Carly)
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 1: Creating user entity (Carly R. Anderson)..."

sqlite3 "$WORKSPACE_DB" << SQL
INSERT OR REPLACE INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'user',
    'user-carly',
    'Carly R. Anderson',
    'Admiral, empirica-foundation BDFL. Epistemic profile: calibration trajectory for mesh-wide decisions.',
    'workspace',
    'entity_registry',
    '👁️',
    'active',
    $TIMESTAMP,
    $TIMESTAMP,
    json_object(
      'role', 'admiral',
      'org', 'empirica-foundation',
      'practices_owned', json_array('empirica-foundation-evaluator', 'humanaios', 'empirica-autonomy'),
      'epistemic_profile', json_object(
        'know', 0.88,
        'do', 0.92,
        'context', 0.85,
        'clarity', 0.87,
        'coherence', 0.89,
        'signal', 0.86
      ),
      'portfolio', json_array(
        'empirica-foundation-evaluator',
        'humanaios',
        'empirica-autonomy'
      )
    )
  );
SQL

echo "✓ User entity created: user-carly"

# ─────────────────────────────────────────────────────────────────
# STEP 2: Create Credential Entities
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 2: Creating credential entities..."

# 2a. Supabase Witness Credentials
sqlite3 "$WORKSPACE_DB" << SQL
INSERT OR REPLACE INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'credential',
    'cred-supabase-humanaios-witness',
    'Supabase · humanaios-witness',
    'API credentials for HUMANAIOS Witness real-time dashboard (Supabase PostgreSQL)',
    'workspace',
    'entity_registry',
    '🔑',
    'active',
    $TIMESTAMP,
    $TIMESTAMP,
    json_object(
      'service', 'supabase',
      'project_name', 'humanaios-witness',
      'vault_location', '$CREDENTIAL_VAULT/supabase-humanaios-witness.enc',
      'keys', json_array(
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY'
      ),
      'visibility', 'private',
      'access_control', json_array('user-carly', 'project:empirica-foundation-evaluator'),
      'status', 'pending-configuration'
    )
  );
SQL

echo "✓ Credential entity created: cred-supabase-humanaios-witness"

# 2b. GitHub Token
sqlite3 "$WORKSPACE_DB" << SQL
INSERT OR REPLACE INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'credential',
    'cred-github-token',
    'GitHub · Personal Access Token',
    'GitHub API token for webhook registration and repo management',
    'workspace',
    'entity_registry',
    '🔑',
    'active',
    $TIMESTAMP,
    $TIMESTAMP,
    json_object(
      'service', 'github',
      'vault_location', '$CREDENTIAL_VAULT/github-token.enc',
      'keys', json_array('GITHUB_TOKEN'),
      'visibility', 'private',
      'access_control', json_array('user-carly'),
      'status', 'pending-configuration'
    )
  );
SQL

echo "✓ Credential entity created: cred-github-token"

# ─────────────────────────────────────────────────────────────────
# STEP 3: Create Knowledge Base Entities
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 3: Creating knowledge base entities..."

# 3a. ACAT Calibration Knowledge
sqlite3 "$WORKSPACE_DB" << SQL
INSERT OR REPLACE INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'knowledge',
    'kb-acat-calibration',
    'ACAT Dimension Calibration Guide',
    'Cross-practice reference: how to calibrate the 6 epistemic dimensions (know, do, context, clarity, coherence, signal)',
    'workspace',
    'entity_registry',
    '📚',
    'active',
    $TIMESTAMP,
    $TIMESTAMP,
    json_object(
      'category', 'calibration',
      'domain', 'empirica',
      'visibility', 'shared',
      'source', '$KNOWLEDGE_BASE/acat-calibration.md',
      'indexed', true,
      'tags', json_array('acat', 'calibration', 'epistemic-vector', 'foundation'),
      'access_level', 'public-read'
    )
  );
SQL

echo "✓ Knowledge entity created: kb-acat-calibration"

# 3b. M3 Nervous System Architecture
sqlite3 "$WORKSPACE_DB" << SQL
INSERT OR REPLACE INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'knowledge',
    'kb-m3-nervous-system',
    'M3 Nervous System Architecture',
    'Cross-practice reference: M3 ranks (Batch Sync, Divergence Detection, State Validation) and integration patterns',
    'workspace',
    'entity_registry',
    '🧠',
    'active',
    $TIMESTAMP,
    $TIMESTAMP,
    json_object(
      'category', 'architecture',
      'domain', 'governance',
      'visibility', 'shared',
      'source', '$KNOWLEDGE_BASE/m3-nervous-system.md',
      'indexed', true,
      'tags', json_array('m3', 'mesh', 'governance', 'nervous-system', 'foundation'),
      'access_level', 'public-read'
    )
  );
SQL

echo "✓ Knowledge entity created: kb-m3-nervous-system"

# 3c. Witness Brand Integration
sqlite3 "$WORKSPACE_DB" << SQL
INSERT OR REPLACE INTO entity_registry
  (entity_type, entity_id, display_name, description, source_db, source_table, emoji_state, status, created_at, updated_at, metadata)
VALUES
  (
    'knowledge',
    'kb-witness-brand-integration',
    'HUMANAIOS Witness Brand Integration',
    'Cross-practice reference: The Witness as live observability glyph, visual mappings, real-time data sources',
    'workspace',
    'entity_registry',
    '👁️',
    'active',
    $TIMESTAMP,
    $TIMESTAMP,
    json_object(
      'category', 'brand',
      'domain', 'empirica',
      'visibility', 'shared',
      'source', '$KNOWLEDGE_BASE/witness-brand-integration.md',
      'indexed', true,
      'tags', json_array('witness', 'brand', 'observability', 'humanaios', 'foundation'),
      'access_level', 'public-read'
    )
  );
SQL

echo "✓ Knowledge entity created: kb-witness-brand-integration"

# ─────────────────────────────────────────────────────────────────
# STEP 4: Create Memberships (Relations)
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 4: Creating entity memberships (relations)..."

# 4a. User → Projects (ownership)
sqlite3 "$WORKSPACE_DB" << SQL
-- Carly owns empirica-foundation-evaluator
INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('user', 'user-carly', 'project', '428902a7-19dd-4598-b655-51a4a689934f', 'owner', $TIMESTAMP, $TIMESTAMP, 'Admiral seat');

-- Carly owns humanaios
INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('user', 'user-carly', 'project', '72b1e100-aa2b-4cfe-97e9-345eb23b964a', 'owner', $TIMESTAMP, $TIMESTAMP, 'Primary practice');

-- Carly owns empirica-autonomy
INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('user', 'user-carly', 'project', '492482dc-8156-40cd-a110-ce7081212215', 'collaborator', $TIMESTAMP, $TIMESTAMP, 'Cross-org mesh');
SQL

echo "✓ Memberships created: user-carly → [projects]"

# 4b. Project → Credentials (access control)
sqlite3 "$WORKSPACE_DB" << SQL
-- empirica-foundation-evaluator has access to supabase credentials
INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '428902a7-19dd-4598-b655-51a4a689934f', 'credential', 'cred-supabase-humanaios-witness', 'reader', $TIMESTAMP, $TIMESTAMP, 'Witness integration');

-- empirica-foundation-evaluator has access to github token
INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '428902a7-19dd-4598-b655-51a4a689934f', 'credential', 'cred-github-token', 'reader', $TIMESTAMP, $TIMESTAMP, 'Webhook registration');
SQL

echo "✓ Memberships created: projects → [credentials]"

# 4c. Project → Knowledge (reference access)
sqlite3 "$WORKSPACE_DB" << SQL
-- All projects can reference shared knowledge
INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '428902a7-19dd-4598-b655-51a4a689934f', 'knowledge', 'kb-acat-calibration', 'reader', $TIMESTAMP, $TIMESTAMP, 'Shared reference');

INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '428902a7-19dd-4598-b655-51a4a689934f', 'knowledge', 'kb-m3-nervous-system', 'reader', $TIMESTAMP, $TIMESTAMP, 'Shared reference');

INSERT OR REPLACE INTO entity_memberships
  (entity_type, entity_id, group_type, group_id, role, joined_at, created_at, notes)
VALUES
  ('project', '428902a7-19dd-4598-b655-51a4a689934f', 'knowledge', 'kb-witness-brand-integration', 'reader', $TIMESTAMP, $TIMESTAMP, 'Shared reference');
SQL

echo "✓ Memberships created: projects → [knowledge]"

# ─────────────────────────────────────────────────────────────────
# STEP 5: Verification
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 5: Verification..."

echo ""
echo "User entities:"
sqlite3 "$WORKSPACE_DB" "SELECT entity_type, entity_id, display_name FROM entity_registry WHERE entity_type='user';"

echo ""
echo "Credential entities:"
sqlite3 "$WORKSPACE_DB" "SELECT entity_type, entity_id, display_name FROM entity_registry WHERE entity_type='credential';"

echo ""
echo "Knowledge entities:"
sqlite3 "$WORKSPACE_DB" "SELECT entity_type, entity_id, display_name FROM entity_registry WHERE entity_type='knowledge';"

echo ""
echo "New memberships:"
sqlite3 "$WORKSPACE_DB" "SELECT COUNT(*) as membership_count FROM entity_memberships WHERE created_at >= $((TIMESTAMP - 10));"

# ─────────────────────────────────────────────────────────────────
# STEP 6: Next Steps
# ─────────────────────────────────────────────────────────────────

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ ✅ Workspace Source of Truth Initialized                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "📋 Next Steps:"
echo ""
echo "1. POPULATE CREDENTIAL VAULT"
echo "   Create encrypted credential files:"
echo "   - $CREDENTIAL_VAULT/supabase-humanaios-witness.enc"
echo "   - $CREDENTIAL_VAULT/github-token.enc"
echo ""
echo "2. POPULATE KNOWLEDGE BASE"
echo "   Create markdown files:"
echo "   - $KNOWLEDGE_BASE/acat-calibration.md"
echo "   - $KNOWLEDGE_BASE/m3-nervous-system.md"
echo "   - $KNOWLEDGE_BASE/witness-brand-integration.md"
echo ""
echo "3. UPDATE PROJECT CONFIGS"
echo "   Modify each project's .empirica/project.yaml to reference workspace credentials:"
echo "   supabase_credential_id: cred-supabase-humanaios-witness"
echo ""
echo "4. VERIFY CROSS-PROJECT ACCESS"
echo "   $ empirica entity-walk project:empirica-foundation-evaluator --type credential"
echo "   Should return: cred-supabase-humanaios-witness, cred-github-token"
echo ""
echo "5. RESUME WITNESS INTEGRATION"
echo "   Once credentials are in vault, run witness setup with:"
echo "   $ empirica entity-show credential:cred-supabase-humanaios-witness"
echo ""

echo "✓ Setup complete. Workspace is now source of truth."
