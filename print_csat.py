import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("C:/Users/1286o/.gemini/antigravity/scratch/rootmath/master_killer_census.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print("=== ALL CSAT (수능) KILLER AUDIT MATRIX ===")
for item in db:
    if item["agency"] == "수능":
        print(f"{item['id']}: {item['killer_answers']}")
