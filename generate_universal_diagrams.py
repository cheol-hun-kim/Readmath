"""
=============================================================================
Universal Mathematical Diagram Generator (UniversalDiagramGenerator v3.2)
=============================================================================
Powered by MathEngineCore v3.1.
Enforces pure mathematical canvas: axes, curves, drop lines, brackets,
shaded regions, and right-angle markers without redundant badge/title collisions.
=============================================================================
"""

import math
from math_engine_core import MathEngineCore

def build_universal_svg_for_problem(prob_num: int, is_variation: bool = False) -> str:
    """
    Constructs declarative mathematical specifications for each problem type
    and renders them using MathEngineCore v3.1.
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
                "x": 150, "y": 42, "rule": f"홀수", "value": "a=1",
                "subs": [
                    {"x": 240, "y": 32, "rule": f"×{base}", "value": f"{base}"},
                    {"x": 240, "y": 52, "rule": f"log", "value": "1"}
                ]
            },
            {
                "x": 150, "y": 92, "rule": f"짝수", "value": f"a={base}",
                "subs": [
                    {"x": 240, "y": 82, "rule": f"×{base}", "value": f"{base*2}"},
                    {"x": 240, "y": 102, "rule": f"제약", "value": f"{base*base}"}
                ]
            }
        ]
        
        return MathEngineCore.render_tree_diagram(
            title=f"수열 귀납적 역추적 상태 트리 ({end_cond} 기준 역방향 탐색)",
            start_node={"x": 48, "y": 66, "label": "종착", "value": "End"},
            branches=branches,
            summary_badge={"title": "가능한 a₁ 합", "value": str(target_sum)},
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 2 & 14: Symmetric Exponential Curves & Orthogonal Tangents
    # -------------------------------------------------------------------------
    elif prob_num in [2, 14]:
        base = 2 if prob_num == 2 else 3
        t = 1.0
        
        f1 = lambda x: base**x
        f2 = lambda x: -(base**(-x))
        m = (base**t) * math.log(base)
        tangent1 = lambda x: m * (x - t) + (base**t)
        tangent2 = lambda x: m * (x + t) - (base**(-t))
        
        functions = [
            {"fn": f1, "x_min": -2.0, "x_max": 1.4, "color": "#080908", "width": 1.8, "label": f"y={base}ˣ"},
            {"fn": f2, "x_min": -1.4, "x_max": 2.0, "color": "#080908", "width": 1.8, "label": f"y=-{base}⁻ˣ"},
            {"fn": tangent1, "x_min": -0.8, "x_max": 1.5, "color": "#DC2626", "width": 1.2, "style": "dashed"},
            {"fn": tangent2, "x_min": -1.5, "x_max": 0.8, "color": "#DC2626", "width": 1.2, "style": "dashed"}
        ]
        
        points = [
            {"x": t, "y": base**t, "label": f"(t, {base}ᵗ)", "color": "#DC2626", "drop_x": True, "label_pos": "above_left"},
            {"x": -t, "y": -(base**(-t)), "label": f"(-t, -{base}⁻ᵗ)", "color": "#DC2626", "drop_x": True, "label_pos": "below_right"}
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-2.2, 2.2),
            y_range=(-3.2, 3.2),
            functions=functions,
            points=points,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 3 & 15: Cubic Function Tangent Boundary & 1:1:1 Ratio
    # -------------------------------------------------------------------------
    elif prob_num in [3, 15]:
        slope = -2 if prob_num == 3 else -3
        k = 2 if prob_num == 3 else 3
        g_fn = lambda x: ((x - k)**2) * (x + 1)
        tangent_fn = lambda x: slope * (x + 1)
        
        xi = (2.0 * k - 1.0) / 3.0
        x_min_pt = k
        x_cross = k + (k - xi)
        
        functions = [
            {"fn": g_fn, "x_min": -1.3, "x_max": x_cross + 0.3, "color": "#080908", "width": 1.8, "label": "g(x)"},
            {"fn": tangent_fn, "x_min": -1.3, "x_max": 1.5, "color": "#DC2626", "width": 1.2, "style": "dashed", "label": "접선"}
        ]
        
        points = [
            {"x": -1.0, "y": 0.0, "label": "t=-1", "color": "#DC2626", "drop_x": True, "label_pos": "above_left"},
            {"x": xi, "y": g_fn(xi), "label": f"변곡점", "color": "#080908", "drop_x": True, "label_pos": "above"},
            {"x": float(x_min_pt), "y": 0.0, "label": f"극소{x_min_pt}", "color": "#080908", "drop_x": True, "label_pos": "below"},
            {"x": x_cross, "y": g_fn(x_cross), "label": "교점α", "color": "#DC2626", "drop_x": True, "label_pos": "above_right"}
        ]
        
        intervals = [
            {
                "points": [-1.0, xi, float(x_min_pt), x_cross],
                "labels": ["1", "1", "1"],
                "y_level": -2.2
            }
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-1.6, x_cross + 0.6),
            y_range=(-3.2, 9.0),
            functions=functions,
            points=points,
            intervals=intervals,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 4 & 16: Quartic Function Differentiability & Fold Line y = a
    # -------------------------------------------------------------------------
    elif prob_num in [4, 16]:
        c_sq = 2.0 if prob_num == 4 else 6.0
        c = math.sqrt(c_sq)
        
        g_fn = lambda x: (x**2 - c_sq)**2
        f_fn = lambda x: -(x**2 - c_sq)**2
        
        functions = [
            {"fn": g_fn, "x_min": -2.2, "x_max": 2.2, "color": "#080908", "width": 1.8, "label": "g(x)=|f(x)-a|"},
            {"fn": f_fn, "x_min": -c, "x_max": c, "color": "#94A3B8", "width": 1.0, "style": "dashed"}
        ]
        
        points = [
            {"x": 0.0, "y": c_sq**2, "label": f"극대(0, {c_sq**2:.0f})", "color": "#DC2626", "drop_x": True, "label_pos": "above"},
            {"x": -c, "y": 0.0, "label": f"-c", "color": "#080908", "drop_x": True, "label_pos": "below"},
            {"x": c, "y": 0.0, "label": f"c", "color": "#080908", "drop_x": True, "label_pos": "below"}
        ]
        
        lines = [
            {"p1": (-2.5, 0.0), "p2": (2.5, 0.0), "color": "#0F172A", "width": 1.2, "style": "solid"}
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-2.6, 2.6),
            y_range=(-(c_sq**2)*0.5, (c_sq**2)*1.3),
            functions=functions,
            points=points,
            lines=lines,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 5 & 17: Geometric Series Convergence & Asymptote
    # -------------------------------------------------------------------------
    elif prob_num in [5, 17]:
        lim_val = 3.0 if prob_num == 5 else 4.0
        ans_val = 3 if prob_num == 5 else 6
        
        lines = [
            {"p1": (0.0, lim_val), "p2": (6.5, lim_val), "color": "#DC2626", "width": 1.3, "style": "dashed", "label": f"수렴선 y = {lim_val:.0f}"}
        ]
        
        points = []
        for n in range(1, 6):
            yn = lim_val + (ans_val - lim_val) * (0.35**(n-1))
            points.append({
                "x": float(n),
                "y": yn,
                "label": f"a{n}" if n <= 2 else "",
                "color": "#080908",
                "drop_x": True,
                "label_pos": "above"
            })
            
        return MathEngineCore.render_cartesian_graph(
            x_range=(0.0, 6.8),
            y_range=(0.0, max(ans_val, lim_val) * 1.4),
            functions=[],
            lines=lines,
            points=points,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 6 & 18: Exponential & Log Curves with Perpendicular Tangents
    # -------------------------------------------------------------------------
    elif prob_num in [6, 18]:
        coeff = 1.0 if prob_num == 6 else 2.0
        t = 1.0
        ans_sq = 14 if prob_num == 6 else 20
        
        f_exp = lambda x: coeff * math.exp(x)
        f_log = lambda x: coeff * math.log(x)
        Ax = t - 1.0
        By = coeff * t - coeff
        
        functions = [
            {"fn": f_exp, "x_min": -1.8, "x_max": 1.1, "color": "#080908", "width": 1.8, "label": f"y={coeff:.0f}eˣ" if coeff > 1 else "y=eˣ"},
            {"fn": f_log, "x_min": 0.2, "x_max": 3.4, "color": "#080908", "width": 1.8, "label": f"y={coeff:.0f}ln x" if coeff > 1 else "y=ln x"}
        ]
        
        lines = [
            {"p1": (Ax, 0.0), "p2": (t, f_exp(t)), "color": "#94A3B8", "width": 1.0, "style": "dashed"},
            {"p1": (0.0, By), "p2": (math.exp(t), coeff * t), "color": "#94A3B8", "width": 1.0, "style": "dashed"},
            {"p1": (Ax, 0.0), "p2": (0.0, By), "color": "#DC2626", "width": 2.0, "style": "solid", "label": "선분 AB"}
        ]
        
        points = [
            {"x": Ax, "y": 0.0, "label": f"A({Ax:.0f},0)", "color": "#DC2626", "label_pos": "below"},
            {"x": 0.0, "y": By, "label": f"B(0,{By:.0f})", "color": "#DC2626", "label_pos": "left"},
            {"x": t, "y": f_exp(t), "label": f"(t, eᵗ)", "color": "#080908", "label_pos": "above_left"}
        ]
        
        right_angles = [
            {"vertex": (0.0, 0.0), "dir1": (1.0, 0.0), "dir2": (0.0, -1.0), "size": 7}
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-2.0, 3.6),
            y_range=(-2.8, 3.8),
            functions=functions,
            lines=lines,
            points=points,
            right_angles=right_angles,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 7 & 19: Confocal Ellipse & Hyperbola Orthogonality
    # -------------------------------------------------------------------------
    elif prob_num in [7, 19]:
        ans_c = 16 if prob_num == 7 else 12
        c = 4.0 if prob_num == 7 else math.sqrt(12.0)
        a_e = 5.0 if prob_num == 7 else 4.0
        b_e = 3.0 if prob_num == 7 else math.sqrt(7.0)
        
        fn_ell_top = lambda x: b_e * math.sqrt(max(0.0, 1.0 - (x/a_e)**2))
        fn_ell_bot = lambda x: -b_e * math.sqrt(max(0.0, 1.0 - (x/a_e)**2))
        
        a_h = math.sqrt(2.0)
        b_h = math.sqrt(c**2 - a_h**2)
        fn_hyp_top = lambda x: b_h * math.sqrt(max(0.0, (x/a_h)**2 - 1.0))
        fn_hyp_bot = lambda x: -b_h * math.sqrt(max(0.0, (x/a_h)**2 - 1.0))
        
        functions = [
            {"fn": fn_ell_top, "x_min": -a_e, "x_max": a_e, "color": "#080908", "width": 1.6, "label": "타원"},
            {"fn": fn_ell_bot, "x_min": -a_e, "x_max": a_e, "color": "#080908", "width": 1.6},
            {"fn": fn_hyp_top, "x_min": a_h, "x_max": a_e + 0.3, "color": "#080908", "width": 1.6, "label": "쌍곡선"},
            {"fn": fn_hyp_bot, "x_min": a_h, "x_max": a_e + 0.3, "color": "#080908", "width": 1.6}
        ]
        
        points = [
            {"x": -c, "y": 0.0, "label": "F'", "color": "#DC2626", "label_pos": "below"},
            {"x": c, "y": 0.0, "label": "F", "color": "#DC2626", "label_pos": "below"},
            {"x": 2.5, "y": 2.1, "label": "P (직교!)", "color": "#EA580C", "label_pos": "above_right"}
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-5.8, 5.8),
            y_range=(-3.6, 3.6),
            functions=functions,
            points=points,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 8 & 20: Vector Addition & Midpoint Circle Decomposition
    # -------------------------------------------------------------------------
    elif prob_num in [8, 20]:
        R = 2.0 if prob_num == 8 else 3.0
        Ax = 3.0 if prob_num == 8 else 4.0
        ans_v = 68 if prob_num == 8 else 136
        
        fn_c_top = lambda x: math.sqrt(max(0.0, R**2 - x**2))
        fn_c_bot = lambda x: -math.sqrt(max(0.0, R**2 - x**2))
        
        functions = [
            {"fn": fn_c_top, "x_min": -R, "x_max": R, "color": "#080908", "width": 1.6, "label": f"x²+y²={R**2:.0f}"},
            {"fn": fn_c_bot, "x_min": -R, "x_max": R, "color": "#080908", "width": 1.6}
        ]
        
        lines = [
            {"p1": (0.0, 0.0), "p2": (Ax, 0.0), "color": "#94A3B8", "width": 1.0, "style": "dashed"},
            {"p1": (Ax, 0.0), "p2": (-R, 0.0), "color": "#DC2626", "width": 1.8, "style": "solid", "label": "|AM|_max"}
        ]
        
        points = [
            {"x": Ax, "y": 0.0, "label": f"A({Ax:.0f},0)", "color": "#DC2626", "label_pos": "above"},
            {"x": -R, "y": 0.0, "label": "최대M", "color": "#DC2626", "label_pos": "below_left"},
            {"x": R, "y": 0.0, "label": "최소M", "color": "#EA580C", "label_pos": "below_right"}
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-R - 1.0, Ax + 1.0),
            y_range=(-R - 0.8, R + 0.8),
            functions=functions,
            lines=lines,
            points=points,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 9 & 21: Spatial Geometry & 3D Projection
    # -------------------------------------------------------------------------
    elif prob_num in [9, 21]:
        ans_s = 120 if prob_num == 9 else 270
        side = 4.0 if prob_num == 9 else 6.0
        
        Ax, Ay = -side/2.0, 0.0
        Bx, By = side/2.0, 0.0
        Cx, Cy = 0.0, (math.sqrt(3.0)/2.0) * side
        R = side / 2.0
        fn_c_top = lambda x: math.sqrt(max(0.0, R**2 - x**2))
        
        functions = [
            {"fn": fn_c_top, "x_min": -R, "x_max": R, "color": "#94A3B8", "width": 1.0, "style": "dashed", "label": "P 자취"}
        ]
        
        lines = [
            {"p1": (Ax, Ay), "p2": (Bx, By), "color": "#080908", "width": 1.8},
            {"p1": (Bx, By), "p2": (Cx, Cy), "color": "#080908", "width": 1.8},
            {"p1": (Cx, Cy), "p2": (Ax, Ay), "color": "#080908", "width": 1.8},
            {"p1": (0.0, R), "p2": (Bx/2.0, Cy/2.0), "color": "#DC2626", "width": 1.3, "style": "dashed", "label": "d_max"}
        ]
        
        points = [
            {"x": Ax, "y": Ay, "label": "A", "color": "#080908", "label_pos": "below_left"},
            {"x": Bx, "y": By, "label": "B", "color": "#080908", "label_pos": "below_right"},
            {"x": Cx, "y": Cy, "label": "C", "color": "#080908", "label_pos": "above"},
            {"x": 0.0, "y": R, "label": "P(최대)", "color": "#DC2626", "label_pos": "above_left"}
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-side/2.0 - 0.8, side/2.0 + 0.8),
            y_range=(-0.8, Cy + 0.8),
            functions=functions,
            lines=lines,
            points=points,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 10 & 22: Conditional Probability Reduced Sample Space Partition
    # -------------------------------------------------------------------------
    elif prob_num in [10, 22]:
        p_ans = "3/5" if prob_num == 10 else "4/5"
        parts = ["A₁ (홀3)", "A₂ (홀1 짝2)", "A₃ (짝3)"]
        return MathEngineCore.render_venn_partition(
            title="조건부확률: 표본공간 S 축소 및 배반사건 직교 분할",
            partitions=parts,
            condition_name="조건 사건 B",
            target_indices=[1],
            p_val=p_ans,
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 11 & 23: Stars and Bars / Combinatorics Grid Partition
    # -------------------------------------------------------------------------
    elif prob_num in [11, 23]:
        ans_h = 25 if prob_num == 11 else 36
        target_sum = 12 if prob_num == 11 else 14
        
        branches = [
            {
                "x": 150, "y": 42, "rule": "a=1" if prob_num == 11 else "a=0", "value": "C1",
                "subs": [
                    {"x": 240, "y": 42, "rule": "H분할", "value": "₁₅"}
                ]
            },
            {
                "x": 150, "y": 92, "rule": "a=3" if prob_num == 11 else "a=2", "value": "C2",
                "subs": [
                    {"x": 240, "y": 92, "rule": "H분할", "value": "₁₀"}
                ]
            }
        ]
        
        return MathEngineCore.render_tree_diagram(
            title=f"중복조합 격자 분할 치환 (총합={target_sum}, a 제약)",
            start_node={"x": 48, "y": 66, "label": "제약", "value": "a"},
            branches=branches,
            summary_badge={"title": "순서쌍 개수", "value": str(ans_h)},
            width=460,
            height=125
        )

    # -------------------------------------------------------------------------
    # Problem 12 & 24: Probability Density Parabola & Symmetric Integral
    # -------------------------------------------------------------------------
    else: # 12, 24
        x_max = 4.0 if prob_num == 12 else 6.0
        axis_x = 2.0 if prob_num == 12 else 3.0
        x_start = 1.0 if prob_num == 12 else 2.0
        x_end = 3.0 if prob_num == 12 else 4.0
        ans_p = 69 if prob_num == 12 else 74
        
        k = (3.0 / 32.0) if prob_num == 12 else (1.0 / 36.0)
        f_pdf = lambda x: k * x * (x_max - x)
        
        functions = [
            {"fn": f_pdf, "x_min": 0.0, "x_max": x_max, "color": "#080908", "width": 2.0, "label": "f(x)"}
        ]
        
        lines = [
            {"p1": (axis_x, 0.0), "p2": (axis_x, f_pdf(axis_x)), "color": "#3B82F6", "width": 1.2, "style": "dashed", "label": f"대칭축 x={axis_x:.0f}"}
        ]
        
        points = [
            {"x": 0.0, "y": 0.0, "label": "0", "color": "#080908", "label_pos": "below"},
            {"x": x_start, "y": f_pdf(x_start), "label": f"x={x_start:.0f}", "color": "#DC2626", "drop_x": True, "label_pos": "above_left"},
            {"x": x_end, "y": f_pdf(x_end), "label": f"x={x_end:.0f}", "color": "#DC2626", "drop_x": True, "label_pos": "above_right"},
            {"x": x_max, "y": 0.0, "label": f"{x_max:.0f}", "color": "#080908", "label_pos": "below"}
        ]
        
        shaded_regions = [
            {
                "fn_top": f_pdf,
                "range": (x_start, x_end),
                "color": "rgba(220, 38, 38, 0.14)"
            }
        ]
        
        return MathEngineCore.render_cartesian_graph(
            x_range=(-0.4, x_max + 0.6),
            y_range=(-0.04, f_pdf(axis_x) * 1.3),
            functions=functions,
            lines=lines,
            points=points,
            shaded_regions=shaded_regions,
            width=460,
            height=125
        )
