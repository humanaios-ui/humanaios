# Artillery JSON Output — Quick Reference

How to interpret Artillery's JSON results and extract key metrics.

## Running Artillery

```bash
# Run test and save JSON output
artillery run assessment-submission.yml --output results/test-output.json

# Review summary in console
# Detailed metrics in results/test-output.json
```

## Artillery JSON Structure

```json
{
  "summary": {
    "rps": 0.12,                    // Requests per second
    "scenariosCreated": 1,          // Number of scenarios started
    "scenariosCompleted": 1,        // Successfully completed
    "requestsCompleted": 14,        // Total requests
    "latency": {
      "min": 45,
      "max": 4850,
      "mean": 1250,
      "median": 980,
      "p95": 3200,
      "p99": 4100
    },
    "codes": {
      "201": 1,                     // POST /assessments responses
      "200": 11,                    // GET responses
      "429": 0,                     // Rate limit errors
      "503": 0,                     // Service unavailable
      "504": 0                      // Gateway timeout
    },
    "errors": 0,                    // Total error count
    "customStats": {}
  },
  "aggregate": {
    "/api/v1/assessments": {
      "POST": {
        "codes": { "201": 1 },
        "latency": { "mean": 85, "p99": 120 },
        "rps": 0.5
      },
      "GET": {
        "codes": { "200": 10 },
        "latency": { "mean": 52, "p99": 95 },
        "rps": 5.0
      }
    },
    "/api/v1/assessments/:id/result": {
      "GET": {
        "codes": { "200": 1 },
        "latency": { "mean": 340, "p99": 450 },
        "rps": 0.5
      }
    }
  }
}
```

## Key Metrics to Extract

### Latency Metrics
```bash
# From JSON:
jq '.summary.latency' results/test-output.json

# Expected output:
{
  "min": 45,
  "max": 4850,
  "mean": 1250,
  "median": 980,
  "p95": 3200,
  "p99": 4100
}
```

### HTTP Response Codes
```bash
jq '.summary.codes' results/test-output.json

# Count errors by type:
jq '.summary.codes | to_entries | map("\(.key): \(.value)")' results/test-output.json
```

### Requests Per Second (Throughput)
```bash
jq '.summary.rps' results/test-output.json
# Result: 0.12 (baseline with 1 user)
```

### Error Rate
```bash
# Total errors
jq '.summary.errors' results/test-output.json

# Error rate percentage (manual calculation):
# Error Rate = (errors / requestsCompleted) * 100
```

### Per-Endpoint Breakdown
```bash
jq '.aggregate | keys' results/test-output.json
# Shows which endpoints were tested

# Latency per endpoint:
jq '.aggregate[] | with_entries(.value |= .latency)' results/test-output.json
```

## One-Liner Extraction Commands

Extract to CSV format for easy comparison:

```bash
# Extract summary line
jq -r '.summary | "\(.rps),\(.latency.mean),\(.latency.p95),\(.latency.p99),\(.errors)"' results/test-output.json
# Output: 0.12,1250,3200,4100,0

# Extract all endpoints with metrics
jq -r '.aggregate | to_entries | .[] | "\(.key), \(.value | keys[])"' results/test-output.json
```

## Comparing Multiple Test Runs

Create a comparison table:

```bash
#!/bin/bash
echo "Concurrency,RPS,Avg Latency,P99,Errors,Error Rate"

for f in results/*.json; do
  concurrency=$(basename $f | grep -oP '(?<=-)[0-9]+(?=_)' | head -1)
  rps=$(jq '.summary.rps' "$f")
  avg=$(jq '.summary.latency.mean' "$f")
  p99=$(jq '.summary.latency.p99' "$f")
  errors=$(jq '.summary.errors' "$f")
  total=$(jq '.summary.requestsCompleted' "$f")
  rate=$(echo "scale=2; ($errors / $total) * 100" | bc)
  
  echo "$concurrency,$rps,$avg,$p99,$errors,$rate%"
done
```

## Common Analysis Patterns

### 1. Identify Bottleneck Endpoint

```bash
# Compare latencies by endpoint
jq '.aggregate | to_entries | map({
  endpoint: .key,
  methods: .value | keys,
  avg_latency: (.value[] | .latency.mean) | max
})' results/test-output.json | jq 'sort_by(.avg_latency) | reverse'
```

### 2. Error Rate by HTTP Status

```bash
# Break down errors by type
jq -r '.summary.codes | to_entries | 
  map(select(.value > 0)) | 
  map("\(.key): \(.value) errors")' results/test-output.json
```

### 3. Latency Distribution

```bash
# Show percentile distribution
jq '.summary.latency | to_entries | 
  map("\(.key): \(.value)ms")' results/test-output.json
```

## Integration with Spreadsheet

Save results to CSV for analysis in Excel/Sheets:

```bash
#!/bin/bash
{
  echo "Test,Concurrency,RPS,Avg Latency (ms),P50 (ms),P95 (ms),P99 (ms),Errors,Error Rate (%)"
  
  for f in results/*.json; do
    name=$(basename $f .json)
    concurrency=$(echo "$name" | grep -oP '(?<=-)[0-9]+(?=_)' | head -1 || echo "1")
    
    jq -r --arg name "$name" --arg conc "$concurrency" '
      .summary | 
      "\($name),\($conc),\(.rps),\(.latency.mean),\(.latency.median),\(.latency.p95),\(.latency.p99),\(.errors),\((.errors/.summary.requestsCompleted * 100))"' "$f"
  done
} > results/summary.csv

echo "Results saved to results/summary.csv"
```

## Interpreting Latency Percentiles

| Percentile | Meaning | Example |
|-----------|---------|---------|
| **Min** | Fastest response | 45 ms (almost instant) |
| **P50 (Median)** | Half of users experience this or faster | 980 ms (typical experience) |
| **P95** | 95% of users experience this or faster | 3,200 ms (unlucky users) |
| **P99** | 99% of users experience this or faster | 4,100 ms (very unlucky users) |
| **Max** | Slowest response (outlier) | 4,850 ms (spike) |
| **Mean (Avg)** | Average across all requests | 1,250 ms (overall trend) |

**Production targets:**
- Mean < 2s (user expectation: "fast")
- P95 < 10s (most users happy)
- P99 < 30s (tail latency acceptable)

## Troubleshooting Artillery Output

### Issue: All 503 or 504 errors
```json
"codes": { "503": 145, "504": 45 }
```
**Cause:** API or database overload
**Check:** CPU %, connection pool size, DB slow queries

### Issue: High error rate but low latency
```bash
jq '.summary | "\(.errors) errors but mean latency \(.latency.mean)ms"'
```
**Cause:** Rate limiting or quota exceeded
**Check:** API rate limit settings, concurrent user target

### Issue: Latency increases but throughput flat
```bash
# Mean latency up, but rps same
```
**Cause:** Connection pooling, queueing, or queue depth growing
**Check:** DB connections, request queue depth, memory

## Next Steps

1. Run test: `./run-all-tests.sh`
2. Extract metrics: Use commands above
3. Fill RESULTS_ANALYSIS_TEMPLATE.md for each test
4. Compare across concurrency levels
5. Identify bottleneck (connection pool / CPU / memory)
6. Proceed to Task 7.5 optimization
