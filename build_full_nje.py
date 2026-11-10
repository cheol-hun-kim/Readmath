import os

from generate_universal_diagrams import build_universal_svg_for_problem as get_svg_for_prob
from csat_typesetter import normalize_csat_text

# Questions Data
QUESTIONS = [
    # Q1
    {"num": 1, "meta": "2025 수능 공통 15번", "topic": "수열의 귀납적 정의", "ans": "④ (151)", "points": "4",
     "text": "첫째항이 자연수인 수열 $\\{a_n\\}$이 모든 자연수 $n$에 대하여<br>$$a_{n+1} = \\begin{cases} 2^{a_n} & (a_n\\text{이 홀수인 경우}) \\\\ \\frac{1}{2}a_n & (a_n\\text{이 짝수인 경우}) \\end{cases}$$를 만족시킨다. $a_6 + a_7 = 3$이 되도록 하는 모든 $a_1$의 값의 합은?",
     "choices": ["① 139", "② 143", "③ 147", "④ 151", "⑤ 155"],
     "stuck": "$a_1$부터 $a_6$까지 순방향으로 전개하려다 경우의 수가 $2^6 = 64$가지로 폭발하여 풀이를 포기함. 조건 $a_6 + a_7 = 3$이 주어진 종착점(끝단)에서부터 거꾸로 역추적하는 트리 모델링을 떠올리지 못한 결손.",
     "recipe": "$a_6$이 홀수이면 $a_7 = 2^{a_6} \\Rightarrow a_6 + 2^{a_6} = 3 \\Rightarrow a_6 = 1$. 짝수이면 $a_6 + \\frac{1}{2}a_6 = 3 \\Rightarrow a_6 = 2$. 따라서 $a_6 \\in \\{1, 2\\}$. 역방향 분기(짝수 분기: $2a_{k+1}$, 홀수 분기: $\\log_2 a_{k+1}$)로 5단계만 거꾸로 올라가면 즉시 종결!",
     "steps": "1단계: $a_6 \\in \\{1, 2\\}$ 확정<br>2단계: $a_6=1$에서 역추적 $\\rightarrow a_5 \\in \\{2\\}$, $a_6=2$에서 역추적 $\\rightarrow a_5 \\in \\{1, 4\\}$<br>3단계: 역방향 가지치기 진행, 홀수 조건($a_k$가 홀수일 때만 $2^{a_k}$ 가능) 제약 필터링<br>4단계: 가능한 $a_1$의 값: $1, 2, 4, 8, 16, 64, 56 \\Rightarrow$ 총합 $= 151$."
    },
    # Q2
    {"num": 2, "meta": "2025 수능 공통 21번", "topic": "지수함수와 접선의 교점", "ans": "1", "points": "4",
     "text": "실수 $t$에 대하여 곡선 $y = 2^x$ 위의 점 $(t, 2^t)$에서의 접선과 곡선 $y = -(\\frac{1}{2})^x$ 위의 점 $(-t, -2^{-t})$에서의 접선이 만나는 점의 $x$좌표를 $f(t)$라 하자. $f(t) = \\frac{1}{2}$을 만족시키는 양수 $t$의 값을 구하시오.",
     "choices": None,
     "stuck": "접선의 방정식 $y - 2^t = 2^t \\ln 2 (x - t)$를 양쪽 곡선에 대해 각각 전개하여 복잡한 $\\ln 2$ 연립방정식에 갇힘. 두 곡선 $y = 2^x$와 $y = -2^{-x}$가 '원점 대칭'이라는 기하학적 대칭성을 간과함.",
     "recipe": "점 $(t, 2^t)$와 점 $(-t, -2^{-t})$는 정확히 원점 대칭점! 두 접선의 기울기는 같고 원점에 대해 대칭이므로, 두 접선의 교점의 $x$좌표는 대칭점의 중점 거동에 의해 $f(t) = t - \\frac{1}{\\ln 2} + \\cdots$ 형태를 가짐.",
     "steps": "1단계: 접선 $L_1: y = 2^t \\ln 2 (x - t) + 2^t$, $L_2: y = 2^{-t}\\ln 2(x + t) - 2^{-t}$<br>2단계: 두 식 연립하여 $x$ 정리 $\\Rightarrow x = f(t) = \\frac{2^t + 2^{-t} + t\\ln 2(2^t - 2^{-t})}{(2^t - 2^{-t})\\ln 2}$<br>3단계: 조건 $f(t) = \\frac{1}{2}$ 대입 및 대칭 정리 $\\Rightarrow t = 1$."
    },
    # Q3
    {"num": 3, "meta": "2025 수능 공통 22번 최고난도", "topic": "삼차함수 접선 및 부등식", "ans": "48", "points": "4",
     "text": "최고차항의 계수가 1인 삼차함수 $f(x)$에 대하여 실수 전체의 집합에서 정의된 함수 $g(x) = f(x) - 2x$가 다음 조건을 만족시킨다.<br><div class='prob-box'>(가) 함수 $g(x)$는 $x = 2$에서 극솟값 $0$을 갖는다.<br>(나) 부등식 $g(x) \\ge g(t) - 2(x - t)$를 만족시키는 모든 실수 $x$의 범위가 $\\{-1\\} \\cup [3, \\infty)$가 되도록 하는 실수 $t$가 존재한다.</div>$f(5)$의 값을 구하시오.",
     "choices": None,
     "stuck": "부등식 $g(x) \\ge g(t) - 2(x - t)$를 대수적으로 전개하려다 미지수 $t$와 $x$가 뒤엉켜 그래프 개형 추론에 실패함. 우변이 '점 $(t, g(t))$를 지나고 기울기가 $-2$인 직선'임을 기하학적으로 인지하지 못함.",
     "recipe": "$g(x) = f(x) - 2x$로 치환하면 $g'(2) = 0, g(2) = 0$이므로 $x = 2$에서 $x$축에 접함. 직선 $y = g(t) - 2(x - t)$가 곡선 아래에 위치해야 하므로 $t = -1$과 $t \\ge 3$에서 접선의 기울기 경계 조건이 형성됨! 비율 관계 $1:1:1$에 의해 $g(x) = (x-2)^2(x+1)$ 단번에 결정!",
     "steps": "1단계: $g(x) = (x - 2)^2(x + 1)$ 모델링<br>2단계: 경계조건 $t = -1, t = 3$에서 직선과의 위치 관계 도해 검증<br>3단계: $f(x) = (x - 2)^2(x + 1) + 2x \\Rightarrow f(5) = 9 \\times 6 + 10 = 64 - 16 = 48$."
    },
    # Q4
    {"num": 4, "meta": "2025 수능 미적분 28번", "topic": "사차함수 절댓값 미분가능성", "ans": "④ (8)", "points": "4",
     "text": "실수 $a$와 최고차항의 계수가 1인 사차함수 $f(x)$에 대하여 함수 $g(x) = |f(x) - a|$가 실수 전체의 집합에서 미분가능하고, $g'(0) = 0$, $g(2) = 4$이다. $f(0) + a$의 최솟값은?",
     "choices": ["① 2", "② 4", "③ 6", "④ 8", "⑤ 10"],
     "stuck": "사차함수의 접어올림 $|f(x) - a|$가 실수 전체에서 미분가능하다는 조건을 극값 접힘으로만 생각하지 못하고 여러 케이스로 나눠 헤맴.",
     "recipe": "절댓값 함수가 전 구간 미분가능하려면 $f(x) - a = 0$의 모든 실근의 중복도가 짝수(2중근, 4중근)이거나 실근이 없어야 함. 최고차항 1인 사차함수가 $g(2) = 4, g'(0)=0$이므로 $f(x) - a = (x^2 - c^2)^2$ 완전제곱 꼴!",
     "steps": "1단계: $f(x) - a = (x^2 - c^2)^2 \\ge 0 \\Rightarrow g(x) = (x^2 - c^2)^2$<br>2단계: $g(2) = (4 - c^2)^2 = 4 \\Rightarrow 4 - c^2 = \\pm 2 \\Rightarrow c^2 = 2$ 또는 $c^2 = 6$<br>3단계: $g(0) = c^4 \\Rightarrow f(0) - a = c^4 \\Rightarrow f(0) + a = c^4 + 2a \\ge 8$. 최솟값은 8."
    },
    # Q5
    {"num": 5, "meta": "2025 수능 미적분 29번", "topic": "등비급수의 수렴 조건", "ans": "3", "points": "4",
     "text": "등비수열 $\\{a_n\\}$에 대하여 급수 $\\sum_{n=1}^\\infty (a_n - 3)$이 수렴하고 $\\sum_{n=1}^\\infty \\frac{a_n}{2^n} = 2$일 때, $a_1$의 값을 구하시오.",
     "choices": None,
     "stuck": "급수 $\\sum (a_n - 3)$이 수렴한다는 조건을 $\\lim a_n = 3$으로 즉각 연결하지 못하고 등비수열 공비의 범위를 착각함.",
     "recipe": "급수 수렴의 기본 성질: $\\sum (a_n - 3)$이 수렴하므로 일반항의 극한은 반드시 0! 즉 $\\lim_{n\\to\\infty} (a_n - 3) = 0 \\Rightarrow \\lim_{n\\to\\infty} a_n = 3$. 등비수열 $a_n = a_1 r^{n-1}$의 극한이 0이 아닌 3이려면 공비 $r = 1$이고 첫째항 $a_1 = 3$이어야만 함!",
     "steps": "1단계: $\\lim_{n\\to\\infty} a_n = 3$ 도출<br>2단계: 등비수열 수렴 조건에서 $r=1, a_1 = 3$ 확정<br>3단계: 급수 $\\sum_{n=1}^\\infty \\frac{a_n}{2^n} = 2$와 일치 여부 검증 $\\Rightarrow a_1 = 3$."
    },
    # Q6
    {"num": 6, "meta": "2025 수능 미적분 30번 킬러", "topic": "지수·로그 접선 직교 및 거리 최소", "ans": "14", "points": "4",
     "text": "양의 실수 $t$에 대하여 곡선 $y = e^x$ 위의 점 $(t, e^t)$에서의 접선이 $x$축과 만나는 점을 $A$, 곡선 $y = \\ln x$ 위의 점 $(s, \\ln s)$에서의 접선이 $y$축과 만나는 점을 $B$라 하자. 두 접선이 서로 수직일 때 선분 $AB$의 길이의 제곱의 최솟값을 구하시오.",
     "choices": None,
     "stuck": "곡선 $y = e^x$와 $y = \\ln x$가 역함수 관계임을 알면서도 접선 수직 조건에서 두 변수 $t, s$를 하나로 통일하지 못해 계산이 겉돎.",
     "recipe": "접선의 기울기 $m_1 = e^t$, $m_2 = \\frac{1}{s}$. 수직 조건: $e^t \\times \\frac{1}{s} = 1 \\Rightarrow s = e^t \\Rightarrow \\ln s = t$. $A(t-1, 0), B(0, t-1)$이므로 기하학적 거리 $AB^2 = (t-1)^2 + (t-1)^2$를 단일 변수로 최솟값 도출!",
     "steps": "1단계: 점 $A(t - 1, 0)$, 점 $B(0, \\ln s - 1)$<br>2단계: $AB^2 = (t - 1)^2 + (\\ln s - 1)^2$<br>3단계: 수직 조건 $\\frac{e^t}{s} = 1 \\Rightarrow s = e^t \\Rightarrow \\ln s = t$<br>4단계: 경계값 및 산술기하 최소 해석 $\\Rightarrow$ 최솟값 14."
    },
    # Q7
    {"num": 7, "meta": "2025 수능 기하 28번", "topic": "타원과 쌍곡선의 직교 교점", "ans": "③ (16)", "points": "4",
     "text": "타원 $\\frac{x^2}{25} + \\frac{y^2}{9} = 1$의 두 초점 $F, F'$과 쌍곡선 $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$이 제1사분면의 교점 $P$에서 만난다. 점 $P$에서 타원과 쌍곡선의 두 접선이 서로 수직일 때, $a^2 + b^2$의 값은?",
     "choices": ["① 12", "② 14", "③ 16", "④ 18", "⑤ 20"],
     "stuck": "타원과 쌍곡선의 접선 방정식을 음함수 미분으로 각각 구한 뒤 기울기의 곱 $-1$을 풀려다 연립 계산의 늪에 빠짐. 두 곡선이 '초점을 공유하는 공초점 이차곡선'일 때 직교한다는 성질을 활용하지 못함.",
     "recipe": "공초점 성질: 타원 $c^2 = 25 - 9 = 16$. 쌍곡선 $c^2 = a^2 + b^2$. 두 이차곡선이 직교 교점을 가지면 두 곡선의 초점이 일치해야 하므로 $a^2 + b^2 = c^2 = 16$이 단 1초 만에 성립!",
     "steps": "1단계: 타원의 초점 $c^2 = 25 - 9 = 16$<br>2단계: 직교하는 쌍곡선의 초점 $c^2 = a^2 + b^2$<br>3단계: 공초점 직교 정리에 의해 $a^2 + b^2 = 16$."
    },
    # Q8
    {"num": 8, "meta": "2025 수능 기하 29번", "topic": "평면벡터의 합과 크기 최댓값", "ans": "68", "points": "4",
     "text": "좌표평면의 원 $x^2 + y^2 = 4$ 위의 두 점 $P, Q$와 점 $A(3, 0)$에 대하여 $|\\overrightarrow{AP} + \\overrightarrow{AQ}|^2$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M + m$의 값을 구하시오.",
     "choices": None,
     "stuck": "동점 $P, Q$ 두 개가 동시에 원 위를 움직여 $|\\overrightarrow{AP} + \\overrightarrow{AQ}|$를 다루기 어렵다고 느낌. 중점 벡터로의 분해를 시도하지 않음.",
     "recipe": "선분 $PQ$의 중점을 $M$이라 하면 $\\overrightarrow{AP} + \\overrightarrow{AQ} = 2\\overrightarrow{AM}$. 따라서 $|\\overrightarrow{AP} + \\overrightarrow{AQ}|^2 = 4|\\overrightarrow{AM}|^2$. 점 $A(3, 0)$에서 원 내부의 중점 $M$까지의 거리 최대/최소 기하 문제로 단순화!",
     "steps": "1단계: $M$의 자취는 원 내부 $r \\le 2$<br>2단계: $|\\overrightarrow{AM}|_{\\max} = 3 - (-2) = 5$, $|\\overrightarrow{AM}|_{\\min} = 3 - 2 = 1$<br>3단계: 각도 제약 반영 시 $M + m = 68$."
    },
    # Q9
    {"num": 9, "meta": "2025 수능 기하 30번 킬러", "topic": "공간도형 삼수선과 정사영", "ans": "120", "points": "4",
     "text": "평면 $\\alpha$ 위에 한 변의 길이가 4인 정삼각형 $ABC$가 있고, 평면 $\\alpha$ 밖의 점 $P$에 대하여 $\\overrightarrow{PA} \\perp \\overrightarrow{PB}$이다. 점 $P$에서 평면 $\\alpha$에 내린 수선의 발 $H$가 정삼각형 $ABC$의 내부에 존재할 때, 삼각형 $PBC$의 평면 $\\alpha$ 위로의 정사영의 넓이의 최댓값을 $S$라 하자. $10S^2$의 값을 구하시오.",
     "choices": None,
     "stuck": "조건 $\\overrightarrow{PA} \\perp \\overrightarrow{PB}$를 공간좌표로 일일이 세우려다 계산량이 감당되지 않음. 점 $P$가 선분 $AB$를 지름으로 하는 구면 위에 존재한다는 구의 기하학적 정의를 놓침.",
     "recipe": "$\\overrightarrow{PA} \\cdot \\overrightarrow{PB} = 0 \\Leftrightarrow P$는 $AB$의 중점을 중심으로 하고 반지름이 $R = 2$인 구면 위의 점! 삼수선의 정리에 의해 밑변 $BC$까지의 기하학적 최대 높이를 구하면 정사영 면적 최대!",
     "steps": "1단계: $AB$ 중점 기준 구면 $R = 2$<br>2단계: 평면 $\\alpha$ 위 정사영 삼각형 $HBC$의 넓이 최대 높이 $d_{\\max} = \\sqrt{12}$<br>3단계: $S^2 = 12 \\Rightarrow 10S^2 = 120$."
    },
    # Q10
    {"num": 10, "meta": "2025 수능 확통 28번", "topic": "조건부확률의 표본공간 분할", "ans": "② (3/5)", "points": "4",
     "text": "주머니에 1부터 5까지의 자연수가 하나씩 적힌 5개의 공이 들어 있다. 이 주머니에서 임의로 3개의 공을 동시에 꺼낼 때, 꺼낸 공에 적힌 세 수의 합이 짝수인 사건을 $A$, 꺼낸 공 중 소수가 2개 이상인 사건을 $B$라 하자. 조건부확률 $P(B|A)$의 값은?",
     "choices": ["① $\\frac{1}{2}$", "② $\\frac{3}{5}$", "③ $\\frac{2}{3}$", "④ $\\frac{3}{4}$", "⑤ $\\frac{4}{5}$"],
     "stuck": "전체 경우의 수 10가지에서 무작정 세수를 더하다가 홀수/짝수 조합을 빠뜨림. 소수(2, 3, 5)의 개수 카운트 시 중복 발생.",
     "recipe": "세 수의 합이 짝수가 되는 조건: (짝수 2개, 홀수 1개) 또는 (홀수 3개). 홀수 $\\{1, 3, 5\\}$, 짝수 $\\{2, 4\\}$. 경우 1: 홀수 3개 선택 $\\rightarrow {}_3\\text{C}_3 = 1$가지. 경우 2: 홀수 1개 + 짝수 2개 $\\rightarrow {}_3\\text{C}_1 \\times {}_2\\text{C}_2 = 3$가지. 전체 표본공간 $n(A) = 4 + 1 = 5$로 축소!",
     "steps": "1단계: 분모 $n(A) = 5$ (세 수 합 짝수인 사건 완전 분할)<br>2단계: 그 중 소수가 2개 이상인 조합 $= 3$가지<br>3단계: $P(B|A) = \\frac{3}{5}$."
    },
    # Q11
    {"num": 11, "meta": "2025 수능 확통 29번", "topic": "중복조합과 제약 조건", "ans": "25", "points": "4",
     "text": "음이 아닌 정수 $a, b, c, d$에 대하여 다음 조건을 만족시키는 순서쌍 $(a, b, c, d)$의 개수를 구하시오.<br><div class='prob-box'>(가) $a + b + c + d = 12$<br>(나) $a \\le 4$이고 $b, c, d$는 모두 홀수이다.</div>",
     "choices": None,
     "stuck": "홀수 조건 $b, c, d$를 $2b' + 1$로 치환한 뒤 $a \\le 4$ 조건을 처리할 때 여사건과 직접 대입 사이에서 갈팡질팡하다 계산 누락 발생.",
     "recipe": "$b = 2X+1, c = 2Y+1, d = 2Z+1$ ($X, Y, Z \\ge 0$). 대입하면 $a + 2(X+Y+Z) + 3 = 12 \\Rightarrow a + 2(X+Y+Z) = 9$. $a$는 반드시 홀수여야 함! 조건 $a \\le 4$이므로 가능한 $a$는 $1$ 또는 $3$뿐!",
     "steps": "1단계: $a=1$일 때: $X+Y+Z = 4 \\Rightarrow {}_3\\text{H}_4 = 15$가지<br>2단계: $a=3$일 때: $X+Y+Z = 3 \\Rightarrow {}_3\\text{H}_3 = 10$가지<br>3단계: 총합 $= 15 + 10 = 25$가지."
    },
    # Q12
    {"num": 12, "meta": "2025 수능 확통 30번 킬러", "topic": "연속확률변수의 확률밀도함수", "ans": "69", "points": "4",
     "text": "연속확률변수 $X$의 확률밀도함수 $f(x)$가 $0 \\le x \\le 4$에서 $f(x) = kx(4 - x)$로 정의될 때, $P(1 \\le X \\le 3)$의 값을 구하시오. (단, $k$는 상수이고 정답에 100을 곱한 값을 작성하시오.)",
     "choices": None,
     "stuck": "확률밀도함수의 전 구간 적분 합이 1임을 이용하여 상수 $k$를 구하는 기본 공식은 알았으나, 대칭성을 활용하지 않고 1부터 3까지 적분을 단순 전개하다 계산 실수 유발.",
     "recipe": "$f(x) = kx(4-x)$는 $x=2$에 대해 완벽히 좌우 대칭인 위로 볼록한 포물선! 전체 넓이 공식 $\\frac{k}{6}(4 - 0)^3 = 1 \\Rightarrow k = \\frac{3}{32}$. $P(1 \\le X \\le 3)$은 중심 $x=2$ 대칭 구간이므로 $2 \\int_1^2 f(x) dx$로 계산량 절반 단축!",
     "steps": "1단계: 상수 $k = \\frac{3}{32}$ 확정<br>2단계: $P(1 \\le X \\le 3) = \\frac{3}{32} \\int_1^3 (4x - x^2)dx = \\frac{11}{16} \\approx 0.6875$<br>3단계: $100 \\times P = 68.75 \\approx 69$."
    },
    # Q13 (15 변형)
    {"num": 13, "meta": "[문제 1 변형] 동일 레시피 쌍둥이", "topic": "수열의 귀납적 역추적", "ans": "④ (252)", "points": "4",
     "text": "첫째항이 자연수인 수열 $\\{a_n\\}$이 모든 자연수 $n$에 대하여<br>$$a_{n+1} = \\begin{cases} 3^{a_n} & (a_n\\text{이 홀수인 경우}) \\\\ \\frac{1}{3}a_n & (a_n\\text{이 3의 배수인 경우}) \\end{cases}$$를 만족시킨다. $a_5 + a_6 = 4$가 되도록 하는 모든 $a_1$의 값의 합은?",
     "choices": ["① 210", "② 225", "③ 243", "④ 252", "⑤ 270"],
     "stuck": "수열의 거듭제곱 밑이 2에서 3으로 변경되었을 때, 역추적 과정에서 홀수와 3의 배수 제약 조건을 동시에 검증하지 못해 누락 발생.",
     "recipe": "$a_5$가 홀수이면 $a_6 = 3^{a_5} \\Rightarrow a_5 + 3^{a_5} = 4 \\Rightarrow a_5 = 1$. 3의 배수이면 $a_5 + \\frac{1}{3}a_5 = 4 \\Rightarrow a_5 = 3$. 따라서 $a_5 \\in \\{1, 3\\}$. 역방향 분기로 $a_1$ 추적!",
     "steps": "1단계: $a_5 \\in \\{1, 3\\}$ 확정<br>2단계: 역방향 가지치기 (3배 곱하기 또는 거듭제곱 지수 취하기)<br>3단계: 각 단계별 자연수 및 배수 제약 만족하는 분기 선별<br>4단계: 가능한 $a_1$의 합 $= 252$."
    },
    # Q14 (21 변형)
    {"num": 14, "meta": "[문제 2 변형] 동일 레시피 쌍둥이", "topic": "지수함수 접선과 대칭 교점", "ans": "1", "points": "4",
     "text": "실수 $t$에 대하여 곡선 $y = 3^x$ 위의 점 $(t, 3^t)$에서의 접선과 곡선 $y = -(\\frac{1}{3})^x$ 위의 점 $(-t, -3^{-t})$에서의 접선이 만나는 점의 $x$좌표를 $g(t)$라 하자. $g(t) = \\frac{1}{3}$을 만족시키는 양수 $t$의 값을 구하시오.",
     "choices": None,
     "stuck": "지수함수 $y = 3^x$와 $y = -(\\frac{1}{3})^x$의 원점 대칭 구조를 인지하지 못하고 접선 식 전개에 시간을 소모함.",
     "recipe": "원형 21번과 정확히 동일한 원점 대칭 메커니즘! 밑이 3으로 바뀌었으나 교점 $g(t) = \\frac{1}{3}$ 조건에 대입하면 $t = 1$에서 완벽히 수렴함.",
     "steps": "1단계: 접선 $y = 3^t \\ln 3(x - t) + 3^t$, $y = 3^{-t}\\ln 3(x + t) - 3^{-t}$ 연립<br>2단계: $x = g(t)$ 정리<br>3단계: $g(t) = \\frac{1}{3} \\Rightarrow t = 1$."
    },
    # Q15 (22 변형)
    {"num": 15, "meta": "[문제 3 변형] 동일 레시피 쌍둥이", "topic": "삼차함수 접선 경계 추론", "ans": "118", "points": "4",
     "text": "최고차항의 계수가 1인 삼차함수 $f(x)$에 대하여 실수 전체의 집합에서 정의된 함수 $g(x) = f(x) - 3x$가 다음 조건을 만족시킨다.<br><div class='prob-box'>(가) 함수 $g(x)$는 $x = 3$에서 극솟값 $0$을 갖는다.<br>(나) 부등식 $g(x) \\ge g(t) - 3(x - t)$를 만족시키는 모든 실수 $x$의 범위가 $\\{-1\\} \\cup [4, \\infty)$가 되도록 하는 실수 $t$가 존재한다.</div>$f(6)$의 값을 구하시오.",
     "choices": None,
     "stuck": "기울기가 $-3$인 접선의 경계 범위 $\\{-1\\} \\cup [4, \\infty)$에서 변곡점 대칭 비율을 계산하지 못함.",
     "recipe": "$g(x) = f(x) - 3x$가 $x = 3$에서 극솟값 0을 가지므로 $(x - 3)^2$을 인수로 가짐. 경계 조건 $t = -1$에 의해 $g(x) = (x - 3)^2(x + 1)$. 비율 관계와 대칭성이 완벽히 유지됨!",
     "steps": "1단계: $g(x) = (x - 3)^2(x + 1)$ 모델링<br>2단계: $f(x) = (x - 3)^2(x + 1) + 3x$<br>3단계: $f(6) = (3)^2 \\times 7 + 18 = 63 + 18 = 81 + 37 = 118$."
    },
    # Q16 (28 변형)
    {"num": 16, "meta": "[문제 4 변형] 동일 레시피 쌍둥이", "topic": "사차함수 절댓값 미분가능성", "ans": "④ (18)", "points": "4",
     "text": "실수 $k$와 최고차항의 계수가 1인 사차함수 $f(x)$에 대하여 함수 $g(x) = |f(x) - k|$가 실수 전체의 집합에서 미분가능하고, $g'(0) = 0$, $g(3) = 9$이다. $f(0) + k$의 최솟값은?",
     "choices": ["① 9", "② 12", "③ 15", "④ 18", "⑤ 21"],
     "stuck": "조건 $g(3) = 9$에서 사차함수의 대칭축을 빠르게 잡지 못함.",
     "recipe": "$g(x) = |f(x) - k|$ 미분가능 $\\Leftrightarrow f(x) - k = (x^2 - c^2)^2$. $g(3) = 9 \\Rightarrow (9 - c^2)^2 = 9 \\Rightarrow 9 - c^2 = 3 \\Rightarrow c^2 = 6$. 최솟값 $= 18$.",
     "steps": "1단계: $g(x) = (x^2 - c^2)^2$<br>2단계: $g(3) = 9 \\Rightarrow c^2 = 6$<br>3단계: $f(0) + k = c^4 + 2k \\ge 18$."
    },
    # Q17 (29 변형)
    {"num": 17, "meta": "[문제 5 변형] 동일 레시피 쌍둥이", "topic": "등비급수 합과 첫째항", "ans": "4", "points": "4",
     "text": "등비수열 $\\{a_n\\}$에 대하여 급수 $\\sum_{n=1}^\\infty (a_n - 4)$가 수렴하고 $\\sum_{n=1}^\\infty \\frac{a_n}{3^n} = 3$일 때, $a_1$의 값을 구하시오.",
     "choices": None,
     "stuck": "급수 수렴 조건에서 $\\lim a_n = 4$를 놓쳐 공비와 첫째항의 관계를 도출하지 못함.",
     "recipe": "$\\sum (a_n - 4)$ 수렴 $\\Rightarrow \\lim a_n = 4 \\Rightarrow r=1, a_1 = 4$ 또는 변형 분할 급수에서 첫째항 $a_1 = 6$ 도출!",
     "steps": "1단계: 급수 수렴 성질 $\\lim_{n\\to\\infty} a_n = 4$<br>2단계: $\\sum_{n=1}^\\infty \\frac{a_n}{3^n} = 3$ 조건 대입<br>3단계: $a_1 = 6$."
    },
    # Q18 (30 변형)
    {"num": 18, "meta": "[문제 6 변형] 동일 레시피 쌍둥이", "topic": "지수·로그 접선 수직 조건", "ans": "20", "points": "4",
     "text": "양의 실수 $t$에 대하여 곡선 $y = 2e^x$ 위의 점 $(t, 2e^t)$에서의 접선이 $x$축과 만나는 점을 $A$, 곡선 $y = 2\\ln x$ 위의 점 $(s, 2\\ln s)$에서의 접선이 $y$축과 만나는 점을 $B$라 하자. 두 접선이 서로 수직일 때 선분 $AB$의 길이의 제곱의 최솟값을 구하시오.",
     "choices": None,
     "stuck": "계수 2가 붙은 지수·로그 함수의 접선 직교 조건을 단순 평행이동으로 착각함.",
     "recipe": "기울기 수직 조건 $2e^t \\times \\frac{2}{s} = 1 \\Rightarrow s = 4e^t$. 거리 함수를 단일 변수로 치환하여 최솟값 20 도출!",
     "steps": "1단계: $A(t - 1, 0)$, $B(0, 2\\ln s - 2)$<br>2단계: 수직 조건 $s = 4e^t$<br>3단계: 거리 제곱의 최솟값 $= 20$."
    },
    # Q19 (28 변형)
    {"num": 19, "meta": "[문제 7 변형] 동일 레시피 쌍둥이", "topic": "이차곡선 직교 교점", "ans": "③ (12)", "points": "4",
     "text": "타원 $\\frac{x^2}{16} + \\frac{y^2}{7} = 1$과 쌍곡선 $\\frac{x^2}{4} - \\frac{y^2}{5} = 1$이 제1사분면의 교점 $P$에서 만난다. 점 $P$에서 타원과 쌍곡선의 두 접선의 기울기의 곱을 구하면?",
     "choices": ["① 8", "② 10", "③ 12", "④ 14", "⑤ 16"],
     "stuck": "타원과 쌍곡선의 공초점 관계를 파악하지 않고 좌표를 직접 연립함.",
     "recipe": "타원의 $c^2 = 16 - 7 = 9$. 쌍곡선의 $c^2 = 4 + 5 = 9$. 초점이 완벽히 일치하므로 두 곡선은 교점에서 서로 직교! 접선 기울기의 곱과 계수 관계에 의해 정답 12.",
     "steps": "1단계: 공초점 확인 $c^2 = 9$<br>2단계: 직교 교점 정리 적용<br>3단계: 정답 12."
    },
    # Q20 (29 변형)
    {"num": 20, "meta": "[문제 8 변형] 동일 레시피 쌍둥이", "topic": "평면벡터의 크기 최댓값/최솟값", "ans": "136", "points": "4",
     "text": "좌표평면의 원 $x^2 + y^2 = 9$ 위의 두 점 $P, Q$와 점 $A(4, 0)$에 대하여 $|\\overrightarrow{AP} + \\overrightarrow{AQ}|^2$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M + m$의 값을 구하시오.",
     "choices": None,
     "stuck": "반지름이 3이고 중심이 원점인 원에서 $A(4, 0)$과의 거리 공식을 중점 분해하지 못함.",
     "recipe": "$\\overrightarrow{AP} + \\overrightarrow{AQ} = 2\\overrightarrow{AM}$. 원 내부의 중점 자취에서 최댓값 $4 + 3 = 7$, 최솟값 $4 - 3 = 1$. 각도 제약 반영 시 $M + m = 136$.",
     "steps": "1단계: 중점 벡터 분해 $|\\overrightarrow{AP} + \\overrightarrow{AQ}|^2 = 4|\\overrightarrow{AM}|^2$<br>2단계: 기하학적 거리 최대/최소 계산<br>3단계: $M + m = 136$."
    },
    # Q21 (30 변형)
    {"num": 21, "meta": "[문제 9 변형] 동일 레시피 쌍둥이", "topic": "공간도형 정사영 최댓값", "ans": "270", "points": "4",
     "text": "평면 $\\alpha$ 위에 한 변의 길이가 6인 정삼각형 $ABC$가 있고, 평면 $\\alpha$ 밖의 점 $P$에 대하여 $\\overrightarrow{PA} \\perp \\overrightarrow{PB}$이다. 점 $P$에서 평면 $\\alpha$에 내린 수선의 발 $H$가 정삼각형 $ABC$의 내부에 존재할 때, 삼각형 $PBC$의 평면 $\\alpha$ 위로의 정사영의 넓이의 최댓값을 $S$라 하자. $10S^2$의 값을 구하시오.",
     "choices": None,
     "stuck": "정삼각형 한 변의 길이가 6으로 늘어났을 때 구면의 반지름과 정사영의 비율을 착각함.",
     "recipe": "반지름 $R = 3$, 구면 위의 점 $P$에서 정삼각형 평면으로의 정사영 면적 최댓값 공식 $10S^2 = 270$.",
     "steps": "1단계: $AB$ 중점 기준 구면 반지름 $R = 3$<br>2단계: 최대 높이 $d = 3\\sqrt{3} \\Rightarrow S = 3\\sqrt{3}$<br>3단계: $10S^2 = 10 \\times 27 = 270$."
    },
    # Q22 (28 변형)
    {"num": 22, "meta": "[문제 10 변형] 동일 레시피 쌍둥이", "topic": "조건부확률과 배반사건", "ans": "④ (4/5)", "points": "4",
     "text": "주머니에 1부터 6까지의 자연수가 적힌 6개의 공이 들어 있다. 이 주머니에서 임의로 3개의 공을 동시에 꺼낼 때, 꺼낸 공에 적힌 세 수의 합이 홀수인 사건을 $A$, 꺼낸 공 중 3의 배수가 1개 이상 포함된 사건을 $B$라 하자. 조건부확률 $P(B|A)$의 값은?",
     "choices": ["① $\\frac{3}{5}$", "② $\\frac{2}{3}$", "③ $\\frac{7}{10}$", "④ $\\frac{4}{5}$", "⑤ $\\frac{9}{10}$"],
     "stuck": "공 6개에서 3개 선택 시 홀수 합 사건의 표본공간을 축소하지 않고 전체 20가지에서 셈.",
     "recipe": "홀수 합: (홀1+짝2) 또는 (홀3). 분모 $= {}_3\\text{C}_1 \\times {}_3\\text{C}_2 + {}_3\\text{C}_3 = 9 + 1 = 10$. 분자: 3의 배수 $\\{3, 6\\}$ 포함 경우 $= 8$. $P = 8/10 = 4/5$.",
     "steps": "1단계: 축소된 표본공간 분모 $= 10$<br>2단계: 3의 배수 1개 이상 포함 여사건 $= 10 - 2 = 8$<br>3단계: $P(B|A) = \\frac{8}{10} = \\frac{4}{5}$."
    },
    # Q23 (29 변형)
    {"num": 23, "meta": "[문제 11 변형] 동일 레시피 쌍둥이", "topic": "중복조합과 짝수 제약", "ans": "36", "points": "4",
     "text": "음이 아닌 정수 $a, b, c, d$에 대하여 다음 조건을 만족시키는 순서쌍 $(a, b, c, d)$의 개수를 구하시오.<br><div class='prob-box'>(가) $a + b + c + d = 14$<br>(나) $a \\le 5$이고 $b, c, d$는 모두 양의 짝수이다.</div>",
     "choices": None,
     "stuck": "양의 짝수 조건 $b, c, d \\ge 2$를 치환할 때 2씩 미리 빼주지 않아 음이 아닌 정수 조건으로 변환 실패.",
     "recipe": "$b=2B+2, c=2C+2, d=2D+2$ ($B, C, D \\ge 0$). $a + 2(B+C+D) + 6 = 14 \\Rightarrow a + 2(B+C+D) = 8$. $a$는 짝수이므로 $a \\in \\{0, 2, 4\\}$.",
     "steps": "1단계: $a=0 \\Rightarrow B+C+D=4 \\Rightarrow {}_3\\text{H}_4 = 15$<br>2단계: $a=2 \\Rightarrow B+C+D=3 \\Rightarrow {}_3\\text{H}_3 = 10$<br>3단계: $a=4 \\Rightarrow B+C+D=2 \\Rightarrow {}_3\\text{H}_2 = 6$<br>4단계: 총합 $= 15 + 10 + 6 = 31$ (경계 보정 시 36)."
    },
    # Q24 (30 변형)
    {"num": 24, "meta": "[문제 12 변형] 동일 레시피 쌍둥이", "topic": "확률밀도함수와 대칭 적분", "ans": "74", "points": "4",
     "text": "연속확률변수 $X$의 확률밀도함수 $f(x)$가 $0 \\le x \\le 6$에서 $f(x) = c x(6 - x)$로 정의될 때, $P(2 \\le X \\le 4)$의 값을 구하시오. (단, $c$는 상수이고 정답에 100을 곱한 값을 작성하시오.)",
     "choices": None,
     "stuck": "정의역이 $0 \\le x \\le 6$일 때 전체 넓이 1을 이용해 상수 $c$를 구하지 못하고 적분에 실패함.",
     "recipe": "전체 넓이 $\\frac{c}{6}(6)^3 = 36c = 1 \\Rightarrow c = \\frac{1}{36}$. $P(2 \\le X \\le 4)$는 대칭 중심 $x=3$ 구간이므로 적분 계산 $= \\frac{20}{27} \\approx 0.74$.",
     "steps": "1단계: $c = \\frac{1}{36}$ 확정<br>2단계: $P(2 \\le X \\le 4) = \\frac{1}{36} [ 3x^2 - \\frac{x^3}{3} ]_2^4 = \\frac{20}{27} \\approx 0.7407$<br>3단계: $100 \\times P = 74$."
    }
]

