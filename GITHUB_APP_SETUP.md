# GitHub App: HumanAIOS Security Scanner

This document describes the GitHub App for automating security scanning deployment across multiple repositories.

## Overview

The **HumanAIOS Security Scanner** GitHub App:
- Automatically deploys credential scanning on repository installation
- Provides unified incident detection across multiple repos
- Routes security alerts to repository owners
- Maintains an audit trail in Empirica

## Installation

### For Repository Owners

1. **Navigate to the App installation page:**
   ```
   https://github.com/apps/humanaios-security-scanner/installations/new
   ```

2. **Select repositories** you want to protect
   - All repositories (recommended)
   - Or select specific repos

3. **Authorize permissions:**
   - `contents: read` — read repository files
   - `pull_requests: write` — comment on PRs with scan results
   - `workflows: write` — deploy security scanning workflow
   - `security_events: write` — log security events

4. **Install** — The app will automatically:
   - Deploy `.github/workflows/secret-scan.yml`
   - Deploy `.githooks/pre-commit` hook
   - Update `.gitignore` with credential patterns
   - Create initial commit documenting the deployment

## What Gets Deployed

### Workflow: `.github/workflows/secret-scan.yml`

Runs on every PR and push to main/staging:
- Scans for hardcoded credentials (PostgreSQL, API keys, private keys)
- Blocks PRs if secrets detected
- Comments with scan results and remediation guidance

### Pre-Commit Hook: `.githooks/pre-commit`

Runs locally on every `git commit`:
- Detects credential patterns in staged changes
- Prevents accidental commits with secrets
- Guides developer toward secure alternatives

### Gitignore Patterns

Added to `.gitignore`:
```
.env
.env.local
.env.production
.secrets
*.key
*.pem
```

## Architecture

```
GitHub Repository
├── .github/workflows/secret-scan.yml ← Auto-deployed by App
├── .githooks/pre-commit              ← Auto-deployed by App
├── .gitignore (updated)              ← Auto-deployed by App
└── (your code)

When PR is created:
├── Workflow triggers
├── Scans for credentials
├── Comments with results
└── Blocks merge if secrets found

When commit is created (locally):
├── Pre-commit hook triggers
├── Scans staged changes
├── Blocks commit if secrets found
└── Shows remediation guidance
```

## Webhook Events Handled

| Event | Action | Response |
|-------|--------|----------|
| `installation` | `created` | Deploy scanning to repos |
| `installation` | `deleted` | Remove scanning (optional cleanup) |
| `pull_request` | `opened/synchronize` | Trigger security scan |
| `push` | `main/staging` | Trigger security scan |

## Webhook Receiver Deployment

### Option 1: AWS Lambda (Recommended)

```bash
# Deploy webhook receiver to Lambda
serverless deploy --function security-scanner-webhook

# Environment variables needed:
# GITHUB_WEBHOOK_SECRET
# GITHUB_APP_ID
# GITHUB_PRIVATE_KEY (base64 encoded)
```

### Option 2: Autonomy Service

Deploy webhook receiver within autonomy practice:
- REST endpoint: `POST /webhooks/github`
- Authenticates with GitHub App credentials
- Logs events to Empirica
- Orchestrates repo deployments

### Option 3: GitHub Actions (Self-Hosted)

Use GitHub Actions runner to handle webhook:
- Webhook → Action trigger
- Action performs deployment
- Uses `GITHUB_TOKEN` for repo access

## Configuration

### App Manifest (`app.yml`)

Located in repository root, defines:
- App name, description, homepage
- Webhook URL (change before deploying)
- Permissions required
- Events to subscribe to

**Before deploying, update:**

```yaml
hook_attributes:
  url: https://<your-webhook-endpoint>/webhooks/github  # CHANGE THIS
```

### Environment Variables

Required for webhook receiver:

```bash
export GITHUB_WEBHOOK_SECRET="your-webhook-secret"
export GITHUB_APP_ID="your-app-id"
export GITHUB_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n..."
export EMPIRICA_API_KEY="your-empirica-key"
```

## Creating Your Own GitHub App

### Step 1: Register App

