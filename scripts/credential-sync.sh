#!/bin/bash
# Credential Sync Manager
# Purpose: Sync credentials from workspace vault → Supabase Edge Function secrets
# Usage: ./scripts/credential-sync.sh <sync|show|add> [options]
# Date: 2026-07-20

set -e

VAULT_DIR="${HOME}/.empirica/workspace/secrets"
MASTER_KEY_FILE="${VAULT_DIR}/.master-key"
SUPABASE_URL="https://ksinisdzgtnqzsymhfya.supabase.co"
SUPABASE_PROJECT_ID="ksinisdzgtnqzsymhfya"

# ─────────────────────────────────────────────────────────────────
# Helper: Decrypt credential file
# ─────────────────────────────────────────────────────────────────

decrypt_credential() {
    local cred_file=$1

    if [ ! -f "$MASTER_KEY_FILE" ]; then
        echo "❌ Master key not found: $MASTER_KEY_FILE"
        exit 1
    fi

    MASTER_KEY=$(cat "$MASTER_KEY_FILE")

    if [ ! -f "$cred_file" ]; then
        echo "❌ Credential file not found: $cred_file"
        exit 1
    fi

    openssl enc -aes-256-cbc -d -in "$cred_file" \
        -pass pass:"$MASTER_KEY" -md sha256 2>/dev/null
}

# ─────────────────────────────────────────────────────────────────
# Helper: Extract JSON field from credential
# ─────────────────────────────────────────────────────────────────

extract_field() {
    local json=$1
    local field_path=$2

    echo "$json" | jq -r "$field_path" 2>/dev/null
}

# ─────────────────────────────────────────────────────────────────
# Command: show <credential-name>
# Show decrypted credentials from vault (for verification only)
# ─────────────────────────────────────────────────────────────────

cmd_show() {
    local cred_name=$1

    case "$cred_name" in
        supabase)
            echo "🔓 Decrypting: supabase-humanaios-witness.enc"
            CREDS=$(decrypt_credential "$VAULT_DIR/supabase-humanaios-witness.enc")
            echo ""
            echo "=== SUPABASE CREDENTIALS ==="
            echo "$CREDS" | jq '.credentials'
            ;;
        github)
            echo "🔓 Decrypting: github-token.enc"
            CREDS=$(decrypt_credential "$VAULT_DIR/github-token.enc")
            echo ""
            echo "=== GITHUB CREDENTIALS ==="
            echo "$CREDS" | jq '.credentials'
            ;;
        *)
            echo "❌ Unknown credential: $cred_name"
            echo "Available: supabase, github"
            exit 1
            ;;
    esac
}

# ─────────────────────────────────────────────────────────────────
# Command: set-secret <SECRET_NAME> <SECRET_VALUE>
# Set a secret in Supabase Edge Function
# ─────────────────────────────────────────────────────────────────

cmd_set_secret() {
    local secret_name=$1
    local secret_value=$2

    if [ -z "$secret_name" ] || [ -z "$secret_value" ]; then
        echo "❌ Usage: $0 set-secret <SECRET_NAME> <SECRET_VALUE>"
        exit 1
    fi

    echo "🔐 Loading Supabase credentials from vault..."
    SUPABASE_CREDS=$(decrypt_credential "$VAULT_DIR/supabase-humanaios-witness.enc")
    SUPABASE_SERVICE_ROLE_KEY=$(extract_field "$SUPABASE_CREDS" '.credentials.SUPABASE_SERVICE_ROLE_KEY')

    echo "📝 Setting secret in Edge Function: $secret_name"

    # Use curl to set the secret via Supabase REST API
    curl -s -X POST \
        "$SUPABASE_URL/rest/v1/rpc/set_secret" \
        -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"secret_name\": \"$secret_name\", \"secret_value\": \"$secret_value\"}" \
        2>/dev/null || {
        # Fallback: use supabase CLI if API fails
        echo "Note: Using Supabase CLI for secret management"
        echo "Requires: npm install -g @supabase/cli"
        echo ""
        echo "Command: supabase secrets set $secret_name='$secret_value' --project-ref $SUPABASE_PROJECT_ID"
        exit 1
    }

    echo "✅ Secret '$secret_name' updated in Supabase"
}

# ─────────────────────────────────────────────────────────────────
# Command: sync-supabase-secrets
# Sync all Supabase secrets from vault to Edge Function
# ─────────────────────────────────────────────────────────────────

