import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getMunicipalities, validMunicipality, filterDestinations } from '../src/destination-filters.js';
const catalog = Object.freeze([
  Object.freeze({name:'Centro',municipality:'Neiva',category:'Cultura'}),
  Object.freeze({name:'Rio',municipality:'Neiva',category:'Aventura'}),
  Object.freeze({name:'Termales',municipality:'Rivera',category:'Bienestar'})
]);
test('unique ordered municipalities without empty values', () => {
  assert.deepEqual(getMunicipalities([...catalog,{municipality:''}]), ['Neiva','Rivera']);
});
test('all destinations by default', () => assert.equal(filterDestinations(catalog).length,3));
test('municipality selection', () => assert.equal(filterDestinations(catalog,{municipality:'Neiva'}).length,2));
test('three filters use AND and normalize search', () => assert.deepEqual(filterDestinations(catalog,{municipality:'Neiva',category:'Cultura',search:' CENTRO '}),[catalog[0]]));
test('empty results and recovery preserving category', () => {
  assert.deepEqual(filterDestinations(catalog,{municipality:'Rivera',category:'Cultura'}),[]);
  assert.deepEqual(filterDestinations(catalog,{municipality:'Todos',category:'Cultura'}),[catalog[0]]);
});
test('catalog replacement resets invalid selection', () => assert.equal(validMunicipality('Neiva',['Rivera']),'Todos'));
test('valid selection and Todos remain', () => {
  assert.equal(validMunicipality('Neiva',['Neiva']),'Neiva');
  assert.equal(validMunicipality('Todos',[]),'Todos');
});
test('empty catalog', () => {
  assert.deepEqual(getMunicipalities([]),[]); assert.deepEqual(filterDestinations([]),[]);
});
test('does not mutate input', () => {
  getMunicipalities(catalog); filterDestinations(catalog,{municipality:'Neiva'});
  assert.equal(catalog.length,3); assert.equal(catalog[0].name,'Centro');
});
