#!/usr/bin/env python3
"""
Grafana Dashboard Builder for Phase 3.5.3

Generates dashboard JSON for all 6 Phase 3.5.3 dashboards:
1. Empirica Phase Latency
2. Multi-Practice Traces
3. Log Completeness
4. Vector Calibration (ACAT)
5. Practice Deep-Dive (Autonomy)
6. Cross-Practice Integration

Usage:
    python3 grafana-dashboard-builder.py
    # Generates dashboard-*.json files

    # Or deploy directly to Grafana:
    ./deploy-dashboards.sh
"""

import json
from typing import Dict, List, Any
from datetime import datetime

# ============================================================================
# Dashboard Base Template
# ============================================================================

def create_base_dashboard(title: str, description: str = "") -> Dict[str, Any]:
    """Create base dashboard template"""
    return {
        "dashboard": {
            "title": title,
            "description": description,
            "tags": ["phase-3.5", "observability"],
            "timezone": "browser",
            "panels": [],
            "refresh": "30s",
            "time": {
                "from": "now-7d",
                "to": "now"
            },
            "timepicker": {
                "refresh_intervals": ["30s", "1m", "5m", "15m", "30m", "1h"]
            }
        }
    }


# ============================================================================
# Panel Builders
# ============================================================================

def create_timeseries_panel(
    title: str,
    query: str,
    datasource: str = "Loki",
    x: int = 0,
    y: int = 0,
    w: int = 12,
    h: int = 8
) -> Dict[str, Any]:
    """Create timeseries (line chart) panel"""
    return {
        "title": title,
        "type": "timeseries",
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "targets": [
            {
                "refId": "A",
                "datasource": datasource,
                "expr": query
            }
        ],
        "options": {
            "legend": {"calcs": ["mean", "max"], "displayMode": "table"},
            "tooltip": {"mode": "multi"},
            "thresholds": {
                "mode": "percentage",
                "steps": [
                    {"color": "green", "value": 0},
                    {"color": "yellow", "value": 50},
                    {"color": "red", "value": 80}
                ]
            }
        }
    }


def create_stat_panel(
    title: str,
    query: str,
    datasource: str = "Loki",
    unit: str = "short",
    x: int = 0,
    y: int = 0,
    w: int = 6,
    h: int = 4
) -> Dict[str, Any]:
    """Create stat panel (gauge)"""
    return {
        "title": title,
        "type": "stat",
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "targets": [
            {
                "refId": "A",
                "datasource": datasource,
                "expr": query
            }
        ],
        "options": {
            "graphMode": "area",
            "orientation": "auto",
            "textMode": "auto",
            "colorMode": "value",
            "decimals": 2,
            "thresholds": {
                "mode": "absolute",
                "steps": [
                    {"color": "red", "value": 0},
                    {"color": "yellow", "value": 0.05},
                    {"color": "green", "value": 0.1}
                ]
            }
        },
        "fieldConfig": {
            "defaults": {
                "unit": unit,
                "custom": {}
            }
        }
    }


def create_heatmap_panel(
    title: str,
    query: str,
    datasource: str = "Loki",
    x: int = 0,
    y: int = 0,
    w: int = 12,
    h: int = 8
) -> Dict[str, Any]:
    """Create heatmap panel"""
    return {
        "title": title,
        "type": "heatmap",
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "targets": [
            {
                "refId": "A",
                "datasource": datasource,
                "expr": query
            }
        ],
        "options": {
            "calculate": False,
            "cellGap": 2,
            "cellRadius": 2,
            "color": {
                "scheme": "Spectral"
            },
            "exemplars": {
                "color": "rgba(255,0,255,0.7)"
            },
            "filterValues": {
                "le": 1e-9
            },
            "legend": {
                "show": True
            },
            "tooltip": {
                "enabled": True
            }
        }
    }


def create_table_panel(
    title: str,
    query: str,
    datasource: str = "Loki",
    x: int = 0,
    y: int = 0,
    w: int = 12,
    h: int = 8
) -> Dict[str, Any]:
    """Create table panel"""
    return {
        "title": title,
        "type": "table",
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "targets": [
            {
                "refId": "A",
                "datasource": datasource,
                "expr": query
            }
        ],
        "options": {
            "showHeader": True,
            "sortBy": []
        },
        "transformations": []
    }


