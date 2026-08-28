import { bootPython, parsePythonJson } from './pyodide-helper.js';

const samples = ['Mateo 2026!', '¡Hola, Salta!', 'Python + accesibilidad'];
const source = document.querySelector('#source');
const cells = document.querySelector('#cells');
const unicode = document.querySelector('#unicode');
const unknown = document.querySelector('#unknown');
const run = document.querySelector('#run');
let py;
let sampleIndex = 0;
let timer;

async function init() { py = await bootPython(['braille.py']); run.disabled = false; render(); }

function escapeHtml(value) { return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char])); }

function cellHtml(cell) {
  let html = `<div title="${escapeHtml(cell.kind)}"><div class="braille-cell" aria-label="${escapeHtml(cell.source || 'space')}: dots ${cell.dots.join(', ') || 'none'}">`;
  for (const dot of [1, 4, 2, 5, 3, 6]) html += `<span class="dot ${cell.dots.includes(dot) ? 'on' : ''}"></span>`;
  return `${html}</div><small class="muted">${escapeHtml(cell.source || '␠')}</small></div>`;
}

function render() {
  if (!py) return;
  py.globals.set('demo_text', source.value);
  const raw = py.runPython(`import json\nfrom braille import translate\nt=translate(demo_text)\njson.dumps({'unicode':t.unicode_text,'unknown':list(t.unknown_characters),'cells':[{'source':c.source,'dots':list(c.dots),'kind':c.kind} for c in t.cells]},ensure_ascii=False)`);
  const data = parsePythonJson(raw);
  unicode.textContent = data.unicode || '(empty input)';
  cells.innerHTML = data.cells.map(cellHtml).join('');
  const indicators = data.cells.filter((cell) => cell.kind.endsWith('sign')).length;
  document.querySelector('#brailleMetrics').innerHTML = `<div class="metric"><strong>${data.cells.length}</strong><small>Output cells</small></div><div class="metric"><strong>${indicators}</strong><small>Indicators</small></div><div class="metric"><strong>${data.unknown.length}</strong><small>Unknown symbols</small></div>`;
  unknown.textContent = data.unknown.length ? `Unknown characters are rendered as a full cell: ${data.unknown.join(' ')}` : 'Every character in this sample is covered by the educational mapping.';
}

run.disabled = true;
run.addEventListener('click', render);
source.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(render, 120); });
document.querySelector('#sample').addEventListener('click', () => { source.value = samples[sampleIndex++ % samples.length]; render(); });
init().catch(() => {});
