"""
ReadMath 108-Je Masterpiece Final Exam Compiler
Compiles 108 questions (36 seeds + 72 variations) + 4-Way solutions into CSAT publication
"""

import os
import sys
from mathdata.questions_part1 import PART_1_QUESTIONS
from mathdata.questions_part2 import PART_2_QUESTIONS
from mathdata.questions_part3 import PART_3_QUESTIONS
from generate_universal_diagrams import build_universal_svg_for_problem as get_svg_for_prob
from csat_typesetter import normalize_csat_text

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

ALL_QUESTIONS = PART_1_QUESTIONS + PART_2_QUESTIONS + PART_3_QUESTIONS
assert len(ALL_QUESTIONS) == 108, f"Expected 108 questions, got {len(ALL_QUESTIONS)}"

html_pages = []

TOTAL_PROB_PAGES = 27
TOTAL_SOL_PAGES = 27
TOTAL_PAGES = TOTAL_PROB_PAGES + TOTAL_SOL_PAGES + 1  # 55 pages

# ==============================================================================
# PART 1, 2, 3: PROBLEM PAGES (Pages 1 to 27)
# ==============================================================================
for p_idx in range(TOTAL_PROB_PAGES):
    page_num = p_idx + 1
    q_start = p_idx * 4
    q_page = ALL_QUESTIONS[q_start:q_start+4]
    
    col_left_html = ""
    col_right_html = ""
    
    for i, q in enumerate(q_page):
        norm_text = normalize_csat_text(q["text"])
        ch_html = ""
        if q.get("choices"):
            ch_spans = "".join([f"<span>{normalize_csat_text(c)}</span>" for c in q["choices"]])
            ch_html = f'<div class="prob-choices">{ch_spans}</div>'
            
        box_type = "5지선다" if q.get("choices") else "단답형"
        
        q_item = f'''<div class="prob-item">
          <div class="prob-meta">
            <span class="tag">{q["meta"]}</span>
            <span class="type-pill">{box_type}</span>
          </div>
          <div class="prob-title">
            <span class="num">{q["num"]}.</span>{norm_text}<span class="prob-points">[{q["points"]}점]</span>
          </div>
          {ch_html}
          <div class="calc-space"></div>
        </div>'''
        
        if i < 2:
            col_left_html += q_item
        else:
            col_right_html += q_item
            
    # Distinct Header Titles per Exam Part
    if page_num <= 9:
        header_title = "2025학년도 대수능 킬러 & 심층·융합 36제 N제"
        sub_badge = "ReadMath 1:1 약점 역추적 시리즈 (평가원 원본 12제 + 정밀 변형 24제)"
    elif page_num <= 18:
        header_title = "2026학년도 6월 모의평가 킬러 & 심층·융합 36제 N제"
        sub_badge = "평가원 출제 DNA 원형 보존 & 실전 킬러 대비 36제"
    else:
        header_title = "2026학년도 9월 모의평가 킬러 & 심층·융합 36제 N제"
        sub_badge = "수능 D-9 초격차 파이널 총정리 36제"
        
    student_info = '''<div class="csat-student-info">
      <span>성명: ____________________</span>
      <span>수험번호: ____________________</span>
    </div>''' if page_num in (1, 10, 19) else ""

    p_html = f'''<div class="page">
    <div>
      <div class="csat-header" style="position: relative;">
        <div class="csat-header-top">
          <span class="csat-year-title">{header_title}</span>
          <span class="csat-sub-badge">{sub_badge}</span>
        </div>
        <div class="csat-header-mid">
          <div class="csat-period">제 2 교시</div>
          <div class="csat-subject-title">수 학 &nbsp; 영 역</div>
          <div class="csat-type-badge">파이널 N제</div>
        </div>
        {student_info}
      </div>
      <div class="csat-grid">
        <div class="col-divider"></div>
        <div class="col-left">{col_left_html}</div>
        <div class="col-right">{col_right_html}</div>
      </div>
    </div>
    <div class="csat-footer">
      <div class="csat-footer-left">ReadMath 1:1 약점 역추적 클리닉</div>
      <div class="csat-footer-center">
        <span class="csat-page-box">[ - {page_num} - ]</span>
      </div>
      <div class="csat-footer-right">{page_num} / {TOTAL_PAGES}</div>
    </div>
  </div>'''
    html_pages.append(p_html)

