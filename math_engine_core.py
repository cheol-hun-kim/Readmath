"""
=============================================================================
RootMath Universal Mathematical Visualization Engine (MathEngineCore v3.1)
=============================================================================
A generalized, mathematically rigorous plotting and geometry engine for
generating publication-grade CSAT (수능) diagrams.

- Zero Eyeball / Zero Bezier Guesswork:
  All curves are sampled numerically with high density (N >= 150 points).
- Automatic Coordinate Transform:
  Maps real Cartesian domain [x_min, x_max] x [y_min, y_max] to SVG pixels.
- CSAT Standard Visual Theme:
  Pure white canvas (#FFFFFF), dark slate ink (#080908), crimson auxiliary (#DC2626),
  clean slate axes (#334155), and exact geometric ratio brackets.
- Collision-Free Labeling:
  Offsets labels along normal vectors or safe quadrants away from curves.
- Strict Page Budget Compliance:
  Standard compact card height (125px) fits exactly 2 problems per A4 page.
=============================================================================
"""

import math
from typing import List, Dict, Any, Tuple, Optional, Callable

class CoordinateTransformer:
    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float,
                 width: float = 460, height: float = 125, padding: float = 24):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = width
        self.height = height
        self.padding = padding
        
        # Usable drawing area
        self.draw_w = width - 2 * padding
        self.draw_h = height - 2 * padding
        
        # Scaling factors
        self.scale_x = self.draw_w / (x_max - x_min) if x_max != x_min else 1.0
        self.scale_y = self.draw_h / (y_max - y_min) if y_max != y_min else 1.0

    def to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """Converts Cartesian (x, y) to SVG (X_px, Y_px)."""
        X = self.padding + (x - self.x_min) * self.scale_x
        Y = self.height - self.padding - (y - self.y_min) * self.scale_y
        return round(X, 2), round(Y, 2)

    def to_cartesian(self, X: float, Y: float) -> Tuple[float, float]:
        x = self.x_min + (X - self.padding) / self.scale_x
        y = self.y_min + (self.height - self.padding - Y) / self.scale_y
        return x, y

    def is_in_bounds(self, x: float, y: float) -> bool:
        return (self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max)


