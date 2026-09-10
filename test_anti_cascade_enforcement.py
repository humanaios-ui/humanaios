#!/usr/bin/env python3
"""
test_anti_cascade_enforcement.py — Anti-cascade Rule Enforcement Tests

Verify all 5 anti-cascade rules are properly enforced in molt_cycle.py:
1. One open molt per constant (no new candidate inside window W)
2. No self-reference (candidate not from events in its own window)
3. K=3 system-wide limit on open molts
4. Freeze after 2 reverts (Z2 Tier 2 override required)
5. Ranking by Priority Queue score (no bypass)
"""

import json
import unittest
from datetime import datetime, timezone, timedelta
from collections import defaultdict

from molt_cycle import MoltCycle, MoltCycleState, MoltPhase


class TestAntiCascadeRule1(unittest.TestCase):
    """Test Rule 1: One open molt per constant (no new candidate inside window W)."""

    def setUp(self):
        self.mc = MoltCycle(k_limit=3)

    def test_rule1_allows_first_molt_candidate(self):
        """First molt candidate for a constant should be allowed."""
        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule1_violations = [v for v in violations if 'Rule 1' in v]
        self.assertEqual(len(rule1_violations), 0, "First candidate should not violate Rule 1")

    def test_rule1_blocks_second_molt_candidate_same_constant(self):
        """Second molt candidate for same constant should violate Rule 1."""
        # Mark constant as having open molt
        self.mc.state.constants_in_molt['PRIOR_QUALITY'] = 'molt-001'

        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule1_violations = [v for v in violations if 'Rule 1' in v]
        self.assertGreater(len(rule1_violations), 0, "Second candidate should violate Rule 1")


class TestAntiCascadeRule2(unittest.TestCase):
    """Test Rule 2: No self-reference (candidate not from events in its own window)."""

    def setUp(self):
        self.mc = MoltCycle(k_limit=3)

    def test_rule2_allows_candidate_outside_window(self):
        """Candidate proposed outside its measurement window should be allowed."""
        # Simulate events from 30 days ago
        old_dt = datetime.now(timezone.utc) - timedelta(days=40)
        self.mc.nf_entries = [
            {
                'type': 'VERDICT',
                'at': old_dt.isoformat(),
                'target': 'quality_forecast',
                'constant': 'PRIOR_QUALITY',
            }
        ]

        # Propose candidate now (40 days after the event)
        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule2_violations = [v for v in violations if 'Rule 2' in v]
        self.assertEqual(len(rule2_violations), 0, "Event outside window should not violate Rule 2")

    def test_rule2_blocks_self_referential_candidate(self):
        """Candidate generated from events in its own window should violate Rule 2."""
        # Simulate event within window
        now = datetime.now(timezone.utc)
        recent_dt = now - timedelta(days=15)  # 15 days ago, within 30-day window

        self.mc.nf_entries = [
            {
                'type': 'VERDICT',
                'at': recent_dt.isoformat(),
                'target': 'quality_forecast',
                'constant': 'PRIOR_QUALITY',
            }
        ]

        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': now.isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule2_violations = [v for v in violations if 'Rule 2' in v]
        self.assertGreater(len(rule2_violations), 0, "Event within window should violate Rule 2")


