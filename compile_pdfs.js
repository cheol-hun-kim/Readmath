const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT_DIR = path.resolve(__dirname);
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

if (!fs.existsSync(CHROME_PATH)) {
  console.error('Chrome not found at', CHROME_PATH);
  process.exit(1);
}

// Ensure download directories exist
const publicDownloadsDir = path.join(ROOT_DIR, 'public', 'downloads');
const downloadsDir = path.join(ROOT_DIR, 'downloads');
if (!fs.existsSync(publicDownloadsDir)) fs.mkdirSync(publicDownloadsDir, { recursive: true });
if (!fs.existsSync(downloadsDir)) fs.mkdirSync(downloadsDir, { recursive: true });

const tasks = [
  {
    html: path.join(ROOT_DIR, 'templates', 'concept_book.html'),
    pdfName: 'ReadMath_개별맞춤_개념서_Sample.pdf'
  },
  {
    html: path.join(ROOT_DIR, 'templates', 'nje_exam_24.html'),
    pdfName: 'ReadMath_2025수능킬러_변형24제_N제.pdf'
  }
];

tasks.forEach(task => {
  console.log(`\nCompiling ${task.pdfName}...`);
  if (!fs.existsSync(task.html)) {
    console.error(`HTML template not found: ${task.html}`);
    process.exit(1);
  }

  const fileUrl = 'file:///' + task.html.replace(/\\/g, '/');
  const tempPdf = path.join(ROOT_DIR, 'temp_build.pdf');
  if (fs.existsSync(tempPdf)) fs.unlinkSync(tempPdf);

  const cmd = `"${CHROME_PATH}" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=5000 --run-all-compositor-stages-before-draw --print-to-pdf="${tempPdf}" "${fileUrl}"`;
  execSync(cmd, { stdio: 'inherit' });

  if (!fs.existsSync(tempPdf)) {
    console.error(`Failed to compile ${task.pdfName}`);
    process.exit(1);
  }

  const stat = fs.statSync(tempPdf);
  console.log(`✓ Successfully compiled ${task.pdfName} (${stat.size} bytes)`);

  // Copy to public/downloads/ and downloads/
  const target1 = path.join(publicDownloadsDir, task.pdfName);
  const target2 = path.join(downloadsDir, task.pdfName);

  fs.copyFileSync(tempPdf, target1);
  fs.copyFileSync(tempPdf, target2);
  fs.unlinkSync(tempPdf);

  console.log(`  -> Saved to: ${target1}`);
  console.log(`  -> Saved to: ${target2}`);
});

console.log('\n[ALL PDFs SUCCESSFULLY COMPILED & DISTRIBUTED]');
