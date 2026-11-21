import { test } from 'node:test';
import assert from 'node:assert/strict';
import { MAX_BUDGET, apiStatusAfter, parseBudget, recommendationOutcome } from '../src/trip-request.js';

test('REV2-01 el tope del presupuesto coincide con la API', () => {
  assert.equal(MAX_BUDGET, 100000000);
});

test('REV2-01 presupuestos válidos, incluidos los que no son múltiplos de 10.000', () => {
  for (const [input, value] of [['0', 0], ['155000', 155000], [' 200000 ', 200000], ['100000000', 100000000]]) {
    assert.deepEqual(parseBudget(input), { valid: true, value, error: '' });
  }
});

test('REV2-01 presupuesto por encima del tope se rechaza con mensaje', () => {
  const result = parseBudget('200000000');
  assert.equal(result.valid, false);
  assert.match(result.error, /100\.000\.000/);
});

test('REV2-01 presupuesto vacío, negativo, decimal o no numérico se rechaza', () => {
  for (const input of ['', '   ', '-1', '150000.5', 'abc', '1e6', null, undefined]) {
    const result = parseBudget(input);
    assert.equal(result.valid, false, String(input));
    assert.ok(result.error, String(input));
  }
});

test('REV2-01 un 422 de la API es error de validación, no modo demo', () => {
  assert.equal(recommendationOutcome(200), 'api');
  assert.equal(recommendationOutcome(422), 'invalid');
  for (const status of [404, 500, 503]) assert.equal(recommendationOutcome(status), 'demo');
});

test('REV3-01 el indicador de API refleja la última petición de recomendación', () => {
  assert.equal(apiStatusAfter('demo', 'conectada'), 'demostración');
  assert.equal(apiStatusAfter('api', 'demostración'), 'conectada');
  // Un 422 demuestra que la API responde: el indicador no cambia.
  assert.equal(apiStatusAfter('invalid', 'conectada'), 'conectada');
  assert.equal(apiStatusAfter('invalid', 'demostración'), 'demostración');
});
