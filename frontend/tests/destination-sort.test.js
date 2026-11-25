import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { DEFAULT_SORT, SORT_OPTIONS, sortDestinations, sortStatus } from '../src/destination-sort.js';
import { filterDestinations } from '../src/destination-filters.js';

const freeze = items => Object.freeze(items.map(item => Object.freeze(item)));
const catalog = freeze([
  { id: 3, name: 'Termales', price: 65000, category: 'Bienestar', municipality: 'Rivera' },
  { id: 1, name: 'Tatacoa', price: 85000, category: 'Naturaleza', municipality: 'Villavieja' },
  { id: 4, name: 'Bordones', price: 35000, category: 'Naturaleza', municipality: 'Isnos' },
  { id: 2, name: 'Águila', price: 85000, category: 'Cultura', municipality: 'Neiva' }
]);
const ids = list => list.map(d => d.id);

// Fundacional: opciones, valor por defecto y robustez (FR-001, FR-005, FR-006)
test('options keep the order and labels of the contract', () => {
  assert.equal(DEFAULT_SORT, 'recomendados');
  assert.deepEqual(SORT_OPTIONS.map(o => o.value), ['recomendados', 'costo-asc', 'costo-desc', 'nombre-asc']);
  assert.deepEqual(SORT_OPTIONS.map(o => o.label), ['Recomendados', 'Costo: menor a mayor', 'Costo: mayor a menor', 'Nombre: A–Z']);
});
test('default criterion keeps catalog order in a new array', () => {
  const result = sortDestinations(catalog);
  assert.deepEqual(ids(result), [3, 1, 4, 2]);
  assert.notEqual(result, catalog);
});
test('unknown, null or missing criterion behaves as recomendados', () => {
  for (const criterion of ['precio', null, undefined, 42]) assert.deepEqual(ids(sortDestinations(catalog, criterion)), [3, 1, 4, 2]);
});
test('empty or missing catalog returns an empty array', () => {
  assert.deepEqual(sortDestinations([], 'costo-asc'), []);
  assert.deepEqual(sortDestinations(undefined, 'costo-asc'), []);
});
test('does not mutate the received catalog', () => {
  for (const option of SORT_OPTIONS) sortDestinations(catalog, option.value);
  assert.deepEqual(ids(catalog), [3, 1, 4, 2]);
});

// US1: costo (FR-002)
test('costo-asc orders from cheapest and breaks ties by name', () => {
  assert.deepEqual(ids(sortDestinations(catalog, 'costo-asc')), [4, 3, 2, 1]);
});
test('costo-desc orders from most expensive and still breaks ties by name A-Z', () => {
  assert.deepEqual(ids(sortDestinations(catalog, 'costo-desc')), [2, 1, 3, 4]);
});
test('same price and same name fall back to id', () => {
  const twins = freeze([{ id: 9, name: 'Mirador', price: 10 }, { id: 5, name: 'mirador', price: 10 }]);
  assert.deepEqual(ids(sortDestinations(twins, 'costo-asc')), [5, 9]);
  assert.deepEqual(ids(sortDestinations(twins, 'nombre-asc')), [5, 9]);
});

// US2: nombre en español (FR-003)
test('nombre-asc keeps an accented initial next to its plain letter', () => {
  assert.deepEqual(sortDestinations(catalog, 'nombre-asc').map(d => d.name), ['Águila', 'Bordones', 'Tatacoa', 'Termales']);
});

// US3: orden sobre resultados filtrados, con el catálogo del modo demostración (FR-004, FR-008)
test('sorting applies on top of the active filters using the demo catalog', () => {
  const demo = JSON.parse(readFileSync(new URL('../src/fallback-destinations.json', import.meta.url), 'utf8'));
  const cultura = filterDestinations(demo, { category: 'Cultura' });
  const sorted = sortDestinations(cultura, 'costo-asc');
  assert.ok(sorted.every(d => d.category === 'Cultura'));
  assert.deepEqual(sorted.map(d => d.price), [35000, 45000, 120000]);
});

// Anuncio para lectores de pantalla (FR-009)
test('sortStatus announces count and applied criterion', () => {
  assert.equal(sortStatus(8, 'costo-asc'), '8 destinos ordenados por Costo: menor a mayor');
  assert.equal(sortStatus(1, 'nombre-asc'), '1 destino ordenado por Nombre: A–Z');
  assert.equal(sortStatus(0, 'desconocido'), '0 destinos ordenados por Recomendados');
});
