const TEXT_FIELDS = ['summary', 'method', 'notice'];
const TOTAL_FIELDS = ['estimated_total', 'budget', 'remaining_budget'];

// Keep the displayed proposal, not the form's current preferences.
export function serializeItinerary(proposal, origin) {
  if (!proposal || !['api', 'demo'].includes(origin) ||
      !Array.isArray(proposal.itinerary) ||
      proposal.itinerary.some(item => !item || typeof item !== 'object' || Array.isArray(item)) ||
      TEXT_FIELDS.some(key => typeof proposal[key] !== 'string') ||
      TOTAL_FIELDS.some(key => !Number.isFinite(proposal[key]) || proposal[key] < 0)) {
    throw new TypeError('No se puede exportar esta propuesta. Genera una nueva ruta.');
  }
  const data = { format_version: 1, origin, itinerary: proposal.itinerary };
  for (const key of [...TEXT_FIELDS, ...TOTAL_FIELDS]) data[key] = proposal[key];
  return JSON.stringify(data, null, 2);
}

// Browser capabilities are injectable for unit tests; no fetch or remote service.
export function downloadItinerary(proposal, origin, browser = globalThis) {
  const json = serializeItinerary(proposal, origin);
  const blob = new browser.Blob([json], { type: 'application/json;charset=utf-8' });
  const link = browser.document.createElement('a');
  const url = browser.URL.createObjectURL(blob);
  try {
    link.href = url;
    link.download = 'opita360-itinerario.json';
    browser.document.body.appendChild(link);
    link.click();
  } finally {
    link.remove();
    browser.setTimeout(() => browser.URL.revokeObjectURL(url), 1000);
  }
}
