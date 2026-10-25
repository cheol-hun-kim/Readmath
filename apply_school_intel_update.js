const fs = require('fs');
const path = require('path');

const ROOT_DIR = __dirname;
const DB_PATH = path.join(ROOT_DIR, 'school_teacher_intelligence.json');
const PREVIEW_PATH = path.join(ROOT_DIR, 'preview.html');
const ADMIN_PATH = path.join(ROOT_DIR, 'admin.html');

const schoolDb = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));

// Build 46-school options HTML
const bundangSchools = [
  { key: 'naksaeng', name: '낙생고등학교' },
  { key: 'daejin', name: '분당대진고등학교' },
  { key: 'seohyun', name: '서현고등학교' },
  { key: 'bundang', name: '분당고등학교' },
  { key: 'jungang', name: '분당중앙고등학교' },
  { key: 'bopyeong', name: '보평고등학교' },
  { key: 'yatap', name: '야탑고등학교' },
  { key: 'hansol', name: '한솔고등학교' },
  { key: 'neulpureun', name: '늘푸른고등학교' },
  { key: 'yeongdeok', name: '분당영덕여자고등학교' },
  { key: 'bulgok', name: '불곡고등학교' },
  { key: 'sunae', name: '수내고등학교' },
  { key: 'taewon', name: '태원고등학교' },
  { key: 'songlim', name: '송림고등학교' },
  { key: 'dolma', name: '돌마고등학교' },
  { key: 'woonjoong', name: '운중고등학교' },
  { key: 'pangyo', name: '판교고등학교' },
  { key: 'ewoo', name: '이우고등학교' },
  { key: 'seongnam_fl', name: '성남외국어고등학교' }
];

const sujiSchools = [
  { key: 'suji', name: '수지고등학교' },
  { key: 'pungdeok', name: '풍덕고등학교' },
  { key: 'seowon', name: '서원고등학교' },
  { key: 'sanghyeon', name: '상현고등학교' },
  { key: 'shinbong', name: '신봉고등학교' },
  { key: 'hongcheon', name: '홍천고등학교' },
  { key: 'seongbok', name: '성복고등학교' },
  { key: 'jukjeon', name: '죽전고등학교' },
  { key: 'daeji', name: '대지고등학교' },
  { key: 'hyeonam', name: '현암고등학교' }
];

const giheungSchools = [
  { key: 'baekhyeon', name: '용인백현고등학교' },
  { key: 'giheung', name: '기흥고등학교' },
  { key: 'bora', name: '보라고등학교' },
  { key: 'dongbaek', name: '동백고등학교' },
  { key: 'chodang', name: '초당고등학교' },
  { key: 'singal', name: '신갈고등학교' },
  { key: 'heungdeok', name: '흥덕고등학교' },
  { key: 'seocheon', name: '서천고등학교' },
  { key: 'cheongdeok', name: '청덕고등학교' },
  { key: 'guseong', name: '구성고등학교' }
];

const cheoinSchools = [
  { key: 'yongin', name: '용인고등학교' },
  { key: 'taesung', name: '태성고등학교' },
  { key: 'pogok', name: '포곡고등학교' },
  { key: 'baekam', name: '백암고등학교' },
  { key: 'samgye', name: '삼계고등학교' },
  { key: 'gorim', name: '고림고등학교' },
  { key: 'hufs', name: '외대부고(한국외대부설고)' }
];

function generateSchoolOptions(defaultSelectedKey = 'naksaeng', includeCustom = false) {
  let html = '';
  html += `                <optgroup label="성남시 분당구 (19개교)">\n`;
  bundangSchools.forEach(s => {
    const sel = s.key === defaultSelectedKey ? ' selected' : '';
    html += `                  <option value="${s.key}"${sel}>${s.name}</option>\n`;
  });
  html += `                </optgroup>\n`;

  html += `                <optgroup label="용인시 수지구 (10개교)">\n`;
  sujiSchools.forEach(s => {
    const sel = s.key === defaultSelectedKey ? ' selected' : '';
    html += `                  <option value="${s.key}"${sel}>${s.name}</option>\n`;
  });
  html += `                </optgroup>\n`;

  html += `                <optgroup label="용인시 기흥구 (10개교)">\n`;
  giheungSchools.forEach(s => {
    const sel = s.key === defaultSelectedKey ? ' selected' : '';
    html += `                  <option value="${s.key}"${sel}>${s.name}</option>\n`;
  });
  html += `                </optgroup>\n`;

  html += `                <optgroup label="용인시 처인구 (7개교)">\n`;
  cheoinSchools.forEach(s => {
    const sel = s.key === defaultSelectedKey ? ' selected' : '';
    html += `                  <option value="${s.key}"${sel}>${s.name}</option>\n`;
  });
  html += `                </optgroup>`;

  if (includeCustom) {
    html += `\n                <option value="custom">+ 기타 고교 직접입력</option>`;
  }
  return html;
}

