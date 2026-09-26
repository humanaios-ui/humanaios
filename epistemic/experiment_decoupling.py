#!/usr/bin/env python3
"""experiment_decoupling.py — v3.2-DRAFT (fair indicator + nulls). GOD-VIEW."""
from __future__ import annotations
import sys, itertools
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from epistemic.agent_view import EpistemicAgent, ReflexiveInstrument, make_masks
from epistemic.ground import godview_residual_ex

CYCLES = 16
WARMUP = 3
COND_LIMIT = 1e6
N_PERM = 200

def run_one(seed, h_lr, m_lr, noise_h, noise_m, mask_mode, cycles=CYCLES):
    rng = np.random.default_rng(seed)
    mh, mm = make_masks(mode=mask_mode, rng=rng)
    rng_h, rng_m = rng.spawn(2)
    H = EpistemicAgent("H", mh, noise_h, learning_rate=h_lr, rng=rng_h)
    M = EpistemicAgent("M", mm, noise_m, learning_rate=m_lr, rng=rng_m)
    ins = ReflexiveInstrument(H, M, stability_window=5)
    conf, res, cond, mvar = [], [], [], []
    for _ in range(cycles):
        rep = ins.measure()
        conf.append(rep.instrument_confidence)
        mvar.append(rep.mutual_agreement_var)
        r, c = godview_residual_ex(H.projection_history[-1], M.projection_history[-1])
        res.append(r); cond.append(c)
    return (np.array(conf), np.array(res), np.array(mvar), np.array(cond))

def slope(x):
    return float(np.polyfit(np.arange(len(x)), x, 1)[0])

def lead_hit(conf, mvar, warmup=WARMUP):
    t_sat = int(np.argmax(conf[warmup:])) + warmup
    t_collapse = int(np.argmin(mvar[warmup:])) + warmup   # FULL window
    if t_sat <= warmup:
        return None
    return t_collapse < t_sat

def permutation_null(conf, mvar, rng, n=N_PERM, warmup=WARMUP):
    hits = tries = 0
    L = len(mvar)
    for _ in range(n):
        k = int(rng.integers(1, L - 1))
        h = lead_hit(conf, np.roll(mvar, k), warmup)
        if h is not None:
            tries += 1
            hits += int(h)
    return hits / tries if tries else np.nan

grid = list(itertools.product([0.05, 0.14, 0.30], [0.05, 0.09, 0.30],
                              [0.10, 0.25], [0.10, 0.25]))
seeds = range(5)

def main():
    for mask_mode in ("complementary", "independent", "hard_partition"):
        total = decoupled = ill_cond = 0
        conf_up = res_flat = 0
        lead_hits = lead_checks = 0
        null_rates = []
        perm_rng = np.random.default_rng(20260816)
        for h_lr, m_lr, nh, nm in grid:
            for s in seeds:
                conf, res, mvar, cond = run_one(100 + s, h_lr, m_lr, nh, nm, mask_mode)
                total += 1
                if np.median(cond) > COND_LIMIT:
                    ill_cond += 1
                    continue
                cs, rs = slope(conf[WARMUP:]), slope(res[WARMUP:])
                cu, rf = cs > 0.005, rs > -0.005
                conf_up += int(cu); res_flat += int(rf)
                if cu and rf:
                    decoupled += 1
                    h = lead_hit(conf, mvar)
                    if h is not None:
                        lead_checks += 1
                        lead_hits += int(h)
                        null_rates.append(permutation_null(conf, mvar, perm_rng))
        usable = total - ill_cond
        joint = decoupled / usable if usable else 0
        indep = (conf_up / usable) * (res_flat / usable) if usable else 0
        obs_lead = lead_hits / lead_checks if lead_checks else float("nan")
        null_lead = float(np.nanmean(null_rates)) if null_rates else float("nan")
        print(f"\n=== mask_mode = {mask_mode} ===")
        print(f"Sweep: {total} runs; ill-conditioned excluded: {ill_cond}")
        print(f"DECOUPLED joint rate: {decoupled}/{usable} = {100*joint:.1f}%   "
              f"| independence null = {100*indep:.1f}%   "
              f"| joint/null = {joint/indep if indep else float('nan'):.2f}")
        print(f"Lead indicator: observed {lead_hits}/{lead_checks} = {100*obs_lead:.1f}%   "
              f"| shift null = {100*null_lead:.1f}%   "
              f"| lift = {obs_lead - null_lead:+.3f}")

if __name__ == "__main__":
    main()
