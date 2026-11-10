import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

TARGET_FILES = [
    'preview.html',
    'landing.html',
    'admin.html',
    'grant_proposal.html',
    'public/privacy.html',
    'public/terms.html',
    'templates/concept_book.html',
    'templates/nje_exam_24.html'
]

print("=" * 80)
print("[READMATH COMPREHENSIVE MULTI-FILE DESIGN & TYPOGRAPHY SYSTEM AUDIT]")
print("=" * 80)

report = {}

for rel_path in TARGET_FILES:
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        continue

    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    markup = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', content, flags=re.IGNORECASE)
    markup = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', markup, flags=re.IGNORECASE)

    issues = []

    # 1. Indigo / Purple / Violet
    bad_colors = set(re.findall(r'\b(?:bg|text|border)-(?:indigo|purple|violet)-\d+\b', markup))
    if bad_colors:
        issues.append(f"Forbidden Purple/Indigo/Violet classes: {bad_colors}")

    # 2. Harsh yellow/amber text
    harsh_amber = set(re.findall(r'\btext-(?:amber|yellow)-[34]00\b', markup))
    if harsh_amber:
        issues.append(f"Harsh amber/yellow text classes: {harsh_amber}")

    # 3. Table cell flex
    td_flex = re.findall(r'<t[dh][^>]*class="[^"]*\bflex\b[^"]*"[^>]*>', markup)
    if td_flex:
        issues.append(f"Table cell flex anti-pattern ({len(td_flex)} occurrences)")

    # 4. Orange button white text
    orange_btn_tags = re.findall(r'<button[^>]*class="[^"]*(?:bg-\[#EA580C\]|bg-orange-600)[^"]*"[^>]*>', markup)
    bad_orange_btns = [b for b in orange_btn_tags if 'text-white' not in b and '#FFFFFF' not in b and 'var(--text-on-accent)' not in b]
    if bad_orange_btns:
        issues.append(f"Orange button without pure white text ({len(bad_orange_btns)} occurrences)")

    # 5. Headings without break-keep
    headings = re.findall(r'<h[1-4][^>]*>', markup)
    headings_no_break = [h for h in headings if 'break-keep' not in h and 'keep-all' not in h]
    if headings_no_break:
        issues.append(f"Headings missing break-keep ({len(headings_no_break)} / {len(headings)})")

    # 6. Buttons or links without break-keep
    btn_links = re.findall(r'<(?:button|a)[^>]*class="[^"]*(?:btn|py-|px-|rounded-)[^"]*"[^>]*>', markup)
    btn_links_no_break = [b for b in btn_links if 'break-keep' not in b and 'keep-all' not in b and 'whitespace-nowrap' not in b]
    if len(btn_links_no_break) > 5:
        issues.append(f"Buttons/Links missing break-keep/nowrap ({len(btn_links_no_break)} occurrences)")

    # 7. Non-breaking spaces for key units in Korean text
    # e.g., '1순위 클리닉' -> should be '1순위&nbsp;클리닉'
    orphan_units = re.findall(r'(\d+(?:순위|단계|제|문항|개|분|점|%)\s+[가-힣]+)', markup)
    if orphan_units:
        issues.append(f"Potential separated unit/number pairs (consider &nbsp;): {len(orphan_units)} found (samples: {list(set(orphan_units))[:3]})")

    report[rel_path] = issues

for path, issues in report.items():
    print(f"\n[{path}]")
    if not issues:
        print("  [PASS] 100% CLEAN")
    else:
        for iss in issues:
            print(f"  [ISSUE] {iss}")

print("\n" + "=" * 80)
