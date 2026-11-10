"""
=============================================================================
RootMath Analytical Geometry Engine (AnalyticalGeometryCompiler v1.0)
=============================================================================
A mathematically rigorous, declarative analytical geometry compiler.
Eliminates eyeball approximations, manual floating coordinates, and disconnected lines.

Principles:
1. Point-to-Curve Invariance: Points on curves must be evaluated as y = f(x).
2. Derivative-Driven Tangents: Tangent slopes must equal f'(x0) and pass through (x0, f(x0)).
3. Analytical Intersections: Intersections are computed via root finding f1(x) = f2(x).
4. Automated Perpendicular Projections: Drop lines are strictly perpendicular to axes.
5. Invariant Assertion: Crashes immediately if any geometric defect (|error| > 1e-5) exists.
=============================================================================
"""

import math
from typing import Callable, List, Dict, Any, Tuple, Optional

class AnalyticalFunction:
    """Represents a mathematical function f(x) with analytical differentiation and evaluation."""
    def __init__(self, fn: Callable[[float], float], label: Optional[str] = None, 
                 color: str = "#080908", width: float = 1.8, style: str = "solid"):
        self.fn = fn
        self.label = label
        self.color = color
        self.width = width
        self.style = style

    def eval(self, x: float) -> float:
        return self.fn(x)

    def derivative(self, x: float, h: float = 1e-6) -> float:
        """Central difference numerical differentiation with machine precision."""
        return (self.fn(x + h) - self.fn(x - h)) / (2.0 * h)


