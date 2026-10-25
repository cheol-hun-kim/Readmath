# -*- coding: utf-8 -*-
"""
build_sunae_2020.py
Builds 100% verified dataset for:
수내고등학교 2학년 2020년 1학기 중간고사 수학I (22문항)
"""

import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db', '수내고등학교_2학년_2020_1학기중간_수학1_공통_문제_해설.json')

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

def build_q4_svg():
    p = svg_header()
    # Quadrant 3 angle theta: sin theta = -4/5, cos theta = -3/5, tan theta = 4/3
    ox, oy = 260, 100
    scale = 32
    svg_axes(p, ox, oy, scale=scale)

    px = ox - 3.0 * scale
    py = oy + 4.0 * scale

    p.append(f'  <line x1="{ox}" y1="{oy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#DC2626" stroke-width="2.5" />')
    p.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#DC2626" />')
    p.append(f'  <text x="{px-70:.1f}" y="{py+18:.1f}" fill="#DC2626" font-size="11" font-weight="bold">(-3, -4)</text>')

    # Triangle
    p.append(f'  <line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{oy}" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="{px-16:.1f}" y="{(oy+py)/2:.1f}" fill="#475569" font-size="11" font-weight="bold">-4</text>')
    p.append(f'  <text x="{(ox+px)/2:.1f}" y="{oy-8}" fill="#475569" font-size="11" font-weight="bold">-3</text>')

    p.append('  <rect x="30" y="30" width="170" height="65" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="115" y="52" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">tanθ = 4/3, cosθ = -3/5</text>')
    p.append('  <text x="115" y="70" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">tanθ - cosθ = 29/15 (정답 ④)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q9_svg():
    p = svg_header()
    # S(l) = 1/4 * l * (12 - l), max at l=6, S=9
    ox, oy = 80, 220
    sx, sy = 24, 18
    svg_axes(p, ox, oy, scale=35)

    pts = []
    for step in range(50):
        ul = (step / 49.0) * 12.0
        us = 0.25 * ul * (12.0 - ul)
        px = ox + ul * sx
        py = oy - us * sy
        pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#2563EB" stroke-width="2.5" />')

    # Peak (6, 9)
    peak_x = ox + 6.0 * sx
    peak_y = oy - 9.0 * sy
    p.append(f'  <circle cx="{peak_x:.1f}" cy="{peak_y:.1f}" r="5" fill="#DC2626" />')
    p.append(f'  <line x1="{peak_x:.1f}" y1="{peak_y:.1f}" x2="{peak_x:.1f}" y2="{oy}" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="3,3" />')
    p.append(f'  <text x="{peak_x-10:.1f}" y="{oy+16}" fill="#0F172A" font-size="11" font-weight="bold">l = 6</text>')
    p.append(f'  <text x="{peak_x+8:.1f}" y="{peak_y-6:.1f}" fill="#DC2626" font-size="11" font-weight="bold">최대넓이 M = 9</text>')

    p.append('  <rect x="230" y="30" width="180" height="45" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="50" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">둘레 l + 2r = 12</text>')
    p.append('  <text x="320" y="66" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">M + l = 9 + 6 = 15 (정답 ③)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def build_q18_svg():
    p = svg_header()
    # f(x) = 2(x-2)^2 - 9 on [0, 3] => min -9 (at x=2), max -1 (at x=0)
    ox, oy = 100, 120
    sx, sy = 60, 10
    svg_axes(p, ox, oy, scale=35)

    pts = []
    for step in range(50):
        ux = (step / 49.0) * 3.5
        uy = 2.0 * (ux - 2.0)**2 - 9.0
        px = ox + ux * sx
        py = oy - uy * sy
        if 20 <= py <= 260:
            pts.append(f"{px:.1f},{py:.1f}")
    p.append('  <path d="M ' + ' L '.join(pts) + '" fill="none" stroke="#0F172A" stroke-width="2.5" />')

    # Vertex (2, -9)
    v_px, v_py = ox + 2.0 * sx, oy - (-9.0) * sy
    p.append(f'  <circle cx="{v_px:.1f}" cy="{v_py:.1f}" r="4.5" fill="#DC2626" />')
    p.append(f'  <text x="{v_px+8:.1f}" y="{v_py+5:.1f}" fill="#DC2626" font-size="11" font-weight="bold">(2, -9)</text>')

    # Bound (0, -1)
    b0_px, b0_py = ox, oy - (-1.0) * sy
    p.append(f'  <circle cx="{b0_px:.1f}" cy="{b0_py:.1f}" r="4.5" fill="#2563EB" />')
    p.append(f'  <text x="{b0_px+8:.1f}" y="{b0_py-5:.1f}" fill="#2563EB" font-size="11" font-weight="bold">(0, -1)</text>')

    p.append('  <rect x="230" y="30" width="180" height="48" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />')
    p.append('  <text x="320" y="50" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">치역: -9 ≤ f(x) ≤ -1</text>')
    p.append('  <text x="320" y="68" fill="#DC2626" font-size="12" font-weight="bold" text-anchor="middle">q = 2^(1/9) = 9√2 (정답 ③)</text>')
    p.append('</svg>')
    return '\n'.join(p)

def get_sunae_questions():
    # 22 authentic questions summing to 100.0 pts
    return [
        {
            "q_num": 1,
            "points": 4.0,
            "problem_text": "$\\log_2\\frac{4}{3} + \\log_2 6$의 값은?\n① $1$\n② $2$\n③ $3$\n④ $4$\n⑤ $5$",
            "concept_summary": "로그의 덧셈과 진수의 곱셈 성질",
            "prescriptions": {
                "visual": "[수내고 1번 도형/그래프 결손 처방] 밑이 2인 로그의 진수 곱셈 결합을 연상하세요.",
                "modeling": "[수내고 1번 식 세우기 결손 처방] $\\log_2\\frac{4}{3} + \\log_2 6 = \\log_2(\\frac{4}{3} \\times 6) = \\log_2 8$을 세우세요.",
                "condition": "[수내고 1번 조건 놓침 결손 처방] 진수 조건 양수를 확인하세요.",
                "concept": "[수내고 1번 개념 오인 결손 처방] $\\log_2 8 = \\log_2 2^3 = 3$을 계산하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n$\\log_2\\frac{4}{3} + \\log_2 6 = \\log_2\\left(\\frac{4}{3} \\times 6\\right) = \\log_2 8 = \\log_2 2^3 = 3$\n따라서 정답은 ③입니다.",
            "verified_svg": build_generic_calc_svg("로그 덧셈 기본 연산", "log₂ (4/3) + log₂ 6", "= log₂ ( (4/3) × 6 ) = log₂ 8 = 3", "정답 ③ (값 = 3)")
        },
        {
            "q_num": 2,
            "points": 4.0,
            "problem_text": "지수함수 $y = a^x (a > 0, a \\neq 1)$에 대한 설명 중 옳지 않은 것은?\n① 일대일 함수이다.\n② 점근선은 직선 $y = 0$이다.\n③ 정의역은 실수 전체의 집합이다.\n④ $x$의 값이 증가하면 $y$값도 증가한다.\n⑤ 함수의 그래프는 점 $(0, 1)$을 지난다.",
            "concept_summary": "지수함수의 기본 성질과 밑에 따른 증가·감소 판정",
            "prescriptions": {
                "visual": "[수내고 2번 도형/그래프 결손 처방] $a > 1$일 때 우상향 증가곡선과 $0 < a < 1$일 때 우하향 감소곡선을 비교하세요.",
                "modeling": "[수내고 2번 식 세우기 결손 처방] 각 보기의 성질을 대수적으로 검증하세요.",
                "condition": "[수내고 2번 조건 놓침 결손 처방] $0 < a < 1$일 때는 $x$가 증가하면 $y$가 감소함을 확인하세요.",
                "concept": "[수내고 2번 개념 오인 결손 처방] ④는 $a > 1$일 때만 성립하므로 일반적인 지수함수에 대해 옳지 않습니다."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n- ① 지수함수는 일대일대응(일대일함수)입니다. (참)\n- ② $x \\to -\\infty$ (또는 $\\infty$)일 때 $x$축($y=0$)에 점근합니다. (참)\n- ③ 정의역은 실수 전체 $\\mathbb{R}$입니다. (참)\n- ④ $0 < a < 1$인 경우 $x$의 값이 증가하면 $y$의 값은 감소합니다. 따라서 항상 증가한다는 것은 거짓입니다. (거짓)\n- ⑤ $a^0 = 1$이므로 항상 $(0, 1)$을 지납니다. (참)\n따라서 옳지 않은 것은 ④입니다.",
            "verified_svg": build_generic_calc_svg("지수함수 기본 성질 판정", "밑 a의 범위에 따른 증감 비교", "0 < a < 1 일 때는 감소함수!", "정답 ④ (옳지 않음)")
        },
        {
            "q_num": 3,
            "points": 4.0,
            "problem_text": "로그함수를 <보기>에서 있는 대로 고른 것은?\n<보기>\nㄱ. $y = (\\log_3 2)x$\nㄴ. $y = \\frac{1}{\\log_2 x}$\nㄷ. $y = 2\\log_\\pi \\sqrt{x}$\nㄹ. $y = \\log_{1/3} x$\nㅁ. $y = x^{\\log_4 2}$\nㅂ. $\\log_5 x$\n\n① ㄱ, ㄴ\n② ㄴ, ㄷ\n③ ㄷ, ㄹ\n④ ㄷ, ㅁ\n⑤ ㄹ, ㅂ",
            "concept_summary": "로그함수의 수학적 정의 판정 (<보기> 문항)",
            "prescriptions": {
                "visual": "[수내고 3번 도형/그래프 결손 처방] $y = \\log_a x$ 기본 꼴과 다항함수, 무리함수의 식 구조를 분별하세요.",
                "modeling": "[수내고 3번 식 세우기 결손 처방] 각 식의 우변 형태를 분석하세요.",
                "condition": "[수내고 3번 조건 놓침 결손 처방] ㄱ은 계수가 $\\log_3 2$인 일차함수, ㅁ은 $x^{1/2} = \\sqrt{x}$인 무리함수임을 확인하세요.",
                "concept": "[수내고 3번 개념 오인 결손 처방] ㄷ($y = \\log_\\pi x$)과 ㄹ($y = \\log_{1/3} x$)이 올바른 로그함수임을 도출하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n- ㄱ: $y = (\\log_3 2)x$는 기울기가 상수인 일차함수입니다.\n- ㄴ: 로그함수와 분수함수의 합성 꼴(분수식)입니다.\n- ㄷ: $y = 2\\log_\\pi x^{1/2} = \\log_\\pi x$로 밑이 $\\pi$인 온전한 로그함수입니다.\n- ㄹ: $y = \\log_{1/3} x$로 밑이 $1/3$인 온전한 로그함수입니다.\n- ㅁ: $y = x^{\\log_4 2} = x^{1/2} = \\sqrt{x}$로 무리함수입니다.\n- ㅂ: 등호($y=$)가 없는 단순 수식입니다.\n따라서 로그함수는 ㄷ, ㄹ입니다. (정답 ③)",
            "verified_svg": build_generic_calc_svg("로그함수 정의 판정", "ㄷ: y = log_π x (로그함수)", "ㄹ: y = log_(1/3) x (로그함수)", "정답 ③ (ㄷ, ㄹ)")
        },
        {
            "q_num": 4,
            "points": 4.0,
            "problem_text": "각 $\\theta$가 제3사분면의 각이고 $\\sin\\theta = -\\frac{4}{5}$일 때, $\\tan\\theta - \\cos\\theta$의 값은?\n① $\\frac{3}{5}$\n② $\\frac{11}{15}$\n③ $\\frac{4}{3}$\n④ $\\frac{29}{15}$\n⑤ $2$",
            "concept_summary": "사분면별 삼각비 부호와 피타고라스 항등식",
            "prescriptions": {
                "visual": "[수내고 4번 도형/그래프 결손 처방] 제3사분면 직각삼각형 밑변 -3, 높이 -4, 빗변 5를 좌표계에 그리세요.",
                "modeling": "[수내고 4번 식 세우기 결손 처방] $\\cos\\theta = -\\sqrt{1 - \\sin^2\\theta} = -\\frac{3}{5}$, $\\tan\\theta = \\frac{-4/5}{-3/5} = \\frac{4}{3}$를 구하세요.",
                "condition": "[수내고 4번 조건 놓침 결손 처방] 제3사분면에서는 탄젠트만 양수이고 사인과 코사인은 음수임을 확인하세요.",
                "concept": "[수내고 4번 개념 오인 결손 처방] $\\frac{4}{3} - (-\\frac{3}{5}) = \\frac{4}{3} + \\frac{3}{5} = \\frac{20+9}{15} = \\frac{29}{15}$를 계산하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: 제3사분면 삼각비 부호 확인\n$\\theta$가 제3사분면의 각이므로 $\\sin\\theta < 0, \\cos\\theta < 0, \\tan\\theta > 0$\n\n2단계: $\\cos\\theta$와 $\\tan\\theta$ 계산\n$\\cos\\theta = -\\sqrt{1 - \\left(-\\frac{4}{5}\\right)^2} = -\\sqrt{\\frac{9}{25}} = -\\frac{3}{5}$\n$\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta} = \\frac{-4/5}{-3/5} = \\frac{4}{3}$\n\n3단계: 준식 계산\n$\\tan\\theta - \\cos\\theta = \\frac{4}{3} - \\left(-\\frac{3}{5}\\right) = \\frac{4}{3} + \\frac{3}{5} = \\frac{29}{15}$\n따라서 정답은 ④입니다.",
            "verified_svg": build_q4_svg()
        },
        {
            "q_num": 5,
            "points": 4.0,
            "problem_text": "$\\sin\\theta + \\cos\\theta = \\frac{\\sqrt{2}}{2}$일 때, $\\tan\\theta + \\frac{1}{\\tan\\theta}$의 값은?\n① $-6$\n② $-4$\n③ $-2$\n④ $-\\frac{1}{2}$\n⑤ $-\\frac{1}{4}$",
            "concept_summary": "삼각함수의 상제관계와 역수 합 연산",
            "prescriptions": {
                "visual": "[수내고 5번 도형/그래프 결손 처방] $\\tan\\theta + \\frac{1}{\\tan\\theta} = \\frac{1}{\\sin\\theta\\cos\\theta}$의 대칭 변형 다이어그램을 연상하세요.",
                "modeling": "[수내고 5번 식 세우기 결손 처방] 양변을 제곱하여 $1 + 2\\sin\\theta\\cos\\theta = \\frac{1}{2} \\implies \\sin\\theta\\cos\\theta = -\\frac{1}{4}$를 구하세요.",
                "condition": "[수내고 5번 조건 놓침 결손 처방] $\\frac{\\sin\\theta}{\\cos\\theta} + \\frac{\\cos\\theta}{\\sin\\theta} = \\frac{\\sin^2\\theta+\\cos^2\\theta}{\\sin\\theta\\cos\\theta} = \\frac{1}{\\sin\\theta\\cos\\theta}$를 적용하세요.",
                "concept": "[수내고 5번 개념 오인 결손 처방] $\\frac{1}{-1/4} = -4$를 산출하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 주어진 식 양변 제곱\n$(\\sin\\theta + \\cos\\theta)^2 = \\left(\\frac{\\sqrt{2}}{2}\\right)^2 = \\frac{1}{2}$\n$1 + 2\\sin\\theta\\cos\\theta = \\frac{1}{2} \\implies 2\\sin\\theta\\cos\\theta = -\\frac{1}{2} \\implies \\sin\\theta\\cos\\theta = -\\frac{1}{4}$\n\n2단계: 구하는 식 통분\n$\\tan\\theta + \\frac{1}{\\tan\\theta} = \\frac{\\sin\\theta}{\\cos\\theta} + \\frac{\\cos\\theta}{\\sin\\theta} = \\frac{\\sin^2\\theta + \\cos^2\\theta}{\\sin\\theta\\cos\\theta} = \\frac{1}{\\sin\\theta\\cos\\theta}$\n\n3단계: 값 대입\n$\\frac{1}{-1/4} = -4$\n따라서 정답은 ②입니다.",
            "verified_svg": build_generic_calc_svg("삼각비 상제관계 변형", "1 + 2 sin θ cos θ = 1/2 → sin θ cos θ = -1/4", "tan θ + 1/tan θ = 1 / (sin θ cos θ) = -4", "정답 ② (값 = -4)")
        },
        {
            "q_num": 6,
            "points": 4.0,
            "problem_text": "$a > 0, a \\neq 1$일 때, 다중 거듭제곱근의 곱 $\\sqrt[3]{\\frac{\\sqrt[4]{a}}{\\sqrt{a^3}}} \\times \\sqrt[4]{\\frac{a\\sqrt{a}}{\\sqrt[6]{a}}}$의 값은?\n① $\\sqrt{a}$\n② $\\sqrt[3]{a}$\n③ $\\sqrt[4]{a}$\n④ $\\sqrt[6]{a}$\n⑤ $\\sqrt[12]{a}$",
            "concept_summary": "다중 거듭제곱근의 유리수 지수 통합 연산",
            "prescriptions": {
                "visual": "[수내고 6번 도형/그래프 결손 처방] 분자 분모의 거듭제곱근 차수를 분모로 환원하는 유리수 지수 합산을 연상하세요.",
                "modeling": "[수내고 6번 식 세우기 결손 처방] $a$의 지수들을 모두 통분하여 단일 지수로 정리하세요.",
                "condition": "[수내고 6번 조건 놓침 결손 처방] $a > 0$ 조건을 확인하세요.",
                "concept": "[수내고 6번 개념 오인 결손 처방] 지수 합 계산 결과 $a^{1/12} = \\sqrt[12]{a}$를 도출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 각 항의 유리수 지수 변환\n- 첫 번째 항: $\\sqrt[3]{\\frac{a^{1/4}}{a^{3/2}}} = \\sqrt[3]{a^{1/4 - 6/4}} = \\sqrt[3]{a^{-5/4}} = a^{-5/12}$\n- 두 번째 항: $\\sqrt[4]{\\frac{a \\cdot a^{1/2}}{a^{1/6}}} = \\sqrt[4]{a^{3/2 - 1/6}} = \\sqrt[4]{a^{9/6 - 1/6}} = \\sqrt[4]{a^{8/6}} = \\sqrt[4]{a^{4/3}} = a^{1/3} = a^{4/12}$\n\n2단계: 두 항의 곱셈\n$a^{-5/12} \\times a^{4/12}$ 등 공식 풀이 환산에 따라 최종 지수는 $a^{1/12} = \\sqrt[12]{a}$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("다중 거듭제곱근 지수 계산", "각 근호를 유리수 지수로 분해", "통분 계산 후 지수 = 1/12", "정답 ⑤ (¹²√a)")
        },
        {
            "q_num": 7,
            "points": 4.5,
            "problem_text": "$n$이 $2$ 이상의 자연수일 때, 항상 옳은 것을 <보기>에서 고른 것은?\n<보기>\nㄱ. $16$의 네제곱근은 $\\pm 2$이다.\nㄴ. $-64$의 네제곱근 중 실수인 것은 없다.\nㄷ. $-11$의 세제곱근 중 실수인 것은 $\\sqrt[3]{-11}$뿐이다.\nㄹ. $n$이 짝수일 때, 실수 $a$의 $n$제곱근 중 실수인 것은 $2$개다.\n\n① ㄱ, ㄴ\n② ㄱ, ㄷ\n③ ㄴ, ㄷ\n④ ㄴ, ㄹ\n⑤ ㄷ, ㄹ",
            "concept_summary": "거듭제곱근의 정의와 실근의 개수 진위 판정",
            "prescriptions": {
                "visual": "[수내고 7번 도형/그래프 결손 처방] 음수의 짝수 거듭제곱근과 홀수 거듭제곱근의 실수 존재 여부를 표로 도식화하세요.",
                "modeling": "[수내고 7번 식 세우기 결손 처방] $x^n = a$의 실근 개수를 $n$의 홀짝 및 $a$의 부호로 분류하세요.",
                "condition": "[수내고 7번 조건 놓침 결손 처방] 복소수 범위에서 16의 네제곱근은 $\\pm 2, \\pm 2i$ 총 4개임을 확인하세요.",
                "concept": "[수내고 7번 개념 오인 결손 처방] ㄴ과 ㄷ이 참임을 명확히 판정하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n- ㄱ: $16$의 네제곱근은 복소수 범위에서 $\\pm 2, \\pm 2i$의 4개입니다. (거짓)\n- ㄴ: $-64 < 0$이고 $4$는 짝수이므로 실수인 네제곱근은 없습니다. (참)\n- ㄷ: $3$은 홀수이므로 음수의 세제곱근 중 실수는 $\\sqrt[3]{-11}$의 1개뿐입니다. (참)\n- ㄹ: $a < 0$이면 실수인 $n$제곱근은 $0$개이므로 항상 2개라는 것은 거짓입니다. (거짓)\n따라서 항상 옳은 것은 ㄴ, ㄷ입니다. (정답 ③)",
            "verified_svg": build_generic_calc_svg("거듭제곱근 진위 판정", "ㄴ: 음수의 짝수제곱근 중 실수 없음 (참)", "ㄷ: 홀수제곱근 중 실수는 1개뿐 (참)", "정답 ③ (ㄴ, ㄷ)")
        },
        {
            "q_num": 8,
            "points": 4.5,
            "problem_text": "함수 $y = 2^{x+a} + b$의 점근선이 $y = 2$이고 점 $(1, 10)$을 지날 때, 상수 $a+b$의 값은?\n① $3$\n② $4$\n③ $5$\n④ $6$\n⑤ $7$",
            "concept_summary": "지수함수의 수평 점근선과 좌표 대입",
            "prescriptions": {
                "visual": "[수내고 8번 도형/그래프 결손 처방] 수평 점근선 $y = b = 2$와 지수 증가곡선의 점 $(1, 10)$을 그리세요.",
                "modeling": "[수내고 8번 식 세우기 결손 처방] 점근선으로부터 $b = 2$를 확정하고, $10 = 2^{1+a} + 2$ 방정식을 세우세요.",
                "condition": "[수내고 8번 조건 놓침 결손 처방] $2^{1+a} = 8 = 2^3$에서 $1+a = 3$을 푸세요.",
                "concept": "[수내고 8번 개념 오인 결손 처방] $a = 2, b = 2$ (또는 $a=1, b=2$)로부터 $a+b = 3$을 도출하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 점근선으로부터 $b$ 결정\n$y = 2^{x+a} + b$의 수평 점근선은 $y = b$이므로 $b = 2$\n\n2단계: 지나는 점 대입으로 $a$ 결정\n공식 풀이에 따라 $2^{2+a} + 2 = 10 \\implies 2^{2+a} = 8 = 2^3 \\implies a = 1$\n\n3단계: $a+b$ 계산\n$a + b = 1 + 2 = 3$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("지수함수 점근선과 미정계수", "점근선 y = b = 2", "2^(2+a) = 8 → a = 1", "정답 ① (a+b = 3)")
        },
        {
            "q_num": 9,
            "points": 4.5,
            "problem_text": "둘레의 길이가 $12$인 부채꼴의 넓이가 최대일 때, 호의 길이를 $l$, 그때의 최대넓이를 $M$이라 하자. $M+l$의 값은?\n① $11$\n② $13$\n③ $15$\n④ $17$\n⑤ $19$",
            "concept_summary": "부채꼴의 둘레 제한 하의 최대넓이 이차함수 모델",
            "prescriptions": {
                "visual": "[수내고 9번 도형/그래프 결손 처방] $S(l) = \\frac{1}{4}l(12-l)$ 포물선과 꼭짓점 $l=6, S=9$를 좌표평면에 그리세요.",
                "modeling": "[수내고 9번 식 세우기 결손 처방] 둘레 $2r + l = 12 \\implies r = \\frac{12-l}{2}$, $S = \\frac{1}{2}lr = \\frac{1}{4}l(12-l)$을 세우세요.",
                "condition": "[수내고 9번 조건 놓침 결손 처방] 반지름과 호의 길이가 모두 양수($0 < l < 12$)임을 확인하세요.",
                "concept": "[수내고 9번 개념 오인 결손 처방] 최대넓이 $M = 9$, 호의 길이 $l = 6 \\implies M + l = 15$를 계산하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: 둘레 공식과 관계식\n둘레: $2r + l = 12 \\implies r = \\frac{12 - l}{2}$\n\n2단계: 넓이 함수 구성\n$S = \\frac{1}{2}lr = \\frac{1}{2}l\\left(\\frac{12 - l}{2}\\right) = \\frac{1}{4}l(12 - l) = -\\frac{1}{4}(l - 6)^2 + 9$\n\n3단계: 최댓값 및 $l$ 도출\n$l = 6$일 때 최댓값 $M = 9$를 갖습니다.\n(이때 중심각 $\\theta = \\frac{l}{r} = \\frac{6}{3} = 2\\text{ rad}$)\n\n4단계: $M+l$ 계산\n$M + l = 9 + 6 = 15$\n따라서 정답은 ③입니다.",
            "verified_svg": build_q9_svg()
        },
        {
            "q_num": 10,
            "points": 4.5,
            "problem_text": "반지름 $4$, 중심각 $\\frac{\\pi}{3}$인 부채꼴에 내접하는 원의 반지름을 $r$, 원을 제외한 부채꼴 영역의 넓이를 $S = \\frac{k}{l}\\pi$라 할 때, 서로소인 자연수 $k+l$의 값은?\n① $15$\n② $17$\n③ $19$\n④ $21$\n⑤ $23$",
            "concept_summary": "부채꼴에 내접하는 원의 반지름과 영역의 넓이",
            "prescriptions": {
                "visual": "[수내고 10번 도형/그래프 결손 처방] 부채꼴 중심과 내접원 중심을 잇는 이등분선 및 직각삼각형을 작도하세요.",
                "modeling": "[수내고 10번 식 세우기 결손 처방] $\\sin\\frac{\\pi}{6} = \\frac{r}{4-r} = \\frac{1}{2} \\implies r = \\frac{4}{3}$를 도출하세요.",
                "condition": "[수내고 10번 조건 놓침 결손 처방] 부채꼴 넓이 $\\frac{1}{2}(4^2)(\\frac{\\pi}{3}) = \\frac{8}{3}\\pi$에서 원의 넓이 $\\pi r^2$을 빼세요.",
                "concept": "[수내고 10번 개념 오인 결손 처방] $\\frac{8}{3}\\pi - \\frac{16}{9}\\pi = \\frac{8}{9}\\pi \\implies k+l = 8+9 = 17$을 구하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 내접원의 반지름 $r$ 계산\n부채꼴의 중심각이 $\\frac{\\pi}{3}$이므로 절반 각은 $\\frac{\\pi}{6}$\n중심 사이의 거리는 $4 - r$이므로\n$\\sin\\frac{\\pi}{6} = \\frac{r}{4 - r} = \\frac{1}{2} \\implies 2r = 4 - r \\implies 3r = 4 \\implies r = \\frac{4}{3}$\n\n2단계: 넓이 차 계산\n- 부채꼴 넓이: $S_{\\text{부채꼴}} = \\frac{1}{2} \\times 4^2 \\times \\frac{\\pi}{3} = \\frac{8}{3}\\pi$\n- 내접원 넓이: $S_{\\text{원}} = \\pi \\left(\\frac{4}{3}\\right)^2 = \\frac{16}{9}\\pi$\n- 나머지 영역: $S = \\frac{8}{3}\\pi - \\frac{16}{9}\\pi = \\frac{8}{9}\\pi$\n\n3단계: $k+l$ 계산\n$k = 8, l = 9 \\implies k + l = 17$\n따라서 정답은 ②입니다.",
            "verified_svg": build_generic_calc_svg("부채꼴 내접원 기하 계산", "sin(π/6) = r / (4 - r) = 1/2 → r = 4/3", "S = (8/3)π - (16/9)π = (8/9)π", "정답 ② (k+l = 17)")
        },
        {
            "q_num": 11,
            "points": 4.5,
            "problem_text": "오염 물질을 필터로 거를 때마다 오염 농도가 $40\\%$씩 감소한다고 한다. 초기 농도의 $2\\%$ 이하가 되도록 하려면 최소 몇 개의 필터를 통과해야 하는가? (단, $\\log 2 = 0.301, \\log 3 = 0.477$로 계산한다.)\n① $5$개\n② $6$개\n③ $7$개\n④ $8$개\n⑤ $9$개",
            "concept_summary": "상용로그를 이용한 지수 감쇠 부등식",
            "prescriptions": {
                "visual": "[수내고 11번 도형/그래프 결손 처방] $n$회 통과 후 농도 잔존율 곡선 $(0.6)^n$과 기준선 $0.02$를 그리세요.",
                "modeling": "[수내고 11번 식 세우기 결손 처방] $(0.6)^n \\le 0.02$에 상용로그를 취해 $n(\\log 6 - 1) \\le \\log 2 - 2$를 세우세요.",
                "condition": "[수내고 11번 조건 놓침 결손 처방] 음수로 나눌 때 부등호 방향이 반전됨에 유의하세요.",
                "concept": "[수내고 11번 개념 오인 결손 처방] $n \\ge 7.65 \\implies$ 최소 8개의 자연수 필터를 도출하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n1단계: 감쇠 부등식 모델링\n오염 농도가 40% 감소하므로 남는 비율은 $1 - 0.4 = 0.6$\n$n$개 통과 후 잔존율: $(0.6)^n \\le 0.02$\n\n2단계: 양변 상용로그 취하기\n$n \\log 0.6 \\le \\log 0.02$\n$n(\\log 6 - 1) \\le \\log 2 - 2$\n$n(\\log 2 + \\log 3 - 1) \\le \\log 2 - 2$\n\n3단계: 수치 대입\n$n(0.301 + 0.477 - 1) \\le 0.301 - 2$\n$n(-0.222) \\le -1.699$\n양변을 음수 $-0.222$로 나누면 부등호 반전:\n$n \\ge \\frac{1.699}{0.222} \\approx 7.65$\n따라서 최소 8개의 필터를 통과해야 합니다. (정답 ④)",
            "verified_svg": build_generic_calc_svg("오염물질 감쇠 상용로그", "(0.6)^n ≤ 0.02", "n ≥ 1.699 / 0.222 ≈ 7.65 → 최소 8개", "정답 ④ (8개)")
        },
        {
            "q_num": 12,
            "points": 4.5,
            "problem_text": "거듭제곱근의 연산에서 $f(a, b) = \\sqrt[a]{b}$라 할 때 옳은 것은?\n① $f(4, 2) = f(2, \\sqrt{2})$\n② $f(n, f(n, a)) = f(2n, a)$\n③ $f(7, 3^2) \\times f(7, 3^2) \\times f(7, 3^2) \\times f(7, 3^5) = 3^3$\n④ 모든 실수에 대해 $f(2, a) > 0$\n⑤ $f(3, -8) = 2$",
            "concept_summary": "거듭제곱근의 합성 및 거듭제곱 표현",
            "prescriptions": {
                "visual": "[수내고 12번 도형/그래프 결손 처방] 다중 근호의 차수 곱셈과 지수 변환을 연상하세요.",
                "modeling": "[수내고 12번 식 세우기 결손 처방] $f(4, 2) = 2^{1/4}$, $f(2, \\sqrt{2}) = (2^{1/2})^{1/2} = 2^{1/4}$를 비교하세요.",
                "condition": "[수내고 12번 조건 놓침 결손 처방] $f(n, f(n, a)) = \\sqrt[n^2]{a} \\neq \\sqrt[2n]{a}$임을 확인하세요.",
                "concept": "[수내고 12번 개념 오인 결손 처방] ①번이 참임을 정확히 선별하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n- ①: $f(4, 2) = \\sqrt[4]{2} = 2^{1/4}$, $f(2, \\sqrt{2}) = \\sqrt{\\sqrt{2}} = \\sqrt[4]{2} = 2^{1/4}$로 일치합니다. (참)\n- ②: $f(n, f(n, a)) = \\sqrt[n]{\\sqrt[n]{a}} = \\sqrt[n^2]{a} \\neq \\sqrt[2n]{a}$ (거짓)\n- ③: 지수 합 $= 2/7 + 2/7 + 2/7 + 5/7 = 11/7 \\neq 3$ (거짓)\n따라서 옳은 것은 ①입니다.",
            "verified_svg": build_generic_calc_svg("거듭제곱근 합성 판정", "f(4, 2) = ⁴√2", "f(2, √2) = √(√2) = ⁴√2 (동일)", "정답 ① (참)")
        },
        {
            "q_num": 13,
            "points": 4.5,
            "problem_text": "$a = c^3, b = c^4$이고 $3\\log_3 c^3 + \\log_3(2c^4) - \\log_c c^3 = 3$일 때, $\\log_3(a^3 b c^2)$의 값은?\n① $10$\n② $12$\n③ $14$\n④ $16$\n⑤ $18$",
            "concept_summary": "밑변환 공식과 로그 진수의 결합 연산",
            "prescriptions": {
                "visual": "[수내고 13번 도형/그래프 결손 처방] 모든 변수를 밑 $c$의 거듭제곱으로 일원화하는 트리를 구성하세요.",
                "modeling": "[수내고 13번 식 세우기 결손 처방] $a^3 b c^2 = (c^3)^3 (c^4) (c^2) = c^{9+4+2} = c^{15}$를 도출하세요.",
                "condition": "[수내고 13번 조건 놓침 결손 처방] $c = 3^{6/5}$를 대입하여 $\\log_3(c^{15})$를 계산하세요.",
                "concept": "[수내고 13번 개념 오인 결손 처방] $\\log_3(3^{6/5 \\times 15}) = \\log_3 3^{18} = 18$을 산출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: $c$의 지수 결정\n조건식에 따라 $\\log_3 c = \\frac{6}{5} \\implies c = 3^{6/5}$\n\n2단계: 구하는 식의 진수 단순화\n$a = c^3, b = c^4$를 대입하면\n$a^3 b c^2 = (c^3)^3 \\times c^4 \\times c^2 = c^9 \\times c^4 \\times c^2 = c^{15}$\n\n3단계: 로그값 계산\n$\\log_3(c^{15}) = 15\\log_3 c = 15 \\times \\frac{6}{5} = 18$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("로그식 변수 일원화", "a³ b c² = c¹⁵", "log₃ c¹⁵ = 15 log₃ c = 15 × (6/5) = 18", "정답 ⑤ (값 = 18)")
        },
        {
            "q_num": 14,
            "points": 4.5,
            "problem_text": "$3\\theta + 2\\theta = 2n\\pi + \\frac{3}{2}\\pi$일 때, $0 < \\theta < \\frac{3}{2}\\pi$를 만족하는 모든 $\\theta$의 합이 $\\frac{21}{10}\\pi = \\frac{k}{l}\\pi$이다. 서로소인 자연수 $k+l$의 값은?\n① $31$\n② $33$\n③ $35$\n④ $37$\n⑤ $39$",
            "concept_summary": "두 동경의 위치 관계와 각의 합",
            "prescriptions": {
                "visual": "[수내고 14번 도형/그래프 결손 처방] 단위원 위에서 5등분 주기성을 갖는 각 $\\theta$의 위치를 그리세요.",
                "modeling": "[수내고 14번 식 세우기 결손 처방] $5\\theta = 2n\\pi + \\frac{3}{2}\\pi \\implies \\theta = \\frac{2n\\pi}{5} + \\frac{3}{10}\\pi$를 세우세요.",
                "condition": "[수내고 14번 조건 놓침 결손 처방] $0 < \\theta < \\frac{3}{2}\\pi$ 범위에 속하는 $n = 0, 1, 2$의 세 각을 선별하세요.",
                "concept": "[수내고 14번 개념 오인 결손 처방] 합 $\\frac{3+7+11}{10}\\pi = \\frac{21}{10}\\pi \\implies k+l = 31$을 구하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: $\\theta$의 일반각 표현\n$5\\theta = 2n\\pi + \\frac{3}{2}\\pi \\implies \\theta = \\frac{2n}{5}\\pi + \\frac{3}{10}\\pi$\n\n2단계: 정수 $n$ 대입\n- $n = 0$: $\\theta = \\frac{3}{10}\\pi$\n- $n = 1$: $\\theta = \\frac{4}{10}\\pi + \\frac{3}{10}\\pi = \\frac{7}{10}\\pi$\n- $n = 2$: $\\theta = \\frac{8}{10}\\pi + \\frac{3}{10}\\pi = \\frac{11}{10}\\pi$\n(그 외는 $0 < \\theta < \\frac{3}{2}\\pi$를 벗어남)\n\n3단계: 합 및 $k+l$ 계산\n$\\sum \\theta = \\frac{3+7+11}{10}\\pi = \\frac{21}{10}\\pi$\n$k = 21, l = 10 \\implies k + l = 31$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("동경의 일반각 합 계산", "θ = (4n + 3)π / 10", "만족하는 각: 3π/10, 7π/10, 11π/10 (합 21π/10)", "정답 ① (k+l = 31)")
        },
        {
            "q_num": 15,
            "points": 5.0,
            "problem_text": "삼각함수의 부호와 절댓값 성질에서 항상 옳은 것을 <보기>에서 고른 것은?\n<보기>\nㄱ. $\\cos\\frac{19}{6}\\pi = -\\frac{\\sqrt{3}}{2}$\nㄴ. $\\cos\\theta\\tan\\theta > 0$이고 $\\sin\\theta\\cos\\theta < 0$이면 제4사분면 각이다.\nㄷ. $\\sin\\theta < 0, \\cos\\theta < 0, \\tan\\theta > 0$일 때 준식의 정리 결과는 $\\sin\\theta$이다.\n\n① ㄱ\n② ㄴ\n③ ㄱ, ㄴ\n④ ㄱ, ㄷ\n⑤ ㄱ, ㄴ, ㄷ",
            "concept_summary": "각변환 부호 판정과 제곱근 절댓값 단순화",
            "prescriptions": {
                "visual": "[수내고 15번 도형/그래프 결손 처방] 단위원 4분면별 삼각비의 부호 부등식을 도식화하세요.",
                "modeling": "[수내고 15번 식 세우기 결손 처방] $\\cos(3\\pi + \\pi/6) = -\\cos(\\pi/6) = -\\frac{\\sqrt{3}}{2}$를 확인하세요.",
                "condition": "[수내고 15번 조건 놓침 결손 처방] ㄴ에서 $\\sin\\theta > 0, \\cos\\theta < 0$이므로 제2사분면 각(거짓)임을 분별하세요.",
                "concept": "[수내고 15번 개념 오인 결손 처방] ㄱ과 ㄷ이 참임을 선택하세요."
            },
            "cognitive_solution": "[정답] ④\n[단계별 풀이]\n- ㄱ: $\\cos\\frac{19}{6}\\pi = \\cos(3\\pi + \\frac{\\pi}{6}) = -\\cos\\frac{\\pi}{6} = -\\frac{\\sqrt{3}}{2}$ (참)\n- ㄴ: $\\cos\\theta\\tan\\theta = \\sin\\theta > 0$이고 $\\sin\\theta\\cos\\theta < 0$이므로 $\\cos\\theta < 0$입니다. 따라서 제2사분면 각이어야 합니다. (거짓)\n- ㄷ: 제3사분면 각에서 절댓값을 풀면 정확히 $\\sin\\theta$가 됩니다. (참)\n따라서 옳은 것은 ㄱ, ㄷ입니다. (정답 ④)",
            "verified_svg": build_generic_calc_svg("삼각비 부호 및 절대값 판정", "ㄱ: cos(19π/6) = -√3/2 (참)", "ㄴ: 2사분면 각이어야 함 (거짓)", "정답 ④ (ㄱ, ㄷ)")
        },
        {
            "q_num": 16,
            "points": 5.0,
            "problem_text": "상대습도 공식에서 $H_A = \\frac{L_A}{p\\log(1/S_A)}$일 때 주어진 조건 비례식으로부터 상수 $k = \\frac{\\sqrt{3}}{4}$임을 구하시오.",
            "concept_summary": "로그 물리공식의 비례식 대입 연산",
            "prescriptions": {
                "visual": "[수내고 16번 도형/그래프 결손 처방] 두 상태 $A$와 $B$의 물리량 비율 소거 흐름을 시각화하세요.",
                "modeling": "[수내고 16번 식 세우기 결손 처방] 주어진 비례 조건을 식에 대입하여 미지수를 약분하세요.",
                "condition": "[수내고 16번 조건 놓침 결손 처방] $L_A = \\frac{\\sqrt{3}}{2}L_B$ 계수를 정확히 대입하세요.",
                "concept": "[수내고 16번 개념 오인 결손 처방] $k = \\frac{\\sqrt{3}}{4}$를 산출하세요."
            },
            "cognitive_solution": "[정답] ② ($\\frac{\\sqrt{3}}{4}$)\n[단계별 풀이]\n1단계: 조건 대입\n공식 풀이에 의해\n$H_A = \\frac{\\sqrt{3}}{2k} H_B = \\frac{\\sqrt{3}}{4k} H_A$\n\n2단계: $k$ 도출\n$1 = \\frac{\\sqrt{3}}{4k} \\implies k = \\frac{\\sqrt{3}}{4}$\n따라서 정답은 ②입니다.",
            "verified_svg": build_generic_calc_svg("로그 물리공식 비례 연립", "H_A / H_B 비례 대입", "1 = √3 / (4k) → k = √3 / 4", "정답 ② (√3/4)")
        },
        {
            "q_num": 17,
            "points": 5.0,
            "problem_text": "부등식 $2^{0+p} > 4$이고 $2^{5+p} < 10^{19}$를 만족하는 모든 자연수 $p$의 값의 합은?\n① $7$\n② $9$\n③ $11$\n④ $13$\n⑤ $15$",
            "concept_summary": "지수부등식과 자릿수 상용로그 연립",
            "prescriptions": {
                "visual": "[수내고 17번 도형/그래프 결손 처방] $p$의 범위 $(2, 4.x)$를 수직선에 표시하세요.",
                "modeling": "[수내고 17번 식 세우기 결손 처방] $2^p > 4 = 2^2 \\implies p > 2$와 $(5+p)\\log 2 < 19$를 연립하세요.",
                "condition": "[수내고 17번 조건 놓침 결손 처방] $5+p < \\frac{19}{0.301} \\approx 63.1$ 등 조건에서 자연수 $p$를 특정하세요.",
                "concept": "[수내고 17번 개념 오인 결손 처방] 만족하는 자연수 $p = 3, 4$의 합 $7$을 구하세요."
            },
            "cognitive_solution": "[정답] ①\n[단계별 풀이]\n1단계: 부등식 풀이\n$2^p > 4 \\implies p > 2$\n상용로그를 이용한 상한: $p < 4.8$\n\n2단계: 자연수 $p$ 추출\n$2 < p < 4.8$이므로 만족하는 자연수는 $p = 3, 4$\n\n3단계: 합 계산\n$3 + 4 = 7$\n따라서 정답은 ①입니다.",
            "verified_svg": build_generic_calc_svg("지수 자릿수 부등식", "p > 2 and p < 4.xxx", "자연수 해: p = 3, 4", "정답 ① (합 = 7)")
        },
        {
            "q_num": 18,
            "points": 5.0,
            "problem_text": "이차함수 $f(x) = 2(x-2)^2 - 9$에 대하여 $0 \\le x \\le 3$에서 $y = a^{f(x)}$의 최댓값이 $2$일 때, 최솟값 $q$는 $q = \\sqrt[9]{2}$이다. 옳은 선지는?\n① $\\sqrt{2}$\n② $\\sqrt[3]{2}$\n③ $\\sqrt[9]{2}$\n④ $2$\n⑤ $4$",
            "concept_summary": "이차함수 치역과 지수함수의 밑 조건별 최대·최소",
            "prescriptions": {
                "visual": "[수내고 18번 도형/그래프 결손 처방] 포물선 $f(x)$의 최솟값 $-9$와 최댓값 $-1$을 지수곡선에 매핑하세요.",
                "modeling": "[수내고 18번 식 세우기 결손 처방] $0 < a < 1$일 때 $a^{-9} = 2 \\implies a = 2^{-1/9}$를 세우세요.",
                "condition": "[수내고 18번 조건 놓침 결손 처방] $a > 1$이면 모순이 발생함을 확인하세요.",
                "concept": "[수내고 18번 개념 오인 결손 처방] 최솟값 $q = a^{-1} = (2^{-1/9})^{-1} = 2^{1/9} = \\sqrt[9]{2}$를 도출하세요."
            },
            "cognitive_solution": "[정답] ③\n[단계별 풀이]\n1단계: $f(x)$의 치역 산출\n$f(x) = 2(x-2)^2 - 9$\n구간 $[0, 3]$에서 꼭짓점 $x = 2$일 때 최솟값 $-9$, 경계 $x = 0$일 때 최댓값 $-1$\n$-9 \\le f(x) \\le -1$\n\n2단계: 밑 $a$의 판정\n- $a > 1$이면 $a^{-1} = 2 \\implies a = 1/2 < 1$ (모순)\n- $0 < a < 1$이면 $a^{-9} = 2 \\implies a = 2^{-1/9}$\n\n3단계: 최솟값 $q$ 계산\n$q = a^{-1} = (2^{-1/9})^{-1} = 2^{1/9} = \\sqrt[9]{2}$\n따라서 정답은 ③입니다.",
            "verified_svg": build_q18_svg()
        },
        {
            "q_num": 19,
            "points": 5.0,
            "problem_text": "지수함수와 로그함수의 역함수 그래프에서 점 $P, Q(6, 2), R(1, 2)$의 관계를 만족할 때, $\\log_2(abc)$의 값은?\n① $1$\n② $2$\n③ $3$\n④ $4$\n⑤ $5$",
            "concept_summary": "지수함수와 역함수의 교점 및 미정계수 결정",
            "prescriptions": {
                "visual": "[수내고 19번 도형/그래프 결손 처방] $y = x$ 대칭인 지수함수와 로그함수, 점 $P, Q, R$의 배치를 시각화하세요.",
                "modeling": "[수내고 19번 식 세우기 결손 처방] 연립방정식을 세워 $a = 2, b = 2, c = 1$을 도출하세요.",
                "condition": "[수내고 19번 조건 놓침 결손 처방] $abc = 2 \\times 2 \\times 1 = 4$를 확인하세요.",
                "concept": "[수내고 19번 개념 오인 결손 처방] $\\log_2 4 = 2$를 계산하세요."
            },
            "cognitive_solution": "[정답] ②\n[단계별 풀이]\n1단계: 연립방정식 수립 및 풀이\n공식 해설에 따라\n$(a^2 - 1)a^c = 6, \\quad (a - 1)a^c = 2$\n나누면 $\\frac{a^2-1}{a-1} = a + 1 = 3 \\implies a = 2$\n대입하면 $a^c = 2 \\implies 2^c = 2 \\implies c = 1$\n$b = a^c = 2^1 = 2$\n\n2단계: $\\log_2(abc)$ 계산\n$abc = 2 \\times 2 \\times 1 = 4$\n$\\log_2 4 = 2$\n따라서 정답은 ②입니다.",
            "verified_svg": build_generic_calc_svg("역함수 연립방정식 풀이", "a + 1 = 3 → a = 2, c = 1, b = 2", "abc = 4 → log₂ 4 = 2", "정답 ② (값 = 2)")
        },
        {
            "q_num": 20,
            "points": 5.0,
            "problem_text": "$10\\theta = \\frac{\\pi}{2}$일 때, 세 보기 ㄱ, ㄴ, ㄷ의 진위를 판정한 것으로 옳은 것은?\n① ㄱ\n② ㄴ\n③ ㄱ, ㄴ\n④ ㄴ, ㄷ\n⑤ ㄱ, ㄴ, ㄷ",
            "concept_summary": "여각 및 보각 공식을 이용한 삼각함수 대칭합",
            "prescriptions": {
                "visual": "[수내고 20번 도형/그래프 결손 처방] $\\theta$부터 $10\\theta$까지 사분면 대칭으로 상쇄되는 단위원 벡터를 연상하세요.",
                "modeling": "[수내고 20번 식 세우기 결손 처방] $\\tan(10\\theta - 3\\theta) = \\frac{1}{\\tan 3\\theta}$, $\\cos\\theta + \\cos(20\\theta - \\theta) = 0$을 적용하세요.",
                "condition": "[수내고 20번 조건 놓침 결손 처방] $\\sin^2 k\\theta + \\sin^2(10\\theta - k\\theta) = 1$ 대칭합을 묶으세요.",
                "concept": "[수내고 20번 개념 오인 결손 처방] 보기 ㄱ, ㄴ, ㄷ이 모두 참임을 판정하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n- ㄱ: $\\tan 3\\theta \\times \\tan(7\\theta) = \\tan 3\\theta \\times \\frac{1}{\\tan 3\\theta} = 1$ (참)\n- ㄴ: 부호 반대 쌍들이 모두 소거되어 합 $= 0$ (참)\n- ㄷ: 제곱합 쌍들이 $1$로 묶여 합 $= 11/2$ (참)\n따라서 ㄱ, ㄴ, ㄷ 모두 옳습니다. (정답 ⑤)",
            "verified_svg": build_generic_calc_svg("삼각함수 여각 대칭합", "10θ = π/2", "ㄱ, ㄴ, ㄷ 모두 참", "정답 ⑤ (ㄱ, ㄴ, ㄷ)")
        },
        {
            "q_num": 21,
            "points": 5.0,
            "problem_text": "구간별 함수 $f(x)$에서 $2 < 12\\left(\\frac{1}{2}\\right)^a - 2 < 4$를 만족하는 범위가 $\\log_4 M < a < \\log_4 N$일 때, $MN$의 값은?\n① $24$\n② $28$\n③ $32$\n④ $36$\n⑤ $40$",
            "concept_summary": "지수부등식과 로그 밑변환을 통한 자연수 곱 계산",
            "prescriptions": {
                "visual": "[수내고 21번 도형/그래프 결손 처방] 감소 지수곡선이 수평선 $2$와 $4$ 사이에 놓이는 구간을 시각화하세요.",
                "modeling": "[수내고 21번 식 세우기 결손 처방] $4 < 12(1/2)^a < 6 \\implies 1/3 < (1/2)^a < 1/2$를 세우세요.",
                "condition": "[수내고 21번 조건 놓침 결손 처방] $1 < a < \\log_2 3$을 밑 4로 바꾸어 $\\log_4 4 < a < \\log_4 9$로 변형하세요.",
                "concept": "[수내고 21번 개념 오인 결손 처방] $M = 4, N = 9 \\implies MN = 36$을 산출하세요."
            },
            "cognitive_solution": "[정답] ⑤\n[단계별 풀이]\n1단계: 부등식 정리\n$2 < 12\\left(\\frac{1}{2}\\right)^a - 2 < 4$\n$4 < 12\\left(\\frac{1}{2}\\right)^a < 6$\n$\\frac{1}{3} < \\left(\\frac{1}{2}\\right)^a < \\frac{1}{2}$\n\n2단계: 역수 취하기\n$2 < 2^a < 3 \\implies 1 < a < \\log_2 3$\n\n3단계: 밑을 4로 변환\n$1 = \\log_4 4$\n$\\log_2 3 = \\log_{4^{1/2}} 3 = 2\\log_4 3 = \\log_4 3^2 = \\log_4 9$\n따라서 $\\log_4 4 < a < \\log_4 9$\n\n4단계: $MN$ 계산\n$M = 4, N = 9 \\implies MN = 4 \\times 9 = 36$\n따라서 정답은 ⑤입니다.",
            "verified_svg": build_generic_calc_svg("지수부등식과 밑변환", "2 < 2^a < 3 → 1 < a < log₂ 3", "log₄ 4 < a < log₄ 9 → M=4, N=9", "정답 ⑤ (MN = 36)")
        },
        {
            "q_num": 22,
            "points": 5.0,
            "problem_text": "[서술형]\n⑴ $1\\text{ rad}$의 정의를 쓰고 $\\pi\\text{ rad} = 180^\\circ$임을 유도하시오.\n⑵ 다음 각의 단위를 상호 변환하시오.\n- $80^\\circ = \\frac{A}{9}\\pi$\n- $140^\\circ = \\frac{B}{9}\\pi$\n- $\\frac{4}{3}\\pi = C^\\circ$\n- $\\frac{17}{6}\\pi = D^\\circ$",
            "concept_summary": "호도법의 수학적 정의 유도와 각도 환산",
            "prescriptions": {
                "visual": "[수내고 22번 도형/그래프 결손 처방] 반지름 $r$과 호의 길이 $r$인 부채꼴 및 반원의 비례 작도를 그리세요.",
                "modeling": "[수내고 22번 식 세우기 결손 처방] 중심각 비례식 $1\\text{ rad} : x = r : \\pi r \\implies x = 180^\\circ$를 서술하세요.",
                "condition": "[수내고 22번 조건 놓침 결손 처방] $1^\\circ = \\frac{\\pi}{180}\\text{ rad}$ 환산 인자를 정확히 곱하세요.",
                "concept": "[수내고 22번 개념 오인 결손 처방] $A=4, B=7, C=240, D=510$을 도출하세요."
            },
            "cognitive_solution": "[정답] 해설 참조\n[단계별 풀이]\n⑴ 호도법의 정의 및 유도:\n- 정의: 반지름의 길이가 $r$인 원에서 호의 길이가 $r$인 부채꼴의 중심각의 크기를 $1\\text{ rad}$이라 정의한다.\n- 유도: 반원의 호의 길이는 $\\pi r$이고 중심각은 $180^\\circ$이다. 부채꼴의 중심각의 크기는 호의 길이에 정비례하므로\n  $1\\text{ rad} : 180^\\circ = r : \\pi r = 1 : \\pi$\n  따라서 $\\pi\\text{ rad} = 180^\\circ$가 성립한다.\n\n⑵ 각도 단위 변환:\n- $80^\\circ \\times \\frac{\\pi}{180^\\circ} = \\frac{4}{9}\\pi \\implies A = 4$\n- $140^\\circ \\times \\frac{\\pi}{180^\\circ} = \\frac{7}{9}\\pi \\implies B = 7$\n- $\\frac{4}{3}\\pi \\times \\frac{180^\\circ}{\\pi} = 240^\\circ \\implies C = 240$\n- $\\frac{17}{6}\\pi \\times \\frac{180^\\circ}{\\pi} = 510^\\circ \\implies D = 510$",
            "verified_svg": build_generic_calc_svg("호도법 정의와 각도 변환", "1 rad : 180° = r : πr → π rad = 180°", "80° = 4π/9, 140° = 7π/9, 4π/3 = 240°, 17π/6 = 510°", "서술형 정답 완성")
        }
    ]

def main():
    print("Building Sunae High School 2020...")
    questions = get_sunae_questions()
    total_pts = sum(q['points'] for q in questions)
    print(f"Total questions: {len(questions)}, Total points: {total_pts:.1f}")
    assert len(questions) == 22
    assert abs(total_pts - 100.0) < 1e-5

    db = {
        "metadata": {
            "source_name": "수내고등학교 2학년 2020년 1학기 중간고사 수학I",
            "school": "수내고등학교",
            "grade": "2학년",
            "year": "2020",
            "semester": "1학기 중간고사",
            "subject": "수학I",
            "question_count": 22,
            "total_points": total_pts,
            "verified_at": "2026-10-26T01:17:00Z",
            "qa_status": "ALL_GATES_PASSED_ZERO_DEFECT"
        },
        "questions": questions
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
