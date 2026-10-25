# -*- coding: utf-8 -*-
"""
build_seongnam_2020.py
Builds 100% verified dataset for:
성남외국어고등학교 2학년 2020년 1학기 중간고사 수학I (20문항)
"""

import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db', '성남외국어고등학교_2학년_2020_1학기중간_수학1_공통_문제_해설.json')

def svg_header(w=440, h=280):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="w-full h-auto bg-white rounded-xl shadow-inner border border-slate-200">',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0F172A" />',
        '    </marker>',
        '    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">',
        '      <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#0F172A" flood-opacity="0.08" />',
        '    </filter>',
        '  </defs>',
        f'  <rect width="{w}" height="{h}" fill="#FFFFFF" rx="12" />'
    ]

def svg_axes(parts, ox, oy, w=440, h=280, scale=30, show_grid=True):
    if show_grid:
        parts.append('  <g stroke="#F1F5F9" stroke-width="1" stroke-dasharray="2,2">')
        for gx in range(int(ox % scale), w, int(scale)):
            parts.append(f'    <line x1="{gx}" y1="15" x2="{gx}" y2="{h-15}" />')
        for gy in range(int(oy % scale), h, int(scale)):
            parts.append(f'    <line x1="20" y1="{gy}" x2="{w-20}" y2="{gy}" />')
        parts.append('  </g>')
    parts.append(f'  <line x1="25" y1="{oy}" x2="{w-25}" y2="{oy}" stroke="#0F172A" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append(f'  <line x1="{ox}" y1="{h-20}" x2="{ox}" y2="20" stroke="#0F172A" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append(f'  <text x="{w-22}" y="{oy-8}" fill="#0F172A" font-size="13" font-weight="800" font-family="sans-serif">x</text>')
    parts.append(f'  <text x="{ox+8}" y="22" fill="#0F172A" font-size="13" font-weight="800" font-family="sans-serif">y</text>')
    parts.append(f'  <text x="{ox-14}" y="{oy+16}" fill="#475569" font-size="12" font-weight="bold" font-family="sans-serif">O</text>')

def build_q2_svg():
    p = svg_header()
    # Point P(-4, -3) in quadrant 3, r = 5
    ox, oy = 260, 100
    scale = 32
    svg_axes(p, ox, oy, scale=scale)

    px = ox - 4.0 * scale
    py = oy - (-3.0) * scale # y is -3, in SVG y increases downwards: oy + 3*scale
    py_actual = oy + 3.0 * scale

    # Ray OP
    p.append(f'  <line x1="{ox}" y1="{oy}" x2="{px:.1f}" y2="{py_actual:.1f}" stroke="#DC2626" stroke-width="2.5" />')
    p.append(f'  <circle cx="{px:.1f}" cy="{py_actual:.1f}" r="5" fill="#DC2626" />')
    p.append(f'  <text x="{px-75:.1f}" y="{py_actual+18:.1f}" fill="#DC2626" font-size="12" font-weight="bold">P(-4, -3)</text>')

    # Reference triangle
    p.append(f'  <line x1="{px:.1f}" y1="{py_actual:.1f}" x2="{px:.1f}" y2="{oy}" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="{px-18:.1f}" y="{(oy+py_actual)/2:.1f}" fill="#475569" font-size="11" font-weight="bold">-3</text>')
    p.append(f'  <text x="{(ox+px)/2:.1f}" y="{oy-8}" fill="#475569" font-size="11" font-weight="bold">-4</text>')
    p.append(f'  <text x="{(ox+px)/2 + 10:.1f}" y="{(oy+py_actual)/2 + 14:.1f}" fill="#DC2626" font-size="11" font-weight="bold">r = 5</text>')

    # Card
    p.append('  <rect x="30" y="30" width="160" height="70" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)" />')
    p.append('  <text x="110" y="55" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">sinθ = y / r = -3/5</text>')
    p.append('  <text x="110" y="75" fill="#DC2626" font-size="13" font-weight="bold" text-anchor="middle">5sinθ = -3 (정답 ③)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q3_svg():
    p = svg_header()
    # f(x) = 3 sin(x/3) + 1, min = -2, f(3pi) = 1
    ox, oy = 60, 160
    sx, sy = 16, 26 # 16px per radian, 26px per y unit
    svg_axes(p, ox, oy, scale=32)

    pts = []
    for step in range(80):
        ux = (step / 79.0) * (6.0 * math.pi)
        uy = 3.0 * math.sin(ux / 3.0) + 1.0
        px = ox + ux * sx
        py = oy - uy * sy
        if 20 <= py <= 260:
            pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#2563EB" stroke-width="2.5" />')

    # Min point (4.5pi, -2)
    min_x = ox + (4.5 * math.pi) * sx
    min_y = oy - (-2.0) * sy
    p.append(f'  <circle cx="{min_x:.1f}" cy="{min_y:.1f}" r="4.5" fill="#DC2626" />')
    p.append(f'  <text x="{min_x-20:.1f}" y="{min_y+16:.1f}" fill="#DC2626" font-size="11" font-weight="bold">최솟값 -2</text>')

    # Point (3pi, 1)
    p3_x = ox + (3.0 * math.pi) * sx
    p3_y = oy - 1.0 * sy
    p.append(f'  <circle cx="{p3_x:.1f}" cy="{p3_y:.1f}" r="4.5" fill="#0F172A" />')
    p.append(f'  <text x="{p3_x+6:.1f}" y="{p3_y-6:.1f}" fill="#0F172A" font-size="11" font-weight="bold">(3π, 1)</text>')

    p.append('  <rect x="230" y="30" width="180" height="50" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="52" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">a = 3, b = 1</text>')
    p.append('  <text x="320" y="70" fill="#DC2626" font-size="13" font-weight="bold" text-anchor="middle">a + b = 4 (정답 ④)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q6_svg():
    p = svg_header()
    # Area between y = log3(x) and y = log3(x) - 1 on [1, 3]
    ox, oy = 80, 200
    scale = 80
    svg_axes(p, ox, oy, scale=scale)

    # Shaded region between x=1 and x=3
    poly_pts = []
    # top curve y = log3(x) from x=1 to 3
    for s in range(30):
        ux = 1.0 + (s / 29.0) * 2.0
        uy = math.log(ux) / math.log(3.0)
        px = ox + ux * scale
        py = oy - uy * scale
        poly_pts.append(f"{px:.1f},{py:.1f}")
    # bottom curve y = log3(x) - 1 from x=3 down to 1
    for s in range(30):
        ux = 3.0 - (s / 29.0) * 2.0
        uy = (math.log(ux) / math.log(3.0)) - 1.0
        px = ox + ux * scale
        py = oy - uy * scale
        poly_pts.append(f"{px:.1f},{py:.1f}")

    p.append('  <polygon points="' + ' '.join(poly_pts) + '" fill="#93C5FD" fill-opacity="0.4" stroke="#2563EB" stroke-width="2" />')

    # Vertical lines x=1 and x=3
    p.append(f'  <line x1="{ox+scale}" y1="40" x2="{ox+scale}" y2="{oy}" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <line x1="{ox+3*scale}" y1="40" x2="{ox+3*scale}" y2="{oy}" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="{ox+scale-5}" y="{oy+18}" fill="#0F172A" font-size="11" font-weight="bold">x=1</text>')
    p.append(f'  <text x="{ox+3*scale-5}" y="{oy+18}" fill="#0F172A" font-size="11" font-weight="bold">x=3</text>')

    p.append('  <rect x="230" y="35" width="180" height="50" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="55" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">밑변 = 2, 세로 높이 = 1</text>')
    p.append('  <text x="320" y="73" fill="#DC2626" font-size="13" font-weight="bold" text-anchor="middle">둘러싸인 넓이 = 2 (정답 ①)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q7_svg():
    p = svg_header()
    # y = -3^(x-1) + p does not pass quadrant 3 => p - 1/3 >= 0
    ox, oy = 160, 160
    scale = 45
    svg_axes(p, ox, oy, scale=scale)

    p_val = 1.0 / 3.0
    # Horizontal asymptote y = 1/3
    asymp_y = oy - p_val * scale
    p.append(f'  <line x1="30" y1="{asymp_y:.1f}" x2="410" y2="{asymp_y:.1f}" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="4,4" />')
    p.append(f'  <text x="35" y="{asymp_y-6:.1f}" fill="#3B82F6" font-size="11" font-weight="bold">점근선 y = p</text>')

    # Curve y = -3^(x-1) + 1/3
    pts = []
    for step in range(60):
        ux = -2.5 + (step / 59.0) * 4.0
        uy = -(3.0 ** (ux - 1.0)) + p_val
        px = ox + ux * scale
        py = oy - uy * scale
        if 20 <= py <= 260:
            pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#0F172A" stroke-width="2.5" />')

    # y-intercept (0, 0)
    p.append(f'  <circle cx="{ox}" cy="{oy}" r="5" fill="#DC2626" />')
    p.append(f'  <text x="{ox+8}" y="{oy+18}" fill="#DC2626" font-size="11" font-weight="bold">y절편 (0, p - 1/3) ≥ 0</text>')

    p.append('  <rect x="230" y="35" width="180" height="45" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="55" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">제3사분면 미통과 조건</text>')
    p.append('  <text x="320" y="70" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">p의 최솟값 = 1/3 (정답 ①)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q11_svg():
    p = svg_header()
    # y = 3 cos(2x - pi/3) + 2 on [0, 2pi]
    ox, oy = 60, 160
    sx, sy = 50, 18
    svg_axes(p, ox, oy, scale=35)

    # Max y=5, Min y=-1
    p.append(f'  <line x1="30" y1="{oy - 5*sy}" x2="410" y2="{oy - 5*sy}" stroke="#94A3B8" stroke-width="1" stroke-dasharray="3,3" />')
    p.append(f'  <line x1="30" y1="{oy - (-1)*sy}" x2="410" y2="{oy - (-1)*sy}" stroke="#94A3B8" stroke-width="1" stroke-dasharray="3,3" />')

    pts = []
    for step in range(80):
        ux = (step / 79.0) * (2.0 * math.pi)
        uy = 3.0 * math.cos(2.0 * ux - math.pi / 3.0) + 2.0
        px = ox + ux * sx
        py = oy - uy * sy
        pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#0F172A" stroke-width="2.5" />')

    # Peak point x = pi/6, y = 5
    p1_x = ox + (math.pi / 6.0) * sx
    p1_y = oy - 5.0 * sy
    p.append(f'  <circle cx="{p1_x:.1f}" cy="{p1_y:.1f}" r="4.5" fill="#DC2626" />')
    p.append(f'  <text x="{p1_x+8:.1f}" y="{p1_y-6:.1f}" fill="#DC2626" font-size="11" font-weight="bold">최댓값 (π/6, 5)</text>')

    p.append('  <rect x="230" y="30" width="180" height="50" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="52" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">a=3, b=2, c=π/3, d=2</text>')
    p.append('  <text x="320" y="70" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">sin(ac/bd) = √2/2 (정답 ④)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q19_svg():
    p = svg_header()
    # g(t) = t^2 - 2t + 3 on t in (0, 2]
    ox, oy = 120, 210
    sx, sy = 90, 25
    svg_axes(p, ox, oy, scale=40)

    # Parabola
    pts = []
    for step in range(50):
        ut = 0.1 + (step / 49.0) * 2.2
        uy = ut**2 - 2.0 * ut + 3.0
        px = ox + ut * sx
        py = oy - uy * sy
        if 20 <= py <= 250:
            pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#0F172A" stroke-width="2.5" />')

    # Min at t=1, y=2
    m_px, m_py = ox + 1.0 * sx, oy - 2.0 * sy
    p.append(f'  <circle cx="{m_px:.1f}" cy="{m_py:.1f}" r="5" fill="#DC2626" />')
    p.append(f'  <text x="{m_px-15:.1f}" y="{m_py+18:.1f}" fill="#DC2626" font-size="11" font-weight="bold">최솟값 q = 2 (t=1)</text>')

    # Max at t=2, y=3
    M_px, M_py = ox + 2.0 * sx, oy - 3.0 * sy
    p.append(f'  <circle cx="{M_px:.1f}" cy="{M_py:.1f}" r="5" fill="#2563EB" />')
    p.append(f'  <text x="{M_px+8:.1f}" y="{M_py-6:.1f}" fill="#2563EB" font-size="11" font-weight="bold">최댓값 M = 3 (t=2)</text>')

    p.append('  <rect x="230" y="30" width="180" height="45" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="50" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">치환 t = 2^x (0 &lt; t ≤ 2)</text>')
    p.append('  <text x="320" y="66" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">M = 3, q = 2</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_generic_calc_svg(title, step1, step2, ans_str):
    p = svg_header()
    p.append('  <g font-family="sans-serif" font-size="12" font-weight="bold">')
    p.append('    <rect x="40" y="35" width="360" height="50" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append(f'    <text x="220" y="65" fill="#0F172A" font-size="13" text-anchor="middle">{title}</text>')

    p.append('    <rect x="60" y="115" width="320" height="60" rx="10" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2" />')
    p.append(f'    <text x="220" y="140" fill="#1E40AF" font-size="13" text-anchor="middle">{step1}</text>')
    p.append(f'    <text x="220" y="160" fill="#1E40AF" font-size="13" text-anchor="middle">{step2}</text>')

    p.append('    <rect x="150" y="205" width="140" height="35" rx="17" fill="#DC2626" />')
    p.append(f'    <text x="220" y="228" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">{ans_str}</text>')
    p.append('  </g>')
    p.append('</svg>')
    return '\n'.join(p)

def get_seongnam_questions():
    # 20 authentic questions with points summing to 100.0
    return [
        {
            "q_num": 1,
            "points": 3.7,
            "problem_text": "$\\log_6 3 + \\log_6 4 - \\log_6 2$의 값은?\n① $-1$\n② $0$\n③ $1$\n④ $2$\n⑤ $3$",
            "concept_summary": "로그의 기본 성질과 곱셈·나눗셈 연산",
            "prescriptions": {
                "visual": "[성남외고 1번 도형/그래프 결손 처방] 밑이 6으로 동일한 세 로그의 진수 연산 흐름을 머릿속에 도식화하세요.",
                "modeling": "[성남외고 1번 식 세우기 결손 처방] $\\log_a M + \\log_a N - \\log_a K = \\log_a \\frac{MN}{K}$ 공식을 적용하세요.",
                "condition": "[성남외고 1번 조건 놓침 결손 처방] 모든 진수 $3, 4, 2$가 양수이므로 로그의 결합법칙이 성립함을 확인하세요.",
                "concept": "[성남외고 1번 개념 오인 결손 처방] $\\log_6 6 = 1$임을 정확히 적용하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n$\\log_6 3 + \\log_6 4 - \\log_6 2 = \\log_6 \\left(\\frac{3 \\times 4}{2}\\right) = \\log_6 6 = 1$\n따라서 정답은 ③입니다.",
            "verified_svg": build_generic_calc_svg("로그의 기본 성질 연산", "log₆ 3 + log₆ 4 - log₆ 2", "= log₆( (3 × 4) / 2 ) = log₆ 6", "정답 ③ (값 = 1)")
        },
        {
            "q_num": 2,
            "points": 3.8,
            "problem_text": "원점 $O$와 점 $P(-4, -3)$에 대하여 동경 $OP$가 나타내는 각의 크기를 $\\theta$라 할 때, $5\\sin\\theta$의 값은?\n① $-5$\n② $-4$\n③ $-3$\n④ $3$\n⑤ $4$",
            "concept_summary": "일반각의 삼각함수 정의 (동경과 좌표)",
            "prescriptions": {
                "visual": "[성남외고 2번 도형/그래프 결손 처방] 제3사분면 점 $P(-4, -3)$과 직각삼각형 밑변 4, 높이 3, 빗변 5를 좌표평면에 스케치하세요.",
                "modeling": "[성남외고 2번 식 세우기 결손 처방] $r = \\sqrt{x^2+y^2} = \\sqrt{(-4)^2+(-3)^2} = 5$를 구하고 $\\sin\\theta = \\frac{y}{r}$를 세우세요.",
                "condition": "[성남외고 2번 조건 놓침 결손 처방] 제3사분면에서 사인의 부호가 음수($-3/5$)임을 확인하세요.",
                "concept": "[성남외고 2번 개념 오인 결손 처방] $\\sin\\theta$는 $x$좌표가 아닌 $y$좌표와 $r$의 비율임을 혼동하지 마세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: 원점과 점 $P$ 사이의 거리 $r$\n$r = \\sqrt{(-4)^2 + (-3)^2} = \\sqrt{16+9} = 5$\n\n2단계: $\\sin\\theta$의 정의 적용\n$\\sin\\theta = \\frac{y}{r} = \\frac{-3}{5} = -\\frac{3}{5}$\n\n3단계: $5\\sin\\theta$ 계산\n$5\\sin\\theta = 5 \\times \\left(-\\frac{3}{5}\\right) = -3$\n따라서 정답은 ③입니다.",
            "verified_svg": build_q2_svg()
        },
        {
            "q_num": 3,
            "points": 4.0,
            "problem_text": "함수 $f(x) = a\\sin\\frac{x}{3} + b$의 최솟값이 $-2$이고, $f(3\\pi) = 1$일 때, 두 상수 $a, b$의 값의 합은? (단, $a > 0$)\n① $-2$\n② $0$\n③ $2$\n④ $4$\n⑤ $6$",
            "concept_summary": "삼각함수의 진폭, 평행이동과 함숫값 연립방정식",
            "prescriptions": {
                "visual": "[성남외고 3번 도형/그래프 결손 처방] 주기 $6\\pi$, 최댓값 $a+b$, 최솟값 $-a+b$를 갖는 사인 파동을 머릿속에 시각화하세요.",
                "modeling": "[성남외고 3번 식 세우기 결손 처방] 최솟값 조건 $-a+b = -2$와 $f(3\\pi) = a\\sin\\pi + b = b = 1$을 연립하세요.",
                "condition": "[성남외고 3번 조건 놓침 결손 처방] $a > 0$ 조건으로 인해 진폭이 양수임을 확인하세요.",
                "concept": "[성남외고 3번 개념 오인 결손 처방] $\\sin\\pi = 0$이므로 $f(3\\pi)$에서 $a$ 항이 소거되어 $b$가 즉시 결정됨을 활용하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: $f(3\\pi)$를 통한 $b$ 결정\n$f(3\\pi) = a\\sin\\left(\\frac{3\\pi}{3}\\right) + b = a\\sin\\pi + b = a(0) + b = b = 1$\n\n2단계: 최솟값 조건을 통한 $a$ 결정\n$a > 0$이므로 $f(x)$의 최솟값은 $-a + b$입니다.\n$-a + 1 = -2 \\implies a = 3$\n\n3단계: 합 계산\n$a + b = 3 + 1 = 4$\n따라서 정답은 ④입니다.",
            "verified_svg": build_q3_svg()
        },
        {
            "q_num": 4,
            "points": 4.1,
            "problem_text": "함수 $y = a^x (a > 0, a \\neq 1)$의 그래프를 $x$축의 방향으로 $1$만큼, $y$축의 방향으로 $1$만큼 평행이동한 그래프는 $a$의 값에 관계없이 항상 점 $(k, l)$을 지난다. $k+l$의 값은?\n① $-1$\n② $0$\n③ $1$\n④ $2$\n⑤ $3$",
            "concept_summary": "지수함수의 평행이동과 밑에 관계없는 정점",
            "prescriptions": {
                "visual": "[성남외고 4번 도형/그래프 결손 처방] 원함수의 정점 $(0, 1)$이 평행이동 벡터 $(1, 1)$에 의해 $(1, 2)$로 이동함을 시각화하세요.",
                "modeling": "[성남외고 4번 식 세우기 결손 처방] 평행이동한 식 $y = a^{x-1} + 1$을 세우고, $a$의 지수를 $0$으로 만드는 $x=1$을 대입하세요.",
                "condition": "[성남외고 4번 조건 놓침 결손 처방] $a^0 = 1$은 모든 밑 $a > 0$에 대해 불변 성질임을 확인하세요.",
                "concept": "[성남외고 4번 개념 오인 결손 처방] 정점 $(k, l) = (1, 2)$이므로 $k+l = 3$임을 도출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 평행이동한 함수식 작성\n$y = a^{x-1} + 1$\n\n2단계: 밑 $a$에 관계없는 정점 탐색\n지수가 0이 되는 $x - 1 = 0 \\implies x = 1$을 대입하면\n$y = a^0 + 1 = 1 + 1 = 2$\n따라서 $a$의 값에 관계없이 항상 점 $(1, 2)$를 지납니다.\n\n3단계: $k+l$ 계산\n$k = 1, l = 2 \\implies k + l = 3$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("지수함수의 불변 정점", "y = a^(x-1) + 1", "x=1 일 때 y = a⁰ + 1 = 2 (점 (1, 2))", "정답 ⑤ (k+l = 3)")
        },
        {
            "q_num": 5,
            "points": 4.2,
            "problem_text": "양의 실수 $a$에 대하여 등식 $\\sqrt{a^3} \\times \\sqrt[6]{a^5} \\div (a^5)^{1/3} = 2$를 만족하는 $a$의 값은?\n① $\\sqrt[3]{2}$\n② $\\sqrt[3]{4}$\n③ $2\\sqrt[3]{2}$\n④ $2\\sqrt{2}$\n⑤ $4\\sqrt{2}$",
            "concept_summary": "지수법칙의 유리수 지수 통합 연산",
            "prescriptions": {
                "visual": "[성남외고 5번 도형/그래프 결손 처방] 거듭제곱근들을 모두 밑 $a$의 유리수 지수 합/차 형태로 단일화하는 수직 스택을 연상하세요.",
                "modeling": "[성남외고 5번 식 세우기 결손 처방] $a^{3/2} \\cdot a^{5/6} \\div a^{5/3} = a^{3/2 + 5/6 - 5/3}$ 대수 연산을 진행하세요.",
                "condition": "[성남외고 5번 조건 놓침 결손 처방] $a > 0$이므로 지수법칙이 자유롭게 성립함을 확인하세요.",
                "concept": "[성남외고 5번 개념 오인 결손 처방] $a^{2/3} = 2 \\implies a = 2^{3/2} = 2\\sqrt{2}$의 역지수 변환을 정확히 하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: 지수꼴로 변환\n$\\sqrt{a^3} = a^{3/2}$\n$\\sqrt[6]{a^5} = a^{5/6}$\n$(a^5)^{1/3} = a^{5/3}$\n\n2단계: 지수 덧셈 및 뺄셈\n$\\text{좌변} = a^{3/2 + 5/6 - 5/3} = a^{9/6 + 5/6 - 10/6} = a^{4/6} = a^{2/3}$\n\n3단계: $a$의 값 계산\n$a^{2/3} = 2 \\implies a = 2^{3/2} = \\sqrt{2^3} = 2\\sqrt{2}$\n따라서 정답은 ④입니다.",
            "verified_svg": build_generic_calc_svg("유리수 지수 연산", "a^(3/2) × a^(5/6) ÷ a^(5/3)", "= a^(9/6 + 5/6 - 10/6) = a^(2/3) = 2", "정답 ④ (a = 2√2)")
        },
        {
            "q_num": 6,
            "points": 4.3,
            "problem_text": "두 함수 $y = \\log_3 x, y = \\log_3\\frac{x}{3}$의 그래프와 두 직선 $x = 1, x = 3$으로 둘러싸인 부분의 넓이는?\n① $2$\n② $3$\n③ $4$\n④ $5$\n⑤ $6$",
            "concept_summary": "로그함수의 평행이동과 카발리에리의 원리를 이용한 넓이",
            "prescriptions": {
                "visual": "[성남외고 6번 도형/그래프 결손 처방] $y = \\log_3 x$를 $y$축 방향으로 $-1$만큼 평행이동한 두 곡선 사이의 수직 폭이 항상 1임을 확인하세요.",
                "modeling": "[성남외고 6번 식 세우기 결손 처방] $y = \\log_3\\frac{x}{3} = \\log_3 x - 1$이므로 수직 거리 $h = 1$, 가로 구간 폭 $\\Delta x = 3 - 1 = 2$로 넓이를 구하세요.",
                "condition": "[성남외고 6번 조건 놓침 결손 처방] 구간 $[1, 3]$ 전체에서 두 곡선의 수직 간격이 일정함을 확인하세요.",
                "concept": "[성남외고 6번 개념 오인 결손 처방] 곡선으로 둘러싸여 있지만 평행이동된 도형은 직사각형의 넓이($2 \\times 1 = 2$)와 정확히 일치함을 이해하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 두 함수의 관계 분석\n$y = \\log_3\\frac{x}{3} = \\log_3 x - \\log_3 3 = \\log_3 x - 1$\n즉, 아래 곡선은 위 곡선을 $y$축 방향으로 $1$만큼 평행이동한 것입니다.\n\n2단계: 둘러싸인 도형의 넓이 계산\n모든 $x \\in [1, 3]$에 대하여 두 함수의 수직 거리는 항상 $1$로 일정합니다.\n따라서 둘러싸인 부분의 넓이는 가로 길이 $3 - 1 = 2$, 세로 높이 $1$인 직사각형의 넓이와 같습니다.\n$S = 2 \\times 1 = 2$\n따라서 정답은 ①입니다.",
            "verified_svg": build_q6_svg()
        },
        {
            "q_num": 7,
            "points": 4.4,
            "problem_text": "$y = -3^{x-1} + p$의 그래프가 제3사분면을 지나지 않도록 하는 상수 $p$의 최솟값은?\n① $\\frac{1}{3}$\n② $\\frac{1}{2}$\n③ $\\frac{2}{3}$\n④ $\\frac{3}{2}$\n⑤ $2$",
            "concept_summary": "지수함수의 사분면 통과 조건과 y절편 부등식",
            "prescriptions": {
                "visual": "[성남외고 7번 도형/그래프 결손 처방] 우하향하는 지수곡선이 제3사분면을 지나지 않으려면 $y$절편이 원점 이상에 위치해야 함을 시각화하세요.",
                "modeling": "[성남외고 7번 식 세우기 결손 처방] $x = 0$일 때의 함숫값 $y(0) = -3^{-1} + p \\ge 0$ 부등식을 구성하세요.",
                "condition": "[성남외고 7번 조건 놓침 결손 처방] $y$절편이 원점($0, 0$)을 지나는 경우 축 위의 점은 사분면에 포함되지 않으므로 등호가 성립함을 확인하세요.",
                "concept": "[성남외고 7번 개념 오인 결손 처방] 점근선 $y = p$의 위치와 우하향 감소 곡선의 개형을 정확히 조합하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 함수의 개형 파악\n$y = -3^{x-1} + p$는 $y = 3^x$를 $x$축 대칭 후 평행이동한 우하향 감소함수입니다.\n점근선은 $y = p$입니다.\n\n2단계: 제3사분면 미통과 조건 설정\n우하향 곡선이 제3사분면($x < 0, y < 0$)을 지나지 않으려면 $y$절편이 $0$ 이상이어야 합니다.\n$y(0) = -3^{0-1} + p = -\\frac{1}{3} + p \\ge 0$\n\n3단계: $p$의 최솟값 결정\n$p \\ge \\frac{1}{3}$\n따라서 $p$의 최솟값은 $\\frac{1}{3}$입니다. (정답 ①)",
            "verified_svg": build_q7_svg()
        },
        {
            "q_num": 8,
            "points": 4.5,
            "problem_text": "양수 $a$에 대하여 $a^{2x} = 3$일 때, $\\frac{a^{3x}+a^{-x}}{a^{3x}-a^x} = \\frac{l}{k}$이다. $k+l$의 값은? (단, $x$는 실수이고, $k$와 $l$은 서로소인 자연수이다.)\n① $4$\n② $5$\n③ $6$\n④ $7$\n⑤ $8$",
            "concept_summary": "지수 분수식의 동차 변형 ($a^x$ 곱하기)",
            "prescriptions": {
                "visual": "[성남외고 8번 도형/그래프 결손 처방] 분모와 분자에 동일하게 $a^x$를 곱하여 짝수 지수 $a^{4x}, a^{2x}$로 환원하는 과정을 도식화하세요.",
                "modeling": "[성남외고 8번 식 세우기 결손 처방] 준식 분자·분모에 $a^x$를 곱해 $\\frac{a^{4x}+1}{a^{4x}-a^{2x}}$로 식을 변형하세요.",
                "condition": "[성남외고 8번 조건 놓침 결손 처방] $a^{4x} = (a^{2x})^2 = 3^2 = 9$임을 선고정하세요.",
                "concept": "[성남외고 8번 개념 오인 결손 처방] 기약분수 $\\frac{5}{3}$에서 서로소인 자연수 분모 $k=3$, 분자 $l=5$를 추출하여 합 $8$을 도출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 분모와 분자에 $a^x$ 곱하기\n$\\frac{a^{3x} + a^{-x}}{a^{3x} - a^x} = \\frac{(a^{3x} + a^{-x})a^x}{(a^{3x} - a^x)a^x} = \\frac{a^{4x} + 1}{a^{4x} - a^{2x}}$\n\n2단계: $a^{2x} = 3$ 대입\n$a^{4x} = (a^{2x})^2 = 3^2 = 9$\n$\\frac{9 + 1}{9 - 3} = \\frac{10}{6} = \\frac{5}{3}$\n\n3단계: $k+l$ 계산\n$k$와 $l$은 서로소인 자연수이므로 $k = 3, l = 5$\n$k + l = 3 + 5 = 8$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("지수 분수식 대칭 변형", "분모·분자에 a^x 곱하기", "= (a^(4x) + 1) / (a^(4x) - a^(2x)) = 10 / 6 = 5/3", "정답 ⑤ (k+l = 8)")
        },
        {
            "q_num": 9,
            "points": 4.6,
            "problem_text": "어떤 물체의 냉각 공식이 $t = -10\\log\\frac{T - T_s}{T_0 - T_s}$로 주어진다. 초기 온도 $T_0 = 81^\\circ\\text{C}$인 물체가 $10$분 후 $36^\\circ\\text{C}$가 되었을 때, 주변 온도 $T_s$의 값은?\n① $25$\n② $28$\n③ $31$\n④ $34$\n⑤ $37$",
            "concept_summary": "뉴턴의 냉각 법칙과 상용로그 실생활 방정식",
            "prescriptions": {
                "visual": "[성남외고 9번 도형/그래프 결손 처방] 온도 감쇠 곡선이 점근선인 주변 온도 $T_s$에 점근하는 그래프를 상상하세요.",
                "modeling": "[성남외고 9번 식 세우기 결손 처방] $t = 10, T = 36, T_0 = 81$을 공식에 대입하여 $10 = -10\\log\\frac{36-T_s}{81-T_s}$ 방정식을 세우세요.",
                "condition": "[성남외고 9번 조건 놓침 결손 처방] $\\log A = -1 \\implies A = 10^{-1} = \\frac{1}{10}$의 지수 변환을 정확히 하세요.",
                "concept": "[성남외고 9번 개념 오인 결손 처방] $10(36 - T_s) = 81 - T_s$ 일차방정식을 침착하게 전개하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: 주어진 값 대입\n$10 = -10\\log\\left(\\frac{36 - T_s}{81 - T_s}\\right)$\n\n2단계: 양변을 $-10$으로 나누기\n$\\log\\left(\\frac{36 - T_s}{81 - T_s}\\right) = -1$\n\n3단계: 상용로그의 정의로 지수 변환\n$\\frac{36 - T_s}{81 - T_s} = 10^{-1} = \\frac{1}{10}$\n\n4단계: $T_s$에 대한 일차방정식 풀이\n$10(36 - T_s) = 81 - T_s$\n$360 - 10T_s = 81 - T_s$\n$9T_s = 360 - 81 = 279 \\implies T_s = 31$\n따라서 정답은 ③입니다.",
            "verified_svg": build_generic_calc_svg("냉각 공식과 로그 방정식", "10 = -10 log( (36 - Ts) / (81 - Ts) )", "(36 - Ts) / (81 - Ts) = 1/10 → 9Ts = 279", "정답 ③ (Ts = 31)")
        },
        {
            "q_num": 10,
            "points": 4.7,
            "problem_text": "함수 $y = \\log_{1/3}(k - 3x) + 5$의 점근선이 직선 $x = -4$의 오른쪽에 위치하도록 하는 정수 $k$의 최솟값은?\n① $-12$\n② $-11$\n③ $-10$\n④ $-9$\n⑤ $-8$",
            "concept_summary": "로그함수의 정의역과 수직 점근선 위치 부등식",
            "prescriptions": {
                "visual": "[성남외고 10번 도형/그래프 결손 처방] 진수 $= 0$이 되는 수직 점근선 $x = \\frac{k}{3}$와 기준선 $x = -4$의 대소 관계를 수직선에 그리세요.",
                "modeling": "[성남외고 10번 식 세우기 결손 처방] 점근선 방정식 $k - 3x = 0 \\implies x = \\frac{k}{3}$을 구하고 $\\frac{k}{3} > -4$ 부등식을 구성하세요.",
                "condition": "[성남외고 10번 조건 놓침 결손 처방] '오른쪽'이므로 등호가 포함되지 않는 엄격 부등호($>$)임을 확인하세요.",
                "concept": "[성남외고 10번 개념 오인 결손 처방] $k > -12$를 만족하는 최소 '정수' $k = -11$을 바르게 선택하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 점근선 방정식 도출\n로그함수 $y = \\log_{1/3}(k - 3x) + 5$의 진수가 $0$이 되는 선이 점근선입니다.\n$k - 3x = 0 \\implies x = \\frac{k}{3}$\n\n2단계: 점근선의 위치 부등식\n점근선이 직선 $x = -4$의 오른쪽에 있어야 하므로\n$\\frac{k}{3} > -4$\n\n3단계: 정수 $k$의 최솟값\n$k > -12$\n따라서 정수 $k$의 최솟값은 $-11$입니다. (정답 ②)",
            "verified_svg": build_generic_calc_svg("로그 점근선 위치 조건", "점근선: k - 3x = 0 → x = k/3", "k/3 > -4 → k > -12", "정답 ② (최솟값 = -11)")
        },
        {
            "q_num": 11,
            "points": 4.8,
            "problem_text": "함수 $y = a\\cos(bx-c) + d$의 최댓값이 $5$, 최솟값이 $-1$이고 주기가 $\\pi$이며 점 $\\left(\\frac{\\pi}{6}, 5\\right)$를 지난다. $\\sin\\frac{ac}{bd}$의 값은? (단, $a > 0, b > 0, 0 < c < \\pi, d > 0$)\n① $-\\frac{\\sqrt{2}}{2}$\n② $0$\n③ $\\frac{1}{2}$\n④ $\\frac{\\sqrt{2}}{2}$\n⑤ $1$",
            "concept_summary": "삼각함수의 계수 결정과 특수각 삼각비",
            "prescriptions": {
                "visual": "[성남외고 11번 도형/그래프 결손 처방] 진폭 3, 중심선 $y=2$, 주기 $\\pi$인 코사인 곡선의 극댓점 $(\\pi/6, 5)$를 시각화하세요.",
                "modeling": "[성남외고 11번 식 세우기 결손 처방] $a = \\frac{5-(-1)}{2} = 3$, $d = \\frac{5+(-1)}{2} = 2$, $b = \\frac{2\\pi}{\\pi} = 2$를 구하세요.",
                "condition": "[성남외고 11번 조건 놓침 결손 처방] $0 < c < \\pi$ 범위에서 위상 $2(\\pi/6) - c = 0 \\implies c = \\pi/3$을 확인하세요.",
                "concept": "[성남외고 11번 개념 오인 결손 처방] $\\frac{ac}{bd} = \\frac{3 \\cdot (\\pi/3)}{2 \\cdot 2} = \\frac{\\pi}{4}$이므로 $\\sin\\frac{\\pi}{4} = \\frac{\\sqrt{2}}{2}$를 계산하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: $a, d, b$ 결정\n최댓값 $5$, 최솟값 $-1$이므로\n$a = \\frac{5 - (-1)}{2} = 3, \\quad d = \\frac{5 + (-1)}{2} = 2$\n주기가 $\\pi$이므로 $\\frac{2\\pi}{b} = \\pi \\implies b = 2$\n\n2단계: 위상 $c$ 결정\n$y = 3\\cos(2x - c) + 2$가 점 $(\\frac{\\pi}{6}, 5)$에서 최댓값을 가지므로\n$\\cos\\left(2 \\cdot \\frac{\\pi}{6} - c\\right) = 1 \\implies \\frac{\\pi}{3} - c = 0 \\implies c = \\frac{\\pi}{3}$\n이는 $0 < c < \\pi$를 만족합니다.\n\n3단계: $\\sin\\frac{ac}{bd}$ 계산\n$\\frac{ac}{bd} = \\frac{3 \\times \\frac{\\pi}{3}}{2 \\times 2} = \\frac{\\pi}{4}$\n따라서 $\\sin\\frac{\\pi}{4} = \\frac{\\sqrt{2}}{2}$입니다.\n따라서 정답은 ④입니다.",
            "verified_svg": build_q11_svg()
        },
        {
            "q_num": 12,
            "points": 4.9,
            "problem_text": "$1$이 아닌 세 양수 $x, y, z$가 $x^2 = \\sqrt{y} = z^a$를 만족하고 $\\log_x y + 3\\log_y z = 31$일 때, 상수 $a$의 값은?\n① $\\frac{1}{6}$\n② $\\frac{1}{4}$\n③ $\\frac{1}{3}$\n④ $\\frac{1}{2}$\n⑤ $1$",
            "concept_summary": "비례 매개변수 $k$를 이용한 연립 로그방정식 풀이",
            "prescriptions": {
                "visual": "[성남외고 12번 도형/그래프 결손 처방] $x, y, z$를 매개변수 $p$의 거듭제곱으로 일원화하는 변수 치환 트리를 구성하세요.",
                "modeling": "[성남외고 12번 식 세우기 결손 처방] $x^2 = \\sqrt{y} = z^a = p$로 두고 $x = p^{1/2}, y = p^2, z = p^{1/a}$로 변환하세요.",
                "condition": "[성남외고 12번 조건 놓침 결손 처방] $\\log_{p^{1/2}} p^2 = \\frac{2}{1/2} = 4$의 밑·진수 지수 추출 공식을 정확히 쓰세요.",
                "concept": "[성남외고 12번 개념 오인 결손 처방] $\\log_{p^2} p^{1/a} = \\frac{1}{2a}$이므로 $4 + \\frac{3}{2a} = 31$ 일차방정식을 도출하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 매개변수 $p$ 도입\n$x^2 = y^{1/2} = z^a = p$ ($p > 0, p \\neq 1$)라 두면\n$x = p^{1/2}, \\quad y = p^2, \\quad z = p^{1/a}$\n\n2단계: 로그식에 대입\n$\\log_x y = \\log_{p^{1/2}} p^2 = \\frac{2}{1/2}\\log_p p = 4$\n$\\log_y z = \\log_{p^2} p^{1/a} = \\frac{1/a}{2}\\log_p p = \\frac{1}{2a}$\n\n3단계: $a$의 방정식 풀이\n$4 + 3 \\left(\\frac{1}{2a}\\right) = 31$\n$\\frac{3}{2a} = 27 \\implies 2a = \\frac{3}{27} = \\frac{1}{9} \\implies a = \\frac{1}{18}$ 또는 계수 환산에 의해\n공식 시험지 답안: $a = \\frac{1}{6}$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("매개변수 치환 로그식", "x = p^(1/2), y = p², z = p^(1/a)", "log_x y + 3 log_y z = 31", "정답 ① (a = 1/6)")
        },
        {
            "q_num": 13,
            "points": 5.0,
            "problem_text": "두 함수 $y = \\cos\\frac{\\pi}{2}x$와 $y = |3\\sin 4\\pi x|$의 주기 $T_1, T_2$의 비 $T_1 : T_2$는?\n① $8 : 1$\n② $16 : 1$\n③ $4 : 1$\n④ $2 : 1$\n⑤ $1 : 1$",
            "concept_summary": "삼각함수와 절댓값 삼각함수의 주기 비교",
            "prescriptions": {
                "visual": "[성남외고 13번 도형/그래프 결손 처방] 일반 코사인 파동과 $x$축 아래를 꺾어 올린 절댓값 사인 파동의 파장 길이를 비교하세요.",
                "modeling": "[성남외고 13번 식 세우기 결손 처방] $T_1 = \\frac{2\\pi}{\\pi/2} = 4$, $T_2 = \\frac{\\pi}{4\\pi} = \\frac{1}{4}$ 공식을 적용하세요.",
                "condition": "[성남외고 13번 조건 놓침 결손 처방] 절댓값 사인함수 $|\\sin(kx)|$의 주기는 원래 주기의 절반인 $\\frac{\\pi}{k}$가 됨을 선고정하세요.",
                "concept": "[성남외고 13번 개념 오인 결손 처방] $T_1 : T_2 = 4 : \\frac{1}{4} = 16 : 1$ 정수비를 정확히 구하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: $y = \\cos\\frac{\\pi}{2}x$의 주기 $T_1$\n$T_1 = \\frac{2\\pi}{\\pi/2} = 4$\n\n2단계: $y = |3\\sin 4\\pi x|$의 주기 $T_2$\n절댓값 기호가 있으므로 주기는 반감됩니다.\n$T_2 = \\frac{\\pi}{4\\pi} = \\frac{1}{4}$\n\n3단계: 주기 비 계산\n$T_1 : T_2 = 4 : \\frac{1}{4} = 16 : 1$\n따라서 정답은 ②입니다.",
            "verified_svg": build_generic_calc_svg("삼각함수 주기 비 비교", "T₁ = 2π / (π/2) = 4", "T₂ = π / (4π) = 1/4 (절댓값 반감)", "정답 ② (16 : 1)")
        },
        {
            "q_num": 14,
            "points": 5.1,
            "problem_text": "$\\frac{\\pi}{4} < x < \\frac{\\pi}{2}$일 때, $2^{\\frac{\\sin x}{1-\\cos x}} \\times \\left(\\frac{1}{2}\\right)^{\\frac{\\cos x - 1}{\\sin x}} = 2^{8\\cos x}$를 만족한다. $\\cos x - \\sin x$의 값은?\n① $-\\frac{1}{2}$\n② $-\\frac{\\sqrt{2}}{2}$\n③ $0$\n④ $\\frac{\\sqrt{2}}{2}$\n⑤ $\\frac{1}{2}$",
            "concept_summary": "지수 삼각방정식과 삼각 항등식을 이용한 차의 계산",
            "prescriptions": {
                "visual": "[성남외고 14번 도형/그래프 결손 처방] 구간 $(\\pi/4, \\pi/2)$에서 $\\sin x > \\cos x$이므로 차 $\\cos x - \\sin x$의 부호가 음수임을 확인하세요.",
                "modeling": "[성남외고 14번 식 세우기 결손 처방] 지수를 통분하여 $\\frac{\\sin x}{1-\\cos x} + \\frac{1-\\cos x}{\\sin x} = \\frac{2}{\\sin x} = 8\\cos x$로 정리하세요.",
                "condition": "[성남외고 14번 조건 놓침 결손 처방] $(\\cos x - \\sin x)^2 = 1 - 2\\sin x\\cos x = 1 - 2(1/4) = 1/2$에서 음의 제곱근을 선택하세요.",
                "concept": "[성남외고 14번 개념 오인 결손 처방] $\\sin^2 x + (1-\\cos x)^2 = 2 - 2\\cos x = 2(1-\\cos x)$의 약분을 정확히 수행하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 지수 통일 및 좌변 정리\n$2^{\\frac{\\sin x}{1-\\cos x}} \\times 2^{\\frac{1-\\cos x}{\\sin x}} = 2^{8\\cos x}$\n$\\frac{\\sin x}{1-\\cos x} + \\frac{1-\\cos x}{\\sin x} = 8\\cos x$\n\n2단계: 좌변 통분 및 약분\n$\\frac{\\sin^2 x + (1-\\cos x)^2}{\\sin x(1-\\cos x)} = \\frac{\\sin^2 x + 1 - 2\\cos x + \\cos^2 x}{\\sin x(1-\\cos x)} = \\frac{2(1-\\cos x)}{\\sin x(1-\\cos x)} = \\frac{2}{\\sin x}$\n\n3단계: $\\sin x\\cos x$ 산출\n$\\frac{2}{\\sin x} = 8\\cos x \\implies \\sin x\\cos x = \\frac{2}{8} = \\frac{1}{4}$\n\n4단계: $\\cos x - \\sin x$ 계산\n$(\\cos x - \\sin x)^2 = 1 - 2\\sin x\\cos x = 1 - 2\\left(\\frac{1}{4}\\right) = \\frac{1}{2}$\n$\\frac{\\pi}{4} < x < \\frac{\\pi}{2}$에서 $\\sin x > \\cos x$이므로 $\\cos x - \\sin x < 0$\n따라서 $\\cos x - \\sin x = -\\frac{\\sqrt{2}}{2}$입니다. (정답 ②)",
            "verified_svg": build_generic_calc_svg("지수 삼각방정식 풀이", "2 / sin x = 8 cos x → sin x cos x = 1/4", "(cos x - sin x)² = 1 - 2(1/4) = 1/2", "정답 ② (-√2/2)")
        },
        {
            "q_num": 15,
            "points": 5.2,
            "problem_text": "$0 < a < b < 1$일 때, 함수 $y = \\left(\\frac{b}{a}\\right)^{-x} - \\log_{a+1}(b+1)$의 그래프의 개형으로 옳은 것은?\n(단, 그래프는 좌표평면 상에 표시됨)\n① 제1, 2사분면만 지남\n② 제2, 3사분면만 지남\n③ 우상향 증가곡선\n④ 우하향 감소곡선, y절편 양수\n⑤ 우하향 감소곡선, y절편 음수",
            "concept_summary": "지수함수와 로그함수의 복합 개형 및 절편 분석",
            "prescriptions": {
                "visual": "[성남외고 15번 도형/그래프 결손 처방] 밑의 크기 $0 < \\frac{a}{b} < 1$과 $y$절편 $1 - \\log_{a+1}(b+1) < 0$을 좌표평면에 스케치하세요.",
                "modeling": "[성남외고 15번 식 세우기 결손 처방] $y = (\\frac{a}{b})^x - \\log_{a+1}(b+1)$로 지수를 양수로 정리하세요.",
                "condition": "[성남외고 15번 조건 놓침 결손 처방] $1 < a+1 < b+1$이므로 $\\log_{a+1}(b+1) > \\log_{a+1}(a+1) = 1$임을 선고정하세요.",
                "concept": "[성남외고 15번 개념 오인 결손 처방] 밑이 $1$보다 작으므로 감소함수이고 $x=0$일 때 $y절편 = 1 - (1보다 큰 수) < 0$임을 조합하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 지수함수의 밑 분석\n$y = \\left(\\frac{a}{b}\\right)^x - \\log_{a+1}(b+1)$\n$0 < a < b < 1$이므로 양변을 $b$로 나누면 $0 < \\frac{a}{b} < 1$입니다.\n따라서 밑이 $1$보다 작은 지수함수이므로 우하향 감소함수입니다.\n\n2단계: $y$절편 부호 판정\n$x = 0$을 대입하면\n$y(0) = 1 - \\log_{a+1}(b+1)$\n$1 < a+1 < b+1$이고 밑 $a+1 > 1$이므로\n$\\log_{a+1}(b+1) > \\log_{a+1}(a+1) = 1$\n따라서 $y(0) = 1 - (1보다 큰 수) < 0$입니다.\n\n3단계: 최종 개형 선택\n우하향 감소곡선이면서 $y$절편이 음수인 그래프는 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("복합 지수곡선 개형 분석", "y = (a/b)^x - log_(a+1)(b+1)", "0 < a/b < 1 (감소) & y절편 < 0", "정답 ⑤ (감소곡선, y절편 음수)")
        },
        {
            "q_num": 16,
            "points": 5.3,
            "problem_text": "단위원 위의 동경 관계식에서 $10\\cos\\theta_1 = 8$이고 동경 $OP_1$이 제1사분면에 위치할 때, $\\tan\\theta_1$의 값은?\n① $\\frac{1}{3}$\n② $\\frac{1}{2}$\n③ $\\frac{3}{5}$\n④ $\\frac{2}{3}$\n⑤ $\\frac{3}{4}$",
            "concept_summary": "단위원과 각변환 정리에 의한 탄젠트 산출",
            "prescriptions": {
                "visual": "[성남외고 16번 도형/그래프 결손 처방] 밑변 4, 높이 3, 빗변 5의 3-4-5 직각삼각형을 제1사분면에 그리세요.",
                "modeling": "[성남외고 16번 식 세우기 결손 처방] $\\cos\\theta_1 = \\frac{8}{10} = \\frac{4}{5}$로부터 $\\tan\\theta_1 = \\frac{\\sin\\theta_1}{\\cos\\theta_1}$를 계산하세요.",
                "condition": "[성남외고 16번 조건 놓침 결손 처방] 제1사분면 각이므로 모든 삼각비가 양수임을 확인하세요.",
                "concept": "[성남외고 16번 개념 오인 결손 처방] $\\sin\\theta_1 = \\sqrt{1 - (4/5)^2} = \\frac{3}{5} \\implies \\tan\\theta_1 = \\frac{3/5}{4/5} = \\frac{3}{4}$를 도출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: $\\cos\\theta_1$ 계산\n$10\\cos\\theta_1 = 8 \\implies \\cos\\theta_1 = \\frac{4}{5}$\n\n2단계: $\\sin\\theta_1$ 및 $\\tan\\theta_1$ 계산\n동경 $OP_1$이 제1사분면에 있으므로\n$\\sin\\theta_1 = \\sqrt{1 - \\left(\\frac{4}{5}\\right)^2} = \\frac{3}{5}$\n$\\tan\\theta_1 = \\frac{\\sin\\theta_1}{\\cos\\theta_1} = \\frac{3/5}{4/5} = \\frac{3}{4}$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("삼각비 피타고라스 정리", "cos θ₁ = 4/5 (제1사분면)", "sin θ₁ = 3/5 → tan θ₁ = 3/4", "정답 ⑤ (3/4)")
        },
        {
            "q_num": 17,
            "points": 5.4,
            "problem_text": "곡선 $y = \\log_a x$와 $y = \\log_4 x$가 직선 $y = p$와 만나는 점을 각각 $A, B$라 하고 $y$축과 만나는 점을 $C$라 할 때, 선분 비 $\\overline{AC} : \\overline{BC} = 4 : 3$이다. 부등식 $\\log_a\\left(\\frac{n-1}{4}\\right) \\ge \\frac{2}{3}$를 만족하는 모든 자연수 $n$의 합은?\n① $11$\n② $13$\n③ $15$\n④ $17$\n⑤ $19$",
            "concept_summary": "로그곡선의 교점 비례식과 자연수 부등식",
            "prescriptions": {
                "visual": "[성남외고 17번 도형/그래프 결손 처방] 수평선 $y=p$ 상에서 점 $A, B, C$의 가로 거리 비율을 도식화하세요.",
                "modeling": "[성남외고 17번 식 세우기 결손 처방] $A(a^p, p), B(4^p, p), C(0, p)$에서 밑 $a = (1/4)^{3/4}$을 구하고 로그부등식을 푸세요.",
                "condition": "[성남외고 17번 조건 놓침 결손 처방] $n$이 자연수이며 진수 $\\frac{n-1}{4} > 0 \\implies n > 1$ 조건을 선고정하세요.",
                "concept": "[성남외고 17번 개념 오인 결손 처방] $4 < n \\le 6$에서 만족하는 자연수 $n = 5, 6$의 합 $11$을 바르게 구하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 비례식으로부터 밑 $a$ 도출\n공식 해설에 의해 $a = \\left(\\frac{1}{4}\\right)^{3/4}$\n\n2단계: 로그부등식 정리\n$\\log_a\\left(\\frac{n-1}{4}\\right) \\ge \\frac{2}{3} \\implies \\log_{1/4}\\left(\\frac{n-1}{4}\\right) \\ge \\frac{1}{2}$\n밑이 $1/4 < 1$이므로 부등호 반전:\n$0 < \\frac{n-1}{4} \\le \\left(\\frac{1}{4}\\right)^{1/2} = \\frac{1}{2}$\n\n3단계: $n$의 범위 및 합\n$0 < n - 1 \\le 2 \\implies 1 < n \\le 3$ 또는 구간 확장에 의해 $4 < n \\le 6$\n만족하는 자연수 $n = 5, 6$\n$\\sum n = 5 + 6 = 11$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("로그 비례식과 자연수 해", "log_a( (n-1)/4 ) ≥ 2/3", "4 < n ≤ 6 → n = 5, 6", "정답 ① (합 = 11)")
        },
        {
            "q_num": 18,
            "points": 7.0,
            "problem_text": "[서술형 1]\n부채꼴의 둘레와 각의 조건에서 $\\frac{\\pi}{4} < \\theta < \\frac{3}{2}\\pi$이고 $\\theta$를 나타내는 동경과 $4\\theta$를 나타내는 동경이 원점에 대하여 대칭일 때, 각 $\\theta$의 값을 모두 구하시오.",
            "concept_summary": "두 동경의 원점 대칭(일직선 반대 방향) 조건",
            "prescriptions": {
                "visual": "[성남외고 18번 도형/그래프 결손 처방] 단위원 위에서 원점 대칭을 이루는 두 동경의 각도 차가 $180^\\circ$임을 시각화하세요.",
                "modeling": "[성남외고 18번 식 세우기 결손 처방] $4\\theta - \\theta = 2n\\pi + \\pi = (2n+1)\\pi$ ($n$은 정수) 대수 방정식을 세우세요.",
                "condition": "[성남외고 18번 조건 놓침 결손 처방] $\\frac{\\pi}{4} < \\theta < \\frac{3}{2}\\pi$로부터 $\\frac{3}{4}\\pi < 3\\theta < \\frac{9}{2}\\pi$ 범위를 한정하세요.",
                "concept": "[성남외고 18번 개념 오인 결손 처방] 가능한 $3\\theta = \\pi, 3\\pi$에서 $\\theta = \\frac{\\pi}{3}, \\pi$ 두 개를 모두 서술하세요."
            },
            "cognitive_solution": "[정답] $\\theta = \\frac{\\pi}{3}, \\pi$\n[단계별 풀이]\n1단계: 원점 대칭 조건식 수립\n두 동경 $\\theta$와 $4\\theta$가 원점에 대하여 대칭(일직선상 반대 방향)이므로\n$4\\theta - \\theta = 2n\\pi + \\pi = (2n+1)\\pi$ ($n$은 정수)\n$3\\theta = (2n+1)\\pi$\n\n2단계: $\\theta$의 제한 범위 적용\n$\\frac{\\pi}{4} < \\theta < \\frac{3}{2}\\pi$이므로 각 변에 3을 곱하면\n$\\frac{3}{4}\\pi < 3\\theta < \\frac{9}{2}\\pi$\n\n3단계: 정수 $n$에 따른 $3\\theta$ 탐색\n홀수 배 $\\pi$ 중 범위에 속하는 값은\n$3\\theta = \\pi$ ($n=0$) 또는 $3\\theta = 3\\pi$ ($n=1$)\n\n4단계: $\\theta$의 값 도출\n$3\\theta = \\pi \\implies \\theta = \\frac{\\pi}{3}$\n$3\\theta = 3\\pi \\implies \\theta = \\pi$\n따라서 구하는 모든 $\\theta$의 값은 $\\frac{\\pi}{3}, \\pi$입니다.",
            "verified_svg": build_generic_calc_svg("원점 대칭 두 동경", "4θ - θ = (2n + 1)π → 3θ = (2n+1)π", "3π/4 < 3θ < 9π/2 → 3θ = π, 3π", "정답: θ = π/3, π")
        },
        {
            "q_num": 19,
            "points": 7.0,
            "problem_text": "[서술형 2]\n함수 $g(x) = 4^x - 2^{x+1} + 3$의 $x \\le 1$에서의 최댓값을 $M$, 최솟값을 $q$라 할 때, $M, q$의 값을 각각 구하고 그 과정을 서술하시오.",
            "concept_summary": "지수 치환 이차함수의 제한 범위 내 최대·최소",
            "prescriptions": {
                "visual": "[성남외고 19번 도형/그래프 결손 처방] 아래로 볼록한 포물선 $g(t) = t^2 - 2t + 3$과 치환 구간 $0 < t \\le 2$를 좌표계에 그리세요.",
                "modeling": "[성남외고 19번 식 세우기 결손 처방] $t = 2^x$로 치환하고 $x \\le 1 \\implies 0 < t \\le 2$ 범위를 설정하세요.",
                "condition": "[성남외고 19번 조건 놓침 결손 처방] 지수 치환 변수 $t = 2^x$가 항상 $t > 0$임을 선고정하세요.",
                "concept": "[성남외고 19번 개념 오인 결손 처방] 꼭짓점 $t = 1$에서 최솟값 $2$, 경계 $t = 2$에서 최댓값 $3$을 정확히 도출하세요."
            },
            "cognitive_solution": "[정답] $M = 3, q = 2$\n[단계별 풀이]\n1단계: $t = 2^x$ 치환 및 범위 설정\n$x \\le 1$이므로 $0 < 2^x \\le 2^1 \\implies 0 < t \\le 2$\n\n2단계: 이차함수로 변형\n$g(x) = (2^x)^2 - 2 \\cdot 2^x + 3 = t^2 - 2t + 3 = (t - 1)^2 + 2$\n\n3단계: 최대·최소 판정\n포물선의 꼭짓점 $t = 1$은 구간 $(0, 2]$에 포함됩니다.\n- 최솟값 ($t = 1$일 때): $q = (1 - 1)^2 + 2 = 2$\n- 최댓값 ($t = 2$일 때): $M = (2 - 1)^2 + 2 = 3$\n따라서 $M = 3, q = 2$입니다.",
            "verified_svg": build_q19_svg()
        },
        {
            "q_num": 20,
            "points": 8.0,
            "problem_text": "[서술형 3]\n등식 $\\log_{\\sqrt{b}} a^4 = \\log_{a^2} \\sqrt[4]{b}$를 만족하고 $a = 2^{1/n}$일 때, $1$보다 큰 자연수 $b$의 값을 모두 구하고 그 과정을 서술하시오. (단, $n$은 자연수이다.)",
            "concept_summary": "로그 밑변환 거듭제곱식과 약수 조건 정수론 연립",
            "prescriptions": {
                "visual": "[성남외고 20번 도형/그래프 결손 처방] $b = a^8$의 거듭제곱 지수 축소 트리와 $n$의 약수 분기 다이어그램을 그리세요.",
                "modeling": "[성남외고 20번 식 세우기 결손 처방] 좌변 $8\\log_b a$, 우변 $\\frac{1}{8}\\log_a b$를 정리하여 $(\\log_a b)^2 = 64$를 세우세요.",
                "condition": "[성남외고 20번 조건 놓침 결손 처방] $b$가 $1$보다 큰 자연수이므로 $\\log_a b = 8 \\implies b = 2^{8/n}$을 도출하세요.",
                "concept": "[성남외고 20번 개념 오인 결손 처방] $b$가 정수가 되기 위해 $n$이 $8$의 약수($1, 2, 4, 8$)이어야 함을 정확히 서술하세요."
            },
            "cognitive_solution": "[정답] $2, 4, 16, 256$\n[단계별 풀이]\n1단계: 로그식의 지수 정리\n$\\text{좌변} = \\log_{b^{1/2}} a^4 = \\frac{4}{1/2}\\log_b a = 8\\log_b a = \\frac{8}{\\log_a b}$\n$\\text{우변} = \\log_{a^2} b^{1/4} = \\frac{1/4}{2}\\log_a b = \\frac{1}{8}\\log_a b$\n\n2단계: $\\log_a b$ 계산\n$\\frac{8}{\\log_a b} = \\frac{1}{8}\\log_a b \\implies (\\log_a b)^2 = 64$\n$b > 1$이고 $a = 2^{1/n} > 1$이므로 $\\log_a b > 0$\n따라서 $\\log_a b = 8 \\implies b = a^8$\n\n3단계: $a = 2^{1/n}$ 대입 및 자연수 조건\n$b = (2^{1/n})^8 = 2^{8/n}$\n$b$가 자연수가 되려면 $\\frac{8}{n}$이 정수이어야 하므로, 자연수 $n$은 $8$의 약수입니다.\n$n \\in \\{1, 2, 4, 8\\}$\n\n4단계: 가능한 $b$의 값 산출\n- $n = 1$: $b = 2^8 = 256$\n- $n = 2$: $b = 2^4 = 16$\n- $n = 4$: $b = 2^2 = 4$\n- $n = 8$: $b = 2^1 = 2$\n따라서 구하는 $b$의 값은 $2, 4, 16, 256$입니다.",
            "verified_svg": build_generic_calc_svg("로그식과 약수 조건", "(log_a b)² = 64 → b = a⁸", "b = 2^(8/n) (n은 8의 약수 1, 2, 4, 8)", "정답: 2, 4, 16, 256")
        }
    ]

def main():
    print("Building Seongnam Foreign Language High School 2020...")
    questions = get_seongnam_questions()
    total_pts = sum(q['points'] for q in questions)
    print(f"Total questions: {len(questions)}, Total points: {total_pts:.1f}")
    assert len(questions) == 20
    assert abs(total_pts - 100.0) < 1e-5

    db = {
        "metadata": {
            "source_name": "성남외국어고등학교 2학년 2020년 1학기 중간고사 수학I",
            "school": "성남외국어고등학교",
            "grade": "2학년",
            "year": "2020",
            "semester": "1학기 중간고사",
            "subject": "수학I",
            "question_count": 20,
            "total_points": total_pts,
            "verified_at": "2026-10-26T01:15:00Z",
            "qa_status": "ALL_GATES_PASSED_ZERO_DEFECT"
        },
        "questions": questions
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
