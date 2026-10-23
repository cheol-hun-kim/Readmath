import os
import re
import json
import time
from datetime import datetime
import sys

sys.path.append(r'C:\Users\1286o\.gemini\antigravity\scratch\rootmath')
from batch_math_pipeline import process_exam_pair

DATA_DIR = r'C:\Users\1286o\.gemini\antigravity\scratch\rootmath\mathdata'
OUTPUT_DIR = os.path.join(DATA_DIR, 'processed_db')
PROGRESS_FILE = os.path.join(OUTPUT_DIR, 'batch_progress.json')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load existing progress
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)
else:
    progress = {
        "started_at": datetime.now().isoformat(),
        "total_exams": 0,
        "completed_exams": 0,
        "total_questions_ingested": 0,
        "processed_files": {}
    }

files = os.listdir(DATA_DIR)
q_files = sorted([f for f in files if '해설' not in f and f.endswith('.pdf')])
sol_files = [f for f in files if '해설' in f and f.endswith('.pdf')]

progress["total_exams"] = len(q_files)

print(f"=== READMATH MASTER BATCH INGESTION START ===")
print(f"Total Exam Question PDFs: {len(q_files)}")
print(f"Already processed: {progress['completed_exams']}")

for idx, q_file in enumerate(q_files):
    if q_file in progress["processed_files"]:
        continue

    # Find matching solution
    base = re.sub(r'문제지?\.pdf$', '', q_file).strip()
    match_sol = None
    for s in sol_files:
        if base in s:
            match_sol = s
            break

    if not match_sol:
        # Fuzzy match
        for s in sol_files:
            tokens = [t for t in base.split() if len(t) > 1]
            if all(t in s for t in tokens):
                match_sol = s
                break

    q_path = os.path.join(DATA_DIR, q_file)
    sol_path = os.path.join(DATA_DIR, match_sol) if match_sol else None

    if not sol_path:
        print(f"[{idx+1}/{len(q_files)}] Skipped (No solution match): {q_file}")
        continue

    try:
        t0 = time.time()
        result = process_exam_pair(q_path, sol_path)
        out_filename = re.sub(r'[\\/*?:"<>| ]', '_', result["exam_id"]) + ".json"
        out_path = os.path.join(OUTPUT_DIR, out_filename)

        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)

        q_count = result["total_questions"]
        progress["completed_exams"] += 1
        progress["total_questions_ingested"] += q_count
        progress["processed_files"][q_file] = {
            "status": "completed",
            "questions": q_count,
            "json_file": out_filename,
            "duration_sec": round(time.time() - t0, 2),
            "timestamp": datetime.now().isoformat()
        }

        # Save progress every exam
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as pf:
            json.dump(progress, pf, ensure_ascii=False, indent=2)

        print(f"[{idx+1}/{len(q_files)}] DONE: {result['exam_id']} -> {q_count} questions ({round(time.time() - t0, 2)}s)")

    except Exception as e:
        print(f"[{idx+1}/{len(q_files)}] ERROR on {q_file}: {e}")
        progress["processed_files"][q_file] = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as pf:
            json.dump(progress, pf, ensure_ascii=False, indent=2)

print("=== BATCH INGESTION FINISHED ===")
print(f"Total Completed: {progress['completed_exams']}/{len(q_files)}")
print(f"Total Ingested Questions: {progress['total_questions_ingested']}")
