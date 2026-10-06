import { create } from 'zustand';
import { ENV } from '../config/env';
import { GradeLevel } from '../types/math';

export type AuthProvider = 'kakao' | 'apple' | 'google' | 'guest';

interface AuthState {
  userId: string;
  email: string;
  nickname: string;
  provider: AuthProvider;
  isLoggedIn: boolean;
  grade: GradeLevel;
  geminiApiKey: string;

  // Pro Subscription & Daily Quotas
  isPro: boolean;
  subscriptionPlan: 'free' | 'monthly' | 'annual';
  dailySolvesRemaining: number;
  dailyChatsRemaining: number;
  isSubModalOpen: boolean;
  isLoginModalOpen: boolean;

  // Actions
  setGrade: (grade: GradeLevel) => void;
  setGeminiApiKey: (key: string) => void;
  setSubModalOpen: (open: boolean) => void;
  setLoginModalOpen: (open: boolean) => void;
  loginWithSocial: (provider: AuthProvider) => void;
  logout: () => void;
  upgradeToPro: (plan: 'monthly' | 'annual') => void;
  canSolveProblem: () => boolean;
  consumeSolveQuota: () => boolean;
  canSendChat: () => boolean;
  consumeChatQuota: () => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  userId: ENV.DEFAULT_USER_ID,
  email: 'student@rootmath.ai',
  nickname: '수학1등급도전러',
  provider: 'guest',
  isLoggedIn: true,
  grade: (ENV.DEFAULT_GRADE as GradeLevel) || '고1',
  geminiApiKey: ENV.GEMINI_API_KEY,

  isPro: false,
  subscriptionPlan: 'free',
  dailySolvesRemaining: 3,
  dailyChatsRemaining: 5,
  isSubModalOpen: false,
  isLoginModalOpen: false,

  setGrade: (grade) => set({ grade }),
  setGeminiApiKey: (geminiApiKey) => {
    ENV.GEMINI_API_KEY = geminiApiKey;
    set({ geminiApiKey });
  },
  setSubModalOpen: (open) => set({ isSubModalOpen: open }),
  setLoginModalOpen: (open) => set({ isLoginModalOpen: open }),

  loginWithSocial: (provider) => {
    set({
      isLoggedIn: true,
      provider,
      nickname: provider === 'kakao' ? '카카오_수학러' : provider === 'apple' ? '애플_수학러' : '구글_수학러',
      email: `user_${provider}@rootmath.ai`,
      isLoginModalOpen: false,
    });
  },

  logout: () => {
    set({
      isLoggedIn: false,
      provider: 'guest',
      email: '',
      nickname: '게스트',
      isPro: false,
    });
  },

  upgradeToPro: (plan) => {
    set({
      isPro: true,
      subscriptionPlan: plan,
      dailySolvesRemaining: 9999,
      dailyChatsRemaining: 9999,
      isSubModalOpen: false,
    });
  },

  canSolveProblem: () => {
    const { isPro, dailySolvesRemaining } = get();
    return isPro || dailySolvesRemaining > 0;
  },

  consumeSolveQuota: () => {
    const { isPro, dailySolvesRemaining } = get();
    if (isPro) return true;
    if (dailySolvesRemaining > 0) {
      set({ dailySolvesRemaining: dailySolvesRemaining - 1 });
      return true;
    }
    set({ isSubModalOpen: true });
    return false;
  },

  canSendChat: () => {
    const { isPro, dailyChatsRemaining } = get();
    return isPro || dailyChatsRemaining > 0;
  },

  consumeChatQuota: () => {
    const { isPro, dailyChatsRemaining } = get();
    if (isPro) return true;
    if (dailyChatsRemaining > 0) {
      set({ dailyChatsRemaining: dailyChatsRemaining - 1 });
      return true;
    }
    set({ isSubModalOpen: true });
    return false;
  },
}));
