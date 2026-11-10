import os, sys, glob

sys.stdout.reconfigure(encoding='utf-8')

mathdata_dir = 'mathdata'
files = glob.glob(os.path.join(mathdata_dir, '**', '*.*'), recursive=True)
print(f"Total files in mathdata tree: {len(files)}")

subdirs = [d for d in os.listdir(mathdata_dir) if os.path.isdir(os.path.join(mathdata_dir, d))]
print(f"Subdirectories in mathdata: {subdirs}")

csat_files = []
eval_files = []
edu_files = []
other_files = []

for f in os.listdir(mathdata_dir):
    fp = os.path.join(mathdata_dir, f)
    if os.path.isfile(fp):
        if '수능' in f:
            csat_files.append(f)
        elif '평가원' in f:
            eval_files.append(f)
        elif '교육청' in f:
            edu_files.append(f)
        else:
            other_files.append(f)

print(f"\nTop-level mathdata files count: {len(csat_files) + len(eval_files) + len(edu_files) + len(other_files)}")
print(f"  - '수능' (CSAT actual exams): {len(csat_files)} files")
print(f"  - '평가원' (KICE June/Sept Mock CSATs): {len(eval_files)} files")
print(f"  - '교육청' (Office of Education Mocks): {len(edu_files)} files")
print(f"  - Other files: {len(other_files)} files")

print("\n--- Detailed CSAT ('수능') Files ---")
for f in sorted(csat_files):
    print(f"  {f}")

print("\n--- Also check subdirectories for CSAT data ---")
for sd in subdirs:
    sd_path = os.path.join(mathdata_dir, sd)
    sd_csat = [f for f in glob.glob(os.path.join(sd_path, '**', '*.*'), recursive=True) if '수능' in f]
    if sd_csat:
        print(f"  In {sd}: {len(sd_csat)} files containing '수능'")
        for f in sd_csat[:5]:
            print(f"    {os.path.relpath(f, mathdata_dir)}")
        if len(sd_csat) > 5:
            print(f"    ... and {len(sd_csat)-5} more")
