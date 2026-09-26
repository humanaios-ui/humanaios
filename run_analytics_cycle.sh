#!/bin/bash
# Run complete analytics cycle: anomaly detection -> alert routing -> dashboard update
cd "$(dirname "$0")/analytics"
python3 anomaly_detection.py
python3 alert_manager.py
exit 0
