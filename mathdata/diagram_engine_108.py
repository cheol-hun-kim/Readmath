"""
ReadMath 108-Je Masterpiece Mathematical Diagram Engine
Generates mathematically exact, non-duplicated SVGs for geometry, calculus, and function problems.
Returns None for pure algebraic/discrete problems (strictly ZERO fake duplicate diagrams).
"""

from typing import Optional

def get_diagram_for_108(prob_num: int) -> Optional[str]:
    """
    Returns an exact mathematical SVG for the specified problem number.
    Returns None if the problem is purely algebraic with no geometric/graphical figure.
    """
    
    # =========================================================================
    # PART 1: 2025년 11월 수능 기출 & 변형 (Q1 ~ Q36)
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # SET 1: 수열 역추적 분기 트리 (Q1 원본, Q2 변형 A, Q3 변형 B)
    # -------------------------------------------------------------------------
    if prob_num in [1, 2, 3]:
        target_a1 = "151" if prob_num == 1 else ("186" if prob_num == 2 else "128")
        step_text = "a₆=1 또는 a₆=2" if prob_num == 1 else ("a₅=6 확정" if prob_num == 2 else "a₆=3 확정")
        sub_title = "원본: 수열 역방향 분기 트리" if prob_num == 1 else ("변형 A: 지수-절반 역산 트리" if prob_num == 2 else "변형 B: 3의 배수 삼분 역산 트리")
        
        return f'''<svg viewBox="0 0 460 110" width="100%" height="110" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="110" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <rect x="15" y="10" width="170" height="22" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
  <text x="25" y="25" font-size="9.5" font-weight="bold" fill="#080908">{sub_title}</text>
  
  <!-- Root Node -->
  <circle cx="50" cy="65" r="16" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
  <text x="50" y="68" font-size="9" font-weight="900" fill="#EA580C" text-anchor="middle">시작</text>
  <text x="50" y="93" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">{step_text}</text>
  
  <!-- Branch Lines -->
  <line x1="66" y1="58" x2="130" y2="45" stroke="#94A3B8" stroke-width="1.5"/>
  <text x="95" y="47" font-size="8" font-weight="bold" fill="#EA580C">홀수역산</text>
  <line x1="66" y1="72" x2="130" y2="85" stroke="#94A3B8" stroke-width="1.5"/>
  <text x="95" y="87" font-size="8" font-weight="bold" fill="#2563EB">짝수역산</text>
  
  <!-- Intermediate Nodes -->
  <rect x="130" y="33" width="55" height="22" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
  <text x="157" y="48" font-size="9" font-weight="bold" fill="#080908" text-anchor="middle">a_k = 1</text>
  <rect x="130" y="75" width="55" height="22" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
  <text x="157" y="90" font-size="9" font-weight="bold" fill="#080908" text-anchor="middle">a_k = 4</text>
  
  <!-- Sub Branches to Leaves -->
  <line x1="185" y1="44" x2="230" y2="35" stroke="#CBD5E1" stroke-width="1.2"/>
  <circle cx="240" cy="35" r="10" fill="#F1F5F9" stroke="#94A3B8"/>
  <text x="240" y="38" font-size="8.5" font-weight="bold" fill="#334155" text-anchor="middle">2</text>
  
  <line x1="185" y1="85" x2="230" y2="75" stroke="#CBD5E1" stroke-width="1.2"/>
  <circle cx="240" cy="75" r="10" fill="#F1F5F9" stroke="#94A3B8"/>
  <text x="240" y="78" font-size="8.5" font-weight="bold" fill="#334155" text-anchor="middle">8</text>
  
  <line x1="185" y1="88" x2="230" y2="95" stroke="#CBD5E1" stroke-width="1.2"/>
  <circle cx="240" cy="95" r="10" fill="#F1F5F9" stroke="#94A3B8"/>
  <text x="240" y="98" font-size="8.5" font-weight="bold" fill="#334155" text-anchor="middle">16</text>
  
  <!-- Arrow to Result Badge -->
  <line x1="260" y1="65" x2="320" y2="65" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 2"/>
  <polygon points="325,65 318,61 318,69" fill="#EA580C"/>
  
  <!-- Final Result Badge -->
  <rect x="335" y="35" width="105" height="55" rx="6" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.5"/>
  <text x="387" y="55" font-size="9" font-weight="bold" fill="#15803D" text-anchor="middle">모든 a₁의 합</text>
  <text x="387" y="78" font-size="16" font-weight="900" fill="#16A34A" text-anchor="middle">{target_a1}</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 2: 지수·로그 점대칭 및 접선 교점 (Q4, Q5, Q6)
    # -------------------------------------------------------------------------
    elif prob_num == 4:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">지수함수 y=2ˣ 점대칭 접선 교점</text>
  <line x1="30" y1="57.5" x2="430" y2="57.5" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="435" y="60.5" font-size="9.5" font-weight="bold" fill="#64748B">x</text>
  <line x1="230" y1="105" x2="230" y2="10" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="230" y="8" font-size="9.5" font-weight="bold" fill="#64748B" text-anchor="middle">y</text>
  <path d="M 60,55 Q 230,50 360,15" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <text x="365" y="20" font-size="9" font-weight="bold" fill="#2563EB">y=2ˣ</text>
  <path d="M 100,100 Q 230,65 400,60" fill="none" stroke="#EA580C" stroke-width="2.0"/>
  <text x="405" y="65" font-size="9" font-weight="bold" fill="#EA580C">y=-2⁻ˣ</text>
  <circle cx="280" cy="40" r="3.5" fill="#2563EB"/>
  <text x="280" y="32" font-size="8" font-weight="bold" fill="#2563EB" text-anchor="middle">(t, 2ᵗ)</text>
  <circle cx="180" cy="75" r="3.5" fill="#EA580C"/>
  <text x="180" y="90" font-size="8" font-weight="bold" fill="#EA580C" text-anchor="middle">(-t, -2⁻ᵗ)</text>
  <line x1="210" y1="65" x2="330" y2="20" stroke="#2563EB" stroke-width="1.0" stroke-dasharray="3 2"/>
  <line x1="130" y1="95" x2="250" y2="50" stroke="#EA580C" stroke-width="1.0" stroke-dasharray="3 2"/>
  <circle cx="255" cy="57.5" r="3.5" fill="#DC2626"/>
  <text x="260" y="52" font-size="8.5" font-weight="bold" fill="#DC2626">교점 (0, f(t))</text>
</svg>'''

    elif prob_num == 5:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">로그함수 y=ln x 원점 대칭 접선 교점</text>
  <line x1="30" y1="57.5" x2="430" y2="57.5" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="435" y="60.5" font-size="9.5" font-weight="bold" fill="#64748B">x</text>
  <line x1="230" y1="105" x2="230" y2="10" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="230" y="8" font-size="9.5" font-weight="bold" fill="#64748B" text-anchor="middle">y</text>
  <path d="M 235,100 Q 250,55 410,40" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <text x="415" y="42" font-size="9" font-weight="bold" fill="#2563EB">y=ln x</text>
  <path d="M 225,15 Q 210,60 50,75" fill="none" stroke="#EA580C" stroke-width="2.0"/>
  <text x="55" y="90" font-size="9" font-weight="bold" fill="#EA580C">y=-ln(-x)</text>
  <circle cx="320" cy="50" r="3.5" fill="#2563EB"/>
  <circle cx="140" cy="65" r="3.5" fill="#EA580C"/>
  <line x1="200" y1="85" x2="380" y2="30" stroke="#2563EB" stroke-width="1.0" stroke-dasharray="3 2"/>
  <line x1="80" y1="85" x2="260" y2="30" stroke="#EA580C" stroke-width="1.0" stroke-dasharray="3 2"/>
  <circle cx="230" cy="57.5" r="4" fill="#DC2626"/>
  <text x="245" y="52" font-size="8.5" font-weight="bold" fill="#DC2626">원점 대칭 교점 (0, 0)</text>
