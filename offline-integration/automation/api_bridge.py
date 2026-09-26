#!/usr/bin/env python3
"""
API Bridge: Wire HTML Dashboard to Python Automation Gates
Connects intent-os-universal-v2.html UI to cycle2_registry_gate.py + boundary_and_scorer.py

Endpoints:
  POST /gate/registry       — Submit record to registry gate (3-outcome routing)
  GET  /gate/score/<id>     — Get scoring result for an accepted record
  POST /feedback/report     — Report issue from UI feedback ledger
  GET  /state/sync          — Get current system state (intent reconciliation)
  POST /harness/set         — Set resource harness mode (balanced/ai-led/human-led/capital)

Wire: HTML form submissions → Python gates → UI state updates
"""

import json
import hashlib
import sys
import os
from typing import Dict, Tuple, Any

# Add automation directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from cycle2_registry_gate import registry_gate
from boundary_and_scorer import scorer, ALLOWED_FIELDS

class APIBridge:
    def __init__(self):
        self.state = {
            "pipeline": {"propose": 0, "ratify": 0, "land": 0},
            "intent": {"stated": None, "revealed": None, "gap": None},
            "primary": None,
            "wip": [],
            "harness_mode": "balanced",
            "harness": {"human": 0.5, "machine": 0.3, "capital": 0.2},
            "feedback": [],
        }

    def process_registry_submission(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Submit record through registry gate (3-outcome routing)"""
        outcome, reason = registry_gate(record)

        result = {
            "outcome": outcome,      # ACCEPT|QUARANTINE|CANDIDATE
            "reason": reason,
            "record_id": hashlib.md5(json.dumps(record, sort_keys=True).encode()).hexdigest()[:12],
            "timestamp": self._timestamp(),
        }

        if outcome == "ACCEPT":
            # Route to scorer for landing evaluation
            score = scorer(record)
            result["score"] = score
            self.state["pipeline"]["propose"] += 1
            # Move to ratify queue (Z2 approval)
            self.state["wip"].append({
                "id": result["record_id"],
                "status": "proposed",
                "record": record,
                "score": score,
            })
        elif outcome == "QUARANTINE":
            self.state["feedback"].append({
                "source": "machine",
                "type": "security_reject",
                "severity": "high",
                "message": f"Quarantine: {reason}",
                "timestamp": self._timestamp(),
            })
        elif outcome == "CANDIDATE":
            # Route to discovery pathway
            self.state["wip"].append({
                "id": result["record_id"],
                "status": "candidate",
                "record": record,
                "lane": "discovery_self_tier",
            })

        return result

    def get_feedback_report(self, issue: Dict[str, str]) -> Dict[str, Any]:
        """User-reported issue from feedback ledger"""
        report = {
            "source": "user",
            "type": issue.get("type", "general"),
            "severity": issue.get("severity", "medium"),
            "message": issue.get("message", ""),
            "timestamp": self._timestamp(),
            "status": "open",
        }
        self.state["feedback"].append(report)
        return {"ok": True, "report_id": hashlib.md5(json.dumps(report).encode()).hexdigest()[:12]}

    def sync_state(self) -> Dict[str, Any]:
        """Get current system state for UI (stated vs revealed intent reconciliation)"""
        return {
            "pipeline": self.state["pipeline"],
            "intent": self.state["intent"],
            "primary": self.state["primary"],
            "wip": {"count": len(self.state["wip"]), "slots": self.state["wip"][:3]},
            "harness": self.state["harness"],
            "feedback_count": len(self.state["feedback"]),
            "feedback_recent": self.state["feedback"][-5:],  # last 5
        }

    def set_harness_mode(self, mode: str) -> Dict[str, Any]:
        """Set resource harness mode: balanced | ai-led | human-led | capital-injection"""
        harness_configs = {
            "balanced": {"human": 0.5, "machine": 0.3, "capital": 0.2},
            "ai-led": {"human": 0.2, "machine": 0.6, "capital": 0.2},
            "human-led": {"human": 0.7, "machine": 0.2, "capital": 0.1},
            "capital-injection": {"human": 0.3, "machine": 0.2, "capital": 0.5},
        }

        if mode not in harness_configs:
            return {"error": f"Invalid mode: {mode}. Choose: {list(harness_configs.keys())}"}

        self.state["harness_mode"] = mode
        self.state["harness"] = harness_configs[mode]
        return {"ok": True, "mode": mode, "harness": self.state["harness"]}

    def _timestamp(self) -> str:
        """ISO 8601 timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# Flask app wrapper for local testing
def create_app():
    from flask import Flask, request, jsonify

    app = Flask(__name__)
    bridge = APIBridge()

    @app.route("/gate/registry", methods=["POST"])
    def registry_submission():
        """Submit record to registry gate"""
        try:
            record = request.get_json()
            result = bridge.process_registry_submission(record)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/feedback/report", methods=["POST"])
    def feedback_report():
        """Report issue from UI feedback ledger"""
        try:
            issue = request.get_json()
            result = bridge.get_feedback_report(issue)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/state/sync", methods=["GET"])
    def sync_state():
        """Get current system state"""
        return jsonify(bridge.sync_state()), 200

    @app.route("/harness/set", methods=["POST"])
    def set_harness():
        """Set resource harness mode"""
        try:
            data = request.get_json()
            mode = data.get("mode")
            result = bridge.set_harness_mode(mode)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app


if __name__ == "__main__":
    # For local testing: python api_bridge.py
    # Then open http://localhost:5000/state/sync in browser
    app = create_app()
    print("Starting API bridge on http://localhost:5000")
    print("Endpoints:")
    print("  POST /gate/registry       — Submit record to registry gate")
    print("  POST /feedback/report     — Report issue")
    print("  GET  /state/sync          — Get system state")
    print("  POST /harness/set         — Set resource harness mode")
    app.run(debug=True, port=5000)
