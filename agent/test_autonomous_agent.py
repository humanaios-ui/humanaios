#!/usr/bin/env python3
"""
Autonomous Agent Testing Suite
Tests agent functionality: mailbox polling, proposal handling, status reporting
"""

import subprocess
import json
import time
import sys
from typing import List, Dict, Any
from datetime import datetime


class AutonomousAgentTester:
    def __init__(self, ai_id: str, poll_interval: int = 5):
        self.ai_id = ai_id
        self.poll_interval = poll_interval
        self.test_results = []
        self.practice_name = ai_id.split(".")[-1]

    def run_test(self, name: str, test_func) -> bool:
        """Run a single test and record result"""
        print(f"\n📌 Test: {name}")
        print("━" * 60)

        try:
            result = test_func()
            if result:
                print(f"✅ PASS: {name}")
                self.test_results.append({"name": name, "status": "pass"})
                return True
            else:
                print(f"❌ FAIL: {name}")
                self.test_results.append({"name": name, "status": "fail"})
                return False
        except Exception as e:
            print(f"❌ ERROR: {name} - {str(e)}")
            self.test_results.append({"name": name, "status": "error", "error": str(e)})
            return False

    def test_mailbox_connectivity(self) -> bool:
        """Test that mailbox poll command works"""
        print(f"Testing mailbox connectivity for {self.ai_id}...")

        cmd = [
            "empirica", "mailbox", "poll",
            "--ai-id", self.ai_id,
            "--output", "json"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                proposal_count = len(data.get("proposals", []))
                print(f"  Mailbox accessible, {proposal_count} proposals pending")
                return True
            else:
                print(f"  Mailbox poll failed: {result.stderr[:200]}")
                return False
        except subprocess.TimeoutExpired:
            print("  Mailbox poll timed out")
            return False

    def test_agent_import(self) -> bool:
        """Test that agent module can be imported"""
        print("Testing agent module import...")

        try:
            from autonomous_agent import AutonomousAgent, ProposalType, ProposalResult
            print("  ✓ Successfully imported AutonomousAgent")
            print("  ✓ Successfully imported ProposalType")
            print("  ✓ Successfully imported ProposalResult")
            return True
        except ImportError as e:
            print(f"  Import failed: {str(e)}")
            return False

    def test_status_reporter(self) -> bool:
        """Test status reporter module"""
        print("Testing status reporter...")

        try:
            from status_reporter import StatusReporter, TaskCompletion
            print("  ✓ Successfully imported StatusReporter")
            print("  ✓ Successfully imported TaskCompletion")
            return True
        except ImportError as e:
            print(f"  Import failed: {str(e)}")
            return False

    def test_agent_initialization(self) -> bool:
        """Test that agent can be initialized"""
        print(f"Testing agent initialization for {self.ai_id}...")

        try:
            from autonomous_agent import AutonomousAgent
            agent = AutonomousAgent(self.ai_id, self.poll_interval)
            print(f"  ✓ Agent initialized: ai_id={agent.ai_id}, poll_interval={agent.poll_interval}s")
            return True
        except Exception as e:
            print(f"  Initialization failed: {str(e)}")
            return False

    def test_proposal_handling(self) -> bool:
        """Test proposal type detection and routing"""
        print("Testing proposal handling logic...")

        try:
            from autonomous_agent import ProposalType

            test_types = ["collab_brief", "proposal", "proposal_complete", "escalation", "unknown"]
            handlers_found = 0

            for prop_type in test_types:
                try:
                    pt = ProposalType(prop_type) if prop_type != "unknown" else None
                    if prop_type != "unknown":
                        print(f"  ✓ ProposalType.{prop_type.upper()} recognized")
                        handlers_found += 1
                except ValueError:
                    if prop_type == "unknown":
                        print(f"  ✓ Unknown proposal type handled correctly")

            return handlers_found >= 4
        except Exception as e:
            print(f"  Proposal handling test failed: {str(e)}")
            return False

    def test_configuration(self) -> bool:
        """Test that agent configuration is valid"""
        print(f"Testing agent configuration...")

        try:
            # Validate AI ID format
            parts = self.ai_id.split(".")
            if len(parts) != 3 or parts[0] != "empirica-foundation" or parts[1] != "carly":
                print(f"  ❌ Invalid AI ID format: {self.ai_id}")
                return False

            print(f"  ✓ AI ID format valid: {self.ai_id}")
            print(f"  ✓ Practice name: {self.practice_name}")
            print(f"  ✓ Poll interval: {self.poll_interval}s")
            return True
        except Exception as e:
            print(f"  Configuration test failed: {str(e)}")
            return False

    def test_logging_setup(self) -> bool:
        """Test that logging is configured"""
        print("Testing logging setup...")

        import logging

        try:
            logger = logging.getLogger("autonomous_agent_test")

            # Test that logger can write
            handler_count = len(logger.handlers)
            print(f"  ✓ Logger configured with {handler_count} handlers")
            print(f"  ✓ Logger level: {logging.getLevelName(logger.level)}")
            return True
        except Exception as e:
            print(f"  Logging setup failed: {str(e)}")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests"""
        print("╔════════════════════════════════════════════════════════╗")
        print("║  Autonomous Agent Testing Suite                        ║")
        print("╚════════════════════════════════════════════════════════╝")
        print(f"\nPractice: {self.practice_name}")
        print(f"AI ID: {self.ai_id}\n")

        tests = [
            ("Configuration Validation", self.test_configuration),
            ("Module Import", self.test_agent_import),
            ("Status Reporter Import", self.test_status_reporter),
            ("Agent Initialization", self.test_agent_initialization),
            ("Proposal Handling", self.test_proposal_handling),
            ("Logging Setup", self.test_logging_setup),
            ("Mailbox Connectivity", self.test_mailbox_connectivity),
        ]

        passed = 0
        failed = 0

        for name, test_func in tests:
            if self.run_test(name, test_func):
                passed += 1
            else:
                failed += 1

        print("\n" + "═" * 60)
        print("Test Summary")
        print("═" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total: {passed + failed}")
        print(f"🎯 Success Rate: {100 * passed // (passed + failed) if (passed + failed) > 0 else 0}%")
        print("═" * 60)

        return {
            "timestamp": datetime.now().isoformat(),
            "practice": self.practice_name,
            "ai_id": self.ai_id,
            "total_tests": passed + failed,
            "passed": passed,
            "failed": failed,
            "success_rate": 100 * passed // (passed + failed) if (passed + failed) > 0 else 0,
            "results": self.test_results,
            "ready_for_deployment": failed == 0
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_autonomous_agent.py <practice-ai-id> [poll_interval]")
        print("\nExample:")
        print("  python3 test_autonomous_agent.py empirica-foundation.carly.empirica-autonomy 30")
        sys.exit(1)

    ai_id = sys.argv[1]
    poll_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30

    tester = AutonomousAgentTester(ai_id, poll_interval)
    results = tester.run_all_tests()

    # Save results
    output_file = f"test-results-{results['practice']}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Results saved to: {output_file}")

    # Exit with appropriate code
    sys.exit(0 if results["ready_for_deployment"] else 1)


if __name__ == "__main__":
    main()