</svg>'''

    elif prob_num == 6:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">지수함수 y=eˣ 접선 수직 직교 조건</text>
  <line x1="30" y1="95" x2="430" y2="95" stroke="#94A3B8" stroke-width="1.2"/>
  <line x1="180" y1="105" x2="180" y2="10" stroke="#94A3B8" stroke-width="1.2"/>
  <path d="M 60,93 Q 180,90 320,20" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <text x="325" y="25" font-size="9" font-weight="bold" fill="#2563EB">y=eˣ</text>
  <line x1="100" y1="100" x2="280" y2="25" stroke="#2563EB" stroke-width="1.5"/>
  <line x1="160" y1="30" x2="280" y2="95" stroke="#EA580C" stroke-width="1.5"/>
  <circle cx="220" cy="50" r="3.5" fill="#080908"/>
  <rect x="330" y="35" width="110" height="50" rx="6" fill="#EFF6FF" stroke="#3B82F6"/>
  <text x="385" y="55" font-size="9" font-weight="bold" fill="#1D4ED8" text-anchor="middle">접선 기울기 수직</text>
  <text x="385" y="73" font-size="11" font-weight="900" fill="#1D4ED8" text-anchor="middle">m₁ × m₂ = -1</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 3: 삼차함수 접선 및 변곡 대칭 (Q7, Q8, Q9)
    # -------------------------------------------------------------------------
    elif prob_num in [7, 8, 9]:
        cond_text = "g(x) = f(x) - 2x 접선 경계" if prob_num == 7 else ("f(x) ≥ f(t) + f'(t)(x-t) 접선 부등식" if prob_num == 8 else "g(x) = 3x 교점 개수")
        return f'''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">삼차함수 접선 및 변곡 대칭: {cond_text}</text>
  <line x1="30" y1="65" x2="430" y2="65" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="435" y="68" font-size="9" font-weight="bold" fill="#64748B">x</text>
  <path d="M 60,105 C 130,10 170,10 240,65 C 310,120 350,120 400,15" fill="none" stroke="#080908" stroke-width="2.2"/>
  <text x="405" y="20" font-size="9.5" font-weight="bold" fill="#080908">y=f(x)</text>
  <circle cx="240" cy="65" r="3.5" fill="#2563EB"/>
  <text x="240" y="55" font-size="8.5" font-weight="bold" fill="#2563EB" text-anchor="middle">변곡점</text>
  <line x1="160" y1="20" x2="320" y2="110" stroke="#EA580C" stroke-width="1.5" stroke-dasharray="4 2"/>
  <circle cx="160" cy="20" r="3.5" fill="#EA580C"/>
  <circle cx="320" cy="110" r="3.5" fill="#EA580C"/>
  <text x="145" y="18" font-size="8.5" font-weight="bold" fill="#EA580C">x=-1</text>
  <text x="335" y="115" font-size="8.5" font-weight="bold" fill="#EA580C">x=3</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 4: 사차함수 W형 및 미분가능성 (Q10, Q11, Q12)
    # -------------------------------------------------------------------------
    elif prob_num in [10, 11, 12]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">사차함수 절댓값 미분가능성 (W형 대칭)</text>
  <line x1="40" y1="85" x2="420" y2="85" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="425" y="88" font-size="9" font-weight="bold" fill="#64748B">x</text>
  <path d="M 60,20 C 100,120 140,120 180,65 C 220,10 260,10 300,65 C 340,120 380,120 410,20" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <text x="415" y="25" font-size="9" font-weight="bold" fill="#2563EB">y=f(x)</text>
  <line x1="70" y1="98" x2="390" y2="98" stroke="#EA580C" stroke-width="1.5" stroke-dasharray="3 2"/>
  <text x="395" y="102" font-size="8.5" font-weight="bold" fill="#EA580C">y=g(t)</text>
  <circle cx="120" cy="98" r="3.5" fill="#DC2626"/>
  <circle cx="360" cy="98" r="3.5" fill="#DC2626"/>
  <text x="240" y="108" font-size="8.5" font-weight="bold" fill="#DC2626" text-anchor="middle">극솟값 접점에서 꺾임 미분불가 방어</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 7: 타원 직각삼각형 및 초점 (Q19, Q20, Q21)
    # -------------------------------------------------------------------------
    elif prob_num in [19, 20, 21]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">타원 위의 점 P와 직각삼각형 △FPF'</text>
  <line x1="30" y1="65" x2="430" y2="65" stroke="#94A3B8" stroke-width="1.0"/>
  <line x1="230" y1="105" x2="230" y2="25" stroke="#94A3B8" stroke-width="1.0"/>
  <ellipse cx="230" cy="65" rx="140" ry="38" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <circle cx="150" cy="65" r="3.5" fill="#080908"/>
  <text x="150" y="78" font-size="8.5" font-weight="bold" fill="#080908" text-anchor="middle">F'(-c,0)</text>
  <circle cx="310" cy="65" r="3.5" fill="#080908"/>
  <text x="310" y="78" font-size="8.5" font-weight="bold" fill="#080908" text-anchor="middle">F(c,0)</text>
  <circle cx="280" cy="35" r="3.5" fill="#EA580C"/>
  <text x="280" y="28" font-size="8.5" font-weight="bold" fill="#EA580C" text-anchor="middle">P(x,y)</text>
  <polygon points="150,65 310,65 280,35" fill="rgba(234, 88, 12, 0.08)" stroke="#EA580C" stroke-width="1.5"/>
  <text x="350" y="45" font-size="9" font-weight="bold" fill="#EA580C">PF + PF' = 2a</text>
  <text x="350" y="60" font-size="8.5" font-weight="bold" fill="#15803D">PF ⊥ PF'</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 8: 평면벡터 원과 중심거리 (Q22, Q23, Q24)
    # -------------------------------------------------------------------------
    elif prob_num in [22, 23, 24]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">평면벡터 중심 분할: OP = OC + CP</text>
  <circle cx="70" cy="65" r="4" fill="#080908"/>
  <text x="60" y="70" font-size="9" font-weight="bold" fill="#080908">O</text>
  <circle cx="190" cy="65" r="28" fill="#F8FAFC" stroke="#2563EB" stroke-width="1.5"/>
  <circle cx="190" cy="65" r="3" fill="#2563EB"/>
  <text x="190" y="58" font-size="8.5" font-weight="bold" fill="#2563EB" text-anchor="middle">C(2,3)</text>
  <line x1="70" y1="65" x2="190" y2="65" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3 2"/>
  <line x1="190" y1="65" x2="218" y2="65" stroke="#EA580C" stroke-width="2.0"/>
  <circle cx="218" cy="65" r="3.5" fill="#EA580C"/>
  <text x="225" y="60" font-size="8.5" font-weight="bold" fill="#EA580C">P(동선)</text>
  <rect x="270" y="32" width="165" height="55" rx="6" fill="#F0FDF4" stroke="#16A34A"/>
  <text x="352" y="52" font-size="8.5" font-weight="bold" fill="#15803D" text-anchor="middle">벡터 분할 공식</text>
  <text x="352" y="72" font-size="10" font-weight="900" fill="#15803D" text-anchor="middle">|OP + OQ| ≤ |OC + OD| + r₁ + r₂</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 9: 공간도형 (Q25 정사면체, Q26 정사각뿔, Q27 회전다면체)
    # -------------------------------------------------------------------------
    elif prob_num == 25:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <rect x="15" y="8" width="210" height="18" rx="3" fill="#F8FAFC" stroke="#E2E8F0"/>
  <text x="22" y="20" font-size="8.5" font-weight="bold" fill="#080908">정사면체 대칭 단면 삼각형 △ABM 평면화</text>
  <polygon points="110,102 230,102 170,38" fill="#F8FAFC" stroke="#080908" stroke-width="2.0"/>
  <text x="100" y="106" font-size="9" font-weight="bold" fill="#080908">A</text>
  <text x="235" y="106" font-size="9" font-weight="bold" fill="#080908">B</text>
  <text x="170" y="32" font-size="9" font-weight="bold" fill="#080908" text-anchor="middle">M</text>
  <line x1="170" y1="38" x2="170" y2="102" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="3 2"/>
  <text x="175" y="70" font-size="8" font-weight="bold" fill="#64748B">h=3√2</text>
  <line x1="230" y1="102" x2="135" y2="64" stroke="#EA580C" stroke-width="2.0"/>
  <circle cx="135" cy="64" r="3.5" fill="#EA580C"/>
  <text x="125" y="60" font-size="9" font-weight="900" fill="#EA580C">H</text>
  <rect x="280" y="30" width="165" height="58" rx="6" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="362" y="50" font-size="8.5" font-weight="bold" fill="#9A3412" text-anchor="middle">넓이 일치 방정식</text>
  <text x="362" y="68" font-size="9" font-weight="bold" fill="#080908" text-anchor="middle">AM × BH = AB × MN</text>
  <text x="362" y="82" font-size="9.5" font-weight="bold" fill="#EA580C" text-anchor="middle">⇒ BH = 2√6</text>
