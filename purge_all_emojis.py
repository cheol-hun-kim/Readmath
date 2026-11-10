import re

# 1. Update build_full_nje.py
with open('build_full_nje.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace emojis with clean CSAT editorial titles
text = text.replace('📖 ReadMath', 'ReadMath')
text = text.replace('⚡ 동일 레시피 핵심 발상', '동일 레시피 핵심 발상')
text = text.replace('📊 2025 수능 킬러', '2025 수능 킬러')
text = text.replace('● 수험생이 펜을 멈춘', '[수험생이 펜을 멈춘')
text = text.replace('진단)', '진단]')
text = text.replace('▶ 단계별 사고 흐름 해금 풀이', '[단계별 사고 흐름 해금 풀이]')

# Add KaTeX sqrt clamp to CSS to prevent stretching radical lines
katex_sqrt_clamp = '''
    /* KaTeX Radical & SVG Clamp Guard */
    .katex .sqrt {
      max-width: 100% !important;
      overflow: hidden !important;
    }
    .katex .sqrt-sign svg {
      max-width: 100% !important;
    }
    .sol-card {
      overflow: hidden;
    }
'''

if '/* KaTeX Radical & SVG Clamp Guard */' not in text:
    text = text.replace('.katex {', katex_sqrt_clamp + '\n    .katex {')

with open('build_full_nje.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: Purged emojis and added KaTeX sqrt clamp in build_full_nje.py')

# 2. Update generate_universal_diagrams.py
with open('generate_universal_diagrams.py', 'r', encoding='utf-8') as f:
    diag_code = f.read()

# Replace arrow emoji with clean ASCII or SVG arrow
diag_code = diag_code.replace('원점 확대 ➔', '원점 확대 ->')

with open('generate_universal_diagrams.py', 'w', encoding='utf-8') as f:
    f.write(diag_code)

print('SUCCESS: Purged emojis from generate_universal_diagrams.py')
