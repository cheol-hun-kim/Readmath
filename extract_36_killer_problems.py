import os
import json
import re

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(ROOT_DIR, "mathdata", "processed_db")

from csat_typesetter import normalize_csat_text

EXAM_TARGETS = [
    {
        "exam_id": "2025_CSAT",
        "name": "2025학년도 수능",
        "files": {
            "common": "2025-11_고3_수능_미적분.json",
            "calculus": "2025-11_고3_수능_미적분.json",
            "geometry": "2025-11_고3_수능_기하.json",
            "probability": "2025-11_고3_수능_확률과통계.json"
        }
    },
    {
        "exam_id": "2026_06_MOCK",
        "name": "2026학년도 6월 모평",
        "files": {
            "common": "2026-06_고3_평가원_미적분.json",
            "calculus": "2026-06_고3_평가원_미적분.json",
            "geometry": "2026-06_고3_평가원_기하.json",
            "probability": "2026-06_고3_평가원_확률과통계.json"
        }
    },
    {
        "exam_id": "2026_09_MOCK",
        "name": "2026학년도 9월 모평",
        "files": {
            "common": "2026-09_고3_평가원_미적분.json",
            "calculus": "2026-09_고3_평가원_미적분.json",
            "geometry": "2026-09_고3_평가원_기하.json",
            "probability": "2026-09_고3_평가원_확률과통계.json"
        }
    }
]

TARGET_NUMBERS = {
    "common": [15, 21, 22],
    "calculus": [28, 29, 30],
    "geometry": [28, 29, 30],
    "probability": [28, 29, 30]
}

extracted_36 = []

for exam in EXAM_TARGETS:
    exam_name = exam["name"]
    for domain, filename in exam["files"].items():
        fpath = os.path.join(DB_DIR, filename)
        if not os.path.exists(fpath):
            print(f"Warning: {filename} not found!")
            continue
            
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        questions = data.get("questions", [])
        q_map = {q.get("q_num"): q for q in questions if "q_num" in q}
        
        target_nums = TARGET_NUMBERS[domain]
        for qnum in target_nums:
            q_obj = q_map.get(qnum)
            if q_obj:
                raw_text = q_obj.get("problem_text", "")
                norm_text = normalize_csat_text(raw_text)
                
                # Check choices if any
                choices = []
                # parse (1) ~ (5) or ① ~ ⑤
                choice_matches = re.findall(r'(?:\([1-5]\)|[①-⑤])\s*([^\n]+)', raw_text)
                if len(choice_matches) == 5:
                    choices = [f"{i+1}. {c.strip()}" for i, c in enumerate(choice_matches)]

                extracted_36.append({
                    "exam_id": exam["exam_id"],
                    "exam_name": exam_name,
                    "domain": domain,
                    "domain_name": "공통(수1·수2)" if domain == "common" else ("미적분" if domain == "calculus" else ("기하" if domain == "geometry" else "확률과통계")),
                    "qnum": qnum,
                    "points": q_obj.get("points", 4),
                    "raw_text": raw_text,
                    "norm_text": norm_text,
                    "choices": choices,
                    "official_answer": q_obj.get("official_answer", ""),
                    "cognitive_solution": q_obj.get("cognitive_solution", {})
                })

print(f"Successfully extracted {len(extracted_36)} killer questions across 3 exams!")

out_file = os.path.join(ROOT_DIR, "mathdata", "extracted_36_killers.json")
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(extracted_36, f, ensure_ascii=False, indent=2)

print(f"Saved to {out_file}")
