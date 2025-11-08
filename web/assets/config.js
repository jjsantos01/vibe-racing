export function resolveMetaUrl() {
  const qs = new URLSearchParams(location.search);
  const fromQuery = qs.get('meta') || qs.get('api'); // compat
  const fromGlobal = typeof window !== 'undefined' ? (window.DEV_NOTES_METADATA || window.DEV_NOTES_API) : null; // compat
  const fromLocal = typeof localStorage !== 'undefined' ? (localStorage.getItem('devNotesMeta') || localStorage.getItem('devNotesApi')) : null; // compat
  const fallback = location.origin + '/metadata';
  return finalizeMetaUrl((fromQuery && fromQuery.trim()) || (fromGlobal && String(fromGlobal).trim()) || (fromLocal && fromLocal.trim()) || fallback);
}

export function saveMetaUrl(url) {
  try { localStorage.setItem('devNotesMeta', finalizeMetaUrl(url)); } catch {}
}

export function finalizeMetaUrl(url){
  if (!url) return location.origin + '/metadata';
  try { return new URL(url, location.href).toString().replace(/\/$/, ''); } catch { return url; }
}

export function deriveBaseFromMeta(metaUrl){
  try { const u = new URL(metaUrl, location.href); return u.origin; } catch { return location.origin; }
}
