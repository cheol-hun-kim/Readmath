with open('analytical_geometry_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add sanitize_label static method to AnalyticalGeometryCompiler
sanitize_method = '''    @staticmethod
    def sanitize_label(label: Optional[str]) -> Optional[str]:
        if not label:
            return label
        import re
        # 1. Purge unreduced coefficient 1 before letters or symbols (e.g. 1eᵗ -> eᵗ, 1x -> x, 1eˣ -> eˣ)
        cleaned = re.sub(r'(?<![0-9\.a-zA-Z])1([a-zA-Z\\])(?![0-9])', r'\\1', label)
        # 2. Ban and purge unicode emojis completely
        cleaned = re.sub(r'[\\U00010000-\\U0010ffff\\u2600-\\u26ff\\u2700-\\u27bf]', '', cleaned)
        return cleaned.strip()
'''

if 'def sanitize_label' not in text:
    text = text.replace('self.annotations: List[Dict[str, Any]] = []', 'self.annotations: List[Dict[str, Any]] = []\n\n' + sanitize_method)

# Sanitize in add_curve
text = text.replace('af = AnalyticalFunction(fn, label=label, color=color, width=width, style=style)',
                    'clean_lbl = self.sanitize_label(label)\n        af = AnalyticalFunction(fn, label=clean_lbl, color=color, width=width, style=style)')

# Sanitize in add_point_on_curve
text = text.replace('"label": label,', '"label": self.sanitize_label(label),')

# Sanitize in add_point
text = text.replace('def add_point(self, x: float, y: float, label: Optional[str] = None,',
                    'def add_point(self, x: float, y: float, label: Optional[str] = None,')

# Upgrade add_tangent_line with automatic axis closure
old_tangent = '''        y_contact = curve.eval(x_contact)
        slope = curve.derivative(x_contact)
        
        x1 = x_contact - span_left
        y1 = y_contact - slope * span_left
        x2 = x_contact + span_right
        y2 = y_contact + slope * span_right'''

new_tangent = '''        y_contact = curve.eval(x_contact)
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
        y2 = y_contact + slope * span_right'''

text = text.replace(old_tangent, new_tangent)

with open('analytical_geometry_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: Upgraded AnalyticalGeometryCompiler with auto axis-closure and math sanitizer!')
