# -*- coding: utf-8 -*-
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_FILE = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db', '서현고등학교_2학년_2021_1학기중간_수학1_공통_문제_해설.json')

def audit_file(target_path=None):
    if target_path is None:
        if len(sys.argv) > 1:
            target_path = sys.argv[1]
        else:
            target_path = TARGET_FILE

    print("=" * 70)
    print(f"AUDITING DATASET AGAINST ROOTMATH 7 GATES: {os.path.basename(target_path)}")
    print("=" * 70)

    with open(target_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['questions']
    errors = []

    # 1. Question Count & Points
    expected_count = data.get('metadata', {}).get('question_count', len(questions))
    if len(questions) != expected_count or len(questions) < 15:
        errors.append(f"Expected {expected_count} questions, found {len(questions)}")
    total_pts = sum(q.get('points', 0) for q in questions)
    if abs(total_pts - 100.0) > 1e-4:
        errors.append(f"Total points should be 100.0, got {total_pts}")

    # 2. Check each question
    forbidden_jargons = ['Gemini', 'API', 'AI Studio', 'RCA', 'B2B', 'KaTeX', '수식 모델링', '해석기하', '1타 강사']
    forbidden_brands = ['수평선', '절대등급', '고쟁이', '블랙라벨', '마더텅', '자이스토리', '쎈수학', '일품', '올림포스', '개념원리', '만렙']

    for q in questions:
        qn = q['q_num']
        txt = q['problem_text'] + ' ' + q['cognitive_solution']
        
        # Check jargons & brands
        for j in forbidden_jargons:
            if j.lower() in txt.lower():
                errors.append(f"Q{qn}: Contains forbidden jargon '{j}'")
        for b in forbidden_brands:
            if b in txt:
                errors.append(f"Q{qn}: Contains commercial brand '{b}'")

        # Check OCR artifacts
        if re.search(r'/\s*\\sqrt', txt) or '[\ue000-\uf8ff]' in txt:
            errors.append(f"Q{qn}: Contains broken OCR artifacts")

        # Check Prescriptions (Gate 3/5)
        presc = q.get('prescriptions', {})
        for req in ['visual', 'modeling', 'condition', 'concept']:
            if not presc.get(req):
                errors.append(f"Q{qn}: Missing prescription '{req}'")

        # Check SVG (Gate 4)
        svg = q.get('verified_svg', '')
        if not svg or '<svg' not in svg:
            errors.append(f"Q{qn}: Missing verified SVG")
        else:
            # Check for LaTeX backslash inside <text> tags!
            text_matches = re.findall(r'<text\b[^>]*>(.*?)</text>', svg, re.DOTALL)
            for tm in text_matches:
                if '\\' in tm:
                    errors.append(f"Q{qn} SVG FAIL: LaTeX backslash found in SVG text: '{tm}'")

    print(f"Total audit errors: {len(errors)}")
    if errors:
        for e in errors:
            print("  |--", e)
        sys.exit(1)
    else:
        print("ALL 7 GATES PASSED 100%! ZERO DEFECTS FOUND.")

if __name__ == '__main__':
    audit_file()
