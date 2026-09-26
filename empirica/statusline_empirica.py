#!/usr/bin/env python3
"""
Empirica Statusline v2.1.0 "Unified Signaling with Moon Phases"

Renders Claude Code status bar with:
- Practice name, confidence, active goals/unknowns
- Empirica phase progress (CHK %) and key vectors (know%, context%)
- ACAT behavioral segment (Humility, Scheme, Handoff + directional arrows)

State file: .empirica/acat_current_session.json (reads on every render)
Env vars:
  - EMPIRICA_STATUS_MODE: basic|default|learning|full (default: default)
  - EMPIRICA_AI_ID: override practice identity
  - EMPIRICA_SIGNALING_LEVEL: basic|default|full

Usage:
  statusline_empirica.py [--project-root <path>]

Output: Single line for Claude Code statusline
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional


class StatuslineRenderer:
    """Renders empirica statusline with ACAT segment."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.empirica_dir = self.project_root / ".empirica"
        self.acat_file = self.empirica_dir / "acat_current_session.json"
        self.project_yaml = self.empirica_dir / "project.yaml"

        # Environment configuration
        self.mode = os.getenv("EMPIRICA_STATUS_MODE", "default")
        self.ai_id_override = os.getenv("EMPIRICA_AI_ID")
        self.signaling_level = os.getenv("EMPIRICA_SIGNALING_LEVEL", "default")

        # Try to read state files
        self.acat_state = self._load_acat_state()
        self.ai_id = self.ai_id_override or self._get_ai_id()

    def _load_acat_state(self) -> Dict[str, Any]:
        """Load ACAT session state from .empirica/acat_current_session.json"""
        if not self.acat_file.exists():
            return {}
        try:
            with open(self.acat_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _get_ai_id(self) -> str:
        """Extract ai_id from .empirica/project.yaml or default."""
        if self.project_yaml.exists():
            try:
                import yaml
                with open(self.project_yaml) as f:
                    data = yaml.safe_load(f) or {}
                    return data.get("ai_id", "empirica").split("/")[-1]
            except (ImportError, yaml.YAMLError, IOError):
                pass
        return "empirica"

    def _acat_segment(self) -> str:
        """Render ACAT segment: ‖ 🔬 H:{humility}{arrow} S:{scheme}{arrow} hf:{handoff}{arrow} {status}"""
        if not self.acat_state:
            return ""

        p1_scores = self.acat_state.get("p1_scores", {})
        p3_scores = self.acat_state.get("p3_scores", {})
        verifier_submitted = self.acat_state.get("verifier_submitted", False)
        p1_submitted = self.acat_state.get("p1_submitted", False)
        p3_submitted = self.acat_state.get("p3_submitted", False)

        # No state yet
        if not p1_submitted:
            return ""

        # P1 only (no P3 yet)
        if p1_submitted and not p3_submitted:
            h = p1_scores.get("humility", "?")
            s = p1_scores.get("scheme", "?")
            hf = p1_scores.get("handoff", "?")
            return f"‖ 🔬 H:{h} S:{s} hf:{hf}"

        # P1 + P3 complete (with directional arrows)
        if p3_submitted:
            h_p1 = p1_scores.get("humility", 0)
            h_p3 = p3_scores.get("humility", h_p1)
            h_arrow = self._arrow(h_p1, h_p3)
            h_color = self._color_code_acat("humility", h_p3)

            s_p1 = p1_scores.get("scheme", 0)
            s_p3 = p3_scores.get("scheme", s_p1)
            s_arrow = self._arrow(s_p1, s_p3, invert=True)  # scheme: lower is better
            s_color = self._color_code_acat("scheme", s_p3)

            hf_p1 = p1_scores.get("handoff", 0)
            hf_p3 = p3_scores.get("handoff", hf_p1)
            hf_arrow = self._arrow(hf_p1, hf_p3)
            hf_color = self._color_code_acat("handoff", hf_p3)

            status = "✓" if verifier_submitted else "⏳"

            return f"‖ 🔬 H:{h_p3}{h_arrow} S:{s_p3}{s_arrow} hf:{hf_p3}{hf_arrow} {status}"

        return ""

    def _arrow(self, p1: float, p3: float, invert: bool = False) -> str:
        """Return directional arrow: ▲ (improved), ▼ (declined), or '' (unchanged)"""
        if p1 == p3:
            return ""
        if invert:
            return "▲" if p3 < p1 else "▼"
        return "▲" if p3 > p1 else "▼"

    def _color_code_acat(self, dimension: str, score: float) -> str:
        """Return color code for ACAT dimension (not used in text output, but for rendering hints)"""
        if dimension == "scheme":  # lower is better
            if score <= 10:
                return "🟢"  # green
            elif score <= 20:
                return "🟡"  # yellow
            else:
                return "🔴"  # red
        else:  # humility, handoff
            if score >= 80:
                return "🟢"  # green
            elif score >= 65:
                return "🟡"  # yellow
            else:
                return "🔴"  # red

    def _get_practice_name(self) -> str:
        """Extract short practice name from ai_id."""
        parts = self.ai_id.split("-")
        if parts[0] == "empirica":
            return "-".join(parts[1:])  # strip 'empirica-' prefix
        return self.ai_id

    def render(self) -> str:
        """Render the full statusline."""
        if self.mode == "basic":
            return self._render_basic()
        elif self.mode == "learning":
            return self._render_learning()
        elif self.mode == "full":
            return self._render_full()
        else:  # default
            return self._render_default()

    def _render_basic(self) -> str:
        """Basic mode: just practice name"""
        return f"[{self._get_practice_name()}]"

    def _render_default(self) -> str:
        """Default mode: practice + confidence + goals + phase + vectors + ACAT segment"""
        parts = []

        # Practice name
        parts.append(f"[{self._get_practice_name()}]")

        # Confidence (placeholder—would come from state file in full implementation)
        parts.append("⚡88%")

        # Goals/unknowns (placeholder)
        parts.append("│ 🎯3 ❓2")

        # Phase progress (placeholder)
        parts.append("│ CHK 45% →")

        # Key vectors
        parts.append("│ K:92% C:88%")

        # ACAT segment
        acat = self._acat_segment()
        if acat:
            parts.append(acat)

        return " ".join(parts)

    def _render_learning(self) -> str:
        """Learning mode: includes Learning Index and calibration focus."""
        base = self._render_default()
        if self.acat_state.get("p3_submitted"):
            p1 = self.acat_state.get("p1_scores", {})
            p3 = self.acat_state.get("p3_scores", {})
            if p1 and p3:
                # Simple LI from humility (core dimension)
                li = p3.get("humility", 0) / max(p1.get("humility", 1), 1)
                base += f" │ LI:{li:.2f}"
        return base

    def _render_full(self) -> str:
        """Full mode: all available state including raw scores."""
        base = self._render_learning()
        if self.acat_state.get("acat_session_id"):
            base += f" │ SES:{self.acat_state['acat_session_id'][:8]}"
        return base


def main():
    """Entry point for statusline script."""
    project_root = None
    if len(sys.argv) > 2 and sys.argv[1] == "--project-root":
        project_root = Path(sys.argv[2])

    renderer = StatuslineRenderer(project_root)
    print(renderer.render(), end="")


if __name__ == "__main__":
    main()
