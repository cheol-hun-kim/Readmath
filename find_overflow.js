const fs = require('fs');
const content = fs.readFileSync('preview.html', 'utf8');
const pDbMatch = content.match(/const PROBLEMS_DB = (\{[\s\S]*?\n    \};)/);
const PROBLEMS_DB = eval('(' + pDbMatch[1].replace(/;\s*$/, '') + ')');

for (const [pId, prob] of Object.entries(PROBLEMS_DB)) {
  const allSvgs = (prob.diagrams || []).map(d => d.svg).concat(prob.svg_diagram ? [prob.svg_diagram] : []);
  allSvgs.forEach((svg, sIdx) => {
    if (!svg) return;
    const rects = [];
    const rRegex = /<rect\s+([^>]+)>/gi;
    let rm;
    while ((rm = rRegex.exec(svg)) !== null) {
      const raw = rm[1];
      if (raw.includes('width="420"') || raw.includes('width="100%"') || raw.includes('stroke-dasharray') || raw.includes('fill="none"')) continue;
      const xM = raw.match(/x="([^"]+)"/);
      const yM = raw.match(/y="([^"]+)"/);
      const wM = raw.match(/width="([^"]+)"/);
      const hM = raw.match(/height="([^"]+)"/);
      if (xM && yM && wM && hM) {
        rects.push({ x: parseFloat(xM[1]), y: parseFloat(yM[1]), w: parseFloat(wM[1]), h: parseFloat(hM[1]), raw });
      }
    }

    const texts = [];
    const tRegex = /<text\s+([^>]+)>([\s\S]*?)<\/text>/gi;
    let tm;
    while ((tm = tRegex.exec(svg)) !== null) {
      const rawAttrs = tm[1];
      const textStr = tm[2].replace(/<[^>]+>/g, '').trim();
      const xM = rawAttrs.match(/x="([^"]+)"/);
      const yM = rawAttrs.match(/y="([^"]+)"/);
      const fsM = rawAttrs.match(/font-size="([^"]+)"/);
      const anchorM = rawAttrs.match(/text-anchor="([^"]+)"/);
      if (xM && yM) {
        texts.push({
          x: parseFloat(xM[1]),
          y: parseFloat(yM[1]),
          fs: fsM ? parseFloat(fsM[1]) : 10,
          anchor: anchorM ? anchorM[1] : 'start',
          text: textStr
        });
      }
    }

    rects.forEach(card => {
      const rRight = card.x + card.w;
      const rBottom = card.y + card.h;
      const inside = texts.filter(t => t.x >= card.x - 10 && t.x <= rRight + 20 && t.y >= card.y - 5 && t.y <= rBottom + 15);
      inside.forEach(t => {
        let estW = 0;
        for (let c of t.text) {
          estW += (c.charCodeAt(0) > 127) ? t.fs * 0.95 : t.fs * 0.58;
        }
        let tRight = t.anchor === 'middle' ? (t.x + estW / 2) : (t.x + estW);
        let tLeft = t.anchor === 'middle' ? (t.x - estW / 2) : t.x;
        if (tRight > rRight || tLeft < card.x) {
          console.log(`OVERFLOW in Problem ${pId} SVG #${sIdx}:`);
          console.log(`  Card: x=${card.x}, y=${card.y}, w=${card.w}, h=${card.h} (right=${rRight})`);
          console.log(`  Text: "${t.text}" x=${t.x}, anchor=${t.anchor}, estW=${estW.toFixed(1)}, left=${tLeft.toFixed(1)}, right=${tRight.toFixed(1)}`);
        }
      });
    });
  });
}