// -------------------------------------------------------------
// 1. UPDATE PREVIEW.HTML
// -------------------------------------------------------------
let previewHtml = fs.readFileSync(PREVIEW_PATH, 'utf8');

// Replace #dash-school-select options
const dashSelectRegex = /(<select id="dash-school-select"[^>]*>)([\s\S]*?)(<\/select>)/;
if (dashSelectRegex.test(previewHtml)) {
  previewHtml = previewHtml.replace(dashSelectRegex, `$1\n${generateSchoolOptions('naksaeng', false)}\n              $3`);
  console.log('✅ Updated #dash-school-select in preview.html with 46 high schools');
} else {
  console.warn('⚠️ Could not find #dash-school-select in preview.html');
}

// Replace #intel-school-select options
const intelSelectRegex = /(<select id="intel-school-select"[^>]*>)([\s\S]*?)(<\/select>)/;
if (intelSelectRegex.test(previewHtml)) {
  previewHtml = previewHtml.replace(intelSelectRegex, `$1\n${generateSchoolOptions('naksaeng', true)}\n              $3`);
  console.log('✅ Updated #intel-school-select in preview.html with 46 high schools + custom');
} else {
  console.warn('⚠️ Could not find #intel-school-select in preview.html');
}

// Replace line 2857 static prescription message
previewHtml = previewHtml.replace(
  /<strong class="text-amber-300">긴급 처방:<\/strong>\s*담당 수학교사\(박OO 선생님\)는\s*<span class="text-indigo-300 font-bold">\[수능특강 Level 3 변형\]<\/span>에서 4문항을 출제합니다\.\s*지금 바로 시험준비 탭에서 맞춤 시험지를 생성하여 집중 훈련하세요\./,
  '<strong class="text-amber-300">내신 대비 전략:</strong> 소속 고교 기출 분석 기반 고난도 변형 문항 및 오답 취약 유형을 집중 훈련하여 1등급 진입을 달성하세요.'
);

// Replace line 22090 placeholder
previewHtml = previewHtml.replace(
  'placeholder="예: 박OO 선생님 (1~4반 담당), 최OO 선생님 (5~8반 담당)"',
  'placeholder="예: 홍길동 선생님 (1~4반 담당), 이수학 선생님 (5~8반 담당)"'
);

