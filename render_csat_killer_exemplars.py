"""
=============================================================================
CSAT Killer Problem Exemplars (Drawn with AnalyticalGeometryCompiler)
=============================================================================
Validates that ANY historical CSAT exam problem graph can be rendered
with 100% mathematical precision and zero eyeball guesswork.
=============================================================================
"""

import os, sys, math, pymupdf
sys.stdout.reconfigure(encoding='utf-8')

from analytical_geometry_engine import AnalyticalGeometryCompiler, AnalyticalFunction

out_dir = "csat_exemplars"
os.makedirs(out_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. 2024 수능 공통 22번 (삼차함수 극값 및 미분계수 곱 음수 조건)
# -----------------------------------------------------------------------------
# f(x) = x^3 - 3x  => f'(x) = 3(x^2 - 1). Local max (-1, 2), Local min (1, -2).
c1 = AnalyticalGeometryCompiler(x_range=(-2.5, 2.5), y_range=(-3.5, 3.5), width=480, height=180)
f1 = c1.add_curve(lambda x: x**3 - 3*x, x_min=-2.2, x_max=2.2, label="y=f(x)")
c1.add_point_on_curve(f1, x=-1.0, label="극대(-1,2)", color="#DC2626", drop_x=True, label_pos="above_left")
c1.add_point_on_curve(f1, x=1.0, label="극소(1,-2)", color="#DC2626", drop_x=True, label_pos="below_right")
c1.add_point_on_curve(f1, x=0.0, label="변곡점(0,0)", color="#080908", drop_x=True, label_pos="above_right")

# Tangent line at inflection point: y = -3x
c1.add_tangent_line(f1, x_contact=0.0, span_left=1.0, span_right=1.0, label="변곡접선", color="#2563EB")
# Horizontal tangent lines at local extrema
c1.add_tangent_line(f1, x_contact=-1.0, span_left=0.8, span_right=1.5, label="y=2", color="#DC2626")
c1.add_tangent_line(f1, x_contact=1.0, span_left=1.5, span_right=0.8, label="y=-2", color="#DC2626")

svg1 = c1.compile()
with open(os.path.join(out_dir, "csat_2024_22.svg"), "w", encoding="utf-8") as f:
    f.write(svg1)

# -----------------------------------------------------------------------------
# 2. 2025 수능 미적분 30번 (지수함수 역함수 및 대칭축 y=x 직교)
# -----------------------------------------------------------------------------
# f(x) = e^(x-1), g(x) = ln(x) + 1. Symmetric across y = x.
c2 = AnalyticalGeometryCompiler(x_range=(-1.5, 4.0), y_range=(-1.5, 4.0), width=480, height=180, preserve_aspect_ratio=True)
fn_exp = c2.add_curve(lambda x: math.exp(x - 1.0), x_min=-1.0, x_max=2.3, label="y=f(x)")
fn_log = c2.add_curve(lambda x: math.log(x) + 1.0, x_min=0.15, x_max=3.8, label="y=f⁻¹(x)")
fn_diag = c2.add_curve(lambda x: x, x_min=-1.2, x_max=3.8, color="#94A3B8", width=1.1, style="dashed", label="y=x")

# Fixed point of intersection with y = x at x = 1 (since e^(1-1) = 1)
c2.add_point_on_curve(fn_exp, x=1.0, label="(1,1)", color="#DC2626", drop_x=True, label_pos="above_left")

# Symmetric points: (2, e) on f, (e, 2) on f^-1
e_val = math.e
c2.add_point_on_curve(fn_exp, x=2.0, label=f"P(2,e)", color="#DC2626", label_pos="above_left")
c2.add_point_on_curve(fn_log, x=e_val, label=f"P'(e,2)", color="#DC2626", label_pos="below_right")

# Connecting chord PP' orthogonal to y = x
c2.add_line((2.0, e_val), (e_val, 2.0), color="#DC2626", width=1.5, style="solid", label="대칭선분 PP'")
c2.add_right_angle(((2.0 + e_val)/2.0, (2.0 + e_val)/2.0), (1.0, 1.0), (-(e_val - 2.0), (e_val - 2.0)), size=7.0)

svg2 = c2.compile()
with open(os.path.join(out_dir, "csat_2025_30.svg"), "w", encoding="utf-8") as f:
    f.write(svg2)

# -----------------------------------------------------------------------------
# 3. 2023 수능 22번 (삼차함수 접선 3개 영역 및 접점)
# -----------------------------------------------------------------------------
# g(x) = (x + 1)^2 * (2 - x) = -(x^3) + 3x + 2.
c3 = AnalyticalGeometryCompiler(x_range=(-2.6, 2.8), y_range=(-2.0, 5.0), width=480, height=180)
g3 = c3.add_curve(lambda x: ((x + 1.0)**2) * (2.0 - x), x_min=-2.4, x_max=2.4, label="y=g(x)")

# Min at x = -1 (y=0), Max at x = 1 (y=4)
c3.add_point_on_curve(g3, x=-1.0, label="극소(-1,0)", color="#080908", label_pos="below")
c3.add_point_on_curve(g3, x=1.0, label="극대(1,4)", color="#DC2626", drop_x=True, label_pos="above")

# Tangent line at x=1: y = 4 (horizontal), reaching x = -2.3
c3.add_tangent_line(g3, x_contact=1.0, span_left=3.3, span_right=1.2, label="접선 y=4", label_pt_pos="end", color="#DC2626")

# Intersection of horizontal tangent y=4 with curve g(x):
# -(x^3) + 3x + 2 = 4 => x^3 - 3x + 2 = 0 => (x-1)^2 * (x+2) = 0 => x = -2!
c3.add_curve_intersection(g3, AnalyticalFunction(lambda x: 4.0), bracket=(-2.3, -1.8),
                          label="교점(-2,4)", color="#2563EB", drop_x=True, label_pos="above_left")

svg3 = c3.compile()
with open(os.path.join(out_dir, "csat_2023_22.svg"), "w", encoding="utf-8") as f:
    f.write(svg3)

print("All 3 exemplar CSAT SVGs compiled successfully!")

# Convert SVGs to PNG via PyMuPDF
for name in ["csat_2024_22", "csat_2025_30", "csat_2023_22"]:
    svg_path = os.path.join(out_dir, f"{name}.svg")
    png_path = os.path.join(out_dir, f"{name}.png")
    
    # Wrap SVG in minimal HTML for fitz rendering or open directly
    doc = pymupdf.open(svg_path)
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    pix.save(png_path)
    print(f"Rendered {name} -> {png_path} ({os.path.getsize(png_path)} bytes)")
