export type GradeLevel = 
  | '초1' | '초2' | '초3' | '초4' | '초5' | '초6'
  | '중1' | '중2' | '중3'
  | '고1' | '고2' | '고3/N수';

export type SchoolStage = 'elementary_lower' | 'elementary_upper' | 'middle' | 'high';

export interface CurriculumRule {
  stage: SchoolStage;
  label: string;
  stageName: string;
  allowedScope: string;
  strictlyBanned: string;
  recommendedPedagogy: string;
}

export const CURRICULUM_MAP: Record<GradeLevel, CurriculumRule> = {
  '초1': {
    stage: 'elementary_lower',
    label: '초등학교 1학년',
    stageName: '초등 저학년',
    allowedScope: '100까지의 수, 가르기와 모으기, 10이 되는 덧셈/뺄셈, 입체모양 직관(상자, 둥근기둥, 공), 시계 보기(정각/30분), 규칙 찾기',
    strictlyBanned: '구구단, 음수, 문자식(x, y), 분수, 나눗셈, 각도 공식',
    recommendedPedagogy: '바둑알, 사과, 수막대 등 구체물 그림(SVG)과 실생활 직관으로만 설명',
  },
  '초2': {
    stage: 'elementary_lower',
    label: '초등학교 2학년',
    stageName: '초등 저학년',
    allowedScope: '세 자리/네 자리 수, 두 자리 수 덧셈/뺄셈(받아올림/내림), 곱셈구구(구구단), 길이(cm, m), 시각과 시간(시/분), 평면도형(삼각형, 사각형, 원의 직관적 구별)',
    strictlyBanned: '나눗셈 공식, 분수 사칙연산, 음수, 방정식(x, y), 각도(도)',
    recommendedPedagogy: '묶어 세기, 수직선 뛰어가기, 타일 배열 그림(SVG) 활용',
  },
  '초3': {
    stage: 'elementary_upper',
    label: '초등학교 3학년',
    stageName: '초등 중·고학년',
    allowedScope: '세 자리 수 덧셈/뺄셈, 곱셈(두/세 자리 × 한/두 자리), 나눗셈 기초(몫과 나머지), 분수 기초(1/n, 진분수/가분수), 소수 기초(0.1단위), 각과 직각, 직각삼각형, 직사각형, 정사각형, 원의 중심/반지름/지름, 길이/시간/들이/무게 단위',
    strictlyBanned: '약수와 배수, 분수 통분, 음수, 문자식(x, y), 피타고라스',
    recommendedPedagogy: '피자/초콜릿 분할 그림(SVG), 컴퍼스 원 그리기, 수직선 분할 활용',
  },
  '초4': {
    stage: 'elementary_upper',
    label: '초등학교 4학년',
    stageName: '초등 중·고학년',
    allowedScope: '큰 수(만, 억, 조), 각도(예각/둔각, 삼각형/사각형 내각의 합), 삼각형 분류(이등변, 정삼각형), 사각형(사다리꼴, 평행사변형, 마름모), 동모분수 덧셈/뺄셈, 소수 덧셈/뺄셈, 꺾은선그래프',
    strictlyBanned: '이분모 분수 통분, 비와 비율, 미지수 x 방정식 공식, 연립방정식',
    recommendedPedagogy: '각도기 측정 그림, 도형 겹치기/돌리기, 동모분수 띠 모델(SVG) 활용',
  },
  '초5': {
    stage: 'elementary_upper',
    label: '초등학교 5학년',
    stageName: '초등 중·고학년',
    allowedScope: '자연수 혼합계산, 약수와 배수(최대공약수/최소공배수), 약분과 통분, 이분모 분수 덧셈/뺄셈, 분수 곱셈, 다각형 둘레와 넓이(직사각형, 평행사변형, 삼각형, 마름모, 사다리꼴), 소수 곱셈, 직육면체/정육면체 겨냥도/전개도, 평균',
    strictlyBanned: '비와 비율, 원의 넓이, 음수, 문자식(x, y), 방정식 이항 공식 (선분도/거꾸로 계산으로 해결할 것)',
    recommendedPedagogy: '도형 쪼개 붙이기(등적변형), 통분 면적 모델, 전개도 접기 그림(SVG) 활용',
  },
  '초6': {
    stage: 'elementary_upper',
    label: '초등학교 6학년',
    stageName: '초등 중·고학년',
    allowedScope: '분수 나눗셈, 소수 나눗셈, 공간과 입체(쌓기나무 위/앞/옆), 비와 비율(비율, 백분율), 비례식과 비례배분, 원의 둘레(원주율 3.14)와 넓이, 입체도형(원기둥, 원뿔, 구) 겉넓이와 부피',
    strictlyBanned: '음수 부호(-), 일차방정식 x 이항 공식(비례식 내항/외항의 곱 또는 비의 성질로 해결)',
    recommendedPedagogy: '비례 배분 바 차트, 원을 무한히 잘라 직사각형 만들기 그림(SVG) 활용',
  },
  '중1': {
    stage: 'middle',
    label: '중학교 1학년',
    stageName: '중등 과정',
    allowedScope: '소인수분해, 정수와 유리수의 사칙연산, 문자와 식(일차식), 일차방정식(이항을 통한 해법), 좌표평면과 그래프(정비례/반비례), 기본도형과 위치관계, 작도와 합동(SSS, SAS, ASA), 평면/입체도형의 성질(다면체, 회전체, 부피/겉넓이), 통계',
    strictlyBanned: '제곱근(√), 무리수, 곱셈공식 전개(x^2), 이차방정식, 피타고라스, 삼각비',
    recommendedPedagogy: '좌표평면 격자점, 평행선 엇각/동위각 증명 작도 그림(SVG) 활용',
  },
  '중2': {
    stage: 'middle',
    label: '중학교 2학년',
    stageName: '중등 과정',
    allowedScope: '유리수와 순환소수, 식의 계산(지수법칙, 단항식/다항식), 일차부등식, 연립일차방정식, 일차함수와 그래프, 일차함수와 일차방정식 관계, 삼각형 성질(이등변, 외심, 내심), 사각형 성질(평행사변형, 직사각형, 마름모, 정사각형, 등변사다리꼴), 도형의 닮음(AA닮음 등)과 피타고라스 정리, 확률',
    strictlyBanned: '제곱근(√), 무리수, 이차방정식 근의 공식, 이차함수 꼭짓점, 삼각비(sin, cos, tan), 원의 성질',
    recommendedPedagogy: '닮음비 선분 비율, 일차함수 기울기와 x/y절편, 피타고라스 정사각형 면적 증명(SVG)',
  },
  '중3': {
    stage: 'middle',
    label: '중학교 3학년',
    stageName: '중등 과정',
    allowedScope: '제곱근과 실수(√a), 다항식의 곱셈공식과 인수분해, 이차방정식(인수분해, 완전제곱식, 근의 공식), 이차함수 기본($y=a(x-p)^2+q$), 삼각비(직각삼각형 sin, cos, tan), 원의 성질(원주각, 접선), 통계(분산, 표준편차)',
    strictlyBanned: '허수(i), 고등 판별식 D 판정 공식화, 삼차방정식, 수1 일반각 삼각함수, 미적분 도함수',
    recommendedPedagogy: '포물선 꼭짓점 이동, 직각삼각형 삼각비 빗변/밑변 비율, 원주각 호의 관계(SVG)',
  },
  '고1': {
    stage: 'high',
    label: '고등학교 1학년',
    stageName: '고등 공통수학',
    allowedScope: '다항식의 연산/항등식/나머지정리, 복소수(i)와 이차방정식, 이차방정식과 이차함수(대칭축, 판별식 D, 제한된 범위의 최대최소), 여러 가지 방정식/부등식, 도형의 방정식(점, 직선, 원, 평행/대칭이동), 집합과 명제, 함수(합성, 역함수, 유리함수, 무리함수), 순열과 조합',
    strictlyBanned: '수1 지수/로그/호도법/수열, 수2 다항함수 미적분(도함수 f\'(x)=0으로 극값 구하기 금지 - 반드시 완전제곱식/기하로 해결)',
    recommendedPedagogy: '포물선 대칭축 구간 분할, 원과 직선의 위치관계 d와 r 비교, 좌표평면 이동(SVG)',
  },
  '고2': {
    stage: 'high',
    label: '고등학교 2학년',
    stageName: '고등 일반선택 (수1·수2)',
    allowedScope: '수학I (지수함수와 로그함수, 삼각함수 호도법/그래프/사인법칙/코사인법칙, 수열의 합 ∑, 귀납법), 수학II (함수의 극한과 연속, 다항함수의 미분법-접선/극대극소/최대최소/방부등식, 다항함수의 적분법-정적분/넓이/속도거리)',
    strictlyBanned: '초월함수(지수/로그/삼각) 미적분, 치환적분/부분적분, 기하 벡터',
    recommendedPedagogy: '다항함수 3차/4차 극대극소 개형, 삼각함수 단위원 단위원 동경 회전, 정적분 넓이 구간 셰이딩(SVG)',
  },
  '고3/N수': {
    stage: 'high',
    label: '고3 / N수 (수능·내신 파이널)',
    stageName: '수능·평가원 킬러/준킬러',
    allowedScope: '고등 전 범위 (공통수학, 수1, 수2, 미적분/기하/확률과 통계) 개념 결합 및 수능 킬러/준킬러 다단계 추론 문항',
    strictlyBanned: '대학 수학 (로피탈 정리 지양 - 교육과정 정의에 입각한 극한 증명 권장)',
    recommendedPedagogy: '수능 킬러 다단계 조건 해석, 도함수 부호 판별 및 삼차/사차함수 비율 관계, 조건부 확률/기하 벡터 도식화(SVG)',
  },
};

