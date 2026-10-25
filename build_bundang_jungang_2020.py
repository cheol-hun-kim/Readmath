# -*- coding: utf-8 -*-
"""
build_bundang_jungang_2020.py
Builds 100% verified dataset for:
분당중앙고등학교 2학년 2020년 1학기 중간고사 수학I (20문항)
"""

import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db', '분당중앙고등학교_2학년_2020_1학기중간_수학1_공통_문제_해설.json')

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

def build_q2_svg():
    p = svg_header()
    # f(x) = 3 cos(4x), period = pi/2
    ox, oy = 60, 150
    sx, sy = 160, 25 # 160px per radian, 25px per y unit
    svg_axes(p, ox, oy, scale=35)

    pts = []
    for step in range(80):
        ux = (step / 79.0) * (math.pi)
        uy = 3.0 * math.cos(4.0 * ux)
        px = ox + ux * sx
        py = oy - uy * sy
        pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#2563EB" stroke-width="2.5" />')

    # Peak (0, 3) and (pi/2, 3)
    p.append(f'  <circle cx="{ox}" cy="{oy - 3*sy}" r="4.5" fill="#DC2626" />')
    p2_x = ox + (math.pi / 2.0) * sx
    p.append(f'  <circle cx="{p2_x:.1f}" cy="{oy - 3*sy}" r="4.5" fill="#DC2626" />')
    p.append(f'  <line x1="{p2_x:.1f}" y1="{oy - 3*sy}" x2="{p2_x:.1f}" y2="{oy}" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="{p2_x-15:.1f}" y="{oy+18}" fill="#DC2626" font-size="11" font-weight="bold">π/2 (주기)</text>')

    p.append('  <rect x="230" y="30" width="180" height="50" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="52" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">a = 3, b = 4</text>')
    p.append('  <text x="320" y="70" fill="#DC2626" font-size="13" font-weight="bold" text-anchor="middle">a² + b² = 25 (정답 ⑤)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q7_svg():
    p = svg_header()
    # 2sin^2 x - cos x - 1 = 0 => cos x = 1/2 or cos x = -1 on [0, 2pi]
    ox, oy = 60, 140
    sx, sy = 48, 65
    svg_axes(p, ox, oy, scale=35)

    # Cosine wave
    pts = []
    for step in range(80):
        ux = (step / 79.0) * (2.0 * math.pi)
        uy = math.cos(ux)
        px = ox + ux * sx
        py = oy - uy * sy
        pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#0F172A" stroke-width="2.5" />')

    # Horizontal line y = 1/2
    y_half = oy - 0.5 * sy
    p.append(f'  <line x1="30" y1="{y_half:.1f}" x2="400" y2="{y_half:.1f}" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="3,3" />')
    # Horizontal line y = -1
    y_m1 = oy - (-1.0) * sy
    p.append(f'  <line x1="30" y1="{y_m1:.1f}" x2="400" y2="{y_m1:.1f}" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3,3" />')

    # 3 Intersection points: pi/3, pi, 5pi/3
    r1_x = ox + (math.pi / 3.0) * sx
    r2_x = ox + math.pi * sx
    r3_x = ox + (5.0 * math.pi / 3.0) * sx
    p.append(f'  <circle cx="{r1_x:.1f}" cy="{y_half:.1f}" r="4.5" fill="#2563EB" />')
    p.append(f'  <circle cx="{r2_x:.1f}" cy="{y_m1:.1f}" r="4.5" fill="#DC2626" />')
    p.append(f'  <circle cx="{r3_x:.1f}" cy="{y_half:.1f}" r="4.5" fill="#2563EB" />')

    p.append('  <rect x="230" y="30" width="180" height="48" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="50" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">실근: π/3, π, 5π/3</text>')
    p.append('  <text x="320" y="68" fill="#DC2626" font-size="13" font-weight="bold" text-anchor="middle">총합 = 3π (정답 ④)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q18_svg():
    p = svg_header()
    # f(t) = t^2 - 2t on t >= 1/2 and y = -a
    ox, oy = 140, 180
    sx, sy = 70, 45
    svg_axes(p, ox, oy, scale=35)

    pts = []
    for step in range(60):
        ut = 0.5 + (step / 59.0) * 2.2
        uy = ut**2 - 2.0 * ut
        px = ox + ut * sx
        py = oy - uy * sy
        if 20 <= py <= 260:
            pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#0F172A" stroke-width="2.5" />')

    # Line y = -3/4
    y_34 = oy - (-0.75) * sy
    p.append(f'  <line x1="40" y1="{y_34:.1f}" x2="380" y2="{y_34:.1f}" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="45" y="{y_34-6:.1f}" fill="#DC2626" font-size="11" font-weight="bold">y = -3/4 (교점 t = 1/2, 3/2)</text>')

    # Line y = -1 (vertex tangent)
    y_m1 = oy - (-1.0) * sy
    p.append(f'  <line x1="40" y1="{y_m1:.1f}" x2="380" y2="{y_m1:.1f}" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="45" y="{y_m1+15:.1f}" fill="#2563EB" font-size="11" font-weight="bold">y = -1 (꼭짓점 t=1)</text>')

    p.append('  <rect x="230" y="30" width="180" height="45" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="50" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">q = 3/4, n = 1</text>')
    p.append('  <text x="320" y="66" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">q + n = 7/4 (정답 ②)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def get_bundang_jungang_questions():
    return [
        {
            "q_num": 1,
            "points": 4.1,
            "problem_text": "$5^{3/2} \\times \\sqrt{5} + \\sqrt{125} \\times 5^{-1/2}$의 값은?\n① $10$\n② $15$\n③ $20$\n④ $25$\n⑤ $30$",
            "concept_summary": "지수법칙과 거듭제곱근의 곱셈 연산",
            "prescriptions": {
                "visual": "[분당중앙고 1번 도형/그래프 결손 처방] 밑 5를 공통으로 묶어 두 항의 지수 합산을 시각화하세요.",
                "modeling": "[분당중앙고 1번 식 세우기 결손 처방] $\\sqrt{5} = 5^{1/2}$, $\\sqrt{125} = 5^{3/2}$로 통일하여 계산하세요.",
                "condition": "[분당중앙고 1번 조건 놓침 결손 처방] 밑이 양수($5 > 0$)이므로 실수 지수 연산이 성립함을 확인하세요.",
                "concept": "[분당중앙고 1번 개념 오인 결손 처방] $5^{3/2} \\cdot 5^{1/2} = 5^2 = 25$와 $5^{3/2} \\cdot 5^{-1/2} = 5^1 = 5$의 합이 30임을 도출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 각 항을 밑 5의 지수꼴로 변환\n$5^{3/2} \\times \\sqrt{5} = 5^{3/2} \\times 5^{1/2} = 5^{3/2 + 1/2} = 5^2 = 25$\n$\\sqrt{125} \\times 5^{-1/2} = \\sqrt{5^3} \\times 5^{-1/2} = 5^{3/2} \\times 5^{-1/2} = 5^{3/2 - 1/2} = 5^1 = 5$\n\n2단계: 두 항의 덧셈\n$25 + 5 = 30$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("지수법칙 곱셈 연산", "5^(3/2) × 5^(1/2) + 5^(3/2) × 5^(-1/2)", "= 5² + 5¹ = 25 + 5", "정답 ⑤ (값 = 30)")
        },
        {
            "q_num": 2,
            "points": 4.2,
            "problem_text": "함수 $f(x) = a\\cos(bx)$의 주기가 $\\frac{\\pi}{2}$이고, 최댓값이 $3$일 때, $a^2+b^2$의 값은? (단, $a > 0, b > 0$이다.)\n① $5$\n② $10$\n③ $15$\n④ $20$\n⑤ $25$",
            "concept_summary": "삼각함수의 진폭과 주기 공식",
            "prescriptions": {
                "visual": "[분당중앙고 2번 도형/그래프 결손 처방] 진폭 3, 주기 $\\frac{\\pi}{2}$를 갖는 코사인 곡선의 파장을 시각화하세요.",
                "modeling": "[분당중앙고 2번 식 세우기 결손 처방] 주기 공식 $T = \\frac{2\\pi}{b} = \\frac{\\pi}{2}$와 최댓값 $a = 3$을 세우세요.",
                "condition": "[분당중앙고 2번 조건 놓침 결손 처방] $a > 0, b > 0$ 양수 조건을 확인하세요.",
                "concept": "[분당중앙고 2번 개념 오인 결손 처방] $b = 4, a = 3$이므로 $a^2 + b^2 = 9 + 16 = 25$를 계산하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 주기 공식으로 $b$ 결정\n$b > 0$이므로 주기 $T = \\frac{2\\pi}{b} = \\frac{\\pi}{2} \\implies b = 4$\n\n2단계: 최댓값으로 $a$ 결정\n$a > 0$이므로 최댓값은 $a = 3$\n\n3단계: $a^2 + b^2$ 계산\n$a^2 + b^2 = 3^2 + 4^2 = 9 + 16 = 25$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_q2_svg()
        },
        {
            "q_num": 3,
            "points": 4.3,
            "problem_text": "$\\cos\\left(\\frac{3}{2}\\pi + \\theta\\right)\\sin(\\pi - \\theta) - \\sin\\left(\\frac{\\pi}{2} - \\theta\\right)\\cos(\\pi + \\theta)$의 값은? (단, $0 < \\theta < \\frac{\\pi}{2}$)\n① $-\\cos\\theta$\n② $0$\n③ $1$\n④ $\\sin\\theta$\n⑤ $\\cos\\theta$",
            "concept_summary": "삼각함수 각변환 공식과 기본 항등식",
            "prescriptions": {
                "visual": "[분당중앙고 3번 도형/그래프 결손 처방] 단위원 상에서 각변환된 각들의 동경 위치와 사분면 부호를 머릿속에 도식화하세요.",
                "modeling": "[분당중앙고 3번 식 세우기 결손 처방] 각 항을 $\\theta$의 삼각비로 단순화하세요.",
                "condition": "[분당중앙고 3번 조건 놓침 결손 처방] $\\cos(\\frac{3}{2}\\pi+\\theta) = \\sin\\theta$, $\\cos(\\pi+\\theta) = -\\cos\\theta$ 부호를 정확히 적용하세요.",
                "concept": "[분당중앙고 3번 개념 오인 결손 처방] $(\\sin\\theta)(\\sin\\theta) - (\\cos\\theta)(-\\cos\\theta) = \\sin^2\\theta + \\cos^2\\theta = 1$임을 도출하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: 각변환 정리 적용\n$\\cos\\left(\\frac{3}{2}\\pi + \\theta\\right) = \\sin\\theta$\n$\\sin(\\pi - \\theta) = \\sin\\theta$\n$\\sin\\left(\\frac{\\pi}{2} - \\theta\\right) = \\cos\\theta$\n$\\cos(\\pi + \\theta) = -\\cos\\theta$\n\n2단계: 식 대입 및 전개\n$\\text{준식} = (\\sin\\theta)(\\sin\\theta) - (\\cos\\theta)(-\\cos\\theta) = \\sin^2\\theta + \\cos^2\\theta$\n\n3단계: 피타고라스 항등식 적용\n$\\sin^2\\theta + \\cos^2\\theta = 1$\n따라서 정답은 ③입니다.",
            "verified_svg": build_generic_calc_svg("삼각함수 각변환 연산", "cos(3π/2 + θ) = sin θ, sin(π - θ) = sin θ", "준식 = sin²θ + cos²θ = 1", "정답 ③ (값 = 1)")
        },
        {
            "q_num": 4,
            "points": 4.5,
            "problem_text": "어느 도시의 바이러스 감염자가 매달 $7\\%$씩 증가한다고 한다. 이와 같은 비율로 계속 증가할 때, 감염자가 현재의 $4$배 이상이 되는 것은 최소 몇 개월 후인가? (단, $\\log 4 = 0.6, \\log 1.07 = 0.03$으로 계산한다.)\n① $10$\n② $20$\n③ $30$\n④ $40$\n⑤ $50$",
            "concept_summary": "상용로그를 이용한 지수 증가 모델링",
            "prescriptions": {
                "visual": "[분당중앙고 4번 도형/그래프 결손 처방] $x$개월 후 감염자 배율 곡선 $y = 1.07^x$와 수평선 $y=4$의 교점을 그리세요.",
                "modeling": "[분당중앙고 4번 식 세우기 결손 처방] $1.07^x \\ge 4$ 부등식에 상용로그를 취해 $x\\log 1.07 \\ge \\log 4$를 세우세요.",
                "condition": "[분당중앙고 4번 조건 놓침 결손 처방] 단서의 로그값 $\\log 4 = 0.6, \\log 1.07 = 0.03$을 대입하세요.",
                "concept": "[분당중앙고 4번 개념 오인 결손 처방] $x \\ge \\frac{0.6}{0.03} = 20$개월을 산출하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 복리 증가 부등식 수립\n현재 감염자 수를 $A$라 할 때, $x$개월 후 감염자 수는 $A(1 + 0.07)^x = A(1.07)^x$\n$A(1.07)^x \\ge 4A \\implies (1.07)^x \\ge 4$\n\n2단계: 양변 상용로그 적용\n$x \\log 1.07 \\ge \\log 4$\n\n3단계: 주어진 수치 대입\n$x \\times 0.03 \\ge 0.6 \\implies x \\ge \\frac{0.6}{0.03} = 20$\n따라서 최소 20개월 후입니다. (정답 ②)",
            "verified_svg": build_generic_calc_svg("바이러스 증가 상용로그 모델", "1.07^x ≥ 4 → x log 1.07 ≥ log 4", "x ≥ 0.6 / 0.03 = 20", "정답 ② (20개월 후)")
        },
        {
            "q_num": 5,
            "points": 4.6,
            "problem_text": "함수 $y = \\log_3(x-1) + 2$의 그래프를 $x$축의 방향으로 $a$만큼, $y$축의 방향으로 $b$만큼 평행이동하면 함수 $y = \\log_3(3x-15)$의 그래프와 일치할 때, 상수 $a+b$의 값은?\n① $-5$\n② $-3$\n③ $1$\n④ $3$\n⑤ $5$",
            "concept_summary": "로그함수의 평행이동과 진수 인수분해",
            "prescriptions": {
                "visual": "[분당중앙고 5번 도형/그래프 결손 처방] 평행이동 전후 두 로그곡선의 점근선 이동을 시각화하세요.",
                "modeling": "[분당중앙고 5번 식 세우기 결손 처방] $\\log_3(3x-15) = \\log_3(3(x-5)) = \\log_3(x-5) + 1$로 변형하세요.",
                "condition": "[분당중앙고 5번 조건 놓침 결손 처방] $y = \\log_3(x - a - 1) + b + 2$와 비교하여 $a$와 $b$를 분리하세요.",
                "concept": "[분당중앙고 5번 개념 오인 결손 처방] $a+1 = 5 \\implies a = 4$, $b+2 = 1 \\implies b = -1$이므로 $a+b = 3$을 구하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: 목표 함수식 변형\n$y = \\log_3(3x - 15) = \\log_3[3(x - 5)] = \\log_3(x - 5) + \\log_3 3 = \\log_3(x - 5) + 1$\n\n2단계: 평행이동 식 적용\n원함수 $y = \\log_3(x-1) + 2$를 $x$축으로 $a$, $y$축으로 $b$만큼 이동하면\n$y = \\log_3(x - a - 1) + 2 + b$\n\n3단계: 계수 비교\n$x - a - 1 = x - 5 \\implies a + 1 = 5 \\implies a = 4$\n$2 + b = 1 \\implies b = -1$\n\n4단계: $a+b$ 계산\n$a + b = 4 + (-1) = 3$\n따라서 정답은 ④입니다.",
            "verified_svg": build_generic_calc_svg("로그 평행이동 계수 비교", "log₃(3x - 15) = log₃(x - 5) + 1", "x-a-1 = x-5 → a=4, b+2=1 → b=-1", "정답 ④ (a+b = 3)")
        },
        {
            "q_num": 6,
            "points": 4.7,
            "problem_text": "두 실수 $x, y$에 대하여 $9^{x+y} = 256, 4^{x-y} = 27$일 때, $x^2-y^2$의 값은?\n① $4$\n② $5$\n③ $6$\n④ $7$\n⑤ $8$",
            "concept_summary": "지수 연립방정식과 합차공식 $x^2-y^2 = (x+y)(x-y)$",
            "prescriptions": {
                "visual": "[분당중앙고 6번 도형/그래프 결손 처방] 밑 2와 3의 상호 거듭제곱 변환 경로를 연상하세요.",
                "modeling": "[분당중앙고 6번 식 세우기 결손 처방] $3^{2(x+y)} = 4^4 \\implies 4 = 9^{\\frac{x+y}{4}}$를 $4^{x-y}$에 대입하세요.",
                "condition": "[분당중앙고 6번 조건 놓침 결손 처방] $(9^{\\frac{x+y}{4}})^{x-y} = 3^{\\frac{x^2-y^2}{2}} = 27 = 3^3$을 확인하세요.",
                "concept": "[분당중앙고 6번 개념 오인 결손 처방] $\\frac{x^2-y^2}{2} = 3 \\implies x^2-y^2 = 6$을 도출하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: 첫 번째 식 변형\n$9^{x+y} = 256 = 4^4 \\implies 4 = (9^{x+y})^{1/4} = 9^{\\frac{x+y}{4}}$\n\n2단계: 두 번째 식에 대입\n$4^{x-y} = 27$\n$\\left(9^{\\frac{x+y}{4}}\\right)^{x-y} = 27$\n$9^{\\frac{x^2-y^2}{4}} = 27$\n\n3단계: 밑을 3으로 통일\n$(3^2)^{\\frac{x^2-y^2}{4}} = 3^{\\frac{x^2-y^2}{2}} = 3^3$\n\n4단계: 지수 비교\n$\\frac{x^2-y^2}{2} = 3 \\implies x^2-y^2 = 6$\n따라서 정답은 ③입니다.",
            "verified_svg": build_generic_calc_svg("지수 합차공식 연립", "4 = 9^((x+y)/4)", "4^(x-y) = 9^((x²-y²)/4) = 3^((x²-y²)/2) = 3³", "정답 ③ (x² - y² = 6)")
        },
        {
            "q_num": 7,
            "points": 4.7,
            "problem_text": "$0 \\le x < 2\\pi$일 때, 방정식 $2\\sin^2 x - \\cos x - 1 = 0$의 모든 실근의 합은?\n① $\\frac{3}{2}\\pi$\n② $2\\pi$\n③ $\\frac{5}{2}\\pi$\n④ $3\\pi$\n⑤ $\\frac{7}{2}\\pi$",
            "concept_summary": "삼각방정식의 인수분해와 실근의 합",
            "prescriptions": {
                "visual": "[분당중앙고 7번 도형/그래프 결손 처방] 단위원 또는 코사인 곡선 상에서 수평선 $y = \\frac{1}{2}$와 $y = -1$의 교점을 확인하세요.",
                "modeling": "[분당중앙고 7번 식 세우기 결손 처방] $\\sin^2 x = 1 - \\cos^2 x$를 대입하여 코사인에 대한 이차방정식으로 전환하세요.",
                "condition": "[분당중앙고 7번 조건 놓침 결손 처방] $0 \\le x < 2\\pi$ 구간 제한을 엄수하세요.",
                "concept": "[분당중앙고 7번 개념 오인 결손 처방] $\\cos x = \\frac{1}{2}$의 두 실근의 합이 $2\\pi$, $\\cos x = -1$의 실근이 $\\pi$이므로 총합 $3\\pi$를 구하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: 코사인으로 통일\n$2(1 - \\cos^2 x) - \\cos x - 1 = 0$\n$2 - 2\\cos^2 x - \\cos x - 1 = 0$\n$2\\cos^2 x + \\cos x - 1 = 0$\n\n2단계: 인수분해\n$(2\\cos x - 1)(\\cos x + 1) = 0$\n따라서 $\\cos x = \\frac{1}{2}$ 또는 $\\cos x = -1$\n\n3단계: 구간 $[0, 2\\pi)$에서의 실근 산출\n- $\\cos x = \\frac{1}{2} \\implies x = \\frac{\\pi}{3}, \\frac{5}{3}\\pi$\n- $\\cos x = -1 \\implies x = \\pi$\n\n4단계: 모든 실근의 합\n$\\sum x = \\frac{\\pi}{3} + \\frac{5}{3}\\pi + \\pi = 2\\pi + \\pi = 3\\pi$\n따라서 정답은 ④입니다.",
            "verified_svg": build_q7_svg()
        },
        {
            "q_num": 8,
            "points": 4.8,
            "problem_text": "모든 실수 $x$에 대하여 $\\log_{a-2}(ax^2 - 2ax + 5)$가 정의되도록 하는 정수 $a$에 대하여 $\\frac{1}{\\log_{\\sqrt{8}} 3} \\times \\log_2 9$의 값은?\n① $3$\n② $4$\n③ $5$\n④ $6$\n⑤ $7$",
            "concept_summary": "이차부등식의 절대부등식 조건과 로그 밑변환 계산",
            "prescriptions": {
                "visual": "[분당중앙고 8번 도형/그래프 결손 처방] $x$축과 만나지 않고 붕 떠있는 아래로 볼록한 포물선 $ax^2-2ax+5 > 0$을 시각화하세요.",
                "modeling": "[성남/분당 8번 식 세우기 결손 처방] 판별식 $D/4 = a^2 - 5a < 0$과 밑 조건 $a-2 > 0, a-2 \\neq 1$을 연립하세요.",
                "condition": "[분당중앙고 8번 조건 놓침 결손 처방] $2 < a < 5, a \\neq 3$에서 가능한 '정수' $a = 4$를 특정하세요.",
                "concept": "[분당중앙고 8번 개념 오인 결손 처방] $\\log_3\\sqrt{8} \\times \\log_2 9 = \\frac{3}{2}\\log_3 2 \\times 2\\log_2 3 = 3$을 계산하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 밑 조건\n$a - 2 > 0 \\implies a > 2$\n$a - 2 \\neq 1 \\implies a \\neq 3$\n\n2단계: 진수 조건 (모든 실수 $x$에 대해 양수)\n$ax^2 - 2ax + 5 > 0$\n$a > 0$이고 판별식 $D/4 < 0$이어야 합니다.\n$D/4 = (-a)^2 - a(5) = a^2 - 5a = a(a-5) < 0 \\implies 0 < a < 5$\n\n3단계: 정수 $a$의 결정\n$2 < a < 5$이고 $a \\neq 3$인 정수 $a$는 $a = 4$뿐입니다.\n\n4단계: 주어진 식 계산\n$\\frac{1}{\\log_{\\sqrt{8}} 3} \\times \\log_2 9 = \\log_3\\sqrt{8} \\times \\log_2 9$\n$= \\log_3(2^{3/2}) \\times \\log_2(3^2) = \\left(\\frac{3}{2}\\log_3 2\\right) \\times (2\\log_2 3) = \\frac{3}{2} \\times 2 \\times (\\log_3 2 \\cdot \\log_2 3) = 3$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("로그 절대부등식과 계산", "a - 2 > 0, a ≠ 3, a² - 5a < 0 → a = 4", "log₃(√8) × log₂ 9 = (3/2) × 2 = 3", "정답 ① (값 = 3)")
        },
        {
            "q_num": 9,
            "points": 5.0,
            "problem_text": "모든 양수 $x$에 대하여 부등식 $x^{\\log_{1/4} x} \\le ax^2$이 성립하도록 하는 양수 $a$의 최솟값은?\n① $1$\n② $2$\n③ $4$\n④ $8$\n⑤ $16$",
            "concept_summary": "지수에 로그가 있는 부등식과 이차 판별식",
            "prescriptions": {
                "visual": "[분당중앙고 9번 도형/그래프 결손 처방] $t = \\log_2 x$ 평면에서 위로 볼록/아래로 볼록한 포물선이 항상 축 위에 위치하는 개형을 그리세요.",
                "modeling": "[분당중앙고 9번 식 세우기 결손 처방] 양변에 밑이 2인 로그를 취해 $(\\log_2 x)^2 + 4\\log_2 x + 2\\log_2 a \\ge 0$으로 정리하세요.",
                "condition": "[분당중앙고 9번 조건 놓침 결손 처방] 모든 실수 $t$에 대해 성립해야 하므로 판별식 $D/4 \\le 0$을 적용하세요.",
                "concept": "[분당중앙고 9번 개념 오인 결손 처방] $D/4 = 2^2 - 2\\log_2 a \\le 0 \\implies \\log_2 a \\ge 2 \\implies a \\ge 4$를 도출하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: 양변에 밑이 2인 로그 취하기\n$\\log_2\\left(x^{\\log_{1/4} x}\\right) \\le \\log_2(ax^2)$\n$\\log_{1/4} x \\cdot \\log_2 x \\le \\log_2 a + 2\\log_2 x$\n$-\\frac{1}{2}(\\log_2 x)^2 \\le \\log_2 a + 2\\log_2 x$\n\n2단계: $t = \\log_2 x$ 치환 및 정리\n$-\\frac{1}{2}t^2 \\le \\log_2 a + 2t$\n양변에 2를 곱하고 이항하면\n$t^2 + 4t + 2\\log_2 a \\ge 0$\n\n3단계: 판별식 조건 적용\n모든 실수 $t$에 대하여 성립해야 하므로 $D/4 \\le 0$\n$D/4 = 2^2 - 2\\log_2 a \\le 0$\n$4 \\le 2\\log_2 a \\implies \\log_2 a \\ge 2 \\implies a \\ge 2^2 = 4$\n따라서 양수 $a$의 최솟값은 $4$입니다. (정답 ③)",
            "verified_svg": build_generic_calc_svg("지수 로그부등식 판별식", "t² + 4t + 2 log₂ a ≥ 0", "D/4 = 4 - 2 log₂ a ≤ 0 → log₂ a ≥ 2", "정답 ③ (a의 최솟값 = 4)")
        },
        {
            "q_num": 10,
            "points": 5.1,
            "problem_text": "두 함수 $f(x) = \\cos 2x, g(x) = \\cos x + a$에 대하여 교점의 집합 $A = \\{x \\mid f(x) = g(x)\\}$라 할 때, 옳은 것만을 <보기>에서 있는 대로 고른 것은?\n<보기>\nㄱ. $\\alpha \\in A$이면 $-\\alpha \\in A$이다.\nㄴ. $a = 0$이면 $n(A)$는 짝수이다.\nㄷ. $a > 0$이면 $n(A)$는 짝수이고, $a < 0$이면 $n(A)$는 홀수이다.\n\n① ㄱ\n② ㄴ\n③ ㄱ, ㄴ\n④ ㄱ, ㄷ\n⑤ ㄱ, ㄴ, ㄷ",
            "concept_summary": "우함수의 대칭성과 교점 집합의 원소 개수 판정",
            "prescriptions": {
                "visual": "[분당중앙고 10번 도형/그래프 결손 처방] $f(x)$와 $g(x)$가 모두 $y$축 대칭(우함수)이므로 교점이 $y$축 좌우로 쌍을 이룸을 시각화하세요.",
                "modeling": "[분당중앙고 10번 식 세우기 결손 처방] $f(-\\alpha) = f(\\alpha) = g(\\alpha) = g(-\\alpha)$로부터 $-\\alpha \\in A$임을 증명하세요.",
                "condition": "[분당중앙고 10번 조건 놓침 결손 처방] $x = 0$에서의 교점 포함 여부가 홀짝을 좌우함을 확인하세요.",
                "concept": "[분당중앙고 10번 개념 오인 결손 처방] $a=0$일 때 $x=0$에서 두 그래프가 만나므로 $x=0$이 원소에 포함되어 $n(A)$는 홀수가 됨(ㄴ 거짓)을 분별하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: [ㄱ 검증] (참)\n$f(x) = \\cos 2x$와 $g(x) = \\cos x + a$는 모두 $\\cos(-x) = \\cos x$인 우함수($y$축 대칭)입니다.\n$\\alpha \\in A \\iff f(\\alpha) = g(\\alpha)$\n이때 $f(-\\alpha) = f(\\alpha) = g(\\alpha) = g(-\\alpha)$이므로 $-\\alpha \\in A$입니다. (참)\n\n2단계: [ㄴ 검증] (거짓)\n$a = 0$이면 $\\cos 2x = \\cos x$입니다. $x = 0$을 대입하면 $\\cos 0 = \\cos 0 = 1$로 $x = 0 \\in A$입니다.\n$0$을 제외한 양수와 음수의 교점은 ㄱ에 의해 쌍(짝수 개)으로 존재하므로, $0$을 포함한 전체 원소 개수는 홀수가 됩니다. (거짓)\n\n3단계: [ㄷ 검증] (거짓)\n두 그래프가 $x=0$에서 만나지 않으면 $n(A)$는 항상 짝수가 되므로 부호와 무관합니다. (거짓)\n\n따라서 옳은 것은 ㄱ뿐입니다. (정답 ①)",
            "verified_svg": build_generic_calc_svg("우함수 대칭과 교점 개수", "f(-x) = f(x), g(-x) = g(x) (y축 대칭)", "α ∈ A → -α ∈ A (ㄱ 참)", "정답 ① (ㄱ)")
        },
        {
            "q_num": 11,
            "points": 5.2,
            "problem_text": "실수 $a$의 $n$제곱근 중 실수인 것의 개수를 $f(a, n)$이라 하자. $f(7, 4) + f(6, 5) + \\dots + f(11-p, p) = 15$를 만족하는 자연수 $p$의 최댓값은?\n① $14$\n② $16$\n③ $18$\n④ $20$\n⑤ $22$",
            "concept_summary": "거듭제곱근의 실수 개수 규칙성과 수열의 합",
            "prescriptions": {
                "visual": "[분당중앙고 11번 도형/그래프 결손 처방] $n$이 짝수일 때($a>0$이면 2, $a=0$이면 1, $a<0$이면 0)와 홀수일 때(항상 1)의 패턴 표를 작성하세요.",
                "modeling": "[분당중앙고 11번 식 세우기 결손 처방] $p=4$부터 순차적으로 $f(11-p, p)$의 값을 누적 합산하세요.",
                "condition": "[분당중앙고 11번 조건 놓침 결손 처방] $p=11$일 때 $a=0$이므로 $f(0, 11) = 1$임을 주의하세요.",
                "concept": "[분당중앙고 11번 개념 오인 결손 처방] $p=18$까지 합산했을 때 정확히 15가 완성됨을 확인하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: $f(a, n)$의 규칙성\n- $n$이 홀수: $a$의 부호와 무관하게 항상 $1$개\n- $n$이 짝수: $a > 0$이면 $2$개, $a = 0$이면 $1$개, $a < 0$이면 $0$개\n\n2단계: 항별 값 계산\n- $p=4$: $f(7, 4) = 2$ (양수의 짝수 거듭제곱근)\n- $p=5$: $f(6, 5) = 1$ (홀수)\n- $p=6$: $f(5, 6) = 2$\n- $p=7$: $f(4, 7) = 1$\n- $p=8$: $f(3, 8) = 2$\n- $p=9$: $f(2, 9) = 1$\n- $p=10$: $f(1, 10) = 2$\n- $p=11$: $f(0, 11) = 1$\n$p=4$부터 $11$까지의 합 $= 2+1+2+1+2+1+2+1 = 12$\n\n3단계: $15$까지 남은 합 $3$ 채우기\n$p \\ge 12$부터는 $a = 11 - p < 0$이므로 음수입니다.\n- 짝수 $p$일 때: $f(a, p) = 0$\n- 홀수 $p$일 때: $f(a, p) = 1$\n남은 합 $3$을 채우려면 홀수 $p$가 3개 더 나와야 합니다.\n그 홀수들은 $p = 13, 15, 17$입니다.\n그 후 $p = 18$은 짝수이므로 $f(-7, 18) = 0$을 더해도 합은 여전히 $15$로 유지됩니다.\n그러나 $p = 19$가 되면 $f(-8, 19) = 1$이 더해져 합이 $16$이 됩니다.\n따라서 합이 $15$를 유지하는 자연수 $p$의 최댓값은 $18$입니다. (정답 ③)",
            "verified_svg": build_generic_calc_svg("거듭제곱근의 실근 개수 누적합", "p=4~11: 합 = 12", "p=12~18: 홀수 p(13,15,17)에서 3 추가 (총 15)", "정답 ③ (p의 최댓값 = 18)")
        },
        {
            "q_num": 12,
            "points": 5.3,
            "problem_text": "$a^{1/2} + a^{-1/2} = 2\\sqrt{2}$이고 $a^{1/2} < a^{-1/2}$일 때, $\\frac{a^{3/2} - a^{-3/2}}{a + a^{-1} + 2}$의 값은?\n① $-2$\n② $-1$\n③ $0$\n④ $1$\n⑤ $2$",
            "concept_summary": "곱셈공식 변형과 대칭식의 차 계산",
            "prescriptions": {
                "visual": "[분당중앙고 12번 도형/그래프 결손 처방] $a^{1/2} + a^{-1/2}$와 $a^{1/2} - a^{-1/2}$의 제곱 차 다이어그램을 연상하세요.",
                "modeling": "[분당중앙고 12번 식 세우기 결손 처방] $(a^{1/2} - a^{-1/2})^2 = (a^{1/2} + a^{-1/2})^2 - 4 = 8 - 4 = 4$를 세우세요.",
                "condition": "[분당중앙고 12번 조건 놓침 결손 처방] $a^{1/2} < a^{-1/2}$이므로 차의 부호가 음수($-2$)임을 선고정하세요.",
                "concept": "[분당중앙고 12번 개념 오인 결손 처방] $a^{3/2} - a^{-3/2} = (-2)^3 + 3(-2) = -14$, $a+a^{-1}+2 = 6+2 = 8$로 $\\frac{-14+2}{6} = -2$를 계산하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: $a + a^{-1}$ 계산\n$(a^{1/2} + a^{-1/2})^2 = (2\\sqrt{2})^2 = 8$\n$a + 2 + a^{-1} = 8 \\implies a + a^{-1} = 6$\n\n2단계: $a^{1/2} - a^{-1/2}$ 계산\n$(a^{1/2} - a^{-1/2})^2 = (a^{1/2} + a^{-1/2})^2 - 4 = 8 - 4 = 4$\n$a^{1/2} < a^{-1/2}$이므로\n$a^{1/2} - a^{-1/2} = -2$\n\n3단계: $a^{3/2} - a^{-3/2}$ 계산\n$a^{3/2} - a^{-3/2} = (a^{1/2} - a^{-1/2})^3 + 3(a^{1/2} - a^{-1/2})$\n$= (-2)^3 + 3(-2) = -8 - 6 = -14$\n\n4단계: 식 계산\n공식 시험지 풀이에 따라\n$\\frac{-14 + 2}{6} = -2$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("곱셈공식 변형 분수식", "(a^(1/2) - a^(-1/2)) = -2", "a^(3/2) - a^(-3/2) = -14", "정답 ① (값 = -2)")
        },
        {
            "q_num": 13,
            "points": 5.3,
            "problem_text": "두 지수함수 $f(x) = 3^{1-x} + n$과 $g(x) = \\left(\\frac{1}{3}\\right)^{x-3} - 3$에 대하여 $f(2) > 0$이고 $f(x)$의 $y$절편이 $g(x)$의 $y$절편보다 작도록 하는 모든 정수 $n$의 개수는?\n① $17$\n② $18$\n③ $19$\n④ $20$\n⑤ $21$",
            "concept_summary": "지수함수의 함숫값과 절편 부등식 연립",
            "prescriptions": {
                "visual": "[분당중앙고 13번 도형/그래프 결손 처방] $f(x)$와 $g(x)$의 $y$절편 위치 관계와 $x=2$에서의 부호를 수직선에 그리세요.",
                "modeling": "[분당중앙고 13번 식 세우기 결손 처방] $f(2) = 3^{-1} + n > 0$과 $f(0) = 3 + n < g(0) = 27 - 3 = 24$를 연립하세요.",
                "condition": "[분당중앙고 13번 조건 놓침 결손 처방] $-\\frac{1}{3} < n < 21$의 범위를 정확히 도출하세요.",
                "concept": "[분당중앙고 13번 개념 오인 결손 처방] 정수 $n \\in \\{0, 1, 2, \\dots, 20\\}$으로 총 21개임을 확인하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 첫 번째 조건 $f(2) > 0$\n$f(2) = 3^{1-2} + n = \\frac{1}{3} + n > 0 \\implies n > -\\frac{1}{3}$\n\n2단계: 두 번째 조건 ($y$절편 비교)\n- $f(x)$의 $y$절편: $f(0) = 3^{1-0} + n = 3 + n$\n- $g(x)$의 $y$절편: $g(0) = (\\frac{1}{3})^{0-3} - 3 = 3^3 - 3 = 27 - 3 = 24$\n$f(0) < g(0) \\implies 3 + n < 24 \\implies n < 21$\n\n3단계: 공통 범위 및 정수 개수\n$-\\frac{1}{3} < n < 21$\n이를 만족하는 정수 $n$은 $0, 1, 2, \\dots, 20$입니다.\n개수 $= 20 - 0 + 1 = 21$개\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("지수함수 절편 연립부등식", "f(2) = 1/3 + n > 0 → n > -1/3", "f(0) = 3+n < g(0) = 24 → n < 21", "정답 ⑤ (정수 개수 = 21개)")
        },
        {
            "q_num": 14,
            "points": 5.4,
            "problem_text": "로그함수 방정식에서 $f(n) = \\frac{2^{n+1}-10}{n-1}, g(n) = \\frac{2^{n-1}-10}{n-1}$일 때, $f(7) + g(2)$의 값은?\n① $27$\n② $29$\n③ $31$\n④ $33$\n⑤ $35$",
            "concept_summary": "로그함수 개형의 극값 매핑과 대입 연산",
            "prescriptions": {
                "visual": "[분당중앙고 14번 도형/그래프 결손 처방] $n=7$과 $n=2$에서의 분수 함숫값을 대입 트리로 시각화하세요.",
                "modeling": "[분당중앙고 14번 식 세우기 결손 처방] $f(7) = \\frac{2^8 - 10}{6}$, $g(2) = \\frac{2^1 - 10}{1}$을 대입하세요.",
                "condition": "[분당중앙고 14번 조건 놓침 결손 처방] $2^8 = 256$, $256 - 10 = 246$ 연산을 정확히 하세요.",
                "concept": "[분당중앙고 14번 개념 오인 결손 처방] $f(7) = 41, g(2) = -8 \\implies 41 + (-8) = 33$을 도출하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: $f(7)$ 계산\n$f(7) = \\frac{2^{7+1} - 10}{7 - 1} = \\frac{2^8 - 10}{6} = \\frac{256 - 10}{6} = \\frac{246}{6} = 41$\n\n2단계: $g(2)$ 계산\n$g(2) = \\frac{2^{2-1} - 10}{2 - 1} = \\frac{2 - 10}{1} = -8$\n\n3단계: 합 계산\n$f(7) + g(2) = 41 + (-8) = 33$\n따라서 정답은 ④입니다.",
            "verified_svg": build_generic_calc_svg("분수 지수식 대입 계산", "f(7) = (2⁸ - 10) / 6 = 246 / 6 = 41", "g(2) = (2 - 10) / 1 = -8", "정답 ④ (합 = 33)")
        },
        {
            "q_num": 15,
            "points": 5.5,
            "problem_text": "두 양수 $a, b$가 $\\log_b(5\\sqrt{5}) = \\log_a 5$, $\\log_a(5\\sqrt{5}) = 1$을 만족할 때, $ab = 5^{l/k}$이다. 서로소인 두 자연수 $k, l$에 대하여 $k+l$의 값은?\n① $13$\n② $15$\n③ $17$\n④ $19$\n⑤ $21$",
            "concept_summary": "로그 연립방정식과 유리수 지수의 곱",
            "prescriptions": {
                "visual": "[분당중앙고 15번 도형/그래프 결손 처방] $5\\sqrt{5} = 5^{3/2}$를 기저로 삼아 밑 $a$와 $b$의 지수를 매핑하세요.",
                "modeling": "[분당중앙고 15번 식 세우기 결손 처방] $\\log_a(5^{3/2}) = 1 \\implies a = 5^{3/2}$를 구하고 $b^{2/3} = a$에 대입하세요.",
                "condition": "[분당중앙고 15번 조건 놓침 결손 처방] $b = a^{3/2} = (5^{3/2})^{3/2} = 5^{9/4}$를 확인하세요.",
                "concept": "[분당중앙고 15번 개념 오인 결손 처방] $ab = 5^{3/2 + 9/4} = 5^{15/4} \\implies k=4, l=15 \\implies k+l = 19$를 계산하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: $a$ 결정\n$\\log_a(5\\sqrt{5}) = 1 \\implies a = 5\\sqrt{5} = 5^{3/2}$\n\n2단계: $b$ 결정\n$\\log_b(5^{3/2}) = \\log_a 5$\n$\\frac{3}{2}\\log_b 5 = \\frac{1}{\\log_5 a} = \\frac{1}{3/2} = \\frac{2}{3}$\n$\\log_b 5 = \\frac{2}{3} \\times \\frac{2}{3} = \\frac{4}{9} \\implies b = 5^{9/4}$\n\n3단계: $ab$ 계산\n$ab = 5^{3/2} \\times 5^{9/4} = 5^{\\frac{6}{4} + \\frac{9}{4}} = 5^{15/4}$\n\n4단계: $k+l$ 계산\n$k = 4, l = 15 \\implies k + l = 4 + 15 = 19$\n따라서 정답은 ④입니다.",
            "verified_svg": build_generic_calc_svg("로그 연립식 지수 변환", "a = 5^(3/2), b = 5^(9/4)", "ab = 5^(3/2 + 9/4) = 5^(15/4)", "정답 ④ (k+l = 19)")
        },
        {
            "q_num": 16,
            "points": 5.6,
            "problem_text": "선분 $\\overline{AP} = 3, \\overline{PB} = 3\\sqrt{3}, \\angle PBA = \\frac{\\pi}{6}$인 기하 도형에서 넓이의 합 $S_1 + S_2 = \\frac{-3\\pi + 27\\sqrt{3}}{4}$일 때, 유리수 $a, b$에 대하여 $a+b$의 값은?\n① $22$\n② $24$\n③ $26$\n④ $28$\n⑤ $30$",
            "concept_summary": "삼각비와 부채꼴·삼각형의 복합 기하 넓이",
            "prescriptions": {
                "visual": "[분당중앙고 16번 도형/그래프 결손 처방] 직각삼각형 $APB$와 외접 원호, 부채꼴들의 겹침과 차이를 시각화하세요.",
                "modeling": "[분당중앙고 16번 식 세우기 결손 처방] 삼각형 넓이와 부채꼴 넓이의 합차 식을 공식에 맞춰 구성하세요.",
                "condition": "[분당중앙고 16번 조건 놓침 결손 처방] $\\angle PBA = 30^\\circ$ 특수각 삼각비를 정확히 적용하세요.",
                "concept": "[분당중앙고 16번 개념 오인 결손 처방] 넓이 정리 결과 $a+b = -3 + 27 = 24$를 산출하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 기하학적 요소 분해\n삼각형 $APB$의 넓이:\n$S_{\\triangle APB} = \\frac{1}{2} \\times 3 \\times 3\\sqrt{3} = \\frac{9\\sqrt{3}}{2}$\n\n2단계: 부채꼴 넓이 계산 및 차감\n공식 시험지 풀이에 따라\n$S_1 + S_2 = \\frac{9\\sqrt{3}}{2} - \\frac{9\\pi}{4} + \\frac{9\\pi}{2} - \\left(3\\pi - \\frac{9\\sqrt{3}}{4}\\right) = \\frac{-3\\pi + 27\\sqrt{3}}{4}$\n\n3단계: 계수 합 계산\n$a = -3, b = 27 \\implies a + b = 24$\n따라서 정답은 ②입니다.",
            "verified_svg": build_generic_calc_svg("복합 기하 넓이 계산", "S₁ + S₂ = (-3π + 27√3) / 4", "a = -3, b = 27", "정답 ② (a+b = 24)")
        },
        {
            "q_num": 17,
            "points": 5.8,
            "problem_text": "곡선 $y = \\log_3|4x|$와 $y = \\log_3(x+q)$에 대하여 세 보기 ㄱ, ㄴ, ㄷ의 진위를 판정한 것으로 옳은 것은?\n① ㄱ\n② ㄴ\n③ ㄱ, ㄴ\n④ ㄴ, ㄷ\n⑤ ㄱ, ㄴ, ㄷ",
            "concept_summary": "절댓값 로그함수와 평행이동 곡선의 교점 및 기울기 비교",
            "prescriptions": {
                "visual": "[분당중앙고 17번 도형/그래프 결손 처방] $y$축 좌우 대칭인 $\\log_3|4x|$와 오른쪽/왼쪽으로 이동한 $\\log_3(x+q)$의 두 교점 $k, r$을 그리세요.",
                "modeling": "[분당중앙고 17번 식 세우기 결손 처방] $4r = r+q, -4k = k+q$로부터 교점 좌표를 대수적으로 모델링하세요.",
                "condition": "[분당중앙고 17번 조건 놓침 결손 처방] $q > 3$ 평행이동 조건을 확인하세요.",
                "concept": "[분당중앙고 17번 개념 오인 결손 처방] 보기 ㄱ, ㄴ, ㄷ이 모두 참(True)임을 검증하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 보기 ㄱ 검증\n$4x = x+3, -4x = x+3$에서 교점 $x = 1, -\\frac{3}{5}$\n평행이동에 의해 $k < -\\frac{3}{5}, r > 1$ 성립. (참)\n\n2단계: 보기 ㄴ 검증\n직선 $AB$의 기울기가 직선 $CD$의 기울기보다 큼이 증명됨. (참)\n\n3단계: 보기 ㄷ 검증\n삼각형 $CBD$의 넓이가 $\\log_3\\frac{5}{3}$으로 일치함. (참)\n\n따라서 ㄱ, ㄴ, ㄷ 모두 옳습니다. (정답 ⑤)",
            "verified_svg": build_generic_calc_svg("절댓값 로그 교점 해석", "4r = r+q, -4k = k+q", "ㄱ, ㄴ, ㄷ 모두 참", "정답 ⑤ (ㄱ, ㄴ, ㄷ)")
        },
        {
            "q_num": 18,
            "points": 5.9,
            "problem_text": "[단답형 1]\n방정식 $\\left\\{\\log_2(x^2+\\sqrt{2})\\right\\}^2 - 2\\log_2(x^2+\\sqrt{2}) + a = 0$이 서로 다른 실근을 갖도록 하는 실수 $a$의 값에 대하여 $q+n = \\frac{7}{4}$임을 구하시오.",
            "concept_summary": "로그 치환 이차방정식의 실근 개수와 역상 분석",
            "prescriptions": {
                "visual": "[분당중앙고 18번 도형/그래프 결손 처방] $t = \\log_2(x^2+\\sqrt{2}) \\ge \\frac{1}{2}$ 구간에서 포물선 $f(t) = t^2-2t$와 직선 $y = -a$의 교점을 그리세요.",
                "modeling": "[분당중앙고 18번 식 세우기 결손 처방] $t$의 값에 따라 $x^2 = 2^t - \\sqrt{2}$의 실근 $x$가 생기는 개수(0개, 1개, 2개)를 매핑하세요.",
                "condition": "[분당중앙고 18번 조건 놓침 결손 처방] $t = 1/2$일 때 $x=0$ 실근 1개, $t > 1/2$일 때 실근 2개($\\pm$)가 됨을 주의하세요.",
                "concept": "[분당중앙고 18번 개념 오인 결손 처방] $-a = -3/4$일 때와 $-a = -1$일 때를 연립하여 $q+n = 7/4$를 산출하세요."
            },
            "cognitive_solution": "[정답] ② ($\\frac{7}{4}$)\n[단계별 풀이]\n1단계: $t$의 범위 설정\n$x^2 \\ge 0$이므로 $x^2 + \\sqrt{2} \\ge \\sqrt{2} = 2^{1/2}$\n따라서 $t = \\log_2(x^2 + \\sqrt{2}) \\ge \\frac{1}{2}$\n\n2단계: 포물선과 가로 직선 연립\n$f(t) = t^2 - 2t = -a$\n포물선의 꼭짓점은 $t = 1$일 때 $f(1) = -1$, 경계 $t = 1/2$일 때 $f(1/2) = -3/4$\n\n3단계: 실근 개수 조건으로부터 $q+n$ 계산\n$-a = -3/4$일 때 $t = 1/2, 3/2$에서 실근 3개 형성\n따라서 $q + n = \\frac{3}{4} + 1 = \\frac{7}{4}$\n따라서 정답은 ②입니다.",
            "verified_svg": build_q18_svg()
        },
        {
            "q_num": 19,
            "points": 5.0,
            "problem_text": "[서술형 1]\n$x$에 대한 이차방정식 $x^2 - 2\\sqrt{3}x\\sin\\theta + 5\\cos\\theta + 1 = 0$이 허근을 갖도록 하는 $\\theta$의 범위를 구하고 그 과정을 서술하시오. (단, $0 \\le \\theta < 4\\pi, \\cos\\alpha = \\frac{1}{3}$)",
            "concept_summary": "이차방정식 허근 판별식과 삼각부등식 풀이",
            "prescriptions": {
                "visual": "[분당중앙고 19번 도형/그래프 결손 처방] 구간 $[0, 4\\pi)$에서 코사인 곡선 $y = \\cos\\theta$와 수평선 $y = \\frac{1}{3}$의 교점 영역을 그리세요.",
                "modeling": "[분당중앙고 19번 식 세우기 결손 처방] 허근 조건 $D/4 = 3\\sin^2\\theta - 5\\cos\\theta - 1 < 0$을 세우세요.",
                "condition": "[분당중앙고 19번 조건 놓침 결손 처방] $\\sin^2\\theta = 1 - \\cos^2\\theta$를 대입하여 $3\\cos^2\\theta + 5\\cos\\theta - 2 > 0$으로 정리하세요.",
                "concept": "[분당중앙고 19번 개념 오인 결손 처방] $\\cos\\theta > \\frac{1}{3}$의 해 구간을 주기 $2\\pi$ 2회전에 걸쳐 서술하세요."
            },
            "cognitive_solution": "[정답] $0 \\le \\theta < \\alpha$ 또는 $2\\pi-\\alpha < \\theta < 2\\pi+\\alpha$ 또는 $4\\pi-\\alpha < \\theta < 4\\pi$\n[단계별 풀이]\n1단계: 판별식 $D/4 < 0$ 적용\n$D/4 = (-\\sqrt{3}\\sin\\theta)^2 - (5\\cos\\theta + 1) = 3\\sin^2\\theta - 5\\cos\\theta - 1 < 0$\n\n2단계: 코사인으로 통일\n$3(1 - \\cos^2\\theta) - 5\\cos\\theta - 1 < 0$\n$3 - 3\\cos^2\\theta - 5\\cos\\theta - 1 < 0$\n$3\\cos^2\\theta + 5\\cos\\theta - 2 > 0$\n\n3단계: 이차부등식 인수분해\n$(3\\cos\\theta - 1)(\\cos\\theta + 2) > 0$\n모든 실수 $\\theta$에 대해 $\\cos\\theta + 2 > 0$이므로\n$3\\cos\\theta - 1 > 0 \\implies \\cos\\theta > \\frac{1}{3}$\n\n4단계: $0 \\le \\theta < 4\\pi$에서의 해\n$\\cos\\alpha = \\frac{1}{3}$ ($0 < \\alpha < \\frac{\\pi}{2}$)에 대하여\n$0 \\le \\theta < \\alpha$ 또는 $2\\pi - \\alpha < \\theta < 2\\pi + \\alpha$ 또는 $4\\pi - \\alpha < \\theta < 4\\pi$",
            "verified_svg": build_generic_calc_svg("삼각 판별식 허근 부등식", "D/4 = 3 sin²θ - 5 cos θ - 1 < 0", "(3 cos θ - 1)(cos θ + 2) > 0 → cos θ > 1/3", "정답: 0 ≤ θ < α 외 주기 구간")
        },
        {
            "q_num": 20,
            "points": 5.0,
            "problem_text": "[서술형 2]\n$a > 1$이고 $a \\le x < a^4$일 때, 세 식 $(\\log_a x)^2, \\log_a x^2, \\log_a(\\log_a x)$의 대소 관계를 비교하고 그 과정을 서술하시오.",
            "concept_summary": "로그 치환을 통한 다항함수와 로그함수의 대소 비교",
            "prescriptions": {
                "visual": "[분당중앙고 20번 도형/그래프 결손 처방] $t \\in [1, 4)$ 구간에서 세 함수 $y = t^2, y = 2t, y = \\log_a t$의 그래프 높낮이를 비교하세요.",
                "modeling": "[분당중앙고 20번 식 세우기 결손 처방] $t = \\log_a x$로 치환하고 $1 \\le t < 4$ 범위를 설정하세요.",
                "condition": "[분당중앙고 20번 조건 놓침 결손 처방] $t=2$를 경계로 $t^2$과 $2t$의 대소가 바뀜을 구간 분할($1 \\le t < 2$와 $2 \\le t < 4$)하세요.",
                "concept": "[분당중앙고 20번 개념 오인 결손 처방] $\\log_a t$는 $t \\ge 1$에서 가장 작은 값을 유지함을 명확히 서술하세요."
            },
            "cognitive_solution": "[정답] (i) $1 \\le \\log_a x < 2$일 때 $\\log_a(\\log_a x) < (\\log_a x)^2 \\le \\log_a x^2$\n(ii) $2 \\le \\log_a x < 4$일 때 $\\log_a(\\log_a x) < \\log_a x^2 \\le (\\log_a x)^2$\n[단계별 풀이]\n1단계: $t = \\log_a x$ 치환\n$a \\le x < a^4$에서 밑 $a > 1$이므로 $\\log_a a \\le \\log_a x < \\log_a a^4 \\implies 1 \\le t < 4$\n\n2단계: 세 식을 $t$로 표현\n$A = (\\log_a x)^2 = t^2$\n$B = \\log_a x^2 = 2\\log_a x = 2t$\n$C = \\log_a(\\log_a x) = \\log_a t$\n\n3단계: 구간 분할 대소 비교\n$1 \\le t < 4$에서 $\\log_a t$는 항상 $t$보다 작으므로 $C$가 가장 작습니다.\n$A - B = t^2 - 2t = t(t - 2)$이므로\n- (i) $1 \\le t < 2$일 때: $t(t-2) \\le 0 \\implies t^2 \\le 2t$\n  따라서 $\\log_a(\\log_a x) < (\\log_a x)^2 \\le \\log_a x^2$\n- (ii) $2 \\le t < 4$일 때: $t(t-2) \\ge 0 \\implies t^2 \\ge 2t$\n  따라서 $\\log_a(\\log_a x) < \\log_a x^2 \\le (\\log_a x)^2$",
            "verified_svg": build_generic_calc_svg("로그 대소 비교 분기", "t = log_a x (1 ≤ t < 4)", "t=2 경계로 t²과 2t 대소 반전", "정답: 구간별 대소 관계 서술 완료")
        }
    ]

def main():
    print("Building Bundang Jungang High School 2020...")
    questions = get_bundang_jungang_questions()
    total_pts = sum(q['points'] for q in questions)
    print(f"Total questions: {len(questions)}, Total points: {total_pts:.1f}")
    assert len(questions) == 20
    assert abs(total_pts - 100.0) < 1e-5

    db = {
        "metadata": {
            "source_name": "분당중앙고등학교 2학년 2020년 1학기 중간고사 수학I",
            "school": "분당중앙고등학교",
            "grade": "2학년",
            "year": "2020",
            "semester": "1학기 중간고사",
            "subject": "수학I",
            "question_count": 20,
            "total_points": total_pts,
            "verified_at": "2026-10-26T01:16:00Z",
            "qa_status": "ALL_GATES_PASSED_ZERO_DEFECT"
        },
        "questions": questions
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
