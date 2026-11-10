with open('build_full_nje.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add sqrt-sign clamp
old_clamp = '''.katex .sqrt {{
      max-width: 100% !important;
      overflow: hidden !important;
    }}
    .katex .sqrt-sign svg {{
      max-width: 100% !important;
    }}
    .sol-card {{
      overflow: hidden;
    }}'''

new_clamp = '''.katex .sqrt {{
      max-width: 100% !important;
      overflow: hidden !important;
    }}
    .katex .sqrt-sign {{
      max-width: 150px !important;
      overflow: hidden !important;
    }}
    .katex .sqrt-sign svg {{
      max-width: 150px !important;
      overflow: hidden !important;
    }}
    .sol-card {{
      overflow: hidden;
    }}'''

text = text.replace(old_clamp, new_clamp)

with open('build_full_nje.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated sqrt-sign clamp in build_full_nje.py')
