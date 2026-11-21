import { test } from 'node:test';
import assert from 'node:assert/strict';
import { FAVORITES_KEY, loadFavorites, saveFavorites, toggleFavorite } from '../src/favorites.js';
function storage(raw=null) { return {raw,writes:[],getItem(key){assert.equal(key,FAVORITES_KEY);return this.raw;},setItem(key,value){this.writes.push([key,value]);this.raw=value;}}; }
test('S03 AC-01 roundtrip persists version and IDs only',()=>{
 const s=storage();assert.equal(saveFavorites([3,3,999],()=>s).saved,true);
 assert.deepEqual(JSON.parse(s.raw),{version:1,ids:[3,999]});
 assert.deepEqual(loadFavorites(()=>s).ids,[3,999]);
});
test('S03 initialization never overwrites stored favorites',()=>{
 const s=storage(JSON.stringify({version:1,ids:[3,999]}));assert.deepEqual(loadFavorites(()=>s).ids,[3,999]);assert.equal(s.writes.length,0);
});
test('S03 missing storage value is empty without write',()=>{
 const s=storage();assert.deepEqual(loadFavorites(()=>s).ids,[]);assert.equal(s.writes.length,0);
});
test('S03 AC-03 corrupt JSON recovers without overwriting evidence',()=>{
 const s=storage('{broken');const result=loadFavorites(()=>s);assert.deepEqual(result.ids,[]);assert.ok(result.notice);assert.equal(s.raw,'{broken');assert.equal(s.writes.length,0);
});
test('S03 manipulated IDs are deduplicated and only safe positive integers survive',()=>{
 const s=storage(JSON.stringify({version:1,ids:[3,3,-1,0,1.5,'2',null,{},999,Number.MAX_SAFE_INTEGER+1]}));
 assert.deepEqual(loadFavorites(()=>s).ids,[3,999]);assert.equal(s.writes.length,0);
});
test('S03 invalid shapes and unknown versions remain untouched',()=>{
 for(const value of [null,[],{}, {version:2,ids:[3]}, {version:1,ids:'3'}]){
  const s=storage(JSON.stringify(value));const before=s.raw;assert.deepEqual(loadFavorites(()=>s).ids,[]);assert.equal(s.raw,before);assert.equal(s.writes.length,0);
 }
});
test('S03 AC-04 storage getter and read exceptions use session mode',()=>{
 for(const provider of [()=>{throw new Error('blocked');},()=>({getItem(){throw new Error('denied');}})]){
  const result=loadFavorites(provider);assert.deepEqual(result.ids,[]);assert.equal(result.storageAvailable,false);assert.ok(result.notice.includes('sesión'));
 }
});
test('S03 AC-04 write failure reports no persistence',()=>{
 const result=saveFavorites([3],()=>({setItem(){throw new Error('quota');}}));assert.equal(result.saved,false);assert.ok(result.notice.includes('sesión'));
});
test('S03 AC-02 toggles without mutating input or unknown IDs',()=>{
 const original=Object.freeze([3,999]);assert.deepEqual(toggleFavorite(original,3),[999]);assert.deepEqual(toggleFavorite(original,2),[3,999,2]);assert.deepEqual(original,[3,999]);assert.deepEqual(toggleFavorite(original,-1),[3,999]);
});
test('S03 saves only application key and sanitized IDs',()=>{
 const s=storage();saveFavorites([3,'4',-1,3,999],()=>s);assert.deepEqual(s.writes,[[FAVORITES_KEY,JSON.stringify({version:1,ids:[3,999]})]]);
});
