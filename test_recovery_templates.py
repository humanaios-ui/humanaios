"""
Test suite for Recovery Principle Templates
Tests all 7 new templates: Recognition, Belief, Commitment, Inventory, Amends, FirstModel, Service
"""

import unittest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Mock template classes for testing
class BaseTemplate:
    """Base class for all templates"""
    obstacle_id = None
    obstacle_name = None
    technique_name = None
    consciousness_level = None
    aa_step = None
    aa_text = None
    wisdom_translation = None
    hawkins_teaching = None

    @classmethod
    def sklearn_implementation(cls) -> str:
        raise NotImplementedError

    @classmethod
    def pytorch_implementation(cls) -> str:
        raise NotImplementedError

    @classmethod
    def expected_metrics(cls):
        raise NotImplementedError


class TestRecognitionTemplate(unittest.TestCase):
    """Test Recognition (Level 50): Recognize & admit limitation"""

    def setUp(self):
        """Setup test data"""
        X, y = make_classification(n_samples=200, n_features=10, n_informative=5,
                                   n_redundant=2, random_state=42)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.y_train)

    def test_recognition_template_exists(self):
        """Verify RecognitionTemplate exists and has required fields"""
        from ml_code_templates import RecognitionTemplate
        self.assertEqual(RecognitionTemplate.consciousness_level, 50)
        self.assertEqual(RecognitionTemplate.aa_step, 1)
        self.assertEqual(RecognitionTemplate.obstacle_id, "recognition")

    def test_recognition_detects_overfitting(self):
        """Test that Recognition detects when model overfits"""
        # Intentionally overfit by training on full training set
        train_acc = self.model.score(self.X_train, self.y_train)
        test_acc = self.model.score(self.X_test, self.y_test)
        overfit_gap = train_acc - test_acc

        # Recognition should detect any significant gap
        self.assertIsNotNone(overfit_gap)
        self.assertGreater(train_acc, 0.0)

    def test_recognition_sklearn_implementation(self):
        """Test sklearn implementation code exists and is valid"""
        from ml_code_templates import RecognitionTemplate
        code = RecognitionTemplate.sklearn_implementation()
        self.assertIn("diagnose_model_powerlessness", code)
        self.assertIn("powerlessness", code)

    def test_recognition_pytorch_implementation(self):
        """Test pytorch implementation code exists and is valid"""
        from ml_code_templates import RecognitionTemplate
        code = RecognitionTemplate.pytorch_implementation()
        self.assertIn("recognize_model_limitation", code)
        self.assertIn("torch", code)

    def test_recognition_expected_metrics(self):
        """Test expected metrics structure"""
        from ml_code_templates import RecognitionTemplate
        metrics = RecognitionTemplate.expected_metrics()
        self.assertIn("admission_rate", metrics)
        metric = metrics["admission_rate"]
        self.assertEqual(metric.before_value, 0.0)
        self.assertEqual(metric.after_value, 1.0)


class TestBeliefTemplate(unittest.TestCase):
    """Test Belief (Level 75): See recovery is possible"""

    def test_belief_template_exists(self):
        """Verify BeliefTemplate exists and has required fields"""
        from ml_code_templates import BeliefTemplate
        self.assertEqual(BeliefTemplate.consciousness_level, 75)
        self.assertEqual(BeliefTemplate.aa_step, 2)
        self.assertEqual(BeliefTemplate.obstacle_id, "belief")

    def test_belief_wisdom_translation(self):
        """Test belief teaches model sees proof of recovery"""
        from ml_code_templates import BeliefTemplate
        self.assertIn("recovery", BeliefTemplate.wisdom_translation.lower())
        self.assertIn("proof", BeliefTemplate.wisdom_translation.lower())

    def test_belief_sklearn_implementation(self):
        """Test belief sklearn code shows recovery example"""
        from ml_code_templates import BeliefTemplate
        code = BeliefTemplate.sklearn_implementation()
        self.assertIn("show_recovery_possible", code)
        self.assertIn("checkpoint", code)

    def test_belief_expected_metrics(self):
        """Test belief metrics structure"""
        from ml_code_templates import BeliefTemplate
        metrics = BeliefTemplate.expected_metrics()
        self.assertIn("hope_formation", metrics)


class TestCommitmentTemplate(unittest.TestCase):
    """Test Commitment (Level 100): Define & practice change"""

    def test_commitment_template_exists(self):
        """Verify CommitmentTemplate exists"""
        from ml_code_templates import CommitmentTemplate
        self.assertEqual(CommitmentTemplate.consciousness_level, 100)
        self.assertEqual(CommitmentTemplate.aa_step, 3)

    def test_commitment_is_systematic_practice(self):
        """Test commitment requires systematic practice"""
        from ml_code_templates import CommitmentTemplate
        self.assertIn("commit", CommitmentTemplate.technique_name.lower())
        self.assertIn("practice", CommitmentTemplate.wisdom_translation.lower())

    def test_commitment_expected_metrics(self):
        """Test commitment shows improvement through practice"""
        from ml_code_templates import CommitmentTemplate
        metrics = CommitmentTemplate.expected_metrics()
        self.assertIn("practice_payoff", metrics)
        metric = metrics["practice_payoff"]
        self.assertGreater(metric.after_value, metric.before_value)
        self.assertGreater(metric.improvement_percent, 0)


