'use client';

import { useEffect, useState, useCallback } from 'react';
import { createClient } from '@supabase/supabase-js';
import { logSupabaseQuery } from '@/utils/supabase-monitoring';
import { SigilData, BehavioralDimensions } from '@/components/LivingPool/SigilGeometry';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export function useLivingPoolData() {
  const [sigils, setSigils] = useState<Map<string, SigilData>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize Supabase
  const supabase = supabaseUrl && supabaseKey
    ? createClient(supabaseUrl, supabaseKey)
    : null;

  const fetchInitialData = useCallback(async () => {
    if (!supabase) {
      setIsLoading(false);
      return;
    }

    try {
      // Fetch behavioral scores (latest for each agent)
      const startScores = performance.now();
      const { data: scores, error: scoresError } = await supabase
        .from('behavioral_scores')
        .select('agent_id, phase, truthfulness, service_orientation, harm_awareness, autonomy_respect, value_alignment, humility')
        .order('measured_at', { ascending: false })
        .limit(1000);

      const scoresDuration = performance.now() - startScores;
      logSupabaseQuery({
        method: 'SELECT',
        table: 'behavioral_scores',
        duration: scoresDuration,
        error: scoresError?.message,
        rowsAffected: scores?.length || 0,
      });

      if (scoresError) {
        setError(scoresError.message);
        setIsLoading(false);
        return;
      }

      // Fetch learning indices
      const startLI = performance.now();
      const { data: li, error: liError } = await supabase
        .from('learning_index')
        .select('agent_id, li_value')
        .order('calculated_at', { ascending: false })
        .limit(500);

      const liDuration = performance.now() - startLI;
      logSupabaseQuery({
        method: 'SELECT',
        table: 'learning_index',
        duration: liDuration,
        error: liError?.message,
        rowsAffected: li?.length || 0,
      });

      if (liError) {
        setError(liError.message);
        setIsLoading(false);
        return;
      }

      // Process data into sigils
      const sigilMap = new Map<string, SigilData>();
      const agentScores = new Map<string, any[]>();

      // Group scores by agent
      scores?.forEach((score) => {
        if (!agentScores.has(score.agent_id)) {
          agentScores.set(score.agent_id, []);
        }
        agentScores.get(score.agent_id)!.push(score);
      });

      // Build sigils
      agentScores.forEach((scores, agentId) => {
        const phase1 = scores.find((s) => s.phase === 1);
        const phase3 = scores.find((s) => s.phase === 3) || phase1;

        if (phase1) {
          const learning = li?.find((l) => l.agent_id === agentId);

          const sigil: SigilData = {
            id: agentId,
            phase1: {
              truthfulness: phase1.truthfulness || 50,
              serviceOrientation: phase1.service_orientation || 50,
              harmAwareness: phase1.harm_awareness || 50,
              autonomyRespect: phase1.autonomy_respect || 50,
              valueAlignment: phase1.value_alignment || 50,
              humility: phase1.humility || 50,
            },
            phase3: {
              truthfulness: phase3.truthfulness || 50,
              serviceOrientation: phase3.service_orientation || 50,
              harmAwareness: phase3.harm_awareness || 50,
              autonomyRespect: phase3.autonomy_respect || 50,
              valueAlignment: phase3.value_alignment || 50,
              humility: phase3.humility || 50,
            },
            learningIndex: learning?.li_value || 0.85,
            position: {
              x: (Math.random() - 0.5) * 20,
              y: (Math.random() - 0.5) * 20,
              z: Math.random() * 15 - 5,
            },
          };

          sigilMap.set(agentId, sigil);
        }
      });

      setSigils(sigilMap);
      setIsLoading(false);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMsg);
      logSupabaseQuery({
        method: 'SELECT',
        table: 'behavioral_scores|learning_index',
        duration: 0,
        error: errorMsg,
      });
      setIsLoading(false);
    }
  }, [supabase]);

  useEffect(() => {
    fetchInitialData();

    if (!supabase) return;

    // Subscribe to behavioral_scores changes
    const subscription = supabase
      .channel('behavioral_scores_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'behavioral_scores' },
        (payload) => {
          logSupabaseQuery({
            method: 'LISTEN',
            table: 'behavioral_scores',
            duration: 0,
            rowsAffected: 1,
          });

          // Update sigil with new data
          const { new: newRecord } = payload;
          if (newRecord) {
            setSigils((prev) => {
              const updated = new Map(prev);
              const existing = updated.get(newRecord.agent_id) || {
                id: newRecord.agent_id,
                phase1: {} as BehavioralDimensions,
                phase3: {} as BehavioralDimensions,
                learningIndex: 0.85,
                position: { x: 0, y: 0, z: 0 },
              };

              if (newRecord.phase === 1) {
                existing.phase1 = {
                  truthfulness: newRecord.truthfulness || 50,
                  serviceOrientation: newRecord.service_orientation || 50,
                  harmAwareness: newRecord.harm_awareness || 50,
                  autonomyRespect: newRecord.autonomy_respect || 50,
                  valueAlignment: newRecord.value_alignment || 50,
                  humility: newRecord.humility || 50,
                };
              } else if (newRecord.phase === 3) {
                existing.phase3 = {
                  truthfulness: newRecord.truthfulness || 50,
                  serviceOrientation: newRecord.service_orientation || 50,
                  harmAwareness: newRecord.harm_awareness || 50,
                  autonomyRespect: newRecord.autonomy_respect || 50,
                  valueAlignment: newRecord.value_alignment || 50,
                  humility: newRecord.humility || 50,
                };
              }

              updated.set(newRecord.agent_id, existing);
              return updated;
            });
          }
        }
      )
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, [supabase, fetchInitialData]);

  return { sigils, isLoading, error, refetch: fetchInitialData };
}
