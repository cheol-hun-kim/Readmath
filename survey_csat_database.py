import json, glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')

files = sorted(glob.glob('mathdata/processed_db/*수능*.json'))
total_q = 0
sigmas = 0
vectors = 0
integrals = 0
limits = 0
trig = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        for q in data.get('questions', []):
            total_q += 1
            sol = q.get('cognitive_solution', '')
            if isinstance(sol, dict):
                sol_str = json.dumps(sol, ensure_ascii=False)
            elif isinstance(sol, list):
                sol_str = " ".join([str(x) for x in sol])
            else:
                sol_str = str(sol)
            txt = str(q.get('problem_text', '')) + ' ' + sol_str
            if re.search(r'(\\sum|급수|시그마)', txt):
                sigmas += 1
            if re.search(r'(\\vec|\\overrightarrow|벡터)', txt):
                vectors += 1
            if re.search(r'(\\int|적분)', txt):
                integrals += 1
            if re.search(r'(\\lim|극한)', txt):
                limits += 1
            if re.search(r'(\\sin|\\cos|\\tan|삼각함수)', txt):
                trig += 1

print(f"Analyzed {total_q} CSAT Questions across {len(files)} JSON files:")
print(f"  - Involves Sum / Series (\\sum, 급수): {sigmas} questions")
print(f"  - Involves Vectors / Directed Segments: {vectors} questions")
print(f"  - Involves Integrals (\\int, 적분): {integrals} questions")
print(f"  - Involves Limits (\\lim, 극한): {limits} questions")
print(f"  - Involves Trigonometry (sin, cos, tan): {trig} questions")
