const fs = require('fs');
const content = fs.readFileSync('preview.html', 'utf8');
const pDbMatch = content.match(/const PROBLEMS_DB = (\{[\s\S]*?\n    \};)/);
const objCode = pDbMatch[1];
const PROBLEMS_DB = eval('(' + objCode.replace(/;\s*$/, '') + ')');

console.log('[EXHAUSTIVE AUDIT: Exposed Coding Jargon & Math Delimiters]');

const issues = [];

function checkText(str, path) {
  if (typeof str !== 'string' || !str.trim()) return;

  // 1. Check for odd number of $ delimiters
  const dollarCount = (str.match(/\$/g) || []).length;
  if (dollarCount % 2 !== 0) {
    issues.push({ path, type: 'ODD_DOLLAR_COUNT', text: str, detail: `Found ${dollarCount} '$' characters` });
  }

  // 2. Tokenize by $ and check outside math
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
      // Check for raw LaTeX backslash commands outside $
      const rawCommands = token.text.match(/\\[a-zA-Z]+/g);
      if (rawCommands) {
        // filter out \n, \r, \t, etc.
        const mathCommands = rawCommands.filter(c => !['\\n', '\\r', '\\t', '\\"', '\\\\'].includes(c));
        if (mathCommands.length > 0) {
          issues.push({ path, type: 'RAW_LATEX_OUTSIDE_MATH', text: token.text.trim(), detail: mathCommands.join(', ') });
        }
      }

      // Check for naked Greek words (theta, alpha, beta, phi) when used in math contexts
      const greekWords = token.text.match(/\b(theta|alpha|beta)\b/gi);
      if (greekWords) {
        issues.push({ path, type: 'NAKED_GREEK_WORD', text: token.text.trim(), detail: greekWords.join(', ') });
      }

      // Check for unicode Greek / math symbols outside $
      const unicodeSymbols = token.text.match(/[θϕφ≠≤≥±×÷]/g);
      if (unicodeSymbols) {
        issues.push({ path, type: 'UNICODE_SYMBOL_OUTSIDE_MATH', text: token.text.trim(), detail: unicodeSymbols.join(', ') });
      }

      // Check for raw HTML entities in math-like expressions
      const htmlEntities = token.text.match(/&(?:lt|gt|amp);/g);
      if (htmlEntities && /[0-9a-zA-Z]/.test(token.text)) {
        issues.push({ path, type: 'HTML_ENTITY', text: token.text.trim(), detail: htmlEntities.join(', ') });
      }
    } else {
      // Inside math: check for nested $ or broken constructs
      if (token.text.includes('$')) {
        issues.push({ path, type: 'NESTED_DOLLAR', text: token.text, detail: 'Nested dollar found' });
      }
      // Check for \mathrm or \mathbf artifacts
      if (/\\?(?:mathrm|mathbf|mathit)\s*\{?[A-Z]{2,}/.test(token.text)) {
        issues.push({ path, type: 'MATHRM_ARTIFACT', text: token.text, detail: 'Raw mathrm found' });
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

console.log(`\nAudit completed. Total text issues found: ${issues.length}`);
issues.forEach((iss, i) => {
  console.log(`[${i + 1}] [${iss.type}] at ${iss.path}`);
  console.log(`    Detail: ${iss.detail}`);
  console.log(`    Snippet: ${iss.text.slice(0, 80)}`);
});
