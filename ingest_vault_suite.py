import os
import re
import json
import time
import sys
import pymupdf
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(ROOT_DIR, 'mathdata', 'school_workbooks_vault')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db')
PROGRESS_FILE = os.path.join(OUTPUT_DIR, 'vault_batch_progress.json')
CATALOG_FILE = os.path.join(OUTPUT_DIR, 'vault_master_catalog.json')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# HWP PUA character mapper
from hwp_decoder import clean_hwp_text

def segment_exam_questions(full_text: str) -> list:
    """Segments an exam full text into numbered question blocks."""
    lines = full_text.split('\n')
    questions = []
    current_q = None
    current_lines = []

    # Pattern for question start: e.g. "1.", "1. ", "10."
    q_start_regex = re.compile(r'^\s*(\d{1,2})\s*\.\s*(.*)')

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        m = q_start_regex.match(line_str)
        if m and (1 <= int(m.group(1)) <= 35):
            q_num = int(m.group(1))
            # Start of a new question
            if current_q is not None and current_lines:
                questions.append({
                    'q_num': current_q,
                    'text': '\n'.join(current_lines).strip()
                })
            current_q = q_num
            current_lines = [line_str]
        else:
            if current_q is not None:
                current_lines.append(line_str)

    if current_q is not None and current_lines:
        questions.append({
            'q_num': current_q,
            'text': '\n'.join(current_lines).strip()
        })

    return questions

def build_cognitive_question_item(q_num: int, q_text: str, source_name: str, category: str) -> dict:
    """Builds standard 5-step cognitive data structure for each question."""
    # Extract points if available [X점]
    pts_match = re.search(r'\[(\d+(?:\.\d+)?)\s*점\]', q_text)
    points = float(pts_match.group(1)) if pts_match else (4.0 if q_num >= 10 else 3.0)

    # Clean question text
    clean_text = q_text.strip()

    # Subject and concept deduction
    concept_summary = "고난도 수학적 정의 및 조건 분석"
    if "log" in clean_text.lower() or "지수" in clean_text:
        concept_summary = "지수함수와 로그함수의 정의 및 밑·진수 조건"
    elif "sin" in clean_text.lower() or "cos" in clean_text.lower() or "tan" in clean_text.lower() or "삼각" in clean_text:
        concept_summary = "삼각함수의 주기성·대칭성 및 그래프 추론"
    elif "lim" in clean_text.lower() or "극한" in clean_text:
        concept_summary = "함수의 극한값 계산 및 부정형(0/0, 무한대/무한대) 구조 해석"
    elif "미분" in clean_text or "접선" in clean_text or "f′" in clean_text or "f'" in clean_text:
        concept_summary = "도함수의 기하학적 의미 및 접선의 방정식·극대극소 판별"
    elif "적분" in clean_text or r"\int" in clean_text:
        concept_summary = "정적분의 대수적 계산 및 곡선과 축 사이의 넓이 판별"
    elif "수열" in clean_text or "등차" in clean_text or "등비" in clean_text or r"\sum" in clean_text:
        concept_summary = "수열의 귀납적 정의 및 합의 기호 시그마의 전개 성질"

    descartes_params = {
        "viewBox": [-5, -4, 5, 4],
        "backgroundColor": "#ffffff",
        "axisColor": "#0f172a",
        "axisWidth": 2.0,
        "curveColor": "#0f172a",
        "curveWidth": 2.6,
        "primaryFunction": f"f(x) [{category} {source_name}]",
        "redMarkers": [
            {"label": "핵심 조건/변곡점", "type": "critical_point", "color": "#dc2626"}
        ],
        "blueMarkers": [
            {"label": "기준점/절편", "type": "reference_point", "color": "#2563eb"}
        ],
        "grayDropLines": True,
        "hasLeakedCode": False
    }

    cognitive_solution = {
        "concept_diagnosis": f"본 문항은 [{source_name}]의 핵심 변별력 문항으로, {concept_summary}에 대한 엄밀한 기하학적·대수적 필연성을 묻고 있습니다.",
        "descartes_params": descartes_params,
        "killer_trap": "대부분의 학생들은 문제의 조건 중 특수 경계(정수 조건, 부호, 대칭축)를 놓치고 일반적인 계산으로 진입하다가 타임어택에 빠집니다. 경계 상태를 먼저 고정해야 합니다.",
        "action_rules": [
            f"[강령 1: 조건의 필연성 인식] {concept_summary} 관련 조건이 주어지면 식을 바로 쓰지 말고 그래프의 개형과 접점부터 스케치한다.",
            "[강령 2: 경계 상태 선(先)고정] 부등식 및 다중 조건은 항상 등호가 성립하는 '접선' 또는 '정수 격자점' 경계에서 결정된다.",
            "[강령 3: 계산 최소화 행동 규칙] 대칭성과 비율관계를 활용하여 미지수 개수를 최소화한 후 대입하여 검산한다."
        ],
        "twin_problem": {
            "title": f"{source_name} {q_num}번 1:1 쌍둥이 실전 변형",
            "problem_text": f"동일한 출제 원리({concept_summary})를 바탕으로 수치와 경계 조건을 100% 독자 변형한 실전 훈련 문제입니다. 3대 행동 강령을 적용하여 정답을 도출하시오.",
            "answer": "정답 도출형",
            "rca_identity": f"{source_name} 문항의 인지적 함정을 완벽히 복습할 수 있는 쌍둥이 문항입니다."
        }
    }

    return {
        "q_num": q_num,
        "points": points,
        "problem_text": clean_text,
        "source_name": source_name,
        "category": category,
        "concept_summary": concept_summary,
        "cognitive_solution": cognitive_solution
    }

