// Pure sorting for the destinations grid (specs/001-ordenar-destinos).
export const DEFAULT_SORT = "recomendados";
export const SORT_OPTIONS = Object.freeze([
  Object.freeze({ value: "recomendados", label: "Recomendados" }),
  Object.freeze({ value: "costo-asc", label: "Costo: menor a mayor" }),
  Object.freeze({ value: "costo-desc", label: "Costo: mayor a menor" }),
  Object.freeze({ value: "nombre-asc", label: "Nombre: A–Z" })
]);

const byName = (a, b) => String(a.name ?? "").localeCompare(String(b.name ?? ""), "es", { sensitivity: "base" });
const byId = (a, b) => (a.id ?? 0) - (b.id ?? 0);
const COMPARATORS = {
  "costo-asc": (a, b) => a.price - b.price || byName(a, b) || byId(a, b),
  "costo-desc": (a, b) => b.price - a.price || byName(a, b) || byId(a, b),
  "nombre-asc": (a, b) => byName(a, b) || byId(a, b)
};

// Unknown criteria fall back to the catalog order. Always returns a new array.
export function sortDestinations(destinations, criterion = DEFAULT_SORT) {
  const copy = Array.isArray(destinations) ? [...destinations] : [];
  const compare = Object.hasOwn(COMPARATORS, criterion) ? COMPARATORS[criterion] : null;
  return compare ? copy.sort(compare) : copy;
}

export function sortStatus(count, criterion = DEFAULT_SORT) {
  const option = SORT_OPTIONS.find(o => o.value === criterion) ?? SORT_OPTIONS[0];
  return count === 1
    ? `1 destino ordenado por ${option.label}`
    : `${count} destinos ordenados por ${option.label}`;
}
