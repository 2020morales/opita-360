// Pure functions shared by the React view and its regression tests.
export function getMunicipalities(destinations) {
  return [...new Set(destinations.map(d => d.municipality).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, "es"));
}

export function validMunicipality(selected, municipalities) {
  return selected === "Todos" || municipalities.includes(selected) ? selected : "Todos";
}

export function filterDestinations(destinations, { category = "Todos", municipality = "Todos", search = "" } = {}) {
  const query = search.trim().toLowerCase();
  return destinations.filter(d =>
    (category === "Todos" || d.category === category) &&
    (municipality === "Todos" || d.municipality === municipality) &&
    (!query || `${d.name} ${d.municipality} ${d.category}`.toLowerCase().includes(query)));
}
