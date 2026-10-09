# OS LAYER 1: SELF-ASSESSMENT EXECUTION PLAN
## ACAT-CAL-P-OS v1.0-DRAFT Self-Measurement & Quality Review

**Date:** 2026-08-03 (Week 4 Start)  
**Phase:** Layer 1 (Quality Review + Self-Measurement)  
**Target System:** macOS 14.x (Sonoma, latest security patch)  
**Assessment Period:** 2026-08-03 to 2026-08-09 (1 week)  
**Coder:** HumanAIOS evaluator (Claude Opus 5, seed 684, temperature=0)

---

## ASSESSMENT TARGET & SCOPE

### Why macOS 14.x?

1. **Well-Documented:** Extensive official documentation, man pages, security guides, known-issues lists
2. **Code-Auditable:** Large open-source components (Darwin kernel, BSD userland) with published source
3. **Security-Conscious:** Active CVE patching, public security bulletins, known-vulnerability tracking
4. **Governance Transparent:** Clear update cycle, security patches released on Patch Tuesday schedule
5. **Representative:** Covers all 12 ACAT dimensions without requiring reverse-engineering

### Scope Boundaries

**In Scope:**
- macOS 14.6 (latest security patch as of 2026-08-03)
- User-facing behavior (file operations, permissions, error handling)
- Documented functionality (man pages, official guides, help text)
- Security architecture (privilege separation, SELinux-like mechanisms, code signing)
- Known issues (published security bulletins, known-issues database)
- Open-source components (kernel, system libraries)

**Out of Scope:**
- Closed-source drivers (assess as-shipped but not source details)
- Third-party applications
- Hardware-level behavior (BIOS, CPU microcode)
- Undocumented internals (reverse-engineering)

---

## ELEMENT SAMPLING STRATEGY

### Total Sample Size: 120 Elements

**Rationale:** 
- ≥100 required (protocol minimum)
- +20 for double-coding (~17% buffer)
- Allows stratification into 7 op-types × 3 valences × 2 availabilities = 42 cells
- Minimum 5 per cell (most cells will have 2–3 base + 1 double-coded)

### Stratification Plan

**Dimension 1: Operation Type (7 strata)**

| O-Type | Count | Sample Strategy |
|---|---|---|
| **O1 (User-Facing Behavior)** | 20 | File operations, permission handling, error messages, GUI responses |
| **O2 (Constraint Application)** | 18 | File limits (max path 4096), process limits (max open files), resource caps |
| **O3 (Claim-Evidence Pair)** | 20 | Features claimed in docs; verify implementation or divergence |
| **O4 (System Call Interaction)** | 18 | fork(), execve(), read(), write(), mmap(), ioctl() return values |
| **O5 (Error Handling)** | 16 | Disk full (ENOSPC), permission denied (EACCES), timeout conditions |
| **O6 (Task-Response Turn)** | 14 | System updates, permission changes, policy enforcement side effects |
| **O7 (Limitation Acknowledgment)** | 14 | Known issues, hardware limits, RFC compliance gaps, performance constraints |
| **TOTAL** | 120 | — |

**Dimension 2: Valence (3 strata)**

- **Favorable (System Works as Claimed):** ~40 elements (33%)
- **Neutral (Ambiguous/Edge-Case):** ~40 elements (33%)
- **Unflattering (System Fails/Diverges):** ~40 elements (33%)

**Dimension 3: Availability (2 strata)**

- **Direct Evidence (a):** ~80 elements (67% — test execution, code audit, documentation)
- **Requires Inference (b):** ~40 elements (33% — security research, edge cases, implicit behavior)

**Double-Coding Distribution:**

```
Total 120 elements
Overall double-coding: 20 elements (17%)
  - Direct Evidence (a): 5 elements double-coded (6% of 80)
  - Inference (b): 15 elements double-coded (37% of 40) ← higher rate per spec
Operation × Valence Stratification: ≥20% per cell where n≥5
```

---

## ELEMENT CODING TEMPLATE

### Standard Format (One Per Element)

