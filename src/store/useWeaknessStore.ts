import { create } from 'zustand';
import { mathSolverService } from '../services/ai/mathSolver';
import { dbService } from '../services/supabase/client';
import { AdaptiveDiagnosticAlert, FailureType, WeaknessRecord } from '../types/math';

interface WeaknessStats {
  total: number;
  byType: Record<FailureType, number>;
  topKeywords: { keyword: string; count: number }[];
}

interface WeaknessState {
  weaknesses: WeaknessRecord[];
  adaptiveAlert: AdaptiveDiagnosticAlert | null;
  isAnalyzingAdaptive: boolean;
  stats: WeaknessStats;
  
  // Actions
  evaluateAdaptiveAlert: (concepts: string[], ocrText: string, userId: string) => Promise<void>;
  dismissAdaptiveAlert: () => void;
  loadWeaknessStats: (userId: string) => Promise<void>;
  recordWeaknessLocal: (record: WeaknessRecord) => void;
}

export const useWeaknessStore = create<WeaknessState>((set, get) => ({
  weaknesses: [
    {
      id: 'mock_w_1',
      user_id: 'default',
      question_id: 'mock_q_1',
      failure_type: 'visual',
      missed_keyword: '대칭축의 구간 분할',
      selected_clause: '닫힌구간 [0, 2]에서 최댓값 5',
      prescription_notes: '그래프 개형을 3단계로 나누어 그리는 연습 필요',
      created_at: new Date(Date.now() - 3600000 * 24 * 2).toISOString(),
    },
    {
      id: 'mock_w_2',
      user_id: 'default',
      question_id: 'mock_q_2',
      failure_type: 'visual',
      missed_keyword: '포물선 꼭짓점 위치',
      selected_clause: '이차함수 f(x)의 최솟값',
      prescription_notes: '대칭축이 범위 밖일 때 경계값 비교 누락',
      created_at: new Date(Date.now() - 3600000 * 24).toISOString(),
    },
    {
      id: 'mock_w_3',
      user_id: 'default',
      question_id: 'mock_q_3',
      failure_type: 'interpretation',
      missed_keyword: '양수 a',
      selected_clause: '양수 a의 값을 구하시오',
      prescription_notes: '부등식 조건 누락으로 음수 해 포함',
      created_at: new Date(Date.now() - 3600000 * 12).toISOString(),
    },
  ],
  adaptiveAlert: null,
  isAnalyzingAdaptive: false,
  stats: {
    total: 3,
    byType: {
      concept: 0,
      modeling: 0,
      visual: 2,
      interpretation: 1,
    },
    topKeywords: [
      { keyword: '대칭축의 구간 분할', count: 2 },
      { keyword: '양수 조건', count: 1 },
    ],
  },

  evaluateAdaptiveAlert: async (concepts: string[], ocrText: string, userId: string) => {
    set({ isAnalyzingAdaptive: true });
    try {
      const history = await dbService.fetchRecentDiagnosticHistory(userId, 10);
      const alert = await mathSolverService.analyzeAdaptiveWeakness(concepts, ocrText, history);

      if (alert && alert.has_critical_warning) {
        set({ adaptiveAlert: alert });
      }
    } catch (err) {
      console.error('[evaluateAdaptiveAlert error]', err);
    } finally {
      set({ isAnalyzingAdaptive: false });
    }
  },

  dismissAdaptiveAlert: () => {
    set({ adaptiveAlert: null });
  },

  loadWeaknessStats: async (userId: string) => {
    try {
      const stats = await dbService.fetchUserWeaknessStats(userId);
      set((state) => ({
        stats: {
          total: stats.total || state.weaknesses.length,
          byType: {
            concept: stats.byType?.concept || state.stats.byType.concept,
            modeling: stats.byType?.modeling || state.stats.byType.modeling,
            visual: stats.byType?.visual || state.stats.byType.visual,
            interpretation: stats.byType?.interpretation || state.stats.byType.interpretation,
          },
          topKeywords: stats.topKeywords?.length ? stats.topKeywords : state.stats.topKeywords,
        },
      }));
    } catch (err) {
      console.error('[loadWeaknessStats error]', err);
    }
  },

  recordWeaknessLocal: (record: WeaknessRecord) => {
    set((state) => {
      const updatedWeaknesses = [record, ...state.weaknesses];
      const updatedByType = { ...state.stats.byType };
      updatedByType[record.failure_type] = (updatedByType[record.failure_type] || 0) + 1;

      return {
        weaknesses: updatedWeaknesses,
        stats: {
          ...state.stats,
          total: updatedWeaknesses.length,
          byType: updatedByType,
        },
      };
    });
  },
}));
