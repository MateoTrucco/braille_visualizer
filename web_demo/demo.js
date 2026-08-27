import { bootPython, parsePythonJson } from './pyodide-helper.js';
const source=document.querySelector('#source'), cells=document.querySelector('#cells'), unicode=document.querySelector('#unicode'), unknown=document.querySelector('#unknown'), run=document.querySelector('#run');let py;
async function init(){py=await bootPython(['braille.py']);run.disabled=false;render();}
function cellHtml(dots,label){let html='<div><div class="braille-cell">';for(const dot of [1,4,2,5,3,6])html+=`<span class="dot ${dots.includes(dot)?'on':''}"></span>`;return html+`</div><small class="muted">${escapeHtml(label||'␠')}</small></div>`;}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function render(){if(!py)return;py.globals.set('demo_text',source.value);const raw=py.runPython(`import json
from braille import translate
t=translate(demo_text)
json.dumps({'unicode':t.unicode_text,'unknown':list(t.unknown_characters),'cells':[{'source':c.source,'dots':list(c.dots),'kind':c.kind} for c in t.cells]},ensure_ascii=False)`);const data=parsePythonJson(raw);unicode.textContent=data.unicode||'(empty)';cells.innerHTML=data.cells.map(c=>cellHtml(c.dots,c.source)).join('');unknown.textContent=data.unknown.length?'Unknown characters: '+data.unknown.join(' '):'All characters in this sample are supported by the project mapping.';}
run.disabled=true;run.addEventListener('click',render);init().catch(()=>{});