class TestAntiCascadeRule3(unittest.TestCase):
    """Test Rule 3: K=3 system-wide limit on open molts."""

    def setUp(self):
        self.mc = MoltCycle(k_limit=3)

    def test_rule3_allows_below_k_limit(self):
        """Candidate when open_molts < K should be allowed."""
        self.mc.state.open_molts_count = 2  # Below K=3

        candidate = {
            'name': 'NEW_CONSTANT',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule3_violations = [v for v in violations if 'Rule 3' in v]
        self.assertEqual(len(rule3_violations), 0, "Count < K should not violate Rule 3")

    def test_rule3_blocks_at_k_limit(self):
        """Candidate when open_molts >= K should violate Rule 3."""
        self.mc.state.open_molts_count = 3  # At K=3

        candidate = {
            'name': 'ANOTHER_CONSTANT',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule3_violations = [v for v in violations if 'Rule 3' in v]
        self.assertGreater(len(rule3_violations), 0, "Count >= K should violate Rule 3")

    def test_rule3_blocks_above_k_limit(self):
        """Candidate when open_molts > K should violate Rule 3."""
        self.mc.state.open_molts_count = 5  # Above K=3

        candidate = {
            'name': 'YET_ANOTHER',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule3_violations = [v for v in violations if 'Rule 3' in v]
        self.assertGreater(len(rule3_violations), 0, "Count > K should violate Rule 3")


class TestAntiCascadeRule4(unittest.TestCase):
    """Test Rule 4: Freeze after 2 reverts (Z2 Tier 2 override required)."""

    def setUp(self):
        self.mc = MoltCycle(k_limit=3)

    def test_rule4_allows_unfrozen_constant(self):
        """Candidate for unfrozen constant should be allowed."""
        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule4_violations = [v for v in violations if 'Rule 4' in v]
        self.assertEqual(len(rule4_violations), 0, "Unfrozen constant should not violate Rule 4")

    def test_rule4_blocks_frozen_constant(self):
        """Candidate for frozen constant should violate Rule 4."""
        self.mc.state.constants_frozen.add('PRIOR_QUALITY')

        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule4_violations = [v for v in violations if 'Rule 4' in v]
        self.assertGreater(len(rule4_violations), 0, "Frozen constant should violate Rule 4")


class TestAntiCascadeRule5(unittest.TestCase):
    """Test Rule 5: Ranking by Priority Queue score (no bypass)."""

    def setUp(self):
        self.mc = MoltCycle(k_limit=3)

    def test_rule5_allows_ranked_candidate(self):
        """Candidate with valid PQ rank should be allowed."""
        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            'priority_queue_rank': 1,
            'priority_queue_score': 50.0,
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule5_violations = [v for v in violations if 'Rule 5' in v]
        self.assertEqual(len(rule5_violations), 0, "Ranked candidate should not violate Rule 5")

    def test_rule5_blocks_unranked_candidate(self):
        """Candidate without PQ rank should violate Rule 5."""
        candidate = {
            'name': 'PRIOR_QUALITY',
            'proposed_at': datetime.now(timezone.utc).isoformat(),
            'measurement_window_days': 30,
            # No priority_queue_rank field
        }
        violations = self.mc._validate_anti_cascade_rules(candidate)
        rule5_violations = [v for v in violations if 'Rule 5' in v]
        self.assertGreater(len(rule5_violations), 0, "Unranked candidate should violate Rule 5")


class TestAntiCascadeProposeMolts(unittest.TestCase):
    """Test propose_molts() with anti-cascade rule filtering."""

    def setUp(self):
        self.mc = MoltCycle(k_limit=3)

    def test_propose_molts_filters_violations(self):
        """propose_molts should filter candidates by rule violations."""
        # Create 3 candidates: 1 valid, 2 with violations
        candidates = [
            {
                'name': 'VALID_CONSTANT',
                'proposed_at': datetime.now(timezone.utc).isoformat(),
                'measurement_window_days': 30,
                'priority_queue_rank': 1,
                'priority_queue_score': 50.0,
            },
            {
                'name': 'FROZEN_CONSTANT',
                'proposed_at': datetime.now(timezone.utc).isoformat(),
                'measurement_window_days': 30,
                'priority_queue_rank': 1,
                'priority_queue_score': 50.0,
            },
            {
                'name': 'UNRANKED',
                'proposed_at': datetime.now(timezone.utc).isoformat(),
                'measurement_window_days': 30,
                # No rank
            },
        ]

        # Freeze one constant
        self.mc.state.constants_frozen.add('FROZEN_CONSTANT')

        result = self.mc.propose_molts(candidates)

        # Should have 1 valid candidate, 2 violations
        self.assertEqual(result['candidates_proposed'], 1, "Only 1 candidate should pass rules")
        self.assertEqual(result['violations_count'], 2, "2 candidates should have violations")
        self.assertEqual(
            [c['name'] for c in result['candidates']],
            ['VALID_CONSTANT'],
            "Only VALID_CONSTANT should be in proposals"
        )

    def test_propose_molts_reports_violations(self):
        """propose_molts should report detailed violation reasons."""
        self.mc.state.constants_frozen.add('FROZEN')
        self.mc.state.constants_in_molt['OPEN'] = 'molt-001'
        self.mc.state.open_molts_count = 3

        candidates = [
            {
                'name': 'FROZEN',
                'proposed_at': datetime.now(timezone.utc).isoformat(),
                'measurement_window_days': 30,
                'priority_queue_rank': 1,
                'priority_queue_score': 50.0,
            },
            {
                'name': 'OPEN',
                'proposed_at': datetime.now(timezone.utc).isoformat(),
                'measurement_window_days': 30,
                'priority_queue_rank': 2,
                'priority_queue_score': 45.0,
            },
        ]

        result = self.mc.propose_molts(candidates)

        # Check violations are reported
        self.assertEqual(len(result['rule_violations']), 2)
        frozen_violation = next(v for v in result['rule_violations'] if v['constant'] == 'FROZEN')
        open_violation = next(v for v in result['rule_violations'] if v['constant'] == 'OPEN')

        # Verify rule descriptions
        self.assertTrue(any('Rule 4' in v for v in frozen_violation['violations']))
        self.assertTrue(any('Rule 1' in v for v in open_violation['violations']))


if __name__ == '__main__':
    unittest.main()
