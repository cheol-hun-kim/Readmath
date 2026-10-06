const fs = require('fs');

function robustJsonParse(rawText) {
  if (!rawText) throw new Error('Empty response from AI');

  // Strip markdown code fences
  let cleaned = rawText.trim();
  cleaned = cleaned.replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/i, '').trim();

  // Try direct parse first
  try {
    return JSON.parse(cleaned);
  } catch (err1) {
    console.warn('Initial JSON.parse failed, attempting robust repair...', err1.message);
  }

  // Find outermost { ... }
  const firstBrace = cleaned.indexOf('{');
  const lastBrace = cleaned.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
    cleaned = cleaned.substring(firstBrace, lastBrace + 1);
    try {
      return JSON.parse(cleaned);
    } catch (err2) {
      console.warn('Trimmed brace JSON.parse failed...', err2.message);
    }
  }

  // Fix unescaped backslashes commonly found in LaTeX formulas
  // e.g. \frac, \begin, \alpha -> replace single backslashes that are not valid JSON escape sequences with \\
  let repaired = cleaned.replace(/\\([a-zA-Z{}_^])/g, '\\\\$1');
  try {
    return JSON.parse(repaired);
  } catch (err3) {
    console.warn('LaTeX backslash repair failed...', err3.message);
  }

  // Fix unescaped newlines inside strings
  repaired = repaired.replace(/(?<!\\)\n/g, '\\n');
  try {
    return JSON.parse(repaired);
  } catch (err4) {
    console.warn('Newline repair failed...', err4.message);
  }

  throw new Error('JSON parsing failed after all repair attempts: ' + cleaned.slice(0, 100));
}

try {
  const content = fs.readFileSync('gemini_raw_out.json', 'utf8').replace(/^\uFEFF/, '');
  const parsedResponse = JSON.parse(content);
  const text = parsedResponse.candidates[0].content.parts[0].text;
  const result = robustJsonParse(text);
  console.log('SUCCESS! Title:', result.title);
  console.log('Final Answer:', result.final_answer);
  console.log('Steps:', result.solution_steps?.length);
} catch (e) {
  console.error('Error in test:', e);
}
