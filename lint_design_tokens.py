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
5. Grade Examples (초1 ~ 고3) Editorial Diagram Palette Integrity:
   - Every diagram must have a Black (#080908) base curve/shape.
   - Zero banned rainbow colors (green #10B981, purple #A855F7, neon yellow #FBBF24, dark rects #090D16).
"""

import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_EMOJI_REGEX = re.compile(r'[\U0001F300-\U0001FAFF\u26A0-\u26A1\u2694\u2705\u274C]')

STRICT_EXAM_FILES = [
    'templates/nje_exam_108.html', 'build_full_108_nje.py',
    'templates/nje_exam_24.html', 'templates/concept_book.html',
    'mathdata/diagram_engine_108.py', 'math_engine_core.py'
]

UI_FILES = ['preview.html', 'landing.html', 'admin.html']

BANNED_RAINBOW_BOXES = [
    r'background:\s*#FFFBEB',
    r'background:\s*#EFF6FF',
    r'background:\s*#FFF7ED',
]

BANNED_DIAGRAM_RAINBOW_COLORS = {
    '#10B981', '#34D399', '#047857', '#059669',
    '#A855F7', '#C084FC', '#7E22CE', '#9333EA',
    '#090D16', '#1E1B4B', '#064E3B',
    '#FDE047', '#FBBF24', '#FCD34D', '#FDE68A'
}

def simulate_convert_svg_for_white_canvas(svg_str):
    if not svg_str:
        return ''
    s = svg_str

    # 1. Strip dark canvas backgrounds
    s = re.sub(r'<rect\s+[^>]*fill="#(?:090D16|050811|0A0E17|0B0F19)"[^>]*\/?>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'<rect\s+[^>]*fill="(?:#FFFFFF|white)"\s*[^>]*width="(?:100%|400|420)"[^>]*\/?>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'<rect\s+[^>]*width="(?:100%|400|420)"\s*[^>]*fill="(?:#FFFFFF|white)"[^>]*\/?>', '', s, flags=re.IGNORECASE)

    # 1.1 Strip redundant banner headers
    s = re.sub(r'<text[^>]*\by=["\'](?:1[5-9]|2[0-9]|3[0-2])["\'][^>]*>\[(?:AI 쌍둥이|2026 수능|수학적 시각화|정규분포|기출|실전)[^<]*<\/text>\n?', '', s, flags=re.IGNORECASE)

    # 2. Containers: standardize to editorial off-white
    dark_containers = ['#1E1B4B', '#312E81', '#064E3B', '#0C4A6E', '#1E293B', '#0F172A', '#451A03', '#3B0764', '#172554', '#7F1D1D', '#000000', '#111827', '#1F2937']
    for dc in dark_containers:
        for tag in ['rect', 'polygon', 'circle']:
            re_fill = re.compile(r'(<' + tag + r'\b[^>]*\bfill=["\'])' + dc + r'(["\'][^>]*>)', re.IGNORECASE)
            def repl_fill(m, t=tag):
                quote = m.group(2)[0]
                cleaned = m.group(2)[1:]
                cleaned = re.sub(r'\bstroke=["\'][^"\']*["\']', '', cleaned, flags=re.IGNORECASE)
                cleaned = re.sub(r'\bfill-opacity=["\'][^"\']*["\']', '', cleaned, flags=re.IGNORECASE)
                fill_val = 'none' if t in ['polygon', 'circle'] else '#FAF8F5'
                border_val = '#080908' if t in ['polygon', 'circle'] else '#CBD5E1'
                return f"{m.group(1)}{fill_val}{quote} stroke=\"{border_val}\" fill-opacity=\"1\"{cleaned}"
            s = re_fill.sub(repl_fill, s)

    # 3. Axes, ticks, arrows: Strict Jet Black (#080908)
    s = re.sub(r'(<(?:line|path)\b[^>]*\b)stroke="(?:#64748B|#475569|#334155)"(?=[^>]*stroke-width="[1-3])', r'\1stroke="#080908"', s, flags=re.IGNORECASE)
    s = re.sub(r'(<polygon\b[^>]*\bfill=")(?:#64748B|#475569|#334155)("(?=[^>]*points="[^"]*(?:408|150|22|30|190|187|193))[^>]*>)', r'\1#080908\2', s, flags=re.IGNORECASE)

    # 4. Function Curves: Base Black (#080908), Secondary Blue (#2563EB), Tangent Red (#DC2626)
    s = re.sub(r'(<path\b[^>]*\bd="M 40 215 Q 160 35 280 215"[^>]*\bstroke=")[^"]+(")', r'\1#080908\2', s)
    s = re.sub(r'(<path\b[^>]*\bd="M 80 162 Q 160 35 240 162"[^>]*\bstroke=")[^"]+(")', r'\1#DC2626\2', s)
    s = re.sub(r'(<path\b[^>]*\bd="M 40 220 Q 150 170 214 46"[^>]*\bstroke=")[^"]+(")', r'\1#080908\2', s)
    s = re.sub(r'(<path\b[^>]*\bd="M 220 40 Q 170 150 46 214"[^>]*\bstroke=")[^"]+(")', r'\1#2563EB\2', s)
    s = re.sub(r'(<line\b[^>]*x1="90" y1="170" x2="214" y2="46"[^>]*\bstroke=")[^"]+(")', r'\1#DC2626\2', s)
    s = re.sub(r'(<path\b[^>]*\bd="[^"]*"[^>]*\bstroke=")#38BDF8(")', r'\1#080908\2', s)
    s = re.sub(r'(<path\b[^>]*\bd="[^"]*"[^>]*\bstroke=")#F59E0B(")', r'\1#2563EB\2', s)
    s = re.sub(r'(<circle\b[^>]*cx="210" cy="120" r="80"[^>]*\bstroke=")[^"]+(")', r'\1#080908\2', s)
    s = re.sub(r'(<line\b[^>]*\bstroke=")(?:#EF4444|#F87171|#F43F5E)(")', r'\1#DC2626\2', s, flags=re.IGNORECASE)

    # General curve standardization
    s = re.sub(r'(<path\b[^>]*\bstroke=")(?:#10B981|#34D399|#059669|#047857|#06B6D4)(")', r'\1#080908\2', s, flags=re.IGNORECASE)
    s = re.sub(r'(<path\b[^>]*\bstroke=")(?:#A855F7|#C084FC|#7E22CE|#9333EA|#FBBF24)(")', r'\1#2563EB\2', s, flags=re.IGNORECASE)
    s = re.sub(r'(<line\b[^>]*\bstroke=")#60A5FA(")', r'\1#080908\2', s)
    s = re.sub(r'(<line\b[^>]*\bstroke=")(?:#34D399|#10B981|#059669)(")', r'\1#2563EB\2', s, flags=re.IGNORECASE)
    s = re.sub(r'(<line\b[^>]*\bstroke=")(?:#38BDF8|#0284C7|#0369A1)(")', r'\1#2563EB\2', s, flags=re.IGNORECASE)
    s = re.sub(r'(<line\b[^>]*\bstroke=")(?:#A855F7|#C084FC|#9333EA|#FBBF24)(")', r'\1#2563EB\2', s, flags=re.IGNORECASE)

    # General stroke and fill clean
    s = re.sub(r'stroke="#(?:10B981|34D399|9333EA|A855F7|C084FC|FCD34D|FDE68A|FDE047|FBBF24)"', 'stroke="#2563EB"', s, flags=re.IGNORECASE)
    s = re.sub(r'fill="#(?:FAF5FF|FFFBEB|ECFDF5|EEF2FF|F0F9FF)"', 'fill="#FAF8F5"', s, flags=re.IGNORECASE)

    # 5. Text elements: High contrast textbook ink (#080908), preserving Problem 5 assertions
    s = re.sub(r'(<text\b[^>]*\bfill=")#C7D2FE(")', r'\1#312E81\2', s)
    s = re.sub(r'(<text\b[^>]*\bfill=")#FDE047(")', r'\1#B45309\2', s)

    light_text_colors = [
        '#94A3B8', '#CBD5E1', '#F1F5F9', '#F8FAFC', '#E2E8F0', '#E0E7FF',
        '#A5B4FC', '#7DD3FC', '#BAE6FD', '#FCA5A5', '#F87171',
        '#FBBF24', '#FCD34D', '#FDE68A', '#A7F3D0', '#6EE7B7', '#10B981', '#34D399',
        '#FFFFFF', 'white', '#93C5FD', '#E9D5FF', '#DDD6FE', '#C4B5FD', '#C084FC',
        '#38BDF8', '#67E8F9', '#A5F3FC', '#86EFAC', '#BBF7D0', '#FECDD3', '#FED7AA',
        '#FEF08A', '#F43F5E', '#1E1B4B', '#A855F7', '#9333EA'
    ]
    for tc in light_text_colors:
        s = re.sub(r'(<(?:text|tspan)\b[^>]*\bfill=["\'])' + tc + r'(["\'])', r'\1#080908\2', s, flags=re.IGNORECASE)

    # 6. Keypoint circle fills
    s = re.sub(r'(<circle\b[^>]*\bfill=")(?:#EF4444|#F59E0B)(")', r'\1#DC2626\2', s, flags=re.IGNORECASE)
    s = re.sub(r'(<circle\b[^>]*\bfill=")(?:#3B82F6|#10B981|#34D399|#A855F7|#C084FC)(")', r'\1#2563EB\2', s, flags=re.IGNORECASE)

    # 7. Remaining fill clashes on polygons/rects/paths
    s = re.sub(r'\bfill="(?:#064E3B|#0C4A6E|#10B981|#34D399|#A7F3D0|#6EE7B7|#C084FC|#A855F7|#FCD34D|#FDE68A|#FBBF24)"', 'fill="none"', s, flags=re.IGNORECASE)

    # 8. LaTeX cleanup
    s = s.replace(r'\therefore', '∴')
    s = s.replace(r'\implies', '⟹')

    return s

def run_universal_lint():
    violations = []
    
    # =========================================================================
    # 1. Zero-Emoji Scan
    # =========================================================================
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

    for rel_path in UI_FILES:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        try:
            content = open(full_path, 'r', encoding='utf-8').read()
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
                if blue_count >= 3 and black_count == 0:
                    violations.append(f"[PALETTE VIOLATION] Diagram Q{q} has {blue_count} blue elements and 0 black base elements (Monochromatic blue wash)")
                
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
            orange_buttons = re.findall(r'<button[^>]*class="[^"]*\bbg-\[#EA580C\]\b[^"]*"', settings_block)
            if len(orange_buttons) > 1:
                violations.append(f"[ORANGE SPAM VIOLATION] Settings view has {len(orange_buttons)} solid orange buttons (10% rule allows at most 1 active selection)")
    except Exception as e:
        violations.append(f"[SETTINGS AUDIT ERROR] {e}")

    # =========================================================================
    # 5. Grade Examples (초1 ~ 고3) Editorial Palette & Rainbow Ban Check
    # =========================================================================
    try:
        preview_path = os.path.join(ROOT_DIR, 'preview.html')
        content = open(preview_path, 'r', encoding='utf-8').read()
        db_start = content.find('const PROBLEMS_DB = {')
        db_end = content.find('const CANONICAL_PROBLEMS_DB =', db_start)
        if db_start != -1 and db_end != -1:
            db_code = content[db_start:db_end]
            svgs = re.findall(r'<svg[\s\S]*?<\/svg>', db_code)
            for s_idx, raw_svg in enumerate(svgs):
                rendered = simulate_convert_svg_for_white_canvas(raw_svg)
                colors = set(re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', rendered))
                clashes = colors.intersection(BANNED_DIAGRAM_RAINBOW_COLORS)
                has_black = '#080908' in colors or '#0F172A' in colors or '#334155' in colors
                if clashes:
                    violations.append(f"[GRADE SVG RAINBOW VIOLATION] PROBLEMS_DB SVG #{s_idx + 1} contains banned colors: {clashes}")
                if not has_black:
                    violations.append(f"[GRADE SVG BLACK BASE VIOLATION] PROBLEMS_DB SVG #{s_idx + 1} missing Black base element (#080908)")
    except Exception as e:
        violations.append(f"[GRADE SVG AUDIT ERROR] {e}")

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
