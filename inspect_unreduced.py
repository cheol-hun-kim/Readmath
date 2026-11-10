import json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
from csat_typesetter import normalize_csat_text

unreduced_coeff_regex = re.compile(r'(?<![0-9\.a-zA-Z])1([eExX]|\\ln|\\exp)(?![\d])')

for fn in os.listdir('mathdata/processed_db'):
    if not fn.endswith('.json'):
        continue
    fp = os.path.join('mathdata/processed_db', fn)
    with open(fp, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for q in d.get('questions', []):
        txt = normalize_csat_text(q.get('problem_text', ''))
        matches = list(unreduced_coeff_regex.finditer(txt))
        if matches:
            print(f"=== {fn} Q{q.get('q_num')} ===")
            for m in matches:
                start = max(0, m.start() - 30)
                end = min(len(txt), m.end() + 30)
                print(f"  Match '{m.group(0)}': ...{txt[start:end]}...")