// Replace TEACHER_INTEL_STATS and renderSchoolIntelDashboard
const intelDashboardBlock = `    // ================= SCHOOL INTEL DASHBOARD & GRADE PREDICTOR ENGINE =================
    function renderSchoolIntelDashboard() {
      const schoolSelect = document.getElementById('dash-school-select');
      const gradeSelect = document.getElementById('dash-grade-select');
      const schoolKey = schoolSelect?.value || 'naksaeng';
      const gradeKey = gradeSelect?.value || '2';

      const schoolData = (typeof SCHOOL_INTEL_DB !== 'undefined' && SCHOOL_INTEL_DB.schools) ? SCHOOL_INTEL_DB.schools[schoolKey] : null;
      const schoolName = schoolData?.name || '소속 고교';

      const titleEl = document.getElementById('dash-school-title');
      if (titleEl) {
        titleEl.textContent = \`\${schoolName} \${gradeKey}학년 수학교사진 출제 경향 & 내신 예측\`;
      }

      // Populate Teachers list or Honest Archive Status
      const teachersContainer = document.getElementById('dash-teachers-container');
      const gradeData = schoolData?.grades?.[gradeKey];
      const verifiedTeachers = gradeData?.teachers || [];

      if (teachersContainer) {
        if (verifiedTeachers.length > 0) {
          teachersContainer.innerHTML = verifiedTeachers.map((t, idx) => \`
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                  <span class="font-extrabold text-amber-300 text-xs">\${t.name} 선생님</span>
                  <span class="text-[10px] text-slate-400">(\${t.role})</span>
                </div>
                <span class="px-2 py-0.5 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-300 text-[10px] font-black flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  연계 분석완료
                </span>
              </div>
              <div class="text-[11px] text-slate-300">
                <span class="text-slate-400 font-medium">선호 출제원: </span>
                <span class="text-indigo-300 font-bold">\${t.source}</span>
              </div>
              <p class="text-[10.5px] text-slate-400 italic pt-1 border-t border-slate-800/80">
                "\${t.style}"
              </p>
            </div>
          \`).join('');
        } else if (schoolData?.verified_exams && schoolData.verified_exams.length > 0) {
          teachersContainer.innerHTML = \`
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2.5 text-xs">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                  <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                  <span class="font-extrabold text-emerald-400 text-xs">\${schoolName} 실기출 족보 보유</span>
                </div>
                <span class="px-2 py-0.5 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-300 text-[10px] font-black">
                  \${schoolData.exam_files_count}건 정밀 분석 완료
                </span>
              </div>
              <p class="text-[11px] text-slate-300 leading-relaxed">
                수학 자료실에 등록된 \${schoolName} 실제 내신 기출 데이터를 기반으로 문항 변형 및 출제 알고리즘이 가동 중입니다:
              </p>
              <div class="space-y-1.5">
                \${schoolData.verified_exams.map(e => \`
                  <div class="p-2 rounded-lg bg-indigo-950/40 border border-indigo-500/30 flex items-center justify-between text-[11px]">
                    <span class="text-indigo-200 font-medium truncate">• \${e}</span>
                    <span class="text-[9.5px] px-1.5 py-0.2 rounded bg-indigo-500/20 text-indigo-300 font-bold shrink-0 ml-1">연계 분석완료</span>
                  </div>
                \`).join('')}
              </div>
              <div class="pt-2 border-t border-slate-800 flex items-center justify-between text-[10.5px]">
                <span class="text-slate-400">2026 출제 선생님 추가 제보 시 즉시 연동</span>
                <button type="button" onclick="openCrowdsourceModal('teacher')" class="text-amber-400 hover:text-amber-300 font-bold flex items-center gap-1">
                  <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i> 선생님 직접 제보
                </button>
              </div>
            </div>
          \`;
        } else {
          teachersContainer.innerHTML = \`
            <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-center space-y-2.5 text-xs">
              <div class="w-10 h-10 rounded-full bg-slate-900 border border-slate-700 flex items-center justify-center text-slate-400 mx-auto">
                <i data-lucide="clipboard-list" class="w-5 h-5 text-indigo-400"></i>
              </div>
              <div class="space-y-1">
                <h4 class="font-bold text-slate-200 text-xs">\${schoolName} \${gradeKey}학년 출제 교사진 정보 접수 대기 중</h4>
                <p class="text-[11px] text-slate-400 leading-relaxed">
                  재학생 제보를 통해 담당 선생님의 출제 스타일과 부교재(수특, 모의고사, 학평 등)를 등록해 주시면, 맞춤 족보와 예상 킬러 문항이 실시간으로 동기화됩니다.
                </p>
              </div>
              <button type="button" onclick="openCrowdsourceModal('teacher')" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md transition mx-auto">
                <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i> 우리 학교 선생님 / 부교재 제보하기
              </button>
            </div>
          \`;
        }
      }

      // Update Weakness Impact & Grade Simulator based on Grade
      const weaknessUnitEl = document.getElementById('dash-weakness-unit');
      const weaknessRatioEl = document.getElementById('dash-weakness-ratio');
      const prescriptionTextEl = document.getElementById('dash-prescription-text');

      const isGrade1 = gradeKey === '1';
      if (weaknessUnitEl) {
        weaknessUnitEl.textContent = isGrade1 ? '다항식 나머지정리 & 이차함수 킬러' : '지수·로그 킬러 & 수열 점화식';
      }
      if (weaknessRatioEl) {
        weaknessRatioEl.textContent = isGrade1 ? '32점' : '35점';
      }
      if (prescriptionTextEl) {
        if (schoolData?.verified_exams && schoolData.verified_exams.length > 0) {
          prescriptionTextEl.innerHTML = \`
            <strong class="text-amber-300">내신 대비 전략:</strong> \${schoolName} \${gradeKey}학년 실기출 분석 기반, 고난도 변형 문항 및 오답 취약 유형을 집중 배치하여 1등급 진입 훈련을 시작하세요.
          \`;
        } else {
          prescriptionTextEl.innerHTML = \`
            <strong class="text-amber-300">내신 대비 전략:</strong> \${schoolName} \${gradeKey}학년 교육과정 핵심 기출 변형 문항을 시험준비 탭에서 즉시 생성하여 1등급 안정권 진입을 훈련하세요.
          \`;
        }
      }

      lucide.createIcons();
    }`;

