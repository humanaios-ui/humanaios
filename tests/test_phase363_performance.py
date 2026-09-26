#!/usr/bin/env python3
"""
Phase 3.6.3 Task 3.3: Performance Measurement
Measures CPU/memory overhead of instrumentation library + Prometheus scrape performance
"""

import sys
import time
import subprocess
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from empirica.otel_instrumentation import initialize_instrumentation
from empirica.epistemic_metrics import EPISTEMIC_VECTORS


class PerformanceTest:
    """Performance measurement suite"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def log_result(self, test_name: str, passed: bool, value: str = "", threshold: str = ""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.results.append((test_name, status, value, threshold))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{status}: {test_name}")
        if value or threshold:
            print(f"     Value: {value}, Threshold: {threshold}")

    def test_instrumentation_memory_overhead(self):
        """Test 1: Instrumentation library memory overhead"""
        try:
            import tracemalloc
            tracemalloc.start()

            # Measure baseline
            baseline = tracemalloc.take_snapshot()

            # Initialize instrumentation 100 times
            for i in range(100):
                instr = initialize_instrumentation()

            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.compare_to(baseline, 'lineno')

            total_memory = sum(stat.size_diff for stat in top_stats) / (1024 * 1024)  # Convert to MB
            passed = total_memory < 50  # SLA: <50MB

            self.log_result(
                "Instrumentation Memory Overhead (100 initializations)",
                passed,
                f"{total_memory:.2f} MB",
                "< 50 MB"
            )
        except Exception as e:
            self.log_result("Instrumentation Memory Overhead", False, str(e), "< 50 MB")

    def test_vector_validation_latency(self):
        """Test 2: Vector validation latency"""
        try:
            valid_vectors = {v: 0.5 for v in EPISTEMIC_VECTORS}

            start = time.perf_counter()
            for i in range(1000):
                from empirica.epistemic_metrics import validate_vector_dict
                validate_vector_dict(valid_vectors)
            elapsed = time.perf_counter() - start

            avg_latency_us = (elapsed / 1000) * 1_000_000
            passed = avg_latency_us < 100  # SLA: <100 microseconds per call

            self.log_result(
                "Vector Validation Latency (1000 calls)",
                passed,
                f"{avg_latency_us:.2f} µs",
                "< 100 µs"
            )
        except Exception as e:
            self.log_result("Vector Validation Latency", False, str(e), "< 100 µs")

    def test_prometheus_scrape_latency(self):
        """Test 3: Prometheus scrape endpoint latency"""
        try:
            latencies = []
            for i in range(10):
                start = time.perf_counter()
                result = subprocess.check_output(
                    ['curl', '-s', 'http://localhost:9090/api/v1/query?query=up'],
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
                elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
                latencies.append(elapsed)

            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            passed = avg_latency < 100  # SLA: <100ms average

            self.log_result(
                "Prometheus Query Latency (avg of 10)",
                passed,
                f"Avg: {avg_latency:.1f}ms, Max: {max_latency:.1f}ms",
                "Avg < 100ms"
            )
        except Exception as e:
            self.log_result("Prometheus Query Latency", False, str(e), "Avg < 100ms")

    def test_jaeger_query_latency(self):
        """Test 4: Jaeger API query latency"""
        try:
            latencies = []
            for i in range(5):
                start = time.perf_counter()
                result = subprocess.check_output(
                    ['curl', '-s', 'http://localhost:16686/api/services'],
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
                elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
                latencies.append(elapsed)

            avg_latency = sum(latencies) / len(latencies)
            passed = avg_latency < 500  # SLA: <500ms for Jaeger

            self.log_result(
                "Jaeger API Latency (avg of 5)",
                passed,
                f"{avg_latency:.1f}ms",
                "< 500ms"
            )
        except Exception as e:
            self.log_result("Jaeger API Latency", False, str(e), "< 500ms")

    def test_otel_collector_cpu_impact(self):
        """Test 5: OTEL Collector CPU usage (should be minimal at rest)"""
        try:
            # Get OTEL Collector container stats
            stats = subprocess.check_output(
                ['docker', 'stats', '--no-stream', '--format', '{{.CPUPerc}}', 'otel-collector-empirica-evaluator'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Parse CPU percentage (e.g., "1.23%")
            cpu_percent = float(stats.rstrip('%'))
            passed = cpu_percent < 5  # SLA: <5% CPU at rest

            self.log_result(
                "OTEL Collector CPU Usage (at rest)",
                passed,
                f"{cpu_percent:.2f}%",
                "< 5%"
            )
        except Exception as e:
            self.log_result("OTEL Collector CPU Usage", False, str(e), "< 5%")

    def test_prometheus_memory_usage(self):
        """Test 6: Prometheus memory usage"""
        try:
            # Get Prometheus container stats
            stats = subprocess.check_output(
                ['docker', 'stats', '--no-stream', '--format', '{{.MemUsage}}', 'prometheus-empirica-evaluator'],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Parse memory (e.g., "512MiB / 4GiB")
            mem_part = stats.split('/')[0].strip()
            mem_value = float(mem_part.split()[0])
            mem_unit = mem_part.split()[1]

            # Convert to MB
            if 'GiB' in mem_unit:
                mem_mb = mem_value * 1024
            elif 'MiB' in mem_unit:
                mem_mb = mem_value
            else:
                mem_mb = mem_value / 1024  # KiB

            # Prometheus should use <500MB for this workload
            passed = mem_mb < 500

            self.log_result(
                "Prometheus Memory Usage",
                passed,
                f"{mem_mb:.0f} MB",
                "< 500 MB"
            )
        except Exception as e:
            self.log_result("Prometheus Memory Usage", False, str(e), "< 500 MB")

    def test_graceful_degradation_path(self):
        """Test 7: Instrumentation library gracefully degrades when OTEL unavailable"""
        try:
            instr = initialize_instrumentation()

            # Library should initialize successfully even if OTEL disabled
            passed = instr is not None

            # Verify all methods are no-ops when disabled
            if instr.enabled:
                status = "OTEL enabled (packages available)"
            else:
                # Try calling methods — should not raise exceptions
                try:
                    instr.start_transaction("test", "test", "code")
                    with instr.phase_span("noetic"):
                        pass
                    instr.emit_vector_metrics({v: 0.5 for v in EPISTEMIC_VECTORS})
                    instr.close_transaction()
                    status = "OTEL disabled (graceful degradation working)"
                except Exception as e:
                    passed = False
                    status = f"Degradation failed: {e}"

            self.log_result(
                "Graceful Degradation Path",
                passed,
                status,
                "No exceptions"
            )
        except Exception as e:
            self.log_result("Graceful Degradation Path", False, str(e), "No exceptions")

    def run_all_tests(self):
        """Run all performance tests"""
        print("=" * 70)
        print("Phase 3.6.3 Performance Measurement Suite")
        print("=" * 70)
        print()

        self.test_instrumentation_memory_overhead()
        self.test_vector_validation_latency()
        self.test_prometheus_scrape_latency()
        self.test_jaeger_query_latency()
        self.test_otel_collector_cpu_impact()
        self.test_prometheus_memory_usage()
        self.test_graceful_degradation_path()

        print()
        print("=" * 70)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 70)
        print()
        print("Summary:")
        for test_name, status, value, threshold in self.results:
            print(f"  {status}: {test_name}")
            if value or threshold:
                print(f"         {value} ({threshold})")

        return self.failed == 0


if __name__ == "__main__":
    suite = PerformanceTest()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
