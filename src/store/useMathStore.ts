import { create } from 'zustand';
import { mathSolverService } from '../services/ai/mathSolver';
import { dbService } from '../services/supabase/client';
import { ChatMessage, FailureType, MathSolveResponse } from '../types/math';
import { useWeaknessStore } from './useWeaknessStore';

interface MathState {
  currentImageUri: string | null;
  currentBase64: string | null;
  isSolving: boolean;
  solveError: string | null;
  currentProblem: MathSolveResponse | null;
  currentQuestionId: string | null;
  
  // RCA Interaction State
  selectedClause: string | null;
  selectedKeyword: string | null;
  selectedFailureType: FailureType | null;
  isDiagnosticModalOpen: boolean;
  prescriptionResponse: string | null;
  isGeneratingPrescription: boolean;

  // 1:1 Visual Math Chatbot State ('루트 쌤')
  chatMessages: ChatMessage[];
  isChatLoading: boolean;

  // Actions
  setImage: (uri: string | null, base64: string | null) => void;
  solveProblem: (grade: string, userId: string) => Promise<boolean>;
  setSelectedClause: (clause: string | null) => void;
  setSelectedKeyword: (keyword: string | null) => void;
  setSelectedFailureType: (type: FailureType | null) => void;
  setDiagnosticModalOpen: (open: boolean) => void;
  submitDiagnosisAndGetPrescription: (userId: string) => Promise<void>;
  
  // Chat Actions
  initChatForProblem: (problem: MathSolveResponse, grade: string) => void;
  sendChatMessage: (questionText: string, grade: string) => Promise<void>;
  resetCurrentProblem: () => void;
}

export const useMathStore = create<MathState>((set, get) => ({
  currentImageUri: null,
  currentBase64: null,
  isSolving: false,
  solveError: null,
  currentProblem: null,
  currentQuestionId: null,

  selectedClause: null,
  selectedKeyword: null,
  selectedFailureType: null,
  isDiagnosticModalOpen: false,
  prescriptionResponse: null,
  isGeneratingPrescription: false,

  chatMessages: [],
  isChatLoading: false,

  setImage: (uri, base64) => set({ currentImageUri: uri, currentBase64: base64 }),

  solveProblem: async (grade: string, userId: string) => {
    set({ isSolving: true, solveError: null, currentProblem: null, prescriptionResponse: null, chatMessages: [] });
    try {
      const base64 = get().currentBase64 || '';
      const response = await mathSolverService.solveMathProblemWithVision(base64, 'image/jpeg', grade);

      // Save to Supabase
      const savedQuestion = await dbService.saveQuestion(userId, response, get().currentImageUri || undefined);
      const questionId = savedQuestion?.id || `q_${Date.now()}`;

      set({
        currentProblem: response,
        currentQuestionId: questionId,
        isSolving: false,
      });

      // Initialize Chatbot with welcome message
      get().initChatForProblem(response, grade);

      // Trigger Adaptive Diagnostic Engine asynchronously
      useWeaknessStore.getState().evaluateAdaptiveAlert(response.concepts, response.ocr_text, userId);

      return true;
    } catch (err: any) {
      console.error('[MathStore solveProblem Error]', err);
      set({
        isSolving: false,
        solveError: err.message || '문제 풀이 중 오류가 발생했습니다.',
      });
      return false;
    }
  },

  setSelectedClause: (clause) => set({ selectedClause: clause }),
  setSelectedKeyword: (keyword) => set({ selectedKeyword: keyword }),
  setSelectedFailureType: (type) => set({ selectedFailureType: type }),
  setDiagnosticModalOpen: (open) => set({ isDiagnosticModalOpen: open }),

  submitDiagnosisAndGetPrescription: async (userId: string) => {
    const { currentProblem, currentQuestionId, selectedClause, selectedKeyword, selectedFailureType } = get();
    if (!currentProblem || !selectedFailureType) return;

    set({ isGeneratingPrescription: true });

    const clause = selectedClause || currentProblem.ocr_text;
    const keyword = selectedKeyword || '핵심 조건';

    try {
      const prescription = await mathSolverService.generatePrescriptionHint(
        currentProblem.ocr_text,
        clause,
        selectedFailureType,
        keyword
      );

      if (currentQuestionId) {
        await dbService.saveWeakness(
          userId,
          currentQuestionId,
          selectedFailureType,
          keyword,
          clause,
          prescription
        );
      }

      useWeaknessStore.getState().recordWeaknessLocal({
        id: `w_${Date.now()}`,
        user_id: userId,
        question_id: currentQuestionId || 'unknown',
        failure_type: selectedFailureType,
        missed_keyword: keyword,
        selected_clause: clause,
        prescription_notes: prescription,
        created_at: new Date().toISOString(),
      });

      set({
        prescriptionResponse: prescription,
        isGeneratingPrescription: false,
        isDiagnosticModalOpen: false,
      });
    } catch (err) {
      console.error('[submitDiagnosis error]', err);
      set({ isGeneratingPrescription: false });
    }
  },

  initChatForProblem: (problem: MathSolveResponse, grade: string) => {
    const initialMsg: ChatMessage = {
      id: `welcome_${Date.now()}`,
      sender: 'ai',
      text: `안녕하세요! AI 수학 멘토 '루트 쌤'입니다. 🧑‍🏫\n\n방금 분석한 **[${problem.concepts[0] || '수학 문제'}]**에 대해 궁금한 점이나 헷갈리는 부분이 있나요?\n"왜 이렇게 풀었는지", "그림을 다른 각도로 보고 싶은지" 무엇이든 편하게 물어보세요! 모든 설명에 시각화 그림(SVG)을 그려서 보여줄게요.`,
      timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
      suggested_followups: [
        '대칭축이 음수일 땐 그림이 어떻게 바뀌나요?',
        '초등학생/중학생도 이해할 수 있게 더 쉽게 설명해줘.',
        '완전제곱식으로 바꾸는 이유가 뭔가요?',
      ],
    };
    set({ chatMessages: [initialMsg] });
  },

  sendChatMessage: async (questionText: string, grade: string) => {
    const { currentProblem, chatMessages } = get();
    if (!currentProblem || !questionText.trim()) return;

    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      sender: 'user',
      text: questionText,
      timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
    };

    set({
      chatMessages: [...chatMessages, userMsg],
      isChatLoading: true,
    });

    try {
      const historyPayload = chatMessages.map((m) => ({
        role: (m.sender === 'user' ? 'user' : 'model') as 'user' | 'model',
        parts: m.text,
      }));

      const aiResponse = await mathSolverService.askMathTutorChat(
        currentProblem.ocr_text,
        currentProblem,
        historyPayload,
        questionText,
        grade
      );

      set((state) => ({
        chatMessages: [...state.chatMessages, aiResponse],
        isChatLoading: false,
      }));
    } catch (err) {
      console.error('[sendChatMessage error]', err);
      set({ isChatLoading: false });
    }
  },

  resetCurrentProblem: () => {
    set({
      currentImageUri: null,
      currentBase64: null,
      currentProblem: null,
      currentQuestionId: null,
      selectedClause: null,
      selectedKeyword: null,
      selectedFailureType: null,
      prescriptionResponse: null,
      isDiagnosticModalOpen: false,
      solveError: null,
      chatMessages: [],
    });
  },
}));
