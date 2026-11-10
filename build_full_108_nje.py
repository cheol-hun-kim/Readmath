"""
ReadMath 108-Je Masterpiece Final Exam Compiler
Authentic CSAT 2-Column Layout, 2-Solution Spacious Layout, KICE Diagonal Slash Page Box, and Zero-Duplicate SVG Diagrams
"""

import os
import sys
from mathdata.questions_part1 import PART_1_QUESTIONS
from mathdata.questions_part2 import PART_2_QUESTIONS
from mathdata.questions_part3 import PART_3_QUESTIONS
from mathdata.diagram_engine_108 import get_diagram_for_108
from csat_typesetter import normalize_csat_text

sys.stdout.reconfigure(encoding='utf-8')

ALL_QUESTIONS = PART_1_QUESTIONS + PART_2_QUESTIONS + PART_3_QUESTIONS
assert len(ALL_QUESTIONS) == 108, f"Expected 108 questions, got {len(ALL_QUESTIONS)}"

html_pages = []

TOTAL_PROB_PAGES = 27
TOTAL_SOL_PAGES = 54   # 108 questions / 2 per page = 54 spacious pages
TOTAL_MATRIX_PAGES = 2 # Page 82 (Quick Answer Key), Page 83 (36-Killer Matrix)
TOTAL_PAGES = TOTAL_PROB_PAGES + TOTAL_SOL_PAGES + TOTAL_MATRIX_PAGES  # 83 pages

# ==============================================================================
# HELPER: AUTHENTIC KICE DIAGONAL SLASH FOOTER
# ==============================================================================
def render_csat_footer(page_num: int, total_pages: int) -> str:
    return f'''<div class="csat-footer">
      <span class="csat-footer-left">ReadMath 1:1 약점 역추적 클리닉</span>
      <div class="csat-page-box">
        <svg viewBox="0 0 38 18" preserveAspectRatio="none">
          <line x1="0" y1="18" x2="38" y2="0" stroke="#000000" stroke-width="0.8" />
        </svg>
        <span class="curr-num">{page_num}</span>
        <span class="total-num">{total_pages}</span>
      </div>
      <span class="csat-copyright">2026학년도 대학수학능력시험 대비</span>
    </div>'''

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
        # Format problem choices
        choices_html = ""
        if q["choices"]:
            c_items = "".join([f'<span class="choice-item"><span class="choice-num">{c[:1]}</span> {c[2:]}</span>' for c in q["choices"]])
            choices_html = f'<div class="choices-row">{c_items}</div>'
        else:
            choices_html = ''
            
        q_item = f'''<div class="prob-card">
          <div class="prob-meta-row">
            <span class="prob-meta-badge">{q["meta"]}</span>
            <span class="prob-type-badge">{"5지선다형" if q["choices"] else "단답형"}</span>
          </div>
          <div class="prob-text">
            <b>{q["num"]}.</b> {normalize_csat_text(q["text"])}
          </div>
          {choices_html}
        </div>'''
        
        if i < 2:
            col_left_html += q_item
        else:
            col_right_html += q_item
            
    # Distinct Header Titles with exact calendar year provenance
    if page_num <= 9:
        header_title = "2025년 11월 수능 기출 킬러 & 심층·융합 36제 N제"
        sub_badge = "ReadMath 1:1 약점 역추적 시리즈 (평가원 원본 12제 + 정밀 변형 24제)"
    elif page_num <= 18:
        header_title = "2026년 6월 평가원 기출 킬러 & 심층·융합 36제 N제"
        sub_badge = "평가원 출제 DNA 원형 보존 & 실전 킬러 대비 36제"
    else:
        header_title = "2026년 9월 평가원 기출 킬러 & 심층·융합 36제 N제"
        sub_badge = "수능 D-9 초격차 파이널 총정리 36제"
        
    student_info = '''<div class="csat-student-info">
      <span>성명: ____________________</span>
      <span>수험번호: ____________________</span>
    </div>''' if page_num in [1, 10, 19] else ""
    
    p_html = f'''<div class="page">
    <div>
      <div class="csat-header">
        <div class="csat-header-top">
          <span class="csat-year-title">{header_title}</span>
          <span class="csat-sub-badge">{sub_badge}</span>
        </div>
        <div class="csat-header-mid">
          <div class="csat-period">제 2 교시</div>
          <div class="csat-subject-title">수 &nbsp; 학 &nbsp; 영 &nbsp; 역</div>
          <div class="csat-type-badge">파이널 N제</div>
        </div>
        {student_info}
      </div>
      <div class="csat-body">
        <div class="col-left">{col_left_html}</div>
        <div class="col-divider"></div>
        <div class="col-right">{col_right_html}</div>
      </div>
    </div>
    {render_csat_footer(page_num, TOTAL_PAGES)}
  </div>'''
    html_pages.append(p_html)

