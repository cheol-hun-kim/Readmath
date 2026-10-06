import { create } from 'zustand';
import { QuestionRecord, FailureType } from '../types/math';

interface HistoryState {
  savedProblems: QuestionRecord[];
  activeFilter: 'all' | FailureType | 'resolved';
  searchQuery: string;
  
  // Actions
  addSavedProblem: (problem: QuestionRecord) => void;
  toggleResolved: (questionId: string) => void;
  setActiveFilter: (filter: 'all' | FailureType | 'resolved') => void;
  setSearchQuery: (query: string) => void;
  deleteProblem: (questionId: string) => void;
}

export const useHistoryStore = create<HistoryState>((set) => ({
  savedProblems: [
    {
      id: 'demo_saved_1',
      user_id: 'default_user',
      ocr_text: '이차함수 f(x) = -x² + 2ax + 1이 닫힌구간 [0, 2]에서 최댓값 5를 가질 때, 양수 a의 값을 구하시오.',
      concepts_used: ['이차함수의 최대·최소', '대칭축 구간 분할'],
      step_by_step_solution: [
        {
          step_number: 1,
          title: '1. 표준형 변환',
          latex_content: 'f(x) = -(x-a)^2 + a^2 + 1',
          explanation: '꼭짓점 (a, a²+1), 대칭축 x=a',
        },
      ],
      answer: 'a = 2',
      created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
      weakness: {
        id: 'w_1',
        user_id: 'default_user',
        question_id: 'demo_saved_1',
        failure_type: 'visual',
        missed_keyword: '대칭축의 구간 분할',
        selected_clause: '닫힌구간 [0, 2]에서 최댓값 5',
        is_resolved: false,
        created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
      },
    },
    {
      id: 'demo_saved_2',
      user_id: 'default_user',
      ocr_text: '두 직선 y = 2x + 1과 y = -1/2x + k가 x축 위에서 만날 때, 상수 k의 값을 구하시오.',
      concepts_used: ['직선의 방정식', 'x절편 조건'],
      step_by_step_solution: [
        {
          step_number: 1,
          title: '1. x절편 도출',
          latex_content: 'y=0 \\implies 2x+1=0 \\implies x=-1/2',
          explanation: '만나는 점 (-1/2, 0) 대입',
        },
      ],
      answer: 'k = -1/4',
      created_at: new Date(Date.now() - 3600000 * 26).toISOString(),
      weakness: {
        id: 'w_2',
        user_id: 'default_user',
        question_id: 'demo_saved_2',
        failure_type: 'modeling',
        missed_keyword: 'x축 위에서 만날 때',
        selected_clause: 'x축 위에서 만날 때',
        is_resolved: true,
        created_at: new Date(Date.now() - 3600000 * 26).toISOString(),
      },
    },
  ],
  activeFilter: 'all',
  searchQuery: '',

  addSavedProblem: (problem) =>
    set((state) => ({
      savedProblems: [problem, ...state.savedProblems],
    })),

  toggleResolved: (questionId) =>
    set((state) => ({
      savedProblems: state.savedProblems.map((p) => {
        if (p.id === questionId && p.weakness) {
          return {
            ...p,
            weakness: {
              ...p.weakness,
              is_resolved: !p.weakness.is_resolved,
            },
          };
        }
        return p;
      }),
    })),

  setActiveFilter: (filter) => set({ activeFilter: filter }),
  setSearchQuery: (query) => set({ searchQuery: query }),
  deleteProblem: (questionId) =>
    set((state) => ({
      savedProblems: state.savedProblems.filter((p) => p.id !== questionId),
    })),
}));
