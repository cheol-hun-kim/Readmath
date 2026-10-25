const fs = require('fs');
const path = require('path');

const QA_PATH = path.join(__dirname, 'qa_matrix_7gates.js');
let content = fs.readFileSync(QA_PATH, 'utf8');

const target = `  failGate(1, 'High-Contrast Color Armor', contrastViolations.join('; '));
}

passGate(1, 'DOM Structure, Tag Balance & Zero-Jargon Cleanliness', [`;

const replacement = `  failGate(1, 'High-Contrast Color Armor', contrastViolations.join('; '));
}

// 1.9 Zero Commercial Private Workbook & Mock Exam Brand Exposure Scanner
const forbiddenCommercialBrands = [
  { pattern: /수평선\\s*(?:미적분|수학|기출|모의고사|봉투|직전)/, desc: 'Commercial mock exam brand "수평선" exposed' },
  { pattern: /절대등급/, desc: 'Commercial workbook brand "절대등급" exposed' },
  { pattern: /고쟁이/, desc: 'Commercial workbook brand "고쟁이" exposed' },
  { pattern: /블랙라벨/, desc: 'Commercial workbook brand "블랙라벨" exposed' },
  { pattern: /마더텅/, desc: 'Commercial workbook brand "마더텅" exposed' },
  { pattern: /자이스토리/, desc: 'Commercial workbook brand "자이스토리" exposed' },
  { pattern: /쎈수학|쎈\\s*C단계/, desc: 'Commercial workbook brand "쎈수학" exposed' },
  { pattern: /일등급수학/, desc: 'Commercial workbook brand "일등급수학" exposed' },
  { pattern: /일품\\s*(?:고등|수학)/, desc: 'Commercial workbook brand "일품" exposed' },
  { pattern: /올림포스/, desc: 'Commercial workbook brand "올림포스" exposed' },
  { pattern: /개념원리/, desc: 'Commercial workbook brand "개념원리" exposed' },
  { pattern: /만렙(?:PM|AM)?/, desc: 'Commercial workbook brand "만렙" exposed' },
  { pattern: /짱_확장판/, desc: 'Commercial workbook brand "짱" exposed' },
  { pattern: /하이퍼스트/, desc: 'Commercial workbook brand "하이퍼스트" exposed' }
];

const brandViolations = [];
forbiddenCommercialBrands.forEach(({ pattern, desc }) => {
  if (pattern.test(cleanHtml)) {
    brandViolations.push(\`\${desc} in preview.html (matched: \${pattern})\`);
  }
});

const SCHOOL_DB_PATH = path.join(ROOT_DIR, 'school_teacher_intelligence.json');
if (fs.existsSync(SCHOOL_DB_PATH)) {
  const schoolDbStr = fs.readFileSync(SCHOOL_DB_PATH, 'utf8');
  forbiddenCommercialBrands.forEach(({ pattern, desc }) => {
    if (pattern.test(schoolDbStr)) {
      brandViolations.push(\`\${desc} in school_teacher_intelligence.json (matched: \${pattern})\`);
    }
  });
}

if (brandViolations.length > 0) {
  failGate(1, 'Zero Commercial Workbook Brand Names Armor', brandViolations.join('; '));
}

passGate(1, 'DOM Structure, Tag Balance & Zero-Jargon Cleanliness', [
  'Zero commercial private workbook / mock brands (수평선, 절대등급, 고쟁이, 블랙라벨, 마더텅, 자이스토리 등) 100% purged',`;

if (content.includes(target)) {
  content = content.replace(target, replacement);
  fs.writeFileSync(QA_PATH, content, 'utf8');
  console.log('✅ Successfully added commercial brand scanner to qa_matrix_7gates.js');
} else {
  console.error('❌ Could not locate target in qa_matrix_7gates.js');
}
