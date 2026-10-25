import os
import re
import pymupdf
import sys
from hwp_decoder import clean_hwp_text

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHOOL_DIR = os.path.join(ROOT_DIR, 'mathdata', 'school_workbooks_vault', '수학 기출문제 또는 문제집')

def robust_segment_questions(text: str) -> list:
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    questions = []
    
    current_q_num = None
    current_lines = []
    
    # Regex for a question start line:
    # 1. "1. 다음 중"
    # 2. "1. 1. 8/5"
    # 3. "1. log5/6"
    q_start_re = re.compile(r'^(?:(?:\d{1,2}\.\s*)+|\b[0-9]{1,2}\.\s+)(.*)')
    bare_num_re = re.compile(r'^\d{1,2}\.$')

    for i, line in enumerate(lines):
        # Check if line is a bare number e.g. "1."
        if bare_num_re.match(line):
            # If next line starts with "1. 1." or text, continue to next line
            if i + 1 < len(lines) and re.match(r'^\d{1,2}\.', lines[i+1]):
                continue

        m = re.match(r'^(\d{1,2})\.\s*(.*)', line)
        if m and (1 <= int(m.group(1)) <= 35):
            q_num = int(m.group(1))
            body_part = m.group(2).strip()
            # If body_part starts with another "1. ", strip it: "1. 1. text" -> "text"
            body_part = re.sub(r'^\d{1,2}\.\s*', '', body_part)

            # Check if previous question was meaningful
            if current_q_num is not None:
                full_body = '\n'.join(current_lines).strip()
                if len(full_body) > 15:
                    questions.append({'q_num': current_q_num, 'text': full_body})
            
            current_q_num = q_num
            current_lines = [body_part] if body_part else []
        else:
            if current_q_num is not None:
                current_lines.append(line)

    if current_q_num is not None and current_lines:
        full_body = '\n'.join(current_lines).strip()
        if len(full_body) > 15:
            questions.append({'q_num': current_q_num, 'text': full_body})

    # Deduplicate by q_num (keep longest text)
    dedup = {}
    for q in questions:
        qn = q['q_num']
        if qn not in dedup or len(q['text']) > len(dedup[qn]['text']):
            dedup[qn] = q

    return sorted(dedup.values(), key=lambda x: x['q_num'])

pdf_files = [f for f in os.listdir(SCHOOL_DIR) if f.endswith('.pdf') and not f.startswith('절대등급')]
for f in pdf_files:
    p = os.path.join(SCHOOL_DIR, f)
    doc = pymupdf.open(p)
    raw = ""
    for page in doc:
        raw += page.get_text('text') + "\n"
    cleaned = clean_hwp_text(raw)
    qs = robust_segment_questions(cleaned)
    print(f"File: {f[:35]}... -> Exact Real Questions: {len(qs)} (Q{qs[0]['q_num']} ~ Q{qs[-1]['q_num']})")
    print(f"   Sample Q1: {repr(qs[0]['text'][:60])}")
