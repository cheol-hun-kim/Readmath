with open('build_full_nje.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix single braces in katex_sqrt_clamp inside f-string
old_clamp = '''.katex .sqrt {
      max-width: 100% !important;
      overflow: hidden !important;
    }
    .katex .sqrt-sign svg {
      max-width: 100% !important;
    }
    .sol-card {
      overflow: hidden;
    }'''

new_clamp = '''.katex .sqrt {{
      max-width: 100% !important;
      overflow: hidden !important;
    }}
    .katex .sqrt-sign svg {{
      max-width: 100% !important;
    }}
    .sol-card {{
      overflow: hidden;
    }}'''

text = text.replace(old_clamp, new_clamp)

with open('build_full_nje.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: Fixed f-string double curly braces in build_full_nje.py')
