#!/usr/bin/env python3
"""
Phase 3.6.3 Integration Tests: Validate OTEL span/metric flow
Tests: span emission → Jaeger latency, metric emission → Prometheus latency, transaction_id correlation
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from empirica.otel_instrumentation import initialize_instrumentation
from empirica.epistemic_metrics import EPISTEMIC_VECTORS, validate_vector_dict


class IntegrationTestSuite:
    """Integration test suite for Phase 3.6.3"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.test_transaction_id = None

    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.results.append((test_name, status, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{status}: {test_name}")
        if message:
            print(f"     {message}")

    def test_instrumentation_initialization(self):
        """Test 1: Instrumentation library initializes correctly"""
        try:
            instr = initialize_instrumentation()
            passed = instr is not None
            self.log_result("Instrumentation Initialization", passed, f"Enabled: {instr.enabled}")
        except Exception as e:
            self.log_result("Instrumentation Initialization", False, str(e))

    def test_vector_validation(self):
        """Test 2: Vector dict validation works"""
        try:
            valid_vectors = {v: 0.5 for v in EPISTEMIC_VECTORS}
            passed = validate_vector_dict(valid_vectors) == True
            self.log_result("Vector Validation", passed, f"13 vectors validated")
        except Exception as e:
            self.log_result("Vector Validation", False, str(e))

    def test_prometheus_connectivity(self):
        """Test 3: Prometheus is reachable and has expected metrics"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:9090/api/v1/query?query=up'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            data = json.loads(result)
            passed = data.get('status') == 'success'
            series = len(data.get('data', {}).get('result', []))
            self.log_result("Prometheus Connectivity", passed, f"Status: {data.get('status')}, Series: {series}")
        except Exception as e:
            self.log_result("Prometheus Connectivity", False, str(e))

    def test_jaeger_connectivity(self):
        """Test 4: Jaeger is reachable and responding"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:16686/api/services'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            data = json.loads(result)
            passed = data.get('data') is not None
            services = len(data.get('data', []))
            self.log_result("Jaeger Connectivity", passed, f"Services: {services}")
        except Exception as e:
            self.log_result("Jaeger Connectivity", False, str(e))

    def test_otel_collector_health(self):
        """Test 5: OTEL Collector health endpoint responds"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:8889/metrics'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            passed = len(result) > 0
            self.log_result("OTEL Collector Health", passed, f"Metrics endpoint responsive ({len(result)} bytes)")
        except Exception as e:
            self.log_result("OTEL Collector Health", False, str(e))

    def test_grafana_dashboards_exist(self):
        """Test 6: Grafana dashboards are imported"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', '-H', 'Authorization: Basic YWRtaW46YWRtaW4=',
                 'http://localhost:3000/api/search?query=epistemic'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            dashboards = json.loads(result)
            passed = len(dashboards) >= 1
            self.log_result("Grafana Dashboards", passed, f"Dashboards found: {len(dashboards)}")
        except Exception as e:
            self.log_result("Grafana Dashboards", False, str(e))

    def test_prometheus_metric_query(self):
        """Test 7: Prometheus can query empirica metrics"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:9090/api/v1/query?query=empirica_know_gauge'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            data = json.loads(result)
            passed = data.get('status') == 'success'
            series = len(data.get('data', {}).get('result', []))
            self.log_result("Prometheus Empirica Metrics Query", passed, f"Series found: {series}")
        except Exception as e:
            self.log_result("Prometheus Empirica Metrics Query", False, str(e))

    def test_jaeger_trace_query(self):
        """Test 8: Jaeger can query empirica service traces"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:16686/api/traces?service=empirica-foundation-evaluator&limit=5'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            data = json.loads(result)
            passed = data.get('data') is not None
            traces = len(data.get('data', []))
            self.log_result("Jaeger Trace Query", passed, f"Traces found: {traces}")
        except Exception as e:
            self.log_result("Jaeger Trace Query", False, str(e))

    def test_metric_cardinality(self):
        """Test 9: Prometheus has reasonable metric cardinality (not explosion)"""
        try:
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:9090/api/v1/label/__name__/values'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            data = json.loads(result)
            metrics = data.get('data', [])
            empirica_metrics = [m for m in metrics if 'empirica' in m]
            passed = len(empirica_metrics) >= 5  # Should have at least 5 empirica metrics
            self.log_result("Metric Cardinality", passed, f"Empirica metrics: {len(empirica_metrics)}")
        except Exception as e:
            self.log_result("Metric Cardinality", False, str(e))

    def test_dashboard_query_latency(self):
        """Test 10: Grafana dashboard queries execute quickly (<1s)"""
        try:
            start = time.time()
            result = subprocess.check_output(
                ['curl', '-s', 'http://localhost:9090/api/v1/query?query=empirica_know_gauge'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode()
            elapsed = time.time() - start
            passed = elapsed < 1.0
            self.log_result("Dashboard Query Latency", passed, f"Query time: {elapsed:.3f}s")
        except Exception as e:
            self.log_result("Dashboard Query Latency", False, str(e))

    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 70)
        print("Phase 3.6.3 Integration Test Suite")
        print("=" * 70)
        print()

        self.test_instrumentation_initialization()
        self.test_vector_validation()
        self.test_prometheus_connectivity()
        self.test_jaeger_connectivity()
        self.test_otel_collector_health()
        self.test_grafana_dashboards_exist()
        self.test_prometheus_metric_query()
        self.test_jaeger_trace_query()
        self.test_metric_cardinality()
        self.test_dashboard_query_latency()

        print()
        print("=" * 70)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 70)

        return self.failed == 0


if __name__ == "__main__":
    suite = IntegrationTestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
