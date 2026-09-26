#!/usr/bin/env python3
"""
Phase 3.5.6 Phase 2: CLI Instrumentation Hooks
Auto-instrument empirica CLI commands to emit transaction spans and metrics
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from otel_instrumentation import get_instrumentation


class EmpiricalCLIInstrumentationHook:
    """Wrap empirica CLI commands to emit OTEL instrumentation"""

    # Command patterns that mark transaction phases
    PREFLIGHT_COMMANDS = [
        "preflight-submit",
        "preflight",
    ]

    CHECK_COMMANDS = [
        "check-submit",
        "check",
    ]

    POSTFLIGHT_COMMANDS = [
        "postflight-submit",
        "postflight",
    ]

    NOETIC_COMMANDS = [
        "investigate",
        "project-search",
        "finding-log",
        "unknown-log",
        "assumption-log",
        "deadend-log",
    ]

    PRAXIC_COMMANDS = [
        "goals-create",
        "goals-add-task",
        "goals-complete-task",
        "goals-complete",
        "finding-log",
        "decision-log",
    ]

    def __init__(self):
        self.instr = get_instrumentation()
        self.current_transaction_span = None
        self.current_phase_span = None
        self.transaction_start = None
        self.phase_start = None

    def classify_command(self, cmd: str) -> Optional[str]:
        """Classify command into transaction phase"""
        if any(c in cmd for c in self.PREFLIGHT_COMMANDS):
            return "preflight"
        elif any(c in cmd for c in self.CHECK_COMMANDS):
            return "CHECK"
        elif any(c in cmd for c in self.POSTFLIGHT_COMMANDS):
            return "postflight"
        elif any(c in cmd for c in self.NOETIC_COMMANDS):
            return "noetic"
        elif any(c in cmd for c in self.PRAXIC_COMMANDS):
            return "praxic"
        return None

    def extract_context_from_file(self, stdin_data: Optional[str] = None) -> Dict[str, Any]:
        """Extract transaction context from PREFLIGHT/CHECK/POSTFLIGHT JSON payloads"""
        context = {}

        if not stdin_data:
            return context

        try:
            payload = json.loads(stdin_data)
            context["work_type"] = payload.get("work_type", "unknown")
            context["work_summary"] = payload.get("work_summary", "")

            # Extract vectors for recording
            if "vectors" in payload:
                context["vectors"] = payload["vectors"]

            # Extract goals
            if "goals" in payload:
                context["goals"] = payload["goals"]
                if isinstance(context["goals"], list) and context["goals"]:
                    context["goal_objective"] = context["goals"][0].get("objective", "")

        except (json.JSONDecodeError, TypeError):
            pass  # Not JSON, continue with empty context

        return context

    def pre_command_hook(self, cmd: str, stdin_data: Optional[str] = None) -> None:
        """Called before empirica command executes"""
        phase = self.classify_command(cmd)

        if not phase:
            return  # Not an instrumented command

        context = self.extract_context_from_file(stdin_data)

        # Start transaction span for PREFLIGHT
        if phase == "preflight":
            self.transaction_start = time.time()
            work_type = context.get("work_type", "unknown")
            goal = context.get("goal_objective", None)

            # We'll use a simple span context instead of nested spans
            attributes = {
                "cli.command": cmd,
                "cli.phase": phase,
                "work.type": work_type,
            }
            if goal:
                attributes["goal"] = goal

            span = self.instr.tracer.start_span(f"cli_command_{phase}")
            for key, value in attributes.items():
                span.set_attribute(key, value)
            self.current_transaction_span = span
            self.current_transaction_span.__enter__()

        elif self.current_transaction_span:
            # Start phase span within transaction
            self.phase_start = time.time()
            phase_span = self.instr.tracer.start_span(f"cli_phase_{phase}")
            phase_span.set_attribute("phase", phase)
            phase_span.set_attribute("cli.command", cmd)
            self.current_phase_span = phase_span
            self.current_phase_span.__enter__()

            # Record vectors if available
            if "vectors" in context:
                for vector_name, value in context["vectors"].items():
                    self.instr.record_vector(vector_name, value, phase)

    def post_command_hook(self, cmd: str, returncode: int) -> None:
        """Called after empirica command executes"""
        phase = self.classify_command(cmd)

        if not phase:
            return

        # Close phase span
        if self.current_phase_span:
            elapsed = time.time() - self.phase_start
            self.current_phase_span.set_attribute("phase.duration.seconds", elapsed)
            self.current_phase_span.set_attribute("cli.returncode", returncode)

            # Record phase duration metric
            self.instr.phase_duration.record(elapsed, {"phase": phase})

            self.current_phase_span.__exit__(None, None, None)
            self.current_phase_span = None

        # Close transaction span for POSTFLIGHT
        if phase == "postflight" and self.current_transaction_span:
            elapsed = time.time() - self.transaction_start
            self.current_transaction_span.set_attribute("transaction.duration.seconds", elapsed)
            self.current_transaction_span.set_attribute("cli.returncode", returncode)
            self.current_transaction_span.__exit__(None, None, None)
            self.current_transaction_span = None

        # Track CHECK decisions
        if phase == "CHECK":
            decision = "proceed" if returncode == 0 else "block"
            self.instr.increment_CHECK_decision(decision)


class CLIHookWrapper:
    """Wrapper for empirica CLI commands that injects instrumentation"""

    def __init__(self):
        self.hook = EmpiricalCLIInstrumentationHook()
        self.enabled = os.getenv("EMPIRICA_OTEL_CLI_HOOKS", "true").lower() != "false"

    def run_with_instrumentation(self, args: List[str]) -> int:
        """Execute empirica CLI command with OTEL instrumentation"""
        if not self.enabled:
            return self._run_command(args)

        cmd_str = " ".join(args)

        # Capture stdin for JSON payloads (used by PREFLIGHT/CHECK/POSTFLIGHT)
        stdin_data = None
        if not sys.stdin.isatty():
            try:
                stdin_data = sys.stdin.read()
            except:
                pass

        # Pre-command hook
        self.hook.pre_command_hook(cmd_str, stdin_data)

        # Execute command
        try:
            returncode = self._run_command(args, stdin_input=stdin_data)
        except Exception as e:
            returncode = 1
            self.hook.post_command_hook(cmd_str, returncode)
            raise

        # Post-command hook
        self.hook.post_command_hook(cmd_str, returncode)

        return returncode

    def _run_command(self, args: List[str], stdin_input: Optional[str] = None) -> int:
        """Execute empirica CLI command via subprocess"""
        try:
            result = subprocess.run(
                ["empirica"] + args,
                input=stdin_input,
                text=True,
                capture_output=False,
            )
            return result.returncode
        except FileNotFoundError:
            print(f"Error: 'empirica' command not found", file=sys.stderr)
            return 127


def create_cli_wrapper_script() -> None:
    """Create a wrapper script for empirica CLI (optional)"""
    script_content = '''#!/usr/bin/env python3
"""
Empirica CLI wrapper with OTEL instrumentation
This is an optional wrapper that can be used instead of directly calling empirica
"""

import sys
from empirica.cli_instrumentation_hooks import CLIHookWrapper

if __name__ == "__main__":
    wrapper = CLIHookWrapper()
    sys.exit(wrapper.run_with_instrumentation(sys.argv[1:]))
'''

    script_path = Path(__file__).parent / "empirica-otel"
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    print(f"✓ Created wrapper script at {script_path}")


if __name__ == "__main__":
    create_cli_wrapper_script()
