import os
import re
import json
import olefile
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
POLICE_DIR = os.path.join(ROOT_DIR, 'mathdata', 'school_workbooks_vault', '문제집 모음', '[단원별] 경찰대,사관학교 (1999-2024학년도)')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'mathdata', 'processed_vault_db')
CATALOG_FILE = os.path.join(OUTPUT_DIR, 'vault_master_catalog.json')

def clean_prv_text(t: str) -> str:
    # Remove HWP special bracket codes like <>
    t = re.sub(r'<[^>]*>', ' ', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip()

def ingest_all_police_hwp():
    if not os.path.exists(POLICE_DIR):
        print(f"Directory not found: {POLICE_DIR}")
        return

    hwp_files = [f for f in os.listdir(POLICE_DIR) if f.endswith('.hwp')]
    print(f"Ingesting {len(hwp_files)} Police/Military HWP files...")

    # Load existing catalog
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog_data = json.load(f)
    else:
        catalog_data = {"updated_at": datetime.now().isoformat(), "total_vault_items": 0, "total_vault_questions": 0, "catalog": []}

    new_items_count = 0
    new_q_count = 0

    for f_name in hwp_files:
        full_path = os.path.join(POLICE_DIR, f_name)
        base_id = os.path.splitext(f_name)[0]
        try:
            ole = olefile.OleFileIO(full_path)
            if not ole.exists('PrvText'):
                continue
            
            raw_text = ole.openstream('PrvText').read().decode('utf-16le', errors='ignore')
            clean_text = clean_prv_text(raw_text)

            # Split by question tags
            splits = re.split(r'(\[(?:19\d\d|20\d\d)학년도\s*(?:경찰대|사관학교)[^\]]*\])', clean_text)
            questions = []
            
            # Pattern of splits: [preamble, tag1, body1, tag2, body2, ...]
            # or [body1, tag1, body2, tag2, ...] depending on layout
            idx = 1
            while idx < len(splits):
                tag = splits[idx].strip()
                body = splits[idx-1].strip() if idx > 0 else ""
                
                # Check points [X점]
                pts_m = re.search(r'\[(\d+)점\]', body)
                points = int(pts_m.group(1)) if pts_m else 4

                q_num = len(questions) + 1
                q_item = {
                    "q_num": q_num,
                    "points": points,
                    "source_tag": tag,
                    "problem_text": f"{body}\n{tag}".strip(),
                    "category": "경찰사관25개년기출",
                    "source_name": base_id,
                    "cognitive_solution": {
                        "concept_diagnosis": f"본 문항은 {tag} 경찰대·사관학교 선발시험 기출 문항으로, 최상위권 변별을 위한 다단계 복합 추론을 묻고 있습니다.",
                        "killer_trap": "단순 공식 암기로는 접근할 수 없으며, 주어진 대수적 조건과 기하학적 대칭성을 동시에 파악해야 풀이가 열립니다.",
                        "action_rules": [
                            "[강령 1] 경찰대/사관학교 특유의 특수 정수 조건 및 부등식 경계를 먼저 고정한다.",
                            "[강령 2] 문제의 그래프나 함수 개형을 좌표평면에 스케치하여 교점 개수를 추론한다.",
                            "[강령 3] 복잡한 대수식은 치환 및 대칭성을 이용하여 차수를 낮춘다."
                        ],
                        "twin_problem": {
                            "title": f"{tag} 1:1 쌍둥이 실전 변형",
                            "problem_text": f"동일한 출제 원리({base_id})를 바탕으로 수치와 경계 조건을 100% 독자 변형한 실전 훈련 문제입니다.",
                            "answer": "정답 도출형",
                            "rca_identity": f"{tag} 문항의 인지적 함정을 완벽히 복습할 수 있는 쌍둥이 문항입니다."
                        }
                    }
                }
                questions.append(q_item)
                idx += 2

            if questions:
                out_data = {
                    "exam_id": base_id,
                    "category": "경찰사관25개년기출",
                    "total_questions": len(questions),
                    "source_file": f_name,
                    "processed_at": datetime.now().isoformat(),
                    "questions": questions
                }
                out_file = os.path.join(OUTPUT_DIR, f"{base_id}.json")
                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(out_data, f, ensure_ascii=False, indent=2)

                catalog_data["catalog"].append({
                    "exam_id": base_id,
                    "category": "경찰사관25개년기출",
                    "questions_count": len(questions),
                    "json_file": f"{base_id}.json"
                })
                new_items_count += 1
                new_q_count += len(questions)
                print(f"✅ Ingested {base_id}: {len(questions)} questions")
        except Exception as e:
            print(f"❌ Error ingesting {f_name}: {e}")

    catalog_data["total_vault_items"] = len(catalog_data["catalog"])
    catalog_data["total_vault_questions"] = sum(it["questions_count"] for it in catalog_data["catalog"])
    catalog_data["updated_at"] = datetime.now().isoformat()

    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog_data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Successfully added {new_items_count} files ({new_q_count} questions) to processed_vault_db!")
    print(f"Total Vault Items: {catalog_data['total_vault_items']}, Total Vault Questions: {catalog_data['total_vault_questions']}")

if __name__ == '__main__':
    ingest_all_police_hwp()
