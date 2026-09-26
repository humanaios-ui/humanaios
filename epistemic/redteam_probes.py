#!/usr/bin/env python3
"""redteam_probes.py — adversarial audit of epistemic v3.1 (S-081626 audit pass)."""
from __future__ import annotations
import sys, subprocess, hashlib
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from epistemic.agent_view import EpistemicAgent, ReflexiveInstrument, make_masks, run_ensemble
from epistemic.ground import godview_residual, GROUND_TRUTH

print("=" * 72)
print("RT-1  SENSOR-MASK INERTNESS (S4 null-condition integrity)")
print("=" * 72)
# masks are clipped to >= 0.05 in both modes, and absorb uses (mask > 0.0)
# as a boolean gate only -> masks can never gate, magnitudes never used.
rng = np.random.default_rng(0)
mins = []
for mode in ("complementary", "independent"):
    for s in range(1000):
        mh, mm = make_masks(mode=mode, rng=np.random.default_rng(s))
        mins.append(min(mh.min(), mm.min()))
print(f"min mask value over 2000 mask draws (both modes): {min(mins):.4f}  (gate fires only at exactly 0.0)")

def traj_with_masks(seed, mh, mm, cycles=12):
    np.random.seed(seed)
    H = EpistemicAgent("H", mh, 0.2, learning_rate=0.14)
    M = EpistemicAgent("M", mm, 0.1, learning_rate=0.09)
    ins = ReflexiveInstrument(H, M)
    return ins.run_dialectic(cycles=cycles, verbose=False)

r = np.random.default_rng(7)
mh_c, mm_c = make_masks(mode="complementary", rng=np.random.default_rng(7))
mh_i, mm_i = make_masks(mode="independent",  rng=np.random.default_rng(7))
a = traj_with_masks(7, mh_c, mm_c)
b = traj_with_masks(7, mh_i, mm_i)
c = traj_with_masks(7, np.full(4, 1e-9), np.full(4, 1e-9))  # near-zero but >0
identical_ci = all(np.allclose(a[k], b[k], atol=0.0) for k in a)
identical_tiny = all(np.allclose(a[k], c[k], atol=0.0) for k in a)
print(f"complementary vs independent masks, same seed -> trajectories bit-identical: {identical_ci}")
print(f"mask=1e-9 (near-blind agent) vs full masks    -> trajectories bit-identical: {identical_tiny}")
print("VERDICT: sensor_mask is functionally inert; 'partial observer' and the")
print("         independent-mask null condition are not implemented in dynamics.")

print()
print("=" * 72)
print("RT-2  LEADING-INDICATOR TAUTOLOGY (the 100.0% result)")
print("=" * 72)
# t_collapse = argmin(mvar[3:t_sat]) + 3  -> searches ONLY indices < t_sat,
# so t_collapse < t_sat is guaranteed by construction whenever t_sat > 4.
# Empirical demonstration: feed pure iid noise; 'indicator' still fires 100%.
rng = np.random.default_rng(123)
hits = checks = 0
for _ in range(2000):
    conf = rng.uniform(size=16)   # random 'confidence'
    mvar = rng.uniform(size=16)   # random, unrelated 'mvar'
    t_sat = int(np.argmax(conf[3:])) + 3
    if t_sat > 4:
        checks += 1
        t_collapse = int(np.argmin(mvar[3:t_sat])) + 3
        if t_collapse < t_sat:
            hits += 1
print(f"pure-noise series through the v3.1 indicator logic: {hits}/{checks} = "
      f"{100*hits/checks:.1f}% 'lead hits'")
print("VERDICT: 100.0% is guaranteed by the windowing (argmin over [3:t_sat] is")
print("         always < t_sat). The reported leading-indicator result carries")
print("         zero evidential content as computed.")

print()
print("=" * 72)
print("RT-3  RESIDUAL = SPAN-COLLAPSE MECHANICS (the 52.2% framing)")
print("=" * 72)
# godview_residual is the lstsq residual of GROUND_TRUTH on span{h,m}.
# As agents converge (h ~ m), the 2D span degenerates to 1D and the residual
# rises for purely linear-algebraic reasons. Demonstrate with synthetic pairs.
g = GROUND_TRUTH
rng = np.random.default_rng(5)
print("angle between h,m (deg) | mean residual (100 random pairs each)")
for ang in (90, 45, 20, 5, 1):
    vals = []
    for _ in range(100):
        h = rng.normal(size=4); h /= np.linalg.norm(h)
        # build m at fixed angle to h
        p = rng.normal(size=4); p -= (p @ h) * h; p /= np.linalg.norm(p)
        m = np.cos(np.radians(ang)) * h + np.sin(np.radians(ang)) * p
        vals.append(godview_residual(h * 3, m * 3))
    print(f"  {ang:3d}                  | {np.mean(vals):8.3f}")
