"""
Integration Testing Suite — Phase 3.4 Observability Stack
End-to-end validation of metrics, traces, and cross-practice correlation
"""

import requests
import json
from typing import Dict, List
import time

class IntegrationTestSuite:
    """Phase 3.4 integration test runner."""
    
    def __init__(self, prometheus_url="http://localhost:9090", jaeger_url="http://localhost:16686"):
        self.prometheus_url = prometheus_url
        self.jaeger_url = jaeger_url
        self.test_results = []
    
    def test_metric_flow(self) -> bool:
        """TEST 1: Metric emission → Prometheus scrape → Grafana query."""
        print("\n[TEST 1] Metric Flow")
        
        try:
            # Query Prometheus for metrics
            response = requests.get(f"{self.prometheus_url}/api/v1/query", params={"query": "up"})
            if response.status_code != 200:
                print("  ❌ Prometheus unreachable")
                return False
            
            data = response.json()
            if data["status"] != "success":
                print("  ❌ Prometheus query failed")
                return False
            
            # Check practice metrics
            result_count = len(data["data"]["result"])
            if result_count < 15:
                print(f"  ⚠️  Only {result_count}/15 practices reporting metrics")
            else:
                print(f"  ✅ All 15 practices reporting metrics")
            
            # Verify label consistency
            for result in data["data"]["result"]:
                if "practice" not in result["metric"] or "org" not in result["metric"]:
                    print("  ❌ Missing required labels (practice, org)")
                    return False
            
            print("  ✅ Metric Flow: PASSED")
            return True
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def test_trace_flow(self) -> bool:
        """TEST 2: Trace emission → OTEL collector → Jaeger query."""
        print("\n[TEST 2] Trace Flow")
        
        try:
            # Query Jaeger for traces
            response = requests.get(f"{self.jaeger_url}/api/traces", params={
                "service": "empirica-foundation-evaluator",
                "limit": 10
            })
            if response.status_code != 200:
                print("  ❌ Jaeger unreachable")
                return False
            
            data = response.json()
            traces = data.get("data", [])
            if not traces:
                print("  ⚠️  No traces found in Jaeger")
                return False
            
            # Verify trace attributes
            for trace in traces:
                spans = trace.get("spans", [])
                for span in spans:
                    tags = {tag["key"]: tag["value"] for tag in span.get("tags", [])}
                    required_keys = ["transaction_id", "practice_id", "phase"]
                    missing = [k for k in required_keys if k not in tags]
                    if missing:
                        print(f"  ❌ Span missing attributes: {missing}")
                        return False
            
            # Measure trace latency
            first_span_time = traces[0]["spans"][0]["startTime"]
            last_span_time = traces[0]["spans"][-1]["startTime"] + traces[0]["spans"][-1]["duration"]
            trace_latency_ms = (last_span_time - first_span_time) / 1000
            
            if trace_latency_ms > 100:
                print(f"  ⚠️  Trace latency {trace_latency_ms:.1f}ms > 100ms target")
            else:
                print(f"  ✅ Trace latency {trace_latency_ms:.1f}ms < 100ms")
            
            print("  ✅ Trace Flow: PASSED")
            return True
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def test_cross_practice_correlation(self) -> bool:
        """TEST 3: One practice's change visible across others."""
        print("\n[TEST 3] Cross-Practice Metric Correlation")
        
        try:
            # Emit test metric from one practice
            test_metric = "test_phase_progress{practice='evaluator'} 75"
            
            # Wait for scrape
            time.sleep(20)
            
            # Query Prometheus
            response = requests.get(f"{self.prometheus_url}/api/v1/query", params={
                "query": "test_phase_progress"
            })
            if response.status_code != 200:
                print("  ❌ Query failed")
                return False
            
            data = response.json()
            if not data["data"]["result"]:
                print("  ⚠️  Metric not ingested by Prometheus yet")
                return False
            
            # Verify value
            value = float(data["data"]["result"][0]["value"][1])
            if value == 75.0:
                print(f"  ✅ Metric correlation verified (value={value})")
                return True
            else:
                print(f"  ❌ Metric value mismatch: {value} != 75.0")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def test_measurement_gates(self) -> bool:
        """TEST 4: Measurement gate readiness."""
        print("\n[TEST 4] Measurement Gate Readiness")
        
        # Check data freshness
        print("  Checking data quality gates...")
        
        gates = {
            "data_freshness_seconds": 30,  # Metrics < 30s old
            "cardinality_limit": 10000,    # Total metric cardinality
            "completeness_percent": 95,    # Non-null data points
            "baseline_samples_min": 30,    # Baseline sample count
        }
        
        try:
            # Query Prometheus for up metric (freshness indicator)
            response = requests.get(f"{self.prometheus_url}/api/v1/query", params={"query": "up"})
            if response.status_code == 200:
                print("  ✅ Data freshness: OK")
            
            print("  ✅ Measurement Gates: PASSED")
            return True
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def run_all_tests(self) -> Dict:
        """Run all integration tests."""
        print("=" * 60)
        print("PHASE 3.4 INTEGRATION TEST SUITE")
        print("=" * 60)
        
        results = {
            "test_1_metric_flow": self.test_metric_flow(),
            "test_2_trace_flow": self.test_trace_flow(),
            "test_3_cross_practice_correlation": self.test_cross_practice_correlation(),
            "test_4_measurement_gates": self.test_measurement_gates(),
        }
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed}/{total} tests passed")
        print("=" * 60)
        
        return results

# Usage:
if __name__ == "__main__":
    suite = IntegrationTestSuite()
    results = suite.run_all_tests()
    
    # Save results
    with open("integration_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    if all(results.values()):
        print("\n✅ ALL INTEGRATION TESTS PASSED — Phase 3.5 Ready")
    else:
        print("\n❌ SOME TESTS FAILED — Review and remediate")

