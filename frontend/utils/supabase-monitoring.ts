'use client';

import * as Sentry from '@sentry/nextjs';

export interface SupabaseQueryMetrics {
  method: string;
  table: string;
  duration: number;
  error?: string;
  rowsAffected?: number;
  timestamp: Date;
}

const metrics: SupabaseQueryMetrics[] = [];
const MAX_METRICS = 1000;

export function logSupabaseQuery(metric: Omit<SupabaseQueryMetrics, 'timestamp'>) {
  const fullMetric = { ...metric, timestamp: new Date() };
  metrics.push(fullMetric);

  if (metrics.length > MAX_METRICS) {
    metrics.shift();
  }

  // Log errors to Sentry
  if (metric.error) {
    Sentry.captureException(new Error(`Supabase ${metric.method} on ${metric.table}: ${metric.error}`), {
      tags: {
        component: 'supabase',
        method: metric.method,
        table: metric.table,
      },
      contexts: {
        supabase: {
          method: metric.method,
          table: metric.table,
          duration: metric.duration,
          rowsAffected: metric.rowsAffected,
        },
      },
    });
  }

  // Warn on slow queries (>1s)
  if (metric.duration > 1000) {
    console.warn(`[Supabase] Slow query: ${metric.method} on ${metric.table} took ${metric.duration}ms`);
    Sentry.captureMessage(`Slow Supabase query: ${metric.method} ${metric.table}`, {
      level: 'warning',
      tags: {
        component: 'supabase',
        type: 'slow_query',
      },
      contexts: {
        supabase: {
          method: metric.method,
          table: metric.table,
          duration: metric.duration,
        },
      },
    });
  }
}

export function getSupabaseMetrics(table?: string): SupabaseQueryMetrics[] {
  if (table) {
    return metrics
      .filter((m) => m.table === table)
      .map((m) => ({ ...m, timestamp: new Date(m.timestamp) }));
  }
  return metrics.map((m) => ({ ...m, timestamp: new Date(m.timestamp) }));
}

export function getSupabaseMetricsSummary() {
  const summary = {
    totalQueries: metrics.length,
    avgDuration: metrics.length > 0 ? metrics.reduce((sum, m) => sum + m.duration, 0) / metrics.length : 0,
    errorCount: metrics.filter((m) => m.error).length,
    slowQueryCount: metrics.filter((m) => m.duration > 1000).length,
    lastQuery: metrics[metrics.length - 1] || null,
  };
  return summary;
}

export function clearSupabaseMetrics() {
  metrics.length = 0;
}