# and inside the actual sweep: does agreement slope alone predict the flag?
sys.path.insert(0, str(ROOT))
from epistemic.agent_view import EpistemicAgent as EA
import itertools
def run_one(seed, h_lr, m_lr, nh, nm, cycles=16):
    np.random.seed(seed)
    mh, mm = make_masks(rng=np.random.default_rng(seed))
    H = EA("H", mh, nh, learning_rate=h_lr); M = EA("M", mm, nm, learning_rate=m_lr)
    ins = ReflexiveInstrument(H, M, stability_window=5)
    conf, res, mut = [], [], []
    for _ in range(cycles):
        rep = ins.measure()
        conf.append(rep.instrument_confidence); mut.append(abs(rep.mutual_agreement))
        res.append(godview_residual(H.projection_history[-1], M.projection_history[-1]))
    return map(np.array, (conf, res, mut))
def slope(x): return float(np.polyfit(np.arange(len(x)), x, 1)[0])
grid = list(itertools.product([0.05,0.14,0.30],[0.05,0.09,0.30],[0.10,0.25],[0.10,0.25]))
res_slopes, mut_slopes, flags = [], [], []
for h_lr, m_lr, nh, nm in grid:
    for s in range(5):
        conf, res, mut = run_one(100+s, h_lr, m_lr, nh, nm)
        res_slopes.append(slope(res[3:])); mut_slopes.append(slope(mut[3:]))
        flags.append(slope(conf[3:]) > 0.005 and slope(res[3:]) > -0.005)
r_corr = np.corrcoef(mut_slopes, res_slopes)[0, 1]
print(f"\nwithin the 180-run sweep: corr(|agreement| slope, residual slope) = {r_corr:+.3f}")
print("VERDICT: residual growth is substantially a geometric consequence of span")
print("         collapse under convergence; 52.2% is a regime-existence result,")
print("         not an epistemic base rate, and needs a mechanical-null control.")

print()
print("=" * 72)
print("RT-4  T6 NULL-CONTROL NONDETERMINISM")
print("=" * 72)
# run_ensemble never seeds the global RNG used for private states/noise ->
# T6 output varies run-to-run, and (per RT-1) arms differ only via that noise.
d_vals = []
for _ in range(3):
    comp = run_ensemble(n_runs=40, cycles=10, mask_mode="complementary", seed=42)
    ind = run_ensemble(n_runs=40, cycles=10, mask_mode="independent", seed=42)
    d1 = np.array(comp.final_disagreement_distribution); d2 = np.array(ind.final_disagreement_distribution)
    pooled = np.sqrt((d1.var() + d2.var()) / 2)
    d_vals.append((d1.mean() - d2.mean()) / pooled)
print(f"Cohen's d across 3 back-to-back T6 executions: {[f'{d:+.3f}' for d in d_vals]}")
print("VERDICT: T6 is unseeded in the quantity that matters (global RNG for")
print("         states/noise); combined with RT-1, its effect size is pure noise")
print("         between two functionally identical arms.")

print()
print("=" * 72)
print("RT-5  T7 SELF-RESEALING PRE-COMMITMENT")
print("=" * 72)
h_before = hashlib.sha256((ROOT/"epistemic/agent_view.py").read_bytes()).hexdigest()
tampered = (ROOT/"epistemic/agent_view.py").read_text() + "\n# TAMPER\n"
(ROOT/"epistemic/agent_view.py").write_text(tampered)
r = subprocess.run([sys.executable, str(ROOT/"epistemic/validate.py")], capture_output=True, text=True)
last = [l for l in r.stdout.splitlines() if l.strip()][-1]
import json
man = json.loads((ROOT/"epistemic/PRECOMMIT_MANIFEST.json").read_text())
print(f"after tampering agent_view.py, validate.py exit={r.returncode}, verdict line: '{last}'")
print(f"manifest now pins the TAMPERED hash: {man['agent_view.py'][:16]}... != committed {h_before[:16]}...")
# restore
(ROOT/"epistemic/agent_view.py").write_text(tampered.replace("\n# TAMPER\n", ""))
print("VERDICT: T7 re-writes the manifest on every run instead of verifying")
print("         against the committed one — the envelope reseals itself. A")
print("         post-hoc code change passes 7/7 and mints a fresh 'pre-commitment'.")