# ==============================================================================
# PART 4: 4-WAY COMPREHENSIVE SOLUTIONS (Pages 28 to 54)
# ==============================================================================
for s_idx in range(TOTAL_SOL_PAGES):
    sol_page_num = TOTAL_PROB_PAGES + s_idx + 1
    q_start = s_idx * 4
    q_page = ALL_QUESTIONS[q_start:q_start+4]
    
    cards_html = ""
    for q in q_page:
        svg_code = get_svg_for_prob(q["num"]) if q["num"] % 2 == 1 or q.get("svg") else ""
        svg_block = f'<div class="sol-diagram-box">{svg_code}</div>' if svg_code else ""
        
        cards_html += f'''<div class="sol-card">
          <div class="sol-header">
            <div class="sol-meta-row">
              <span class="sol-qnum">{q["num"]}번</span>
              <span class="sol-meta-tag">{q["meta"]}</span>
              <span class="sol-topic-tag">{q["topic"]}</span>
            </div>
            <div class="sol-ans-badge">정답 {q["ans"]}</div>
          </div>
          <div class="sol-body">
            <div class="sol-grid-3way">
              <div class="sol-box sol-stuck">
                <div class="sol-box-title">
                  <span class="sol-box-icon">⚠️</span> [시험장 3초 컷 오답 함정 분석]
                </div>
                <div class="sol-box-content">{q["stuck"]}</div>
              </div>
              <div class="sol-box sol-recipe">
                <div class="sol-box-title">
                  <span class="sol-box-icon">🔑</span> [동일 출제 원리 & 핵심 키]
                </div>
                <div class="sol-box-content">{q["recipe"]}</div>
              </div>
            </div>
            <div class="sol-box sol-steps">
              <div class="sol-box-title">
                <span class="sol-box-icon">📝</span> [단계별 논리적 풀이]
              </div>
              <div class="sol-box-content">{q["steps"]}</div>
            </div>
            <div class="sol-box sol-defense">
              <div class="sol-box-title">
                <span class="sol-box-icon">🛡️</span> [실전 오답 방어 행동 공식]
              </div>
              <div class="sol-box-content">{q.get("defense", "")}</div>
            </div>
            {svg_block}
          </div>
        </div>'''
        
    s_html = f'''<div class="page">
    <div>
      <div class="csat-header">
        <div class="csat-header-top">
          <span class="csat-year-title">ReadMath 수능 D-9 초격차 파이널 108제 마스터피스 해설지</span>
          <span class="csat-sub-badge">4-Way 입체 심층 해설 & 실전 행동 강령</span>
        </div>
        <div class="csat-header-mid">
          <div class="csat-period">정밀 정답 & 입체 해설</div>
          <div class="csat-subject-title">수 학 &nbsp; 영 역</div>
          <div class="csat-type-badge">해설지</div>
        </div>
      </div>
      <div class="sol-container">
        {cards_html}
      </div>
    </div>
    <div class="csat-footer">
      <div class="csat-footer-left">ReadMath 1:1 약점 역추적 클리닉</div>
      <div class="csat-footer-center">
        <span class="csat-page-box">[ - {sol_page_num} - ]</span>
      </div>
      <div class="csat-footer-right">{sol_page_num} / {TOTAL_PAGES}</div>
    </div>
  </div>'''
    html_pages.append(s_html)

# ==============================================================================
# PART 5: QUICK ANSWER KEY & 36-THEME DIAGNOSTIC MATRIX (Page 55)
# ==============================================================================
ans_cells = "".join([f'''<div class="ans-cell">
  <span class="ans-cell-num">{q["num"]}</span>
  <span class="ans-cell-val">{q["ans"]}</span>
</div>''' for q in ALL_QUESTIONS])

theme_rows = ""
for set_idx in range(36):
    q_orig = ALL_QUESTIONS[set_idx * 3]
    theme_rows += f'''<tr>
      <td class="text-center font-bold">{set_idx+1}</td>
      <td class="font-bold">{q_orig["meta"].replace(" [평가원 원본]", "")}</td>
      <td>{q_orig["topic"]}</td>
      <td class="text-center font-mono">{set_idx*3+1}, {set_idx*3+2}, {set_idx*3+3}번</td>
      <td class="text-xs text-slate-600">{q_orig.get("defense", "")[:36]}...</td>
    </tr>'''

