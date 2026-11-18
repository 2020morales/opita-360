// Browser-only persistence is injected so helpers are testable without window.
export const FAVORITES_KEY = "opita360:favorites:v1";
export const SESSION_NOTICE = "Solo esta sesión: los favoritos no se conservarán al recargar porque el almacenamiento no está disponible.";
const browserStorage = () => window.localStorage;
const validId = id => Number.isSafeInteger(id) && id > 0;
function sanitize(ids) { return [...new Set(ids.filter(validId))]; }

export function loadFavorites(getStorage = browserStorage) {
  let raw;
  try { raw = getStorage().getItem(FAVORITES_KEY); }
  catch { return { ids: [], storageAvailable: false, notice: SESSION_NOTICE }; }
  if (raw === null) return { ids: [], storageAvailable: true, notice: "" };
  try {
    const data = JSON.parse(raw);
    if (!data || data.version !== 1 || !Array.isArray(data.ids)) throw new Error("Invalid shape");
    const ids = sanitize(data.ids);
    return { ids, storageAvailable: true,
      notice: ids.length === data.ids.length ? "" : "Se ignoraron IDs inválidos o repetidos en los favoritos." };
  } catch {
    return { ids: [], storageAvailable: true, notice: "Los datos guardados de favoritos no son válidos. Se inicia una lista vacía sin sobrescribirlos hasta que guardes un cambio." };
  }
}

export function saveFavorites(ids, getStorage = browserStorage) {
  try {
    getStorage().setItem(FAVORITES_KEY, JSON.stringify({ version: 1, ids: sanitize(ids) }));
    return { saved: true, notice: "" };
  } catch { return { saved: false, notice: SESSION_NOTICE }; }
}

export function toggleFavorite(ids, id) {
  const clean = sanitize(ids);
  if (!validId(id)) return clean;
  return clean.includes(id) ? clean.filter(value => value !== id) : [...clean, id];
}
