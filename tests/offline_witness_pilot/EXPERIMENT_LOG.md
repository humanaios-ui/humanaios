# Synthetic Offline Execution / Separate-Process Witness — Qualification Log
**State:** OBSERVED **synthetic local experiment**, not E1 deployed-agent evidence or independent organizational attestation.  
**Date:** 2026-10-22. **Links:** humanaios#122, operations#974, security prerequisite PR #123.

## Frozen intention
Falsify three invariants inside a disposable SQLite sandbox with synthetic task `synthetic-task-001`: (a) a worker cannot create a side effect before a synthetic approval bit; (b) an authorized write survives a worker exit after commit but before acknowledgment; (c) retry with the same idempotency key yields one side effect, not two. Use a **separate read-only process** to inspect the sink before and after. No live services, credentials, public ports, databases or user exports.

## Executed locally
A source-equivalent prototype was executed in an isolated temporary directory, with a separate read-only observer subprocess and a synthetic approval fixture. The local executable's SHA-256 was `2b5ecd9adcfc024b50edfc5bba7510c9b60e7b53989d5d6dd96b5a65cc074d1a`; its test SHA-256 was `078a8a9972ec3a8c456721707b23655467041c856f6af8955cc2624f500cca97`. **These hashes refer to the *local tested scripts*, not to the reformatted source committed in this PR.** The exact repository version must pass its own CI job before claiming even branch-level reproducibility.

| Step | Separate process exit | Read-only sink count |
|---|---:|---:|
| Initialize synthetic sink | 0 | — |
| Attempt effect without approval | 3 (denied) | 0 |
| Set **synthetic** approval fixture | 0 | 0 |
| Worker writes, commits, then exits before ACK | 23 (injected worker termination) | 1 |
| New worker retries same key | 0 | 1 |

The independent read-only *process* observed the same sink digest both after crash and retry: `42d7aa69c641ca8fdca1ba69e7177e255bfce7d02a71b4243500e5e8b6cfa1e0`. Local Python unittest: **1 test passed** (first invocation encountered environment-related timeout; timeout bound was then increased from 15 to 45 seconds and the repeat succeeded). Report the failed first attempt, not only the successful retest.

## Strict evidence boundaries
- **SUPPORTED for synthetic fixture only:** The temporary SQLite worker recovered from after-commit/before-ACK termination without duplicating the sink row; denied action created no sink effect.
- **UNVERIFIED:** Human authorization, real INTENT-OS/API bridge runtime, cloud durable state, network partitions, post-outage delivery, authentic user disconnect, tenant-specific authorization, independent external side-effect sink, production resilience, 30-day randomly sampled logs.
- Separate executable observer is **not** an independently governed auditor. No cryptographic external witness/attestation was obtained.
- This program is *not* a test of the API bridge in PR #123; its objective is to qualify a witness harness before integrating with a real worker.
- **Claim C1: INCONCLUSIVE. Claim C2: NOT TESTED. authority_effect=NONE. merge_authority=false.**

## Next independently witnessed experiment — NOT YET AUTHORIZED
Human-approved, sandbox-scoped exercise must name the bridge deployment SHA, host/network boundaries, actor, real external sink, repeatable task, operator and **independent witness not controlled by the same worker**. Collect a signed sink receipt before and after fault injection and verify denial/approval/replay and exact-head CI. Do not crash a live service or substitute the synthetic `approve` CLI for a real human approval record.