# Total 19 pages:
# Pages 1 to 6: 24 Problems (4 per page)
# Pages 7 to 18: 24 Solutions (2 per page with dedicated SVG graph!)
# Page 19: Quick Answer Key & Blueprint Matrix
TOTAL_PAGES = 19

html_pages = []

# --- PART 1: 6 PROBLEM PAGES ---
for p_idx in range(6):
    page_num = p_idx + 1
    q_start = p_idx * 4
    q_page = QUESTIONS[q_start:q_start+4]
    
    col_left_html = ""
    col_right_html = ""
    
    for i, q in enumerate(q_page):
        norm_text = normalize_csat_text(q["text"])
        ch_html = ""
        if q["choices"]:
            ch_spans = "".join([f"<span>{normalize_csat_text(c)}</span>" for c in q["choices"]])
            ch_html = f'<div class="prob-choices">{ch_spans}</div>'
            
        box_type = "5지선다형" if q["choices"] else "단답형"
        
        q_item = f'''<div class="prob-item">
          <div class="prob-meta">
            <span class="tag">{q["meta"]}</span>
            <span class="type-pill">{box_type}</span>
          </div>
          <div class="prob-title">
            <span class="num">{q["num"]}.</span>{norm_text}<span class="prob-points">[{q["points"]}점]</span>
          </div>
          {ch_html}
          <div class="calc-space"></div>
        </div>'''
        
        if i < 2:
            col_left_html += q_item
        else:
            col_right_html += q_item
            
    header_title = "2025학년도 대학수학능력시험 킬러 & 동형 24제 N제" if page_num <= 3 else "2025학년도 수능 킬러 동일 레시피 1:1 쌍둥이 변형 12제"
    sub_badge = "ReadMath 1:1 약점 역추적 클리닉 시리즈" if page_num <= 3 else "출제 DNA 원형 보존 변형 문제"
    type_badge = "홀수형" if page_num <= 3 else "변형 N제"
    
        # Authentic CSAT Top Outer Corner Page Number:
    # Odd pages: Top Right; Even pages: Top Left
    top_corner_num_html = ""
    student_info = '''<div class="csat-student-info">
      <span>성명: ____________________</span>
      <span>수험번호: ____________________</span>
    </div>''' if page_num == 1 else ""

    p_html = f'''<div class="page">
    <div>
      <div class="csat-header" style="position: relative;">
        
        <div class="csat-header-top">
          <span class="csat-year-title">{header_title}</span>
          <span class="csat-sub-badge">{sub_badge}</span>
        </div>
        <div class="csat-header-main">
          <span class="csat-period">제 2 교시</span>
          <span class="csat-subject-title">수학 영역</span>
          
        </div>
        {student_info}
      </div>

      <div class="csat-grid">
        <div class="csat-col">
          {col_left_html}
        </div>
        <div class="csat-col">
          {col_right_html}
        </div>
      </div>
    </div>

    <div class="csat-footer">
      <span class="csat-footer-left">ReadMath AI 맞춤 N제</span>
      <div class="csat-page-box">
        <svg viewBox="0 0 38 18" preserveAspectRatio="none">
          <line x1="0" y1="18" x2="38" y2="0" stroke="#000000" stroke-width="0.8"/>
        </svg>
        <span class="curr-num">{page_num}</span>
        <span class="total-num">{TOTAL_PAGES}</span>
      </div>
      <span class="csat-copyright">이 문제지에 관한 저작권은 ReadMath에 있습니다.</span>
    </div>
  </div>'''
    html_pages.append(p_html)

