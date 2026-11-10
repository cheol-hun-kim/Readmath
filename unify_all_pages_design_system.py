import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

TYPOGRAPHY_ARMOR_CSS = """
/* ==========================================================================
   GLOBAL SYSTEMIC TYPOGRAPHY & ORPHAN WORD DEFENSE (Systemic Charter Art. 3)
   ========================================================================== */
h1, h2, h3, h4, h5, h6,
.card-title, .headline, [role="heading"],
button, .btn, [role="button"],
.badge, .pill,
label, th {
  word-break: keep-all !important;
  overflow-wrap: break-word !important;
}

h1, h2, h3, h4, .balance-text {
  text-wrap: balance;
}

p, .description, .explanation, .pretty-text {
  word-break: keep-all;
  overflow-wrap: break-word;
  text-wrap: pretty;
}
"""

TARGETS = [
    'preview.html',
    'landing.html',
    'admin.html',
    'grant_proposal.html',
    'public/privacy.html',
    'public/terms.html'
]

# 1. Clean and transform grant_proposal.html
gp_path = os.path.join(ROOT_DIR, 'grant_proposal.html')
if os.path.exists(gp_path):
    with open(gp_path, 'r', encoding='utf-8') as f:
        gp_text = f.read()
    
    # Replace Indigo/Purple with ReadMath Slate/Terracotta
    gp_text = re.sub(r'\bbg-indigo-600\b', 'bg-[#EA580C]', gp_text)
    gp_text = re.sub(r'\bbg-indigo-700\b', 'bg-[#C2410C]', gp_text)
    gp_text = re.sub(r'\bbg-indigo-950\b', 'bg-slate-900', gp_text)
    gp_text = re.sub(r'\bbg-indigo-50\b', 'bg-orange-50', gp_text)
    gp_text = re.sub(r'\bfrom-indigo-900\b', 'from-slate-950', gp_text)
    gp_text = re.sub(r'\bvia-indigo-950\b', 'via-slate-900', gp_text)
    
    gp_text = re.sub(r'\btext-indigo-400\b', 'text-[#EA580C]', gp_text)
    gp_text = re.sub(r'\btext-indigo-300\b', 'text-stone-300', gp_text)
    gp_text = re.sub(r'\btext-indigo-200\b', 'text-stone-400', gp_text)
    gp_text = re.sub(r'\btext-indigo-100\b', 'text-stone-200', gp_text)
    gp_text = re.sub(r'\btext-indigo-700\b', 'text-[#C2410C]', gp_text)
    gp_text = re.sub(r'\btext-indigo-900\b', 'text-slate-900', gp_text)
    gp_text = re.sub(r'\btext-indigo-950\b', 'text-slate-950', gp_text)
    
    gp_text = re.sub(r'\bborder-indigo-500\b', 'border-[#EA580C]', gp_text)
    gp_text = re.sub(r'\bborder-indigo-600\b', 'border-[#EA580C]', gp_text)
    gp_text = re.sub(r'\bborder-indigo-700\b', 'border-slate-800', gp_text)
    gp_text = re.sub(r'\bborder-indigo-200\b', 'border-orange-200', gp_text)
    
    # Replace text-amber-400 in grant proposal
    gp_text = re.sub(r'\btext-amber-400\b', 'text-white font-extrabold', gp_text)
    
    with open(gp_path, 'w', encoding='utf-8') as f:
        f.write(gp_text)
    print("✓ Harmonized grant_proposal.html to ReadMath design system!")

# 2. Clean privacy.html and terms.html
for p_rel in ['public/privacy.html', 'public/terms.html']:
    p_path = os.path.join(ROOT_DIR, p_rel)
    if os.path.exists(p_path):
        with open(p_path, 'r', encoding='utf-8') as f:
            t = f.read()
        t = re.sub(r'\btext-indigo-400\b', 'text-[#EA580C]', t)
        with open(p_path, 'w', encoding='utf-8') as f:
            f.write(t)
        print(f"✓ Harmonized {p_rel} brand colors!")

# 3. Inject Global Typography Armor into all TARGETS
for rel_path in TARGETS:
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        continue
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already injected
    if 'GLOBAL SYSTEMIC TYPOGRAPHY & ORPHAN WORD DEFENSE' not in content:
        # Find </style>
        if '</style>' in content:
            idx = content.find('</style>')
            content = content[:idx] + TYPOGRAPHY_ARMOR_CSS + "\n" + content[idx:]
        elif '</head>' in content:
            idx = content.find('</head>')
            content = content[:idx] + f"<style>{TYPOGRAPHY_ARMOR_CSS}</style>\n" + content[idx:]
        
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Injected Global Typography & Orphan Word Armor into {rel_path}")
    else:
        print(f"- Armor already present in {rel_path}")

# 4. Enforce &nbsp; on separated unit/number pairs
# e.g., '1순위 클리닉' -> '1순위&nbsp;클리닉'
REPLACEMENTS = [
    (r'(\b\d+순위)\s+(클리닉)', r'\1&nbsp;\2'),
    (r'(\b\d+단계)\s+(대화|추가|해설|풀이|진단|심층)', r'\1&nbsp;\2'),
    (r'(\b\d+%)\s+(할인|보존|일치|성취|동일)', r'\1&nbsp;\2'),
    (r'(\b\d+초)\s+(컷)', r'\1&nbsp;\2'),
    (r'(\b\d+문항)\s+(수록|완비|출제)', r'\1&nbsp;\2'),
    (r'(\b\d+제)\s+(N제|변형|실전|모음)', r'\1&nbsp;\2')
]

for rel_path in TARGETS:
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        continue
    with open(abs_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    
    for pat, rep in REPLACEMENTS:
        txt = re.sub(pat, rep, txt)
        
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    print(f"✓ Locked unit non-breaking spaces in {rel_path}")

print("\nAll target files harmonized successfully!")