export type FailureType = 
  | 'concept'          // [개념 미학습] 해당 학년 공식/정리의 정의를 모름
  | 'modeling'         // [수식 모델링 실패] 조건을 해당 학년 도구로 모델링 못함
  | 'visual'           // [도식화 실패] 해당 학년 수준의 그림/도형/그래프를 그리지 못함
  | 'interpretation';  // [조건 해석 실패] 문제의 제한 조건이나 단어를 간과함

export interface FailureTypeInfo {
  type: FailureType;
  label: string;
  badge: string;
  description: string;
  iconName: string;
  color: string;
}

export const FAILURE_TYPE_MAP: Record<FailureType, FailureTypeInfo> = {
  concept: {
    type: 'concept',
    label: '개념 미학습',
    badge: '개념 부재',
    description: '공식이나 정리의 유도 과정과 정의를 명확히 알지 못함',
    iconName: 'BookOpen',
    color: '#EF4444',
  },
  modeling: {
    type: 'modeling',
    label: '수식 모델링 실패',
    badge: '수식 변환 불가',
    description: '문장 형태의 조건을 해당 학년 도구로 표현하지 못함',
    iconName: 'Sigma',
    color: '#F59E0B',
  },
  visual: {
    type: 'visual',
    label: '도식화 실패',
    badge: '그래프/그림 부재',
    description: '수식이나 조건을 그림/좌표평면/도형으로 시각화하지 못함',
    iconName: 'LineChart',
    color: '#3B82F6',
  },
  interpretation: {
    type: 'interpretation',
    label: '특정 조건/단어 해석 실패',
    badge: '조건 간과',
    description: '자연수/정수 조건, 범위 제한, 접점 등 핵심 단서를 놓침',
    iconName: 'SearchCode',
    color: '#8B5CF6',
  },
};

