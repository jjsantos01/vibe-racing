export function resolveApiBase() {
  const urlParams = new URLSearchParams(location.search);
  const fromQuery = urlParams.get('api');
  const fromGlobal = typeof window !== 'undefined' ? window.DEV_NOTES_API : null;
  const fromLocal = typeof localStorage !== 'undefined' ? localStorage.getItem('devNotesApi') : null;
  return (fromQuery && fromQuery.trim()) || (fromGlobal && String(fromGlobal).trim()) || (fromLocal && fromLocal.trim()) || location.origin;
}

export function saveApiBase(url) {
  try { localStorage.setItem('devNotesApi', url); } catch {}
}

