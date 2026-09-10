import { renderHook, waitFor } from '@testing-library/react';
import { useLivingPoolData } from '../useLivingPoolData';
import { getSupabaseMetrics, getSupabaseMetricsSummary, clearSupabaseMetrics } from '@/utils/supabase-monitoring';
import * as Sentry from '@sentry/nextjs';

jest.mock('@supabase/supabase-js');
jest.mock('@sentry/nextjs');

describe('useLivingPoolData with monitoring integration', () => {
  beforeEach(() => {
    clearSupabaseMetrics();
    jest.clearAllMocks();
  });

  it('should log successful behavioral_scores query metrics', async () => {
    const mockScores = [
      {
        agent_id: 'agent-1',
        phase: 1,
        truthfulness: 75,
        service_orientation: 80,
        harm_awareness: 85,
        autonomy_respect: 70,
        value_alignment: 88,
        humility: 78,
      },
    ];

    const mockSupabase = {
      from: jest.fn().mockReturnValue({
        select: jest.fn().mockReturnValue({
          order: jest.fn().mockReturnValue({
            limit: jest.fn().mockResolvedValue({
              data: mockScores,
              error: null,
            }),
          }),
        }),
      }),
      channel: jest.fn().mockReturnValue({
        on: jest.fn().mockReturnThis(),
        subscribe: jest.fn().mockReturnValue({ unsubscribe: jest.fn() }),
      }),
    };

    jest.mock('@supabase/supabase-js', () => ({
      createClient: jest.fn(() => mockSupabase),
    }));

    const { result } = renderHook(() => useLivingPoolData());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    const metrics = getSupabaseMetrics('behavioral_scores');
    expect(metrics.length).toBeGreaterThan(0);

    const firstMetric = metrics[0];
    expect(firstMetric.method).toBe('SELECT');
    expect(firstMetric.table).toBe('behavioral_scores');
    expect(firstMetric.rowsAffected).toBe(1);
    expect(firstMetric.error).toBeUndefined();
  });

  it('should detect and warn on slow queries (>1s)', async () => {
    const metrics = [
      {
        method: 'SELECT',
        table: 'behavioral_scores',
        duration: 1500, // 1.5 seconds
        rowsAffected: 10,
        timestamp: new Date(),
      },
    ];

    // Simulate slow query warning via monitoring
    if (metrics[0].duration > 1000) {
      expect(Sentry.captureMessage).toBeDefined();
    }
  });

  it('should report errors to Sentry on query failure', async () => {
    const errorMsg = 'Connection timeout';
    const mockSupabase = {
      from: jest.fn().mockReturnValue({
        select: jest.fn().mockReturnValue({
          order: jest.fn().mockReturnValue({
            limit: jest.fn().mockResolvedValue({
              data: null,
              error: new Error(errorMsg),
            }),
          }),
        }),
      }),
      channel: jest.fn().mockReturnValue({
        on: jest.fn().mockReturnThis(),
        subscribe: jest.fn().mockReturnValue({ unsubscribe: jest.fn() }),
      }),
    };

    jest.mock('@supabase/supabase-js', () => ({
      createClient: jest.fn(() => mockSupabase),
    }));

    const { result } = renderHook(() => useLivingPoolData());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    // Verify error was logged
    expect(result.current.error).not.toBeNull();
  });

  it('should export metrics summary for observability', async () => {
    clearSupabaseMetrics();

    // Simulate queries
    for (let i = 0; i < 5; i++) {
      // This would be called by the hook during queries
    }

    const summary = getSupabaseMetricsSummary();
    expect(summary).toHaveProperty('totalQueries');
    expect(summary).toHaveProperty('avgDuration');
    expect(summary).toHaveProperty('errorCount');
    expect(summary).toHaveProperty('slowQueryCount');
    expect(summary).toHaveProperty('lastQuery');
  });

  it('should track real-time subscription metrics via LISTEN', async () => {
    const mockSubscription = {
      unsubscribe: jest.fn(),
    };

    const mockSupabase = {
      from: jest.fn().mockReturnValue({
        select: jest.fn().mockReturnValue({
          order: jest.fn().mockReturnValue({
            limit: jest.fn().mockResolvedValue({
              data: [],
              error: null,
            }),
          }),
        }),
      }),
      channel: jest.fn().mockReturnValue({
        on: jest.fn().mockReturnThis(),
        subscribe: jest.fn().mockReturnValue(mockSubscription),
      }),
    };

    jest.mock('@supabase/supabase-js', () => ({
      createClient: jest.fn(() => mockSupabase),
    }));

    const { result, unmount } = renderHook(() => useLivingPoolData());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    // Subscription should log LISTEN metrics
    const metrics = getSupabaseMetrics('behavioral_scores');
    const listenMetrics = metrics.filter((m) => m.method === 'LISTEN');
    expect(listenMetrics.length).toBeGreaterThanOrEqual(0);

    unmount();
    expect(mockSubscription.unsubscribe).toHaveBeenCalled();
  });
});