# ==============================================================================
# PART 4: 4-WAY COMPREHENSIVE SOLUTIONS (Pages 28 to 81, 2 Solutions Per Page)
# ==============================================================================
for s_idx in range(TOTAL_SOL_PAGES):
    sol_page_num = TOTAL_PROB_PAGES + s_idx + 1
    q_start = s_idx * 2
    q_page = ALL_QUESTIONS[q_start:q_start+2]
    
    cards_html = ""
    for q in q_page:
        svg_code = get_diagram_for_108(q["num"])
        # Strictly only render diagram container if an actual mathematical SVG is defined
        svg_block = f'<div class="sol-diagram-box">{svg_code}</div>' if svg_code else ""
        
        cards_html += f'''<div class="sol-card">
          <div class="sol-header">
            <div class="sol-meta-row">
              <span class="sol-num-badge">{q["num"]}번</span>
              <span class="sol-provenance">{q["meta"]}</span>
              <span class="sol-topic-title">{q["topic"]}</span>
            </div>
            <span class="sol-ans-pill">정답 {q["ans"]}</span>
          </div>
          
          <div class="sol-body">
            <div class="sol-grid-3way">
              <div class="sol-box sol-box-trap">
                <div class="sol-box-title">⚠️ [시험장 3초 컷 오답 함정 분석]</div>
                <div>{normalize_csat_text(q.get("stuck", ""))}</div>
              </div>
              <div class="sol-box sol-box-key">
                <div class="sol-box-title">🔑 [동일 출제 원리 & 핵심 키]</div>
                <div>{normalize_csat_text(q.get("recipe", ""))}</div>
              </div>
            </div>
            
            <div class="sol-box sol-box-steps">
              <div class="sol-box-title">📝 [단계별 논리적 풀이]</div>
              <div>{normalize_csat_text(q.get("steps", ""))}</div>
            </div>
            
            <div class="sol-box sol-box-defense">
              <div class="sol-box-title">🛡️ [실전 오답 방어 행동 공식]</div>
              <div>{normalize_csat_text(q.get("defense", ""))}</div>
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
          <div class="csat-subject-title">수 &nbsp; 학 &nbsp; 영 &nbsp; 역</div>
          <div class="csat-type-badge">해설지</div>
        </div>
      </div>
      <div class="sol-container">
        {cards_html}
      </div>
    </div>
    {render_csat_footer(sol_page_num, TOTAL_PAGES)}
  </div>'''
    html_pages.append(s_html)

# ==============================================================================
# PART 5: QUICK ANSWER KEY (Page 82)
# ==============================================================================
ans_cells = "".join([f'''<div class="ans-cell">
  <span class="ans-cell-num">{q["num"]}</span>
  <span class="ans-cell-val">{q["ans"]}</span>
</div>''' for q in ALL_QUESTIONS])

