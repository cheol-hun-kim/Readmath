-- ==============================================================================
-- ReadMath (리드매스) - Supabase Database Schema
-- Root Cause Analysis (RCA) & Adaptive Weakness Tracking for Math Students
-- ==============================================================================

-- 1. Create Enums
DO $$ BEGIN
    CREATE TYPE failure_type_enum AS ENUM (
        'concept',          -- [개념 미학습] 해당 개념 자체를 모름
        'modeling',         -- [수식 모델링 실패] 조건을 수식/방정식으로 바꾸지 못함
        'visual',           -- [도식화 실패] 그래프나 기하 도형을 그리지 못함
        'interpretation'    -- [조건 해석 실패] 문제의 특정 단어나 제한 조건을 간과함
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE,
    nickname TEXT,
    name TEXT NOT NULL,
    phone TEXT,
    school TEXT,
    grade TEXT NOT NULL DEFAULT '고1', -- '초1' ~ '고3/N수'
    target_exam TEXT DEFAULT '수능/내신 1등급',
    is_suspended BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Questions Table
CREATE TABLE IF NOT EXISTS public.questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    image_url TEXT,
    ocr_text TEXT NOT NULL,
    concepts_used TEXT[] NOT NULL DEFAULT '{}',
    step_by_step_solution JSONB NOT NULL DEFAULT '[]'::jsonb,
    answer TEXT NOT NULL,
    visualization_svg TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Weaknesses Table (RCA Log)
CREATE TABLE IF NOT EXISTS public.weaknesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    failure_type failure_type_enum NOT NULL,
    missed_keyword TEXT NOT NULL,
    selected_clause TEXT,
    prescription_notes TEXT,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Student Feedbacks & Problem Reports Table
CREATE TABLE IF NOT EXISTS public.feedbacks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_name TEXT NOT NULL,
    school TEXT,
    grade TEXT,
    phone TEXT,
    category TEXT NOT NULL, -- '풀이 및 도식 오류', '기능 개선 제안', '기타 문의'
    content TEXT NOT NULL,
    is_reviewed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Indexes for Fast Querying & Analytics
CREATE INDEX IF NOT EXISTS idx_questions_user_id_created_at ON public.questions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_questions_concepts_used ON public.questions USING GIN(concepts_used);
CREATE INDEX IF NOT EXISTS idx_weaknesses_user_id_created_at ON public.weaknesses(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_weaknesses_failure_type ON public.weaknesses(user_id, failure_type);
CREATE INDEX IF NOT EXISTS idx_feedbacks_created_at ON public.feedbacks(created_at DESC);

-- 7. Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.weaknesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedbacks ENABLE ROW LEVEL SECURITY;

-- Allow public / anon read/write for MVP development (or bind to auth.uid())
CREATE POLICY "Users access own profile" ON public.users FOR ALL USING (true);
CREATE POLICY "Users access own questions" ON public.questions FOR ALL USING (true);
CREATE POLICY "Users access own weaknesses" ON public.weaknesses FOR ALL USING (true);
CREATE POLICY "Public insert feedbacks" ON public.feedbacks FOR INSERT WITH CHECK (true);
CREATE POLICY "Public select feedbacks" ON public.feedbacks FOR SELECT USING (true);
CREATE POLICY "Public update feedbacks" ON public.feedbacks FOR UPDATE USING (true);

-- 7. Analytics View: Student Weakness Summary (Aggregation for Adaptive Alerts)
CREATE OR REPLACE VIEW public.view_student_weakness_summary AS
SELECT 
    w.user_id,
    w.failure_type,
    COUNT(*) as total_occurrences,
    array_agg(DISTINCT w.missed_keyword) as missed_keywords,
    array_agg(DISTINCT c.concept) as recurring_concepts
FROM public.weaknesses w
JOIN public.questions q ON w.question_id = q.id
CROSS JOIN LATERAL unnest(q.concepts_used) as c(concept)
GROUP BY w.user_id, w.failure_type;

-- 8. RPC Function: Get Recent 10 Question History with RCA for Adaptive AI Diagnostic Engine
CREATE OR REPLACE FUNCTION public.get_recent_diagnostic_context(p_user_id UUID, p_limit INT DEFAULT 10)
RETURNS TABLE (
    question_id UUID,
    ocr_text TEXT,
    concepts_used TEXT[],
    failure_type failure_type_enum,
    missed_keyword TEXT,
    created_at TIMESTAMPTZ
) 
LANGUAGE sql STABLE AS $$
    SELECT 
        q.id as question_id,
        q.ocr_text,
        q.concepts_used,
        w.failure_type,
        w.missed_keyword,
        q.created_at
    FROM public.questions q
    LEFT JOIN public.weaknesses w ON q.id = w.question_id
    WHERE q.user_id = p_user_id
    ORDER BY q.created_at DESC
    LIMIT p_limit;
$$;
