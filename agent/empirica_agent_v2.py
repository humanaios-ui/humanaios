#!/usr/bin/env python3
"""
Empirica Foundation Evaluator — Shared Internal Agent v2
Phase 2 Refinement: Improved model integration with retry logic

Enhancements:
- Retry logic with exponential backoff for timeouts
- Better response validation and error handling
- Detailed logging for debugging
- Result synchronization between model outputs and Empirica artifacts
"""

import json
import subprocess
import os
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import requests
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('empirica-agent-v2')


class ReActPhase(Enum):
    UNDERSTANDING = "understanding"
    PLANNING = "planning"
    EXECUTION = "execution"
    REFLECTION = "reflection"


@dataclass
class AgentTask:
    id: str
    title: str
    description: str
    requesting_practice: str
    context: Optional[Dict[str, Any]] = None
    success_criteria: Optional[str] = None


class BifrostGateway:
    """Client for Bifrost with retry logic"""

    def __init__(self, base_url: str = "http://localhost:8080",
                 api_key: Optional[str] = None, max_retries: int = 3):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.session = requests.Session()
        self.max_retries = max_retries
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })

    def health_check(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def call_model(self, model: str, prompt: str,
                   temperature: float = 0.7,
                   max_tokens: int = 2000) -> Tuple[bool, str]:
        """
        Call a model via Bifrost with retry logic.
        Returns: (success, response_text)
        """
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Calling {model} (attempt {attempt + 1}/{self.max_retries})")

                response = self.session.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    timeout=150  # Extended timeout for reasoning models
                )

                if response.status_code == 200:
                    result = response.json()
                    content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    if content:
                        logger.info(f"Model {model} response: {len(content)} chars")
                        return True, content
                    else:
                        logger.warning(f"Empty content from {model}")
                        return False, ""
                else:
                    logger.error(f"API error {response.status_code}: {response.text[:200]}")

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}, retrying...")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                return False, ""
            except Exception as e:
                logger.error(f"Error calling {model}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return False, ""

        return False, ""


class EmpiricalArtifactLogger:
    """Log agent reasoning as Empirica artifacts"""

    def __init__(self):
        self.empirica_path = "empirica"

    def log_finding(self, finding: str, impact: float = 0.7) -> bool:
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
                logger.info(f"✅ Finding logged: {finding[:80]}...")
                return True
            else:
                logger.error(f"Failed to log finding: {result.stderr[:100]}")
                return False
        except Exception as e:
            logger.error(f"Error logging finding: {e}")
            return False

    def log_decision(self, choice: str, rationale: str) -> bool:
        try:
            result = subprocess.run(
                [self.empirica_path, "decision-log",
                 "--choice", choice,
                 "--rationale", rationale,
                 "--reversibility", "exploratory"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"✅ Decision logged: {choice[:80]}...")
                return True
            else:
                logger.error(f"Failed to log decision: {result.stderr[:100]}")
                return False
        except Exception as e:
            logger.error(f"Error logging decision: {e}")
            return False

    def log_unknown(self, unknown: str) -> bool:
        try:
            result = subprocess.run(
                [self.empirica_path, "unknown-log",
                 "--unknown", unknown],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"✅ Unknown logged: {unknown[:80]}...")
                return True
            else:
                logger.error(f"Failed to log unknown: {result.stderr[:100]}")
                return False
        except Exception as e:
            logger.error(f"Error logging unknown: {e}")
            return False


class ReActAgent:
    """Improved ReAct agent with better response handling"""

    def __init__(self, gateway: BifrostGateway,
                 artifact_logger: EmpiricalArtifactLogger):
        self.gateway = gateway
        self.logger = artifact_logger
        self.task_context: Optional[AgentTask] = None
        self.outputs = {
            "understanding": "",
            "planning": "",
            "execution": "",
            "reflection": ""
        }

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        logger.info(f"🚀 Starting task: {task.title}")
        self.task_context = task

        # Phase 1: Understanding
        logger.info("📖 Phase 1: Understanding task...")
        understanding = self._phase_understanding(task)

        # Phase 2: Planning
        logger.info("🎯 Phase 2: Planning approach...")
        planning = self._phase_planning(task, understanding)

        # Phase 3: Execution
        logger.info("⚙️  Phase 3: Executing plan...")
        execution = self._phase_execution(task, planning)

        # Phase 4: Reflection
        logger.info("🔍 Phase 4: Reflecting on results...")
        reflection = self._phase_reflection(task, execution)

        return {
            "task_id": task.id,
            "status": "complete",
            "understanding": understanding,
            "planning": planning,
            "execution": execution,
            "reflection": reflection,
            "outputs": self.outputs
        }

    def _phase_understanding(self, task: AgentTask) -> Dict[str, Any]:
        prompt = f"""Analyze and understand this task:

Title: {task.title}
Description: {task.description}
Requesting Practice: {task.requesting_practice}
Context: {json.dumps(task.context or {})}
Success Criteria: {task.success_criteria or "Not specified"}

Provide your understanding in 2-3 sentences. What are the key requirements?
What assumptions are you making?"""

        success, response = self.gateway.call_model(
            "openrouter/moonshotai/kimi-k2.6",
            prompt,
            temperature=0.7,
            max_tokens=1000
        )

        self.outputs["understanding"] = response

        if success and response:
            self.logger.log_finding(
                f"Task analysis complete for '{task.title}': {response[:200]}...",
                impact=0.8
            )
        else:
            self.logger.log_unknown(
                f"Unable to fully analyze task '{task.title}' - model response incomplete"
            )

        return {
            "analysis": response,
            "success": success,
            "clarity": 0.8 if success else 0.5
        }

    def _phase_planning(self, task: AgentTask,
                       understanding: Dict) -> Dict[str, Any]:
        if not understanding.get("analysis"):
            logger.warning("Skipping planning - no understanding")
            return {"approach": "", "success": False}

        prompt = f"""Based on this understanding:
{understanding['analysis'][:500]}

Now plan your approach:
1. What approach will you take?
2. Why this approach?
3. What are the main steps?

Be concise and specific."""

        success, response = self.gateway.call_model(
            "openrouter/moonshotai/kimi-k2.6",
            prompt,
            temperature=0.7,
            max_tokens=1500
        )

        self.outputs["planning"] = response

        if success and response:
            self.logger.log_decision(
                choice=f"Approach for '{task.title}'",
                rationale=response[:300]
            )
        else:
            self.logger.log_unknown(
                f"Unable to formulate complete plan for '{task.title}'"
            )

        return {
            "approach": response,
            "success": success,
            "confidence": 0.8 if success else 0.4
        }

    def _phase_execution(self, task: AgentTask,
                        planning: Dict) -> Dict[str, Any]:
        if not planning.get("approach"):
            logger.warning("Skipping execution - no plan")
            return {"output": "", "success": False}

        prompt = f"""Execute this plan:
{planning['approach'][:500]}

Provide implementation details:
- Step-by-step execution
- Key decisions
- Rationale

Be thorough but concise."""

        success, response = self.gateway.call_model(
            "openrouter/poolside/laguna-s-2.1",
            prompt,
            temperature=0.3,
            max_tokens=2000
        )

        self.outputs["execution"] = response

        if success and response:
            self.logger.log_finding(
                f"Execution complete for '{task.title}': {response[:200]}...",
                impact=0.85
            )
        else:
            self.logger.log_unknown(
                f"Execution incomplete for '{task.title}' - model response failed"
            )

        return {
            "output": response,
            "success": success,
            "quality": 0.8 if success else 0.3
        }

    def _phase_reflection(self, task: AgentTask,
                         execution: Dict) -> Dict[str, Any]:
        prompt = f"""Reflect on this result:
{execution['output'][:500]}

For task: {task.title}

Did we succeed? What worked? What could improve?"""

        success, response = self.gateway.call_model(
            "openrouter/moonshotai/kimi-k2.6",
            prompt,
            temperature=0.7,
            max_tokens=1000
        )

        self.outputs["reflection"] = response

        return {
            "reflection": response,
            "success": success,
            "quality": 0.8 if success else 0.4
        }


def main():
    """Main entry point"""
    logger.info("🔌 Initializing agent...")
    gateway = BifrostGateway()
    artifact_logger = EmpiricalArtifactLogger()
    agent = ReActAgent(gateway, artifact_logger)

    if not gateway.health_check():
        logger.error("❌ Bifrost gateway not responding")
        return

    logger.info("✅ Bifrost gateway healthy")

    pilot_task = AgentTask(
        id="gates-a.0.1-design-v2",
        title="Design state machine for gates feature A.0.1",
        description="""Design a state machine for handling task acceptance/rejection workflow.
Requirements:
- Support task acceptance/rejection workflow
- Handle concurrent requests
- Enable priority-based execution
- Support cancellation midway

Analyze architecture options, recommend approach, identify risks.""",
        requesting_practice="empirica-foundation.carly.empirica-autonomy",
        context={
            "existing_patterns": ["state machine in routes", "task queue in persistence"],
            "constraints": ["must integrate with existing auth", "minimize latency"],
        },
        success_criteria="Clear architecture with state transitions, rationale, and integration points"
    )

    logger.info("🎬 Executing pilot task...")
    result = agent.execute_task(pilot_task)

    # Save results
    results_file = "/tmp/agent-pilot-results-v2.json"
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2)

    logger.info(f"✅ Pilot complete. Results: {results_file}")
    logger.info(f"📊 Understanding: {len(result['outputs']['understanding'])} chars")
    logger.info(f"📊 Planning: {len(result['outputs']['planning'])} chars")
    logger.info(f"📊 Execution: {len(result['outputs']['execution'])} chars")
    logger.info(f"📊 Reflection: {len(result['outputs']['reflection'])} chars")

    return result


if __name__ == "__main__":
    main()