page_82_html = f'''<div class="page">
  <div>
    <div class="csat-header">
      <div class="csat-header-top">
        <span class="csat-year-title">ReadMath 수능 D-9 초격차 파이널 108제 빠른 정답표</span>
        <span class="csat-sub-badge">1~108번 전 문항 공식 정답 일람표</span>
      </div>
      <div class="csat-header-mid">
        <div class="csat-period">파이널 총정리</div>
        <div class="csat-subject-title">빠 &nbsp; 른 &nbsp; 정 &nbsp; 답 &nbsp; 표</div>
        <div class="csat-type-badge">정답표</div>
      </div>
    </div>
    
    <div style="margin-top: 15px;">
      <h3 class="section-title">108제 전 문항 빠른 정답표 (1번 ~ 108번)</h3>
      <div class="ans-grid-108">
        {ans_cells}
      </div>
      
      <div class="quick-summary-box" style="margin-top: 25px;">
        <h4>💡 ReadMath 파이널 N제 채점 및 회고 가이드</h4>
        <p>1. 틀린 문항은 단순 계산 실수가 아닌 <b>'시험장 3초 컷 오답 함정'</b> 중 어떤 패턴에 걸렸는지 4-Way 해설지에서 확인하십시오.</p>
        <p>2. 동일 레시피 변형 문제에서 또다시 막혔다면 개념 발원지가 결손된 상태이므로 뒷면의 <b>'36대 킬러 출제 테마 & 오답 방어 매트릭스'</b>를 참조하여 행동 공식을 암기하십시오.</p>
      </div>
    </div>
  </div>
  {render_csat_footer(82, TOTAL_PAGES)}
</div>'''

html_pages.append(page_82_html)

# ==============================================================================
# PART 6: 36-THEME DIAGNOSTIC MATRIX (Page 83)
# ==============================================================================
theme_rows = ""
for set_idx in range(36):
    q_orig = ALL_QUESTIONS[set_idx * 3]
    theme_rows += f'''<tr>
      <td class="text-center font-bold">{set_idx+1}</td>
      <td class="font-bold">{q_orig["meta"].replace(" [원본]", "")}</td>
      <td>{q_orig["topic"]}</td>
      <td class="text-center font-mono">{set_idx*3+1}, {set_idx*3+2}, {set_idx*3+3}번</td>
      <td class="text-xs text-slate-600">{q_orig.get("defense", "")[:28]}...</td>
    </tr>'''

page_83_html = f'''<div class="page">
  <div>
    <div class="csat-header">
      <div class="csat-header-top">
        <span class="csat-year-title">ReadMath 수능 D-9 초격차 파이널 36대 킬러 진단 매트릭스</span>
        <span class="csat-sub-badge">평가원 출제 DNA 원형 보존 및 3초 컷 행동 공식 총정리</span>
      </div>
      <div class="csat-header-mid">
        <div class="csat-period">약점 역추적</div>
        <div class="csat-subject-title">출 &nbsp; 제 &nbsp; 매 &nbsp; 트 &nbsp; 릭 &nbsp; 스</div>
        <div class="csat-type-badge">진단표</div>
      </div>
    </div>
    
    <div style="margin-top: 8px;">
      <h3 class="section-title">36대 킬러 테마별 출제 원형 & 처방 매트릭스</h3>
      <div class="matrix-table-wrap">
        <table class="matrix-table">
          <thead>
            <tr>
              <th style="width: 28px;">세트</th>
              <th style="width: 135px;">출제 원형</th>
              <th style="width: 145px;">핵심 테마 & 개념</th>
              <th style="width: 70px;">문항 번호</th>
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
  {render_csat_footer(83, TOTAL_PAGES)}
</div>'''

html_pages.append(page_83_html)

# ==============================================================================
# FULL HTML WRAPPER WITH PRECISE CSAT STYLING
# ==============================================================================
all_pages_html = "\n".join(html_pages)

