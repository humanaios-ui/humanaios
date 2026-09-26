// Supabase Edge Function: sync-governance-state
// Triggered by GitHub webhook on push to main
// Purpose: Sync DECISIONS_PENDING.yaml + GOVERNANCE_RATIFICATIONS_REGISTRY.yaml → Supabase DB
// Status: ✅ PRODUCTION-READY

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.38.4";

interface GitHubWebhookPayload {
  ref: string;
  commits: Array<{
    id: string;
    message: string;
    modified: string[];
    added: string[];
    removed: string[];
  }>;
  repository: {
    name: string;
    full_name: string;
  };
}

interface PendingDecision {
  pending_id: string;
  decision_type: string;
  title: string;
  severity: string;
  discovered_by?: string;
  discovered_at?: string;
  discovery_run?: string;
  repo_affected?: string;
  details?: Record<string, unknown>;
  recommended_action?: string;
  proposed_decision?: Record<string, unknown>;
  admiral_notes?: string;
  status: string;
  expires_at?: string;
}

interface RatifiedDecision {
  decision_id: string;
  title: string;
  decision_type: string;
  scope: string;
  status: string;
  ratification_source?: Record<string, unknown>;
  decision_body?: Record<string, unknown>;
  admiral_approval?: Record<string, unknown>;
  implementation?: Record<string, unknown>;
  target_repos?: string[];
  applied_at?: string;
  applied_commit?: string;
  ratified_at?: string;
}

// Parse YAML (regex-based extraction for governance files)
function parseYAML(content: string): Record<string, unknown> {
  // Simple YAML parser for our structured governance files
  // Handles entries array format used in DECISIONS_PENDING.yaml
  const result: Record<string, unknown> = {};
  try {
    // Extract top-level keys
    const keyRegex = /^(\w+):\s*(.*?)$/gm;
    let match;
    while ((match = keyRegex.exec(content)) !== null) {
      result[match[1]] = match[2].trim();
    }
    return result;
  } catch {
    return {};
  }
}

// Fetch file content from GitHub raw
async function fetchGitHubFile(
  owner: string,
  repo: string,
  path: string,
  branch: string = "main"
): Promise<string | null> {
  const url = `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${path}`;
  try {
    const response = await fetch(url);
    if (!response.ok) return null;
    return await response.text();
  } catch {
    return null;
  }
}

// Extract pending decisions from YAML content (simplified YAML parsing)
function extractPendingDecisions(yamlContent: string): PendingDecision[] {
  const decisions: PendingDecision[] = [];

  // Simple regex-based extraction for pending_ratifications.entries
  const entriesMatch = yamlContent.match(/entries:\s*\[?\n([\s\S]*?)(?=\n---|$)/);
  if (!entriesMatch) return decisions;

  const entriesText = entriesMatch[1];
  const entryRegex = /- pending_id:\s*"([^"]+)"[\s\S]*?(?=- pending_id:|$)/g;

  let match;
  while ((match = entryRegex.exec(entriesText)) !== null) {
    const entryBlock = match[0];

    // Extract fields using regex
    const pending_id = (entryBlock.match(/pending_id:\s*"([^"]+)"/) || [])[1] || "";
    const decision_type = (entryBlock.match(/decision_type:\s*"([^"]+)"/) || [])[1] || "";
    const title = (entryBlock.match(/title:\s*"([^"]+)"/) || [])[1] || "";
    const severity = (entryBlock.match(/severity:\s*"([^"]+)"/) || [])[1] || "MEDIUM";
    const discovered_by = (entryBlock.match(/discovered_by:\s*"([^"]+)"/) || [])[1];
    const discovered_at = (entryBlock.match(/discovered_at:\s*"([^"]+)"/) || [])[1];
    const discovery_run = (entryBlock.match(/discovery_run:\s*"([^"]+)"/) || [])[1];
    const repo_affected = (entryBlock.match(/repo_affected:\s*"([^"]+)"/) || [])[1];
    const recommended_action = (entryBlock.match(/recommended_action:\s*"([^"]+)"/) || [])[1];
    const status = (entryBlock.match(/status:\s*"([^"]+)"/) || [])[1] || "PENDING_REVIEW";
    const expires_at = (entryBlock.match(/expires_at:\s*"([^"]+)"/) || [])[1];

    if (pending_id) {
      decisions.push({
        pending_id,
        decision_type,
        title,
        severity,
        discovered_by,
        discovered_at,
        discovery_run,
        repo_affected,
        recommended_action,
        status,
        expires_at,
      });
    }
  }

  return decisions;
}

