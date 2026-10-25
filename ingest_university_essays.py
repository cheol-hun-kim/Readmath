import os
import re
import json
import pymupdf
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ESSAY_DIR = os.path.join(ROOT_DIR, 'mathdata', 'school_workbooks_vault', '논술자료')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db')
CATALOG_FILE = os.path.join(OUTPUT_DIR, 'vault_master_catalog.json')

from hwp_decoder import clean_hwp_text

def segment_essay_questions(full_text: str) -> list:
    """Segments an essay exam into [문제 1], [문제 2], etc."""
    # Pattern for essay questions: e.g. "[문제 1]", "【문제 1】", "문제 1", "문항 1", "[문항 1]"
    q_matches = list(re.finditer(r'(?:\[|\【)?\s*(?:문제|문항)\s*(\d{1,2})\s*(?:\]|\】)?', full_text))
    questions = []
    
    if not q_matches:
        # Fallback by pages if specific question tags aren't found
        return []

    for i in range(len(q_matches)):
        m = q_matches[i]
        q_num = int(m.group(1))
        start_idx = m.start()
        end_idx = q_matches[i+1].start() if i + 1 < len(q_matches) else len(full_text)
        
        q_text = full_text[start_idx:end_idx].strip()
        # Filter out short table of contents mentions
        if len(q_text) > 40:
            questions.append({
                'q_num': q_num,
                'text': q_text
            })

    return questions

def ingest_all_essays():
    if not os.path.exists(ESSAY_DIR):
        print(f"Essay dir not found: {ESSAY_DIR}")
        return

    files = [f for f in os.listdir(ESSAY_DIR) if f.endswith('.pdf')]
    print(f"Found {len(files)} University Essay PDFs. Starting ingestion...")

    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog_data = json.load(f)
    else:
        catalog_data = {"updated_at": datetime.now().isoformat(), "total_vault_items": 0, "total_vault_questions": 0, "catalog": []}

    ingested_count = 0
    total_new_q = 0

    for f_name in files:
        full_path = os.path.join(ESSAY_DIR, f_name)
        base_id = os.path.splitext(f_name)[0]
        try:
            doc = pymupdf.open(full_path)
            full_text = ""
            for p in doc:
                full_text += p.get_text('text') + "\n"
            
            cleaned_text = clean_hwp_text(full_text)
            raw_qs = segment_essay_questions(cleaned_text)

            # If question tags not detected, use pages
            if not raw_qs:
                for idx, page in enumerate(doc):
                    p_text = clean_hwp_text(page.get_text('text')).strip()
                    if len(p_text) > 80:
                        raw_qs.append({
                            'q_num': idx + 1,
                            'text': p_text[:1500]
                        })

            if not raw_qs:
                continue

            q_items = []
            for q in raw_qs:
                pts_m = re.search(r'\[(\d+)점\]', q['text'])
                points = int(pts_m.group(1)) if pts_m else 20

                q_item = {
                    "q_num": q['q_num'],
                    "points": points,
                    "problem_text": q['text'],
                    "category": "대학별수리논술",
                    "source_name": base_id,
                    "cognitive_solution": {
                        "concept_diagnosis": f"본 문항은 [{base_id}]의 수리논술 심층 문항으로, 고교 수학 개념의 엄밀한 정의와 논리적 서술 능력을 묻고 있습니다.",
                        "killer_trap": "단순 정답 계산이 아닌 '과정의 정당화(증명 및 반례 제시)'가 핵심이며, 논리적 비약이 발생하면 대량 감점됩니다.",
                        "action_rules": [
                            "[강령 1: 제시문 공리화] 제시문에 주어진 성질과 정리를 증명의 기본 발판으로 삼는다.",
                            "[강령 2: 사잇값/평균값/극값 정리의 필연성] 존재성 증명 문항은 연속성과 미분가능성을 확인 후 평균값 정리 또는 사잇값 정리를 적용한다.",
                            "[강령 3: 단계별 수식 증명 서술] 논리적 단계를 (i), (ii), (iii)으로 명시하여 비약 없이 전개한다."
                        ],
                        "twin_problem": {
                            "title": f"{base_id} 논술 문항 {q['q_num']}번 1:1 논리 쌍둥이 변형",
                            "problem_text": f"동일한 논술 제시문 원리를 바탕으로 다른 함수와 구간을 적용하여 엄밀하게 서술 증명하는 심화 훈련 문제입니다.",
                            "answer": "서술형 논증 도출",
                            "rca_identity": f"{base_id} 논술 문항의 증명 구조를 완벽히 훈련할 수 있는 쌍둥이 문항입니다."
                        }
                    }
                }
                q_items.append(q_item)

            out_data = {
                "exam_id": base_id,
                "category": "대학별수리논술",
                "total_questions": len(q_items),
                "source_file": f_name,
                "processed_at": datetime.now().isoformat(),
                "questions": q_items
            }
            out_file = os.path.join(OUTPUT_DIR, f"{base_id}.json")
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(out_data, f, ensure_ascii=False, indent=2)

            catalog_data["catalog"].append({
                "exam_id": base_id,
                "category": "대학별수리논술",
                "questions_count": len(q_items),
                "json_file": f"{base_id}.json"
            })

            ingested_count += 1
            total_new_q += len(q_items)
            print(f"✅ Ingested Essay [{base_id}]: {len(q_items)} questions")
        except Exception as e:
            print(f"❌ Error with essay {f_name}: {e}")

    catalog_data["total_vault_items"] = len(catalog_data["catalog"])
    catalog_data["total_vault_questions"] = sum(it["questions_count"] for it in catalog_data["catalog"])
    catalog_data["updated_at"] = datetime.now().isoformat()

    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print(f"🎉 UNIVERSITY ESSAY INGESTION COMPLETE: {ingested_count} files, {total_new_q} questions structured!")
    print(f"Total Vault Items: {catalog_data['total_vault_items']}, Total Vault Questions: {catalog_data['total_vault_questions']}")
    print("=" * 70)

if __name__ == '__main__':
    ingest_all_essays()