page_55_html = f'''<div class="page">
  <div>
    <div class="csat-header">
      <div class="csat-header-top">
        <span class="csat-year-title">ReadMath 수능 D-9 초격차 파이널 108제 빠른 정답표 & 출제 매트릭스</span>
        <span class="csat-sub-badge">1~108번 전 문항 일람 및 36대 킬러 출제 테마</span>
      </div>
      <div class="csat-header-mid">
        <div class="csat-period">파이널 총정리</div>
        <div class="csat-subject-title">빠 른 &nbsp; 정 답 표</div>
        <div class="csat-type-badge">정답표</div>
      </div>
    </div>
    
    <div style="margin-top: 10px;">
      <h3 class="section-title">108제 전 문항 빠른 정답표 (1 ~ 108번)</h3>
      <div class="ans-grid-108">
        {ans_cells}
      </div>
      
      <h3 class="section-title" style="margin-top: 14px;">36대 킬러 테마 결손 역추적 & 처방 매트릭스</h3>
      <div class="matrix-table-wrap">
        <table class="matrix-table">
          <thead>
            <tr>
              <th style="width: 32px;">세트</th>
              <th style="width: 140px;">출제 원형</th>
              <th style="width: 150px;">핵심 테마 & 개념</th>
              <th style="width: 80px;">문항 번호</th>
              <th>시험장 3초 컷 오답 방어 행동 공식</th>
            </tr>
          </thead>
          <tbody>
            {theme_rows}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="csat-footer">
    <div class="csat-footer-left">ReadMath 1:1 약점 역추적 클리닉</div>
    <div class="csat-footer-center">
      <span class="csat-page-box">[ - 55 - ]</span>
    </div>
    <div class="csat-footer-right">55 / {TOTAL_PAGES}</div>
  </div>
</div>'''

html_pages.append(page_55_html)

