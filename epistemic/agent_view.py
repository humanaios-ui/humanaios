"""
agent_view.py — Layers 1–5 under strict agent-view constraints (v3.2-DRAFT)

v3.2 CHANGELOG (S-081626 adversarial audit, Z1-proposed, PENDING Z2):
  - IC-CAND-MASK-INERT-01: sensor_mask now a continuous absorption weight
    (v3.1 boolean gate could never fire; masks were inert).
  - Per-agent np.random.Generator; run_ensemble fully seeded.
  - make_masks gains mode='hard_partition' (true zero-support complement).
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from copy import deepcopy


class EpistemicAgent:
    """Partial observer; init deliberately unanchored (radical unknowability)."""

    def __init__(self, name, sensor_mask, noise_scale, learning_rate=0.15,
                 init_scale=1.0, rng: Optional[np.random.Generator] = None):
        self.name = name
        self.sensor_mask = np.asarray(sensor_mask, dtype=float)
        self.noise_scale = float(noise_scale)
        self.learning_rate = float(learning_rate)
        self._rng = rng if rng is not None else np.random.default_rng(
            np.random.randint(0, 2**31 - 1))
        dim = len(self.sensor_mask)
        self._private_state = self._rng.normal(0.0, init_scale, size=dim)
        self.perceived_other_projection = np.zeros(dim)
        self.projection_history: List[np.ndarray] = []

    def project(self) -> np.ndarray:
        noise = self._rng.normal(0.0, self.noise_scale * 0.5, size=self._private_state.shape)
        proj = self._private_state + noise
        self.projection_history.append(proj.copy())
        return proj

    def absorb_projection(self, other_projection: np.ndarray) -> None:
        """v3.2: sensor_mask is a CONTINUOUS per-dimension absorption weight.
        eff rate = learning_rate * mask[d]; mask=0 -> truly blind dim."""
        other_projection = np.asarray(other_projection, dtype=float)
        self.perceived_other_projection = other_projection.copy()
        eff = self.learning_rate * np.clip(self.sensor_mask, 0.0, 1.0)
        self._private_state = ((1.0 - eff) * self._private_state
                               + eff * other_projection)
        self._private_state += self._rng.normal(
            0.0, self.noise_scale * 0.05, size=self._private_state.shape)

    def private_magnitude(self) -> float:
        return float(np.linalg.norm(self._private_state))


@dataclass
class EpistemicReport:
    human_private_magnitude: float
    machine_private_magnitude: float
    mutual_agreement: float
    disagreement_magnitude: float
    mutual_instability: float
    instrument_confidence: float
    mutual_agreement_var: float = 0.0
    disagreement_var: float = 0.0


@dataclass
class EnsembleSummary:
    n_runs: int
    disagreement_mean: float
    disagreement_std: float
    mutual_mean: float
    mutual_std: float
    confidence_mean: float
    final_disagreement_distribution: List[float]


class ReflexiveInstrument:
    """Measures observer-observed structure from inside the loop. No ground."""

    def __init__(self, human, machine, stability_window: int = 5):
        self.human = human
        self.machine = machine
        self.stability_window = max(2, stability_window)
        self.measurement_history: List[EpistemicReport] = []
        self._prev_mutual_vec: Optional[np.ndarray] = None
        self._mutual_history: List[float] = []
        self._disagreement_history: List[float] = []

    def measure(self) -> EpistemicReport:
        h_proj = self.human.project()
        m_proj = self.machine.project()
        self.human.absorb_projection(m_proj)
        self.machine.absorb_projection(h_proj)

        h_norm = np.linalg.norm(h_proj); m_norm = np.linalg.norm(m_proj)
        mutual = float(np.dot(h_proj, m_proj) / (h_norm * m_norm)) if (h_norm > 1e-9 and m_norm > 1e-9) else 0.0
        disagreement = float(np.linalg.norm(h_proj - m_proj))

        current_mutual_vec = 0.5 * (h_proj + m_proj)
        mutual_instability = 0.0 if self._prev_mutual_vec is None else float(
            np.linalg.norm(current_mutual_vec - self._prev_mutual_vec))
        self._prev_mutual_vec = current_mutual_vec.copy()

        self._mutual_history.append(mutual)
        self._disagreement_history.append(disagreement)
        w = self.stability_window
        rm = self._mutual_history[-w:]; rd = self._disagreement_history[-w:]
        mutual_var = float(np.var(rm)) if len(rm) > 1 else 0.0
        disagree_var = float(np.var(rd)) if len(rd) > 1 else 0.0
        combined_var = mutual_var + 0.1 * disagree_var
        confidence = float(1.0 / (1.0 + 10.0 * combined_var + mutual_instability))

        report = EpistemicReport(
            human_private_magnitude=self.human.private_magnitude(),
            machine_private_magnitude=self.machine.private_magnitude(),
            mutual_agreement=mutual,
            disagreement_magnitude=disagreement,
            mutual_instability=mutual_instability,
            instrument_confidence=min(1.0, max(0.0, confidence)),
            mutual_agreement_var=mutual_var,
            disagreement_var=disagree_var,
        )
        self.measurement_history.append(report)
        return report

    def run_dialectic(self, cycles: int = 12, verbose: bool = True,
                      disturbance_threshold: float = 0.25) -> Dict[str, List[float]]:
        for i in range(cycles):
            rep = self.measure()
            if verbose:
                print(f"{i+1:6d} | {rep.mutual_agreement:7.3f} | "
                      f"{rep.disagreement_magnitude:8.3f} | {rep.instrument_confidence:6.3f}")
            if rep.instrument_confidence < disturbance_threshold and i > 3:
                if verbose:
                    print("MEASUREMENT DISTURBANCE: instrument observing its own footprints.")
                break
        return {
            "human_private": [r.human_private_magnitude for r in self.measurement_history],
            "machine_private": [r.machine_private_magnitude for r in self.measurement_history],
            "mutual": [r.mutual_agreement for r in self.measurement_history],
            "disagreement": [r.disagreement_magnitude for r in self.measurement_history],
            "instability": [r.mutual_instability for r in self.measurement_history],
            "confidence": [r.instrument_confidence for r in self.measurement_history],
            "mutual_var": [r.mutual_agreement_var for r in self.measurement_history],
        }


def make_masks(dim: int = 4, mode: str = "complementary", rng=None):
    if rng is None:
        rng = np.random.default_rng()
    if mode == "independent":
        mask_h = rng.uniform(0.05, 1.0, size=dim)
        mask_m = rng.uniform(0.05, 1.0, size=dim)
    elif mode == "hard_partition":
        half = rng.permutation(dim)[: dim // 2]
        mask_h = np.zeros(dim); mask_h[half] = rng.uniform(0.5, 1.0, size=len(half))
        mask_m = np.where(mask_h > 0, 0.0, rng.uniform(0.5, 1.0, size=dim))
    else:
        mask_h = rng.uniform(0.1, 1.0, size=dim)
        mask_m = np.clip(1.0 - mask_h + rng.uniform(-0.2, 0.2, size=dim), 0.05, 1.0)
    return mask_h, mask_m


def run_ensemble(n_runs=20, cycles=10, mask_mode="complementary",
                 human_lr=0.14, machine_lr=0.10, seed=42) -> EnsembleSummary:
    rng = np.random.default_rng(seed)
    final_disagreements: List[float] = []
    all_mutuals: List[float] = []
    all_confidences: List[float] = []
    for _ in range(n_runs):
        mask_h, mask_m = make_masks(dim=4, mode=mask_mode, rng=rng)
        noise_h = float(rng.uniform(0.10, 0.35)); noise_m = float(rng.uniform(0.05, 0.25))
        rng_h, rng_m = rng.spawn(2)
        human = EpistemicAgent("Human", mask_h, noise_h, learning_rate=human_lr, init_scale=1.0, rng=rng_h)
        machine = EpistemicAgent("Machine", mask_m, noise_m, learning_rate=machine_lr, init_scale=1.0, rng=rng_m)
        instrument = ReflexiveInstrument(human, machine, stability_window=5)
        results = instrument.run_dialectic(cycles=cycles, verbose=False)
        final_disagreements.append(results["disagreement"][-1])
        all_mutuals.append(results["mutual"][-1])
        all_confidences.append(results["confidence"][-1])
    return EnsembleSummary(
        n_runs=n_runs,
        disagreement_mean=float(np.mean(final_disagreements)),
        disagreement_std=float(np.std(final_disagreements)),
        mutual_mean=float(np.mean(all_mutuals)),
        mutual_std=float(np.std(all_mutuals)),
        confidence_mean=float(np.mean(all_confidences)),
        final_disagreement_distribution=[float(x) for x in final_disagreements],
    )
