// Pure functions shared by the React view and its regression tests.
export function getMunicipalities(destinations) {
  return [...new Set(destinations.map(d => d.municipality).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, "es"));
}

export function validMunicipality(selected, municipalities) {
  return selected === "Todos" || municipalities.includes(selected) ? selected : "Todos";
}

// Empty means no limit. Reject coercions such as hex, exponents, objects or Infinity.
export function parseMaxCost(input) {
  if (input == null || (typeof input === "string" && input.trim() === "")) return { valid: true, value: null };
  if (!["string", "number"].includes(typeof input)) return { valid: false, value: null };
  const text = String(input).trim();
  const value = Number(text);
  return /^\d+(?:\.\d+)?$/.test(text) && Number.isFinite(value) && value >= 0
    ? { valid: true, value } : { valid: false, value: null };
}

export function filterDestinations(destinations, { category = "Todos", municipality = "Todos", search = "", maxCost = null } = {}) {
  const query = search.trim().toLowerCase();
  const limit = parseMaxCost(maxCost);
  return destinations.filter(d =>
    (!limit.valid || limit.value === null || d.price <= limit.value) &&
    (category === "Todos" || d.category === category) &&
    (municipality === "Todos" || d.municipality === municipality) &&
    (!query || `${d.name} ${d.municipality} ${d.category}`.toLowerCase().includes(query)));
}