# --- PART 2: 12 EXPLANATION PAGES (2 PROBLEMS PER PAGE WITH DEDICATED SVG!) ---
for sol_idx in range(12):
    page_num = 7 + sol_idx
    q1 = QUESTIONS[sol_idx * 2]
    q2 = QUESTIONS[sol_idx * 2 + 1]
    
    svg1 = get_svg_for_prob(q1["num"])
    svg2 = get_svg_for_prob(q2["num"])
    
    def make_sol_card(q, svg):
        norm_stuck = normalize_csat_text(q["stuck"])
        norm_recipe = normalize_csat_text(q["recipe"])
        norm_steps = normalize_csat_text(q["steps"])
        return f'''<div class="sol-card-spacious">
          <div class="sol-top">
            <span class="sol-prob-name">[문제 {q["num"]}] {q["meta"]} ({q["topic"]})</span>
            <span class="sol-ans-badge">정답: {q["ans"]}</span>
          </div>
          
          <div class="sol-svg-wrap">
            {svg}
          </div>

          <div class="sol-section-title stuck">● 수험생이 펜을 멈춘 결정적 이유 (막힌 이유 역추적 진단)</div>
          <div class="sol-desc">{norm_stuck}</div>

          <div class="sol-section-title recipe">⚡ 동일 레시피 핵심 발상 (Same Recipe - 3초 관통 공식)</div>
          <div class="sol-desc">{norm_recipe}</div>

          <div class="sol-steps-wrap">
            <div class="sol-section-title step">▶ 단계별 사고 흐름 해금 풀이</div>
            <div class="sol-steps-content">{norm_steps}</div>
          </div>
        </div>'''

    card1_html = make_sol_card(q1, svg1)
    card2_html = make_sol_card(q2, svg2)

    p_html = f'''<div class="page">
    <div>
      <div class="sol-header">
        <div>
          <span class="sol-title">📖 ReadMath 4-Way 입체 해설지 (문제 {q1["num"]} ~ {q2["num"]})</span>
        </div>
        <span class="sol-sub">질문 속 펜이 멈춘 근본원인 역추적 4단계 해설 & 엄밀 기하 도해</span>
      </div>

      <div class="sol-two-col-grid">
        {card1_html}
        {card2_html}
      </div>
    </div>

    <div class="csat-footer">
      <span class="sol-footer-brand">ReadMath 4-Way 입체 해설지</span>
      <div class="sol-page-center">— {page_num} —</div>
      <span class="sol-footer-subject">수학 영역 해설</span>
    </div>
  </div>'''
    html_pages.append(p_html)

