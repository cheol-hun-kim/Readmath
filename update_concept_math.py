import os
import re

pts = []
for i in range(121):
    x = -2.15 + (4.3 * i / 120.0)
    y = x**3 - 3*x
    X = 250 + x * 70
    Y = 110 - y * 28
    pts.append(f'{X:.2f},{Y:.2f}')
polyline_pts = ' '.join(pts)

svg_cubic = f'''<svg viewBox="0 0 500 215" width="100%" height="205" xmlns="http://www.w3.org/2000/svg">
          <!-- Cartesian Axes -->
          <line x1="30" y1="110" x2="470" y2="110" stroke="#334155" stroke-width="1.2"/>
          <line x1="250" y1="200" x2="250" y2="15" stroke="#334155" stroke-width="1.2"/>
          <text x="475" y="114" fill="#080908" font-size="11" font-weight="bold" font-family="Pretendard, sans-serif">x</text>
          <text x="245" y="12" fill="#080908" font-size="11" font-weight="bold" font-family="Pretendard, sans-serif">y</text>
          <text x="238" y="124" fill="#64748B" font-size="10" font-family="serif">O</text>

          <!-- Exact Mathematical Cubic Curve y = x^3 - 3x -->
          <polyline fill="none" stroke="#080908" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" points="{polyline_pts}" />
          <text x="412" y="24" fill="#080908" font-size="11" font-weight="bold" font-family="Pretendard, sans-serif">y = f(x)</text>

          <!-- Horizontal Tangent Line at Local Max y = 2 (Y = 54) -->
          <line x1="90" y1="54" x2="430" y2="54" stroke="#DC2626" stroke-width="1.5" stroke-dasharray="4 3"/>
          <text x="435" y="58" fill="#DC2626" font-size="10" font-weight="bold" font-family="Pretendard, sans-serif">접선</text>

          <!-- 4 Equal Interval Projection Lines -->
          <!-- 1. 접점 t: x = -1 (X = 180, Y = 54) -->
          <line x1="180" y1="54" x2="180" y2="180" stroke="#94A3B8" stroke-width="1" stroke-dasharray="2 2"/>
          <circle cx="180" cy="54" r="3.5" fill="#DC2626"/>
          <text x="180" y="42" fill="#DC2626" font-size="10" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">접점 t</text>
          <text x="180" y="124" fill="#334155" font-size="10" text-anchor="middle" font-style="italic" font-family="serif">t</text>

          <!-- 2. 변곡점 x_i: x = 0 (X = 250, Y = 110) -->
          <circle cx="250" cy="110" r="3.5" fill="#080908"/>
          <text x="278" y="104" fill="#080908" font-size="10" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">변곡점</text>
          <text x="250" y="180" fill="#94A3B8" font-size="9" text-anchor="middle"></text>

          <!-- 3. 극소점: x = 1 (X = 320, Y = 166) -->
          <line x1="320" y1="166" x2="320" y2="180" stroke="#94A3B8" stroke-width="1" stroke-dasharray="2 2"/>
          <circle cx="320" cy="166" r="3.5" fill="#080908"/>
          <text x="320" y="156" fill="#080908" font-size="10" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">극소</text>

          <!-- 4. 교점 α: x = 2 (X = 390, Y = 54) -->
          <line x1="390" y1="54" x2="390" y2="180" stroke="#94A3B8" stroke-width="1" stroke-dasharray="2 2"/>
          <circle cx="390" cy="54" r="3.5" fill="#DC2626"/>
          <text x="390" y="42" fill="#DC2626" font-size="10" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">교점 α</text>
          <text x="390" y="124" fill="#334155" font-size="10" text-anchor="middle" font-style="italic" font-family="serif">α</text>

          <!-- Mathematical 1 : 1 : 1 Equal Dimension Brackets -->
          <line x1="180" y1="178" x2="250" y2="178" stroke="#080908" stroke-width="1.2"/>
          <line x1="180" y1="174" x2="180" y2="182" stroke="#080908" stroke-width="1.2"/>
          <text x="215" y="193" fill="#080908" font-size="9.5" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">비율 1</text>

          <line x1="250" y1="178" x2="320" y2="178" stroke="#080908" stroke-width="1.2"/>
          <line x1="250" y1="174" x2="250" y2="182" stroke="#080908" stroke-width="1.2"/>
          <text x="285" y="193" fill="#080908" font-size="9.5" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">비율 1</text>

          <line x1="320" y1="178" x2="390" y2="178" stroke="#080908" stroke-width="1.2"/>
          <line x1="320" y1="174" x2="320" y2="182" stroke="#080908" stroke-width="1.2"/>
          <line x1="390" y1="174" x2="390" y2="182" stroke="#080908" stroke-width="1.2"/>
          <text x="355" y="193" fill="#080908" font-size="9.5" font-weight="bold" text-anchor="middle" font-family="Pretendard, sans-serif">비율 1</text>
        </svg>'''

target_path = r'C:\Users\1286o\.gemini\antigravity\scratch\rootmath\templates\concept_book.html'
with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the cubic svg
new_content = re.sub(r'<svg viewBox="0 0 460 160"[\s\S]*?</svg>', svg_cubic, content)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('✓ Successfully replaced cubic SVG in concept_book.html with exact coordinates!')
