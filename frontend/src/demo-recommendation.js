// Réplica del algoritmo de POST /api/recommendations (backend/app/main.py) para el modo
// demostración: misma selección por intereses, mismo orden y mismo respeto al presupuesto.
const normalize = value => String(value).trim().toLowerCase();

export function buildItinerary(candidates, { days, budget, interests }) {
  const wanted = interests.map(normalize);
  const matches = candidates.filter(d =>
    wanted.some(interest => d.tags.some(tag => normalize(tag) === interest) || normalize(d.category) === interest));
  // Asequibles primero y luego por precio; se ordena una copia para no mutar el catálogo.
  const selected = [...(matches.length ? matches : candidates)]
    .sort((a, b) => (a.price > budget) - (b.price > budget) || a.price - b.price);
  const itinerary = [];
  let total = 0;
  for (const destination of selected) {
    if (itinerary.length >= days) break;
    // Igual que la API: la primera parada se admite aunque supere el presupuesto.
    if (total + destination.price <= budget || !itinerary.length) {
      itinerary.push(destination);
      total += destination.price;
    }
  }
  return { itinerary, total };
}

// Mismos avisos que agrega la API al campo notice.
export function itineraryNotices({ days, budget, itinerary, total }) {
  let notice = "";
  if (total > budget) notice += "La primera parada supera tu presupuesto; se incluye como referencia. ";
  if (itinerary.length && itinerary.length < days) notice += `Solo hay ${itinerary.length} parada(s) para ${days} día(s) con estos filtros. `;
  return notice;
}