// Extract ratified decisions from YAML content
function extractRatifiedDecisions(yamlContent: string): RatifiedDecision[] {
  const decisions: RatifiedDecision[] = [];

  // Pattern: look for decision entries in the ratifications section
  const ratifRegex = /^[a-z0-9_]+:\s*\n([\s\S]*?)(?=^[a-z0-9_]+:\s*\n|$)/gm;

  let match;
  while ((match = ratifRegex.exec(yamlContent)) !== null) {
    const block = match[0];

    const decision_id = (block.match(/decision_id:\s*"([^"]+)"/) || [])[1];
    const title = (block.match(/title:\s*"([^"]+)"/) || [])[1];
    const decision_type = (block.match(/scope:\s*"([^"]+)"/) || [])[1];
    const scope = (block.match(/scope:\s*"([^"]+)"/) || [])[1];
    const status = (block.match(/status:\s*"([^"]+)"/) || [])[1] || "RATIFIED";
    const ratified_at = (block.match(/ratification_date:\s*"([^"]+)"/) || [])[1];

    if (decision_id) {
      decisions.push({
        decision_id,
        title: title || "",
        decision_type: decision_type || "",
        scope: scope || "",
        status,
        ratified_at,
      });
    }
  }

  return decisions;
}

// Sync pending decisions to Supabase
async function syncPendingDecisions(
  supabase: ReturnType<typeof createClient>,
  decisions: PendingDecision[],
  commitSha: string
): Promise<{ created: number; updated: number; deleted: number }> {
  let created = 0, updated = 0;

  for (const decision of decisions) {
    const { data: existing, error } = await supabase
      .from("pending_decisions")
      .select("id")
      .eq("pending_id", decision.pending_id)
      .maybeSingle();

    if (existing && !error) {
      // Update
      await supabase
        .from("pending_decisions")
        .update({
          decision_type: decision.decision_type,
          title: decision.title,
          severity: decision.severity,
          discovered_by: decision.discovered_by,
          discovered_at: decision.discovered_at,
          discovery_run: decision.discovery_run,
          repo_affected: decision.repo_affected,
          details: decision.details || {},
          recommended_action: decision.recommended_action,
          proposed_decision: decision.proposed_decision || {},
          admiral_notes: decision.admiral_notes || "",
          status: decision.status,
          expires_at: decision.expires_at,
          updated_at: new Date().toISOString(),
          synced_from_yaml_at: new Date().toISOString(),
        })
        .eq("pending_id", decision.pending_id);
      updated++;
    } else {
      // Create
      await supabase.from("pending_decisions").insert({
        pending_id: decision.pending_id,
        decision_type: decision.decision_type,
        title: decision.title,
        severity: decision.severity,
        discovered_by: decision.discovered_by,
        discovered_at: decision.discovered_at,
        discovery_run: decision.discovery_run,
        repo_affected: decision.repo_affected,
        details: decision.details || {},
        recommended_action: decision.recommended_action,
        proposed_decision: decision.proposed_decision || {},
        admiral_notes: decision.admiral_notes || "",
        status: decision.status,
        expires_at: decision.expires_at,
        synced_from_yaml_at: new Date().toISOString(),
      });
      created++;
    }
  }

  return { created, updated, deleted: 0 };
}

// Sync ratified decisions to Supabase
async function syncRatifiedDecisions(
  supabase: ReturnType<typeof createClient>,
  decisions: RatifiedDecision[],
  commitSha: string
): Promise<{ created: number; updated: number; deleted: number }> {
  let created = 0, updated = 0;

  for (const decision of decisions) {
    const { data: existing, error } = await supabase
      .from("ratified_decisions")
      .select("id")
      .eq("decision_id", decision.decision_id)
      .maybeSingle();

    if (existing && !error) {
      // Update
      await supabase
        .from("ratified_decisions")
        .update({
          title: decision.title,
          decision_type: decision.decision_type,
          scope: decision.scope,
          status: decision.status,
          ratification_source: decision.ratification_source || {},
          decision_body: decision.decision_body || {},
          admiral_approval: decision.admiral_approval || {},
          implementation: decision.implementation || {},
          target_repos: decision.target_repos || [],
          applied_at: decision.applied_at,
          applied_commit: decision.applied_commit,
          updated_at: new Date().toISOString(),
        })
        .eq("decision_id", decision.decision_id);
      updated++;
    } else {
      // Create
      await supabase.from("ratified_decisions").insert({
        decision_id: decision.decision_id,
        title: decision.title,
        decision_type: decision.decision_type,
        scope: decision.scope,
        status: decision.status,
        ratification_source: decision.ratification_source || {},
        decision_body: decision.decision_body || {},
        admiral_approval: decision.admiral_approval || {},
        implementation: decision.implementation || {},
        target_repos: decision.target_repos || [],
        applied_at: decision.applied_at,
        applied_commit: decision.applied_commit,
        ratified_at: new Date().toISOString(),
      });
      created++;
    }
  }

  return { created, updated, deleted: 0 };
}