full_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>ReadMath 수능 D-9 초격차 파이널 108제 마스터피스 N제</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap');
    
    @page {{
      size: 210mm 297mm;
      margin: 0;
    }}
    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      color: #080908;
      background: #F1F5F9;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      word-break: keep-all;
      overflow-wrap: break-word;
    }}
    
    .page {{
      width: 182mm;
      height: 268mm;
      margin: 10mm auto;
      background: #FFFFFF;
      padding: 8mm 10mm 8mm 10mm;
      position: relative;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    @media print {{
      body {{ background: transparent; }}
      .page {{
        margin: 0 auto;
        padding: 8mm 10mm 8mm 10mm;
        box-shadow: none;
        width: 182mm;
        height: 268mm;
        overflow: hidden;
      }}
    }}
    
    /* CSAT Header */
    .csat-header {{
      border-bottom: 2px solid #080908;
      padding-bottom: 5px;
      margin-bottom: 8px;
    }}
    .csat-header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 3px;
    }}
    .csat-year-title {{
      font-size: 11.5px;
      color: #080908;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      letter-spacing: -0.3px;
    }}
    .csat-sub-badge {{
      font-size: 9.5px;
      color: #EA580C;
      font-weight: 800;
      background: #FFF7ED;
      padding: 1px 6px;
      border-radius: 4px;
      border: 1px solid #FFEDD5;
    }}
    .csat-header-mid {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 2px 0;
    }}
    .csat-period {{
      font-size: 14px;
      font-weight: 800;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
    }}
    .csat-subject-title {{
      font-size: 20px;
      font-weight: 900;
      letter-spacing: 4px;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
    }}
    .csat-type-badge {{
      border: 1px solid #080908;
      padding: 1px 8px;
      font-size: 11px;
      font-weight: 800;
      border-radius: 3px;
    }}
    .csat-student-info {{
      display: flex;
      justify-content: flex-end;
      gap: 24px;
      font-size: 10px;
      margin-top: 3px;
      font-family: 'Nanum Myeongjo', serif;
      color: #475569;
    }}
    
    /* 2-Column CSAT Layout */
    .csat-body {{
      display: flex;
      justify-content: space-between;
      position: relative;
    }}
    .col-left, .col-right {{
      width: 48.2%;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .col-divider {{
      position: absolute;
      left: 50%;
      top: 0;
      bottom: 0;
      width: 1px;
      background: #E2E8F0;
      transform: translateX(-50%);
    }}
    
    /* Problem Card */
    .prob-card {{
      border: 1px solid #F1F5F9;
      border-radius: 6px;
      padding: 8px 9px;
      background: #FFFFFF;
      min-height: 100mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .prob-meta-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 5px;
    }}
    .prob-meta-badge {{
      font-size: 9px;
      font-weight: 700;
      color: #334155;
      background: #F1F5F9;
      padding: 1px 5px;
      border-radius: 3px;
    }}
    .prob-type-badge {{
      font-size: 8.5px;
      color: #64748B;
      border: 1px solid #E2E8F0;
      padding: 1px 4px;
      border-radius: 2px;
    }}
    .prob-text {{
      font-size: 11px;
      line-height: 1.6;
      color: #080908;
      flex-grow: 1;
    }}
    .choices-row {{
      display: flex;
      justify-content: space-between;
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px dashed #E2E8F0;
      font-size: 10px;
    }}
    .choice-item {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}
    .choice-num {{
      font-weight: 700;
      color: #080908;
    }}
    .short-ans-box {{
      margin-top: 8px;
      border: 1px dashed #CBD5E1;
      border-radius: 4px;
      padding: 6px;
      text-align: center;
      font-size: 9px;
      color: #94A3B8;
      background: #F8FAFC;
    }}
    
    /* Authentic CSAT & Editorial Footers */
    .csat-footer {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #CBD5E1;
      padding: 0 10px;
      font-size: 10px;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #475569;
    }}
    .csat-footer-left {{
      font-size: 10px;
      font-weight: 700;
      color: #334155;
      font-family: 'Nanum Myeongjo', serif;
    }}
    .csat-copyright {{
      font-size: 9px;
      color: #64748B;
      font-family: 'Nanum Myeongjo', serif;
    }}

    /* Authentic KICE Diagonal Slash Page Box (Centered) */
    .csat-page-box {{
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      width: 38px;
      height: 18px;
      border: 0.8px solid #000000;
      background: #FFFFFF;
    }}
    .csat-page-box svg {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }}
    .csat-page-box .curr-num {{
      position: absolute;
      top: -1px;
      left: 4px;
      font-size: 11px;
      font-weight: 800;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #000000;
      line-height: 1;
    }}
    .csat-page-box .total-num {{
      position: absolute;
      bottom: 1px;
      right: 4px;
      font-size: 10px;
      font-weight: 700;
      font-family: 'Nanum Myeongjo', 'Batang', serif;
      color: #000000;
      line-height: 1;
    }}
    
    /* Solutions Styles (2 Spacious Solutions Per Page) */
    .sol-container {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .sol-card {{
      border: 1px solid #CBD5E1;
      border-radius: 8px;
      padding: 9px 12px;
      background: #FFFFFF;
    }}
    .sol-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #F1F5F9;
      padding-bottom: 5px;
      margin-bottom: 6px;
    }}
    .sol-meta-row {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .sol-num-badge {{
      font-size: 11.5px;
      font-weight: 900;
      color: #FF5A1F;
    }}
    .sol-provenance {{
      font-size: 9.5px;
      font-weight: 700;
      color: #475569;
      background: #F1F5F9;
      padding: 1px 5px;
      border-radius: 3px;
    }}
    .sol-topic-title {{
      font-size: 10px;
      color: #64748B;
    }}
    .sol-ans-pill {{
      font-size: 10.5px;
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
      gap: 4px;
    }}
    .sol-box-trap {{
      background: #FFFBEB;
      border: 1px solid #FEF3C7;
      color: #92400E;
    }}
    .sol-box-key {{
      background: #EFF6FF;
      border: 1px solid #DBEAFE;
      color: #1E40AF;
    }}
    .sol-box-steps {{
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      color: #080908;
    }}
    .sol-steps-list {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .sol-box-defense {{
      background: #FFF7ED;
      border: 1px solid #FFEDD5;
      color: #9A3412;
      font-weight: 700;
    }}
    
    /* Non-clipped, Auto-height Diagram Box */
    .sol-diagram-box {{
      margin-top: 5px;
      border: 1px solid #E2E8F0;
      border-radius: 6px;
      background: #FFFFFF;
      width: 100%;
      height: auto;
      overflow: visible;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 3px;
    }}
    .sol-diagram-box svg {{
      max-width: 100%;
      height: auto;
      max-height: 155px;
      display: block;
    }}
    
    /* Page 82 & 83: Quick Answer Key & Matrix */
    .section-title {{
      font-size: 12.5px;
      font-weight: 800;
      color: #080908;
      border-left: 3px solid #EA580C;
      padding-left: 6px;
      margin-bottom: 8px;
    }}
    .ans-grid-108 {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 3px;
      font-size: 9px;
    }}
    .ans-cell {{
      border: 1px solid #E2E8F0;
      border-radius: 3px;
      padding: 2px 1px;
      text-align: center;
      background: #FFFFFF;
    }}
    .ans-cell-num {{
      display: block;
      font-size: 7.5px;
      color: #64748B;
    }}
    .ans-cell-val {{
      display: block;
      font-weight: 800;
      color: #080908;
    }}
    .quick-summary-box {{
      border: 1px solid #CBD5E1;
      border-radius: 6px;
      padding: 12px 16px;
      background: #F8FAFC;
      font-size: 11px;
      line-height: 1.6;
    }}
    .quick-summary-box h4 {{
      font-size: 12px;
      font-weight: 800;
      color: #080908;
      margin-bottom: 6px;
    }}
    
    .matrix-table-wrap {{
      border: 1px solid #CBD5E1;
      border-radius: 6px;
      overflow: hidden;
    }}
    .matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8px;
    }}
    .matrix-table th {{
      background: #F1F5F9;
      color: #334155;
      font-weight: 800;
      padding: 2px 4px;
      border-bottom: 1px solid #CBD5E1;
      border-right: 1px solid #E2E8F0;
      text-align: left;
    }}
    .matrix-table td {{
      padding: 1.5px 4px;
      border-bottom: 1px solid #F1F5F9;
      border-right: 1px solid #F1F5F9;
      color: #080908;
      line-height: 1.25;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .matrix-table tr:nth-child(even) {{
      background: #F8FAFC;
    }}
  </style>
</head>
<body>
  {all_pages_html}
  
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      renderMathInElement(document.body, {{
        delimiters: [
          {{left: "$$", right: "$$", display: true}},
          {{left: "$", right: "$", display: false}}
        ],
        throwOnError: false
      }});
    }});
  </script>
</body>
</html>'''

with open("templates/nje_exam_108.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Successfully generated templates/nje_exam_108.html ({len(html_pages)} pages, {len(full_html)} bytes)!")