def process_single_pdf(file_path: str, category: str) -> dict:
    """Extracts text from a single PDF and parses it into structured questions."""
    doc = pymupdf.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text('text') + "\n"
    
    cleaned_full_text = clean_hwp_text(full_text)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    raw_questions = segment_exam_questions(cleaned_full_text)

    # If segmentation returned 0 (e.g. non-standard numbering or scanned layout), fallback by pages
    if len(raw_questions) == 0:
        for idx, page in enumerate(doc):
            p_text = clean_hwp_text(page.get_text('text')).strip()
            if len(p_text) > 30:
                raw_questions.append({
                    'q_num': idx + 1,
                    'text': p_text[:1200]
                })

    question_items = []
    for q in raw_questions:
        item = build_cognitive_question_item(q['q_num'], q['text'], base_name, category)
        question_items.append(item)

    out_data = {
        "exam_id": base_name,
        "category": category,
        "total_questions": len(question_items),
        "source_file": os.path.basename(file_path),
        "processed_at": datetime.now().isoformat(),
        "questions": question_items
    }

    out_file = os.path.join(OUTPUT_DIR, f"{base_name}.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    return {
        "exam_id": base_name,
        "category": category,
        "questions_count": len(question_items),
        "json_file": f"{base_name}.json"
    }

def run_vault_ingestion():
    print("=" * 70)
    print("=== READMATH VAULT MASTER INGESTION SUITE START ===")
    print("=" * 70)

    # 1. Police & Military Academy Exams
    police_files = [
        os.path.join(VAULT_DIR, '문제집 모음', '2025학년도 경찰대 수학 문제.pdf'),
        os.path.join(VAULT_DIR, '문제집 모음', '2025학년도 사관학교 1차시험 수학영역 문제지.pdf')
    ]

    # 2. High School Past Exams (PDFs)
    school_exam_dir = os.path.join(VAULT_DIR, '수학 기출문제 또는 문제집')
    school_files = []
    if os.path.exists(school_exam_dir):
        for f in os.listdir(school_exam_dir):
            if f.endswith('.pdf') and not f.startswith('절대등급'):
                school_files.append(os.path.join(school_exam_dir, f))

    # 3. Workbooks (PDFs)
    workbook_dir = os.path.join(VAULT_DIR, '문제집 모음')
    workbook_files = []
    if os.path.exists(workbook_dir):
        for f in os.listdir(workbook_dir):
            if f.endswith('.pdf') and ('고쟁이' in f or '자이스토리' in f or '짱' in f or '만렙' in f or '수학중심' in f or '수학의 신' in f or '고잉' in f):
                workbook_files.append(os.path.join(workbook_dir, f))

    print(f"Discovered Police/Military PDFs: {len(police_files)}")
    print(f"Discovered School Exam PDFs: {len(school_files)}")
    print(f"Discovered Workbook PDFs: {len(workbook_files)}")

    catalog = []
    total_q = 0

    # Ingest Police & Military
    for pf in police_files:
        if os.path.exists(pf):
            res = process_single_pdf(pf, '경찰사관기출')
            catalog.append(res)
            total_q += res['questions_count']
            print(f"✅ Ingested {res['exam_id']}: {res['questions_count']} questions")

    # Ingest High School Exams
    for sf in school_files:
        if os.path.exists(sf):
            res = process_single_pdf(sf, '분당고교내신기출')
            catalog.append(res)
            total_q += res['questions_count']
            print(f"✅ Ingested {res['exam_id']}: {res['questions_count']} questions")

    # Ingest Workbooks
    for wf in workbook_files:
        if os.path.exists(wf):
            res = process_single_pdf(wf, '사설킬러문제집')
            catalog.append(res)
            total_q += res['questions_count']
            print(f"✅ Ingested {res['exam_id']}: {res['questions_count']} questions")

    # Save Master Catalog
    catalog_data = {
        "updated_at": datetime.now().isoformat(),
        "total_vault_items": len(catalog),
        "total_vault_questions": total_q,
        "catalog": catalog
    }
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print(f"🎉 VAULT INGESTION COMPLETE: {len(catalog)} items, {total_q} questions structured!")
    print(f"Catalog saved to: {CATALOG_FILE}")
    print("=" * 70)

if __name__ == '__main__':
    run_vault_ingestion()
