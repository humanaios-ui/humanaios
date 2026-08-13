# Supabase Database Monitoring Integration

This document describes the Supabase monitoring infrastructure integrated into the website practice frontend.

## Overview

The monitoring system provides automatic observability for Supabase queries with:
- **Query performance tracking** — measures query duration and detects slow queries (>1s)
- **Error reporting** — automatically sends failures to Sentry
- **Metrics collection** — in-memory buffer with queryable metrics and summaries
- **Real-time tracking** — monitors both initial queries and subscription updates

## Architecture

### Monitoring Utility
- **File:** `frontend/utils/supabase-monitoring.ts`
- **Exports:** 
  - `logSupabaseQuery(metric)` — log a single query
  - `getSupabaseMetrics(table?)` — retrieve metrics (filtered by table)
  - `getSupabaseMetricsSummary()` — get aggregated statistics
  - `clearSupabaseMetrics()` — reset buffer

### Integration Points
- **useLivingPoolData hook** (`frontend/hooks/useLivingPoolData.ts`)
  - Wraps Supabase queries with `performance.now()` timing
  - Calls `logSupabaseQuery()` after each query completes
  - Logs errors, row counts, and query duration

## Usage

### In Hooks

```typescript
import { logSupabaseQuery } from '@/utils/supabase-monitoring';

const { data, error } = await supabase
  .from('behavioral_scores')
  .select('*');

logSupabaseQuery({
  method: 'SELECT',
  table: 'behavioral_scores',
  duration: performance.now() - startTime,
  error: error?.message,
  rowsAffected: data?.length || 0,
});
```

### Accessing Metrics

```typescript
// Get all metrics
const allMetrics = getSupabaseMetrics();

// Get metrics for a specific table
const scoreMetrics = getSupabaseMetrics('behavioral_scores');

// Get summary statistics
const summary = getSupabaseMetricsSummary();
// {
//   totalQueries: 42,
//   avgDuration: 245.5,
//   errorCount: 2,
//   slowQueryCount: 3,
//   lastQuery: {...}
// }
```

## Slow Query Detection

Queries exceeding **1000ms** trigger:
1. Console warning: `[Supabase] Slow query: SELECT on behavioral_scores took 1234ms`
2. Sentry report with full context (query, duration, table)

Adjust threshold in `frontend/utils/supabase-monitoring.ts` line 32:
```typescript
if (metric.duration > 1000) {  // <-- Change threshold here
  // Warning and Sentry report
}
```

## Error Tracking

All query errors are automatically captured by Sentry with:
- **Error message** and operation type
- **Query context** (table, method, duration)
- **Timestamp** and client context

Example Sentry tags:
- `component: supabase`
- `method: SELECT | INSERT | UPDATE | DELETE | LISTEN`
- `table: behavioral_scores | learning_index`

## Dashboard Integration

### Grafana
Create a dashboard datasource pointing to your application metrics endpoint:

```yaml
SELECT
  table,
  method,
  AVG(duration) as avg_duration,
  MAX(duration) as max_duration,
  COUNT(*) as query_count,
  COUNT(CASE WHEN duration > 1000 THEN 1 END) as slow_queries
FROM supabase_metrics
GROUP BY table, method
```

### Datadog
Export metrics via custom metric collection (requires agent instrumentation layer — see Sentry integration for event stream).

### Sentry
Supabase errors and slow queries are reported to Sentry automatically:
1. Navigate to Issues → Filter by `component: supabase`
2. View by table to identify problem areas
3. Check error trends and slow query volume

## Testing

Run the monitoring integration tests:

```bash
npm run test -- frontend/hooks/__tests__/useLivingPoolData.monitoring.spec.ts
```

Test coverage includes:
- Successful query metric logging
- Slow query detection and warnings
- Error reporting to Sentry
- Metrics summary export
- Real-time subscription tracking
- Cleanup on component unmount

## Production Deployment

Before deploying to production:

1. **Verify Sentry DSN** is configured in environment
   ```bash
   echo $SENTRY_DSN  # Must be set
   ```

2. **Test slow query detection**
   - Deliberately run a slow query
   - Verify Sentry receives the warning

3. **Monitor initial load**
   - Check Sentry dashboard for errors
   - Verify metrics are collecting
   - Adjust slow query threshold if needed

4. **Set up alerts** (Sentry → Alerts tab)
   - Alert on `issue-frequency: high` for Supabase errors
   - Alert on `error-volume: >5 in 1m` for slow queries

## Troubleshooting

### Metrics not collecting
- Check that `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are set
- Verify `useLivingPoolData` hook is mounted (component must be rendered)
- Check browser console for errors

### Sentry not receiving errors
- Verify `SENTRY_DSN` is set and valid
- Check Sentry project settings → Client Keys
- Confirm Sentry client initialization in your app layout

### Slow query threshold too sensitive
- Edit threshold in `supabase-monitoring.ts` (currently 1000ms)
- Document threshold change in this file
- Test with synthetic slow query before adjusting production threshold

## Future Enhancements

- [ ] Custom metric dimensions (user ID, region, etc.)
- [ ] Query parameter logging (with PII masking)
- [ ] Real-time metrics export (WebSocket to dashboard)
- [ ] Predictive slow query alerting
- [ ] Automatic performance recommendations
