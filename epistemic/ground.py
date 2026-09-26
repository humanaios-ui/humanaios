"""
ground.py — Generative ground (Layer 0)  (v3.2-DRAFT)
Simulation contrast / god-view only. NEVER imported by agent_view.py.
v3.2: GROUND_TRUTH write-protected; narrow exception handling; residual
returns conditioning diagnostics via godview_residual_ex.
"""
from __future__ import annotations
import os
import numpy as np

GROUND_TRUTH = np.array([42.0, 3.14, -1.0, 2.71], dtype=float)
GROUND_TRUTH.setflags(write=False)  # v3.2: immutable — tests must swap, not mutate

def godview_residual_ex(h_proj: np.ndarray, m_proj: np.ndarray):
    """Return (residual, condition_number). v3.2: near-collinear projections
    make X ill-conditioned; lstsq silently rescues rank with huge
    coefficients, so downstream analyses must be able to flag cond blowup."""
    X = np.column_stack([h_proj, m_proj])
    try:
        coeffs, _, _, sv = np.linalg.lstsq(X, GROUND_TRUTH, rcond=None)
        cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
        return float(np.linalg.norm(GROUND_TRUTH - X @ coeffs)), cond
    except np.linalg.LinAlgError:
        return float(np.linalg.norm(GROUND_TRUTH)), float("inf")

def godview_residual(h_proj: np.ndarray, m_proj: np.ndarray) -> float:
    return godview_residual_ex(h_proj, m_proj)[0]

def assert_not_imported_by_agent_view() -> None:
    """UPGRADE v3.1: strict mode raises; default remains soft warn."""
    import sys
    present = any("agent_view" in (getattr(m, "__name__", "") or "")
                  for m in sys.modules.values() if m)
    if present:
        msg = ("[ground.py] ground loaded while agent_view present. "
               "Ensure operational paths never depend on this import.")
        if os.environ.get("AGENT_VIEW_STRICT") == "1":
            raise RuntimeError(msg)
        print("WARNING: " + msg)