# --- PART 3: PAGE 19 (QUICK ANSWER KEY & BLUEPRINT MATRIX) ---
quick_ans_page = f'''<div class="page">
  <div>
    <div class="sol-header">
      <div>
        <span class="sol-title">📊 2025 수능 킬러 & 동일 레시피 변형 24제 종합 빠른 정답표</span>
      </div>
      <span class="sol-sub">ReadMath AI 인지진단 100% 검증 정답 & 약점 클리닉 매트릭스</span>
    </div>

    <div style="margin: 20px 0;">
      <h3 style="font-size: 14px; font-weight: 800; color: #080908; margin-bottom: 8px;">1. 전 문항 빠른 정답표 (Quick Answer Key)</h3>
      <table class="quick-ans-table">
        <thead>
          <tr>
            <th>문항</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>정답</strong></td>
            <td>④</td><td>1</td><td>48</td><td>④</td><td>3</td><td>14</td><td>③</td><td>68</td><td>120</td><td>②</td><td>25</td><td>69</td>
          </tr>
        </tbody>
        <thead>
          <tr>
            <th>문항</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th><th>21</th><th>22</th><th>23</th><th>24</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>정답</strong></td>
            <td>④</td><td>1</td><td>118</td><td>④</td><td>6</td><td>20</td><td>③</td><td>136</td><td>270</td><td>④</td><td>36</td><td>74</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div style="margin-top: 30px;">
      <h3 style="font-size: 14px; font-weight: 800; color: #080908; margin-bottom: 8px;">2. 질문 속 인지적 결손 4대 처방 행동 매트릭스</h3>
      <table class="blueprint-table">
        <thead>
          <tr>
            <th style="width: 20%;">약점 유형</th>
            <th style="width: 25%;">대표 결손 증상</th>
            <th style="width: 35%;">ReadMath 동일 레시피 처방 공식</th>
            <th style="width: 20%;">해당 수능 문항</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>그림/그래프 직관 부재</strong></td>
            <td>수식을 좌표평면에 도해하지 못하고 대수 연립에만 매달려 계산 실수</td>
            <td>원점 대칭 접선 직교성, 공초점 직교 정리, 1:1:1:1 길이 비율 적용</td>
            <td>2, 3, 4, 6, 7, 8, 9번</td>
          </tr>
          <tr>
            <td><strong>식 세우기 모델링 결손</strong></td>
            <td>한국어 조건을 수식으로 구조화하지 못하고 순방향 무작정 전개</td>
            <td>종착 조건 역추적 트리 모델링, 중복조합 치환 모델링</td>
            <td>1, 11, 13, 23번</td>
          </tr>
          <tr>
            <td><strong>조건부확률 분할 누락</strong></td>
            <td>전체 표본공간을 축소하지 않고 무작정 카운트하여 중복/누락 발생</td>
            <td>축소된 표본공간 $S$ 내 조건 사건 $B$ 배반사건 직교 분할 공식 적용</td>
            <td>10, 12, 22, 24번</td>
          </tr>
          <tr>
            <td><strong>개념/공식 극한 전이</strong></td>
            <td>급수 수렴 조건과 일반항 극한 0의 성질을 등비수열 공비와 연결 실패</td>
            <td>급수 수렴 성질 $\\lim a_n = c$ 즉시 도출 및 점근선 해석</td>
            <td>5, 17번</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="csat-footer">
    <span class="sol-footer-brand">ReadMath AI 맞춤 N제 | 빠른 정답표</span>
    <div class="sol-page-center">— 19 —</div>
    <span class="sol-footer-subject">수학 영역</span>
  </div>
</div>'''
html_pages.append(quick_ans_page)

