import os, sys

sys.stdout.reconfigure(encoding='utf-8')

landing_path = "landing.html"
with open(landing_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block_start = '<!-- 2 Downloadable Preview Showcase Cards -->'
old_block_end = '<!-- ================= FOUNDER\'S STORY & 300-STUDENT TRACTION ================= -->'

start_idx = content.find(old_block_start)
end_idx = content.find(old_block_end)

if start_idx == -1 or end_idx == -1:
    print(f"Error: Indices not found. start={start_idx}, end={end_idx}")
    sys.exit(1)

new_cards_html = '''<!-- 2 Downloadable Preview Showcase Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 pt-4 items-stretch">
        
        <!-- Book 1: 개별 맞춤 개념서 -->
        <div class="bg-white rounded-3xl p-7 sm:p-8 border border-[#E2D9CC] shadow-md flex flex-col justify-between h-full relative overflow-hidden group hover:border-[#EA580C]/40 hover:shadow-lg transition">
          <div class="space-y-4">
            <div class="flex items-center justify-between h-7">
              <span class="px-3 py-1 rounded-full bg-orange-50 text-[#EA580C] border border-orange-200/80 text-[11px] font-black tracking-wide">
                맞춤 개념서 샘플 (PDF)
              </span>
              <span class="text-xs text-stone-500 font-bold">A4 에디토리얼 프리미엄 조판</span>
            </div>

            <div class="space-y-2">
              <h3 class="text-xl sm:text-2xl font-black text-[#080908] break-keep leading-tight h-14 flex flex-col justify-center">
                <span>ReadMath 1:1 약점 역추적</span>
                <span>개별 맞춤 개념서</span>
              </h3>
              <p class="text-xs sm:text-sm text-[#57534E] leading-relaxed break-keep h-[4.25rem] flex items-start" style="text-wrap: pretty;">
                오직 학생 질문에서 역추적된 결손 개념만을 핀포인트로 편철한 세상에 단 한 권뿐인 맞춤서입니다. 
                수학적 기하 직관 다이어그램과 시험장 3초 컷 오답 방어 행동 공식이 결합되어 있습니다.
              </p>
            </div>

            <!-- Features Pill List -->
            <div class="space-y-2.5 pt-3 border-t border-[#F2ECE1] text-xs text-[#44403C]">
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#EA580C] shrink-0"></i>
                <span>학생 질문 역추적 기반 핀포인트 약점 개념 수록</span>
              </div>
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#EA580C] shrink-0"></i>
                <span>삼차함수 비율 관계, 조건부확률 표본공간 분할 시각 도해</span>
              </div>
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#EA580C] shrink-0"></i>
                <span>함정에 빠지지 않는 실전 오답 방어 행동 공식 가이드</span>
              </div>
            </div>
          </div>

          <div class="pt-6">
            <a href="/downloads/ReadMath_개별맞춤_개념서_Sample.pdf" download="ReadMath_개별맞춤_개념서_Sample.pdf" class="w-full py-4 px-6 rounded-2xl bg-[#EA580C] hover:bg-[#C2410C] text-white font-extrabold text-sm flex items-center justify-center gap-2 shadow-lg shadow-orange-900/10 active:scale-95 transition">
              <i data-lucide="download" class="w-4 h-4 text-white"></i>
              <span>맞춤 개념서 맛보기 PDF 다운로드 (무료)</span>
            </a>
            <div class="text-center mt-2.5 text-[11px] text-stone-500 h-5">
              * 실제 인쇄 및 태블릿 필기가 가능한 벡터급 고해상도 PDF
            </div>
          </div>
        </div>

        <!-- Book 2: 2025 수능 킬러 & 동일 레시피 변형 24제 N제 -->
        <div class="bg-white rounded-3xl p-7 sm:p-8 border border-[#E2D9CC] shadow-md flex flex-col justify-between h-full relative overflow-hidden group hover:border-[#EA580C]/40 hover:shadow-lg transition">
          <div class="space-y-4">
            <div class="flex items-center justify-between h-7">
              <span class="px-3 py-1 rounded-full bg-orange-50 text-[#EA580C] border border-orange-200/80 text-[11px] font-black tracking-wide">
                수능 실전 N제 샘플 (PDF)
              </span>
              <span class="text-xs text-stone-500 font-bold">실제 평가원 수능 시험지 2단 구성</span>
            </div>

            <div class="space-y-2">
              <h3 class="text-xl sm:text-2xl font-black text-[#080908] break-keep leading-tight h-14 flex flex-col justify-center">
                <span>2025 수능 킬러 & 동일</span>
                <span>레시피 변형 24제 N제</span>
              </h3>
              <p class="text-xs sm:text-sm text-[#57534E] leading-relaxed break-keep h-[4.25rem] flex items-start" style="text-wrap: pretty;">
                2025 수능 최고난도 킬러 12제와 평가원 DNA를 100% 보존한 1:1 동일 레시피 변형 12제로 구성된 실전 시험지입니다. 
                1~24번 전 문항의 4-Way 심층 입체 해설지가 완벽 수록되어 있습니다.
              </p>
            </div>

            <!-- Features Pill List -->
            <div class="space-y-2.5 pt-3 border-t border-[#F2ECE1] text-xs text-[#44403C]">
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#EA580C] shrink-0"></i>
                <span>2025 수능 공통 15·21·22번, 미적·기하·확통 킬러 12제 수록</span>
              </div>
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#EA580C] shrink-0"></i>
                <span>알맹이는 같고 껍데기만 바꾼 1:1 쌍둥이 변형 12제 수록</span>
              </div>
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#EA580C] shrink-0"></i>
                <span>막힌 이유 + 동일 레시피 + 단계별 풀이 4-Way 해설지 완벽 탑재</span>
              </div>
            </div>
          </div>

          <div class="pt-6">
            <a href="/downloads/ReadMath_2025수능킬러_변형24제_N제.pdf" download="ReadMath_2025수능킬러_변형24제_N제.pdf" class="w-full py-4 px-6 rounded-2xl bg-[#EA580C] hover:bg-[#C2410C] text-white font-extrabold text-sm flex items-center justify-center gap-2 shadow-lg shadow-orange-900/10 active:scale-95 transition">
              <i data-lucide="download" class="w-4 h-4 text-white"></i>
              <span>24제 N제 시험지+해설 PDF 다운로드 (무료)</span>
            </a>
            <div class="text-center mt-2.5 text-[11px] text-stone-500 h-5">
              * 실제 수능 시험지 규격 2단 레이아웃 및 1~24번 전 문항 입체 해설 수록
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  '''

updated_content = content[:start_idx] + new_cards_html + content[end_idx:]

with open(landing_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("SUCCESS: Harmonized showcase cards in landing.html with exact 2-line title alignment!")