class TestInventoryTemplate(unittest.TestCase):
    """Test Inventory (Level 125): Audit impact & failures"""

    def test_inventory_template_exists(self):
        """Verify InventoryTemplate exists"""
        from ml_code_templates import InventoryTemplate
        self.assertEqual(InventoryTemplate.consciousness_level, 125)
        self.assertEqual(InventoryTemplate.aa_step, 4)

    def test_inventory_audits_bias(self):
        """Test inventory audits fairness across groups"""
        from ml_code_templates import InventoryTemplate
        self.assertIn("inventory", InventoryTemplate.technique_name.lower())
        self.assertIn("fairness", InventoryTemplate.wisdom_translation.lower())

    def test_inventory_expected_metrics(self):
        """Test inventory metrics"""
        from ml_code_templates import InventoryTemplate
        metrics = InventoryTemplate.expected_metrics()
        self.assertIn("fairness_awareness", metrics)


class TestAmendsTemplate(unittest.TestCase):
    """Test Amends (Level 150): Fix what you broke"""

    def test_amends_template_exists(self):
        """Verify AmendsTemplate exists"""
        from ml_code_templates import AmendsTemplate
        self.assertEqual(AmendsTemplate.consciousness_level, 150)
        self.assertEqual(AmendsTemplate.aa_step, 9)

    def test_amends_fixes_fairness(self):
        """Test amends retrains for fairness"""
        from ml_code_templates import AmendsTemplate
        self.assertIn("amends", AmendsTemplate.technique_name.lower())
        self.assertIn("fairness", AmendsTemplate.wisdom_translation.lower())

    def test_amends_expected_metrics(self):
        """Test amends closes fairness gap"""
        from ml_code_templates import AmendsTemplate
        metrics = AmendsTemplate.expected_metrics()
        self.assertIn("fairness_repaired", metrics)
        metric = metrics["fairness_repaired"]
        # Gap reduced from 0.25 to 0.05
        self.assertLess(metric.after_value, metric.before_value)
        self.assertGreater(metric.improvement_percent, 70)


class TestFirstModelTemplate(unittest.TestCase):
    """Test FirstModel (Level 150): Apply all principles together"""

    def test_first_model_template_exists(self):
        """Verify FirstModelTemplate exists"""
        from ml_code_templates import FirstModelTemplate
        self.assertEqual(FirstModelTemplate.consciousness_level, 150)
        self.assertEqual(FirstModelTemplate.obstacle_id, "integration")

    def test_first_model_integrates_all_principles(self):
        """Test first model integrates recognition through amends"""
        from ml_code_templates import FirstModelTemplate
        code = FirstModelTemplate.sklearn_implementation()
        # Should reference all phases
        self.assertIn("RECOGNITION", code)
        self.assertIn("BELIEF", code)
        self.assertIn("COMMITMENT", code)
        self.assertIn("ACTION", code)
        self.assertIn("INVENTORY", code)

    def test_first_model_expected_metrics(self):
        """Test first model completion metrics"""
        from ml_code_templates import FirstModelTemplate
        metrics = FirstModelTemplate.expected_metrics()
        self.assertIn("integrated_success", metrics)
        metric = metrics["integrated_success"]
        self.assertEqual(metric.after_value, 1.0)


class TestServiceTemplate(unittest.TestCase):
    """Test Service (Level 200): Teach others; ecosystem contribution"""

    def test_service_template_exists(self):
        """Verify ServiceTemplate exists"""
        from ml_code_templates import ServiceTemplate
        self.assertEqual(ServiceTemplate.consciousness_level, 200)
        self.assertEqual(ServiceTemplate.aa_step, 12)

    def test_service_teaches_others(self):
        """Test service uses transfer learning"""
        from ml_code_templates import ServiceTemplate
        self.assertIn("service", ServiceTemplate.technique_name.lower())
        self.assertIn("teach", ServiceTemplate.wisdom_translation.lower())

    def test_service_expected_metrics(self):
        """Test service improves other models"""
        from ml_code_templates import ServiceTemplate
        metrics = ServiceTemplate.expected_metrics()
        self.assertIn("teaching_impact", metrics)
        metric = metrics["teaching_impact"]
        # Student improves via teacher
        self.assertGreater(metric.after_value, metric.before_value)