# ==============================================================================
# FULL HTML WRAPPER WITH PRECISE CSAT STYLING
# ==============================================================================
full_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>ReadMath 수능 D-9 초격차 파이널 마스터피스 108제 N제</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    @page {{
      size: 210mm 297mm;
      margin: 12mm 14mm 14mm 14mm;
    }}
    
    * {{
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
      word-break: keep-all;
      overflow-wrap: break-word;
    }}
    
    body {{
      margin: 0;
      padding: 0;
      background: #EAE6DE;
      font-family: 'Pretendard', -apple-system, sans-serif;
      color: #080908;
    }}
    
    .page {{
      width: 182mm;
      height: 268mm;
      margin: 10mm auto;
      background: #FFFFFF;
      padding: 10mm 12mm 10mm 12mm;
      position: relative;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    @media print {{
      body {{ background: transparent; }}
      .page {{
        margin: 0 auto;
        padding: 8mm 10mm 8mm 10mm;
        box-shadow: none;
        height: 268mm;
      }}
    }}
    
    /* CSAT Header */
    .csat-header {{
      border-bottom: 2px solid #080908;
      padding-bottom: 6px;
      margin-bottom: 12px;
    }}
    .csat-header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }}
    .csat-year-title {{
      font-size: 13px;
      font-weight: 800;
      color: #080908;
      letter-spacing: -0.02em;
    }}
    .csat-sub-badge {{
      font-size: 11px;
      font-weight: 700;
      color: #EA580C;
    }}
    .csat-header-mid {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 4px;
      padding-top: 4px;
      border-top: 1px solid #CBD5E1;
    }}
    .csat-period {{
      font-size: 13px;
      font-weight: 800;
      color: #080908;
      min-width: 65px;
    }}
    .csat-subject-title {{
      font-size: 20px;
      font-weight: 900;
      letter-spacing: 0.25em;
      text-align: center;
      flex: 1;
    }}
    .csat-type-badge {{
      font-size: 11px;
      font-weight: 800;
      border: 1.5px solid #080908;
      padding: 1px 8px;
      border-radius: 4px;
    }}
    .csat-student-info {{
      display: flex;
      justify-content: flex-end;
      gap: 24px;
      font-size: 11px;
      font-weight: 600;
      color: #334155;
      margin-top: 4px;
    }}
    
    /* 2-Column Grid */
    .csat-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 16mm;
      position: relative;
    }}
    .col-divider {{
      position: absolute;
      left: 50%;
      top: 0;
      bottom: 0;
      width: 1px;
      background: #CBD5E1;
    }}
    .col-left, .col-right {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    
    /* Problem Item */
    .prob-item {{
      display: flex;
      flex-direction: column;
      min-height: 102mm;
    }}
    .prob-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }}
    .prob-meta .tag {{
      font-size: 10px;
      font-weight: 700;
      color: #475569;
      background: #F1F5F9;
      padding: 1px 6px;
      border-radius: 3px;
    }}
    .prob-meta .type-pill {{
      font-size: 9.5px;
      font-weight: 700;
      color: #64748B;
      border: 1px solid #CBD5E1;
      padding: 0 4px;
      border-radius: 3px;
    }}
    .prob-title {{
      font-size: 12.5px;
      line-height: 1.6;
      font-weight: 500;
      color: #080908;
    }}
    .prob-title .num {{
      font-weight: 900;
      font-size: 14px;
      margin-right: 4px;
    }}
    .prob-points {{
      font-size: 11px;
      font-weight: 700;
      color: #475569;
      margin-left: 4px;
    }}
    .prob-box {{
      border: 1px solid #94A3B8;
      border-radius: 4px;
      padding: 6px 10px;
      margin: 6px 0;
      font-size: 12px;
      line-height: 1.55;
      background: #FAF8F3;
    }}
    .prob-choices {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 4px;
      font-size: 11.5px;
      margin-top: 6px;
      padding-top: 4px;
    }}
    .calc-space {{
      flex: 1;
      min-height: 25mm;
    }}
    
    /* Footer */
    .csat-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #080908;
      padding-top: 4px;
      font-size: 10px;
      color: #64748B;
    }}
    .csat-footer-left {{
      font-weight: 700;
      color: #334155;
    }}
    .csat-footer-center {{
      font-size: 12px;
      font-weight: 900;
      color: #080908;
    }}
    .csat-page-box {{
      padding: 0 6px;
    }}
    .csat-footer-right {{
      font-weight: 600;
    }}
    
    /* Solutions Styles */
    .sol-container {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .sol-card {{
      border: 1px solid #CBD5E1;
      border-radius: 8px;
      padding: 8px 10px;
      background: #FFFFFF;
    }}
    .sol-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #F1F5F9;
      padding-bottom: 4px;
      margin-bottom: 6px;
    }}
    .sol-meta-row {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .sol-qnum {{
      font-size: 13px;
      font-weight: 900;
      color: #EA580C;
    }}
    .sol-meta-tag {{
      font-size: 10.5px;
      font-weight: 700;
      color: #334155;
      background: #F1F5F9;
      padding: 1px 6px;
      border-radius: 3px;
    }}
    .sol-topic-tag {{
      font-size: 10px;
      font-weight: 600;
      color: #64748B;
    }}
    .sol-ans-badge {{
      font-size: 11px;
      font-weight: 900;
      color: #FFFFFF;
      background: #EA580C;
      padding: 2px 8px;
      border-radius: 4px;
    }}
    .sol-body {{
      display: flex;
      flex-direction: column;
      gap: 5px;
    }}
    .sol-grid-3way {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }}
    .sol-box {{
      border-radius: 5px;
      padding: 5px 8px;
      font-size: 10.5px;
      line-height: 1.5;
    }}
    .sol-box-title {{
      font-weight: 800;
      font-size: 10.5px;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 3px;
    }}
    .sol-stuck {{
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      color: #78350F;
    }}
    .sol-recipe {{
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      color: #1E3A8A;
    }}
    .sol-steps {{
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      color: #0F172A;
    }}
    .sol-defense {{
      background: #FFF7ED;
      border: 1px solid #FED7AA;
      color: #9A3412;
      font-weight: 700;
    }}
    .sol-diagram-box {{
      margin-top: 4px;
      border: 1px solid #E2E8F0;
      border-radius: 6px;
      overflow: hidden;
      max-height: 85px;
    }}
    
    /* Page 55: Quick Answer Key & Matrix */
    .section-title {{
      font-size: 13px;
      font-weight: 900;
      color: #080908;
      border-left: 3px solid #EA580C;
      padding-left: 6px;
      margin: 8px 0 6px 0;
    }}
    .ans-grid-108 {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 3px;
    }}
    .ans-cell {{
      border: 1px solid #CBD5E1;
      border-radius: 4px;
      padding: 3px 2px;
      text-align: center;
      background: #F8FAFC;
    }}
    .ans-cell-num {{
      display: block;
      font-size: 9px;
      font-weight: 800;
      color: #64748B;
    }}
    .ans-cell-val {{
      display: block;
      font-size: 10px;
      font-weight: 900;
      color: #EA580C;
    }}
    .matrix-table-wrap {{
      max-height: 155mm;
      overflow-y: hidden;
      border: 1px solid #CBD5E1;
      border-radius: 6px;
    }}
    .matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5px;
    }}
    .matrix-table th {{
      background: #F1F5F9;
      color: #1E293B;
      padding: 4px 6px;
      border: 1px solid #CBD5E1;
      font-weight: 800;
      text-align: left;
    }}
    .matrix-table td {{
      padding: 2.5px 6px;
      border: 1px solid #E2E8F0;
      color: #334155;
      line-height: 1.35;
    }}
    .matrix-table tr:nth-child(even) {{
      background: #FAFAFA;
    }}
  </style>
</head>
<body>
{''.join(html_pages)}

<script>
  document.addEventListener("DOMContentLoaded", function() {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ],
      throwOnError: false
    }});
  }});
</script>
</body>
</html>'''

target_nje_path = os.path.join(ROOT_DIR, 'templates', 'nje_exam_108.html')
with open(target_nje_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Successfully generated templates/nje_exam_108.html ({len(html_pages)} pages, {len(full_html)} bytes)!")