cmd_sync_supabase() {
    echo "🔓 Decrypting Supabase credentials from vault..."
    SUPABASE_CREDS=$(decrypt_credential "$VAULT_DIR/supabase-humanaios-witness.enc")

    SUPABASE_URL_VAL=$(extract_field "$SUPABASE_CREDS" '.credentials.SUPABASE_URL')
    SUPABASE_ANON_KEY=$(extract_field "$SUPABASE_CREDS" '.credentials.SUPABASE_ANON_KEY')
    SUPABASE_SERVICE_ROLE_KEY=$(extract_field "$SUPABASE_CREDS" '.credentials.SUPABASE_SERVICE_ROLE_KEY')

    echo ""
    echo "📋 Supabase secrets to sync:"
    echo "  - SUPABASE_URL: ${SUPABASE_URL_VAL:0:40}..."
    echo "  - SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY:0:40}..."
    echo "  - SUPABASE_SERVICE_ROLE_KEY: ${SUPABASE_SERVICE_ROLE_KEY:0:40}..."
    echo ""
    echo "To sync these to Supabase Edge Function, use:"
    echo ""
    echo "  supabase secrets set \\"
    echo "    SUPABASE_URL='$SUPABASE_URL_VAL' \\"
    echo "    SUPABASE_ANON_KEY='$SUPABASE_ANON_KEY' \\"
    echo "    SUPABASE_SERVICE_ROLE_KEY='$SUPABASE_SERVICE_ROLE_KEY' \\"
    echo "    --project-ref $SUPABASE_PROJECT_ID"
    echo ""
    echo "Or via this script:"
    echo "  $0 set-secret SUPABASE_URL '$SUPABASE_URL_VAL'"
    echo "  $0 set-secret SUPABASE_ANON_KEY '$SUPABASE_ANON_KEY'"
    echo "  $0 set-secret SUPABASE_SERVICE_ROLE_KEY '$SUPABASE_SERVICE_ROLE_KEY'"
}

# ─────────────────────────────────────────────────────────────────
# Command: encrypt-and-store <SERVICE> <JSON-CREDENTIALS>
# Add a new credential to the vault
# ─────────────────────────────────────────────────────────────────

cmd_encrypt() {
    local service=$1
    local cred_json=$2

    if [ -z "$service" ] || [ -z "$cred_json" ]; then
        echo "❌ Usage: $0 encrypt-and-store <SERVICE> '<JSON>'"
        echo ""
        echo "Example:"
        echo "  $0 encrypt-and-store slack '{\"SLACK_BOT_TOKEN\": \"xoxb-...\"}'"
        exit 1
    fi

    MASTER_KEY=$(cat "$MASTER_KEY_FILE")
    OUTPUT_FILE="$VAULT_DIR/${service}-credentials.enc"

    FULL_JSON=$(cat <<EOF
{
  "service": "$service",
  "credentials": $cred_json,
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "encrypted": true
}
EOF
)

    echo "$FULL_JSON" | openssl enc -aes-256-cbc -salt -out "$OUTPUT_FILE" \
        -pass pass:"$MASTER_KEY" -md sha256

    chmod 600 "$OUTPUT_FILE"

    echo "✅ Encrypted credential stored: $OUTPUT_FILE"
    echo ""
    echo "Decrypt with:"
    echo "  $0 show $service"
}

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

case "${1:-}" in
    show)
        cmd_show "$2"
        ;;
    set-secret)
        cmd_set_secret "$2" "$3"
        ;;
    sync)
        cmd_sync_supabase
        ;;
    encrypt-and-store)
        cmd_encrypt "$2" "$3"
        ;;
    *)
        cat << 'EOF'
📋 Credential Sync Manager
   Manage workspace secrets → Supabase Edge Function integration

USAGE
    ./scripts/credential-sync.sh <command> [options]

COMMANDS

    show <credential>
        Decrypt and display credentials from vault
        Options: supabase, github
        Example: ./scripts/credential-sync.sh show supabase

    set-secret <NAME> <VALUE>
        Set a single secret in Supabase Edge Function
        Example: ./scripts/credential-sync.sh set-secret GITHUB_WEBHOOK_SECRET "abc123xyz"

    sync
        Show how to sync Supabase credentials to Edge Function
        Example: ./scripts/credential-sync.sh sync

    encrypt-and-store <SERVICE> <JSON>
        Add a new credential to the workspace vault
        Example: ./scripts/credential-sync.sh encrypt-and-store slack '{"SLACK_BOT_TOKEN": "xoxb-..."}'

WORKFLOW

    1. View credentials:
       ./scripts/credential-sync.sh show supabase

    2. Set a secret in Supabase:
       ./scripts/credential-sync.sh set-secret GITHUB_WEBHOOK_SECRET "your-webhook-secret"

    3. Verify it worked:
       supabase secrets list --project-ref ksinisdzgtnqzsymhfya

SECURITY NOTES

    ✓ Master key is in: ~/.empirica/workspace/secrets/.master-key (600 perms)
    ✓ Encrypted files: ~/.empirica/workspace/secrets/*.enc
    ✓ Never commit master key or .enc files to git
    ✓ Back up master key to password manager or hardware key

EOF
        exit 1
        ;;
esac