// Replace the entire block from TEACHER_INTEL_STATS down to end of renderSchoolIntelDashboard
const oldStatsRegex = /\/\/ ================= SCHOOL INTEL DASHBOARD & GRADE PREDICTOR ENGINE =================[\s\S]*?lucide\.createIcons\(\);\s*\}/;
if (oldStatsRegex.test(previewHtml)) {
  previewHtml = previewHtml.replace(oldStatsRegex, intelDashboardBlock);
  console.log('✅ Replaced TEACHER_INTEL_STATS & renderSchoolIntelDashboard in preview.html');
} else {
  console.warn('⚠️ Could not match oldStatsRegex in preview.html');
}

// Replace DEFAULT_SCHOOL_INTEL_DB with clean 46-school DB
const dbRegex = /const DEFAULT_SCHOOL_INTEL_DB = \{[\s\S]*?\};\s*let SCHOOL_INTEL_DB =/m;
if (dbRegex.test(previewHtml)) {
  previewHtml = previewHtml.replace(dbRegex, `const DEFAULT_SCHOOL_INTEL_DB = ${JSON.stringify(schoolDb)};\n    let SCHOOL_INTEL_DB =`);
  console.log('✅ Replaced DEFAULT_SCHOOL_INTEL_DB in preview.html with 46 pure schools');
} else {
  console.warn('⚠️ Could not match dbRegex in preview.html');
}

fs.writeFileSync(PREVIEW_PATH, previewHtml, 'utf8');
console.log('🎉 preview.html updated successfully');

// -------------------------------------------------------------
// 2. UPDATE ADMIN.HTML
// -------------------------------------------------------------
let adminHtml = fs.readFileSync(ADMIN_PATH, 'utf8');

// Replace #intel-filter-school options
const adminFilterRegex = /(<select id="intel-filter-school"[^>]*>)([\s\S]*?)(<\/select>)/;
if (adminFilterRegex.test(adminHtml)) {
  const filterOptions = `                <option value="all">전체 고등학교 (46개교)</option>\n${generateSchoolOptions('naksaeng', false)}`;
  adminHtml = adminHtml.replace(adminFilterRegex, `$1\n${filterOptions}\n            $3`);
  console.log('✅ Updated #intel-filter-school in admin.html with 46 high schools');
}

// Replace #modal-intel-school options
const adminModalSchoolRegex = /(<select id="modal-intel-school"[^>]*>)([\s\S]*?)(<\/select>)/;
if (adminModalSchoolRegex.test(adminHtml)) {
  adminHtml = adminHtml.replace(adminModalSchoolRegex, `$1\n${generateSchoolOptions('naksaeng', false)}\n            $3`);
  console.log('✅ Updated #modal-intel-school in admin.html with 46 high schools');
}

// Replace line 1435 placeholder
adminHtml = adminHtml.replace(
  'placeholder="예: 박OO 선생님"',
  'placeholder="예: 홍길동 선생님"'
);

// Replace MASTER_INTEL_BASELINE
const masterRegex = /const MASTER_INTEL_BASELINE = \{[\s\S]*?\};\s*let schoolIntelDB =/m;
if (masterRegex.test(adminHtml)) {
  adminHtml = adminHtml.replace(masterRegex, `const MASTER_INTEL_BASELINE = ${JSON.stringify(schoolDb)};\n    let schoolIntelDB =`);
  console.log('✅ Replaced MASTER_INTEL_BASELINE in admin.html with 46 pure schools');
} else {
  console.warn('⚠️ Could not match masterRegex in admin.html');
}

fs.writeFileSync(ADMIN_PATH, adminHtml, 'utf8');
console.log('🎉 admin.html updated successfully');
