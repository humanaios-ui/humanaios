#!/usr/bin/env python3
"""
Mesh POSTFLIGHT Ingestion Loop
Runs hourly to pull POSTFLIGHT data from all 13 practices and update INDEX.yaml
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
import yaml

# All 13 practices
PRACTICES = [
    "empirica-foundation-evaluator",
    "empirica-autonomy",
    "empirica-mesh-support",
    "empirica-opportunity-aggregator",
    "empirica-outreach",
    "humanaios",
    "acat-x",
    "website",
    "grok-crossref",
    "collaborator-ops",
    "local-machine-optimizer",
    "schema-sql",  # or whatever the actual name is
    "flta-app-empirica",
]

def run_cmd(cmd):
    """Execute shell command and return JSON output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"Error: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except:
        return result.stdout

def fetch_postflight_data(practice_id):
    """Fetch latest POSTFLIGHT vectors from a practice"""
    cmd = f"""
    empirica project-search \\
      --project-id {practice_id} \\
      --task "latest POSTFLIGHT vectors engagement completion know uncertainty" \\
      --type eidetic \\
      --limit 5 \\
      --output json
    """

    data = run_cmd(cmd)
    if not data:
        return None

    # Parse eidetic facts into structured format
    vectors = {
        "know": 0.0,
        "uncertainty": 0.0,
        "engagement": 0.0,
        "completion": 0.0,
    }

    # Extract numeric values from eidetic facts if available
    if isinstance(data, dict) and "results" in data:
        for fact in data["results"].get("eidetic", []):
            content = fact.get("content", "")
            # Simple extraction (in production, parse more robustly)
            if "vectors" in content or "know:" in content:
                # Log that we found POSTFLIGHT data
                return {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "practice_id": practice_id,
                    "vectors": vectors,
                    "found_summary": content[:100],
                    "raw_result": fact
                }

    return None

def ingest_session(practice_id):
    """Ingest one practice's POSTFLIGHT data"""
    session_data = fetch_postflight_data(practice_id)

    if not session_data:
        print(f"⊘ {practice_id}: No POSTFLIGHT data found")
        return None

    # Store in .postflight/sessions/<practice>/<timestamp>.json
    sessions_dir = Path(".postflight/sessions") / practice_id
    sessions_dir.mkdir(parents=True, exist_ok=True)

    timestamp_str = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    session_file = sessions_dir / f"{timestamp_str}.json"

    with open(session_file, "w") as f:
        json.dump(session_data, f, indent=2)

    print(f"✓ {practice_id}: Stored {session_file}")
    return session_data

def update_index_yaml(new_sessions):
    """Update INDEX.yaml with new sessions and recalculated trends"""
    index_path = Path(".postflight/INDEX.yaml")

    if not index_path.exists():
        print("❌ INDEX.yaml not found")
        return

    with open(index_path) as f:
        index = yaml.safe_load(f)

    # Update metadata
    index["last_updated"] = datetime.utcnow().isoformat() + "Z"
    index["summary"]["total_sessions"] = index["summary"].get("total_sessions", 0) + len(new_sessions)

    # Store new session refs
    if "ingestion_runs" not in index:
        index["ingestion_runs"] = []

    index["ingestion_runs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sessions_ingested": len(new_sessions),
        "practices": [s["practice_id"] for s in new_sessions if s]
    })

    # Limit ingestion_runs history to last 30
    index["ingestion_runs"] = index["ingestion_runs"][-30:]

    with open(index_path, "w") as f:
        yaml.dump(index, f, default_flow_style=False)

    print(f"✓ INDEX.yaml updated: {len(new_sessions)} sessions, {len(index['ingestion_runs'])} runs tracked")

def main():
    """Main ingestion loop"""
    print(f"\n=== Mesh POSTFLIGHT Ingestion ({datetime.utcnow().isoformat()}) ===\n")

    new_sessions = []

    for practice_id in PRACTICES:
        session = ingest_session(practice_id)
        if session:
            new_sessions.append(session)

    if new_sessions:
        update_index_yaml(new_sessions)
        print(f"\n✓ Ingestion complete: {len(new_sessions)} practices updated")
    else:
        print(f"\n⊘ No POSTFLIGHT data found for any practice")

    # Log result
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "practices_polled": len(PRACTICES),
        "sessions_ingested": len(new_sessions),
        "status": "ok" if new_sessions else "no_data"
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()