def create_piechart_panel(
    title: str,
    query: str,
    datasource: str = "Loki",
    x: int = 0,
    y: int = 0,
    w: int = 6,
    h: int = 6
) -> Dict[str, Any]:
    """Create pie chart panel"""
    return {
        "title": title,
        "type": "piechart",
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "targets": [
            {
                "refId": "A",
                "datasource": datasource,
                "expr": query
            }
        ],
        "options": {
            "legend": {
                "displayMode": "table",
                "placement": "right"
            },
            "pieType": "pie",
            "tooltip": {"mode": "single"}
        }
    }


# ============================================================================
# Dashboard Builders
# ============================================================================

def build_dashboard_1_phase_latency() -> Dict[str, Any]:
    """Dashboard 1: Empirica Phase Latency"""
    dashboard = create_base_dashboard(
        title="Empirica Phase Latency",
        description="Transaction phase duration trends (PREFLIGHT → CHECK → POSTFLIGHT)"
    )

    panels = dashboard["dashboard"]["panels"]

    # Panel 1a: Phase Duration Trend
    panels.append(create_timeseries_panel(
        title="Phase Duration Trend (ms)",
        query='{job="empirica-sessions"} | json | phase != "" | duration_ms > 0',
        x=0, y=0, w=12, h=8
    ))

    # Panel 1b: P95 Latency per Phase (stacked stats)
    panels.append(create_stat_panel(
        title="PREFLIGHT P95",
        query='{job="empirica-sessions", phase="PREFLIGHT"} | json | duration_ms > 0 | quantile_over_time(0.95, duration_ms[5m])',
        unit="ms",
        x=0, y=8, w=3, h=4
    ))

    panels.append(create_stat_panel(
        title="CHECK P95",
        query='{job="empirica-sessions", phase="CHECK"} | json | duration_ms > 0 | quantile_over_time(0.95, duration_ms[5m])',
        unit="ms",
        x=3, y=8, w=3, h=4
    ))

    panels.append(create_stat_panel(
        title="POSTFLIGHT P95",
        query='{job="empirica-sessions", phase="POSTFLIGHT"} | json | duration_ms > 0 | quantile_over_time(0.95, duration_ms[5m])',
        unit="ms",
        x=6, y=8, w=3, h=4
    ))

    panels.append(create_stat_panel(
        title="SLA Compliance",
        query='{job="empirica-sessions"} | json | duration_ms < 300 | count / ({job="empirica-sessions"} | count)',
        unit="percentunit",
        x=9, y=8, w=3, h=4
    ))

    # Panel 1c: Phase Duration by Practice (heatmap)
    panels.append(create_heatmap_panel(
        title="Duration by Practice & Phase (ms)",
        query='{job="empirica-sessions"} | json | practice != "" | phase != "" | duration_ms > 0',
        x=0, y=12, w=12, h=8
    ))

    return dashboard


def build_dashboard_2_multi_practice_traces() -> Dict[str, Any]:
    """Dashboard 2: Multi-Practice Traces"""
    dashboard = create_base_dashboard(
        title="Multi-Practice Traces",
        description="Request flow across practice boundaries"
    )

    panels = dashboard["dashboard"]["panels"]

    # Panel 2a: Request Flow (timeseries)
    panels.append(create_timeseries_panel(
        title="Request Count by Source→Target",
        query='{job="empirica-sessions"} | json | source_practice != "" | target_practice != "" | count by source_practice, target_practice',
        x=0, y=0, w=12, h=8
    ))

    # Panel 2b: Request Type Distribution (pie)
    panels.append(create_piechart_panel(
        title="Request Type Distribution",
        query='{job="empirica-sessions"} | json | request_type != "" | count by request_type',
        x=0, y=8, w=6, h=6
    ))

    # Panel 2c: Trace Latency Percentiles (timeseries)
    panels.append(create_timeseries_panel(
        title="Trace Latency Percentiles (ms)",
        query='{job="empirica-sessions"} | json | duration_ms > 0 | quantile_over_time(0.5, duration_ms[5m]) as p50, quantile_over_time(0.95, duration_ms[5m]) as p95, quantile_over_time(0.99, duration_ms[5m]) as p99',
        x=6, y=8, w=6, h=6
    ))

    # Panel 2d: Error Traces (table)
    panels.append(create_table_panel(
        title="Error Traces (last 50)",
        query='{job="empirica-sessions"} | json | result="error" | timestamp, source_practice, target_practice, error_type',
        datasource="Loki",
        x=0, y=14, w=12, h=8
    ))

    return dashboard


