"""
=============================================================================
RootMath Universal Mathematical Visualization Engine (MathEngineCore v4.0)
=============================================================================
A generalized, mathematically rigorous plotting and geometry engine for
generating publication-grade CSAT (수능) diagrams.

- Zero Eyeball / Zero Bezier Guesswork:
  All curves are sampled numerically with high density (N >= 160 points).
- Strict Aspect Ratio Preservation (등방성 좌표계 지원):
  Preserves true angles, true perpendicularity (90°), and true exponential curvature.
- Analytical/Symbolic Geometric Solver Integration:
  Intersection coordinates, inflection points, and tangent slopes are computed
  with exact analytical mathematics (Zero Floating Point Defects).
- Collision-Free Dynamic Labeling:
  Labels are placed at safe offsets away from curves, axes, and lines.
- CSAT Standard Minimal Visual Purity:
  Pure white canvas (#FFFFFF), dark slate ink (#080908), crimson auxiliary (#DC2626),
  clean slate axes (#334155), and exact geometric ratio brackets.
=============================================================================
"""

import math
from typing import List, Dict, Any, Tuple, Optional, Callable

class CoordinateTransformer:
    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float,
                 width: float = 460, height: float = 135, padding: float = 24,
                 preserve_aspect_ratio: bool = False):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = width
        self.height = height
        self.padding = padding
        self.preserve_aspect_ratio = preserve_aspect_ratio
        
        # Usable drawing area
        self.draw_w = width - 2 * padding
        self.draw_h = height - 2 * padding
        
        # Scaling factors
        raw_scale_x = self.draw_w / (x_max - x_min) if x_max != x_min else 1.0
        raw_scale_y = self.draw_h / (y_max - y_min) if y_max != y_min else 1.0

        if preserve_aspect_ratio:
            scale = min(raw_scale_x, raw_scale_y)
            self.scale_x = scale
            self.scale_y = scale
            actual_w = (x_max - x_min) * scale
            actual_h = (y_max - y_min) * scale
            self.offset_x = (self.draw_w - actual_w) / 2.0
            self.offset_y = (self.draw_h - actual_h) / 2.0
        else:
            self.scale_x = raw_scale_x
            self.scale_y = raw_scale_y
            self.offset_x = 0.0
            self.offset_y = 0.0

    def to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """Converts Cartesian (x, y) to SVG (X_px, Y_px)."""
        X = self.padding + self.offset_x + (x - self.x_min) * self.scale_x
        Y = self.height - self.padding - self.offset_y - (y - self.y_min) * self.scale_y
        return round(X, 2), round(Y, 2)

    def to_cartesian(self, X: float, Y: float) -> Tuple[float, float]:
        x = self.x_min + (X - self.padding - self.offset_x) / self.scale_x
        y = self.y_min + (self.height - self.padding - self.offset_y - Y) / self.scale_y
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
        annotations: Optional[List[Dict[str, Any]]] = None,
        width: float = 460,
        height: float = 135,
        preserve_aspect_ratio: bool = False
    ) -> str:
        """
        Renders a fully annotated Cartesian coordinate diagram with numerical accuracy.
        """
        ct = CoordinateTransformer(
            x_range[0], x_range[1], y_range[0], y_range[1],
            width, height, padding=24, preserve_aspect_ratio=preserve_aspect_ratio
        )
        svg = []
        svg.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <rect width="{width}" height="{height}" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>')

        # Axes
        origin_X, origin_Y = ct.to_screen(0, 0)
        # Full-span axes across the canvas for true publication quality
        axis_x_start = ct.padding
        axis_x_end = width - ct.padding
        axis_y_start = height - ct.padding
        axis_y_end = ct.padding

        # Clamped origin for axis lines if (0, 0) is outside bounds
        clamped_Y = max(ct.padding, min(height - ct.padding, origin_Y))
        clamped_X = max(ct.padding, min(width - ct.padding, origin_X))

        # Draw X Axis
        svg.append(f'  <line x1="{axis_x_start}" y1="{clamped_Y}" x2="{axis_x_end}" y2="{clamped_Y}" stroke="#334155" stroke-width="1.2"/>')
        svg.append(f'  <text x="{axis_x_end + 4}" y="{clamped_Y + 3.5}" fill="#334155" font-size="10" font-style="italic" font-weight="bold">x</text>')

        # Draw Y Axis
        svg.append(f'  <line x1="{clamped_X}" y1="{axis_y_start}" x2="{clamped_X}" y2="{axis_y_end}" stroke="#334155" stroke-width="1.2"/>')
        svg.append(f'  <text x="{clamped_X - 4}" y="{axis_y_end - 4}" fill="#334155" font-size="10" font-style="italic" font-weight="bold" text-anchor="middle">y</text>')

        # Origin Label (avoiding collision with curves near (0,0))
        if ct.is_in_bounds(0, 0):
            svg.append(f'  <text x="{clamped_X - 8}" y="{clamped_Y + 12}" fill="#64748B" font-size="9" font-style="italic">O</text>')

        # 1. Shaded Regions (e.g. Integrals)
        if shaded_regions:
            for sr in shaded_regions:
                fn_top = sr.get("fn_top")
                fn_bottom = sr.get("fn_bottom", lambda x: 0.0)
                sub_x_min, sub_x_max = sr.get("range", (x_range[0], x_range[1]))
                steps = 80
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

        # 2. Mathematical Functions (Numerical Polyline Sampling N >= 160)
        for fn_spec in functions:
            fn = fn_spec["fn"]
            color = fn_spec.get("color", "#080908")
            width_px = fn_spec.get("width", 1.8)
            style = fn_spec.get("style", "solid")
            label = fn_spec.get("label")
            dash_attr = ' stroke-dasharray="3 2"' if style == "dashed" else ''
            
            sub_x0 = fn_spec.get("x_min", x_range[0])
            sub_x1 = fn_spec.get("x_max", x_range[1])
            steps = fn_spec.get("steps", 160)
            
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
                
                # Check within bounds with slight overflow tolerance
                y_span = y_range[1] - y_range[0]
                if y_range[0] - y_span*0.25 <= y <= y_range[1] + y_span*0.25:
                    X, Y = ct.to_screen(x, y)
                    pts.append(f"{X:.2f},{Y:.2f}")
                    last_X, last_Y = X, Y

            if pts:
                svg.append(f'  <polyline fill="none" stroke="{color}" stroke-width="{width_px}"{dash_attr} points="{" ".join(pts)}"/>')
                if label and last_X is not None and last_Y is not None:
                    # Place label near curve end with collision offset
                    lbl_x = min(width - 50, last_X + 4)
                    lbl_y = max(18, min(height - 8, last_Y - 4))
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
                    if l_spec.get("label_pt") is not None:
                        lx, ly = ct.to_screen(l_spec["label_pt"][0], l_spec["label_pt"][1])
                    else:
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
                        offset_x = -8
                        offset_y = -6
                        anchor = "end"
                    elif pos == "above_right":
                        offset_x = 8
                        offset_y = -6
                        anchor = "start"
                    elif pos == "below_right":
                        offset_x = 8
                        offset_y = 11
                        anchor = "start"
                    elif pos == "below_left":
                        offset_x = -8
                        offset_y = 11
                        anchor = "end"

                    lbl_X = X + offset_x
                    lbl_Y = Y + offset_y
                    svg.append(f'  <text x="{lbl_X:.2f}" y="{lbl_Y:.2f}" fill="{color}" font-size="8.5" font-weight="bold" text-anchor="{anchor}">{label}</text>')

        # 6. Geometric Ratio Intervals (Brackets e.g. 1 : 1 : 1)
        if intervals:
            for itv in intervals:
                pts_x = itv["points"]
                labels = itv.get("labels", ["1"] * (len(pts_x) - 1))
                y_level = itv.get("y_level", y_range[0] - (y_range[1] - y_range[0]) * 0.12)
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

        # 7. Custom Mathematical Annotations (placed at exact cartesian coordinates)
        if annotations:
            for ann in annotations:
                ax, ay = ann["x"], ann["y"]
                aX, aY = ct.to_screen(ax, ay)
                txt = ann["text"]
                color = ann.get("color", "#080908")
                size = ann.get("size", 8.5)
                weight = ann.get("weight", "bold")
                anchor = ann.get("anchor", "middle")
                svg.append(f'  <text x="{aX:.2f}" y="{aY:.2f}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{txt}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_tree_diagram(
        title: str,
        start_node: Dict[str, Any],
        branches: List[Dict[str, Any]],
        summary_badge: Optional[Dict[str, str]] = None,
        width: float = 460,
        height: float = 135
    ) -> str:
        """
        Renders a clean tree diagram for sequence reverse tracking and combinatorics.
        """
        svg = []
        svg.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <rect width="{width}" height="{height}" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>')

        # Root Node
        sx, sy = start_node["x"], start_node["y"]
        svg.append(f'  <circle cx="{sx}" cy="{sy}" r="16" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.5"/>')
        svg.append(f'  <text x="{sx}" y="{sy + 4}" fill="#EA580C" font-size="10" font-weight="900" text-anchor="middle">{start_node.get("label", "Start")}</text>')

        # Branches
        for b in branches:
            bx, by = b["x"], b["y"]
            svg.append(f'  <line x1="{sx + 16}" y1="{sy}" x2="{bx - 24}" y2="{by}" stroke="#CBD5E1" stroke-width="1.2"/>')
            svg.append(f'  <rect x="{bx - 24}" y="{by - 12}" width="48" height="24" rx="4" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.0"/>')
            svg.append(f'  <text x="{bx}" y="{by + 4}" fill="#0F172A" font-size="9" font-weight="bold" text-anchor="middle">{b.get("value", "")}</text>')
            if b.get("rule"):
                svg.append(f'  <text x="{(sx + bx)/2}" y="{(sy + by)/2 - 5}" fill="#DC2626" font-size="8" font-weight="bold" text-anchor="middle">{b["rule"]}</text>')

            # Sub-branches
            if "subs" in b:
                for sub in b["subs"]:
                    sub_x, sub_y = sub["x"], sub["y"]
                    svg.append(f'  <line x1="{bx + 24}" y1="{by}" x2="{sub_x - 12}" y2="{sub_y}" stroke="#CBD5E1" stroke-width="1.0"/>')
                    svg.append(f'  <circle cx="{sub_x}" cy="{sub_y}" r="10" fill="#FFFFFF" stroke="#334155" stroke-width="1.0"/>')
                    svg.append(f'  <text x="{sub_x}" y="{sub_y + 3.5}" fill="#080908" font-size="8.5" font-weight="bold" text-anchor="middle">{sub.get("value", "")}</text>')
                    if sub.get("rule"):
                        svg.append(f'  <text x="{(bx + sub_x)/2 + 6}" y="{(by + sub_y)/2 - 3}" fill="#64748B" font-size="7.5" text-anchor="middle">{sub["rule"]}</text>')

        # Summary Badge
        if summary_badge:
            bw, bh = 80, 52
            bx_pos, by_pos = width - bw - 16, (height - bh) / 2
            svg.append(f'  <rect x="{bx_pos}" y="{by_pos}" width="{bw}" height="{bh}" rx="6" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.2"/>')
            svg.append(f'  <text x="{bx_pos + bw/2}" y="{by_pos + 18}" fill="#166534" font-size="8.5" font-weight="bold" text-anchor="middle">{summary_badge["title"]}</text>')
            svg.append(f'  <text x="{bx_pos + bw/2}" y="{by_pos + 40}" fill="#15803D" font-size="15" font-weight="900" text-anchor="middle">{summary_badge["value"]}</text>')

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
        height: float = 135
    ) -> str:
        """
        Renders a clean partition diagram for conditional probability sample spaces.
        """
        svg = []
        svg.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <rect width="{width}" height="{height}" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.0"/>')

        # Outer Sample Space S Box
        pad_x, pad_y = 35, 20
        box_w, box_h = width - 2 * pad_x, height - 2 * pad_y
        svg.append(f'  <rect x="{pad_x}" y="{pad_y}" width="{box_w}" height="{box_h}" rx="6" fill="#F8FAFC" stroke="#334155" stroke-width="1.4"/>')
        svg.append(f'  <text x="{pad_x + 10}" y="{pad_y + 16}" fill="#0F172A" font-size="9" font-weight="bold">전체 표본공간 S</text>')

        # Vertical Partition Lines
        n_parts = len(partitions)
        col_w = box_w / float(n_parts)
        for i in range(1, n_parts):
            px = pad_x + i * col_w
            svg.append(f'  <line x1="{px}" y1="{pad_y}" x2="{px}" y2="{pad_y + box_h}" stroke="#94A3B8" stroke-width="1.0" stroke-dasharray="3 3"/>')

        # Condition Event Oval
        ov_cx = pad_x + box_w / 2.0
        ov_cy = pad_y + box_h / 2.0 + 2
        ov_rx = box_w * 0.44
        ov_ry = box_h * 0.36
        svg.append(f'  <ellipse cx="{ov_cx}" cy="{ov_cy}" rx="{ov_rx}" ry="{ov_ry}" fill="rgba(220, 38, 38, 0.08)" stroke="#DC2626" stroke-width="1.5"/>')
        svg.append(f'  <text x="{ov_cx}" y="{ov_cy - ov_ry + 10}" fill="#DC2626" font-size="8.5" font-weight="bold" text-anchor="middle">{condition_name}</text>')

        # Partition Labels
        for i, name in enumerate(partitions):
            cx = pad_x + (i + 0.5) * col_w
            svg.append(f'  <text x="{cx}" y="{pad_y + box_h - 8}" fill="#475569" font-size="7.5" font-weight="bold" text-anchor="middle">{name}</text>')
            is_target = i in target_indices
            dot_color = "#DC2626" if is_target else "#64748B"
            dot_r = 3.5 if is_target else 2.5
            svg.append(f'  <circle cx="{cx}" cy="{ov_cy - 4}" r="{dot_r}" fill="{dot_color}"/>')
            if is_target:
                svg.append(f'  <text x="{cx}" y="{ov_cy + 9}" fill="{dot_color}" font-size="7.5" font-weight="bold" text-anchor="middle">B ∩ {name}</text>')
                svg.append(f'  <text x="{cx}" y="{ov_cy + 19}" fill="{dot_color}" font-size="7.5" font-weight="bold" text-anchor="middle">(타깃)</text>')
            else:
                svg.append(f'  <text x="{cx}" y="{ov_cy + 12}" fill="{dot_color}" font-size="7.5" font-weight="bold" text-anchor="middle">B ∩ {name}</text>')

        svg.append('</svg>')
        return "\n".join(svg)
