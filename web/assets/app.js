import { resolveMetaUrl, saveMetaUrl, deriveBaseFromMeta } from './config.js';

const apiInput = document.getElementById('apiInput');
const apiSave = document.getElementById('apiSave');

const avatarEl = document.getElementById('avatar');
const nameEl = document.getElementById('name');
const contactsEl = document.getElementById('contacts');
const versionEl = document.getElementById('version');
const fileListUrlEl = document.getElementById('fileListUrl');

const notesListEl = document.getElementById('notesList');
const noteTitleEl = document.getElementById('noteTitle');
const noteContentEl = document.getElementById('noteContent');
const openRawEl = document.getElementById('openRaw');

let META_URL = resolveMetaUrl();
apiInput.value = META_URL;

apiSave.addEventListener('click', () => {
  const url = apiInput.value.trim();
  if (!url) return;
  saveMetaUrl(url);
  META_URL = url;
  bootstrap();
});

window.addEventListener('DOMContentLoaded', bootstrap);

async function bootstrap(){
  try{
    // Metadata (from explicit META_URL)
    const meta = await fetchJson(META_URL);
    renderProfile(meta);
  }catch(err){
    console.error('Error metadata', err);
  }
  try{
    // Notes list: prefer meta.fileList.url; fallback to origin/notes
    const meta = await fetchJson(META_URL).catch(()=>null);
    const origin = deriveBaseFromMeta(META_URL);
    const endpoint = (meta && meta.fileList && meta.fileList.url)
      ? new URL(meta.fileList.url, META_URL).toString()
      : new URL('/notes', origin).toString();
    const notes = await fetchJson(endpoint);
    renderNotes(notes);
  }catch(err){
    console.error('Error notes', err);
  }
}

function renderProfile(meta){
  versionEl.textContent = meta.version || '—';
  fileListUrlEl.textContent = meta?.fileList?.url || '—';
  const p = meta.profile || {};
  nameEl.textContent = p.name || '—';
  if (p.avatar){
    avatarEl.style.backgroundImage = `url('${p.avatar}')`;
  } else {
    avatarEl.style.backgroundImage = 'none';
    avatarEl.style.backgroundColor = '#e6faff';
  }
  contactsEl.innerHTML = '';
  if (p.contact){
    const c = p.contact;
    const entries = [
      ['github', c.github, v => `https://github.com/${v.replace(/^@/, '')}`],
      ['linkedin', c.linkedin, v => v],
      ['email', c.email, v => `mailto:${v}`],
      ['twitter', c.twitter, v => `https://x.com/${v.replace(/^@/, '')}`],
      ['website', c.website, v => v],
    ];
    for (const [label, val, link] of entries){
      if (!val) continue;
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = link(String(val)); a.textContent = `${label}: ${val}`; a.target = '_blank';
      li.appendChild(a); contactsEl.appendChild(li);
    }
    if (Array.isArray(c.other)){
      for (const o of c.other){
        if (!o?.url) continue;
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = o.url; a.textContent = `${o.label || o.platform || 'link'}`; a.target = '_blank';
        li.appendChild(a); contactsEl.appendChild(li);
      }
    }
  }
}

function renderNotes(urls){
  notesListEl.innerHTML = '';
  const list = Array.isArray(urls) ? urls : [];
  for (const url of list){
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#';
    const name = displayName(url);
    a.textContent = name;
    a.title = url;
    a.addEventListener('click', (e)=>{ e.preventDefault(); openNote(url); });
    const btn = document.createElement('button');
    btn.className = 'open'; btn.textContent = 'Abrir';
    btn.addEventListener('click', ()=> openNote(url));
    li.appendChild(a); li.appendChild(btn); notesListEl.appendChild(li);
  }
  if (list.length){ openNote(list[0]); }
}

async function openNote(url){
  try{
    const text = await fetchText(url);
    noteTitleEl.textContent = basename(url);
    openRawEl.href = url;
    noteContentEl.innerHTML = markdownToHtml(stripFrontMatter(text));
  }catch(err){
    noteTitleEl.textContent = 'Error cargando nota';
    noteContentEl.textContent = String(err);
  }
}

function stripFrontMatter(text){
  if (text.startsWith('---\n')){
    const end = text.indexOf('\n---\n', 4);
    if (end !== -1){ return text.slice(end+5); }
  }
  return text;
}

function markdownToHtml(md){
  // Parser mínimo: headings, code fences, paragraphs
  const lines = md.replace(/\r\n?/g, '\n').split('\n');
  let html = '';
  let inCode = false;
  for (let raw of lines){
    const line = raw;
    if (line.trim().startsWith('```')){
      if (!inCode){ html += '<pre><code>'; inCode = true; }
      else { html += '</code></pre>'; inCode = false; }
      continue;
    }
    if (inCode){ html += escapeHtml(line) + '\n'; continue; }
    if (/^###\s+/.test(line)) { html += `<h3>${escapeHtml(line.replace(/^###\s+/, ''))}</h3>`; continue; }
    if (/^##\s+/.test(line)) { html += `<h2>${escapeHtml(line.replace(/^##\s+/, ''))}</h2>`; continue; }
    if (/^#\s+/.test(line)) { html += `<h1>${escapeHtml(line.replace(/^#\s+/, ''))}</h1>`; continue; }
    if (line.trim() === '') { html += '<br/>'; continue; }
    // inline bold/italic super simple
    let p = escapeHtml(line).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>');
    html += `<p>${p}</p>`;
  }
  if (inCode){ html += '</code></pre>'; }
  return html;
}

function escapeHtml(s){
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function basename(u){
  try { const p = new URL(u); const parts = p.pathname.split('/'); return parts[parts.length-1] || u; } catch { return u; }
}

function displayName(u){
  const base = basename(u);
  const noExt = base.endsWith('.md') ? base.slice(0, -3) : base;
  return noExt;
}

async function fetchJson(url){
  try{
    const res = await fetch(url, { headers: { 'Accept':'application/json' } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  }catch(err){
    // Fallback via local proxy to bypass CORS
    const prox = new URL('/proxy', location.origin);
    prox.searchParams.set('url', url);
    const res2 = await fetch(prox, { headers: { 'Accept':'application/json' } });
    if (!res2.ok) throw new Error(`Proxy HTTP ${res2.status}`);
    return await res2.json();
  }
}
async function fetchText(url){
  try{
    const res = await fetch(url, { headers: { 'Accept':'text/plain' } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  }catch(err){
    const prox = new URL('/proxy', location.origin);
    prox.searchParams.set('url', url);
    const res2 = await fetch(prox, { headers: { 'Accept':'text/plain' } });
    if (!res2.ok) throw new Error(`Proxy HTTP ${res2.status}`);
    return await res2.text();
  }
}
