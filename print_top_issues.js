const fs = require('fs');
const targetFile = process.argv[2] || 'preview.html';
const content = fs.readFileSync(targetFile, 'utf8');
const pDbMatch = content.match(/const PROBLEMS_DB = (\{[\s\S]*?\n    \};)/);
const PROBLEMS_DB = eval('(' + pDbMatch[1].replace(/;\s*$/, '') + ')');

const issues = [];
function checkText(str, path) {
  if (typeof str !== 'string' || !str.trim()) return;
  const tokens = [];
  let inDollar = false;
  let current = '';
  for (let i = 0; i < str.length; i++) {
    if (str[i] === '$') {
      tokens.push({ text: current, isMath: inDollar });
      current = '';
      inDollar = !inDollar;
    } else {
      current += str[i];
    }
  }
  tokens.push({ text: current, isMath: inDollar });

  tokens.forEach((token, idx) => {
    if (!token.isMath) {
      const rawCommands = token.text.match(/\\[a-zA-Z]+/g);
      if (rawCommands) {
        const mathCommands = rawCommands.filter(c => !['\\n', '\\r', '\\t', '\\"', '\\\\'].includes(c));
        if (mathCommands.length > 0) {
          issues.push({ path, type: 'RAW_LATEX_OUTSIDE_MATH', text: token.text.trim(), detail: mathCommands.join(', ') });
        }
      }
      const greekWords = token.text.match(/\b(theta|alpha|beta)\b/gi);
      if (greekWords) {
        issues.push({ path, type: 'NAKED_GREEK_WORD', text: token.text.trim(), detail: greekWords.join(', ') });
      }
      const unicodeSymbols = token.text.match(/[θϕφ≠≤≥±×÷]/g);
      if (unicodeSymbols) {
        issues.push({ path, type: 'UNICODE_SYMBOL_OUTSIDE_MATH', text: token.text.trim(), detail: unicodeSymbols.join(', ') });
      }
    }
  });
}

function traverse(obj, path = '') {
  for (const [k, v] of Object.entries(obj)) {
    const curPath = path ? path + '.' + k : k;
    if (typeof v === 'string') {
      if (k !== 'svg' && k !== 'svg_diagram') {
        checkText(v, curPath);
      }
    } else if (typeof v === 'object' && v !== null) {
      traverse(v, curPath);
    }
  }
}

traverse(PROBLEMS_DB);
console.log('Total issues:', issues.length);
issues.slice(0, 10).forEach((iss, i) => {
  console.log(`[${i + 1}] [${iss.type}] at ${iss.path}`);
  console.log(`    Detail: ${iss.detail}`);
  console.log(`    Snippet: ${iss.text.slice(0, 80)}`);
});