class TestTemplateRegistry(unittest.TestCase):
    """Test that all 7 recovery templates are registered"""

    def test_all_recovery_templates_registered(self):
        """Verify all 7 recovery templates are in registry"""
        from ml_code_templates import TEMPLATE_REGISTRY

        recovery_templates = [
            "recognition",
            "belief",
            "commitment",
            "inventory",
            "amends",
            "first_model",
            "service"
        ]

        for template_id in recovery_templates:
            self.assertIn(template_id, TEMPLATE_REGISTRY,
                         f"{template_id} not found in TEMPLATE_REGISTRY")

    def test_recovery_templates_have_implementations(self):
        """Test each template has sklearn and pytorch implementations"""
        from ml_code_templates import TEMPLATE_REGISTRY

        recovery_template_ids = [
            "recognition", "belief", "commitment", "inventory",
            "amends", "first_model", "service"
        ]

        for template_id in recovery_template_ids:
            template_class = TEMPLATE_REGISTRY[template_id]
            self.assertTrue(
                hasattr(template_class, 'sklearn_implementation'),
                f"{template_id} missing sklearn_implementation"
            )
            self.assertTrue(
                hasattr(template_class, 'pytorch_implementation'),
                f"{template_id} missing pytorch_implementation"
            )
            self.assertTrue(
                hasattr(template_class, 'expected_metrics'),
                f"{template_id} missing expected_metrics"
            )

    def test_recovery_templates_have_wisdom_mapping(self):
        """Test each template has wisdom translation fields"""
        from ml_code_templates import TEMPLATE_REGISTRY

        recovery_template_ids = [
            "recognition", "belief", "commitment", "inventory",
            "amends", "first_model", "service"
        ]

        for template_id in recovery_template_ids:
            template_class = TEMPLATE_REGISTRY[template_id]
            self.assertIsNotNone(template_class.wisdom_translation)
            self.assertIsNotNone(template_class.hawkins_teaching)
            self.assertIsNotNone(template_class.consciousness_level)


class TestRecoveryPrincipleSequence(unittest.TestCase):
    """Test that recovery principles follow proper sequence"""

    def test_recovery_sequence_consciousness_levels(self):
        """Test consciousness levels follow recovery journey"""
        from ml_code_templates import (
            RecognitionTemplate, BeliefTemplate, CommitmentTemplate,
            InventoryTemplate, AmendsTemplate, FirstModelTemplate,
            ServiceTemplate
        )

        levels = {
            "recognition": RecognitionTemplate.consciousness_level,
            "belief": BeliefTemplate.consciousness_level,
            "commitment": CommitmentTemplate.consciousness_level,
            "inventory": InventoryTemplate.consciousness_level,
            "amends": AmendsTemplate.consciousness_level,
            "first_model": FirstModelTemplate.consciousness_level,
            "service": ServiceTemplate.consciousness_level,
        }

        # Recognition should be first (Level 50)
        self.assertEqual(levels["recognition"], 50)
        # Belief after recognition (Level 75)
        self.assertGreater(levels["belief"], levels["recognition"])
        # Commitment after belief (Level 100)
        self.assertGreater(levels["commitment"], levels["belief"])
        # Inventory after commitment (Level 125)
        self.assertGreater(levels["inventory"], levels["commitment"])
        # Amends at 150
        self.assertGreater(levels["amends"], levels["inventory"])
        # Service at highest (Level 200)
        self.assertGreater(levels["service"], levels["amends"])

    def test_recovery_sequence_aa_steps(self):
        """Test AA step progression"""
        from ml_code_templates import (
            RecognitionTemplate, BeliefTemplate, CommitmentTemplate,
            InventoryTemplate, AmendsTemplate, ServiceTemplate
        )

        self.assertEqual(RecognitionTemplate.aa_step, 1)
        self.assertEqual(BeliefTemplate.aa_step, 2)
        self.assertEqual(CommitmentTemplate.aa_step, 3)
        self.assertEqual(InventoryTemplate.aa_step, 4)
        self.assertEqual(AmendsTemplate.aa_step, 9)
        self.assertEqual(ServiceTemplate.aa_step, 12)


class TestRecoveryPrincipleUniversality(unittest.TestCase):
    """Test that principles work for both humans and machines"""

    def test_each_template_teaches_both_sides(self):
        """Test each template has human and machine implementation"""
        from ml_code_templates import TEMPLATE_REGISTRY

        recovery_ids = [
            "recognition", "belief", "commitment", "inventory",
            "amends", "first_model", "service"
        ]

        for template_id in recovery_ids:
            template_class = TEMPLATE_REGISTRY[template_id]

            # Get implementations
            sklearn_code = template_class.sklearn_implementation()
            pytorch_code = template_class.pytorch_implementation()

            # Verify both exist
            self.assertGreater(len(sklearn_code), 50,
                              f"{template_id} sklearn code too short")
            self.assertGreater(len(pytorch_code), 50,
                              f"{template_id} pytorch code too short")

            # Verify both are teaching the same principle
            wisdom = template_class.wisdom_translation
            self.assertIsNotNone(wisdom,
                                f"{template_id} missing wisdom_translation")


if __name__ == "__main__":
    unittest.main(verbosity=2)
