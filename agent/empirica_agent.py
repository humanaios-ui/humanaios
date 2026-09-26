#!/usr/bin/env python3
"""
Empirica Foundation Evaluator — Shared Internal Agent
Phase 2: ReAct Reasoning Loop Implementation

Agent orchestrates Kimi K2.6 (planning) + Laguna M.1 (execution) models
via Bifrost gateway. Logs all reasoning as Empirica artifacts (shared visibility).

Implements ReAct pattern:
1. Reasoning: Understand task, identify approach
2. Acting: Execute plan via code/analysis
3. Observation: Verify results
4. Reflection: Learn from outcome
"""

import json
import subprocess
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import requests
import logging
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('empirica-agent')


class ReActPhase(Enum):
    """Reasoning phases in ReAct loop"""
    UNDERSTANDING = "understanding"
    PLANNING = "planning"
    EXECUTION = "execution"
    REFLECTION = "reflection"


@dataclass
class AgentTask:
    """Task request for agent"""
    id: str
    title: str
    description: str
    requesting_practice: str
    context: Optional[Dict[str, Any]] = None
    success_criteria: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class ReActStep:
    """Single step in ReAct reasoning loop"""
    phase: ReActPhase
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None
    confidence: float = 0.5


class EmpiricalArtifactLogger:
    """Log agent reasoning as Empirica artifacts"""

    def __init__(self):
        self.empirica_path = "empirica"  # Assume in PATH

    def log_finding(self, finding: str, impact: float = 0.7,
                   phase: str = "reasoning") -> str:
        """Log a finding via empirica CLI"""
        try:
            result = subprocess.run(
                [self.empirica_path, "finding-log",
                 "--finding", finding,
                 "--impact", str(impact),
                 "--epistemic-source", "search"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Finding logged: {finding[:60]}...")
                return "ok"
            else:
                logger.error(f"Failed to log finding: {result.stderr}")
                return "failed"
        except Exception as e:
            logger.error(f"Error logging finding: {e}")
            return "error"

    def log_decision(self, choice: str, rationale: str,
                    reversibility: str = "exploratory") -> str:
        """Log a decision via empirica CLI"""
        try:
            result = subprocess.run(
                [self.empirica_path, "decision-log",
                 "--choice", choice,
                 "--rationale", rationale,
                 "--reversibility", reversibility],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Decision logged: {choice[:60]}...")
                return "ok"
            else:
                logger.error(f"Failed to log decision: {result.stderr}")
                return "failed"
        except Exception as e:
            logger.error(f"Error logging decision: {e}")
            return "error"

    def log_unknown(self, unknown: str, domain: str = "general") -> str:
        """Log an unknown via empirica CLI"""
        try:
            result = subprocess.run(
                [self.empirica_path, "unknown-log",
                 "--unknown", unknown],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Unknown logged: {unknown[:60]}...")
                return "ok"
            else:
                logger.error(f"Failed to log unknown: {result.stderr}")
                return "failed"
        except Exception as e:
            logger.error(f"Error logging unknown: {e}")
            return "error"

    def log_deadend(self, approach: str, why_failed: str) -> str:
        """Log a dead-end via empirica CLI"""
        try:
            result = subprocess.run(
                [self.empirica_path, "deadend-log",
                 "--approach", approach,
                 "--why-failed", why_failed],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Dead-end logged: {approach[:60]}...")
                return "ok"
            else:
                logger.error(f"Failed to log dead-end: {result.stderr}")
                return "failed"
        except Exception as e:
            logger.error(f"Error logging dead-end: {e}")
            return "error"


class BifrostGateway:
    """Client for Bifrost LLM gateway"""

    def __init__(self, base_url: str = "http://localhost:8080",
                 api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })

    def health_check(self) -> bool:
        """Check if Bifrost gateway is alive"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def call_planning_model(self, prompt: str,
                           context: Optional[Dict] = None) -> str:
        """Call Kimi K2.6 (planning model) via Bifrost"""
        try:
            payload = {
                "model": "openrouter/moonshotai/kimi-k2.6",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }

            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"API error: {response.status_code} {response.text}")
                return ""
        except Exception as e:
            logger.error(f"Error calling planning model: {e}")
            return ""

    def call_execution_model(self, prompt: str,
                            context: Optional[Dict] = None) -> str:
        """Call Laguna S 2.1 (execution model) via Bifrost"""
        try:
            payload = {
                "model": "openrouter/poolside/laguna-s-2.1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,  # Lower temp for code
                "max_tokens": 4000
            }

            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"API error: {response.status_code} {response.text}")
                return ""
        except Exception as e:
            logger.error(f"Error calling execution model: {e}")
            return ""


class ReActAgent:
    """Main ReAct reasoning agent"""

    def __init__(self, gateway: BifrostGateway,
                 artifact_logger: EmpiricalArtifactLogger):
        self.gateway = gateway
        self.logger = artifact_logger
        self.reasoning_chain: List[ReActStep] = []
        self.task_context: Optional[AgentTask] = None

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task through full ReAct loop"""
        logger.info(f"Starting task: {task.title}")
        self.task_context = task
        self.reasoning_chain = []

        # Phase 1: Understanding
        logger.info("Phase 1: Understanding task...")
        understanding = self._phase_understanding(task)

        # Phase 2: Planning
        logger.info("Phase 2: Planning approach...")
        planning = self._phase_planning(task, understanding)

        # Phase 3: Execution
        logger.info("Phase 3: Executing plan...")
        execution = self._phase_execution(task, planning)

        # Phase 4: Reflection
        logger.info("Phase 4: Reflecting on results...")
        reflection = self._phase_reflection(task, execution)

        # Return complete reasoning trace
        return {
            "task_id": task.id,
            "status": "complete",
            "reasoning_chain": self.reasoning_chain,
            "understanding": understanding,
            "planning": planning,
            "execution": execution,
            "reflection": reflection,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _phase_understanding(self, task: AgentTask) -> Dict[str, Any]:
        """Phase 1: Understand the task"""

        # Ask planning model to understand task
        prompt = f"""Analyze and understand this task:

Title: {task.title}
Description: {task.description}
Requesting Practice: {task.requesting_practice}
Context: {json.dumps(task.context or {})}
Success Criteria: {task.success_criteria or "Not specified"}

What do you understand about this task? What are the key requirements?
What assumptions are you making? What needs clarification?"""

        response = self.gateway.call_planning_model(prompt)

        # Log findings from understanding
        if response:
            self.logger.log_finding(
                f"Task analysis complete: {task.title}. Key insights documented.",
                impact=0.8,
                phase="understanding"
            )

        return {
            "analysis": response,
            "assumptions": self._extract_assumptions(response),
            "clarity": 0.75
        }

    def _phase_planning(self, task: AgentTask,
                       understanding: Dict) -> Dict[str, Any]:
        """Phase 2: Plan the approach"""

        prompt = f"""Based on this understanding of the task:
{understanding['analysis'][:1000]}

Now plan your approach:
1. What approach will you take?
2. Why this approach over alternatives?
3. What are the main steps?
4. What could go wrong?

Provide structured plan with rationale."""

        response = self.gateway.call_planning_model(prompt)

        # Log planning decision
        if response:
            self.logger.log_decision(
                choice=f"Approach planned for {task.title}",
                rationale=response[:200],
                reversibility="exploratory"
            )

        return {
            "approach": response,
            "steps": self._extract_steps(response),
            "confidence": 0.70
        }

    def _phase_execution(self, task: AgentTask,
                        planning: Dict) -> Dict[str, Any]:
        """Phase 3: Execute the plan"""

        prompt = f"""Execute this plan:
{planning['approach'][:1000]}

Provide detailed implementation/analysis:
- Step-by-step execution
- Code/pseudocode where relevant
- Rationale for each step
- Handling of edge cases"""

        response = self.gateway.call_execution_model(prompt)

        # Log findings from execution
        if response:
            self.logger.log_finding(
                f"Execution complete for {task.title}. Results documented.",
                impact=0.85,
                phase="execution"
            )

        return {
            "output": response,
            "success": bool(response),
            "quality": 0.75
        }

    def _phase_reflection(self, task: AgentTask,
                         execution: Dict) -> Dict[str, Any]:
        """Phase 4: Reflect on results"""

        prompt = f"""Reflect on this execution result:
{execution['output'][:1000]}

For task: {task.title}
Success criteria: {task.success_criteria or "Not specified"}

Did we succeed? What would you change? What did we learn?"""

        response = self.gateway.call_planning_model(prompt)

        return {
            "reflection": response,
            "success_assessment": self._assess_success(response, task),
            "lessons": self._extract_lessons(response)
        }

    def _extract_assumptions(self, text: str) -> List[str]:
        """Extract assumptions from response text"""
        # Simple heuristic: look for "assume", "assuming", etc.
        assumptions = []
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['assume', 'assuming', 'presume', 'expect']):
                assumptions.append(line.strip())
        return assumptions[:5]  # Return top 5

    def _extract_steps(self, text: str) -> List[str]:
        """Extract steps from response text"""
        steps = []
        lines = text.split('\n')
        for line in lines:
            if any(line.strip().startswith(prefix) for prefix in ['1.', '2.', '-', '*', '•']):
                steps.append(line.strip())
        return steps[:10]  # Return top 10

    def _assess_success(self, reflection: str, task: AgentTask) -> bool:
        """Simple heuristic: assess if task was successful"""
        success_keywords = ['succeeded', 'success', 'complete', 'accomplished', 'done']
        failure_keywords = ['failed', 'blocked', 'unable', 'incomplete']

        reflection_lower = reflection.lower()

        success_count = sum(1 for word in success_keywords if word in reflection_lower)
        failure_count = sum(1 for word in failure_keywords if word in reflection_lower)

        return success_count >= failure_count

    def _extract_lessons(self, text: str) -> List[str]:
        """Extract lessons learned from response"""
        lessons = []
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['learn', 'lesson', 'found that', 'discovered']):
                lessons.append(line.strip())
        return lessons[:5]


def main():
    """Main entry point for agent"""

    # Initialize components
    gateway = BifrostGateway()
    artifact_logger = EmpiricalArtifactLogger()
    agent = ReActAgent(gateway, artifact_logger)

    # Check gateway health
    if not gateway.health_check():
        logger.error("Bifrost gateway is not responding. Start it with: docker-compose up")
        return

    logger.info("Bifrost gateway is healthy")

    # Example pilot task: autonomy gates design
    pilot_task = AgentTask(
        id="gates-a.0.1-design",
        title="Design state machine for gates feature A.0.1",
        description="""
        Autonomy practice needs to design state machine for gates feature A.0.1.
        Requirements:
        - Support task acceptance/rejection workflow
        - Handle concurrent requests
        - Enable priority-based execution
        - Support cancellation midway

        Analyze architecture options, recommend approach, identify risks.
        """,
        requesting_practice="empirica-foundation.carly.empirica-autonomy",
        context={
            "existing_patterns": ["state machine in routes", "task queue in persistence"],
            "constraints": ["must integrate with existing auth", "minimize latency"],
            "related_features": ["A.0.2 reporting", "A.0.3 cancellation"]
        },
        success_criteria="Clear architecture document with state transitions, rationale, and integration points"
    )

    # Execute task
    logger.info("Executing pilot task...")
    result = agent.execute_task(pilot_task)

    # Save results
    results_file = "/tmp/agent-pilot-results.json"
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2)

    logger.info(f"Pilot task complete. Results saved to {results_file}")
    logger.info(f"Task success: {result['reflection']['success_assessment']}")

    return result


if __name__ == "__main__":
    main()