1. Go to GitHub Settings → Developer settings → GitHub Apps
2. Click "New GitHub App"
3. Fill in details:
   - **App name:** HumanAIOS Security Scanner (or your variant)
   - **Homepage URL:** https://github.com/humanaios-ui/humanaios
   - **Webhook URL:** `https://your-endpoint/webhooks/github`
   - **Webhook secret:** Generate random secret (`openssl rand -hex 32`)

### Step 2: Set Permissions

```
Repository permissions:
- Contents: Read & write
- Pull requests: Read & write
- Workflows: Read & write
- Security events: Write

User permissions:
- None required
```

### Step 3: Subscribe to Events

```
- Repository
- Pull request
- Push
```

### Step 4: Install Locally for Testing

1. Click "Install App"
2. Select your test repository
3. Verify webhook receiver receives events

### Step 5: Deploy Webhook Receiver

Choose one of the deployment options above (Lambda, Autonomy, Actions)

## Monitoring & Logs

### GitHub App Activity

View in GitHub:
Settings → Developer settings → GitHub Apps → [Your App] → Advanced → Delivery logs

### Empirica Logs

All deployments logged to Empirica with:
- Finding: "GitHub App [action]: [repo_name]"
- Impact: 0.8
- Audit trail: installation_id, timestamp, error status

View with:
```bash
empirica project-search --task "GitHub App deployment" --project-id humanaios
```

### Webhook Receiver Logs

Depending on deployment:
- **Lambda:** CloudWatch Logs
- **Autonomy:** `/var/log/autonomy/security-scanner.log`
- **GitHub Actions:** Job logs

## Troubleshooting

### Webhook Not Received

1. **Check webhook URL** — Settings → Developer settings → GitHub Apps → [Your App] → Webhook URL
2. **Check secret** — Must match `GITHUB_WEBHOOK_SECRET` env var
3. **Check logs** — Advanced → Delivery logs shows HTTP responses

### Deployment Failed

1. **Check permissions** — App must have `workflows: write`, `contents: write`
2. **Check credentials** — `GITHUB_APP_ID` and `GITHUB_PRIVATE_KEY` must be valid
3. **Check API limits** — GitHub has rate limits (60 requests/hour for auth'd apps)

### Scan Not Triggering on PR

1. **Check workflow** — Verify `.github/workflows/secret-scan.yml` exists and is valid YAML
2. **Check branch** — Workflow only runs on `main` and `staging` branches by default
3. **Check permissions** — PR author must have push access (not always true for external contributors)

## Uninstalling

### For Repository Owners

1. Go to Settings → Integrations → GitHub Apps
2. Find "HumanAIOS Security Scanner"
3. Click "Uninstall"

The app will:
- Receive `installation.deleted` event
- (Optional) Remove deployed files from repository
- Stop monitoring the repository

## Cross-Repo Incident Response

When a secret is detected across multiple repos:

1. **Individual PR Comments** — Each repo gets scan results on its PR
2. **Empirica Logging** — Finding logged with repo+incident ID
3. **Mesh Notification** — Alert routed to repo owner via Empirica collab
4. **Coordination** — If same credential across repos, trigger orchestrated rotation

Example orchestration:
```
Repo A: PostgreSQL secret detected
├→ Log to Empirica
├→ Comment on PR with guidance
├→ Alert: "Rotate db.prod.co:5432 password"
└→ Route to repo owner via mesh

Repo B: Same PostgreSQL secret detected (within 1 hour)
├→ Log to Empirica (flagged: duplicate)
├→ Escalate: "Credential in multiple repos - emergency rotation"
└→ Propose to autonomy: "Orchestrate emergency password rotation"
```

## Related Documentation

- [SECURITY_SCANNING.md](SECURITY_SCANNING.md) — Scanning system details
- [app.yml](app.yml) — GitHub App manifest
- [.github/app-webhook-receiver.js](.github/app-webhook-receiver.js) — Webhook handler source

## Questions / Issues

For questions about this GitHub App, see:
- GitHub Issues: [humanaios-ui/humanaios/issues](https://github.com/humanaios-ui/humanaios/issues)
- Empirica Mesh: Collab with humanaios practice
- Security Incidents: [security@humanaios.empirica](mailto:security@humanaios.empirica)

---

**App Version:** 1.0  
**Last Updated:** 2026-08-08  
**Maintainer:** HumanAIOS Security Team
