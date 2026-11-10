import json, sys

sys.stdout.reconfigure(encoding='utf-8')
filepath = 'mathdata/processed_db/2025-11_고3_수능_미적분.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Exam: {data.get('exam_id')}, total questions: {len(data['questions'])}")
for q in data['questions']:
    q_num = q.get('q_num')
    pts = q.get('points')
    text = q.get('problem_text', '').strip()
    ans = q.get('official_answer')
    if q_num in [27, 28, 29, 30]:
        print(f"\n--- [Q{q_num}] ({pts}점, 정답: {ans}) ---")
        print(text[:200])
