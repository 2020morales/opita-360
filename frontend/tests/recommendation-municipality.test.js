import {test} from 'node:test';
import assert from 'node:assert/strict';
import {normalizeRecommendationMunicipality, recommendationCandidates} from '../src/recommendation-municipality.js';
const catalog=Object.freeze([Object.freeze({id:1,municipality:'Neiva'}),Object.freeze({id:2,municipality:'San Agustín'}),Object.freeze({id:3,municipality:'Neiva'})]);
test('S04 omission null empty whitespace are unrestricted',()=>{for(const value of [undefined,null,'','   '])assert.deepEqual(recommendationCandidates(catalog,value),catalog);});
test('S04 normalization preserves accents and ignores case and outer spaces',()=>{assert.equal(normalizeRecommendationMunicipality('  sAn aGuStÍn '),'san agustín');assert.deepEqual(recommendationCandidates(catalog,'  NEIVA '),[catalog[0],catalog[2]]);});
test('S04 unknown municipality never returns global fallback',()=>assert.deepEqual(recommendationCandidates(catalog,'Municipio sin destinos'),[]));
test('S04 rejects nontext input instead of coercing it',()=>{for(const value of [1,true,[],{}])assert.throws(()=>normalizeRecommendationMunicipality(value),TypeError);});
test('S04 candidate selection does not mutate catalogue',()=>{const before=JSON.stringify(catalog);recommendationCandidates(catalog,'Neiva');assert.equal(JSON.stringify(catalog),before);});