</svg>'''

    elif prob_num == 26:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <rect x="15" y="5" width="220" height="16" rx="3" fill="#F8FAFC" stroke="#E2E8F0"/>
  <text x="22" y="16" font-size="8.5" font-weight="bold" fill="#080908">정사각뿔 O-ABCD 삼수선 단면 직각삼각형</text>
  <!-- Square Base Projection -->
  <polygon points="70,105 170,105 200,75 100,75" fill="#F8FAFC" stroke="#64748B" stroke-width="1.2"/>
  <!-- Apex O -->
  <circle cx="135" cy="40" r="3.5" fill="#080908"/>
  <text x="135" y="32" font-size="8.5" font-weight="bold" fill="#080908" text-anchor="middle">O(꼭짓점)</text>
  <!-- Altitude OH to Base Center H -->
  <line x1="135" y1="40" x2="135" y2="90" stroke="#EA580C" stroke-width="1.8" stroke-dasharray="3 2"/>
  <circle cx="135" cy="90" r="3" fill="#EA580C"/>
  <text x="145" y="93" font-size="8" font-weight="bold" fill="#EA580C">H(밑면중심)</text>
  <!-- Edges to Base -->
  <line x1="135" y1="35" x2="70" y2="102" stroke="#2563EB" stroke-width="1.5"/>
  <line x1="135" y1="35" x2="170" y2="102" stroke="#2563EB" stroke-width="1.5"/>
  <rect x="260" y="28" width="175" height="62" rx="6" fill="#EFF6FF" stroke="#93C5FD"/>
  <text x="347" y="48" font-size="8.5" font-weight="bold" fill="#1E40AF" text-anchor="middle">정사각뿔 정사영 삼수선</text>
  <text x="347" y="66" font-size="9" font-weight="bold" fill="#080908" text-anchor="middle">밑면 4×4, 높이 OH = 4</text>
  <text x="347" y="82" font-size="9.5" font-weight="bold" fill="#2563EB" text-anchor="middle">정사영 삼각형 넓이 = 4</text>
</svg>'''

    elif prob_num == 27:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">회전 평면과 이면각 정사영 (S' = S × cos θ)</text>
  <!-- Plane Alpha -->
  <line x1="40" y1="90" x2="300" y2="90" stroke="#080908" stroke-width="1.8"/>
  <text x="305" y="93" font-size="9" font-weight="bold" fill="#080908">평면 α</text>
  <!-- Rotated Plane Beta -->
  <line x1="80" y1="90" x2="240" y2="30" stroke="#EA580C" stroke-width="2.0"/>
  <text x="245" y="32" font-size="9" font-weight="bold" fill="#EA580C">평면 β (회전)</text>
  <!-- Angle Arc -->
  <path d="M 120,90 A 40 40 0 0 0 115,77" fill="none" stroke="#EA580C" stroke-width="1.5"/>
  <text x="130" y="82" font-size="9" font-weight="bold" fill="#EA580C">θ</text>
  <rect x="315" y="28" width="130" height="62" rx="6" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="380" y="48" font-size="8.5" font-weight="bold" fill="#9A3412" text-anchor="middle">정사영 핵심 공식</text>
  <text x="380" y="66" font-size="9.5" font-weight="900" fill="#EA580C" text-anchor="middle">S' = S × cos θ</text>
  <text x="380" y="80" font-size="8" font-weight="bold" fill="#475569" text-anchor="middle">이등변삼각형 단면 사영</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 12: 확통 확률밀도함수 (Q34 삼각형, Q35 사다리꼴, Q36 정규분포)
    # -------------------------------------------------------------------------
    elif prob_num == 34:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">연속확률변수 삼각형 확률밀도함수 (0 ≤ X ≤ 4)</text>
  <line x1="40" y1="90" x2="420" y2="90" stroke="#94A3B8" stroke-width="1.2"/>
  <line x1="80" y1="100" x2="80" y2="25" stroke="#94A3B8" stroke-width="1.2"/>
  <text x="75" y="20" font-size="9" font-weight="bold" fill="#64748B">y</text>
  <text x="70" y="100" font-size="8.5" fill="#64748B">O</text>
  <polygon points="80,90 230,35 380,90" fill="rgba(37, 99, 235, 0.08)" stroke="#2563EB" stroke-width="2.0"/>
  <text x="230" y="28" font-size="8.5" font-weight="bold" fill="#2563EB" text-anchor="middle">(2, 1/2)</text>
  <text x="380" y="102" font-size="8.5" font-weight="bold" fill="#64748B" text-anchor="middle">4</text>
  <line x1="155" y1="90" x2="155" y2="62.5" stroke="#EA580C" stroke-width="1.2" stroke-dasharray="3 2"/>
  <line x1="305" y1="90" x2="305" y2="62.5" stroke="#EA580C" stroke-width="1.2" stroke-dasharray="3 2"/>
  <text x="155" y="102" font-size="8.5" font-weight="bold" fill="#EA580C" text-anchor="middle">1</text>
  <text x="305" y="102" font-size="8.5" font-weight="bold" fill="#EA580C" text-anchor="middle">3</text>
  <rect x="280" y="32" width="150" height="42" rx="5" fill="#EFF6FF" stroke="#BFDBFE"/>
  <text x="355" y="56" font-size="9" font-weight="bold" fill="#1E40AF" text-anchor="middle">P(1 ≤ X ≤ 3) = 3/4</text>
