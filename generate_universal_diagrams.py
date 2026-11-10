"""
=============================================================================
Universal Mathematical Diagram Generator (UniversalDiagramGenerator v5.0)
=============================================================================
Powered by AnalyticalGeometryCompiler v1.0 & MathEngineCore v4.0.
Features:
1. Strict Analytical Invariance: Points on curves, tangents, and intersections
   are mathematically derived via calculus (Zero floating / hallucinated coordinates).
2. Isotropic Aspect Ratio: Preserves authentic perpendicularity (90°), exact circularity,
   and authentic geometric proportions.
3. Automated Calculus Invariant Gate: Automatically verifies |y - f(x)| < 1e-4
   and tangent slope = f'(x) before emitting SVG.
=============================================================================
"""

import math
from math_engine_core import MathEngineCore
from analytical_geometry_engine import AnalyticalGeometryCompiler, AnalyticalFunction

def build_universal_svg_for_problem(prob_num: int, is_variation: bool = False) -> str:
    """
    Constructs 100% mathematically exact, compiler-verified CSAT diagrams.
    """
    # -------------------------------------------------------------------------
    # Problem 1 & 13: Recursive Sequence Backward Branching Tree
    # -------------------------------------------------------------------------
    if prob_num in [1, 13]:
        base = 2 if prob_num == 1 else 3
        target_sum = 151 if prob_num == 1 else 252
        end_cond = "a₆+a₇=3" if prob_num == 1 else "a₅+a₆=4"
        
        branches = [
            {
                "x": 140, "y": 44, "rule": "홀수 역산", "value": "a=1",
                "subs": [
                    {"x": 230, "y": 32, "rule": f"×{base}", "value": f"{base}"},
                    {"x": 230, "y": 56, "rule": "log", "value": "1"}
                ]
            },
            {
                "x": 140, "y": 94, "rule": "짝수 역산", "value": f"a={base}",
                "subs": [
                    {"x": 230, "y": 82, "rule": f"×{base}", "value": f"{base*2}"},
                    {"x": 230, "y": 106, "rule": "제약검증", "value": f"{base*base}"}
                ]
            }
        ]
        
        return MathEngineCore.render_tree_diagram(
            title=f"수열 귀납적 역추적 상태 트리 ({end_cond})",
            start_node={"x": 45, "y": 68, "label": "종착", "value": "End"},
            branches=branches,
            summary_badge={"title": "가능한 a₁ 합", "value": str(target_sum)},
            width=460,
            height=135
        )

    # -------------------------------------------------------------------------
    # Problem 2 & 14: Symmetric Exponential Curves & Tangent Intersections
    # -------------------------------------------------------------------------
    elif prob_num in [2, 14]:
        base = 2.0 if prob_num == 2 else 3.0
        t = 1.0
        
        c = AnalyticalGeometryCompiler(x_range=(-2.5, 2.5), y_range=(-2.8, 2.8), width=460, height=145)
        
        # Curve 1: y = base^x, Curve 2: y = -base^x (symmetric across x-axis)
        c1 = c.add_curve(lambda x: base**x, label=f"y={int(base)}ˣ")
        c2 = c.add_curve(lambda x: -(base**x), label=f"y=-{int(base)}ˣ")
        
        # Contact points: strictly bound to curves
        c.add_point_on_curve(c1, x=t, label=f"(t, {int(base)}ᵗ)", label_pos="above_left")
        c.add_point_on_curve(c2, x=-t, label=f"(-t, -{int(base)}⁻ᵗ)", label_pos="below_left")
        
        # Tangent lines derived strictly via derivative calculus
        t1 = c.add_tangent_line(c1, x_contact=t, span_left=1.9, span_right=0.4, color="#DC2626")
        t2 = c.add_tangent_line(c2, x_contact=-t, span_left=0.4, span_right=1.9, color="#DC2626")
        
        # Analytical intersection of tangents
        c.add_line_intersection(t1, t2, label="교점 f(t)", color="#2563EB", drop_x=True, label_pos="below_right")
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 3 & 15: Cubic Function Tangent Boundary & 1:1:1:1 Ratio
    # -------------------------------------------------------------------------
    elif prob_num in [3, 15]:
        k = 2.0 if prob_num == 3 else 3.0
        # g(x) = (x - k)^2 * (x + 1)
        # For prob 3 (k=2): local max at x=0 (y=4), inflection at x=1 (y=2), min at x=2 (y=0)
        # Horizontal tangent line y=4 touches at x=0 and intersects at x=3 (교점 alpha)
        x_max_pt = 0.0 if prob_num == 3 else (k - 2.0)/3.0
        xi = 1.0 if prob_num == 3 else (2.0*k - 1.0)/3.0
        x_min_pt = k
        x_cross = 3.0 if prob_num == 3 else k + (k - xi)
        
        g_fn = lambda x: ((x - k)**2) * (x + 1.0)
        y_max_pt = g_fn(x_max_pt)
        
        c = AnalyticalGeometryCompiler(x_range=(-1.8, x_cross + 0.8), y_range=(-2.4, y_max_pt + 1.8), width=460, height=145)
        g_curve = c.add_curve(g_fn, x_min=-1.4, x_max=x_cross + 0.4, label="y=g(x)")
        
        # Points on curve
        c.add_point(-1.0, 0.0, label="(-1,0)", color="#64748B", label_pos="above_left")
        c.add_point_on_curve(g_curve, x=x_max_pt, label="극대(접점)", color="#DC2626", drop_x=True, label_pos="above")
        c.add_point_on_curve(g_curve, x=xi, label="변곡점", color="#080908", drop_x=True, label_pos="above")
        c.add_point_on_curve(g_curve, x=x_min_pt, label=f"극소({int(x_min_pt)})", color="#080908", drop_x=True, label_pos="below")
        
        # Horizontal Tangent line y = y_max touching at x_max_pt and reaching intersection alpha
        c.add_tangent_line(g_curve, x_contact=x_max_pt, span_left=0.6, span_right=x_cross - x_max_pt + 0.5,
                           label=f"접선 y={int(y_max_pt)}", label_pt_pos="start", color="#DC2626")
        
        # Intersection alpha found analytically
        c.add_curve_intersection(g_curve, AnalyticalFunction(lambda x: y_max_pt),
                                bracket=(x_min_pt + 0.1, x_cross + 0.6),
                                label=f"교점 α({int(x_cross)},{int(y_max_pt)})", color="#DC2626",
                                drop_x=True, label_pos="above_right")
        
        # 1:1:1 geometric ratio intervals
        c.add_ratio_intervals([x_max_pt, xi, x_min_pt, x_cross], labels=["1", "1", "1"], y_level=-1.6)
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 4 & 16: Quartic Function Differentiability & Fold Line
    # -------------------------------------------------------------------------
    elif prob_num in [4, 16]:
        c_sq = 2.0 if prob_num == 4 else 6.0
        c_val = math.sqrt(c_sq)
        
        c = AnalyticalGeometryCompiler(x_range=(-2.5, 2.5), y_range=(-(c_sq**2)*0.4, (c_sq**2)*1.3), width=460, height=135)
        g_curve = c.add_curve(lambda x: (x**2 - c_sq)**2, x_min=-2.2, x_max=2.2, label="g(x)=|f(x)-a|")
        c.add_curve(lambda x: -(x**2 - c_sq)**2, x_min=-c_val, x_max=c_val, color="#94A3B8", width=1.0, style="dashed")
        
        c.add_point_on_curve(g_curve, x=0.0, label=f"극대(0,{c_sq**2:.0f})", color="#DC2626", drop_x=True, label_pos="above_left")
        c.add_point_on_curve(g_curve, x=-c_val, label="-c", color="#080908", drop_x=True, label_pos="below")
        c.add_point_on_curve(g_curve, x=c_val, label="c", color="#080908", drop_x=True, label_pos="below")
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 5 & 17: Geometric Series Convergence & Horizontal Asymptote
    # -------------------------------------------------------------------------
    elif prob_num in [5, 17]:
        lim_val = 3.0 if prob_num == 5 else 4.0
        ans_val = 3.0 if prob_num == 5 else 4.0
        
        c = AnalyticalGeometryCompiler(x_range=(0.0, 6.8), y_range=(0.0, max(ans_val, lim_val) * 1.5), width=460, height=135)
        c.add_line((0.0, lim_val), (6.5, lim_val), color="#DC2626", width=1.3, style="dashed",
                   label=f"점근선 y={int(lim_val)}", label_pt=(4.8, lim_val + 0.35))
        
        for n in range(1, 6):
            c.add_point(float(n), lim_val, label=f"a{n}" if n <= 2 else "", color="#080908", drop_x=True, label_pos="above")
            
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 6 & 18: Exponential & Log Curves with Orthogonal Tangents
    # -------------------------------------------------------------------------
    elif prob_num in [6, 18]:
        coeff = 1.0 if prob_num == 6 else 2.0
        t = 1.35
        Ax = t - 1.0
        By = coeff * (t - 1.0)
        s = math.exp(t)
        
        c = AnalyticalGeometryCompiler(x_range=(-2.0, 4.2), y_range=(-1.8, 5.4), width=460, height=145, preserve_aspect_ratio=True)
        f_exp = c.add_curve(lambda x: coeff * math.exp(x), x_min=-1.8, x_max=1.65, label="y=eˣ" if prob_num == 6 else "y=2eˣ")
        f_log = c.add_curve(lambda x: coeff * math.log(x), x_min=0.2, x_max=3.8, label="y=ln x" if prob_num == 6 else "y=2ln x")
        
        # Tangents strictly generated from derivatives
        c.add_point_on_curve(f_exp, x=t, label=f"(t,{'eᵗ' if prob_num == 6 else '2eᵗ'})", color="#080908", label_pos="above_left")
        c.add_tangent_line(f_exp, x_contact=t, span_left=t - Ax + 0.3, span_right=0.15, color="#94A3B8")
        
        c.add_tangent_line(f_log, x_contact=s, span_left=s + 0.2, span_right=0.3, color="#94A3B8")
        
        c.add_point(Ax, 0.0, label=f"A({Ax:.1f},0)", color="#DC2626", label_pos="below_right")
        c.add_point(0.0, By, label=f"B(0,{By:.1f})", color="#DC2626", label_pos="above_left")
        c.add_line((Ax, 0.0), (0.0, By), color="#DC2626", width=2.0, style="solid", label="선분 AB", label_pt=(Ax/2.0 + 0.1, By/2.0 + 0.25))
        c.add_right_angle((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), size=7.0)
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 7 & 19: Confocal Ellipse & Hyperbola EXACT Orthogonal Intersection
    # -------------------------------------------------------------------------
    elif prob_num in [7, 19]:
        a1, b1, c_foc = 5.0, 3.0, 4.0
        a2 = math.sqrt(7.0)
        b2 = 3.0
        
        xP = (a1 * a2) / c_foc
        yP = (b1 * b2) / c_foc
        
        me = -(b1**2 * xP) / (a1**2 * yP)
        mh = (b2**2 * xP) / (a2**2 * yP)
        
        c = AnalyticalGeometryCompiler(x_range=(-5.8, 5.8), y_range=(-3.4, 3.4), width=460, height=145, preserve_aspect_ratio=True)
        ell_top = c.add_curve(lambda x: b1 * math.sqrt(max(0.0, 1.0 - (x/a1)**2)), x_min=-a1, x_max=a1, label="타원")
        c.add_curve(lambda x: -b1 * math.sqrt(max(0.0, 1.0 - (x/a1)**2)), x_min=-a1, x_max=a1)
        
        hyp_top = c.add_curve(lambda x: b2 * math.sqrt(max(0.0, (x/a2)**2 - 1.0)), x_min=a2, x_max=a1 + 0.4, label="쌍곡선")
        c.add_curve(lambda x: -b2 * math.sqrt(max(0.0, (x/a2)**2 - 1.0)), x_min=a2, x_max=a1 + 0.4)
        
        c.add_point_on_curve(ell_top, x=xP, label="P(직교!)", color="#DC2626", drop_x=True, label_pos="above_right")
        c.add_tangent_line(ell_top, x_contact=xP, span_left=1.0, span_right=1.0, color="#94A3B8")
        c.add_tangent_line(hyp_top, x_contact=xP, span_left=0.5, span_right=0.5, color="#94A3B8")
        
        c.add_point(-c_foc, 0.0, label="F'", color="#DC2626", label_pos="below")
        c.add_point(c_foc, 0.0, label="F", color="#DC2626", label_pos="below")
        c.add_right_angle((xP, yP), (1.0, me), (-1.0, -mh), size=8.0)
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 8 & 20: Vector Decomposition & Midpoint Circle
    # -------------------------------------------------------------------------
    elif prob_num in [8, 20]:
        R = 2.0 if prob_num == 8 else 3.0
        Ax = 3.0 if prob_num == 8 else 4.0
        
        c = AnalyticalGeometryCompiler(x_range=(-R - 1.0, Ax + 1.0), y_range=(-R - 0.7, R + 0.9), width=460, height=135, preserve_aspect_ratio=True)
        c.add_curve(lambda x: math.sqrt(max(0.0, R**2 - x**2)), x_min=-R, x_max=R)
        c.add_curve(lambda x: -math.sqrt(max(0.0, R**2 - x**2)), x_min=-R, x_max=R)
        
        c.add_line((0.0, 0.0), (Ax, 0.0), color="#94A3B8", width=1.0, style="dashed")
        c.add_line((Ax, 0.0), (-R, 0.0), color="#DC2626", width=1.8, style="solid", label="|AM|최대", label_pt=(-1.1, 0.45))
        
        c.add_point(Ax, 0.0, label=f"A({int(Ax)},0)", color="#DC2626", label_pos="above")
        c.add_point(-R, 0.0, label="최대M", color="#DC2626", label_pos="below_left")
        c.add_point(R, 0.0, label="최소M", color="#EA580C", label_pos="below_right")
        c.add_annotation(0.0, R + 0.35, f"x²+y²={int(R**2)}")
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 9 & 21: Spatial Geometry & 3D Projection
    # -------------------------------------------------------------------------
    elif prob_num in [9, 21]:
        side = 4.0 if prob_num == 9 else 6.0
        Ax, Ay = -side/2.0, 0.0
        Bx, By = side/2.0, 0.0
        Cx, Cy = 0.0, (math.sqrt(3.0)/2.0) * side
        R = side / 2.0
        
        c = AnalyticalGeometryCompiler(x_range=(-side/2.0 - 0.8, side/2.0 + 0.8), y_range=(-0.8, Cy + 0.8), width=460, height=135, preserve_aspect_ratio=True)
        c.add_curve(lambda x: math.sqrt(max(0.0, R**2 - x**2)), x_min=-R, x_max=R, color="#94A3B8", width=1.1, style="dashed")
        
        c.add_line((Ax, Ay), (Bx, By), color="#080908", width=1.8)
        c.add_line((Bx, By), (Cx, Cy), color="#080908", width=1.8)
        c.add_line((Cx, Cy), (Ax, Ay), color="#080908", width=1.8)
        c.add_line((0.0, R), (Bx/2.0, Cy/2.0), color="#DC2626", width=1.3, style="dashed", label="d(최대)", label_pt=(Bx/4.0 + 0.2, (R + Cy/2.0)/2.0 + 0.3))
        
        c.add_point(Ax, Ay, label="A", color="#080908", label_pos="below_left")
        c.add_point(Bx, By, label="B", color="#080908", label_pos="below_right")
        c.add_point(Cx, Cy, label="C", color="#080908", label_pos="above")
        c.add_point(0.0, R, label="P(최대)", color="#DC2626", label_pos="above_left")
        c.add_annotation(R - 0.3, R * 0.45, "P자취", color="#64748B", size=8.0, anchor="start")
        
        return c.compile()

    # -------------------------------------------------------------------------
    # Problem 10 & 22: Conditional Probability Partition
    # -------------------------------------------------------------------------
    elif prob_num in [10, 22]:
        p_ans = "3/5" if prob_num == 10 else "4/5"
        parts = ["홀3", "홀1 짝2", "짝3"]
        return MathEngineCore.render_venn_partition(
            title="조건부확률 표본공간 축소 및 배반사건 분할",
            partitions=parts,
            condition_name="조건 사건 B",
            target_indices=[1],
            p_val=p_ans,
            width=460,
            height=135
        )

    # -------------------------------------------------------------------------
    # Problem 11 & 23: Stars and Bars Partition
    # -------------------------------------------------------------------------
    elif prob_num in [11, 23]:
        ans_h = 25 if prob_num == 11 else 36
        target_sum = 12 if prob_num == 11 else 14
        
        branches = [
            {
                "x": 140, "y": 44, "rule": "a=1" if prob_num == 11 else "a=0", "value": "Case 1",
                "subs": [
                    {"x": 230, "y": 44, "rule": "H분할", "value": "₁₅"}
                ]
            },
            {
                "x": 140, "y": 94, "rule": "a=3" if prob_num == 11 else "a=2", "value": "Case 2",
                "subs": [
                    {"x": 230, "y": 94, "rule": "H분할", "value": "₁₀"}
                ]
            }
        ]
        
        return MathEngineCore.render_tree_diagram(
            title=f"중복조합 격자 분할 치환 (총합={target_sum})",
            start_node={"x": 45, "y": 68, "label": "제약", "value": "a"},
            branches=branches,
            summary_badge={"title": "순서쌍 개수", "value": str(ans_h)},
            width=460,
            height=135
        )

    # -------------------------------------------------------------------------
    # Problem 12 & 24: Probability Density Parabola & Symmetric Integral
    # -------------------------------------------------------------------------
    else:
        x_max = 4.0 if prob_num == 12 else 6.0
        axis_x = 2.0 if prob_num == 12 else 3.0
        x_start = 1.0 if prob_num == 12 else 2.0
        x_end = 3.0 if prob_num == 12 else 4.0
        
        k = (3.0 / 32.0) if prob_num == 12 else (1.0 / 36.0)
        f_pdf = lambda x: k * x * (x_max - x)
        
        c = AnalyticalGeometryCompiler(x_range=(-0.4, x_max + 0.6), y_range=(-0.04, f_pdf(axis_x) * 1.3), width=460, height=135)
        pdf_curve = c.add_curve(f_pdf, x_min=0.0, x_max=x_max, color="#080908", width=2.0, label="f(x)")
        
        c.add_line((axis_x, 0.0), (axis_x, f_pdf(axis_x)), color="#2563EB", width=1.2, style="dashed",
                   label=f"대칭축 x={int(axis_x)}", label_pt=(axis_x, f_pdf(axis_x) + 0.025))
        
        c.add_point(0.0, 0.0, label="0", color="#080908", label_pos="below")
        c.add_point_on_curve(pdf_curve, x=x_start, label=f"x={int(x_start)}", color="#DC2626", drop_x=True, label_pos="above_left")
        c.add_point_on_curve(pdf_curve, x=x_end, label=f"x={int(x_end)}", color="#DC2626", drop_x=True, label_pos="above_right")
        c.add_point(x_max, 0.0, label=f"{int(x_max)}", color="#080908", label_pos="below")
        
        c.add_shaded_region(fn_top=f_pdf, x_range=(x_start, x_end), color="rgba(220, 38, 38, 0.14)")
        
        return c.compile()