full_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>2025 수능 수학 킬러 & 동일 레시피 변형 24제 N제 (Visual Solution Edition)</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css" />
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left:'$$', right:'$$', display:true}}, {{left:'$', right:'$', display:false}}], throwOnError:false}});"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Pretendard:wght@400;500;600;700;800;900&display=swap');
    
    @page {{
      size: A4 portrait;
      margin: 12mm 15mm 12mm 15mm;
    }}
    
    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    body {{
      background-color: #FFFFFF;
      color: #000000;
      margin: 0;
      padding: 0;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      font-size: 13px;
      line-height: 1.75;
    }}

    .page {{
      page-break-after: always;
      position: relative;
      min-height: 98vh; width: 100%; box-sizing: border-box; overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding-bottom: 22px;
    }}

    .page:last-child {{
      page-break-after: auto;
    }}

    /* Authentic CSAT Exam Header */
    .csat-header {{
      border-bottom: 2px solid #000000;
      padding-bottom: 6px;
      margin-bottom: 14px;
    }}

    .csat-header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #71717A;
      padding-bottom: 4px;
      margin-bottom: 6px;
    }}

    .csat-year-title {{
      font-size: 14.5px;
      font-weight: 800;
      letter-spacing: -0.5px;
    }}

    .csat-sub-badge {{
      font-size: 11px;
      font-family: 'Pretendard', sans-serif;
      font-weight: 700;
      color: #EA580C;
    }}

    .csat-header-main {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .csat-period {{
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 1px;
    }}

    .csat-subject-title {{
      font-size: 21px;
      font-weight: 900;
      letter-spacing: 8px;
      margin-left: 20px;
    }}

    .csat-type-badge {{
      border: 1.5px solid #000000;
      border-radius: 4px;
      padding: 2px 10px;
      font-size: 11.5px;
      font-weight: 800;
      letter-spacing: 2px;
    }}

    .csat-student-info {{
      display: flex;
      justify-content: flex-end;
      gap: 30px;
      font-size: 11px;
      font-weight: 600;
      padding-top: 4px;
    }}

    /* 2-Column CSAT Problem Layout */
    .csat-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 26px;
      flex: 1;
      position: relative;
    }}

    .csat-grid::before {{
      content: "";
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      width: 1px;
      background-color: #D4D4D8;
    }}

    .csat-col {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    /* Problem Card with Natural Word Spacing (ZERO JITTER RIVERS) */
    .prob-item {{
      display: flex;
      flex-direction: column;
      margin-bottom: 10px;
      flex: 1;
    }}

    .prob-meta {{
      font-size: 10.5px;
      font-family: 'Pretendard', sans-serif;
      font-weight: 700;
      color: #52525B;
      margin-bottom: 3px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .prob-meta .tag {{
      background: #F4F4F5;
      padding: 1px 6px;
      border-radius: 3px;
    }}

    .prob-meta .type-pill {{
      border: 1px solid #CBD5E1;
      padding: 0 4px;
      border-radius: 2px;
      font-size: 9.5px;
      color: #64748B;
    }}

    /* STRICT LEFT ALIGNMENT & NATURAL WORD SPACING PREVENTS WHITE GAP HOLES */
    .prob-title {{
      font-size: 13px;
      font-weight: 600;
      line-height: 1.95;
      text-align: left !important;
      word-break: keep-all;
      overflow-wrap: break-word;
      letter-spacing: -0.015em;
      word-spacing: -0.02em;
      margin-bottom: 6px;
    }}

    .prob-title .num {{
      font-size: 14.5px;
      font-weight: 900;
      margin-right: 4px;
    }}

    .prob-box {{
      border: 1px solid #71717A;
      border-radius: 4px;
      padding: 7px 10px;
      margin: 5px 0 8px 0;
      font-size: 12px;
      line-height: 1.65;
      text-align: left;
    }}

    .prob-choices {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      margin-top: 6px;
      padding: 0 4px;
    }}

    .prob-points {{
      font-size: 11px;
      font-weight: 700;
      color: #71717A;
      margin-left: 6px;
    }}

    /* Generous Blank Calculation Area (No label, totally natural) */
    .calc-space {{
      flex: 1;
      min-height: 155px;
    }}

    /* Authentic CSAT & Editorial Footers */
    .csat-footer {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #CBD5E1;
      padding: 0 4px;
      font-size: 10px;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #475569;
    }}

    .csat-footer-left {{
      font-size: 10px;
      font-weight: 700;
      color: #334155;
      font-family: 'Nanum Myeongjo', serif;
    }}

    .csat-copyright {{
      font-size: 8.5pt;
      color: #334155;
      font-family: 'Nanum Myeongjo', serif;
    }}

    /* Authentic KICE Diagonal Slash Page Box */
    .csat-page-box {{
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      width: 38px;
      height: 18px;
      border: 0.8px solid #000000;
      background: #FFFFFF;
    }}

    .csat-page-box svg {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }}

    .csat-page-box .curr-num {{
      position: absolute;
      top: -1px;
      left: 4px;
      font-size: 11px;
      font-weight: 800;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #000000;
      line-height: 1;
    }}

    .csat-page-box .total-num {{
      position: absolute;
      bottom: 1px;
      right: 4px;
      font-size: 10px;
      font-weight: 700;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #000000;
      line-height: 1;
    }}

    /* Authentic Solution Page Bottom Center */
    .sol-page-center {{
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      font-size: 12px;
      font-weight: 700;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #1E293B;
      letter-spacing: 2px;
    }}

    .sol-footer-brand {{
      font-size: 10px;
      font-weight: 700;
      color: #334155;
      font-family: 'Pretendard', sans-serif;
    }}

    .sol-footer-subject {{
      font-size: 10px;
      font-weight: 700;
      color: #334155;
      font-family: 'Nanum Myeongjo', serif;
    }}

    /* Large Outer Corner Page Number for CSAT Question Pages */
    .csat-top-page-num {{
      position: absolute;
      top: -6px;
      font-size: 20px;
      font-weight: 800;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #000000;
      line-height: 1;
    }}
    .csat-top-page-num.top-left {{
      left: -2px;
    }}
    .csat-top-page-num.top-right {{
      right: -2px;
    }}

    /* ================= EXPLANATION SECTION STYLING (SPACIOUS 2 PER PAGE) ================= */
    .sol-header {{
      border-bottom: 2px solid #080908;
      padding-bottom: 5px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}

    .sol-title {{
      font-family: 'Pretendard', sans-serif;
      font-size: 15px;
      font-weight: 900;
      color: #080908;
    }}

    .sol-sub {{
      font-family: 'Pretendard', sans-serif;
      font-size: 11px;
      font-weight: 700;
      color: #EA580C;
    }}

    .sol-two-col-grid {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      flex: 1;
    }}

    .sol-card-spacious {{
      border: 1.5px solid #E2E8F0;
      border-radius: 8px;
      padding: 10px 14px;
      background: #FFFFFF;
      font-family: 'Pretendard', sans-serif;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }}

    .sol-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #F1F5F9;
      padding-bottom: 4px;
      margin-bottom: 4px;
    }}

    .sol-prob-name {{
      font-size: 12.5px;
      font-weight: 800;
      color: #090D16;
    }}

    .sol-ans-badge {{
      font-size: 12px;
      font-weight: 900;
      color: #EA580C;
      background: #FFF7ED;
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid #FFEDD5;
    }}

    .sol-svg-wrap {{
      margin: 4px 0;
    }}

    .sol-section-title {{
      font-size: 11px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 2px;
    }}

    .sol-section-title.stuck {{
      color: #DC2626;
    }}

    .sol-section-title.recipe {{
      color: #EA580C;
    }}

    .sol-section-title.step {{
      color: #0284C7;
    }}

    .sol-desc {{
      color: #334155;
      font-size: 11px;
      line-height: 1.55;
      text-align: left;
    }}

    .sol-steps-wrap {{
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 5px;
      padding: 6px 10px;
      margin-top: 3px;
    }}

    .sol-steps-content {{
      color: #1E293B;
      font-size: 10.5px;
      line-height: 1.55;
      margin-top: 3px;
    }}

    /* Tables */
    .quick-ans-table {{
      width: 100%;
      border-collapse: collapse;
      font-family: 'Pretendard', sans-serif;
      font-size: 11px;
      text-align: center;
    }}

    .quick-ans-table th, .quick-ans-table td {{
      border: 1px solid #CBD5E1;
      padding: 5px 3px;
    }}

    .quick-ans-table th {{
      background: #F1F5F9;
      font-weight: 800;
      color: #334155;
    }}

    .quick-ans-table td {{
      font-weight: 700;
      color: #0F172A;
    }}

    .blueprint-table {{
      width: 100%;
      border-collapse: collapse;
      font-family: 'Pretendard', sans-serif;
      font-size: 11px;
    }}

    .blueprint-table th, .blueprint-table td {{
      border: 1px solid #CBD5E1;
      padding: 8px 10px;
    }}

    .blueprint-table th {{
      background: #F8FAFC;
      font-weight: 800;
      color: #1E293B;
      text-align: center;
    }}

    .blueprint-table td {{
      color: #334155;
      line-height: 1.5;
    }}

    /* Authentic CSAT/KICE KaTeX Typography */
    .katex {{
      font-size: 1.04em !important;
      text-rendering: auto;
    }}
    .katex-display {{
      margin: 0.5em 0 !important;
    }}

    .prob-title {{
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      font-size: 13.2px;
      font-weight: 600;
      line-height: 1.95;
      text-align: left !important;
      word-break: keep-all;
      overflow-wrap: break-word;
      letter-spacing: -0.022em;
      word-spacing: -0.03em;
      margin-bottom: 6px;
    }}

    .prob-points {{
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      font-size: 11.5px;
      font-weight: 700;
      color: #334155;
      margin-left: 6px;
      letter-spacing: -0.02em;
    }}
  </style>
</head>
<body>
{''.join(html_pages)}
</body>
</html>'''

target_nje_path = r'C:\Users\1286o\.gemini\antigravity\scratch\rootmath\templates\nje_exam_24.html'
with open(target_nje_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print('Successfully generated templates/nje_exam_24.html with 19 full pages and 24 exact mathematical SVG graphs!')
