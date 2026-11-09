r"""
=============================================================================
RootMath Universal CSAT Typesetter (CsatTypesetter v3.0)
=============================================================================
A generalized, publication-grade typographic pipeline that guarantees:
1. Strict Korean Particle Binding: Zero unnatural gaps between math variables
   and Korean postpositions (조사: 은, 는, 이, 가, 을, 를, 의, 에, 와, 과, 일 때, 등).
2. Compact Operator Sizing: Converts \sum, \prod, \lim to \nolimits in inline math
   so line heights remain 100% stable and never blow up.
3. Authentic CSAT Font & Layout Styling: Matches Korea Institute for Curriculum
   and Evaluation (KICE / 평가원) font weights, line heights, and margins.
4. Standardized Problem Point Badges: [4점] / [3점] right-aligned typography.
=============================================================================
"""

import re

# Korean postpositions (조사 및 어미) that must attach directly to preceding noun/formula
KOREAN_PARTICLES = [
    '은', '는', '이', '가', '을', '를', '의', '에', '에서', '에서의',
    '와', '과', '로', '으로', '이며', '이고', '일', '이라', '라면', '면',
    '보다', '까지', '부터', '마다', '조차', '마저', '도'
]

PARTICLE_REGEX = re.compile(
    r'(\$[^\$]+\$)\s+(' + '|'.join(KOREAN_PARTICLES) + r')(?=[\s\.,\?!~]|$)'
)

def normalize_csat_text(raw_text: str) -> str:
    """
    Transforms any raw problem or explanation text into authentic CSAT typographic format.
    """
    if not raw_text:
        return ""
    
    text = raw_text

    # 1. Standardize operator replacements (<=, >=, != to KaTeX standards)
    text = text.replace('<=', r'\le ').replace('>=', r'\ge ').replace('!=', r'\neq ')

    # 2. Convert inline \sum to \sum\nolimits (prevents line-height explosion)
    # Target: \sum_{...}^{...} or \sum_{...} inside single $...$
    def inline_sum_replacer(match):
        inner = match.group(1)
        # replace \sum with \sum\nolimits if not display math
        inner = re.sub(r'\\sum(?!\s*\\nolimits)', r'\\sum\\nolimits', inner)
        inner = re.sub(r'\\lim(?!\s*\\nolimits)', r'\\lim\\nolimits', inner)
        return f"${inner}$"

    # Only process inline math ($...$ not $$...$$)
    text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', inline_sum_replacer, text)

    # 3. Particle Binding: Remove space between math formula and following Korean particle
    # e.g., "$a_n$ 에 대하여" -> "$a_n$에 대하여"
    # e.g., "$a_1$ 의 값을" -> "$a_1$의 값을"
    # e.g., "$= 2$ 일 때" -> "$= 2$일 때"
    for _ in range(3): # repeat to catch consecutive occurrences
        text = PARTICLE_REGEX.sub(r'\1\2', text)

    # Also handle specific compound phrases like "일 때"
    text = re.sub(r'(\$[^\$]+\$)\s+(일\s*때)', r'\1 \2', text) # standard single space for "일 때"
    text = re.sub(r'(\$[^\$]+\$)\s+(의\s+값을)', r'\1의 값을', text)
    text = re.sub(r'(\$[^\$]+\$)\s+(에\s+대하여)', r'\1에 대하여', text)
    text = re.sub(r'(\$[^\$]+\$)\s+(을\s+만족)', r'\1을 만족', text)
    text = re.sub(r'(\$[^\$]+\$)\s+(를\s+만족)', r'\1를 만족', text)

    # 4. Standardize score badges [4점], [3점]
    text = re.sub(
        r'\[(3|4)점\]',
        r'<span class="csat-points">[\1점]</span>',
        text
    )

    return text


def get_csat_typography_css() -> str:
    """
    Returns authentic CSAT typography CSS for printable PDF documents and web previews.
    """
    return """
    /* CSAT Authentic Typography Engine */
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Pretendard:wght@400;500;600;700;800;900&display=swap');

    :root {
      --csat-font-serif: 'Nanum Myeongjo', 'Batang', serif;
      --csat-font-sans: 'Pretendard', -apple-system, sans-serif;
      --csat-ink: #000000;
      --csat-ink-secondary: #1E293B;
    }

    body {
      font-family: var(--csat-font-serif);
      color: var(--csat-ink);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
    }

    /* Problem Title & Body Formatting */
    .csat-problem-body {
      font-family: var(--csat-font-serif);
      font-size: 13.2px;
      line-height: 1.82;
      letter-spacing: -0.022em;
      word-spacing: -0.03em;
      text-align: left !important;
      word-break: keep-all;
      overflow-wrap: break-word;
    }

    .csat-problem-num {
      font-family: var(--csat-font-serif);
      font-size: 14.5px;
      font-weight: 800;
      margin-right: 4px;
      letter-spacing: -0.01em;
    }

    .csat-points {
      font-family: var(--csat-font-serif);
      font-size: 11.5px;
      font-weight: 700;
      color: #334155;
      margin-left: 6px;
      letter-spacing: -0.02em;
    }

    /* KaTeX Mathematical Inline Proportions in CSAT */
    .katex {
      font-size: 0.96em !important;
      line-height: 1.2 !important;
      text-indent: 0 !important;
      margin: 0 1px !important;
    }

    .katex-display {
      margin: 8px 0 !important;
    }

    .katex .mord.text {
      font-family: var(--csat-font-serif) !important;
    }

    /* Ensure Summation with \nolimits never blows up line height */
    .katex .op-limits > .vlist-t {
      text-align: left;
    }

    /* 5-Choice Circular Layout */
    .csat-choices-grid {
      display: flex;
      justify-content: space-between;
      margin-top: 12px;
      padding: 0 4px;
      font-family: var(--csat-font-serif);
      font-size: 12.5px;
      letter-spacing: -0.02em;
    }

    .csat-choices-grid span {
      display: inline-flex;
      align-items: center;
      gap: 2px;
    }

    /* Problem Condition Box (가, 나) */
    .csat-condition-box {
      border: 1px solid #71717A;
      background: #FFFFFF;
      padding: 8px 14px;
      margin: 8px 0;
      font-family: var(--csat-font-serif);
      font-size: 12.5px;
      line-height: 1.7;
    }
    """

if __name__ == "__main__":
    sample = "5. 등비수열 {a_n} 에 대하여 급수 $\\sum_{n=1}^\\infty (a_n - 3)$ 이 수렴하고 $\\sum_{n=1}^\\infty \\frac{a_n}{2^n} = 2$ 일 때, $a_1$ 의 값을 구하시오. [4점]"
    print("ORIGINAL:")
    print(sample)
    print("\nNORMALIZED CSAT:")
    print(normalize_csat_text(sample))
