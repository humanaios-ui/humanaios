#!/bin/bash
# Supabase Secrets Management Helper
# Purpose: Update Edge Function secrets from workspace vault
# Usage: ./scripts/manage-supabase-secrets.sh <set|get|list> <SECRET_NAME> [value]
# Date: 2026-07-20

set -e

VAULT_DIR="${HOME}/.empirica/workspace/secrets"
MASTER_KEY_FILE="${VAULT_DIR}/.master-key"
PROJECT_ID="ksinisdzgtnqzsymhfya"
CREDENTIALS_FILE="${VAULT_DIR}/supabase-humanaios-witness.enc"

# Helper: Load Supabase credentials from workspace vault
load_supabase_credentials() {
    if [ ! -f "$MASTER_KEY_FILE" ]; then
        echo "❌ Error: Master key not found at $MASTER_KEY_FILE"
        exit 1
    fi

    MASTER_KEY=$(cat "$MASTER_KEY_FILE")

    if [ ! -f "$CREDENTIALS_FILE" ]; then
        echo "❌ Error: Supabase credentials not found at $CREDENTIALS_FILE"
        exit 1
    fi

    # Decrypt credentials
    CREDS=$(openssl enc -aes-256-cbc -d -in "$CREDENTIALS_FILE" \
        -pass pass:"$MASTER_KEY" -md sha256 2>/dev/null)

    SUPABASE_URL=$(echo "$CREDS" | jq -r '.credentials.SUPABASE_URL')
    SUPABASE_SERVICE_ROLE_KEY=$(echo "$CREDS" | jq -r '.credentials.SUPABASE_SERVICE_ROLE_KEY')

    if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
        echo "❌ Error: Could not decrypt Supabase credentials"
        exit 1
    fi

    export SUPABASE_URL
    export SUPABASE_SERVICE_ROLE_KEY
}

# Command: set <SECRET_NAME> <SECRET_VALUE>
cmd_set() {
    local secret_name=$1
    local secret_value=$2

    if [ -z "$secret_name" ] || [ -z "$secret_value" ]; then
        echo "❌ Usage: $0 set <SECRET_NAME> <SECRET_VALUE>"
        exit 1
    fi

    echo "🔐 Loading Supabase credentials from vault..."
    load_supabase_credentials

    echo "📝 Setting secret: $secret_name"
    supabase secrets set "$secret_name=$secret_value" --project-ref "$PROJECT_ID" || {
        echo "❌ Error: Failed to set secret. Make sure Supabase CLI is installed:"
        echo "   npm install -g @supabase/cli"
        exit 1
    }

    echo "✅ Secret '$secret_name' updated successfully"
}

# Command: get <SECRET_NAME>
cmd_get() {
    local secret_name=$1

    if [ -z "$secret_name" ]; then
        echo "❌ Usage: $0 get <SECRET_NAME>"
        exit 1
    fi

    echo "🔐 Loading Supabase credentials from vault..."
    load_supabase_credentials

    echo "📖 Retrieving secret: $secret_name"
    supabase secrets get "$secret_name" --project-ref "$PROJECT_ID" || {
        echo "⚠️  Secret not found or not accessible"
        exit 1
    }
}

# Command: list
cmd_list() {
    echo "🔐 Loading Supabase credentials from vault..."
    load_supabase_credentials

    echo "📋 Available secrets for project $PROJECT_ID:"
    supabase secrets list --project-ref "$PROJECT_ID" || {
        echo "❌ Error: Could not list secrets"
        exit 1
    }
}

# Main
case "${1:-}" in
    set)
        cmd_set "$2" "$3"
        ;;
    get)
        cmd_get "$2"
        ;;
    list)
        cmd_list
        ;;
    *)
        echo "Supabase Secrets Management Helper"
        echo ""
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  set <NAME> <VALUE>   Set a secret (e.g., set GITHUB_WEBHOOK_SECRET 'abc123')"
        echo "  get <NAME>           Get a secret value"
        echo "  list                 List all secrets"
        echo ""
        echo "Examples:"
        echo "  $0 set GITHUB_WEBHOOK_SECRET 'your-webhook-secret'"
        echo "  $0 get GITHUB_WEBHOOK_SECRET"
        echo "  $0 list"
        echo ""
        echo "Credentials are loaded automatically from: $CREDENTIALS_FILE"
        exit 1
        ;;
esac
