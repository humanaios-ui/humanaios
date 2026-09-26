#!/bin/bash
# Credential Vault Setup
# Purpose: Store API credentials securely (encrypted) in workspace
# Method: OpenSSL encryption (can be integrated with hardware keys later)
# Status: Script-driven, prompts for credentials
# Date: 2026-07-20

set -e

VAULT_DIR="${HOME}/.empirica/secrets"
MASTER_KEY_FILE="${HOME}/.empirica/secrets/.master-key"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Empirica Credential Vault Setup                               ║"
echo "║ Encrypt and store API credentials securely                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Ensure vault directory exists
mkdir -p "$VAULT_DIR"
chmod 700 "$VAULT_DIR"

# ─────────────────────────────────────────────────────────────────
# STEP 1: Create or load master key
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 1: Master Key Setup..."

if [ -f "$MASTER_KEY_FILE" ]; then
    echo "✓ Master key found at: $MASTER_KEY_FILE"
    read -p "Use existing master key? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "⚠ Warning: Creating new master key will invalidate existing encrypted credentials"
        read -p "Continue? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
else
    echo "Creating new master key..."
    openssl rand -hex 32 > "$MASTER_KEY_FILE"
    chmod 600 "$MASTER_KEY_FILE"
    echo "✓ Master key created: $MASTER_KEY_FILE"
    echo "  ⚠️  IMPORTANT: Back this up to a secure location (hardware key, password manager, etc.)"
fi

MASTER_KEY=$(cat "$MASTER_KEY_FILE")

# ─────────────────────────────────────────────────────────────────
# STEP 2: Supabase Credentials
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 2: Supabase Credentials..."
echo "  (Leave blank to skip and configure later)"
echo ""

read -p "  SUPABASE_URL: " SUPABASE_URL
if [ -z "$SUPABASE_URL" ]; then
    echo "  ⏭️  Supabase credentials skipped"
else
    read -p "  SUPABASE_ANON_KEY: " SUPABASE_ANON_KEY
    read -p "  SUPABASE_SERVICE_ROLE_KEY: " SUPABASE_SERVICE_ROLE_KEY

    # Create JSON credential file
    SUPABASE_CREDS=$(cat <<EOF
{
  "service": "supabase",
  "project": "humanaios-witness",
  "credentials": {
    "SUPABASE_URL": "$SUPABASE_URL",
    "SUPABASE_ANON_KEY": "$SUPABASE_ANON_KEY",
    "SUPABASE_SERVICE_ROLE_KEY": "$SUPABASE_SERVICE_ROLE_KEY"
  },
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "encrypted": true
}
EOF
)

    # Encrypt and store
    echo "$SUPABASE_CREDS" | openssl enc -aes-256-cbc -salt -in /dev/stdin -out "$VAULT_DIR/supabase-humanaios-witness.enc" -K "$MASTER_KEY" -md sha256 2>/dev/null || {
        # Fallback if -K flag doesn't work in this OpenSSL version
        echo "$SUPABASE_CREDS" | openssl enc -aes-256-cbc -salt -out "$VAULT_DIR/supabase-humanaios-witness.enc" -pass pass:"$MASTER_KEY" -md sha256
    }

    chmod 600 "$VAULT_DIR/supabase-humanaios-witness.enc"
    echo "✓ Supabase credentials encrypted: $VAULT_DIR/supabase-humanaios-witness.enc"
fi

# ─────────────────────────────────────────────────────────────────
# STEP 3: GitHub Token
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 3: GitHub Token..."
echo "  (Leave blank to skip and configure later)"
echo ""

read -p "  GITHUB_TOKEN: " GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo "  ⏭️  GitHub token skipped"
else
    # Create JSON credential file
    GITHUB_CREDS=$(cat <<EOF
{
  "service": "github",
  "credentials": {
    "GITHUB_TOKEN": "$GITHUB_TOKEN"
  },
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "encrypted": true
}
EOF
)

    # Encrypt and store
    echo "$GITHUB_CREDS" | openssl enc -aes-256-cbc -salt -out "$VAULT_DIR/github-token.enc" -pass pass:"$MASTER_KEY" -md sha256
    chmod 600 "$VAULT_DIR/github-token.enc"
    echo "✓ GitHub token encrypted: $VAULT_DIR/github-token.enc"
fi

# ─────────────────────────────────────────────────────────────────
# STEP 4: Verification & Testing
# ─────────────────────────────────────────────────────────────────

echo ""
echo "Step 4: Verification..."

echo ""
echo "Vault contents:"
ls -lah "$VAULT_DIR"

if [ -f "$VAULT_DIR/supabase-humanaios-witness.enc" ]; then
    echo ""
    echo "Testing Supabase credential decryption..."
    # Attempt to decrypt (this will show if credentials are valid JSON)
    openssl enc -aes-256-cbc -d -in "$VAULT_DIR/supabase-humanaios-witness.enc" -pass pass:"$MASTER_KEY" -md sha256 2>/dev/null | jq . > /dev/null && echo "✓ Supabase credentials decrypt successfully" || echo "⚠ Warning: Could not decrypt Supabase credentials"
fi

if [ -f "$VAULT_DIR/github-token.enc" ]; then
    echo ""
    echo "Testing GitHub credential decryption..."
    openssl enc -aes-256-cbc -d -in "$VAULT_DIR/github-token.enc" -pass pass:"$MASTER_KEY" -md sha256 2>/dev/null | jq . > /dev/null && echo "✓ GitHub credentials decrypt successfully" || echo "⚠ Warning: Could not decrypt GitHub credentials"
fi

# ─────────────────────────────────────────────────────────────────
# STEP 5: Summary
# ─────────────────────────────────────────────────────────────────

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ ✅ Credential Vault Initialized                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "📋 Security Notes:"
echo ""
echo "1. MASTER KEY LOCATION: $MASTER_KEY_FILE"
echo "   - Protect this file with filesystem permissions"
echo "   - Back up to: password manager, hardware key, or encrypted USB"
echo "   - Never commit to git"
echo ""
echo "2. ENCRYPTED CREDENTIALS: $VAULT_DIR/*.enc"
echo "   - These files are encrypted with OpenSSL AES-256"
echo "   - Can only be decrypted with the master key"
echo ""
echo "3. ACCESSING CREDENTIALS FROM PROJECTS:"
echo "   $ export EMPIRICA_VAULT_KEY=\$(cat $MASTER_KEY_FILE)"
echo "   $ empirica credential-get supabase-humanaios-witness SUPABASE_URL"
echo ""
echo "4. FUTURE: Hardware Key Integration"
echo "   - Replace master-key file with hardware key (Yubikey, TPM, etc.)"
echo "   - Credentials remain encrypted at rest"
echo ""
echo "✓ Vault setup complete."