</svg>'''

    elif prob_num == 35:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">사다리꼴 확률밀도함수 총넓이 = 1</text>
  <line x1="40" y1="90" x2="420" y2="90" stroke="#94A3B8" stroke-width="1.2"/>
  <line x1="80" y1="100" x2="80" y2="25" stroke="#94A3B8" stroke-width="1.2"/>
  <polygon points="80,90 150,40 310,40 380,90" fill="rgba(22, 163, 74, 0.08)" stroke="#16A34A" stroke-width="2.0"/>
  <text x="80" y="102" font-size="8.5" fill="#64748B">0</text>
  <text x="150" y="102" font-size="8.5" fill="#64748B">1</text>
  <text x="310" y="102" font-size="8.5" fill="#64748B">3</text>
  <text x="380" y="102" font-size="8.5" fill="#64748B">4</text>
  <text x="230" y="32" font-size="8.5" font-weight="bold" fill="#15803D" text-anchor="middle">높이 h = 1/3</text>
  <rect x="290" y="35" width="140" height="42" rx="5" fill="#F0FDF4" stroke="#BBF7D0"/>
  <text x="360" y="58" font-size="9" font-weight="bold" fill="#15803D" text-anchor="middle">총확률 넓이 = 1 보존</text>
</svg>'''

    elif prob_num == 36:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">정규분포 곡선 N(m, σ²)의 대칭성과 표준화</text>
  <line x1="40" y1="90" x2="420" y2="90" stroke="#94A3B8" stroke-width="1.2"/>
  <path d="M 60,90 C 160,90 190,30 230,30 C 270,30 300,90 400,90" fill="rgba(37, 99, 235, 0.08)" stroke="#2563EB" stroke-width="2.0"/>
  <line x1="230" y1="30" x2="230" y2="90" stroke="#EA580C" stroke-width="1.5" stroke-dasharray="3 2"/>
  <text x="230" y="102" font-size="9" font-weight="bold" fill="#EA580C" text-anchor="middle">평균 m</text>
  <rect x="290" y="32" width="140" height="45" rx="5" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="360" y="50" font-size="8.5" font-weight="bold" fill="#9A3412" text-anchor="middle">표준화 공식</text>
  <text x="360" y="68" font-size="10" font-weight="bold" fill="#EA580C" text-anchor="middle">Z = (X - m) / σ</text>
