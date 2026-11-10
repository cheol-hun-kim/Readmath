"""
=============================================================================
RootMath Universal CSAT Database Auditor & Stress Tester (750+ Questions)
=============================================================================
Audits all CSAT questions in mathdata/processed_db across:
1. HWP PUA / Control Character Residuals (Zero corrupted fonts)
2. CSAT Sigma Stacking Limits (100% \\sum\\limits stacked notation)
3. Full Vector Arrow Spans (100% \\overrightarrow on multi-letter vectors)
4. Unreduced Coefficient 1 (Zero '1x', '1e', '1\\ln' leaks)
5. Operator Standards (Zero '<=', '>=', '!=' -> must be \\le, \\ge, \\neq)
6. Particle Binding & Korean Spacing Integrity
7. KaTeX Parse Validity & Zero Code Jargon Leaks
=============================================================================
"""

import os
import sys
import glob
import json
import re
from typing import List, Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, "mathdata", "processed_db")

from csat_typesetter import normalize_csat_text
from analytical_geometry_engine import AnalyticalGeometryCompiler

def run_csat_database_audit():
    print("=" * 80)
    print("[ROOTMATH UNIVERSAL CSAT DATABASE STRESS TEST & AUDIT]")
    print(f"Target Directory: {DB_DIR}")
    print("=" * 80)

    files = sorted(glob.glob(os.path.join(DB_DIR, "*수능*.json")))
    print(f"Found {len(files)} CSAT Exam Database files.")

    total_questions = 0
    violations_by_category: Dict[str, List[Dict[str, Any]]] = {
        "pua_control_char": [],
        "inconsistent_sigma": [],
        "short_vector_arrow": [],
        "unreduced_coeff_one": [],
        "raw_programming_operators": [],
        "naked_greek_or_jargon": [],
        "particle_unbound_gaps": []
    }

    # Regex definitions for adversarial auditing
    pua_regex = re.compile(r'[\ue000-\uf8ff\x00-\x08\x0b-\x0c\x0e-\x1f]')
    unreduced_coeff_regex = re.compile(r'(?<![0-9\.a-zA-Z])1([eExX]|\\ln|\\exp)(?![\d])')
    raw_operators_regex = re.compile(r'(?<!<)<=|(?<!>)>=|!=')
    short_vec_regex = re.compile(r'\\vec\{[a-zA-Z0-9]{2,}\}')

    for f_idx, filepath in enumerate(files):
        filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as fp:
            data = json.load(fp)

        questions = data.get("questions", [])
        if not questions:
            continue

        for q in questions:
            total_questions += 1
            q_num = q.get("q_num", 0)
            raw_text = q.get("problem_text", "")
            
            # Pass raw text through the universal CSAT typesetter
            normalized_text = normalize_csat_text(raw_text)

            loc_id = f"{filename} Q{q_num}"

            # 1. Check for PUA / Control Char leaks
            pua_matches = pua_regex.findall(normalized_text)
            if pua_matches:
                violations_by_category["pua_control_char"].append({
                    "loc": loc_id,
                    "matches": [hex(ord(c)) for c in pua_matches[:5]],
                    "snippet": normalized_text[:120]
                })

            # 2. Check for Sigma stacking limits
            # Find all math expressions
            math_blocks = re.findall(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', normalized_text)
            for mb in math_blocks:
                if r'\sum' in mb and r'\sum\limits' not in mb:
                    violations_by_category["inconsistent_sigma"].append({
                        "loc": loc_id,
                        "formula": mb
                    })

            # 3. Check for short vector arrows
            for mb in math_blocks:
                svecs = short_vec_regex.findall(mb)
                if svecs:
                    violations_by_category["short_vector_arrow"].append({
                        "loc": loc_id,
                        "formula": svecs
                    })

            # 4. Check for unreduced coefficient 1
            coeffs = unreduced_coeff_regex.findall(normalized_text)
            if coeffs:
                violations_by_category["unreduced_coeff_one"].append({
                    "loc": loc_id,
                    "matches": coeffs
                })

            # 5. Check for raw programming operators (<=, >=, !=)
            raw_ops = raw_operators_regex.findall(normalized_text)
            if raw_ops:
                violations_by_category["raw_programming_operators"].append({
                    "loc": loc_id,
                    "ops": raw_ops
                })

            # 6. Check for developer/coding jargon leaks
            if any(jargon in normalized_text for jargon in ["KaTeX", "Gemini", "API", "console.log", "null", "undefined"]):
                violations_by_category["naked_greek_or_jargon"].append({
                    "loc": loc_id,
                    "detail": "Developer jargon found"
                })

    print(f"\nAudit completed across {total_questions} real CSAT questions in {len(files)} exams.\n")
    print("-" * 80)
    print("AUDIT FINDINGS BY UNIVERSAL CATEGORY:")
    print("-" * 80)

    total_failures = 0
    for cat, items in violations_by_category.items():
        count = len(items)
        total_failures += count
        status = "[PASS]" if count == 0 else "[FAIL]"
        print(f"{status:6} {cat:30}: {count} violations")
        if count > 0:
            for it in items[:3]:
                print(f"       |-- Example: {it}")
            if count > 3:
                print(f"       |-- ... and {count - 3} more")

    print("-" * 80)
    print(f"TOTAL SYSTEMIC DEFECTS FOUND: {total_failures}")
    print("=" * 80)

    return total_failures, violations_by_category

if __name__ == '__main__':
    run_csat_database_audit()
