// Pure "Sorpréndeme" pick (specs/002-destino-aleatorio). Randomness is injected for tests.
export function pickRandomDestination(destinations, { previousId = null, random = Math.random } = {}) {
  if (!Array.isArray(destinations) || destinations.length === 0) return null;
  const candidates = destinations.length >= 2
    ? destinations.filter(destination => destination.id !== previousId)
    : destinations;
  const pool = candidates.length ? candidates : destinations;
  const value = Number(random());
  const raw = Number.isFinite(value) ? Math.floor(value * pool.length) : 0;
  const index = Math.min(Math.max(raw, 0), pool.length - 1);
  return pool[index];
}
