import os
import json
import re

db_dir = r'C:\Users\1286o\.gemini\antigravity\scratch\rootmath\mathdata\processed_db'
json_files = [f for f in os.listdir(db_dir) if f.endswith('.json') and f not in ['batch_progress.json', 'master_catalog.json']]

catalog = []
total_qs = 0

for jf in sorted(json_files):
    filepath = os.path.join(db_dir, jf)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        exam_id = data.get('exam_id', jf.replace('.json', ''))
        q_count = data.get('total_questions', len(data.get('questions', [])))
        total_qs += q_count

        # Extract year, grade, exam type
        year_match = re.search(r'(20\d{2})', exam_id)
        year = year_match.group(1) if year_match else '기타'
        
        grade = '고3' if '고3' in exam_id else ('고2' if '고2' in exam_id else ('고1' if '고1' in exam_id else '공통'))
        
        catalog.append({
            "exam_id": exam_id,
            "filename": jf,
            "year": year,
            "grade": grade,
            "questions_count": q_count
        })
    except Exception as e:
        print(f"Error on {jf}: {e}")

catalog_data = {
    "total_exams": len(catalog),
    "total_questions": total_qs,
    "catalog": catalog
}

with open(os.path.join(db_dir, 'master_catalog.json'), 'w', encoding='utf-8') as f:
    json.dump(catalog_data, f, ensure_ascii=False, indent=2)

print(f"Master Catalog generated: {len(catalog)} exams, {total_qs} total questions!")
