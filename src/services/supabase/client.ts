import { createClient } from '@supabase/supabase-js';
import { ENV } from '../../config/env';
import { DiagnosticHistoryItem, MathSolveResponse, QuestionRecord, WeaknessRecord, FailureType } from '../../types/math';

// Initialize Supabase Client
export const supabase = createClient(ENV.SUPABASE_URL, ENV.SUPABASE_ANON_KEY, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
});

export const dbService = {
  /**
   * Save a newly solved math question into Supabase
   */
  async saveQuestion(
    userId: string,
    solveData: MathSolveResponse,
    imageUrl?: string
  ): Promise<QuestionRecord | null> {
    try {
      const payload = {
        user_id: userId,
        image_url: imageUrl || null,
        ocr_text: solveData.ocr_text,
        concepts_used: solveData.concepts,
        step_by_step_solution: solveData.step_by_step_solution,
        answer: solveData.answer,
        visualization_svg: solveData.visualization_svg,
      };

      const { data, error } = await supabase
        .from('questions')
        .insert(payload)
        .select()
        .single();

      if (error) {
        console.warn('[Supabase saveQuestion Error] Falling back to local ID:', error.message);
        return {
          id: `local_q_${Date.now()}`,
          user_id: userId,
          image_url: imageUrl,
          ocr_text: solveData.ocr_text,
          concepts_used: solveData.concepts,
          step_by_step_solution: solveData.step_by_step_solution,
          answer: solveData.answer,
          visualization_svg: solveData.visualization_svg,
          created_at: new Date().toISOString(),
        };
      }

      return data as QuestionRecord;
    } catch (err) {
      console.warn('[Supabase Connection Exception]', err);
      return {
        id: `local_q_${Date.now()}`,
        user_id: userId,
        image_url: imageUrl,
        ocr_text: solveData.ocr_text,
        concepts_used: solveData.concepts,
        step_by_step_solution: solveData.step_by_step_solution,
        answer: solveData.answer,
        visualization_svg: solveData.visualization_svg,
        created_at: new Date().toISOString(),
      };
    }
  },

  /**
   * Save Root Cause Analysis (RCA) weakness data
   */
  async saveWeakness(
    userId: string,
    questionId: string,
    failureType: FailureType,
    missedKeyword: string,
    selectedClause?: string,
    prescriptionNotes?: string
  ): Promise<WeaknessRecord | null> {
    try {
      const payload = {
        user_id: userId,
        question_id: questionId,
        failure_type: failureType,
        missed_keyword: missedKeyword,
        selected_clause: selectedClause,
        prescription_notes: prescriptionNotes,
      };

      const { data, error } = await supabase
        .from('weaknesses')
        .insert(payload)
        .select()
        .single();

      if (error) {
        console.warn('[Supabase saveWeakness Error] Falling back to local:', error.message);
        return {
          id: `local_w_${Date.now()}`,
          user_id: userId,
          question_id: questionId,
          failure_type: failureType,
          missed_keyword: missedKeyword,
          selected_clause: selectedClause,
          prescription_notes: prescriptionNotes,
          created_at: new Date().toISOString(),
        };
      }

      return data as WeaknessRecord;
    } catch (err) {
      console.warn('[Supabase saveWeakness Exception]', err);
      return {
        id: `local_w_${Date.now()}`,
        user_id: userId,
        question_id: questionId,
        failure_type: failureType,
        missed_keyword: missedKeyword,
        selected_clause: selectedClause,
        prescription_notes: prescriptionNotes,
        created_at: new Date().toISOString(),
      };
    }
  },

  /**
   * Fetch recent 10 questions and their diagnosed failure types for the Adaptive AI Diagnostic Engine
   */
  async fetchRecentDiagnosticHistory(userId: string, limit: number = 10): Promise<DiagnosticHistoryItem[]> {
    try {
      const { data, error } = await supabase
        .from('questions')
        .select(`
          id,
          ocr_text,
          concepts_used,
          created_at,
          weaknesses (
            failure_type,
            missed_keyword
          )
        `)
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
        .limit(limit);

      if (error || !data) {
        return [];
      }

      return data.map((row: any) => {
        const weakness = Array.isArray(row.weaknesses) && row.weaknesses.length > 0 ? row.weaknesses[0] : row.weaknesses;
        return {
          question_id: row.id,
          ocr_text: row.ocr_text,
          concepts_used: row.concepts_used || [],
          failure_type: weakness?.failure_type,
          missed_keyword: weakness?.missed_keyword,
          created_at: row.created_at,
        };
      });
    } catch (err) {
      console.warn('[Supabase fetchRecentDiagnosticHistory Exception]', err);
      return [];
    }
  },

  /**
   * Fetch aggregate weakness statistics for Weakness Report Screen
   */
  async fetchUserWeaknessStats(userId: string) {
    try {
      const { data, error } = await supabase
        .from('weaknesses')
        .select('failure_type, missed_keyword, created_at')
        .eq('user_id', userId);

      if (error || !data) return { total: 0, byType: {}, topKeywords: [] };

      const byType: Record<string, number> = {
        concept: 0,
        modeling: 0,
        visual: 0,
        interpretation: 0,
      };

      const keywordCount: Record<string, number> = {};

      data.forEach((item) => {
        if (byType[item.failure_type] !== undefined) {
          byType[item.failure_type]++;
        }
        if (item.missed_keyword) {
          keywordCount[item.missed_keyword] = (keywordCount[item.missed_keyword] || 0) + 1;
        }
      });

      const topKeywords = Object.entries(keywordCount)
        .map(([keyword, count]) => ({ keyword, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);

      return {
        total: data.length,
        byType,
        topKeywords,
      };
    } catch (err) {
      return { total: 0, byType: {}, topKeywords: [] };
    }
  }
};
