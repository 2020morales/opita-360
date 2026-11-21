import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';

// Regresiones de la auditoría Lighthouse: carga de la portada, fuentes, imágenes,
// contraste, tamaño de letra, nombre accesible del logo y favicon.
const read = path => readFileSync(new URL(path, import.meta.url), 'utf8');
const html = read('../index.html');
const css = read('../src/styles.css');
const jsx = read('../src/main.jsx');

function luminance(hex) {
  const channel = value => {
    const c = parseInt(value, 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  };
  const [r, g, b] = [hex.slice(0, 2), hex.slice(2, 4), hex.slice(4, 6)].map(channel);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function contrast(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}
// Color de texto de la primera regla cuyo selector es exactamente `selector`.
function textColor(selector) {
  const escaped = selector.replace(/[.*+?^${}()|[\]\\>]/g, '\\$&');
  const match = css.match(new RegExp(`(?:^|[}\\n])${escaped}\\{[^}]*?(?<![-\\w])color:#([0-9a-fA-F]{6})`));
  assert.ok(match, `sin color para ${selector}`);
  return match[1];
}

test('PERF-01 la foto de portada se precarga con prioridad alta y es la misma que usa el CSS', () => {
  const preload = html.match(/<link rel="preload" as="image" href="([^"]+)" fetchpriority="high"/);
  assert.ok(preload, 'falta el preload de la portada');
  const heroUrl = css.match(/\.hero-photo\{[^}]*background-image:url\('([^']+)'\)/)[1];
  assert.equal(preload[1].replaceAll('&amp;', '&'), heroUrl);
  assert.doesNotMatch(heroUrl, /w=2000|q=90/, 'la portada sigue a 2000px y calidad 90');
});

test('PERF-03 las tarjetas ofrecen 400w y 800w y declaran el ancho real de cada columna', () => {
  assert.match(jsx, /srcSet=\{\[400, 800\]\.map\(/);
  assert.match(jsx, /const CARD_SIZES = "\(max-width: 380px\) 100vw, \(max-width: 1050px\) 50vw, 25vw";/);
  // Las columnas de la grilla deben ser las que CARD_SIZES declara.
  assert.match(css, /\.destination-grid\{display:grid;grid-template-columns:repeat\(4,/);
  assert.match(css, /@media\(max-width:1050px\)\{[^@]*\.destination-grid\{grid-template-columns:repeat\(2,/);
  assert.match(css, /@media\(max-width:380px\)\{\.destination-grid\{grid-template-columns:1fr\}/);
});

test('PERF-02 las fuentes se cargan desde index.html, no con @import bloqueante', () => {
  assert.doesNotMatch(css, /@import/);
  assert.match(html, /<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com">/);
  assert.match(html, /<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com" crossorigin>/);
  // No bloquea el primer pintado: se aplica al cargar, con respaldo sin JavaScript.
  assert.match(html, /<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com\/css2\?family=DM\+Sans[^"]*" media="print" onload="this\.media='all'">/);
  assert.match(html, /<noscript><link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com\/css2\?family=DM\+Sans/);
});

test('PERF-03 las fotos de las tarjetas son <img> con carga diferida, no fondos CSS', () => {
  // Busca dentro de la misma línea: srcSet contiene "=>" y no puede usarse [^>]*.
  assert.match(jsx, /<img className="destination-photo"[^\n]*loading="lazy"/);
  assert.doesNotMatch(jsx, /backgroundImage:`linear-gradient\([^`]*url\(/);
});

test('A11Y-01 los textos señalados por Lighthouse alcanzan contraste 4.5:1', () => {
  const pairs = [
    ['.nav-wrap .brand b', 'f5f3ec'], ['.brand small', 'f5f3ec'], ['.section-kicker', 'f5f3ec'],
    ['.section-kicker', 'e9eddf'], ['.intro>p', 'f5f3ec'], ['.municipality-filter', 'ffffff'],
    ['.searchbox', 'ffffff'], ['.destination-info p', 'ffffff'], ['.planner-intro>p', 'f5f3ec'],
    ['.form-top p', 'ffffff'], ['.step', 'ffffff'], ['.range-ends', 'ffffff'],
    ['.money-input', 'ffffff'], ['.form-disclaimer', 'ffffff'],
    ['.map-copy>p', 'e9eddf'], ['.map-legend', 'e9eddf'],
  ];
  for (const [selector, background] of pairs) {
    const ratio = contrast(textColor(selector), background);
    assert.ok(ratio >= 4.5, `${selector} sobre #${background}: ${ratio.toFixed(2)}:1`);
  }
});

test('A11Y-02 ningún texto queda por debajo de 12px, salvo el sello decorativo', () => {
  // El sello circular de la portada repite la marca y su texto debe caber en el círculo.
  const rules = [...css.matchAll(/([^{}]+)\{([^}]*)\}/g)];
  const small = rules.filter(([, selector, body]) => !/^\.hero-stamp /.test(selector.trim()))
    .flatMap(([, selector, body]) => [...body.matchAll(/font-size:(\d+(?:\.\d+)?)px/g)]
      .filter(m => Number(m[1]) < 12).map(m => `${selector.trim()}: ${m[1]}px`));
  assert.deepEqual(small, []);
  assert.match(jsx, /<div className="hero-stamp" aria-hidden="true">/);
});

test('A11Y-03 el nombre accesible del logo empieza con su texto visible', () => {
  assert.match(jsx, /className="brand" href="#inicio" aria-label="OPITA 360 El Huila por descubrir, inicio"/);
  // Sin el espacio, el texto visible sería "OPITA 360EL HUILA…" y no coincidiría con la etiqueta.
  assert.match(jsx, /<span>OPITA <b>360<\/b> <small>EL HUILA POR DESCUBRIR<\/small><\/span>/);
});

test('A11Y-04 existe favicon y está enlazado', () => {
  assert.match(html, /<link rel="icon" type="image\/svg\+xml" href="\/favicon\.svg">/);
  assert.ok(existsSync(new URL('../public/favicon.svg', import.meta.url)));
});
