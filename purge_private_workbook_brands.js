const fs = require('fs');
const path = require('path');

const ROOT_DIR = __dirname;
const DB_PATH = path.join(ROOT_DIR, 'school_teacher_intelligence.json');
const PREVIEW_PATH = path.join(ROOT_DIR, 'preview.html');
const ADMIN_PATH = path.join(ROOT_DIR, 'admin.html');

console.log('--- PURGING ALL COMMERCIAL PRIVATE WORKBOOK & MOCK EXAM BRANDS ---');

// 1. UPDATE school_teacher_intelligence.json
const schoolDb = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));

// Sanitize naksaeng
schoolDb.schools.naksaeng.verified_exams = [
  '낙생고등학교 2학년 미적분 심화 기출 족보',
  '낙생고등학교 2학년 수학II 심화 기출 족보'
];
schoolDb.schools.naksaeng.exam_files_count = 2;
['1', '2', '3'].forEach(g => {
  schoolDb.schools.naksaeng.grades[g].workbooks = ['학교 심화 프린트'];
});

// Update genuine school exams
const genuineExamsMap = {
  hansol: {
    verified_exams: ['한솔고등학교 3학년 1학기 중간고사 미적분 기출', '한솔고등학교 3학년 미적분 심화 시험대비 족보'],
    exam_files_count: 2,
    workbooks: ['학교 심화 프린트']
  },
  neulpureun: {
    verified_exams: ['늘푸른고등학교 2학년 1학기 중간고사 확률과 통계 기출', '늘푸른고등학교 2학년 1학기 기말고사 확률과 통계 기출'],
    exam_files_count: 2,
    workbooks: ['학교 수업 심화 프린트']
  },
  daejin: {
    verified_exams: ['분당대진고등학교 2학년 1학기 중간고사 확률과 통계 기출'],
    exam_files_count: 1,
    workbooks: ['학교 수업 심화 프린트']
  },
  yeongdeok: {
    verified_exams: ['분당영덕여자고등학교 2학년 1학기 중간고사 확률과 통계 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  bulgok: {
    verified_exams: ['불곡고등학교 2학년 2학기 기말고사 확률과 통계 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  bopyeong: {
    verified_exams: ['보평고등학교 2학년 2학기 중간고사 수학II 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  yatap: {
    verified_exams: ['야탑고등학교 2학년 2학기 중간고사 확률과 통계 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  taewon: {
    verified_exams: ['태원고등학교 2학년 1학기 중간고사 수학I 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  sunae: {
    verified_exams: ['수내고등학교 2학년 1학기 중간고사 수학I 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  seohyun: {
    verified_exams: ['서현고등학교 2학년 1학기 중간고사 수학I 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  seongnam_fl: {
    verified_exams: ['성남외국어고등학교 2학년 1학기 중간고사 수학I 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  },
  jungang: {
    verified_exams: ['분당중앙고등학교 2학년 1학기 중간고사 수학I 기출'],
    exam_files_count: 1,
    workbooks: ['학교 심화 프린트']
  }
};

Object.keys(genuineExamsMap).forEach(k => {
  if (schoolDb.schools[k]) {
    schoolDb.schools[k].verified_exams = genuineExamsMap[k].verified_exams;
    schoolDb.schools[k].exam_files_count = genuineExamsMap[k].exam_files_count;
    ['1', '2', '3'].forEach(g => {
      schoolDb.schools[k].grades[g].workbooks = genuineExamsMap[k].workbooks;
    });
  }
});

// Final check across all schools in schoolDb to ensure zero private workbook brands
const forbiddenBrands = ['수평선', '절대등급', '고쟁이', '블랙라벨', '마더텅', '자이스토리', '쎈수학', '일등급수학', '일품', '올림포스', '개념원리', 'RPM', '짱', '만렙', '고잉', '수학중심', '수학의 신', '메가헤르츠', '하이퍼스트', '봉투모의고사'];

Object.keys(schoolDb.schools).forEach(k => {
  const s = schoolDb.schools[k];
  s.verified_exams = (s.verified_exams || []).filter(e => {
    return !forbiddenBrands.some(b => e.includes(b));
  });
  s.exam_files_count = s.verified_exams.length;
  ['1', '2', '3'].forEach(g => {
    s.grades[g].workbooks = (s.grades[g].workbooks || []).filter(w => {
      return !forbiddenBrands.some(b => w.includes(b));
    });
  });
});

fs.writeFileSync(DB_PATH, JSON.stringify(schoolDb, null, 2), 'utf8');
console.log('✅ school_teacher_intelligence.json cleaned of all commercial brand names.');

// 2. UPDATE preview.html
let previewHtml = fs.readFileSync(PREVIEW_PATH, 'utf8');

// Replace placeholder with generic educational text
previewHtml = previewHtml.replace(
  'placeholder="예: EBS 올림포스 닥터링 수학I / 학교 자체 킬러 프린트"',
  'placeholder="예: 학교 자체 심화 프린트 / 교육청 학력평가 변형 모의고사"'
);

// Replace DEFAULT_SCHOOL_INTEL_DB
const dbRegex = /const DEFAULT_SCHOOL_INTEL_DB = \{[\s\S]*?\};\s*let SCHOOL_INTEL_DB =/m;
if (dbRegex.test(previewHtml)) {
  previewHtml = previewHtml.replace(dbRegex, `const DEFAULT_SCHOOL_INTEL_DB = ${JSON.stringify(schoolDb)};\n    let SCHOOL_INTEL_DB =`);
  console.log('✅ Replaced DEFAULT_SCHOOL_INTEL_DB in preview.html with sanitized DB.');
}

fs.writeFileSync(PREVIEW_PATH, previewHtml, 'utf8');

// 3. UPDATE admin.html
let adminHtml = fs.readFileSync(ADMIN_PATH, 'utf8');

// Replace placeholders in admin.html
adminHtml = adminHtml.replace(
  'placeholder="예: EBS 올림포스 닥터링 수학I"',
  'placeholder="예: 학교 자체 심화 프린트"'
);
adminHtml = adminHtml.replace(
  "prompt('신규 확보된 부교재 또는 학교 프린트명을 입력하세요:\\n(예: 2026 EBS 올림포스 닥터링 수학I PDF)');",
  "prompt('신규 확보된 부교재 또는 학교 프린트명을 입력하세요:\\n(예: 2026 학교 자체 심화 프린트 PDF)');"
);

// Replace MASTER_INTEL_BASELINE
const masterRegex = /const MASTER_INTEL_BASELINE = \{[\s\S]*?\};\s*let schoolIntelDB =/m;
if (masterRegex.test(adminHtml)) {
  adminHtml = adminHtml.replace(masterRegex, `const MASTER_INTEL_BASELINE = ${JSON.stringify(schoolDb)};\n    let schoolIntelDB =`);
  console.log('✅ Replaced MASTER_INTEL_BASELINE in admin.html with sanitized DB.');
}

fs.writeFileSync(ADMIN_PATH, adminHtml, 'utf8');

console.log('🎉 All files sanitized from commercial workbook brand names!');