def build_dashboard_3_log_completeness() -> Dict[str, Any]:
    """Dashboard 3: Log Completeness"""
    dashboard = create_base_dashboard(
        title="Log Completeness",
        description="Log ingestion health and coverage"
    )

    panels = dashboard["dashboard"]["panels"]

    # Panel 3a: Log Count by Phase (stacked area)
    panels.append(create_timeseries_panel(
        title="Log Count by Phase",
        query='{job="empirica-sessions"} | json | phase != "" | count by phase',
        x=0, y=0, w=12, h=8
    ))

    # Panel 3b: Completeness by Practice (heatmap)
    panels.append(create_heatmap_panel(
        title="Log Completeness by Practice & Phase",
        query='{job="empirica-sessions"} | json | practice != "" | phase != "" | count by practice, phase',
        x=0, y=8, w=12, h=8
    ))

    # Panel 3c: Query Latency (timeseries)
    panels.append(create_timeseries_panel(
        title="Loki Query Latency (ms)",
        query='rate(loki_request_duration_seconds_bucket{handler="query"}[5m])',
        datasource="Loki",
        x=0, y=16, w=6, h=6
    ))

    # Panel 3d: Practice-Stdout Log Count (stats)
    panels.append(create_stat_panel(
        title="practice-stdout Logs (Total)",
        query='{job="practice-stdout"} | count',
        datasource="Loki",
        unit="short",
        x=6, y=16, w=6, h=6
    ))

    return dashboard


def build_dashboard_4_vector_calibration() -> Dict[str, Any]:
    """Dashboard 4: Vector Calibration (ACAT)"""
    dashboard = create_base_dashboard(
        title="Vector Calibration (ACAT)",
        description="Epistemic vector calibration metrics (predicted vs actual)"
    )

    panels = dashboard["dashboard"]["panels"]

    # Panel 4a: Brier Score by Vector (multi-stat)
    vectors = ["know", "do", "context", "clarity", "coherence", "signal", "density", "state", "change", "completion", "impact", "engagement", "uncertainty"]
    x, y = 0, 0
    for i, vec in enumerate(vectors):
        panels.append(create_stat_panel(
            title=f"{vec} Brier Error",
            query=f'{{job="acat-grounding"}} | json | vector_name="{vec}" | avg(brier_error)',
            datasource="Loki",
            unit="short",
            x=x, y=y, w=2, h=4
        ))
        x += 2
        if x >= 12:
            x = 0
            y += 4

    # Panel 4b: Calibration Error Trend (timeseries)
    panels.append(create_timeseries_panel(
        title="Brier Error Trend by Vector",
        query='{job="acat-grounding"} | json | vector_name != "" | avg(brier_error) by vector_name',
        datasource="Loki",
        x=0, y=y+4, w=12, h=8
    ))

    # Panel 4c: Per-Practice Calibration (table)
    panels.append(create_table_panel(
        title="Calibration by Practice",
        query='{job="acat-grounding"} | json | ai_id != "" | avg(brier_error) by ai_id',
        datasource="Loki",
        x=0, y=y+12, w=12, h=8
    ))

    return dashboard


def build_dashboard_5_practice_deep_dive() -> Dict[str, Any]:
    """Dashboard 5: Practice Deep-Dive (Autonomy)"""
    dashboard = create_base_dashboard(
        title="Practice Deep-Dive: Autonomy",
        description="Single-practice operational view (autonomy)"
    )

    panels = dashboard["dashboard"]["panels"]

    # Panel 5a: Session Timeline (timeseries)
    panels.append(create_timeseries_panel(
        title="Session Timeline (Autonomy)",
        query='{practice="autonomy"} | json | session_id, phase, duration_ms | count by phase',
        x=0, y=0, w=12, h=8
    ))

    # Panel 5b: Trace Count (stat)
    panels.append(create_stat_panel(
        title="Total Traces (Autonomy)",
        query='{practice="autonomy"} | count',
        datasource="Loki",
        unit="short",
        x=0, y=8, w=3, h=4
    ))

    # Panel 5c: Error Count (stat)
    panels.append(create_stat_panel(
        title="Error Traces (Autonomy)",
        query='{practice="autonomy"} | json | result="error" | count',
        datasource="Loki",
        unit="short",
        x=3, y=8, w=3, h=4
    ))

    # Panel 5d: Avg Latency (stat)
    panels.append(create_stat_panel(
        title="Avg Latency (Autonomy)",
        query='{practice="autonomy"} | json | duration_ms > 0 | avg(duration_ms)',
        datasource="Loki",
        unit="ms",
        x=6, y=8, w=3, h=4
    ))

    # Panel 5e: Vector Heatmap (Autonomy)
    panels.append(create_heatmap_panel(
        title="Vector Values (Autonomy)",
        query='{practice="autonomy"} | json | vector_name != "" | value by vector_name',
        x=9, y=8, w=3, h=4
    ))

    # Panel 5f: Error Logs (table)
    panels.append(create_table_panel(
        title="Error Logs (Autonomy)",
        query='{practice="autonomy", level="error"} | json | timestamp, message',
        datasource="Loki",
        x=0, y=12, w=12, h=8
    ))

    return dashboard


