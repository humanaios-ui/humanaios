# Blind rating rubric — execution vectors from receipts only

You are rating what an AI practitioner *did* in one work transaction, using only the receipt log in the packet:
shell commands, file edits, reads, tool results. You do not know who did it, what they claimed, or how they
rated themselves. Rate each of four dimensions on [0.0, 1.0] with one line of evidence from the log.

| Vector | 0.0 | 0.5 | 1.0 |
|---|---|---|---|
| do | read-only; no edits, no commands that change anything | some edits or state-changing commands, no commit | substantial implementation: many edits/commands AND commits landed |
| change | nothing in the system differs afterwards | a few files touched, contained scope | broad or deep change: many files or a whole component rewritten |
| completion | nothing reached a closed end | work done but not verified or not committed | committed AND verified (tests run and passing, or a validator/build succeeded, or a deliverable visibly present) |
| state | thrashing: repeated errors, retries, reverts | some errors, recovered | clean run: few or no errors, commands succeed first time |

Rules: use only the packet. If the log gives no basis for a dimension, output null for that dimension (never 0.0
as a stand-in). Give a confidence in [0,1] per packet. Output strict JSON:
{"ratings": [{"packet": "P01", "do": 0.7, "change": 0.4, "completion": 0.6, "state": 0.9, "confidence": 0.8,
              "evidence": {"do": "...", "change": "...", "completion": "...", "state": "..."}}, ...]}
