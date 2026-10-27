#!/usr/bin/env python3
"""Synthetic offline side-effect witness. No external systems or credentials."""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path
from urllib.parse import quote

def init(db):
    with sqlite3.connect(db) as c:
        c.execute("CREATE TABLE IF NOT EXISTS approvals (task TEXT PRIMARY KEY, approved INTEGER NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS effects (task TEXT PRIMARY KEY, payload TEXT NOT NULL)")

def approve(db, task):
    with sqlite3.connect(db) as c:
        c.execute("INSERT OR REPLACE INTO approvals VALUES (?,1)", (task,))

def act(db, task, crash=False):
    with sqlite3.connect(db) as c:
        row = c.execute("SELECT approved FROM approvals WHERE task=?", (task,)).fetchone()
        if row != (1,):
            return 3
        c.execute("INSERT OR IGNORE INTO effects VALUES (?,?)", (task, "synthetic-effect-v1"))
        c.commit()
    if crash:
        # Crash only this disposable synthetic worker after commit, before ACK.
        os._exit(23)
    return 0

def witness(db, task):
    db_uri = "file:" + quote(str(Path(db).resolve()), safe="/") + "?mode=ro"
    c = sqlite3.connect(db_uri, uri=True)
    try:
        rows = c.execute("SELECT task,payload FROM effects ORDER BY task").fetchall()
        approved = c.execute("SELECT approved FROM approvals WHERE task=?", (task,)).fetchone()
    finally:
        c.close()
    only = [row for row in rows if row[0] == task]
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"schema": "humanaios.synthetic-offline-witness.v0.1",
            "task": task, "committed_effects": len(only),
            "approved_in_synthetic_fixture": approved == (1,),
            "sink_sha256": digest, "source_type": "READ_ONLY_SECOND_PROCESS",
            "independent_attestation": False, "authority_effect": "NONE",
            "merge_authority": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("op", choices=["init", "approve", "act", "witness"])
    parser.add_argument("db")
    parser.add_argument("--task", default="synthetic-task-001")
    parser.add_argument("--crash-after-commit", action="store_true")
    args = parser.parse_args()
    if args.op == "init":
        init(args.db)
        return 0
    if args.op == "approve":
        approve(args.db, args.task)
        return 0
    if args.op == "act":
        return act(args.db, args.task, args.crash_after_commit)
    print(json.dumps(witness(args.db, args.task), sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
