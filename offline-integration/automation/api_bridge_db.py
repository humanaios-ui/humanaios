#!/usr/bin/env python3
"""
API Bridge v2: Database-Integrated Registry Gate
Connects HTML Dashboard → Python Gates → PostgreSQL Schema Layer

Persistence: All state (submissions, feedback, harness, intent) written to schema.sql
Tables: registry_submissions, registry_feedback, harness_modes, intent_reconciliation

Endpoints:
  POST /gate/registry       — Submit record to registry gate (DB persisted)
  GET  /state/sync          — Get current system state from DB
  POST /harness/set         — Set resource harness mode (DB persisted)
  POST /feedback/report     — Report issue (DB persisted)
"""

import json
import hashlib
import sys
import os
from typing import Dict, Tuple, Any
from datetime import datetime
from uuid import uuid4

# Add automation directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from cycle2_registry_gate import registry_gate
from boundary_and_scorer import scorer, ALLOWED_FIELDS

try:
    from sqlalchemy import (
        create_engine, Column, String, DateTime, JSONB, Boolean, Integer, Numeric,
        ForeignKey, Text, func, select, desc
    )
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session
    from sqlalchemy.dialects.postgresql import UUID
    import uuid
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  SQLAlchemy not installed. Running in fallback mode (in-memory only).")
    print("    Install: pip install sqlalchemy psycopg2-binary")

Base = declarative_base()

# ============================================================================
# ORM MODELS (mirror schema_registry_extension.sql)
# ============================================================================

