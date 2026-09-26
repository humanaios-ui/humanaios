"""
OpenTelemetry Instrumentation — Empirica Foundation Evaluator
Phase 3.4 Observability Stack Implementation
"""

from opentelemetry import trace
from contextlib import contextmanager
from typing import Dict, Any
import json

tracer = trace.get_tracer("empirica.foundation.evaluator")

class EvaluatorInstrumentation:
    """Context manager for OTEL span tracking in evaluator transactions."""
    
    def __init__(self, transaction_id: str, session_id: str, work_type: str):
        self.transaction_id = transaction_id
        self.session_id = session_id
        self.work_type = work_type
        self.span_stack = []
    
    @contextmanager
    def span(self, span_name: str, attributes: Dict[str, Any] = None):
        """Create a span with consistent attribute set."""
        attrs = {
            "transaction_id": self.transaction_id,
            "session_id": self.session_id,
            "phase": self._infer_phase(span_name),
            "practice_id": "empirica-foundation-evaluator",
        }
        if attributes:
            attrs.update(attributes)
        
        with tracer.start_as_current_span(span_name) as span:
            for key, value in attrs.items():
                span.set_attribute(key, value)
            self.span_stack.append((span_name, span))
            yield span
    
    @staticmethod
    def _infer_phase(span_name: str) -> str:
        """Infer phase from span name."""
        noetic_spans = ["investigation", "poll", "search", "read"]
        praxic_spans = ["execution", "reply", "commit", "goal"]
        
        if any(s in span_name.lower() for s in noetic_spans):
            return "noetic"
        elif any(s in span_name.lower() for s in praxic_spans):
            return "praxic"
        return "unknown"


# Usage Example in empirica workflow:

def instrumented_preflight(session_id: str, work_type: str, vectors: Dict):
    """PREFLIGHT with tracing."""
    instr = EvaluatorInstrumentation(
        transaction_id=str(uuid.uuid4()),
        session_id=session_id,
        work_type=work_type
    )
    
    with instr.span("preflight", {
        "work_type": work_type,
        "vector_count": len(vectors),
    }):
        # PREFLIGHT logic here
        # ... call empirica.preflight_submit(...)
        pass


def instrumented_mailbox_poll():
    """Mailbox polling with tracing."""
    # Assumes transaction context already exists
    with tracer.start_as_current_span("mailbox_poll") as span:
        span.set_attribute("poll_type", "inbox")
        span.set_attribute("status_filter", "accepted,changed")
        
        # ... call empirica.mailbox.poll(...)
        
        span.set_attribute("item_count", 20)
        span.set_attribute("status", "success")


def instrumented_mailbox_reply(parent_id: str, summary: str):
    """Mailbox reply with tracing."""
    with tracer.start_as_current_span("mailbox_reply") as span:
        span.set_attribute("parent_id", parent_id)
        span.set_attribute("summary_length", len(summary))
        span.set_attribute("result", "shipped")
        
        # ... call empirica.mailbox.reply(...)


def instrumented_finding_log(finding: str, impact: float, source: str):
    """Finding logging with tracing."""
    with tracer.start_as_current_span("log_artifact") as span:
        span.set_attribute("artifact_type", "finding")
        span.set_attribute("finding_length", len(finding))
        span.set_attribute("impact", impact)
        span.set_attribute("epistemic_source", source)
        
        # ... call empirica.finding_log(...)


def instrumented_postflight(vectors: Dict, claims: list):
    """POSTFLIGHT with tracing."""
    with tracer.start_as_current_span("postflight") as span:
        span.set_attribute("vector_count", len(vectors))
        span.set_attribute("claims_count", len(claims))
        
        # Calculate deltas
        deltas = {k: v for k, v in vectors.items()}  # Simplified
        span.set_attribute("vector_delta_mean", sum(deltas.values()) / len(deltas))
        
        # ... call empirica.postflight_submit(...)


# Integration pattern for all evaluator operations:
# 1. Wrap in instrumented_* function
# 2. Set attributes for operation-specific context
# 3. Execute empirica CLI command
# 4. Span auto-exports to OTEL collector (batched, async)