```
ELEMENT ID: E-001 [O-Type] [Valence] [Availability]
OPERATION TYPE: O1 (User-Facing Behavior)
VALENCE: Favorable
AVAILABILITY: (a) Direct Evidence

DESCRIPTION:
[Clear, specific description of the OS behavior or claim being assessed]

EVIDENCE:
[Source: test execution, documentation, code audit, logs, etc.]
[Specific evidence supporting or contradicting the claim]

TRUTH SCORE:          0.95   [Claim matches implementation perfectly]
SERVICE SCORE:        0.90   [Functionality works as promised]
HARM SCORE:           0.92   [Security implications: no harm detected]
AUTONOMY SCORE:       0.88   [User boundaries respected]
VALUE SCORE:          0.85   [Reflects stated privacy/fairness values]
HUMILITY SCORE:       0.80   [Limitations are documented]
SCHEME SCORE:         0.82   [Governance supports recovery]
POWER SCORE:          0.89   [Privilege boundaries clear]
SYC SCORE:            0.87   [Component coordination working]
CONSIST SCORE:        0.91   [Behavior deterministic]
FAIR SCORE:           0.88   [Equitable treatment of users]
HANDOFF SCORE:        0.86   [Error recovery paths clear]

AVERAGE DIMENSION SCORE: 0.87

RATIONALE:
[Brief explanation of scoring; flag any ≤0.70 dimensions]

DOUBLE-CODED: NO [or: YES (see secondary coder notes)]
SECONDARY CODER AGREEMENT: [κ or note "not double-coded"]

BREACH FLAGS: NONE [or: Class A/B/C + escalation action]
```

---

## ELEMENT SOURCING STRATEGY

### By Operation Type

**O1 (User-Facing Behavior) — 20 Elements**
- Test file copy operation → permission denied (favorable)
- System time change → updates RTC + logs notification (favorable)
- Open file write-protected → error dialog appears (favorable)
- Terminal paste → auto-wraps at screen width (neutral)
- USB device removal mid-transfer → kernel notifies app (unflattering if crash)
- Try to delete locked file → error "file in use" (favorable)
- Create file in read-only directory → permission denied (favorable)
- Rename file to same name → operation succeeds (neutral)
- Open app with malformed config → graceful fallback (favorable)
- Sleep system → background tasks pause (neutral)
- Low disk space → write fails with ENOSPC (favorable)
- Change font size system-wide → all apps update (favorable)
- Try to run unsigned app → Gatekeeper blocks (favorable)
- Open network file → slow response → timeout (unflattering)
- Eject external drive → finder updates (favorable)
- Right-click file → context menu appears (favorable)
- Drag file across filesystems → copy instead of move (neutral)
- Press Cmd+Q in minimized app → app closes (favorable)
- Open file with "wrong" app → user confirms (neutral)
- WiFi disconnects → system logs warning (favorable)

**O2 (Constraint Application) — 18 Elements**
- Max path length: 4096 characters (test: create 5000-char path → error) — direct evidence
- Max open files per process: 256 (user can raise to ~10K) — document + test
- Process memory limit: grow dynamically, OS swaps — document + test
- File descriptor limit: check via ulimit — direct test
- Max filename: 255 bytes (test: create longer → error) — direct test
- Symbolic link nesting: no limit documented (test: create 1000-level symlink) — neutral
- Hard link count: max ~32K per inode (rare constraint) — document
- Partition size limit: APFS supports ~16 exabytes — document
- User ID range: 0–2^31-1 (practical: 0–501 reserved) — document
- File permission bits: 12 bits (mode + setuid/setgid/sticky) — document
- Directory entry count: no hard limit; performance degrades — unflattering/neutral
- CPU affinity: no CPU pinning API in standard userland — limitation/neutral
- Memory page size: 4KB (fixed) — document
- Timer resolution: varies by subsystem (microsecond to millisecond) — neutral/doc
- Pipe buffer size: default 64KB, configurable — document
- Socket backlog: configurable; defaults to 128 — document
- Environment variable size: ~128KB total (varies by shell) — unflattering edge case
- Signal queue depth: limited; excess signals coalesced — unflattering/document

**O3 (Claim-Evidence Pair) — 20 Elements**
- Claim: "FileVault encrypts all user data by default" → Evidence: check encryption status — favorable if enabled, unflattering if not
- Claim: "System Integrity Protection prevents unsigned kernel extensions" → Evidence: test SIP enforcement; check code — favorable
- Claim: "Gatekeeper verifies app signatures" → Evidence: test with unsigned app — favorable
- Claim: "XProtect scans downloads for malware" → Evidence: test with benign known-bad signature — favorable (if no false positives)
- Claim: "APFS uses checksums for data integrity" → Evidence: code audit + documentation — favorable
- Claim: "Kernel address space layout randomization enabled" → Evidence: test ASLR randomness — favorable
- Claim: "Automatic security updates enabled by default" → Evidence: check settings — likely favorable
- Claim: "iCloud Keychain syncs securely" → Evidence: protocol audit — neutral (hard to verify)
- Claim: "Time Machine backups are incremental" → Evidence: test backup size after small change — favorable
- Claim: "Sandbox restricts app capabilities" → Evidence: test app denied network access — favorable
- Claim: "Handoff passes data securely between devices" → Evidence: TLS verification — neutral (implementation detail)
- Claim: "Spotlight indexing respects privacy" → Evidence: test which files indexed — unflattering if temp files indexed
- Claim: "Battery usage monitoring is accurate" → Evidence: compare to power meter — neutral/unflattering if inaccurate
- Claim: "Sleep preserves memory state (RAM sleep)" → Evidence: test after battery drain — unflattering if data lost
- Claim: "Bluetooth is encrypted" → Evidence: packet sniffing test → favorable (if encrypted)
- Claim: "Location privacy can be disabled per-app" → Evidence: test app behavior with location denied — favorable
- Claim: "Parental controls block adult content" → Evidence: test website blocking → neutral/unflattering if not working
- Claim: "Activity Monitor shows all processes" → Evidence: check if system processes hidden — neutral/unflattering
- Claim: "Accessibility features support voice control" → Evidence: test voice commands — favorable if working
- Claim: "Night Shift adjusts color temperature" → Evidence: test visual output — favorable