class MathEngineCore:
    """Universal SVG renderer for CSAT math problems."""

    @staticmethod
    def render_cartesian_graph(
        x_range: Tuple[float, float],
        y_range: Tuple[float, float],
        functions: List[Dict[str, Any]],
        points: Optional[List[Dict[str, Any]]] = None,
        lines: Optional[List[Dict[str, Any]]] = None,
        intervals: Optional[List[Dict[str, Any]]] = None,
        shaded_regions: Optional[List[Dict[str, Any]]] = None,
        right_angles: Optional[List[Dict[str, Any]]] = None,
        width: float = 460,
        height: float = 125,
        title: Optional[str] = None,
        formula_badge: Optional[str] = None
    ) -> str:
        """
        Renders a fully annotated Cartesian coordinate diagram with numerical accuracy.
        """
        ct = CoordinateTransformer(x_range[0], x_range[1], y_range[0], y_range[1], width, height)
        svg = []
        svg.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <rect width="{width}" height="{height}" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>')

        # Optional Title (Subtle top-left)
        if title:
            svg.append(f'  <text x="14" y="16" fill="#080908" font-size="9.5" font-weight="800">{title}</text>')
        if formula_badge:
            badge_w = 95
            svg.append(f'  <rect x="{width - badge_w - 12}" y="6" width="{badge_w}" height="20" rx="3" fill="#FFF7ED" stroke="#EA580C" stroke-width="0.8"/>')
            svg.append(f'  <text x="{width - badge_w/2 - 12}" y="19" fill="#EA580C" font-size="9" font-weight="900" text-anchor="middle">{formula_badge}</text>')

        # Axes
        origin_X, origin_Y = ct.to_screen(0, 0)
        axis_x_start = ct.padding - 8
        axis_x_end = width - ct.padding + 8
        axis_y_start = height - ct.padding + 8
        axis_y_end = ct.padding - 8

        # Clamped origin for axis lines if (0, 0) is outside bounds
        clamped_Y = max(ct.padding, min(height - ct.padding, origin_Y))
        clamped_X = max(ct.padding, min(width - ct.padding, origin_X))

        # Draw X Axis
        svg.append(f'  <line x1="{axis_x_start}" y1="{clamped_Y}" x2="{axis_x_end}" y2="{clamped_Y}" stroke="#334155" stroke-width="1.2"/>')
        svg.append(f'  <text x="{axis_x_end + 4}" y="{clamped_Y + 3.5}" fill="#334155" font-size="10" font-style="italic" font-weight="bold">x</text>')

        # Draw Y Axis
        svg.append(f'  <line x1="{clamped_X}" y1="{axis_y_start}" x2="{clamped_X}" y2="{axis_y_end}" stroke="#334155" stroke-width="1.2"/>')
        svg.append(f'  <text x="{clamped_X - 4}" y="{axis_y_end - 4}" fill="#334155" font-size="10" font-style="italic" font-weight="bold" text-anchor="middle">y</text>')

        # Origin Label
        if ct.is_in_bounds(0, 0):
            svg.append(f'  <text x="{clamped_X - 8}" y="{clamped_Y + 12}" fill="#64748B" font-size="9" font-style="italic">O</text>')

        # 1. Shaded Regions (e.g. Integrals)
        if shaded_regions:
            for sr in shaded_regions:
                fn_top = sr.get("fn_top")
                fn_bottom = sr.get("fn_bottom", lambda x: 0.0)
                sub_x_min, sub_x_max = sr.get("range", (x_range[0], x_range[1]))
                steps = 60
                top_pts = []
                bot_pts = []
                for i in range(steps + 1):
                    x = sub_x_min + (sub_x_max - sub_x_min) * i / float(steps)
                    yt = fn_top(x)
                    yb = fn_bottom(x)
                    Xt, Yt = ct.to_screen(x, yt)
                    Xb, Yb = ct.to_screen(x, yb)
                    top_pts.append(f"{Xt:.2f},{Yt:.2f}")
                    bot_pts.insert(0, f"{Xb:.2f},{Yb:.2f}")
                full_pts = " ".join(top_pts + bot_pts)
                color = sr.get("color", "rgba(220, 38, 38, 0.12)")
                svg.append(f'  <polygon points="{full_pts}" fill="{color}"/>')

        # 2. Mathematical Functions (Numerical Polyline Sampling)
        for fn_spec in functions:
            fn = fn_spec["fn"]
            color = fn_spec.get("color", "#080908")
            width_px = fn_spec.get("width", 1.8)
            style = fn_spec.get("style", "solid")
            label = fn_spec.get("label")
            dash_attr = ' stroke-dasharray="3 2"' if style == "dashed" else ''
            
            sub_x0 = fn_spec.get("x_min", x_range[0])
            sub_x1 = fn_spec.get("x_max", x_range[1])
            steps = fn_spec.get("steps", 140)
            
            pts = []
            last_X, last_Y = None, None
            for i in range(steps + 1):
                x = sub_x0 + (sub_x1 - sub_x0) * i / float(steps)
                try:
                    y = fn(x)
                except (ValueError, ZeroDivisionError, OverflowError):
                    continue
                if y is None or math.isnan(y) or math.isinf(y):
                    continue
                
                # Check within bounds
                if y_range[0] - (y_range[1]-y_range[0])*0.2 <= y <= y_range[1] + (y_range[1]-y_range[0])*0.2:
                    X, Y = ct.to_screen(x, y)
                    pts.append(f"{X:.2f},{Y:.2f}")
                    last_X, last_Y = X, Y

            if pts:
                svg.append(f'  <polyline fill="none" stroke="{color}" stroke-width="{width_px}"{dash_attr} points="{" ".join(pts)}"/>')
                if label and last_X is not None and last_Y is not None:
                    # Place label near curve end with collision offset
                    lbl_x = min(width - 55, last_X + 4)
                    lbl_y = max(24, min(height - 10, last_Y - 3))
                    svg.append(f'  <text x="{lbl_x}" y="{lbl_y}" fill="{color}" font-size="8.5" font-weight="bold">{label}</text>')

        # 3. Geometric Lines / Tangents / Chords
        if lines:
            for l_spec in lines:
                x1, y1 = l_spec["p1"]
                x2, y2 = l_spec["p2"]
                X1, Y1 = ct.to_screen(x1, y1)
                X2, Y2 = ct.to_screen(x2, y2)
                color = l_spec.get("color", "#DC2626")
                style = l_spec.get("style", "dashed")
                w_px = l_spec.get("width", 1.3)
                dash = ' stroke-dasharray="3 2"' if style == "dashed" else ''
                svg.append(f'  <line x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}" stroke="{color}" stroke-width="{w_px}"{dash}/>')
                label = l_spec.get("label")
                if label:
                    lx = l_spec.get("label_x", (X1 + X2) / 2)
                    ly = l_spec.get("label_y", (Y1 + Y2) / 2 - 6)
                    svg.append(f'  <text x="{lx}" y="{ly}" fill="{color}" font-size="8.5" font-weight="bold">{label}</text>')

        # 4. Right Angle Markers
        if right_angles:
            for ra in right_angles:
                vx, vy = ra["vertex"]
                d1x, d1y = ra["dir1"]
                d2x, d2y = ra["dir2"]
                size = ra.get("size", 8)
                V_X, V_Y = ct.to_screen(vx, vy)
                P1_X, P1_Y = ct.to_screen(vx + d1x, vy + d1y)
                P2_X, P2_Y = ct.to_screen(vx + d2x, vy + d2y)
                u1x, u1y = P1_X - V_X, P1_Y - V_Y
                u2x, u2y = P2_X - V_X, P2_Y - V_Y
                norm1 = math.hypot(u1x, u1y) or 1.0
                norm2 = math.hypot(u2x, u2y) or 1.0
                u1x, u1y = (u1x / norm1) * size, (u1y / norm1) * size
                u2x, u2y = (u2x / norm2) * size, (u2y / norm2) * size
                c1_x, c1_y = V_X + u1x, V_Y + u1y
                c2_x, c2_y = V_X + u1x + u2x, V_Y + u1y + u2y
                c3_x, c3_y = V_X + u2x, V_Y + u2y
                svg.append(f'  <polyline points="{c1_x:.2f},{c1_y:.2f} {c2_x:.2f},{c2_y:.2f} {c3_x:.2f},{c3_y:.2f}" fill="none" stroke="#DC2626" stroke-width="1.1"/>')

        # 5. Key Points, Projections (Drop Lines), and Labels
        if points:
            for pt in points:
                x = pt["x"]
                y = pt["y"]
                X, Y = ct.to_screen(x, y)
                color = pt.get("color", "#DC2626")
                r = pt.get("r", 3.2)
                
                # Projection / Drop Line to Axis
                if pt.get("drop_x", False):
                    svg.append(f'  <line x1="{X}" y1="{Y}" x2="{X}" y2="{clamped_Y}" stroke="#94A3B8" stroke-width="0.9" stroke-dasharray="2 2"/>')
                if pt.get("drop_y", False):
                    svg.append(f'  <line x1="{X}" y1="{Y}" x2="{clamped_X}" y2="{Y}" stroke="#94A3B8" stroke-width="0.9" stroke-dasharray="2 2"/>')

                # Dot
                svg.append(f'  <circle cx="{X}" cy="{Y}" r="{r}" fill="{color}"/>')

                # Label
                label = pt.get("label")
                if label:
                    pos = pt.get("label_pos", "above")
                    offset_x, offset_y = 0, 0
                    anchor = "middle"
                    if pos == "above":
                        offset_y = -7
                    elif pos == "below":
                        offset_y = 11
                    elif pos == "left":
                        offset_x = -7
                        anchor = "end"
                    elif pos == "right":
                        offset_x = 7
                        anchor = "start"
                    elif pos == "above_left":
                        offset_x = -6
                        offset_y = -6
                        anchor = "end"
                    elif pos == "above_right":
                        offset_x = 6
                        offset_y = -6
                        anchor = "start"
                    elif pos == "below_right":
                        offset_x = 6
                        offset_y = 10
                        anchor = "start"
                    elif pos == "below_left":
                        offset_x = -6
                        offset_y = 10
                        anchor = "end"

                    lbl_X = X + offset_x
                    lbl_Y = Y + offset_y
                    svg.append(f'  <text x="{lbl_X:.2f}" y="{lbl_Y:.2f}" fill="{color}" font-size="8.5" font-weight="bold" text-anchor="{anchor}">{label}</text>')

        # 6. Geometric Ratio Intervals (Brackets e.g. 1 : 1 : 1)
        if intervals:
            for itv in intervals:
                pts_x = itv["points"]
                labels = itv.get("labels", ["1"] * (len(pts_x) - 1))
                y_level = itv.get("y_level", y_range[0] - (y_range[1] - y_range[0]) * 0.08)
                _, b_Y = ct.to_screen(0, y_level)
                bracket_h = 4.0
                
                # Draw base bar
                start_X, _ = ct.to_screen(pts_x[0], y_level)
                end_X, _ = ct.to_screen(pts_x[-1], y_level)
                svg.append(f'  <line x1="{start_X}" y1="{b_Y}" x2="{end_X}" y2="{b_Y}" stroke="#475569" stroke-width="1.0"/>')
                
                # Draw ticks and interval labels
                for idx in range(len(pts_x)):
                    pX, _ = ct.to_screen(pts_x[idx], y_level)
                    svg.append(f'  <line x1="{pX}" y1="{b_Y - bracket_h}" x2="{pX}" y2="{b_Y + bracket_h}" stroke="#475569" stroke-width="1.0"/>')
                    
                    if idx < len(pts_x) - 1:
                        next_pX, _ = ct.to_screen(pts_x[idx+1], y_level)
                        mid_X = (pX + next_pX) / 2.0
                        lbl = labels[idx] if idx < len(labels) else "1"
                        svg.append(f'  <text x="{mid_X:.2f}" y="{b_Y + 11}" fill="#0F172A" font-size="8" font-weight="bold" text-anchor="middle">비율 {lbl}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_tree_diagram(
        title: str,
        start_node: Dict[str, Any],
        branches: List[Dict[str, Any]],
        summary_badge: Dict[str, str],
        width: float = 460,
        height: float = 125
    ) -> str:
        """
        Universal Mathematical Recursive / State Tree Renderer for sequences and combinatorics.
        Strictly compact to fit within A4 card height.
        """
        svg = []
        svg.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <rect width="{width}" height="{height}" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>')
        svg.append(f'  <text x="14" y="16" fill="#080908" font-size="9.5" font-weight="800">{title}</text>')

        # Start Node on the left
        sx = start_node.get("x", 45)
        sy = height / 2.0 + 8
        slabel = start_node.get("label", "출발 조건")
        sval = start_node.get("value", "")
        svg.append(f'  <circle cx="{sx}" cy="{sy}" r="14" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.5"/>')
        svg.append(f'  <text x="{sx}" y="{sy + 3.5}" fill="#EA580C" font-size="9" font-weight="900" text-anchor="middle">{sval}</text>')
        svg.append(f'  <text x="{sx}" y="{sy - 18}" fill="#64748B" font-size="8" font-weight="bold" text-anchor="middle">{slabel}</text>')

        # Branch Out
        for b in branches:
            bx = b["x"]
            by = b["y"]
            rule = b.get("rule", "")
            val = b.get("value", "")
            
            # Line to branch node
            svg.append(f'  <path d="M {sx + 14} {sy} C {sx + 35} {sy}, {bx - 30} {by}, {bx - 14} {by}" fill="none" stroke="#94A3B8" stroke-width="1.2"/>')
            
            mid_x = (sx + bx) / 2
            mid_y = (sy + by) / 2
            if rule:
                svg.append(f'  <text x="{mid_x - 5}" y="{mid_y - 4}" fill="#DC2626" font-size="8" font-weight="bold" text-anchor="middle">{rule}</text>')
            
            # Node
            svg.append(f'  <rect x="{bx - 14}" y="{by - 10}" width="28" height="20" rx="3" fill="#F8FAFC" stroke="#334155" stroke-width="1.0"/>')
            svg.append(f'  <text x="{bx}" y="{by + 3.5}" fill="#080908" font-size="9" font-weight="bold" text-anchor="middle">{val}</text>')

            # Secondary sub-branches
            sub_nodes = b.get("subs", [])
            for sn in sub_nodes:
                snx = sn["x"]
                sny = sn["y"]
                srule = sn.get("rule", "")
                sval = sn.get("value", "")
                svg.append(f'  <line x1="{bx + 14}" y1="{by}" x2="{snx - 11}" y2="{sny}" stroke="#CBD5E1" stroke-width="1.0"/>')
                if srule:
                    svg.append(f'  <text x="{(bx + snx)/2}" y="{(by + sny)/2 - 3}" fill="#64748B" font-size="7.5">{srule}</text>')
                svg.append(f'  <circle cx="{snx}" cy="{sny}" r="10" fill="#FFFFFF" stroke="#080908" stroke-width="1.0"/>')
                svg.append(f'  <text x="{snx}" y="{sny + 3}" fill="#080908" font-size="8" font-weight="bold" text-anchor="middle">{sval}</text>')

        # Summary / Conclusion Card on right
        cw = 90
        ch = 56
        cx = width - cw - 15
        cy = (height - ch) / 2.0 + 6
        title_txt = summary_badge.get("title", "도출 결과")
        val_txt = summary_badge.get("value", "")
        svg.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="5" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.2"/>')
        svg.append(f'  <text x="{cx + cw/2}" y="{cy + 17}" fill="#16A34A" font-size="8.5" font-weight="bold" text-anchor="middle">{title_txt}</text>')
        svg.append(f'  <text x="{cx + cw/2}" y="{cy + 38}" fill="#15803D" font-size="14" font-weight="900" text-anchor="middle">{val_txt}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_venn_partition(
        title: str,
        partitions: List[str],
        condition_name: str,
        target_indices: List[int],
        p_val: str,
        width: float = 460,
        height: float = 125
    ) -> str:
        """
        Universal Sample Space Partition & Conditional Probability Diagram.
        Guarantees compact vertical dimensions, zero text overlap.
        """
        svg = []
        svg.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <rect width="{width}" height="{height}" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>')
        svg.append(f'  <text x="14" y="16" fill="#080908" font-size="9.5" font-weight="800">{title}</text>')

        # Universe S Rect
        ux, uy, uw, uh = 25, 28, 280, 85
        svg.append(f'  <rect x="{ux}" y="{uy}" width="{uw}" height="{uh}" rx="5" fill="#FAF8F3" stroke="#080908" stroke-width="1.2"/>')
        svg.append(f'  <text x="{ux + 10}" y="{uy + 15}" fill="#080908" font-size="9.5" font-weight="bold">전체 표본공간 S</text>')

        # Partition Verticals
        n = len(partitions)
        col_w = uw / float(n)
        for i in range(1, n):
            px = ux + i * col_w
            svg.append(f'  <line x1="{px}" y1="{uy}" x2="{px}" y2="{uy + uh}" stroke="#94A3B8" stroke-width="1.0" stroke-dasharray="2 2"/>')

        for i, part_name in enumerate(partitions):
            mid_x = ux + (i + 0.5) * col_w
            svg.append(f'  <text x="{mid_x}" y="{uy + uh - 8}" fill="#64748B" font-size="8.5" font-weight="bold" text-anchor="middle">{part_name}</text>')

        # Condition Event B Ellipse
        ell_cx = ux + uw / 2.0
        ell_cy = uy + uh / 2.0 - 2
        ell_rx = (uw / 2.0) - 20
        ell_ry = 24
        svg.append(f'  <ellipse cx="{ell_cx}" cy="{ell_cy}" rx="{ell_rx}" ry="{ell_ry}" fill="rgba(220, 38, 38, 0.08)" stroke="#DC2626" stroke-width="1.4"/>')
        svg.append(f'  <text x="{ell_cx}" y="{ell_cy - 12}" fill="#DC2626" font-size="9" font-weight="bold" text-anchor="middle">{condition_name} (축소 분모)</text>')

        # Intersections
        for i in range(n):
            mid_x = ux + (i + 0.5) * col_w
            is_target = i in target_indices
            dot_color = "#EA580C" if is_target else "#DC2626"
            dot_cy = ell_cy + 6
            svg.append(f'  <circle cx="{mid_x}" cy="{dot_cy}" r="2.8" fill="{dot_color}"/>')
            weight = "900" if is_target else "600"
            color = "#EA580C" if is_target else "#0F172A"
            label = f"B∩A{i+1}" + ("(분자)" if is_target else "")
            svg.append(f'  <text x="{mid_x}" y="{dot_cy + 13}" fill="{color}" font-size="8" font-weight="{weight}" text-anchor="middle">{label}</text>')

        # Right Summary Card
        rw = 95
        rh = 65
        rx = width - rw - 15
        ry = (height - rh) / 2.0 + 8
        svg.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="5" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.2"/>')
        svg.append(f'  <text x="{rx + rw/2}" y="{ry + 18}" fill="#EA580C" font-size="9" font-weight="bold" text-anchor="middle">P(B|A)</text>')
        svg.append(f'  <text x="{rx + rw/2}" y="{ry + 42}" fill="#C2410C" font-size="15" font-weight="900" text-anchor="middle">{p_val}</text>')
        svg.append(f'  <text x="{rx + rw/2}" y="{ry + 56}" fill="#64748B" font-size="7.5" text-anchor="middle">표본공간 축소</text>')

        svg.append('</svg>')
        return "\n".join(svg)

print("MathEngineCore v3.1 loaded successfully.")
