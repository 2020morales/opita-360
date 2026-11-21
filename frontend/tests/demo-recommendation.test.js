import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildItinerary, itineraryNotices } from '../src/demo-recommendation.js';

// Mismo catálogo que usa el modo demostración y que el backend valida como idéntico.
const catalog = Object.freeze(JSON.parse(readFileSync(new URL('../src/fallback-destinations.json', import.meta.url), 'utf8')));
const ids = list => list.map(d => d.id);

// Los valores esperados se obtuvieron de POST /api/recommendations con la misma entrada.
test('REV-01 demo respeta el presupuesto como la API', () => {
  const { itinerary, total } = buildItinerary(catalog, { days: 3, budget: 50000, interests: ['cultura'] });
  assert.deepEqual(ids(itinerary), [3]);
  assert.equal(total, 35000);
});

test('REV-01 demo coincide con la API en caso normal', () => {
  const { itinerary, total } = buildItinerary(catalog, { days: 2, budget: 200000, interests: ['naturaleza'] });
  assert.deepEqual(ids(itinerary), [6, 5]);
  assert.equal(total, 135000);
});

test('REV-01 demo conserva la excepción de primera parada con presupuesto cero', () => {
  const { itinerary, total } = buildItinerary(catalog, { days: 2, budget: 0, interests: ['naturaleza'] });
  assert.deepEqual(ids(itinerary), [6]);
  assert.equal(total, 65000);
});

test('REV-01 intereses sin coincidencias usan todos los candidatos', () => {
  const { itinerary } = buildItinerary(catalog, { days: 1, budget: 200000, interests: ['sin-coincidencias'] });
  assert.deepEqual(ids(itinerary), [3]);
});

test('REV-05 intereses con mayúsculas y espacios coinciden', () => {
  const { itinerary } = buildItinerary(catalog, { days: 2, budget: 200000, interests: ['  Naturaleza '] });
  assert.deepEqual(ids(itinerary), [6, 5]);
});

test('REV-01 no muta el catálogo', () => {
  const before = JSON.stringify(catalog);
  buildItinerary(catalog, { days: 7, budget: 1000000, interests: ['cultura'] });
  assert.equal(JSON.stringify(catalog), before);
});

test('REV-03 avisa cuando la primera parada supera el presupuesto', () => {
  const notice = itineraryNotices({ days: 1, budget: 0, itinerary: [catalog[5]], total: 65000 });
  assert.match(notice, /supera tu presupuesto/);
});

test('REV-06 avisa cuando hay menos paradas que días', () => {
  const notice = itineraryNotices({ days: 7, budget: 10 ** 8, itinerary: [catalog[0], catalog[1]], total: 205000 });
  assert.match(notice, /2 parada\(s\) para 7 día\(s\)/);
});

test('REV-03/06 sin avisos en un caso normal', () => {
  assert.equal(itineraryNotices({ days: 1, budget: 200000, itinerary: [catalog[2]], total: 35000 }), '');
});

test('REV2-04 avisa cuando ningún destino coincide con los intereses', () => {
  const { itinerary, total, matched } = buildItinerary(catalog, { days: 1, budget: 200000, interests: ['sin-coincidencias'] });
  assert.equal(matched, false);
  assert.match(itineraryNotices({ days: 1, budget: 200000, itinerary, total, matched }), /Ningún destino coincide con tus intereses/);
});

test('REV2-04 sin aviso de intereses cuando sí coinciden', () => {
  const { itinerary, total, matched } = buildItinerary(catalog, { days: 1, budget: 200000, interests: ['cultura'] });
  assert.equal(matched, true);
  assert.doesNotMatch(itineraryNotices({ days: 1, budget: 200000, itinerary, total, matched }), /Ningún destino/);
});
