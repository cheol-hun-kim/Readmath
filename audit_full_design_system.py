import os
import re

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

TARGET_FILES = [
    'landing.html',
    'preview.html',
    'admin.html',
    'grant_proposal.html',
    'public/privacy.html',
    'public/terms.html',
    'templates/concept_book.html',
    'templates/nje_exam_24.html',
    'templates/nje_exam_108.html'
]

print("=" * 75)
print("[READMATH FULL SYSTEM DESIGN RULES AUDIT]")
print("=" * 75)

violations = {f: [] for f in TARGET_FILES}

for rel_path in TARGET_FILES:
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        continue
        
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip style and script tags for markup audit
    markup_only = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', content, flags=re.IGNORECASE)
    markup_only = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', markup_only, flags=re.IGNORECASE)

    # Rule 1: Zero Purple/Indigo Clashes in UI
    purple_matches = re.findall(r'class="[^"]*\b(bg-indigo-\d+|bg-purple-\d+|text-indigo-\d+|text-purple-\d+|border-indigo-\d+|border-purple-\d+)\b[^"]*"', markup_only)
    if purple_matches:
        violations[rel_path].append(f"Forbidden Purple/Indigo colors found ({len(purple_matches)} occurrences): {set(purple_matches)}")

    # Rule 2: Table Cell display:flex Anti-pattern
    td_flex_matches = re.findall(r'<td[^>]*class="[^"]*\bflex\b[^"]*"', markup_only)
    if td_flex_matches:
        violations[rel_path].append(f"Table cell flex anti-pattern found ({len(td_flex_matches)} occurrences): Breaks vertical-align middle")

    # Rule 3: Orange CTA Button must enforce pure white text
    orange_btn_matches = re.finditer(r'<button[^>]*class="[^"]*(?:bg-\[#EA580C\]|bg-orange-600)[^"]*"[^>]*>([\s\S]*?)<\/button>', markup_only)
    for m in orange_btn_matches:
        btn_tag = m.group(0)
        if 'text-white' not in btn_tag and '#FFFFFF' not in btn_tag and 'var(--text-on-accent)' not in btn_tag:
            violations[rel_path].append(f"Orange button without strict white text: {btn_tag[:60]}...")

    # Rule 4: Check for harsh yellow/amber text in markup (Visual noise scanner)
    amber_text_matches = re.findall(r'class="[^"]*\b(text-amber-300|text-amber-400|text-yellow-300|text-yellow-400)\b[^"]*"', markup_only)
    if amber_text_matches:
        violations[rel_path].append(f"Harsh yellow/amber visual noise text found ({len(amber_text_matches)} occurrences): {set(amber_text_matches)}")

    # Rule 5: Check for top-corner page number remnant in PDF templates
    if 'nje_exam' in rel_path or 'concept_book' in rel_path:
        if 'csat-top-page-num' in markup_only:
            violations[rel_path].append("Rogue .csat-top-page-num remnants found")
        if '홀수형' in markup_only:
            violations[rel_path].append("Rogue '홀수형' badge found")

total_violations = 0
for f, v_list in violations.items():
    print(f"\n[{f}]")
    if not v_list:
        print("  [PASS] 100% CLEAN - No design rule violations detected!")
    else:
        for v in v_list:
            total_violations += 1
            print(f"  [FAIL] VIOLATION: {v}")

print("\n" + "=" * 75)
print(f"TOTAL SYSTEMIC DESIGN VIOLATIONS: {total_violations}")
print("=" * 75)
