const fs = require('fs');

// 1. Process preview.html (Web App)
const previewContent = fs.readFileSync('preview.html', 'utf8');

const headPwaSection = `  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>ReadMath (리드매스) - 수학은 해석의 대상이다!</title>
  <meta name="theme-color" content="#0B0F19" />
  <link rel="manifest" href="/manifest.json" />
  <link rel="icon" type="image/png" href="/assets/icon-192.png" />
  <link rel="apple-touch-icon" href="/assets/icon-192.png" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <!-- OpenGraph for KakaoTalk, Instagram, Social Sharing -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="ReadMath (리드매스) - 수학은 해석의 대상이다!" />
  <meta property="og:description" content="외계어 같은 수식을 일상의 한글로 번역하고 그래프로 생생하게 그려주는 1등 AI 시각화 수학 멘토" />
  <meta property="og:image" content="/assets/icon-512.png" />`;

const previewHeadTarget = `  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ReadMath (리드매스) - 수학은 해석의 대상이다!</title>`;

// Replace with either CRLF or LF matching
let appContent;
if (previewContent.includes(previewHeadTarget)) {
  appContent = previewContent.replace(previewHeadTarget, headPwaSection);
} else {
  // Normalize newline
  const normPreview = previewContent.replace(/\r\n/g, '\n');
  const normTarget = previewHeadTarget.replace(/\r\n/g, '\n');
  const normHead = headPwaSection.replace(/\r\n/g, '\n');
  appContent = normPreview.replace(normTarget, normHead);
}

// Sync App to public/app.html & public/preview.html
fs.writeFileSync('public/app.html', appContent, 'utf8');
fs.writeFileSync('public/preview.html', appContent, 'utf8');
console.log('✓ Successfully synchronized preview.html -> public/app.html & public/preview.html!');

// 2. Process landing.html (Brand Homepage) -> public/index.html & public/landing.html
if (fs.existsSync('landing.html')) {
  const landingContent = fs.readFileSync('landing.html', 'utf8');
  fs.writeFileSync('public/index.html', landingContent, 'utf8');
  fs.writeFileSync('public/landing.html', landingContent, 'utf8');
  console.log('✓ Successfully synchronized landing.html -> public/index.html (Root Homepage) & public/landing.html!');
}

// 3. Process admin.html -> public/admin.html
if (fs.existsSync('admin.html')) {
  fs.copyFileSync('admin.html', 'public/admin.html');
  console.log('✓ Successfully synchronized admin.html -> public/admin.html!');
}

// 4. Process grant_proposal.html -> public/proposal.html
if (fs.existsSync('grant_proposal.html')) {
  fs.copyFileSync('grant_proposal.html', 'public/proposal.html');
  console.log('✓ Successfully synchronized grant_proposal.html -> public/proposal.html!');
}

