import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { pickRandomDestination } from '../src/random-destination.js';
import { filterDestinations } from '../src/destination-filters.js';

const freeze = items => Object.freeze(items.map(item => Object.freeze(item)));
const list = freeze([{ id: 1, name: 'Tatacoa' }, { id: 2, name: 'San Agustín' }, { id: 3, name: 'Rivera' }, { id: 4, name: 'Betania' }]);
const fixed = value => () => value;

// Fundacional
test('empty or invalid list returns null', () => {
  assert.equal(pickRandomDestination([]), null);
  assert.equal(pickRandomDestination(undefined), null);
  assert.equal(pickRandomDestination('no es lista'), null);
});
test('does not mutate the list', () => {
  pickRandomDestination(list, { previousId: 2, random: fixed(0.5) });
  assert.deepEqual(list.map(d => d.id), [1, 2, 3, 4]);
});

// US1: misma probabilidad por índice (FR-003)
test('random value maps uniformly to an index', () => {
  assert.equal(pickRandomDestination(list, { random: fixed(0) }).id, 1);
  assert.equal(pickRandomDestination(list, { random: fixed(0.5) }).id, 3);
  assert.equal(pickRandomDestination(list, { random: fixed(0.999) }).id, 4);
});
test('every destination is reachable with the same share of the [0,1) range', () => {
  const counts = new Map();
  for (let i = 0; i < 400; i++) {
    const id = pickRandomDestination(list, { random: fixed(i / 400) }).id;
    counts.set(id, (counts.get(id) ?? 0) + 1);
  }
  assert.deepEqual([...counts.values()], [100, 100, 100, 100]);
});
test('out-of-range or non-numeric random values never return undefined', () => {
  assert.equal(pickRandomDestination(list, { random: fixed(1) }).id, 4);
  assert.equal(pickRandomDestination(list, { random: fixed(-3) }).id, 1);
  assert.equal(pickRandomDestination(list, { random: fixed(Number.NaN) }).id, 1);
  assert.equal(pickRandomDestination(list, { random: fixed('x') }).id, 1);
});

// US2: no repetir el anterior (FR-003, SC-002, Edge Cases)
test('with two or more visible, the previous suggestion is excluded', () => {
  for (const r of [0, 0.3, 0.6, 0.99]) assert.notEqual(pickRandomDestination(list, { previousId: 2, random: fixed(r) }).id, 2);
  const pair = list.slice(0, 2);
  assert.equal(pickRandomDestination(pair, { previousId: 1, random: fixed(0) }).id, 2);
  assert.equal(pickRandomDestination(pair, { previousId: 2, random: fixed(0.99) }).id, 1);
});
test('a single visible destination is suggested even if it was the previous one', () => {
  assert.equal(pickRandomDestination(list.slice(2, 3), { previousId: 3, random: fixed(0.7) }).id, 3);
});
test('a previous id that is no longer visible does not change the candidates', () => {
  assert.equal(pickRandomDestination(list, { previousId: 99, random: fixed(0.999) }).id, 4);
});

// Solo entre los visibles, con el catálogo del modo demostración (FR-002, FR-007, SC-001)
test('suggestions always satisfy the active filters including only favorites', () => {
  const demo = JSON.parse(readFileSync(new URL('../src/fallback-destinations.json', import.meta.url), 'utf8'));
  const favorites = [2, 3, 8];
  const visible = filterDestinations(demo, { category: 'Cultura' }).filter(d => favorites.includes(d.id));
  let previousId = null;
  for (let i = 0; i < 20; i++) {
    const pick = pickRandomDestination(visible, { previousId, random: fixed((i * 7 % 10) / 10) });
    assert.equal(pick.category, 'Cultura');
    assert.ok(favorites.includes(pick.id));
    assert.notEqual(pick.id, previousId);
    previousId = pick.id;
  }
});
