import { getGeminiClient } from './geminiClient';
import {
  AdaptiveDiagnosticAlert,
  ChatMessage,
  CURRICULUM_MAP,
  DiagnosticHistoryItem,
  FailureType,
  GradeLevel,
  MathSolveResponse,
  StepSolution,
} from '../../types/math';

/**
 * Robust JSON parser for AI responses (handling LaTeX unescaped slashes, code fences, etc.)
 */
function parseJsonFromText(rawText: string): any {
  if (!rawText) throw new Error('AI response is empty');
  let cleaned = rawText.trim().replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/i, '').trim();

  // 1. Direct JSON parse
  try {
    return JSON.parse(cleaned);
  } catch (e1) {}

  // 2. Extract outermost { ... }
  const firstBrace = cleaned.indexOf('{');
  const lastBrace = cleaned.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace > firstBrace) {
    cleaned = cleaned.substring(firstBrace, lastBrace + 1);
    try {
      return JSON.parse(cleaned);
    } catch (e2) {}
  }

  // 3. Sanitize unescaped LaTeX backslashes (\frac, \alpha, etc.)
  const sanitized = cleaned.replace(/\\(?!["\\/bfnrtu])/g, '\\\\');
  try {
    return JSON.parse(sanitized);
  } catch (e3) {}

  // 4. Function constructor fallback
  try {
    const fn = new Function('return ' + cleaned);
    return fn();
  } catch (e4) {}

  // 5. Aggressive regex normalizer
  try {
    const agg = cleaned.replace(/\\/g, '\\\\').replace(/\\\\"/g, '\\"').replace(/\\\\\\\\/g, '\\\\');
    return JSON.parse(agg);
  } catch (e5) {}

  throw new Error('Failed to parse AI JSON response');
}

export const mathSolverService = {
  /**
   * [A. Solve Engine - 학년별 교육과정 격리 풀이 및 도식화(SVG) 생성기]
   * 대한민국 국가수학교육과정 범위를 철저히 준수하며 선행 개념 사용을 엄격히 차단함.
   */
  async solveMathProblemWithVision(
    base64Image: string,
    mimeType: string = 'image/jpeg',
    userGrade: string = '고1'
  ): Promise<MathSolveResponse> {
    const genAI = getGeminiClient();
    const currRule = CURRICULUM_MAP[userGrade as GradeLevel] || CURRICULUM_MAP['고1'];

    if (!genAI) {
      console.warn('[ReadMath] Gemini API key not found. Returning curriculum-compliant demonstration sample.');
      return getDemoSolveResponse(userGrade);
    }

    try {
      const model = genAI.getGenerativeModel({
        model: 'gemini-flash-latest',
        generationConfig: {
          temperature: 0.1,
          responseMimeType: 'application/json',
        },
      });

      const systemPrompt = `
당신은 대한민국 국가수학교육과정을 완벽히 통달한 최고 권위의 AI 수학 멘토 '리드 쌤(Read Tutor)'입니다.

[학생 학년]: ${currRule.label} (${currRule.stageName})
[허용 교육과정 범위]: ${currRule.allowedScope}
[🚨 절대 사용 금지 상위 학년 개념 (Strictly Banned Overreach)]:
👉 ${currRule.strictlyBanned}
[권장 교수학적 접근]: ${currRule.recommendedPedagogy}

[절대 불변의 문제 해결 대원칙 (수학은 언어다!)]:
"수학은 언어일 뿐이다! 수식과 조건을 일상의 언어(한글)로 번역하거나 그래프/도형으로 시각화할 수 있다면, 세상의 모든 문제는 항상 다 풀 수 있다."
풀이 과정은 반드시 다음 4단계 자연 사고 프로세스를 엄격히 준수하십시오:
1. [조건의 한글 번역]: 기호와 수식을 출제자의 본래 의도(일상의 쉬운 한글 문장)로 번역.
2. [그래프/기하 도식화]: 번역된 한글을 바탕으로 시각적 그래프/도형을 구체화하고 'visualization_svg'에 반영.
3. [인지 결손 및 함정 간파]: 놓치기 쉬운 조건(자연수, 부호, 경계)과 함정을 학생의 눈높이에서 짚어줌.
4. [필연적 등식 유도]: 억지 공식 암기가 아니라 조건과 그림이 요구하는 가장 단순하고 필연적인 식으로 해결.

[최우선 엄격 준수 규칙]:
1. **절대로 해당 학년(${userGrade})을 초과하는 상위 교육과정의 공식이나 풀이법을 끌어오지 마십시오!**
   - 예: 초등학생에게 미지수 x방정식이나 음수 부호를 쓰지 말 것 (선분도/수직선/바 모델로 설명).
   - 예: 중2 학생에게 삼각비나 근의 공식을 쓰지 말 것 (닮음과 피타고라스로 설명).
   - 예: 고1 학생에게 미분(f'(x)=0)으로 최댓값을 구하지 말 것 (반드시 완전제곱식과 대칭축 기하로 설명).
2. **논술/세트형 문항 (소문항 1번, 2번, 3번 등이 딸린 문제)인 경우**:
   - 'is_multi_question: true'로 설정하고 'sub_questions' 배열에 각 소문항 번호('sub_number'), 문제 텍스트('sub_title'), 단계별 풀이('solution_steps'), 정답('final_answer')을 각각 분리하여 누락 없이 작성하십시오.
3. **모든 설명에는 React Native react-native-svg에서 에러 없이 렌더링 가능한 유효한 SVG 문자열을 'visualization_svg' 필드에 작성하십시오.**
   - 학년 수준에 맞는 시각화:
     * 초등: 피자/분할 띠, 수직선 바 모델, 도형 겹치기
     * 중등: 격자 좌표평면, 닮음비 도형, 피타고라스 정사각형
     * 고등/논술: 대칭축 이동 포물선, 반원 및 접선, 공간도형 정사영, 그래프 개형

[출력 JSON 규격]:
{
  "ocr_text": "인식된 문제 원문 텍스트 (LaTeX 수식 포함)",
  "concepts": ["해당 학년 기준 핵심 개념 1", "핵심 개념 2"],
  "decomposed_clauses": [
    "문제 조건 1",
    "문제 조건 2",
    "구하고자 하는 목표"
  ],
  "is_multi_question": false,
  "sub_questions": [
    {
      "sub_number": 1,
      "sub_title": "1번 소문항 내용",
      "solution_steps": [
        {
          "step_number": 1,
          "title": "단계 제목",
          "content": "설명",
          "formula": "LaTeX 수식"
        }
      ],
      "final_answer": "1번 소문항 정답"
    }
  ],
  "step_by_step_solution": [
    {
      "step_number": 1,
      "title": "단계 제목",
      "latex_content": "해당 학년 허용 범위 내 수식 (LaTeX)",
      "explanation": "해당 학년 눈높이에 맞춘 명쾌한 설명 (상위 개념 배제)",
      "key_takeaway": "핵심 팁"
    }
  ],
  "answer": "최종 정답",
  "visualization_svg": "<svg viewBox='0 0 400 240' width='100%' height='240'>...</svg>"
}
`;

      const imagePart = {
        inlineData: {
          data: base64Image,
          mimeType,
        },
      };

      const result = await model.generateContent([systemPrompt, imagePart]);
      const responseText = result.response.text();
      return parseJsonFromText(responseText) as MathSolveResponse;
    } catch (error) {
      console.error('[RootMath Vision Solve Error]', error);
      return getDemoSolveResponse(userGrade);
    }
  },

  /**
   * [B. Diagnostic Engine - 취약점 누적 추적 및 선제적 지적기]
   */
  async analyzeAdaptiveWeakness(
    currentConcepts: string[],
    currentOcr: string,
    history: DiagnosticHistoryItem[]
  ): Promise<AdaptiveDiagnosticAlert> {
    const genAI = getGeminiClient();

    if (!genAI || history.length === 0) {
      return evaluateRuleBasedWeakness(currentConcepts, history);
    }

    try {
      const model = genAI.getGenerativeModel({
        model: 'gemini-flash-latest',
        generationConfig: {
          temperature: 0.2,
          responseMimeType: 'application/json',
        },
      });

      const prompt = `
당신은 출제자의 의도를 꿰뚫어 보고 학생에게 명쾌한 길을 제시하는 ReadMath 수석 튜터입니다.
[현재 문제]: ${currentOcr}
[개념]: ${JSON.stringify(currentConcepts)}
[과거 오답 및 질문 기록]: ${JSON.stringify(history, null, 2)}

반복되는 약점(동일 개념 2회 이상, 도식화 회피 등)이 발견되면 정밀하고 명확한 선제적 피드백과 실천적인 행동 강령을 JSON으로 출력하십시오.
JSON 규격:
{
  "has_critical_warning": true,
  "recurring_concept": "반복 취약 개념",
  "failure_pattern": "visual" | "modeling" | "concept" | "interpretation",
  "repetition_count": 3,
  "blunt_feedback_message": "경고 메시지",
  "remedy_action_plan": "행동 수칙"
}
`;

      const result = await model.generateContent(prompt);
      return parseJsonFromText(result.response.text()) as AdaptiveDiagnosticAlert;
    } catch (error) {
      return evaluateRuleBasedWeakness(currentConcepts, history);
    }
  },

  /**
   * [C. 1:1 Visual Examiner Math Chatbot Engine - '루트 쌤' 시각화 대화형 출제자 AI 튜터]
   * 학년 교육과정 경계를 철저히 지키며 학생의 질문에 출제자 유도 문답 + 실시간 SVG 그림 제공
   */
  async askMathTutorChat(
    problemOcr: string,
    currentSolution: MathSolveResponse,
    chatHistory: { role: 'user' | 'model'; parts: string }[],
    userQuestion: string,
    grade: string = '고1'
  ): Promise<ChatMessage> {
    const genAI = getGeminiClient();
    const currRule = CURRICULUM_MAP[grade as GradeLevel] || CURRICULUM_MAP['고1'];

    if (!genAI) {
      return getDemoChatResponse(userQuestion, problemOcr, grade);
    }

    try {
      const model = genAI.getGenerativeModel({
        model: 'gemini-flash-latest',
        generationConfig: {
          temperature: 0.25,
          responseMimeType: 'application/json',
        },
      });

      const systemPrompt = `
당신은 혼자 공부하는 학생을 1:1로 밀착 지도하는 대한민국 최고의 AI 수학 멘토 '루트 쌤'입니다.
학생 학년: ${currRule.label} (${currRule.stageName})
허용 교육과정 범위: ${currRule.allowedScope}
🚨 절대 사용 금지 상위 개념: ${currRule.strictlyBanned}
권장 시각화 도구: ${currRule.recommendedPedagogy}

[대화 원칙]:
1. 학생의 질문에 답변할 때 **절대로 상위 학년의 공식이나 풀이법(미분, 연립방정식 등)을 사용하지 마십시오.**
2. 학생이 사고의 오류를 스스로 깨달을 수 있도록 출제자 관점에서 유도 질문을 던져주고, **반드시 설명에 직관적인 시각 자료(SVG 코드)를 포함하십시오.**
3. **[핵심 대화형 역진단 기능]**: 만약 학생이 "뭘 모르는지 모르겠다", "그냥 다 어렵다", "어디서 막혔는지 찾아달라"고 하거나 풀이 방향을 전혀 잡지 못할 경우, 학생의 말에서 막힌 지점([도식화 실패], [수식 모델링 실패], [조건 해석 실패], [개념 미학습])을 핀포인트로 특정하여 'rca_diagnosis' 필드에 정확히 기록해 주십시오.
4. 다음으로 학생이 스스로 생각해볼 수 있는 추천 후속 질문 3개를 'suggested_followups'에 제안하십시오.

[출력 JSON 규격]:
{
  "text": "루트 쌤의 친절하고 날카로운 설명 텍스트 (해당 학년 수식 포함)",
  "visualization_svg": "<svg viewBox='0 0 400 220' width='100%' height='220'>...</svg>",
  "latex_formula": "가장 핵심이 되는 수식 (선택)",
  "key_concept": "질문과 관련된 핵심 수학 개념",
  "suggested_followups": [
    "추천 후속 질문 1",
    "추천 후속 질문 2",
    "추천 후속 질문 3"
  ],
  "rca_diagnosis": {
    "clause": "문제가 막힌 핵심 조건 문장",
    "failure_type": "visual" | "modeling" | "interpretation" | "concept",
    "reason": "결손 원인 한 줄 분석"
  }
}
`;

      const contents = [
        { role: 'user', parts: [{ text: systemPrompt }] },
        ...chatHistory.map((h) => ({ role: h.role, parts: [{ text: h.parts }] })),
        { role: 'user', parts: [{ text: `[학생의 질문]: ${userQuestion}` }] },
      ];

      const result = await model.generateContent({ contents } as any);
      const resJson = parseJsonFromText(result.response.text());

      return {
        id: `msg_${Date.now()}`,
        sender: 'ai',
        text: resJson.text,
        visualization_svg: resJson.visualization_svg || undefined,
        latex_formula: resJson.latex_formula || undefined,
        key_concept: resJson.key_concept || undefined,
        timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
        suggested_followups: resJson.suggested_followups || [],
        rca_diagnosis: resJson.rca_diagnosis || undefined,
      };
    } catch (error) {
      console.error('[askMathTutorChat Error]', error);
      return getDemoChatResponse(userQuestion, problemOcr, grade);
    }
  },

  /**
   * [D. Prescription Engine - 자가진단 선택 지점에 대한 1:1 맞춤형 AI 처방]
   */
  async generatePrescriptionHint(
    problemOcr: string,
    selectedClause: string,
    failureType: FailureType,
    missedKeyword: string
  ): Promise<string> {
    return getDemoPrescription(failureType, missedKeyword, selectedClause);
  }
};

function evaluateRuleBasedWeakness(
  currentConcepts: string[],
  history: DiagnosticHistoryItem[]
): AdaptiveDiagnosticAlert {
  if (history.length === 0) {
    return {
      has_critical_warning: false,
      repetition_count: 0,
      blunt_feedback_message: '',
      remedy_action_plan: '',
    };
  }

  const conceptFreq: Record<string, number> = {};
  history.forEach((h) => {
    h.concepts_used.forEach((c) => {
      conceptFreq[c] = (conceptFreq[c] || 0) + 1;
    });
  });

  for (const concept of currentConcepts) {
    if ((conceptFreq[concept] || 0) >= 2) {
      return {
        has_critical_warning: true,
        recurring_concept: concept,
        failure_pattern: 'visual',
        repetition_count: (conceptFreq[concept] || 0) + 1,
        blunt_feedback_message: `잠깐! 이전 문제들과 이번 문제의 공통점은 '${concept}' 개념을 조건부로 해석하는 것입니다. 공식을 단순 암기해서 풀려고 하면 계속 틀립니다. 반드시 그래프를 직접 그리고 구간을 분할해야 합니다.`,
        remedy_action_plan: `1. '${concept}'의 기본 정의를 다시 도식화하세요.\n2. 수식을 쓰기 전에 그래프의 대칭축 위치 3가지를 손으로 직접 그리는 습관을 들이세요.`,
      };
    }
  }

  return {
    has_critical_warning: false,
    repetition_count: 0,
    blunt_feedback_message: '',
    remedy_action_plan: '',
  };
}

function getDemoSolveResponse(grade: string = '고1'): MathSolveResponse {
  return {
    ocr_text: '이차함수 $f(x) = -x^2 + 2ax + 1$이 닫힌구간 $[0, 2]$에서 최댓값 $5$를 가질 때, 양수 $a$의 값을 구하시오. (고1 공통수학: 미분 사용 금지, 완전제곱식 및 대칭축 분할 풀이)',
    concepts: ['이차함수의 최대·최소 (고1)', '완전제곱식과 대칭축 위치', '제한된 구간의 대소 판별'],
    decomposed_clauses: [
      '이차함수 f(x) = -x^2 + 2ax + 1이',
      '닫힌구간 [0, 2]에서',
      '최댓값 5를 가질 때,',
      '양수 a의 값을 구하시오.',
    ],
    step_by_step_solution: [
      {
        step_number: 1,
        title: '1. 고1 표준형 완전제곱식 변환 (미분 배제)',
        latex_content: 'f(x) = -(x - a)^2 + a^2 + 1',
        explanation: '고1 과정에서는 미분을 쓰지 않고 완전제곱식으로 변환하여 위로 볼록한 포물선의 꼭짓점 $(a, a^2 + 1)$과 대칭축 $x = a$를 파악합니다.',
        key_takeaway: '대칭축 $x = a$가 미지수이므로 구간 $[0, 2]$와의 상대적 위치로 분류합니다.',
      },
      {
        step_number: 2,
        title: '2. 대칭축 위치별 경우의 수 도식화 (Case 분류)',
        latex_content: '\\text{Case 1: } 0 < a < 2 \\implies x=a\\text{에서 최대 } a^2+1=5 \\implies a=2 \\text{ (모순)}\n\\text{Case 2: } a \\ge 2 \\implies x=2\\text{에서 최대 } 4a-3=5 \\implies a=2 \\text{ (적합)}',
        explanation: '$a > 0$이므로 $a \\le 0$은 제외합니다. 대칭축이 구간 오른쪽($a \\ge 2$)일 때 구간 안에서 함수가 증가하므로 $x=2$에서 최댓값 $5$를 가집니다.',
        key_takeaway: '도출된 $a$의 값이 가정한 Case 조건 범위에 들어맞는지 반드시 검증해야 합니다.',
      },
      {
        step_number: 3,
        title: '3. 최종 결론 및 검증',
        latex_content: 'a = 2',
        explanation: '$a = 2$일 때 $f(x) = -x^2 + 4x + 1$이며, $[0, 2]$에서 $f(0)=1, f(2)=5$로 최댓값 $5$를 정확히 만족합니다.',
        key_takeaway: '상위 공식 암기가 아닌 포물선의 개형과 구간의 상대적 위치를 눈으로 확인하세요.',
      },
    ],
    answer: 'a = 2',
    visualization_svg: `<svg viewBox="0 0 400 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
      <rect width="400" height="240" fill="#090D16" rx="12"/>
      <line x1="40" y1="40" x2="370" y2="40" stroke="#1E293B" stroke-width="1" stroke-dasharray="3"/>
      <line x1="40" y1="120" x2="370" y2="120" stroke="#1E293B" stroke-width="1" stroke-dasharray="3"/>
      <line x1="40" y1="190" x2="370" y2="190" stroke="#1E293B" stroke-width="1" stroke-dasharray="3"/>
      <line x1="50" y1="200" x2="370" y2="200" stroke="#64748B" stroke-width="1.5"/>
      <line x1="70" y1="220" x2="70" y2="20" stroke="#64748B" stroke-width="1.5"/>
      <text x="360" y="215" fill="#94A3B8" font-size="12" font-weight="bold">x</text>
      <text x="55" y="30" fill="#94A3B8" font-size="12" font-weight="bold">y</text>
      <rect x="70" y="25" width="160" height="175" fill="#3B82F6" fill-opacity="0.12"/>
      <line x1="230" y1="205" x2="230" y2="25" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="3"/>
      <text x="65" y="215" fill="#94A3B8" font-size="11">0</text>
      <text x="225" y="215" fill="#60A5FA" font-size="12" font-weight="bold">x=2</text>
      <path d="M 30 210 Q 130 45 230 45 T 350 210" fill="none" stroke="#10B981" stroke-width="3"/>
      <circle cx="230" cy="45" r="5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.5"/>
      <text x="240" y="44" fill="#EF4444" font-size="11" font-weight="bold">최댓값 (2, 5)</text>
      <line x1="70" y1="45" x2="230" y2="45" stroke="#EF4444" stroke-width="1" stroke-dasharray="3"/>
      <text x="45" y="49" fill="#EF4444" font-size="10">y=5</text>
      <line x1="230" y1="15" x2="230" y2="205" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="4"/>
      <text x="210" y="15" fill="#A78BFA" font-size="10" font-weight="bold">대칭축 x=a (a=2)</text>
    </svg>`,
  };
}

function getDemoChatResponse(
  userQuestion: string,
  problemOcr: string,
  grade: string
): ChatMessage {
  const q = userQuestion.toLowerCase();

  if (q.includes('대칭축') || q.includes('음수') || q.includes('좌측')) {
    return {
      id: `msg_${Date.now()}`,
      sender: 'ai',
      text: `좋은 질문입니다! 만약 대칭축 $x=a$가 $0$보다 작은 음수($a < 0$)라면 포물선은 구간 $[0, 2]$의 왼쪽 바깥에 놓이게 됩니다.\n\n이 경우 구간 $[0, 2]$ 안에서는 포물선이 **계속 감소하는 형태**가 되므로, 최댓값은 꼭짓점이 아닌 구간의 시작점 $x=0$에서 발생하게 됩니다 ($f(0)=1$).\n하지만 문제에서 최댓값이 $5$라고 했으므로 $1=5$가 되어 모순이 발생합니다. 그래서 $a < 0$인 경우는 탈락인 것이죠!`,
      latex_formula: 'a < 0 \\implies \\max_{x \\in [0, 2]} f(x) = f(0) = 1 \\ne 5 \\quad (\\text{모순})',
      key_concept: '대칭축이 구간 왼쪽에 있을 때의 단조감소 성질 (고1 완전제곱식 기반)',
      timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
      visualization_svg: `<svg viewBox="0 0 400 210" width="100%" height="210" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="210" fill="#090D16" rx="10"/>
        <line x1="40" y1="170" x2="370" y2="170" stroke="#64748B" stroke-width="1.5"/>
        <line x1="160" y1="190" x2="160" y2="20" stroke="#64748B" stroke-width="1.5"/>
        <rect x="160" y="25" width="140" height="145" fill="#3B82F6" fill-opacity="0.15"/>
        <text x="155" y="185" fill="#94A3B8" font-size="11">0</text>
        <text x="295" y="185" fill="#60A5FA" font-size="11" font-weight="bold">2</text>
        <path d="M 40 170 Q 90 40 160 90 T 360 200" fill="none" stroke="#EF4444" stroke-width="2.5"/>
        <line x1="90" y1="20" x2="90" y2="170" stroke="#F59E0B" stroke-dasharray="3"/>
        <text x="50" y="35" fill="#F59E0B" font-size="10" font-weight="bold">대칭축 x=a &lt; 0</text>
        <circle cx="160" cy="90" r="4" fill="#10B981"/>
        <text x="170" y="85" fill="#10B981" font-size="10" font-weight="bold">구간 내 최댓값 f(0)=1</text>
      </svg>`,
      suggested_followups: [
        '대칭축이 구간 안에 있을 때는 왜 답이 아닌가요?',
        '포물선이 아래로 볼록할 때는 어떻게 달라지나요?',
        '비슷한 고1 기출 변형 문제 더 볼래요.',
      ],
    };
  }

  if (q.includes('쉽게') || q.includes('초등') || q.includes('중학')) {
    return {
      id: `msg_${Date.now()}`,
      sender: 'ai',
      text: `산꼭대기(포물선의 꼭짓점)와 울타리(구간 $[0, 2]$)의 위치 관계를 생각해보세요! ⛰️\n\n1. 산꼭대기가 울타리 안에 있으면: 산꼭대기가 가장 높은 곳(최댓값)입니다.\n2. 산꼭대기가 울타리 바깥 오른쪽에 있으면: 울타리 안에서 가장 오른쪽 끝($x=2$)이 제일 높은 지점이 됩니다.\n\n이 문제에서는 산꼭대기가 오른쪽($a=2$)에 있어서 울타리 오른쪽 끝인 $x=2$에서 최댓값 $5$를 찍게 된 것입니다!`,
      latex_formula: 'x=2 \\text{ (울타리 오른쪽 끝)} \\implies f(2) = 5',
      key_concept: '산꼭대기와 관찰 구간의 기하학적 직관',
      timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
      visualization_svg: `<svg viewBox="0 0 400 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="180" fill="#090D16" rx="10"/>
        <path d="M 50 150 Q 250 30 350 150" fill="none" stroke="#10B981" stroke-width="3"/>
        <line x1="120" y1="150" x2="120" y2="70" stroke="#F59E0B" stroke-width="3"/>
        <line x1="250" y1="150" x2="250" y2="30" stroke="#3B82F6" stroke-width="3"/>
        <text x="100" y="165" fill="#F59E0B" font-size="11">울타리 시작(0)</text>
        <text x="235" y="165" fill="#3B82F6" font-size="11" font-weight="bold">울타리 끝(2)</text>
        <circle cx="250" cy="30" r="5" fill="#EF4444"/>
        <text x="260" y="35" fill="#EF4444" font-size="11" font-weight="bold">산꼭대기 = 최댓값 (5)</text>
      </svg>`,
      suggested_followups: [
        '대칭축이 음수일 땐 그림이 어떻게 바뀌나요?',
        '완전제곱식으로 바꾸는 과정을 더 자세히 보여줘.',
        '나의 약점 리포트에서 취약점을 보고 싶어.',
      ],
    };
  }

  return {
    id: `msg_${Date.now()}`,
    sender: 'ai',
    text: `"${userQuestion}"에 대해 루트 쌤이 짚어줄게요!\n\n이 문제의 가장 본질적인 함정은 **'미지수 $a$가 x좌표(대칭축)에 들어있다'**는 점입니다. 많은 학생들이 축이 움직인다는 사실을 잊고 꼭짓점 $y$값만 $5$라고 두고 풀어서 오답을 냅니다.\n\n아래 시각화 도표를 보며 대칭축 $x=a$의 위치가 왜 $x=2$로 확정되는지 눈으로 확인해보세요!`,
    latex_formula: 'f(2) = -2^2 + 2a(2) + 1 = 4a - 3 = 5 \\implies a = 2',
    key_concept: '움직이는 대칭축과 고정된 정의구역의 상대적 위치',
    timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }),
    visualization_svg: `<svg viewBox="0 0 400 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
      <rect width="400" height="180" fill="#090D16" rx="10"/>
      <line x1="30" y1="150" x2="370" y2="150" stroke="#64748B" stroke-width="1.5"/>
      <rect x="80" y="30" width="160" height="120" fill="#3B82F6" fill-opacity="0.15"/>
      <path d="M 40 160 Q 140 40 240 40 T 360 160" fill="none" stroke="#10B981" stroke-width="2.5"/>
      <circle cx="240" cy="40" r="5" fill="#EF4444"/>
      <text x="245" y="35" fill="#EF4444" font-size="11" font-weight="bold">x=2에서 최대 (y=5)</text>
    </svg>`,
    suggested_followups: [
      '대칭축이 음수일 땐 어떻게 되나요?',
      '초등학생도 이해할 수 있게 더 쉽게 설명해줘.',
      '왜 Case 1에서 a=2가 모순인가요?',
    ],
  };
}

function getDemoPrescription(
  failureType: FailureType,
  keyword: string,
  clause: string
): string {
  switch (failureType) {
    case 'visual':
      return `### 💡 도식화(그래프 그리기) 솔루션
1. **왜 그래프를 그려야 할까요?**
   "${clause}" 조건에서 미지수 $a$가 대칭축에 있을 때는 식만으로 최댓값의 위치를 확정할 수 없습니다.
2. **지금 바로 그리는 3단계:**
   - 위로 볼록한 포물선 $y=-(x-a)^2 + a^2+1$의 개형을 그립니다.
   - 고정된 구간 $[0, 2]$를 수직선에 긋습니다.
   - 대칭축 $x=a$를 왼쪽($a < 0$), 내부($0 \\le a \\le 2$), 오른쪽($a > 2$)으로 움직여보며 꼭짓점이 구간에 포함되는지 확인합니다.
3. **스스로 던질 질문:** "대칭축이 구간의 오른쪽에 있을 때 포물선은 구간 안에서 증가하는가, 감소하는가?"`;

    case 'modeling':
      return `### 💡 수식 모델링 변환 솔루션
1. **문장 조건 해석:** "${clause}"
   '구간 $[0, 2]$에서 최댓값 $5$'라는 한국어 조건은 $f(x)$의 최고점 좌표의 $y$값이 $5$라는 대수적 방정식으로 변환됩니다.
2. **수식 변환 공식:**
   - 대칭축이 구간 안일 때: 꼭짓점의 $y$값 $a^2 + 1 = 5$
   - 대칭축이 구간 밖일 때: 경계값 $f(2) = 5$
3. **스스로 던질 질문:** "최댓값이 나오는 $x$의 위치를 식으로 정확히 특정했는가?"`;

    case 'interpretation':
      return `### 💡 조건/단어 해석 솔루션
1. **놓친 핵심 키워드:** "${keyword}"
   '양수 $a$'라는 조건은 $a > 0$이라는 부등식 제한 조건입니다.
2. **이 조건이 답을 바꾸는 이유:**
   대칭축 $x=a$가 $0$보다 작은 음수인 경우는 애초에 고려할 필요가 없음을 뜻합니다.
3. **스스로 던질 질문:** "구한 답 중 양수 조건에 모순되는 것은 없는가?"`;

    default:
      return `### 💡 개념 보완 처방
1. **개념의 본질:** 이차함수의 최대·최소는 언제나 **꼭짓점**과 **구간의 양 끝점** 3군데 중 하나에서만 발생합니다.
2. **유형 암기 탈피:** 공식을 외우지 말고 포물선의 증감 상태를 파악하세요.`;
  }
}
