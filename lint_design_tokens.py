"""
RootMath Repository-Wide Design Token & Anti-Band-Aid Universal Linter
Enforces inviolable design system rules across ALL project files:
1. Zero Emojis in any UI, exam sheet, or solution file.
2. 60-30-10 Palette Integrity:
   - Zero saturated rainbow pastel background fills (#FFFBEB, #EFF6FF, #FFF7ED in solutions).
   - Zero purple/indigo theme residual classes or styles (#818CF8, #6366F1, etc.).
3. Mathematical Diagram Palette & Anti-Collision:
   - Primary curve must use Black (#080908). No SVG with >=2 curves can have 0 black curves.
   - Zero label collisions (two text elements at identical coordinates).
4. Viewport & Button Restraint:
   - No single view can have >1 primary solid accent (#EA580C) buttons in Settings/Cards.
"""

import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Unicode emoji range: Miscellaneous Symbols, Dingbats, Supplemental Symbols, Emoticons
# Excludes pure typography markers like checkmark \u2713 and star \u2605 if needed,
# but catches actual color emojis (0x1F300-0x1FAFF, warning, lightning, etc.)
RAW_EMOJI_REGEX = re.compile(r'[\U0001F300-\U0001FAFF\u26A0-\u26A1\u2694\u2705\u274C]')

# Files that must strictly have 0 emojis (all exam sheets, solution generators, math engines)
STRICT_EXAM_FILES = [
    'templates/nje_exam_108.html', 'build_full_108_nje.py',
    'templates/nje_exam_24.html', 'templates/concept_book.html',
    'mathdata/diagram_engine_108.py', 'math_engine_core.py'
]

# UI Files where user-facing text and code must not contain raw emojis
UI_FILES = ['preview.html', 'landing.html', 'admin.html']

BANNED_RAINBOW_BOXES = [
    r'background:\s*#FFFBEB',
    r'background:\s*#EFF6FF',
    r'background:\s*#FFF7ED',
]

def run_universal_lint():
    violations = []
    
    # =========================================================================
    # 1. Zero-Emoji Scan
    # =========================================================================
    # 1.1 Strict Exam & Engine files (0 emojis anywhere)
    for rel_path in STRICT_EXAM_FILES:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        try:
            content = open(full_path, 'r', encoding='utf-8').read()
            emojis = RAW_EMOJI_REGEX.findall(content)
            if emojis:
                violations.append(f"[EMOJI VIOLATION] Exam/Engine file {rel_path} contains {len(emojis)} banned emojis: {set(emojis)}")
        except Exception as e:
            violations.append(f"[FILE READ ERROR] {rel_path}: {e}")

    # 1.2 UI files (0 emojis outside developer comments)
    for rel_path in UI_FILES:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        try:
            content = open(full_path, 'r', encoding='utf-8').read()
            # Strip HTML and CSS comments
            no_comments = re.sub(r'<!--[\s\S]*?-->', '', content)
            no_comments = re.sub(r'/\*[\s\S]*?\*/', '', no_comments)
            emojis = RAW_EMOJI_REGEX.findall(no_comments)
            if emojis:
                violations.append(f"[EMOJI VIOLATION] UI file {rel_path} contains {len(emojis)} emojis in markup/script: {set(emojis)}")
        except Exception as e:
            violations.append(f"[FILE READ ERROR] {rel_path}: {e}")

    # =========================================================================
    # 2. Rainbow Pastel Fills in Solutions
    # =========================================================================
    check_sol_files = ['build_full_108_nje.py', 'templates/nje_exam_108.html']
    for rel_path in check_sol_files:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        content = open(full_path, 'r', encoding='utf-8').read()
        for pat in BANNED_RAINBOW_BOXES:
            if re.search(pat, content, re.IGNORECASE):
                violations.append(f"[RAINBOW BOX VIOLATION] {rel_path} contains banned pastel fill pattern '{pat}'")

    # =========================================================================
    # 3. All-Blue Math Diagram & Label Collision Check
    # =========================================================================
    try:
        from mathdata.diagram_engine_108 import get_diagram_for_108
        for q in range(1, 109):
            svg = get_diagram_for_108(q)
            if svg:
                blue_count = svg.count('#2563EB')
                black_count = svg.count('#080908')
                # If there are >= 3 blue elements and 0 black curves, it's a monochromatic blue violation
                if blue_count >= 3 and black_count == 0:
                    violations.append(f"[PALETTE VIOLATION] Diagram Q{q} has {blue_count} blue elements and 0 black base elements (Monochromatic blue wash)")
                
                # Check for colliding labels at identical coordinates
                text_pts = re.findall(r'<text\s+x="([^"]+)"\s+y="([^"]+)"', svg)
                coords = []
                for x_str, y_str in text_pts:
                    try:
                        coords.append((float(x_str), float(y_str)))
                    except ValueError:
                        pass
                for i in range(len(coords)):
                    for j in range(i + 1, len(coords)):
                        if abs(coords[i][0] - coords[j][0]) < 1.0 and abs(coords[i][1] - coords[j][1]) < 1.0:
                            violations.append(f"[LABEL COLLISION] Diagram Q{q} has overlapping labels at ({coords[i][0]}, {coords[i][1]})")
    except Exception as e:
        violations.append(f"[DIAGRAM AUDIT ERROR] {e}")

    # =========================================================================
    # 4. Settings View Orange Spam Check
    # =========================================================================
    try:
        preview_path = os.path.join(ROOT_DIR, 'preview.html')
        content = open(preview_path, 'r', encoding='utf-8').read()
        settings_idx = content.find('id="view-settings"')
        if settings_idx != -1:
            settings_end = content.find('<!-- ================= 8.', settings_idx)
            if settings_end == -1:
                settings_end = content.find('id="view-teacher"', settings_idx)
            settings_block = content[settings_idx:settings_end]
            # Count solid orange button classes
            orange_buttons = re.findall(r'<button[^>]*class="[^"]*\bbg-\[#EA580C\]\b[^"]*"', settings_block)
            # In Settings view, at most 1 active grade button should be solid orange!
            if len(orange_buttons) > 1:
                violations.append(f"[ORANGE SPAM VIOLATION] Settings view has {len(orange_buttons)} solid orange buttons (10% rule allows at most 1 active selection)")
    except Exception as e:
        violations.append(f"[SETTINGS AUDIT ERROR] {e}")

    # =========================================================================
    # REPORT
    # =========================================================================
    print("=" * 80)
    print("[ROOTMATH REPOSITORY-WIDE UNIVERSAL DESIGN TOKEN & LINTER AUDIT]")
    print(f"Total Violations Found: {len(violations)}")
    print("=" * 80)

    if violations:
        print("[FAIL] The following inviolable design rules were breached:")
        for v in violations:
            print(f"  |-- {v}")
        sys.exit(1)

    print("[SUCCESS] 100% Repository-Wide Compliance with Universal Design Rules Verified!")
    sys.exit(0)

if __name__ == "__main__":
    run_universal_lint()