def build_dashboard_6_cross_practice_integration() -> Dict[str, Any]:
    """Dashboard 6: Cross-Practice Integration"""
    dashboard = create_base_dashboard(
        title="Cross-Practice Integration",
        description="Mesh-wide coordination and bottleneck detection"
    )

    panels = dashboard["dashboard"]["panels"]

    # Panel 6a: Practice Health Matrix (heatmap)
    panels.append(create_heatmap_panel(
        title="Practice Health Score",
        query='{job="empirica-sessions"} | json | practice != "" | avg(vector_values) by practice',
        x=0, y=0, w=12, h=8
    ))

    # Panel 6b: Mesh Request Volume (stats)
    practices = ["autonomy", "mesh-support", "outreach", "website", "humanaios"]
    x, y = 0, 8
    for i, practice in enumerate(practices):
        panels.append(create_stat_panel(
            title=f"{practice} Requests",
            query=f'{{practice="{practice}"}} | count',
            datasource="Loki",
            unit="short",
            x=x, y=y, w=2.4, h=4
        ))
        x += 2.4
        if x >= 12:
            x = 0
            y += 4

    # Panel 6c: Mesh Latency Percentiles (stats)
    y_next = y + 4
    panels.append(create_stat_panel(
        title="Mesh P50 Latency",
        query='{job="empirica-sessions"} | json | duration_ms > 0 | quantile_over_time(0.5, duration_ms[5m])',
        datasource="Loki",
        unit="ms",
        x=0, y=y_next, w=3, h=4
    ))

    panels.append(create_stat_panel(
        title="Mesh P95 Latency",
        query='{job="empirica-sessions"} | json | duration_ms > 0 | quantile_over_time(0.95, duration_ms[5m])',
        datasource="Loki",
        unit="ms",
        x=3, y=y_next, w=3, h=4
    ))

    panels.append(create_stat_panel(
        title="Mesh P99 Latency",
        query='{job="empirica-sessions"} | json | duration_ms > 0 | quantile_over_time(0.99, duration_ms[5m])',
        datasource="Loki",
        unit="ms",
        x=6, y=y_next, w=3, h=4
    ))

    panels.append(create_stat_panel(
        title="Error Rate",
        query='{job="empirica-sessions"} | json | result="error" | count / ({job="empirica-sessions"} | count)',
        datasource="Loki",
        unit="percentunit",
        x=9, y=y_next, w=3, h=4
    ))

    # Panel 6d: Request Flow Matrix (table)
    panels.append(create_table_panel(
        title="Cross-Practice Request Matrix",
        query='{job="empirica-sessions"} | json | source_practice != "" | target_practice != "" | count by source_practice, target_practice, avg(duration_ms)',
        datasource="Loki",
        x=0, y=y_next+4, w=12, h=8
    ))

    return dashboard


# ============================================================================
# Main
# ============================================================================

def main():
    """Build and export all 6 dashboards"""
    dashboards = [
        ("dashboard-1-phase-latency", build_dashboard_1_phase_latency()),
        ("dashboard-2-multi-practice-traces", build_dashboard_2_multi_practice_traces()),
        ("dashboard-3-log-completeness", build_dashboard_3_log_completeness()),
        ("dashboard-4-vector-calibration", build_dashboard_4_vector_calibration()),
        ("dashboard-5-practice-autonomy", build_dashboard_5_practice_deep_dive()),
        ("dashboard-6-cross-practice", build_dashboard_6_cross_practice_integration()),
    ]

    print("🚀 Building Grafana Dashboards")
    print("=" * 60)
    print()

    for name, dashboard in dashboards:
        filename = f"{name}.json"
        with open(filename, "w") as f:
            json.dump(dashboard, f, indent=2)
        print(f"✓ {name:<40} → {filename}")

    print()
    print("=" * 60)
    print("✅ All 6 dashboards created")
    print()
    print("To deploy to Grafana:")
    print("  ./deploy-dashboards.sh")
    print()


if __name__ == "__main__":
    main()
