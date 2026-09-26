#!/usr/bin/env python3
"""
Integration layer between Phase 1 (OTEL) and Phase 3 (Epistemic Metrics)
Bridges POSTFLIGHT payloads to epistemic health metrics recording
"""

import json
from typing import Optional, Dict, Any
from otel_instrumentation import get_instrumentation

# This module will be updated once Phase 3 (epistemic_metrics.py) is complete
# For now, it provides the integration interface


class OTELEpistemicBridge:
    """Connect POSTFLIGHT data to epistemic health metrics"""

    def __init__(self):
        self.instr = get_instrumentation()
        self.epistemic_metrics = None  # Will be: from epistemic_metrics import EpistemicHealthMetrics

    def process_postflight_payload(self, payload: Dict[str, Any]) -> None:
        """
        Process POSTFLIGHT JSON and record epistemic metrics

        Expected payload structure:
        {
            "vectors": {...},           # 13 epistemic vectors
            "findings": [...],          # findings logged
            "unknowns": [...],          # unknowns logged
            "assumptions": [...],       # assumptions logged
            "decisions": [...],         # decisions logged
            "goals_completed": int,     # count
            "goals_in_scope": int,      # count
            "calibration_reflection": {...}  # calibration drift, etc
        }
        """
        if not payload:
            return

        # Once Phase 3 is complete, initialize epistemic metrics
        # if self.epistemic_metrics is None:
        #     from epistemic_metrics import EpistemicHealthMetrics
        #     self.epistemic_metrics = EpistemicHealthMetrics(self.instr)

        # Record calibration drift (from calibration_reflection)
        if "calibration_reflection" in payload:
            reflection = payload["calibration_reflection"]
            if "calibration_drift" in reflection:
                drift = reflection["calibration_drift"]
                # self.epistemic_metrics.record_calibration_drift(drift)
                self.instr.tracer.start_span("postflight_calibration").set_attribute(
                    "calibration.drift", drift
                )

        # Record unknown accumulation
        if "unknowns" in payload:
            unknown_count = len(payload["unknowns"])
            # self.epistemic_metrics.record_unknown_count(unknown_count)
            self.instr.tracer.start_span("postflight_unknowns").set_attribute(
                "unknowns.count", unknown_count
            )

        # Record goal completion ratio
        if "goals_completed" in payload and "goals_in_scope" in payload:
            completed = payload["goals_completed"]
            in_scope = payload["goals_in_scope"]
            if in_scope > 0:
                ratio = completed / in_scope
                # self.epistemic_metrics.record_goal_completion(completed, in_scope)
                span = self.instr.tracer.start_span("postflight_goals")
                span.set_attribute("goals.completed", completed)
                span.set_attribute("goals.in_scope", in_scope)
                span.set_attribute("goals.completion_ratio", ratio)

        # Record artifact type discipline
        if "findings" in payload:
            artifact_types = self._classify_artifacts(payload)
            if self._is_type_collapse(artifact_types):
                # self.epistemic_metrics.record_type_violation("findings_only_collapse")
                self.instr.tracer.start_span("postflight_type_violation").set_attribute(
                    "violation_type", "type_collapse"
                )

    def _classify_artifacts(self, payload: Dict[str, Any]) -> Dict[str, int]:
        """Count artifact types in payload"""
        return {
            "findings": len(payload.get("findings", [])),
            "unknowns": len(payload.get("unknowns", [])),
            "decisions": len(payload.get("decisions", [])),
            "assumptions": len(payload.get("assumptions", [])),
            "dead_ends": len(payload.get("dead_ends", [])),
            "mistakes": len(payload.get("mistakes", [])),
        }

    def _is_type_collapse(self, artifact_types: Dict[str, int]) -> bool:
        """Check if artifact types violate discipline (e.g., findings-only)"""
        total = sum(artifact_types.values())
        if total == 0:
            return False

        findings_ratio = artifact_types["findings"] / total
        others_ratio = 1 - findings_ratio

        # Collapse if >80% findings and very few other types
        return findings_ratio > 0.8 and artifact_types["unknowns"] < 2


def integrate_epistemic_metrics_with_otel():
    """
    Called from CLI hooks or manually to connect epistemic metrics
    This is the integration point for Phase 3 → Phase 1
    """
    bridge = OTELEpistemicBridge()
    return bridge


# Example: How Phase 2 CLI hooks will use this
def example_postflight_integration():
    """
    Example from cli_instrumentation_hooks.py post_command_hook:

    if phase == "postflight":
        # After empirica postflight-submit succeeds
        postflight_data = json.loads(stdin_data)  # extracted from payload
        bridge = integrate_epistemic_metrics_with_otel()
        bridge.process_postflight_payload(postflight_data)
    """
    pass