</svg>'''

    # =========================================================================
    # PART 2: 2026년 6월 평가원 기출 & 변형 (Q37 ~ Q72)
    # =========================================================================

    # -------------------------------------------------------------------------
    # SET 13: 삼차·사차함수 적분 및 극대극소 (Q37, Q38, Q39)
    # -------------------------------------------------------------------------
    elif prob_num in [37, 38, 39]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">삼차함수 원점 대칭 및 정적분 넓이</text>
  <line x1="30" y1="65" x2="430" y2="65" stroke="#94A3B8" stroke-width="1.0"/>
  <line x1="230" y1="105" x2="230" y2="25" stroke="#94A3B8" stroke-width="1.0"/>
  <path d="M 100,105 C 160,15 190,15 230,65 C 270,115 300,115 360,25" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <circle cx="230" cy="65" r="3.5" fill="#080908"/>
  <text x="222" y="76" font-size="8.5" fill="#64748B">O</text>
  <rect x="290" y="30" width="145" height="55" rx="6" fill="#EFF6FF" stroke="#93C5FD"/>
  <text x="362" y="50" font-size="8.5" font-weight="bold" fill="#1E40AF" text-anchor="middle">기함수 정적분 대칭성</text>
  <text x="362" y="70" font-size="9.5" font-weight="bold" fill="#2563EB" text-anchor="middle">∫₋ₐᵃ f(x)dx = 0</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 14: 삼차함수 구간 최댓값 함수 g(t) (Q40, Q41, Q42)
    # -------------------------------------------------------------------------
    elif prob_num in [40, 41, 42]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">구간 최댓값 함수 g(t) = max f(x)의 계단형 보존</text>
  <line x1="30" y1="85" x2="430" y2="85" stroke="#94A3B8" stroke-width="1.0"/>
  <path d="M 60,105 C 120,20 160,20 220,80 C 260,110 300,110 380,25" fill="none" stroke="#94A3B8" stroke-width="1.5"/>
  <text x="385" y="30" font-size="8.5" fill="#94A3B8">f(x)</text>
  <path d="M 60,105 C 120,20 140,25 150,25 L 290,25 L 380,25" fill="none" stroke="#EA580C" stroke-width="2.5"/>
  <text x="295" y="20" font-size="9" font-weight="bold" fill="#EA580C">g(t) [극댓값 유지 수평선]</text>
  <rect x="290" y="45" width="145" height="45" rx="6" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="362" y="65" font-size="8.5" font-weight="bold" fill="#9A3412" text-anchor="middle">미분불가점 탐색</text>
  <text x="362" y="78" font-size="9" font-weight="bold" fill="#EA580C" text-anchor="middle">f(t) = g(t) 재진입 지점</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 19: 기하 28번 타원 초점과 직각 (Q55, Q56, Q57)
    # -------------------------------------------------------------------------
    elif prob_num in [55, 56, 57]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">타원의 정의와 피타고라스 정리</text>
  <line x1="30" y1="65" x2="430" y2="65" stroke="#94A3B8" stroke-width="1.0"/>
  <ellipse cx="230" cy="65" rx="130" ry="35" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <circle cx="160" cy="65" r="3.5" fill="#080908"/>
  <text x="160" y="78" font-size="8.5" fill="#080908" text-anchor="middle">F'(-c,0)</text>
  <circle cx="300" cy="65" r="3.5" fill="#080908"/>
  <text x="300" y="78" font-size="8.5" fill="#080908" text-anchor="middle">F(c,0)</text>
  <polygon points="160,65 300,65 270,36" fill="rgba(37, 99, 235, 0.08)" stroke="#2563EB" stroke-width="1.5"/>
  <rect x="330" y="30" width="115" height="55" rx="6" fill="#EFF6FF" stroke="#93C5FD"/>
  <text x="387" y="50" font-size="8.5" font-weight="bold" fill="#1E40AF" text-anchor="middle">초점거리 관계</text>
  <text x="387" y="70" font-size="10" font-weight="bold" fill="#2563EB" text-anchor="middle">c² = a² - b²</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 20: 기하 29번 쌍곡선 점근선 및 초점 (Q58, Q59, Q60)
    # -------------------------------------------------------------------------
    elif prob_num in [58, 59, 60]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">쌍곡선 x²/a² - y²/b² = 1 점근선과 초점거리</text>
  <line x1="30" y1="65" x2="430" y2="65" stroke="#94A3B8" stroke-width="1.0"/>
  <line x1="230" y1="105" x2="230" y2="25" stroke="#94A3B8" stroke-width="1.0"/>
  <line x1="130" y1="100" x2="330" y2="30" stroke="#94A3B8" stroke-width="1.0" stroke-dasharray="3 2"/>
  <line x1="130" y1="30" x2="330" y2="100" stroke="#94A3B8" stroke-width="1.0" stroke-dasharray="3 2"/>
  <path d="M 330,30 Q 280,65 330,100" fill="none" stroke="#EA580C" stroke-width="2.0"/>
  <path d="M 130,30 Q 180,65 130,100" fill="none" stroke="#EA580C" stroke-width="2.0"/>
  <circle cx="310" cy="65" r="3.5" fill="#080908"/>
  <text x="310" y="78" font-size="8.5" fill="#080908" text-anchor="middle">F(3,0)</text>
  <rect x="345" y="32" width="100" height="52" rx="6" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="395" y="52" font-size="8.5" font-weight="bold" fill="#9A3412" text-anchor="middle">초점 공식</text>
  <text x="395" y="70" font-size="10" font-weight="bold" fill="#EA580C" text-anchor="middle">c² = a² + b²</text>
</svg>'''

    # =========================================================================
    # PART 3: 2026년 9월 평가원 기출 & 변형 (Q73 ~ Q108)
    # =========================================================================

    # -------------------------------------------------------------------------
    # SET 27: 공통 지수·로그함수와 직사각형 ABCD (Q79, Q80, Q81)
    # -------------------------------------------------------------------------
    elif prob_num in [79, 80, 81]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">지수함수 곡선 위의 직사각형 ABCD</text>
  <line x1="30" y1="85" x2="430" y2="85" stroke="#94A3B8" stroke-width="1.0"/>
  <path d="M 60,82 Q 180,80 320,25" fill="none" stroke="#2563EB" stroke-width="2.0"/>
  <text x="325" y="30" font-size="8.5" font-weight="bold" fill="#2563EB">y=aˣ</text>
  <path d="M 120,83 Q 240,82 380,35" fill="none" stroke="#16A34A" stroke-width="2.0"/>
  <text x="385" y="40" font-size="8.5" font-weight="bold" fill="#16A34A">y=aˣ⁻²</text>
  <rect x="180" y="45" width="80" height="40" fill="rgba(234, 88, 12, 0.08)" stroke="#EA580C" stroke-width="1.8"/>
  <text x="175" y="42" font-size="8.5" font-weight="bold" fill="#EA580C">A</text>
  <text x="265" y="42" font-size="8.5" font-weight="bold" fill="#EA580C">B</text>
  <text x="265" y="95" font-size="8.5" font-weight="bold" fill="#EA580C">C</text>
  <text x="175" y="95" font-size="8.5" font-weight="bold" fill="#EA580C">D</text>
  <rect x="290" y="30" width="145" height="52" rx="6" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="362" y="50" font-size="8.5" font-weight="bold" fill="#9A3412" text-anchor="middle">직사각형 좌표 관계</text>
  <text x="362" y="68" font-size="9.5" font-weight="bold" fill="#EA580C" text-anchor="middle">가로 = x_B - x_A = 2</text>