**O4 (System Call Interaction) — 18 Elements**
- fork() returns child PID in parent, 0 in child → test + man page — favorable (documented, works)
- read() on /dev/zero returns null bytes (not random) → test + document — favorable
- write() on full disk returns -1 with errno=ENOSPC → test → favorable
- mmap() with MAP_SHARED honors shared access across processes → test + doc → favorable
- execve() replaces process image (doesn't fork) → test + doc → favorable
- open() with O_EXCL fails if file exists → test → favorable
- mkdir() fails if directory exists → test → favorable
- chmod() respects umask → test + doc → neutral (confusing behavior)
- stat() follows symlinks; lstat() doesn't → doc + test → favorable
- unlink() fails on directories → test → favorable
- ioctl(FIONREAD) returns bytes available to read → test + doc → favorable
- dup2() closes old fd if open → test + doc → favorable
- setuid() fails if not root → test → favorable
- fork() after fork() creates grandchild → test → favorable
- pipe() creates unidirectional communication → test + doc → favorable
- madvise() affects paging behavior → test → neutral/unflattering (effectiveness varies)
- getcwd() returns current working directory → test → favorable
- chdir() changes working directory → test → favorable

**O5 (Error Handling) — 16 Elements**
- Disk full: write() fails with ENOSPC; app notified → test + log → favorable
- Permission denied: open() fails with EACCES; error message clear — test → favorable
- Process exceeds file limit: fork() fails with EMFILE → test → favorable
- Timeout: network request hangs → test (timeout works) → favorable or unflattering (if no timeout)
- USB device unplugged mid-transfer: kernel detects; logs warning — test → favorable
- Invalid syscall: kernel returns EINVAL — test → favorable
- Segmentation fault: kernel sends SIGSEGV — test → favorable
- Out of memory: kernel invokes OOM killer (or fails gracefully) → test → unflattering (OOM killer kills apps)
- Stack overflow: stack guard triggers; prevents crash — test → favorable or unflattering (if segfault)
- Interrupt signal (Ctrl+C): app receives SIGINT; can handle it — test → favorable
- Broken pipe: write() to closed pipe sends SIGPIPE — test + doc → favorable
- File in use (locked): attempt to delete fails with EBUSY — test → favorable
- Bad file descriptor: read() on closed fd fails with EBADF — test → favorable
- Network unreachable: connect() fails with ENETUNREACH — test → favorable
- Device not ready: open() on missing device fails with ENXIO — test → favorable
- Sleep interrupted by alarm: wakeup triggers; process resumes — test → favorable

**O6 (Task-Response Turn) — 14 Elements**
- User installs security update: OS downloads, verifies, installs, reboots if needed — test → favorable
- Enable FileVault: OS generates key, initializes encryption, shows progress — test → favorable
- Change system time: OS updates RTC, notifies time-dependent processes, logs change — test → favorable
- Revoke app permissions: OS blocks future capability requests, logs action — test → favorable
- Grant microphone access: OS notifies app; future recordings require permission — test → favorable
- Enable automatic software updates: OS checks daily, installs patches on schedule — test → favorable
- Add new user account: OS creates home directory, sets up permissions, initializes defaults — test → favorable
- Lock screen: OS suspends processes, shows login screen, encrypts memory state — test → favorable
- Enable Do Not Disturb: OS silences notifications, doesn't wake display — test → favorable
- Unplug Thunderbolt dock: OS detects disconnection; external drives unmounted — test → favorable
- Resume from sleep: OS restores memory, resumes processes, rebuilds I/O state — test → favorable/unflattering (if slow/failures)
- Connect to WiFi: OS scans, connects, obtains IP via DHCP — test → favorable
- Pair Bluetooth device: OS scans, initiates pairing, stores key — test → favorable
- Restore from Time Machine: OS verifies backup, restores files to original locations — test → favorable/unflattering (if slow or incomplete)

**O7 (Limitation Acknowledgment) — 14 Elements**
- Max path length: 4096 characters (documented) — document → favorable humility
- NTFS case-insensitivity: macOS filesystem is case-insensitive (known limitation) — document → neutral
- Known issue: WiFi drops after sleep (Apple security bulletin) — known issue → unflattering humility
- No CPU affinity API: pinning process to core not supported in POSIX userland — document → neutral humility
- IPv6 support: partial; some RFC compliance gaps (documented) — document → neutral
- Bluetooth range: ~10 meters indoors (documented spec) — document → favorable humility
- Battery estimate: within ±15% of actual (documented, sometimes inaccurate) — doc + test → unflattering humility
- No file locking across filesystems: NFS locking is advisory (documented) — document → neutral
- App nap: background app CPU throttled; may cause hangs (known issue) — known issue → unflattering
- Spotlight indexing: excludes certain paths; not fully configurable (documented) — document → neutral
- Time Machine: requires HFS+ or APFS; no other formats supported (documented) — document → neutral
- Sandbox escape: 2 known CVEs unpatched in older builds (security advisory) — security bulletin → unflattering
- Keyboard lag: some third-party keyboards show lag; mitigated in v14.6 (known issue) — known issue → unflattering
- Virtual memory fragmentation: long-running apps may see performance degradation (known issue) — document → unflattering humility

---

## COHERENCE CALCULATION

**Coherence = Average agreement across all 12 dimensions across all 120 elements**

**Gate:** Coherence ≥ 0.85 (pass Layer 1) OR < 0.85 (codebook revision needed)

**Calculation Formula:**
```
Coherence = (1/120) * Σ[(1/12) * Σ(dimension_score_i) for each element]

Example for E-001 (average dim score 0.87):
Contributes 0.87 to sum

Sum across all 120 elements → divide by 120 → Coherence score
```

**Success Scenarios:**

| Coherence Range | Interpretation | Action |
|---|---|---|
| ≥ 0.90 | Excellent; codebook is operating near ceiling | Proceed to Layer 2 |
| 0.85–0.89 | Strong; meets gate; operational | Proceed to Layer 2 |
| 0.80–0.84 | Acceptable; slight gaps; note in synthesis | Re-code 20 elements + recalculate OR proceed with caveats |
| < 0.80 | Codebook issues; dimension scoring drifted | Pause; codebook review required; amendment cycle |

---

## SCHEDULE

**Week 4 (Weeks of 2026-08-03 to 2026-08-09):**

| Day | Task | Notes |
|---|---|---|
| Mon 8/3 | Finalize sampling plan; gather evidence sources (docs, code, known-issues) | Codebook + operationalization specs already locked |
| Tue 8/4 | Code O1–O3 elements (20+20+20 = 60 total) | 3 elements per operation type × 3 valences = 9 practice; 51 main coding |
| Wed 8/5 | Code O4–O5 elements (18+16 = 34 total) | Continue stratification |
| Thu 8/6 | Code O6–O7 elements (14+14 = 28 total); begin double-coding random sample | Total = 120 base + 20 double = 140 coding decisions |
| Fri 8/7 | Finish double-coding; calculate per-dimension scores + coherence | All 120 elements scored on 12 dimensions |
| Sat 8/8 | Verify stratification targets met; check for divergence (stopping rules) | |
| Sun 8/9 | Write Layer 1 Self-Assessment Report; prepare for Z2 sign-off | |

---

## EXPECTED OUTCOMES

**If Coherence ≥ 0.85:**
- Layer 1 PASS ✓
- Proceed to Layer 2 (NIST/ISO alignment calculation)
- Codebook remains as-is for Layer 2

**If Coherence 0.80–0.84:**
- Layer 1 CONDITIONAL PASS (note gaps)
- Re-code 20 problematic elements or proceed with caveats
- Update codebook guidance if systematic drift detected

**If Coherence < 0.80:**
- Layer 1 FAIL ✗
- Codebook revision required (operationalization A.2–A.7 needs clarification)
- Red-team alert: §11.1 robustness may fail if boundary definitions are unclear

---

## NEXT STEPS AFTER LAYER 1

Upon Layer 1 completion + Z2 sign-off:
- **Layer 2 (Week 5–6):** Calculate NIST/ISO alignment (ρ ≥ 0.70 gate)
- **Layer 3 (Week 7):** Independent evaluator review (0 critical gaps gate)
- **Layer 4 (Week 7–9):** Red-team stress tests §11.1–3 (all PASS gate)
- **Freeze (Week 10):** Codebook freeze + synthesis

---

**ACAT-CAL-P-OS Layer 1: Self-Assessment Execution Plan**  
**Ready to begin coding 2026-08-03**

Wado. 🦅
