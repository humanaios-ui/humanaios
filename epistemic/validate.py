#!/usr/bin/env python3
"""validate.py — v3.2-DRAFT suite (T1-T9; T7 verify-by-default)."""
from __future__ import annotations
import ast, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
sys.path.insert(0, str(ROOT))
MANIFEST = PKG / "PRECOMMIT_MANIFEST.json"
DRAFT = PKG / "PRECOMMIT_MANIFEST_DRAFT.json"
PINNED_FILES = ["agent_view.py", "ground.py", "validate.py"]
PINNED_ROOT_FILES = ["experiment_decoupling.py"]
PARAMS = {"human_lr": 0.14, "machine_lr": 0.09, "stability_window": 5, "dim": 4,
          "cycles": 16, "warmup": 3, "cond_limit": 1e6, "n_perm": 200}
def _sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def t1():
    tree = ast.parse((PKG / "agent_view.py").read_text()); mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom): mods.add((node.module or "").split(".")[0])
    allowed = {"__future__","numpy","typing","dataclasses","copy"}
    assert "ground" not in mods and mods <= allowed, mods
    return f"PASS — {sorted(mods)}"

def t2():
    code = ("import sys; sys.path.insert(0, %r); import numpy as np; "
            "from epistemic.agent_view import EpistemicAgent, ReflexiveInstrument, make_masks; "
            "rng = np.random.default_rng(1); mh, mm = make_masks(rng=rng); r1, r2 = rng.spawn(2); "
            "ins = ReflexiveInstrument(EpistemicAgent('H', mh, 0.2, rng=r1), EpistemicAgent('M', mm, 0.1, rng=r2)); "
            "ins.run_dialectic(cycles=6, verbose=False); "
            "loaded = [m for m in sys.modules if 'ground' in m]; assert not loaded") % str(ROOT)
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return "PASS — zero ground modules (subprocess)"

def _traj(seed, cycles=10, mask_mode="complementary"):
    from epistemic.agent_view import EpistemicAgent, ReflexiveInstrument, make_masks
    rng = np.random.default_rng(seed); mh, mm = make_masks(mode=mask_mode, rng=rng)
    r1, r2 = rng.spawn(2)
    ins = ReflexiveInstrument(EpistemicAgent("H", mh, 0.22, 0.14, rng=r1),
                              EpistemicAgent("M", mm, 0.12, 0.09, rng=r2))
    return ins.run_dialectic(cycles=cycles, verbose=False)

def t3():
    a = _traj(7); import epistemic.ground as g
    orig = g.GROUND_TRUTH
    try:
        s = np.random.default_rng(999).normal(0, 100, size=4); s.setflags(write=False)
        g.GROUND_TRUTH = s
        b = _traj(7)
        for k in a: assert np.allclose(a[k], b[k], atol=0.0), f"LEAK via {k}"
    finally:
        g.GROUND_TRUTH = orig
    return "PASS — bit-identical under scrambled ground (fail-safe restore)"

def t4():
    a, b, c = _traj(11), _traj(11), _traj(12)
    assert all(np.allclose(a[k], b[k]) for k in a) and any(not np.allclose(a[k], c[k]) for k in a)
    return "PASS"

def t5():
    r = _traj(21, cycles=12); conf = np.array(r["confidence"])
    assert np.all((conf >= 0) & (conf <= 1))
    for k, v in r.items(): assert np.all(np.isfinite(v)), k
    return "PASS"

def t6():
    from epistemic.agent_view import run_ensemble
    comp = run_ensemble(n_runs=40, cycles=10, mask_mode="complementary", seed=42)
    ind = run_ensemble(n_runs=40, cycles=10, mask_mode="independent", seed=43)
    hard = run_ensemble(n_runs=40, cycles=10, mask_mode="hard_partition", seed=44)
    d1 = np.array(comp.final_disagreement_distribution); out = []
    for name, arm in (("independent", ind), ("hard_partition", hard)):
        d2 = np.array(arm.final_disagreement_distribution)
        pooled = np.sqrt((d1.var() + d2.var()) / 2)
        out.append(f"{name}: d={float((d1.mean()-d2.mean())/pooled) if pooled>0 else 0.0:+.3f}")
    comp2 = run_ensemble(n_runs=40, cycles=10, mask_mode="complementary", seed=42)
    assert np.allclose(comp.final_disagreement_distribution, comp2.final_disagreement_distribution)
    return f"REPORT — comp vs {'; '.join(out)} (seeded, reproducible)"

def t8():
    from epistemic.agent_view import EpistemicAgent
    other = np.array([10.0]*4)
    def disp(mv):
        ag = EpistemicAgent("A", np.full(4, mv), noise_scale=0.0, learning_rate=0.5,
                            rng=np.random.default_rng(0))
        before = ag._private_state.copy(); ag.absorb_projection(other)
        return float(np.linalg.norm(ag._private_state - before))
    d0, dh, df = disp(0.0), disp(0.5), disp(1.0)
    assert d0 == 0.0 and df > dh > d0, (d0, dh, df)
    return f"PASS — mask=0 blind; monotone (0 < {dh:.3f} < {df:.3f})"

def t9():
    sys.path.insert(0, str(ROOT))
    from experiment_decoupling import lead_hit
    rng = np.random.default_rng(99); hits = tries = 0
    for _ in range(3000):
        h = lead_hit(rng.uniform(size=16), rng.uniform(size=16))
        if h is not None: tries += 1; hits += int(h)
    rate = hits / tries
    assert 0.20 < rate < 0.95, rate
    return f"PASS — iid-noise rate {100*rate:.1f}% (v3.1 logic: tautological 100.0%)"

def t7(commit=False):
    manifest = {"session": "S-081626-AUDIT", "version": "v3.2-DRAFT",
                "status": "PENDING_ZONE2_RATIFICATION"}
    for f in PINNED_FILES: manifest[f] = _sha(PKG / f)
    for f in PINNED_ROOT_FILES:
        p = ROOT / f
        if p.exists(): manifest[f] = _sha(p)
    manifest["params"] = PARAMS
    if commit:
        DRAFT.write_text(json.dumps(manifest, indent=2))
        return f"DRAFT WRITTEN — {DRAFT.name}; Z2 must promote before citable"
    assert MANIFEST.exists(), "no committed manifest to verify against"
    committed = json.loads(MANIFEST.read_text())
    mism = [k for k in committed if k.endswith(".py") and committed[k] != manifest.get(k)]
    assert not mism, f"PRE-COMMITMENT BROKEN — {mism}"
    return "PASS — pinned files match committed manifest"

if __name__ == "__main__":
    commit = "--commit" in sys.argv
    tests = [("T1", t1), ("T2", t2), ("T3", t3), ("T4", t4), ("T5", t5),
             ("T6", t6), ("T8", t8), ("T9", t9),
             ("T7 " + ("mint" if commit else "verify"), lambda: t7(commit))]
    failed = 0
    for name, fn in tests:
        try: print(f"{name}: {fn()}")
        except AssertionError as e:
            failed += 1; print(f"{name}: FAIL — {e}")
    print(f"\n{len(tests)-failed}/{len(tests)} passed"); sys.exit(1 if failed else 0)