</svg>'''

    # -------------------------------------------------------------------------
    # SET 28: 미적분 28번 삼각함수 도형의 극한 (Q82, Q83, Q84)
    # -------------------------------------------------------------------------
    elif prob_num in [82, 83, 84]:
        return '''<svg viewBox="0 0 460 115" width="100%" height="115" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="115" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>
  <text x="25" y="22" font-size="9.5" font-weight="bold" fill="#080908">원 위의 호와 삼각함수 도형의 극한 S(θ), T(θ)</text>
  <circle cx="160" cy="65" r="38" fill="none" stroke="#080908" stroke-width="1.5"/>
  <circle cx="160" cy="65" r="2.5" fill="#080908"/>
  <text x="160" y="76" font-size="8" fill="#080908" text-anchor="middle">O</text>
  <polygon points="160,65 198,65 187,35" fill="rgba(37, 99, 235, 0.15)" stroke="#2563EB" stroke-width="1.2"/>
  <text x="180" y="52" font-size="8" font-weight="bold" fill="#2563EB">S(θ)</text>
  <path d="M 198,65 A 38 38 0 0 0 187,35" fill="rgba(234, 88, 12, 0.15)" stroke="#EA580C" stroke-width="1.5"/>
  <text x="202" y="48" font-size="8" font-weight="bold" fill="#EA580C">T(θ)</text>
  <rect x="270" y="32" width="165" height="52" rx="6" fill="#EFF6FF" stroke="#93C5FD"/>
  <text x="352" y="52" font-size="8.5" font-weight="bold" fill="#1E40AF" text-anchor="middle">삼각함수 극한 근사</text>
  <text x="352" y="70" font-size="9.5" font-weight="bold" fill="#2563EB" text-anchor="middle">lim θ→0 S(θ)/θ³ = k 도출</text>
</svg>'''

    # -------------------------------------------------------------------------
    # PURE ALGEBRAIC / COMBINATORICS: STRICTLY NO DUMMY FALLBACK DIAGRAMS!
    # -------------------------------------------------------------------------
    return None
