import os

def make_poly(fn, x_min, x_max, steps, scale_x, offset_x, scale_y, offset_y):
    pts = []
    for i in range(steps + 1):
        x = x_min + (x_max - x_min) * i / float(steps)
        y = fn(x)
        X = offset_x + x * scale_x
        Y = offset_y - y * scale_y
        pts.append(f"{X:.2f},{Y:.2f}")
    return " ".join(pts)

def get_svg_for_prob(prob_num):
    if prob_num in [1, 13]:
        target_sum = "151" if prob_num == 1 else "252"
        base_title = "a₇+a₆=3 (밑=2)" if prob_num == 1 else "a₆+a₅=4 (밑=3)"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <text x="15" y="18" fill="#080908" font-size="10" font-weight="bold">수열 귀납적 역추적 분기 트리 ({base_title})</text>
          <rect x="20" y="35" width="60" height="24" rx="4" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.2"/>
          <text x="50" y="51" fill="#EA580C" font-size="11" font-weight="bold" text-anchor="middle">종착 분기 1</text>
          <rect x="20" y="70" width="60" height="24" rx="4" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.2"/>
          <text x="50" y="86" fill="#EA580C" font-size="11" font-weight="bold" text-anchor="middle">종착 분기 2</text>
          <line x1="80" y1="47" x2="130" y2="40" stroke="#EA580C" stroke-width="1.2"/>
          <line x1="80" y1="82" x2="130" y2="70" stroke="#EA580C" stroke-width="1.2"/>
          <line x1="80" y1="82" x2="130" y2="92" stroke="#EA580C" stroke-width="1.2"/>
          <rect x="130" y="28" width="65" height="22" rx="4" fill="#F8FAFC" stroke="#64748B" stroke-width="1"/>
          <text x="162" y="43" fill="#080908" font-size="9" font-weight="bold" text-anchor="middle">홀수 역연산</text>
          <rect x="130" y="60" width="65" height="22" rx="4" fill="#F8FAFC" stroke="#64748B" stroke-width="1"/>
          <text x="162" y="75" fill="#080908" font-size="9" font-weight="bold" text-anchor="middle">짝수 역연산</text>
          <text x="235" y="65" fill="#64748B" font-size="12" font-weight="bold">··· 역방향 분기 탐색 ···</text>
          <rect x="330" y="33" width="95" height="60" rx="6" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.5"/>
          <text x="377" y="52" fill="#16A34A" font-size="9.5" font-weight="bold" text-anchor="middle">가능한 a₁ 총합</text>
          <text x="377" y="78" fill="#15803D" font-size="17" font-weight="900" text-anchor="middle">{target_sum}</text>
        </svg>'''
    elif prob_num in [2, 14]:
        base_val = "2" if prob_num == 2 else "3"
        pts1 = make_poly(lambda x: 2**x if prob_num == 2 else 3**x, -1.8, 1.8, 60, 45, 120, 18, 80)
        pts2 = make_poly(lambda x: -(2**(-x)) if prob_num == 2 else -(3**(-x)), -1.8, 1.8, 60, 45, 120, 18, 80)
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="20" y1="80" x2="260" y2="80" stroke="#334155" stroke-width="1"/>
          <line x1="120" y1="105" x2="120" y2="10" stroke="#334155" stroke-width="1"/>
          <polyline fill="none" stroke="#080908" stroke-width="1.8" points="{pts1}"/>
          <polyline fill="none" stroke="#080908" stroke-width="1.8" points="{pts2}"/>
          <line x1="90" y1="95" x2="210" y2="15" stroke="#DC2626" stroke-width="1.4" stroke-dasharray="3 2"/>
          <circle cx="165" cy="48" r="3" fill="#DC2626"/>
          <text x="172" y="44" fill="#DC2626" font-size="9" font-weight="bold">(t, {base_val}ᵗ)</text>
          <circle cx="140" cy="65" r="3.5" fill="#EA580C"/>
          <text x="145" y="75" fill="#EA580C" font-size="8.5" font-weight="bold">교점 대칭</text>
          <text x="290" y="40" fill="#090D16" font-size="10" font-weight="bold">원점 대칭 접선 직교</text>
          <text x="290" y="60" fill="#64748B" font-size="9">기울기 일치 대칭 해석</text>
          <text x="290" y="80" fill="#EA580C" font-size="12" font-weight="bold">⇒ t = 1 확정</text>
        </svg>'''
    elif prob_num in [3, 15]:
        pts = make_poly(lambda x: (x-2)**2 * (x+1), -1.3, 3.1, 70, 42, 135, 9, 75)
        ans_txt = "f(5)=48" if prob_num == 3 else "f(6)=118"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="20" y1="75" x2="265" y2="75" stroke="#334155" stroke-width="1"/>
          <line x1="135" y1="105" x2="135" y2="10" stroke="#334155" stroke-width="1"/>
          <polyline fill="none" stroke="#080908" stroke-width="2" points="{pts}"/>
          <line x1="55" y1="40" x2="255" y2="98" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="4 2"/>
          <circle cx="219" cy="75" r="3.5" fill="#080908"/>
          <text x="219" y="90" fill="#080908" font-size="8.5" font-weight="bold" text-anchor="middle">극소 0 접점</text>
          <circle cx="93" cy="75" r="3.5" fill="#DC2626"/>
          <text x="80" y="68" fill="#DC2626" font-size="8.5" font-weight="bold" text-anchor="end">t=-1</text>
          <text x="300" y="40" fill="#080908" font-size="10" font-weight="bold">비율관계 1:1:1 적용</text>
          <text x="300" y="60" fill="#64748B" font-size="9">경계조건 접선 판별</text>
          <text x="300" y="80" fill="#EA580C" font-size="12" font-weight="bold">{ans_txt}</text>
        </svg>'''
    elif prob_num in [4, 16]:
        pts = make_poly(lambda x: (x**2 - 2)**2, -2.1, 2.1, 70, 40, 150, 16, 85)
        ans_min = "최솟값 = 8" if prob_num == 4 else "최솟값 = 18"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="30" y1="85" x2="265" y2="85" stroke="#334155" stroke-width="1"/>
          <line x1="150" y1="105" x2="150" y2="10" stroke="#334155" stroke-width="1"/>
          <polyline fill="none" stroke="#080908" stroke-width="2" points="{pts}"/>
          <text x="290" y="35" fill="#080908" font-size="10" font-weight="bold">g(x)=|f(x)-a| 미분가능</text>
          <text x="290" y="55" fill="#64748B" font-size="9">⇒ 완전제곱식 (x²-c²)²</text>
          <circle cx="150" cy="21" r="3" fill="#DC2626"/>
          <text x="290" y="78" fill="#EA580C" font-size="12" font-weight="bold">{ans_min}</text>
        </svg>'''
    elif prob_num in [5, 17]:
        lim_val = "3" if prob_num == 5 else "4"
        ans_val = "3" if prob_num == 5 else "6"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="30" y1="85" x2="265" y2="85" stroke="#334155" stroke-width="1"/>
          <line x1="60" y1="105" x2="60" y2="15" stroke="#334155" stroke-width="1"/>
          <line x1="60" y1="40" x2="265" y2="40" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="4 2"/>
          <text x="245" y="34" fill="#DC2626" font-size="9.5" font-weight="bold">y = {lim_val}</text>
          <text x="285" y="35" fill="#080908" font-size="10" font-weight="bold">급수 수렴 성질: lim (aₙ - {lim_val}) = 0</text>
          <text x="285" y="55" fill="#64748B" font-size="9">등비수열 수렴 조건 r = 1 판별</text>
          <text x="285" y="78" fill="#EA580C" font-size="12" font-weight="bold">첫째항 a₁ = {ans_val} 도출</text>
        </svg>'''
    elif prob_num in [6, 18]:
        ans_sq = "14" if prob_num == 6 else "20"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="30" y1="85" x2="265" y2="85" stroke="#334155" stroke-width="1"/>
          <line x1="90" y1="110" x2="90" y2="10" stroke="#334155" stroke-width="1"/>
          <line x1="170" y1="85" x2="90" y2="30" stroke="#DC2626" stroke-width="2"/>
          <circle cx="170" cy="85" r="3.5" fill="#DC2626"/>
          <text x="170" y="98" fill="#DC2626" font-size="9" font-weight="bold" text-anchor="middle">A(t-1, 0)</text>
          <circle cx="90" cy="30" r="3.5" fill="#DC2626"/>
          <text x="82" y="33" fill="#DC2626" font-size="8.5" font-weight="bold" text-anchor="end">B(0, ln s - 1)</text>
          <text x="285" y="38" fill="#080908" font-size="10" font-weight="bold">두 접선의 수직 조건 적용</text>
          <text x="285" y="58" fill="#64748B" font-size="9">거리 함수 단일 변수 치환</text>
          <text x="285" y="78" fill="#EA580C" font-size="12" font-weight="bold">AB² 최솟값 = {ans_sq}</text>
        </svg>'''
    elif prob_num in [7, 19]:
        ans_c = "16" if prob_num == 7 else "12"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="25" y1="60" x2="255" y2="60" stroke="#334155" stroke-width="1"/>
          <line x1="140" y1="110" x2="140" y2="10" stroke="#334155" stroke-width="1"/>
          <ellipse cx="140" cy="60" rx="75" ry="35" fill="none" stroke="#080908" stroke-width="1.8"/>
          <path d="M 195 18 Q 170 60, 195 102" fill="none" stroke="#080908" stroke-width="1.8"/>
          <path d="M 85 18 Q 110 60, 85 102" fill="none" stroke="#080908" stroke-width="1.8"/>
          <circle cx="90" cy="60" r="3.5" fill="#DC2626"/>
          <circle cx="190" cy="60" r="3.5" fill="#DC2626"/>
          <circle cx="178" cy="35" r="3.5" fill="#EA580C"/>
          <text x="170" y="48" fill="#EA580C" font-size="8.5" font-weight="bold" text-anchor="end">P (직교!)</text>
          <text x="285" y="40" fill="#080908" font-size="10" font-weight="bold">공초점 이차곡선 직교</text>
          <text x="285" y="60" fill="#64748B" font-size="9">초점 일치 조건 활용</text>
          <text x="285" y="80" fill="#EA580C" font-size="12" font-weight="bold">a² + b² = {ans_c}</text>
        </svg>'''
    elif prob_num in [8, 20]:
        ans_v = "68" if prob_num == 8 else "136"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="25" y1="60" x2="255" y2="60" stroke="#334155" stroke-width="1"/>
          <line x1="125" y1="110" x2="125" y2="10" stroke="#334155" stroke-width="1"/>
          <circle cx="125" cy="60" r="36" fill="none" stroke="#080908" stroke-width="1.8"/>
          <circle cx="230" cy="60" r="3.5" fill="#DC2626"/>
          <text x="230" y="73" fill="#DC2626" font-size="9" font-weight="bold" text-anchor="middle">점 A</text>
          <text x="285" y="40" fill="#080908" font-size="10" font-weight="bold">중점 벡터 분해</text>
          <text x="285" y="60" fill="#64748B" font-size="9">|AP+AQ|² = 4|AM|²</text>
          <text x="285" y="80" fill="#EA580C" font-size="12" font-weight="bold">M + m = {ans_v}</text>
        </svg>'''
    elif prob_num in [9, 21]:
        ans_s = "120" if prob_num == 9 else "270"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <polygon points="60,90 190,90 125,25" fill="none" stroke="#080908" stroke-width="1.8"/>
          <text x="50" y="96" fill="#080908" font-size="9" font-weight="bold">A</text>
          <text x="195" y="96" fill="#080908" font-size="9" font-weight="bold">B</text>
          <text x="125" y="18" fill="#080908" font-size="9" font-weight="bold" text-anchor="middle">C</text>
          <text x="270" y="40" fill="#080908" font-size="10" font-weight="bold">삼수선의 정리 &amp; 구면 자취</text>
          <text x="270" y="60" fill="#64748B" font-size="9">P는 AB 지름 구면</text>
          <text x="270" y="80" fill="#EA580C" font-size="12" font-weight="bold">10S² = {ans_s}</text>
        </svg>'''
    elif prob_num in [10, 22]:
        p_ans = "3/5" if prob_num == 10 else "4/5"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <rect x="25" y="20" width="210" height="75" rx="6" fill="#FAF8F3" stroke="#080908" stroke-width="1.4"/>
          <text x="35" y="34" fill="#080908" font-size="8.5" font-weight="bold">축소된 표본공간 S (합이 짝수인 사건)</text>
          <ellipse cx="130" cy="62" rx="70" ry="22" fill="rgba(234, 88, 12, 0.12)" stroke="#EA580C" stroke-width="1.5"/>
          <text x="130" y="66" fill="#EA580C" font-size="9.5" font-weight="bold" text-anchor="middle">구하는 사건 B</text>
          <text x="270" y="40" fill="#080908" font-size="10" font-weight="bold">조건부확률 표본공간 분할</text>
          <text x="270" y="60" fill="#64748B" font-size="9">전체 짝수 경우의 수 축소</text>
          <text x="270" y="80" fill="#EA580C" font-size="12" font-weight="bold">P(B|A) = {p_ans}</text>
        </svg>'''
    elif prob_num in [11, 23]:
        ans_h = "25" if prob_num == 11 else "36"
        branch1 = "a = 1 분기" if prob_num == 11 else "a = 0 분기"
        branch2 = "a = 3 분기" if prob_num == 11 else "a = 2 분기"
        comb1 = "₃H₄ = 15가지" if prob_num == 11 else "₃H₄ = 15가지"
        comb2 = "₃H₃ = 10가지" if prob_num == 11 else "₃H₃ = 10가지"
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <text x="20" y="20" fill="#080908" font-size="10" font-weight="bold">중복조합 격자 분할 치환 모델링</text>
          <rect x="25" y="33" width="75" height="25" rx="4" fill="#F8FAFC" stroke="#64748B" stroke-width="1"/>
          <text x="62" y="49" fill="#080908" font-size="8.5" font-weight="bold" text-anchor="middle">{branch1}</text>
          <rect x="25" y="67" width="75" height="25" rx="4" fill="#F8FAFC" stroke="#64748B" stroke-width="1"/>
          <text x="62" y="83" fill="#080908" font-size="8.5" font-weight="bold" text-anchor="middle">{branch2}</text>
          <text x="145" y="50" fill="#080908" font-size="9.5">{comb1}</text>
          <text x="145" y="84" fill="#080908" font-size="9.5">{comb2}</text>
          <rect x="315" y="33" width="105" height="58" rx="6" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.5"/>
          <text x="367" y="52" fill="#16A34A" font-size="9.5" font-weight="bold" text-anchor="middle">순서쌍 총 개수</text>
          <text x="367" y="77" fill="#15803D" font-size="16" font-weight="900" text-anchor="middle">{ans_h}</text>
        </svg>'''
    else: # 12, 24
        ans_p = "69" if prob_num == 12 else "74"
        pts = make_poly(lambda x: (3.0/32.0)*x*(4-x), 0.0, 4.0, 60, 45, 60, 180, 80)
        return f'''<svg viewBox="0 0 440 115" width="100%" height="105" xmlns="http://www.w3.org/2000/svg">
          <rect width="440" height="115" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
          <line x1="20" y1="80" x2="255" y2="80" stroke="#334155" stroke-width="1"/>
          <path d="M 105 80 L 105 56.88 Q 150 12.5, 195 56.88 L 195 80 Z" fill="rgba(234, 88, 12, 0.15)"/>
          <polyline fill="none" stroke="#080908" stroke-width="2" points="{pts}"/>
          <line x1="150" y1="80" x2="150" y2="12.5" stroke="#94A3B8" stroke-width="1" stroke-dasharray="2 2"/>
          <text x="150" y="93" fill="#080908" font-size="8.5" font-weight="bold" text-anchor="middle">대칭축 x=2</text>
          <text x="275" y="38" fill="#080908" font-size="10" font-weight="bold">대칭 구간 적분</text>
          <text x="275" y="56" fill="#64748B" font-size="9">전체 넓이 = 1</text>
          <text x="275" y="76" fill="#EA580C" font-size="12" font-weight="bold">100 × P = {ans_p}</text>
        </svg>'''

if __name__ == "__main__":
    print('Ready to build complete 19-page workbook.')
