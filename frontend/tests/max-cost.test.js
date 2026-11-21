import { test } from 'node:test';
import assert from 'node:assert/strict';
import { filterDestinations, parseMaxCost } from '../src/destination-filters.js';
const catalog = Object.freeze([
  Object.freeze({ name:'Malecón', municipality:'Neiva', category:'Cultura', price:35000 }),
  Object.freeze({ name:'Centro', municipality:'Neiva', category:'Cultura', price:45000 }),
  Object.freeze({ name:'Termales', municipality:'Rivera', category:'Bienestar', price:65000 })
]);
test('S02 AC-01 maximum cost is inclusive', () => {
  assert.deepEqual(filterDestinations(catalog,{maxCost:35000}),[catalog[0]]);
  assert.deepEqual(filterDestinations(catalog,{maxCost:34999}),[]);
});
test('S02 AC-02 empty maximum keeps all other filters active', () => {
  assert.deepEqual(filterDestinations(catalog,{maxCost:'',municipality:'Neiva',category:'Cultura',search:' MALECÓN '}),[catalog[0]]);
});
test('S02 combines price with municipality category and search using AND', () => {
  assert.deepEqual(filterDestinations(catalog,{maxCost:40000,municipality:'Neiva',category:'Cultura',search:'Centro'}),[]);
  assert.deepEqual(filterDestinations(catalog,{maxCost:45000,municipality:'Neiva',category:'Cultura',search:'Centro'}),[catalog[1]]);
});
test('S02 zero is a valid limit and excludes positive prices', () => {
  assert.deepEqual(parseMaxCost('0'),{valid:true,value:0});
  assert.deepEqual(filterDestinations(catalog,{maxCost:0}),[]);
});
test('S02 parsing distinguishes empty, decimal, negative and nonnumeric values', () => {
  for(const value of ['', '  ', null, undefined]) assert.deepEqual(parseMaxCost(value),{valid:true,value:null});
  assert.deepEqual(parseMaxCost(' 35000.50 '),{valid:true,value:35000.5});
  for(const value of ['-1','abc','35abc','Infinity','0x10','1e3',NaN,Infinity,{},[]]) assert.equal(parseMaxCost(value).valid,false);
});
test('S02 filtering does not mutate frozen catalogue', () => {
  const before=JSON.stringify(catalog); filterDestinations(catalog,{maxCost:45000});
  assert.equal(JSON.stringify(catalog),before);
});
