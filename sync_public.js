const fs = require('fs');

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
let publicContent;
if (previewContent.includes(previewHeadTarget)) {
  publicContent = previewContent.replace(previewHeadTarget, headPwaSection);
} else {
  // Normalize newline
  const normPreview = previewContent.replace(/\r\n/g, '\n');
  const normTarget = previewHeadTarget.replace(/\r\n/g, '\n');
  const normHead = headPwaSection.replace(/\r\n/g, '\n');
  publicContent = normPreview.replace(normTarget, normHead);
}

fs.writeFileSync('public/index.html', publicContent, 'utf8');
console.log('✓ Successfully synchronized preview.html -> public/index.html with PWA & OpenGraph headers!');

if (fs.existsSync('admin.html')) {
  fs.copyFileSync('admin.html', 'public/admin.html');
  console.log('✓ Successfully synchronized admin.html -> public/admin.html!');
}

if (fs.existsSync('landing.html')) {
  fs.copyFileSync('landing.html', 'public/landing.html');
  console.log('✓ Successfully synchronized landing.html -> public/landing.html!');
}

