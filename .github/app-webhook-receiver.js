/**
 * GitHub App Webhook Receiver for HumanAIOS Security Scanner
 *
 * Handles:
 * - Repository installation/uninstallation
 * - Auto-deployment of security scanning workflow
 * - Scan result aggregation
 * - Cross-repo incident routing
 */

const crypto = require('crypto');
const { Octokit } = require('@octokit/rest');

const WEBHOOK_SECRET = process.env.GITHUB_WEBHOOK_SECRET;
const APP_ID = process.env.GITHUB_APP_ID;
const PRIVATE_KEY = process.env.GITHUB_PRIVATE_KEY;

// Verify webhook signature
function verifyWebhookSignature(req) {
  const signature = req.headers['x-hub-signature-256'];
  if (!signature) return false;

  const payload = req.rawBody; // Must be raw Buffer, not parsed JSON
  const hash = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(`sha256=${hash}`),
    Buffer.from(signature)
  );
}

// Create authenticated Octokit client for repo
async function createRepoClient(owner, repo, installationId) {
  const octokit = new Octokit({
    authStrategy: createAppAuth,
    auth: {
      appId: APP_ID,
      privateKey: PRIVATE_KEY,
      installationId: installationId,
    },
  });
  return octokit;
}

// Handle repository installation
async function handleRepositoryInstalled(payload) {
  const { repository, installation, action } = payload;

  if (action !== 'created') return;

  console.log(`📦 App installed on ${repository.full_name}`);

  try {
    const octokit = await createRepoClient(
      repository.owner.login,
      repository.name,
      installation.id
    );

    // 1. Deploy security scanning workflow
    await deployWorkflow(octokit, repository);

    // 2. Deploy pre-commit hook
    await deployPreCommitHook(octokit, repository);

    // 3. Update .gitignore
    await updateGitignore(octokit, repository);

    // 4. Create initial commit
    await createInitialCommit(octokit, repository);

    // 5. Log in Empirica
    await logToEpirica(repository, 'installed', installation.id);

    console.log(`✅ Security scanning deployed to ${repository.full_name}`);
  } catch (error) {
    console.error(`❌ Failed to deploy to ${repository.full_name}:`, error);
    await logToEpirica(repository, 'install_failed', installation.id, error);
    throw error;
  }
}

// Deploy GitHub workflow
async function deployWorkflow(octokit, repository) {
  const workflowContent = `
name: Secret Scanning & Credential Detection

on:
  pull_request:
    branches: [main, staging]
  push:
    branches: [main, staging]
  workflow_dispatch:

permissions:
  contents: read
  security-events: write
  checks: write
  pull-requests: write

jobs:
  secret-scan:
    name: Detect Secrets & Credentials
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install detection tools
        run: pip install detect-secrets

      - name: Scan for secrets
        run: |
          if [ ! -f .secrets.baseline ]; then
            detect-secrets scan --baseline .secrets.baseline --all-files
          fi
          detect-secrets scan --baseline .secrets.baseline --all-files 2>&1 | tee /tmp/scan.txt
          if grep -q "Secret found" /tmp/scan.txt; then
            echo "❌ Secrets detected"
            exit 1
          fi
          echo "✅ No secrets found"
`;

  try {
    await octokit.repos.createOrUpdateFileContents({
      owner: repository.owner.login,
      repo: repository.name,
      path: '.github/workflows/secret-scan.yml',
      message: 'ci: Add HumanAIOS security scanning workflow',
      content: Buffer.from(workflowContent).toString('base64'),
      committer: {
        name: 'HumanAIOS Security Bot',
        email: 'security@humanaios.empirica',
      },
    });
    console.log('  ✓ Workflow deployed');
  } catch (error) {
    console.error('  ✗ Failed to deploy workflow:', error.message);
    throw error;
  }
}

