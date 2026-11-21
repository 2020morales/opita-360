// Mismo tope que TripRequest.budget en backend/app/main.py (le=100000000);
// backend/tests/test_review_fixes.py comprueba que ambos coincidan.
export const MAX_BUDGET = 100000000;
const COP = new Intl.NumberFormat("es-CO", { maximumFractionDigits: 0 });

// La API exige un entero entre 0 y MAX_BUDGET; se valida antes de enviar para
// no confundir un dato inválido con una API caída.
export function parseBudget(input) {
  const text = typeof input === "string" ? input.trim() : "";
  if (!text) return { valid: false, value: null, error: "Ingresa un presupuesto en pesos colombianos." };
  if (!/^\d+$/.test(text)) return { valid: false, value: null, error: "El presupuesto debe ser un número entero, sin decimales ni signos." };
  const value = Number(text);
  if (value > MAX_BUDGET) return { valid: false, value: null, error: `El presupuesto máximo es ${COP.format(MAX_BUDGET)} COP.` };
  return { valid: true, value, error: "" };
}

// 2xx: propuesta de la API. 422: la API rechazó los datos (se informa, sin modo demo).
// Cualquier otro estado o un fallo de red: la API no está disponible y se usa el modo demo.
export function recommendationOutcome(status) {
  if (status >= 200 && status < 300) return "api";
  if (status === 422) return "invalid";
  return "demo";
}