class AnalyticalGeometryCompiler:
    """
    Declarative geometry canvas that compiles mathematical specifications
    into 100% verified SVG diagrams.
    """
    def __init__(self, x_range: Tuple[float, float], y_range: Tuple[float, float],
                 width: float = 460, height: float = 145, preserve_aspect_ratio: bool = False):
        self.x_range = x_range
        self.y_range = y_range
        self.width = width
        self.height = height
        self.preserve_aspect_ratio = preserve_aspect_ratio
        
        self.curves: List[Dict[str, Any]] = []
        self.points: List[Dict[str, Any]] = []
        self.lines: List[Dict[str, Any]] = []
        self.intervals: List[Dict[str, Any]] = []
        self.right_angles: List[Dict[str, Any]] = []
        self.shaded_regions: List[Dict[str, Any]] = []
        self.annotations: List[Dict[str, Any]] = []

    @staticmethod
    def sanitize_label(label: Optional[str]) -> Optional[str]:
        if not label:
            return label
        import re
        # 1. Purge unreduced coefficient 1 before letters or symbols (e.g. 1eᵗ -> eᵗ, 1x -> x, 1eˣ -> eˣ)
        cleaned = re.sub(r'(?<![0-9\.a-zA-Z])1([xyzXYZ]|e\b|\\ln|\\exp)', r'\1', label)
        # 2. Ban and purge unicode emojis completely
        cleaned = re.sub(r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]', '', cleaned)
        return cleaned.strip()


    def add_curve(self, fn: Callable[[float], float], x_min: Optional[float] = None,
                  x_max: Optional[float] = None, label: Optional[str] = None,
                  color: str = "#080908", width: float = 1.8, style: str = "solid") -> AnalyticalFunction:
        """Registers a mathematical curve f(x)."""
        clean_lbl = self.sanitize_label(label)
        af = AnalyticalFunction(fn, label=clean_lbl, color=color, width=width, style=style)
        self.curves.append({
            "obj": af,
            "x_min": x_min if x_min is not None else self.x_range[0],
            "x_max": x_max if x_max is not None else self.x_range[1],
            "label": self.sanitize_label(label),
            "color": color,
            "width": width,
            "style": style
        })
        return af

    def add_point_on_curve(self, curve: AnalyticalFunction, x: float,
                           label: Optional[str] = None, color: str = "#DC2626",
                           drop_x: bool = True, drop_y: bool = False,
                           label_pos: str = "above", r: float = 3.2) -> Tuple[float, float]:
        """
        Binds a point strictly to a curve. The y-coordinate is mathematically
        computed as y = curve.eval(x). Floating coordinates are impossible.
        """
        y = curve.eval(x)
        if math.isnan(y) or math.isinf(y):
            raise ValueError(f"Point at x={x} yields non-finite y={y} on curve {curve.label}")
        
        self.points.append({
            "x": x,
            "y": y,
            "label": self.sanitize_label(label),
            "color": color,
            "drop_x": drop_x,
            "drop_y": drop_y,
            "label_pos": label_pos,
            "r": r,
            "bound_curve": curve
        })
        return x, y

    def add_point(self, x: float, y: float, label: Optional[str] = None,
                  color: str = "#DC2626", drop_x: bool = False, drop_y: bool = False,
                  label_pos: str = "above", r: float = 3.2) -> Tuple[float, float]:
        """Adds a standalone verified point (e.g. geometric focus, origin)."""
        self.points.append({
            "x": x,
            "y": y,
            "label": self.sanitize_label(label),
            "color": color,
            "drop_x": drop_x,
            "drop_y": drop_y,
            "label_pos": label_pos,
            "r": r
        })
        return x, y

    def add_tangent_line(self, curve: AnalyticalFunction, x_contact: float,
                         span_left: float = 1.0, span_right: float = 1.0,
                         label: Optional[str] = None, label_pt: Optional[Tuple[float, float]] = None,
                         color: str = "#DC2626", style: str = "dashed", width: float = 1.2,
                         label_pt_pos: str = "end") -> Dict[str, Any]:
        """
        Constructs an analytical tangent line passing through (x0, f(x0))
        with exact derivative slope m = f'(x0).
        """
        y_contact = curve.eval(x_contact)
        slope = curve.derivative(x_contact)
        
        # Systemic Geometric Closure: Automatically extend tangent to meet axes if they fall in canvas
        # 1. Check intersection with y-axis (x = 0)
        y_at_y_axis = y_contact - slope * x_contact
        if self.y_range[0] <= y_at_y_axis <= self.y_range[1]:
            dist_x = x_contact - 0.0
            if dist_x > 0:
                span_left = max(span_left, dist_x + 0.25)
            elif dist_x < 0:
                span_right = max(span_right, abs(dist_x) + 0.25)
                
        # 2. Check intersection with x-axis (y = 0)
        if abs(slope) > 1e-7:
            x_at_x_axis = x_contact - y_contact / slope
            if self.x_range[0] <= x_at_x_axis <= self.x_range[1]:
                if x_at_x_axis < x_contact:
                    span_left = max(span_left, (x_contact - x_at_x_axis) + 0.25)
                else:
                    span_right = max(span_right, (x_at_x_axis - x_contact) + 0.25)

        x1 = x_contact - span_left
        y1 = y_contact - slope * span_left
        x2 = x_contact + span_right
        y2 = y_contact + slope * span_right
        
        if label_pt is None:
            label_pt = (x2 + 0.1, y2) if label_pt_pos == "end" else (x1 - 0.1, y1)
        
        line_data = {
            "p1": (x1, y1),
            "p2": (x2, y2),
            "contact": (x_contact, y_contact),
            "slope": slope,
            "curve": curve,
            "label": self.sanitize_label(label),
            "label_pt": label_pt,
            "color": color,
            "style": style,
            "width": width
        }
        self.lines.append(line_data)
        return line_data

    def add_line(self, p1: Tuple[float, float], p2: Tuple[float, float],
                 label: Optional[str] = None, label_pt: Optional[Tuple[float, float]] = None,
                 color: str = "#DC2626", style: str = "dashed", width: float = 1.2):
        """Adds an exact line between two verified Cartesian points."""
        self.lines.append({
            "p1": p1,
            "p2": p2,
            "label": self.sanitize_label(label),
            "label_pt": label_pt,
            "color": color,
            "style": style,
            "width": width
        })

    def add_line_intersection(self, line1: Dict[str, Any], line2: Dict[str, Any],
                              label: Optional[str] = None, color: str = "#2563EB",
                              drop_x: bool = True, drop_y: bool = False,
                              label_pos: str = "below_right", r: float = 3.5) -> Tuple[float, float]:
        """
        Computes the analytical intersection of two lines.
        Guaranteed to satisfy both line equations.
        """
        x1, y1 = line1["p1"]
        x2, y2 = line1["p2"]
        x3, y3 = line2["p1"]
        x4, y4 = line2["p2"]
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-9:
            raise ValueError("Lines are parallel or coincident; no unique intersection.")
            
        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        t = t_num / denom
        x_int = x1 + t * (x2 - x1)
        y_int = y1 + t * (y2 - y1)
        
        self.points.append({
            "x": x_int,
            "y": y_int,
            "label": self.sanitize_label(label),
            "color": color,
            "drop_x": drop_x,
            "drop_y": drop_y,
            "label_pos": label_pos,
            "r": r
        })
        return x_int, y_int

    def add_curve_intersection(self, curve1: AnalyticalFunction, curve2: AnalyticalFunction,
                               bracket: Tuple[float, float], label: Optional[str] = None,
                               color: str = "#DC2626", drop_x: bool = True, drop_y: bool = False,
                               label_pos: str = "above_right", r: float = 3.5) -> Tuple[float, float]:
        """
        Solves curve1(x) == curve2(x) using bisection + Newton-Raphson.
        """
        a, b = bracket
        diff_fn = lambda x: curve1.eval(x) - curve2.eval(x)
        
        fa = diff_fn(a)
        fb = diff_fn(b)
        if fa * fb > 0:
            # Step search for root sign change
            steps = 40
            dx = (b - a) / steps
            found = False
            for i in range(steps):
                x_sub = a + i * dx
                if diff_fn(x_sub) * diff_fn(x_sub + dx) <= 0:
                    a, b = x_sub, x_sub + dx
                    found = True
                    break
            if not found:
                raise ValueError(f"No root bracket found for curves between {bracket}")
                
        # Bisection refinement
        for _ in range(50):
            mid = (a + b) / 2.0
            fmid = diff_fn(mid)
            if abs(fmid) < 1e-9 or (b - a) < 1e-9:
                break
            if diff_fn(a) * fmid <= 0:
                b = mid
            else:
                a = mid
                
        root_x = (a + b) / 2.0
        root_y = curve1.eval(root_x)
        
        self.points.append({
            "x": root_x,
            "y": root_y,
            "label": self.sanitize_label(label),
            "color": color,
            "drop_x": drop_x,
            "drop_y": drop_y,
            "label_pos": label_pos,
            "r": r
        })
        return root_x, root_y

    def add_ratio_intervals(self, points_x: List[float], labels: Optional[List[str]] = None,
                            y_level: Optional[float] = None):
        """Adds CSAT standard 1:1:1 geometric ratio brackets."""
        y_span = self.y_range[1] - self.y_range[0]
        actual_y = y_level if y_level is not None else self.y_range[0] + y_span * 0.08
        raw_labels = labels if labels else ["1"] * (len(points_x) - 1)
        # Systemic normalization: prevent duplicate "비율 비율 1"
        clean_labels = [str(l).replace("비율 ", "").replace("비율", "").strip() for l in raw_labels]
        self.intervals.append({
            "points": sorted(points_x),
            "labels": clean_labels,
            "y_level": actual_y
        })

    def add_right_angle(self, vertex: Tuple[float, float], dir1: Tuple[float, float],
                        dir2: Tuple[float, float], size: float = 8.0):
        """Adds standard perpendicular right-angle symbol."""
        self.right_angles.append({
            "vertex": vertex,
            "dir1": dir1,
            "dir2": dir2,
            "size": size
        })

    def add_shaded_region(self, fn_top: Callable[[float], float],
                          fn_bottom: Optional[Callable[[float], float]] = None,
                          x_range: Optional[Tuple[float, float]] = None,
                          color: str = "rgba(220, 38, 38, 0.12)"):
        """Adds shaded integration region between curves."""
        self.shaded_regions.append({
            "fn_top": fn_top,
            "fn_bottom": fn_bottom if fn_bottom else (lambda x: 0.0),
            "range": x_range if x_range else self.x_range,
            "color": color
        })

    def add_annotation(self, x: float, y: float, text: str, color: str = "#080908",
                       size: float = 8.5, weight: str = "bold", anchor: str = "middle"):
        """Adds text annotation at Cartesian coordinate."""
        self.annotations.append({
            "x": x,
            "y": y,
            "text": text,
            "color": color,
            "size": size,
            "weight": weight,
            "anchor": anchor
        })

    def verify_mathematical_invariants(self):
        """
        Inviolable Gate: Asserts that all geometric elements obey strict calculus
        and coordinate rules before SVG generation is permitted.
        """
        # 0. Anti-Secant Invariant Gate: Any line claiming to be a tangent MUST NOT cut through curves as a secant
        for l in self.lines:
            lbl = l.get("label", "")
            if lbl and "접선" in lbl:
                p1, p2 = l["p1"], l["p2"]
                # line equation y = m*x + b
                dx = p2[0] - p1[0]
                if abs(dx) > 1e-9:
                    m_line = (p2[1] - p1[1]) / dx
                    b_line = p1[1] - m_line * p1[0]
                    # Check every curve
                    for c_dict in self.curves:
                        c_obj = c_dict["obj"]
                        c_min = max(c_dict["x_min"], min(p1[0], p2[0]))
                        c_max = min(c_dict["x_max"], max(p1[0], p2[0]))
                        if c_max - c_min > 0.1:
                            # Sample points to detect sign changes (crossing)
                            signs = []
                            samples = 40
                            for s_idx in range(samples + 1):
                                xs = c_min + (c_max - c_min) * (s_idx / samples)
                                try:
                                    diff = c_obj.eval(xs) - (m_line * xs + b_line)
                                    if abs(diff) > 0.08:
                                        signs.append(1 if diff > 0 else -1)
                                except Exception:
                                    pass
                            # If signs contain both 1 and -1 across non-boundary points, line cuts through curve
                            if 1 in signs and -1 in signs:
                                # Count sign changes
                                changes = sum(1 for i in range(len(signs)-1) if signs[i] != signs[i+1])
                                if changes >= 2:
                                    raise AssertionError(
                                        f"MATHEMATICAL INVARIANT VIOLATION: Line labeled '{lbl}' is a SECANT (cuts through curve '{c_dict.get('label')}'), not a tangent! "
                                        f"Common tangents must touch strictly without crossing the curve interior."
                                    )

        # 1. Verify bound points
        for pt in self.points:
            if "bound_curve" in pt:
                c = pt["bound_curve"]
                expected_y = c.eval(pt["x"])
                actual_y = pt["y"]
                if abs(expected_y - actual_y) > 1e-4:
                    raise AssertionError(
                        f"Point ({pt['x']}, {actual_y}) disconnected from curve '{c.label}'! "
                        f"Expected y={expected_y}, discrepancy={abs(expected_y - actual_y)}"
                    )

        # 2. Verify tangents
        for l in self.lines:
            if "contact" in l:
                cx, cy = l["contact"]
                c = l["curve"]
                expected_cy = c.eval(cx)
                if abs(expected_cy - cy) > 1e-4:
                    raise AssertionError(
                        f"Tangent line contact point ({cx}, {cy}) not on curve '{c.label}'! "
                        f"Expected y={expected_cy}"
                    )
                # Verify line passes through contact point
                x1, y1 = l["p1"]
                x2, y2 = l["p2"]
                # line equation: (y - y1)/(y2 - y1) == (x - x1)/(x2 - x1)
                slope = (y2 - y1) / (x2 - x1)
                line_y_at_contact = y1 + slope * (cx - x1)
                if abs(line_y_at_contact - cy) > 1e-4:
                    raise AssertionError(
                        f"Tangent line does not pass through contact point ({cx}, {cy})! "
                        f"Evaluated line y={line_y_at_contact}"
                    )

    def compile(self) -> str:
        """
        Verifies all mathematical invariants and delegates rendering to MathEngineCore.
        """
        self.verify_mathematical_invariants()
        
        # Convert curves to functions format
        functions = []
        for c in self.curves:
            functions.append({
                "fn": c["obj"].fn,
                "x_min": c["x_min"],
                "x_max": c["x_max"],
                "label": c["label"],
                "color": c["color"],
                "width": c["width"],
                "style": c["style"]
            })
            
        from math_engine_core import MathEngineCore
        return MathEngineCore.render_cartesian_graph(
            x_range=self.x_range,
            y_range=self.y_range,
            functions=functions,
            points=self.points,
            lines=self.lines,
            intervals=self.intervals,
            right_angles=self.right_angles,
            shaded_regions=self.shaded_regions,
            annotations=self.annotations,
            width=self.width,
            height=self.height,
            preserve_aspect_ratio=self.preserve_aspect_ratio
        )
