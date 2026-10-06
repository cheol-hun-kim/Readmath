const fs = require('fs');
const content = fs.readFileSync('preview.html', 'utf8');
const pDbMatch = content.match(/const PROBLEMS_DB = (\{[\s\S]*?\n    \};)/);
const objCode = pDbMatch[1];
const PROBLEMS_DB = eval('(' + objCode.replace(/;\s*$/, '') + ')');

for (const [id, prob] of Object.entries(PROBLEMS_DB)) {
  console.log('\n========================================');
  console.log('PROBLEM ' + id + ': ' + prob.title);
  console.log('========================================');
  if (!prob.diagrams || prob.diagrams.length === 0) {
    console.log('NO DIAGRAMS');
    continue;
  }
  prob.diagrams.forEach((d, idx) => {
    console.log('\n--- Diagram ' + idx + ': ' + (d.title || 'NO TITLE') + ' ---');
    console.log('ID: ' + d.id + ', Badge: ' + d.badge);
    console.log('Caption: ' + d.caption);
    const svg = d.svg || '';
    console.log('SVG length: ' + svg.length);
    // Find viewBox
    const vb = svg.match(/viewBox="([^"]+)"/);
    console.log('ViewBox: ' + (vb ? vb[1] : 'NONE'));
    // Extract elements
    const paths = (svg.match(/<path[^>]+>/g) || []).map(p => p.slice(0, 80));
    const lines = (svg.match(/<line[^>]+>/g) || []).map(l => l.slice(0, 80));
    const circles = (svg.match(/<circle[^>]+>/g) || []).map(c => c.slice(0, 80));
    const texts = (svg.match(/<text[^>]*>[^<]*<\/text>/g) || []).map(t => t.trim());
    console.log('Circles count: ' + circles.length);
    console.log('Texts: ' + JSON.stringify(texts));
  });
}