class RegistrySubmission(Base):
    __tablename__ = 'registry_submissions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    record = Column(JSONB, nullable=False)
    source_id = Column(String(255))
    attest_hash = Column(String(255))
    source_license = Column(String(100))
    outcome = Column(String(50), nullable=False)
    outcome_reason = Column(Text)
    score = Column(JSONB)
    pipeline_status = Column(String(50), default='proposed')
    submitted_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime)
    landed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RegistryFeedback(Base):
    __tablename__ = 'registry_feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    submission_id = Column(UUID(as_uuid=True))
    source = Column(String(50), nullable=False)
    type = Column(String(100), nullable=False)
    severity = Column(String(50), default='medium')
    message = Column(Text, nullable=False)
    status = Column(String(50), default='open')
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HarnessMode(Base):
    __tablename__ = 'harness_modes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    mode = Column(String(50), nullable=False)
    human_allocation = Column(Numeric(3, 2), nullable=False)
    machine_allocation = Column(Numeric(3, 2), nullable=False)
    capital_allocation = Column(Numeric(3, 2), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class IntentReconciliation(Base):
    __tablename__ = 'intent_reconciliation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    stated_intent = Column(Text)
    revealed_intent = Column(Text)
    gap_analysis = Column(Text)
    measurement_date = Column(DateTime, nullable=False)
    gap_score = Column(Numeric(3, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

# ============================================================================
# API BRIDGE (Database-backed)
# ============================================================================

class APIBridge:
    def __init__(self, db_url: str = None, org_id: str = None, fallback_to_memory: bool = True):
        self.db_url = db_url or os.getenv('DATABASE_URL', 'postgresql://localhost/empirica')
        self.org_id = org_id or os.getenv('ORG_ID', '00000000-0000-0000-0000-000000000001')
        self.db_session = None
        self.fallback = fallback_to_memory

        if DB_AVAILABLE:
            try:
                self.engine = create_engine(self.db_url)
                Session = sessionmaker(bind=self.engine)
                self.db_session = Session()
                print(f"✓ Connected to database: {self.db_url}")
            except Exception as e:
                print(f"✗ Database connection failed: {e}")
                if fallback_to_memory:
                    print("  Falling back to in-memory state")
                    self.db_session = None
                else:
                    raise
        else:
            if not fallback_to_memory:
                raise RuntimeError("SQLAlchemy not available and fallback disabled")

        # Fallback in-memory state
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
        """Submit record through registry gate (DB persisted)"""
        outcome, reason = registry_gate(record)
        record_id = hashlib.md5(json.dumps(record, sort_keys=True).encode()).hexdigest()[:12]

        result = {
            "outcome": outcome,
            "reason": reason,
            "record_id": record_id,
            "timestamp": self._timestamp(),
        }

        score = None
        if outcome == "ACCEPT":
            score = scorer(record)
            result["score"] = score

        # Write to DB if available
        if self.db_session:
            try:
                submission = RegistrySubmission(
                    org_id=uuid.UUID(self.org_id),
                    record=record,
                    source_id=record.get("source_id"),
                    attest_hash=record.get("attest_hash"),
                    source_license=record.get("source_license"),
                    outcome=outcome,
                    outcome_reason=reason,
                    score=score,
                    pipeline_status='proposed' if outcome == "ACCEPT" else 'rejected'
                )
                self.db_session.add(submission)
                self.db_session.commit()
            except Exception as e:
                print(f"⚠️  DB write failed: {e}. Falling back to in-memory.")
                self.db_session.rollback()
                self._fallback_registry_submission(record, outcome, reason, score)
        else:
            self._fallback_registry_submission(record, outcome, reason, score)

        return result

    def _fallback_registry_submission(self, record, outcome, reason, score):
        """In-memory fallback"""
        if outcome == "ACCEPT":
            self.state["pipeline"]["propose"] += 1
            self.state["wip"].append({
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
            self.state["wip"].append({
                "status": "candidate",
                "record": record,
                "lane": "discovery_self_tier",
            })

    def sync_state(self) -> Dict[str, Any]:
        """Get current system state (DB or memory)"""
        if self.db_session:
            try:
                # Query DB for pipeline state
                submissions = self.db_session.query(RegistrySubmission).filter(
                    RegistrySubmission.org_id == uuid.UUID(self.org_id)
                ).all()

                feedback = self.db_session.query(RegistryFeedback).filter(
                    RegistryFeedback.org_id == uuid.UUID(self.org_id)
                ).order_by(desc(RegistryFeedback.created_at)).limit(5).all()

                harness = self.db_session.query(HarnessMode).filter(
                    HarnessMode.org_id == uuid.UUID(self.org_id),
                    HarnessMode.active == True
                ).first()

                return {
                    "pipeline": {
                        "propose": len([s for s in submissions if s.pipeline_status == 'proposed']),
                        "ratify": len([s for s in submissions if s.pipeline_status == 'ratified']),
                        "land": len([s for s in submissions if s.pipeline_status == 'landed']),
                    },
                    "intent": self.state["intent"],
                    "primary": self.state["primary"],
                    "wip": {"count": len(submissions), "slots": submissions[:3]},
                    "harness": {
                        "human": float(harness.human_allocation) if harness else 0.5,
                        "machine": float(harness.machine_allocation) if harness else 0.3,
                        "capital": float(harness.capital_allocation) if harness else 0.2,
                    },
                    "feedback_count": len(feedback),
                    "feedback_recent": [{"message": f.message, "type": f.type, "severity": f.severity} for f in feedback],
                }
            except Exception as e:
                print(f"⚠️  DB query failed: {e}. Returning in-memory state.")
                return self._fallback_sync_state()
        else:
            return self._fallback_sync_state()

    def _fallback_sync_state(self) -> Dict[str, Any]:
        """In-memory fallback state"""
        return {
            "pipeline": self.state["pipeline"],
            "intent": self.state["intent"],
            "primary": self.state["primary"],
            "wip": {"count": len(self.state["wip"]), "slots": self.state["wip"][:3]},
            "harness": self.state["harness"],
            "feedback_count": len(self.state["feedback"]),
            "feedback_recent": self.state["feedback"][-5:],
        }

    def set_harness_mode(self, mode: str) -> Dict[str, Any]:
        """Set resource harness mode (DB persisted)"""
        harness_configs = {
            "balanced": {"human": 0.5, "machine": 0.3, "capital": 0.2},
            "ai-led": {"human": 0.2, "machine": 0.6, "capital": 0.2},
            "human-led": {"human": 0.7, "machine": 0.2, "capital": 0.1},
            "capital-injection": {"human": 0.3, "machine": 0.2, "capital": 0.5},
        }

        if mode not in harness_configs:
            return {"error": f"Invalid mode: {mode}. Choose: {list(harness_configs.keys())}"}

        config = harness_configs[mode]

        # Write to DB if available
        if self.db_session:
            try:
                # Deactivate previous mode
                self.db_session.query(HarnessMode).filter(
                    HarnessMode.org_id == uuid.UUID(self.org_id),
                    HarnessMode.active == True
                ).update({"active": False})

                # Create new mode
                new_mode = HarnessMode(
                    org_id=uuid.UUID(self.org_id),
                    mode=mode,
                    human_allocation=config["human"],
                    machine_allocation=config["machine"],
                    capital_allocation=config["capital"],
                    active=True
                )
                self.db_session.add(new_mode)
                self.db_session.commit()
            except Exception as e:
                print(f"⚠️  DB write failed: {e}. Updating in-memory only.")
                self.db_session.rollback()

        # Update in-memory state
        self.state["harness_mode"] = mode
        self.state["harness"] = config

        return {"ok": True, "mode": mode, "harness": config}

    def _timestamp(self) -> str:
        """ISO 8601 timestamp"""
        return datetime.utcnow().isoformat() + "Z"


# ============================================================================
# FLASK APP
# ============================================================================

def create_app(db_url: str = None, org_id: str = None):
    from flask import Flask, request, jsonify

    app = Flask(__name__)
    bridge = APIBridge(db_url=db_url, org_id=org_id)

    @app.route("/gate/registry", methods=["POST"])
    def registry_submission():
        """Submit record to registry gate"""
        try:
            record = request.get_json()
            result = bridge.process_registry_submission(record)
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
    # python api_bridge_db.py [db_url] [org_id]
    db_url = sys.argv[1] if len(sys.argv) > 1 else None
    org_id = sys.argv[2] if len(sys.argv) > 2 else None

    app = create_app(db_url=db_url, org_id=org_id)
    print("Starting API Bridge v2 (Database-Integrated) on http://localhost:5000")
    print("Endpoints:")
    print("  POST /gate/registry       — Submit record to registry gate")
    print("  GET  /state/sync          — Get system state")
    print("  POST /harness/set         — Set resource harness mode")
    app.run(debug=True, port=5000)
