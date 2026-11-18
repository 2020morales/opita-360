// S04 locality restriction is separate from catalogue filters and trip ranking.
export function normalizeRecommendationMunicipality(value) {
  if (value == null) return "";
  if (typeof value !== "string") throw new TypeError("El municipio debe ser texto");
  return value.trim().toLocaleLowerCase("es-CO");
}
export function recommendationCandidates(destinations, municipality) {
  const normalized = normalizeRecommendationMunicipality(municipality);
  return destinations.filter(destination => !normalized || normalizeRecommendationMunicipality(destination.municipality) === normalized);
}