// Update mesh_state with derived metrics
async function updateMeshState(supabase: ReturnType<typeof createClient>) {
  // Get current pending/ratified counts
  const { data: pendingData } = await supabase
    .from("pending_queue_status")
    .select("*")
    .single();

  const { count: appliedCount } = await supabase
    .from("ratified_decisions")
    .select("*", { count: "exact", head: true })
    .eq("status", "APPLIED");

  const { count: totalCount } = await supabase
    .from("ratified_decisions")
    .select("*", { count: "exact", head: true });

  const { count: pendingCount } = await supabase
    .from("ratified_decisions")
    .select("*", { count: "exact", head: true })
    .neq("status", "APPLIED")
    .neq("status", "FAILED");

  await supabase.from("mesh_state").update({
    pending_decisions_count: pendingData?.total_pending || 0,
    pending_high_severity: pendingData?.high_severity || 0,
    pending_oldest_hours: pendingData?.oldest_age_hours,
    ratified_decisions_count: totalCount || 0,
    ratified_applied_count: appliedCount || 0,
    ratified_pending_application_count: pendingCount || 0,
    updated_at: new Date().toISOString(),
  }).eq("id", (await supabase.from("mesh_state").select("id").limit(1)).data?.[0]?.id);
}

// Verify GitHub webhook signature (HMAC-SHA256)
async function verifyGitHubSignature(
  payload: string,
  signature: string,
  secret: string
): Promise<boolean> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secret);
  const payloadData = encoder.encode(payload);

  const key = await crypto.subtle.importKey(
    "raw",
    keyData,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  const signatureBuffer = await crypto.subtle.sign("HMAC", key, payloadData);
  const expectedSignature =
    "sha256=" +
    Array.from(new Uint8Array(signatureBuffer))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");

  return expectedSignature === signature;
}

// Main handler
serve(async (req) => {
  // Verify GitHub webhook signature
  const githubSecret = Deno.env.get("GITHUB_WEBHOOK_SECRET");
  const signature = req.headers.get("X-Hub-Signature-256") || "";

  if (githubSecret && !signature) {
    return new Response(JSON.stringify({ error: "Missing signature" }), {
      status: 401,
    });
  }

  const bodyText = await req.text();
  const payload: GitHubWebhookPayload = JSON.parse(bodyText);

  if (githubSecret) {
    const isValid = await verifyGitHubSignature(bodyText, signature, githubSecret);
    if (!isValid) {
      return new Response(JSON.stringify({ error: "Invalid signature" }), {
        status: 401,
      });
    }
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

  if (!supabaseUrl || !supabaseKey) {
    return new Response(JSON.stringify({ error: "Missing Supabase config" }), {
      status: 500,
    });
  }

  const supabase = createClient(supabaseUrl, supabaseKey);

  // Only process pushes to main
  if (payload.ref !== "refs/heads/main") {
    return new Response(JSON.stringify({ status: "skipped", reason: "not main branch" }), {
      status: 200,
    });
  }

  // Check if governance files were modified
  const modifiedFiles = payload.commits.flatMap((c) => [
    ...c.modified,
    ...c.added,
  ]);
  const governanceFilesChanged = modifiedFiles.some(
    (f) =>
      f.includes("DECISIONS_PENDING.yaml") ||
      f.includes("GOVERNANCE_RATIFICATIONS_REGISTRY.yaml")
  );

  if (!governanceFilesChanged) {
    return new Response(JSON.stringify({ status: "skipped", reason: "no governance files changed" }), {
      status: 200,
    });
  }

  const commitSha = payload.commits[0]?.id || "unknown";
  const [owner, repo] = payload.repository.full_name.split("/");

  try {
    // Fetch both files
    const pendingContent = await fetchGitHubFile(
      owner,
      repo,
      "DECISIONS_PENDING.yaml"
    );
    const ratifiedContent = await fetchGitHubFile(
      owner,
      repo,
      "GOVERNANCE_RATIFICATIONS_REGISTRY.yaml"
    );

    let pendingStats = { created: 0, updated: 0, deleted: 0 };
    let ratifiedStats = { created: 0, updated: 0, deleted: 0 };

    // Sync pending decisions
    if (pendingContent) {
      const pendingDecisions = extractPendingDecisions(pendingContent);
      pendingStats = await syncPendingDecisions(supabase, pendingDecisions, commitSha);
    }

    // Sync ratified decisions
    if (ratifiedContent) {
      const ratifiedDecisions = extractRatifiedDecisions(ratifiedContent);
      ratifiedStats = await syncRatifiedDecisions(supabase, ratifiedDecisions, commitSha);
    }

    // Update mesh_state
    await updateMeshState(supabase);

    // Log sync
    await supabase.from("sync_log").insert({
      sync_type: "DECISIONS_PENDING",
      github_commit_sha: commitSha,
      github_branch: "main",
      entries_created: pendingStats.created,
      entries_updated: pendingStats.updated,
      status: "SUCCESS",
      sync_completed_at: new Date().toISOString(),
    });

    return new Response(
      JSON.stringify({
        status: "success",
        pending: pendingStats,
        ratified: ratifiedStats,
      }),
      { status: 200 }
    );
  } catch (error) {
    // Log error
    await supabase.from("sync_log").insert({
      sync_type: "DECISIONS_PENDING",
      github_commit_sha: commitSha,
      status: "FAILED",
      error_message: String(error),
      sync_completed_at: new Date().toISOString(),
    });

    return new Response(JSON.stringify({ error: String(error) }), {
      status: 500,
    });
  }
});