export interface StepSolution {
  step_number: number;
  title: string;
  latex_content: string;
  explanation: string;
  key_takeaway?: string;
}

export interface SubQuestionSolution {
  sub_id: number;
  sub_title: string;
  question_text: string;
  solution_steps: StepSolution[];
  final_answer: string;
  svg_diagram?: string;
}

export interface MathSolveResponse {
  ocr_text: string;
  concepts: string[];
  step_by_step_solution: StepSolution[];
  answer: string;
  visualization_svg: string;
  decomposed_clauses?: string[];
  is_multi_question?: boolean;
  sub_questions?: SubQuestionSolution[];
}

export interface AdaptiveDiagnosticAlert {
  has_critical_warning: boolean;
  recurring_concept?: string;
  failure_pattern?: FailureType;
  repetition_count: number;
  blunt_feedback_message: string;
  remedy_action_plan: string;
}

export interface WeaknessRecord {
  id: string;
  user_id: string;
  question_id: string;
  failure_type: FailureType;
  missed_keyword: string;
  selected_clause?: string;
  prescription_notes?: string;
  is_resolved?: boolean;
  created_at: string;
}

export interface QuestionRecord {
  id: string;
  user_id: string;
  image_url?: string;
  ocr_text: string;
  concepts_used: string[];
  step_by_step_solution: StepSolution[];
  answer: string;
  visualization_svg?: string;
  created_at: string;
  weakness?: WeaknessRecord;
}

export interface DiagnosticHistoryItem {
  question_id: string;
  ocr_text: string;
  concepts_used: string[];
  failure_type?: FailureType;
  missed_keyword?: string;
  created_at: string;
}

export interface ChatRcaDiagnosis {
  clause: string;
  failure_type: FailureType;
  reason: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  visualization_svg?: string;
  latex_formula?: string;
  key_concept?: string;
  timestamp: string;
  suggested_followups?: string[];
  rca_diagnosis?: ChatRcaDiagnosis;
}