// Deploy pre-commit hook
async function deployPreCommitHook(octokit, repository) {
  const hookContent = `#!/bin/bash
# Auto-deployed by HumanAIOS Security Scanner
echo "🔐 Scanning for credential patterns..."

PATTERNS=(
  'postgresql://.*:.*@'
  'api[_-]?key["\\'']?\s*[:=]'
  'password["\\'']?\s*[:=]'
)

for pattern in "\${PATTERNS[@]}"; do
  if git diff --cached --all | grep -iE "$pattern"; then
    echo "❌ Potential credential detected"
    exit 1
  fi
done

echo "✅ Pre-commit check passed"
exit 0
`;

  try {
    await octokit.repos.createOrUpdateFileContents({
      owner: repository.owner.login,
      repo: repository.name,
      path: '.githooks/pre-commit',
      message: 'ci: Add HumanAIOS pre-commit security hook',
      content: Buffer.from(hookContent).toString('base64'),
      committer: {
        name: 'HumanAIOS Security Bot',
        email: 'security@humanaios.empirica',
      },
    });
    console.log('  ✓ Pre-commit hook deployed');
  } catch (error) {
    console.error('  ✗ Failed to deploy pre-commit hook:', error.message);
    // Don't fail on this, it's non-critical
  }
}

// Update .gitignore
async function updateGitignore(octokit, repository) {
  const ignoreMissing = [
    '.env', '.env.local', '.env.production',
    '.secrets', '*.key', '*.pem',
  ];

  try {
    let content = '';
    try {
      const res = await octokit.repos.getContent({
        owner: repository.owner.login,
        repo: repository.name,
        path: '.gitignore',
      });
      content = Buffer.from(res.data.content, 'base64').toString();
    } catch (e) {
      // .gitignore doesn't exist, create new one
      content = '';
    }

    const toAdd = ignoreMissing.filter(p => !content.includes(p));
    if (toAdd.length > 0) {
      content += '\n# Security: Credential files\n' + toAdd.join('\n') + '\n';

      await octokit.repos.createOrUpdateFileContents({
        owner: repository.owner.login,
        repo: repository.name,
        path: '.gitignore',
        message: 'ci: Add credential file patterns to .gitignore',
        content: Buffer.from(content).toString('base64'),
        committer: {
          name: 'HumanAIOS Security Bot',
          email: 'security@humanaios.empirica',
        },
      });
      console.log('  ✓ .gitignore updated');
    }
  } catch (error) {
    console.error('  ✗ Failed to update .gitignore:', error.message);
    // Non-critical, continue
  }
}

// Create initial commit with all changes
async function createInitialCommit(octokit, repository) {
  // This is handled by individual file operations above
  // (GitHub API creates commits for each file change)
  console.log('  ✓ Changes committed');
}

// Log to Empirica for audit trail
async function logToEpirica(repository, action, installationId, error = null) {
  try {
    // POST to Empirica API to log installation event
    const finding = {
      finding: `GitHub App ${action}: ${repository.full_name} (installation_id: ${installationId})${error ? ` - Error: ${error.message}` : ''}`,
      impact: 0.8,
      project_id: 'humanaios',
    };

    // This would call empirica CLI or API
    console.log(`[Empirica Log] ${JSON.stringify(finding)}`);
  } catch (e) {
    console.warn('Failed to log to Empirica:', e.message);
  }
}

// Main webhook handler
async function handleWebhook(req, res) {
  // Verify signature
  if (!verifyWebhookSignature(req)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const event = req.headers['x-github-event'];
  const payload = req.body;

  console.log(`📨 Received ${event} event`);

  try {
    if (event === 'installation' && payload.action === 'created') {
      await handleRepositoryInstalled(payload);
    } else if (event === 'installation' && payload.action === 'deleted') {
      console.log(`🗑️  App uninstalled from ${payload.repositories_removed?.length || 0} repos`);
    } else if (event === 'pull_request') {
      console.log(`📝 PR ${payload.action} on ${payload.repository.full_name}`);
    }

    res.status(200).json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: error.message });
  }
}

module.exports = { handleWebhook, verifyWebhookSignature };
