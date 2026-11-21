import React, { useEffect, useMemo, useState, useRef } from "react";
import { createRoot } from "react-dom/client";
import { ArrowDownRight, ArrowRight, ArrowUpRight, Compass, MapPin, Sparkles, CalendarDays, Wallet, Heart, Menu, X, Mountain, Waves, Search } from "lucide-react";
import "./styles.css";
import DestinationDetail from "./destination-detail.jsx";
import { getMunicipalities, validMunicipality, filterDestinations, parseMaxCost } from "./destination-filters.js";
import { loadFavorites, saveFavorites, toggleFavorite, SESSION_NOTICE } from "./favorites.js";
import { recommendationCandidates } from "./recommendation-municipality.js";
import { downloadItinerary } from "./export-itinerary.js";
import { buildItinerary, itineraryNotices } from "./demo-recommendation.js";
import { MAX_BUDGET, parseBudget, recommendationOutcome } from "./trip-request.js";
// Copia exacta del catálogo de la API (verificada por backend/tests/test_review_fixes.py).
import fallbackDestinations from "./fallback-destinations.json";

const API = "http://127.0.0.1:8000";
const COP = new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });
const photos = {
  "Desierto de la Tatacoa":"https://images.unsplash.com/photo-1509316785289-025f5b846b35?auto=format&fit=crop&w=900&q=85",
  "Parque Arqueológico de San Agustín":"https://images.unsplash.com/photo-1565538810643-b5bdb714032a?auto=format&fit=crop&w=900&q=85",
  "Malecón del río Magdalena":"https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=900&q=85",
  "Salto de Bordones":"https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=900&q=85",
  "Estrecho del río Magdalena":"https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=900&q=85",
  "Termales de Rivera":"https://images.unsplash.com/photo-1540541338287-41700207dee6?auto=format&fit=crop&w=900&q=85",
  "Represa de Betania":"https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=85",
  "Centro de Neiva y tradición opita":"https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=900&q=85"
};

function App() {
  const [destinations, setDestinations] = useState(fallbackDestinations);
  const [apiStatus, setApiStatus] = useState("probando");
  const [category, setCategory] = useState("Todos");
  const [municipality, setMunicipality] = useState("Todos");
  const [tripMunicipality, setTripMunicipality] = useState("");
  const [search, setSearch] = useState("");
  const [costInput, setCostInput] = useState("");
  const [maxCost, setMaxCost] = useState(null);
  const [costError, setCostError] = useState("");
  const [days, setDays] = useState(2);
  const [budget, setBudget] = useState("200000");
  const [interests, setInterests] = useState(["naturaleza"]);
  const [result, setResult] = useState(null);
  const [resultOrigin, setResultOrigin] = useState(null);
  const [exportError, setExportError] = useState("");
  const [tripError, setTripError] = useState("");
  const [loading, setLoading] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [detail, setDetail] = useState(null);
  const [favorites, setFavorites] = useState(() => loadFavorites());
  const [onlyFavorites, setOnlyFavorites] = useState(false);
  const favoritesRef = useRef(favorites);
  const favoritesFilterRef = useRef(null);
  const pendingFavoriteFocus = useRef(false);

  useEffect(() => {
    fetch(`${API}/api/destinations`)
      .then(r => { if (!r.ok) throw new Error("API"); return r.json(); })
      .then(data => { setDestinations(data.destinations || fallbackDestinations); setApiStatus("conectada"); })
      .catch(() => setApiStatus("demostración"));
  }, []);

  const municipalities = useMemo(() => getMunicipalities(destinations), [destinations]);

  useEffect(() => {
    setMunicipality(current => validMunicipality(current, municipalities));
    setTripMunicipality(current => municipalities.includes(current) ? current : "");
  }, [municipalities]);

  const filtered = useMemo(() => {
    const matches = filterDestinations(destinations, { category, municipality, search, maxCost });
    return onlyFavorites ? matches.filter(destination => favorites.ids.includes(destination.id)) : matches;
  }, [destinations, category, municipality, search, maxCost, onlyFavorites, favorites.ids]);

  useEffect(() => {
    if (pendingFavoriteFocus.current) {
      pendingFavoriteFocus.current = false;
      favoritesFilterRef.current?.focus();
    }
  }, [favorites.ids]);

  function toggleDestinationFavorite(id) {
    const previous = favoritesRef.current;
    const ids = toggleFavorite(previous.ids, id);
    const persisted = previous.storageAvailable ? saveFavorites(ids) : { saved: false, notice: SESSION_NOTICE };
    const next = { ids, storageAvailable: persisted.saved, notice: persisted.notice };
    pendingFavoriteFocus.current = onlyFavorites && previous.ids.includes(id);
    favoritesRef.current = next;
    setFavorites(next);
  }

  function applyMaxCost(event) {
    event.preventDefault();
    const parsed = parseMaxCost(costInput);
    if (!parsed.valid) {
      setCostError("Ingresa un costo válido: cero o un número positivo, usando punto para decimales.");
      return;
    }
    setCostError("");
    setMaxCost(parsed.value);
  }

  function clearMaxCost() {
    setCostInput(""); setMaxCost(null); setCostError("");
  }

  const toggleInterest = (interest) => setInterests(prev => prev.includes(interest) ? prev.filter(x => x !== interest) : [...prev, interest]);

  async function makeTrip(e) {
    e.preventDefault();
    const parsedBudget = parseBudget(budget);
    if (!parsedBudget.valid) {
      setTripError(parsedBudget.error);
      document.getElementById("budget")?.focus();
      return;
    }
    setTripError("");
    setLoading(true);
    setExportError("");
    const payload = { days: Number(days), budget: parsedBudget.value, interests: interests.length ? interests : ["naturaleza"], ...(tripMunicipality ? { municipality: tripMunicipality } : {}) };
    try {
      const response = await fetch(`${API}/api/recommendations`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
      const outcome = recommendationOutcome(response.status);
      if (outcome === "invalid") {
        // Datos rechazados por la API: se informa en vez de simular una propuesta demo.
        setTripError("La API rechazó los datos del formulario. Revisa los días, el presupuesto y los intereses.");
        setLoading(false);
        return;
      }
      if (outcome !== "api") throw new Error("API");
      setResult(await response.json());
      setResultOrigin("api");
    } catch {
      setResultOrigin("demo");
      const candidates = recommendationCandidates(destinations, payload.municipality);
      const { itinerary, total, matched } = buildItinerary(candidates, payload);
      const localityNotice = payload.municipality && !candidates.length ? "No hay destinos disponibles para el municipio seleccionado. " : "";
      const warnings = itineraryNotices({ ...payload, itinerary, total, matched });
      setResult({summary:`Propuesta de ${itinerary.length} parada(s) para ${days} día(s).`,method:"Recomendación local de demostración.",itinerary,estimated_total:total,budget:payload.budget,remaining_budget:Math.max(payload.budget-total,0),notice:`${localityNotice}${warnings}Valores orientativos; confirma precios y disponibilidad antes de viajar.`});
    }
    setLoading(false);
    setTimeout(() => document.getElementById("resultado")?.scrollIntoView({behavior:"smooth",block:"start"}), 80);
  }

  function exportTrip() {
    setExportError("");
    try { downloadItinerary(result, resultOrigin); }
    catch { setExportError("No se pudo iniciar la descarga. Intenta de nuevo o genera otra propuesta."); }
  }

  return <div className="app-shell">
    {detail && <DestinationDetail key={detail.destination.id} {...detail} api={API} onClose={() => setDetail(null)}/>}

    <div className="announcement"><span className="pulse"></span> Hecho en el Huila, pensado para quienes quieren descubrirlo <span className={`api-pill ${apiStatus}`}>{apiStatus === "conectada" ? "API conectada" : apiStatus === "probando" ? "Conectando API…" : "Modo demostración"}</span></div>
    <header className="nav-wrap">
      <a className="brand" href="#inicio" aria-label="OPITA 360 inicio"><span className="brand-mark"><Compass size={23}/></span><span>OPITA <b>360</b><small>EL HUILA POR DESCUBRIR</small></span></a>
      <button className="mobile-toggle" onClick={()=>setMobileMenu(!mobileMenu)} aria-label={mobileMenu ? "Cerrar menú" : "Abrir menú"} aria-expanded={mobileMenu} aria-controls="main-navigation">{mobileMenu?<X/>:<Menu/>}</button>
      <nav id="main-navigation" className={mobileMenu ? "nav-links open" : "nav-links"}>
        <a href="#destinos" onClick={()=>setMobileMenu(false)}>Destinos</a><a href="#mapa" onClick={()=>setMobileMenu(false)}>Mapa</a><a href="#aventura" onClick={()=>setMobileMenu(false)}>Diseña tu aventura</a>
        <a className="nav-cta" href="#aventura" onClick={()=>setMobileMenu(false)}>Comenzar <ArrowRight size={16}/></a>
      </nav>
    </header>

    <main>
      <section className="hero" id="inicio">
        <div className="hero-photo"></div><div className="hero-shade"></div>
        <div className="hero-content">
          <div className="eyebrow"><span></span> COLOMBIA · DEPARTAMENTO DEL HUILA</div>
          <h1>Tu próxima gran<br/><em>aventura es opita.</em></h1>
          <p>Montañas, desiertos, ríos e historias ancestrales. Descubre el Huila a tu manera y crea un recorrido que se ajuste a ti.</p>
          <div className="hero-actions"><a href="#destinos" className="button button-light">Explorar destinos <ArrowDownRight size={18}/></a><a href="#aventura" className="text-link">Crear mi itinerario <ArrowRight size={16}/></a></div>
          <div className="hero-proof"><div className="proof-icons"><span>🌵</span><span>🗿</span><span>💧</span></div><div><b>Una región, mil historias</b><small>Experiencias naturales y culturales</small></div></div>
        </div>
        <div className="hero-stamp"><span>DESCUBRE</span><b>HUILA</b><small>CON OJOS NUEVOS</small><Compass size={24}/></div>
        <div className="hero-bottom"><span><MapPin size={15}/> Neiva, Huila, Colombia</span><span>02° 55′ N · 75° 18′ O</span></div>
      </section>

      <section className="intro section-pad">
        <div><span className="section-kicker">01 / EXPLORA A TU RITMO</span><h2>No visites por visitar.<br/><em>Vive cada lugar.</em></h2></div>
        <p>OPITA 360 combina información turística y recomendaciones sencillas para ayudarte a elegir qué conocer, cuánto tiempo dedicar y cómo aprovechar tu presupuesto.</p>
      </section>

      <section className="destinations section-pad" id="destinos">
        <div className="section-heading"><div><span className="section-kicker">LUGARES QUE DEJAN HUELLA</span><h2>El Huila te espera<span className="dot">.</span></h2></div><a className="text-link dark" href="#mapa">Ver mapa <ArrowRight size={16}/></a></div>
        <div className="filter-row"><div className="searchbox"><Search size={17}/><input aria-label="Buscar destinos por nombre o municipio" value={search} onChange={e=>setSearch(e.target.value)} placeholder="Busca un destino o municipio…"/></div><label className="municipality-filter" htmlFor="municipality-filter"><MapPin size={16} aria-hidden="true"/><span>Municipio</span><select id="municipality-filter" value={municipality} onChange={e=>setMunicipality(e.target.value)}><option value="Todos">Todos los municipios</option>{municipalities.map(m=><option key={m} value={m}>{m}</option>)}</select></label><div className="filters">{["Todos","Naturaleza","Cultura","Aventura","Bienestar"].map(c=><button type="button" key={c} className={category===c?"filter active":"filter"} aria-pressed={category===c} onClick={()=>setCategory(c)}>{c}</button>)}</div></div>
        <form className="cost-filter" onSubmit={applyMaxCost}>
          <label htmlFor="max-cost">Costo máximo por destino (COP)</label>
          <div className="cost-filter-controls"><input id="max-cost" type="text" inputMode="decimal" value={costInput} onChange={event => setCostInput(event.target.value)} aria-invalid={Boolean(costError)} aria-describedby={costError ? "max-cost-hint max-cost-error" : "max-cost-hint"}/>
            <button type="submit">Aplicar costo</button><button type="button" onClick={clearMaxCost}>Quitar límite de costo</button></div>
          <p id="max-cost-hint">Vacío: sin límite. Usa cero o un número positivo; punto para decimales.</p>
          {costError && <p id="max-cost-error" role="alert">{costError}</p>}
          <p className="cost-filter-status" role="status" aria-live="polite">{maxCost === null ? "Sin límite de costo" : `Costo máximo aplicado: ${COP.format(maxCost)}`}</p>
        </form>
        <div className="favorites-controls"><label htmlFor="only-favorites"><input ref={favoritesFilterRef} id="only-favorites" type="checkbox" checked={onlyFavorites} onChange={event => setOnlyFavorites(event.target.checked)}/> Solo favoritos</label>
          <p role="status" aria-live="polite">{favorites.ids.filter(id => destinations.some(destination => destination.id === id)).length} destinos favoritos en el catálogo.</p>
          {favorites.notice && <p className="favorites-notice" role="alert">{favorites.notice}</p>}
        </div>
        <div className="destination-grid">{filtered.map((d,i)=><article className={`destination-card card-${d.color || "green"}`} key={d.id}>
          <div className="destination-image" style={{backgroundImage:`linear-gradient(180deg,transparent 40%,rgba(9,28,24,.72)),url("${photos[d.name] || photos["Desierto de la Tatacoa"]}")`}}>
            <span className="category-tag">{d.category}</span><button type="button" className={favorites.ids.includes(d.id) ? "heart saved" : "heart"} aria-pressed={favorites.ids.includes(d.id)} aria-label={favorites.ids.includes(d.id) ? `Quitar ${d.name} de favoritos` : `Guardar ${d.name} en favoritos`} title={favorites.ids.includes(d.id) ? "Quitar favorito" : "Guardar favorito"} onClick={()=>toggleDestinationFavorite(d.id)}><Heart size={17} aria-hidden="true"/></button>
            <span className="destination-number">{String(i+1).padStart(2, "0")}</span>
            <div className="destination-title"><span>{d.municipality} · HUILA</span><h3>{d.name}</h3></div>
          </div>
          <div className="destination-info"><p>{d.description}</p><button type="button" className="detail-open" aria-label={`Ver detalle de ${d.name}`} onClick={event => setDetail({ destination: d, demo: apiStatus !== "conectada", trigger: event.currentTarget })}>Ver detalle</button><div className="destination-meta"><span><Wallet size={15}/> Desde {COP.format(d.price)}</span><a href="#aventura" aria-label={`Planear visita a ${d.name}`}><ArrowUpRight size={18}/></a></div></div>
        </article>)}</div>
        {filtered.length===0 && <div className="empty-state">No encontramos destinos con esos filtros. Desactiva Solo favoritos, quita el límite de costo o revisa municipio, nombre y categoría.</div>}
      </section>

      <section className="map-section section-pad" id="mapa">
        <div className="map-copy"><span className="section-kicker">02 / EL HUILA EN EL MAPA</span><h2>Tan cerca.<br/><em>Mucho por descubrir.</em></h2><p>Ubica algunos de los destinos destacados y comienza a imaginar tu próxima ruta por el departamento.</p><div className="map-legend"><span><i className="legend-dot green-dot"></i>Naturaleza</span><span><i className="legend-dot orange-dot"></i>Cultura</span><span><i className="legend-dot blue-dot"></i>Aventura</span></div></div>
        <div className="map-visual">
          <div className="map-grid"></div><svg className="route-line" viewBox="0 0 600 430" preserveAspectRatio="none" aria-hidden="true"><path d="M 300 340 C 220 280 390 260 280 210 S 330 120 420 90" fill="none" stroke="#c1d4a4" strokeWidth="3" strokeDasharray="7 9"/></svg>
          <div className="map-river"></div><div className="map-label map-label-top">CORDILLERA CENTRAL</div><div className="map-label map-label-bottom">RÍO MAGDALENA</div>
          {[{x:48,y:70,n:"San Agustín",e:"🗿"},{x:64,y:30,n:"Salto de Bordones",e:"💧"},{x:37,y:50,n:"Neiva",e:"🌅"},{x:75,y:65,n:"Tatacoa",e:"🌵"},{x:29,y:77,n:"Rivera",e:"♨️"}].map((p,i)=><div key={p.n} className={`map-pin pin-${i}`} style={{left:`${p.x}%`,top:`${p.y}%`}} title={p.n}><span>{p.e}</span><b>{p.n}</b></div>)}
          <div className="map-compass">N<br/><span>↑</span></div><div className="map-note"><MapPin size={15}/> Mapa esquemático · Huila, Colombia</div>
        </div>
      </section>

      <section className="planner section-pad" id="aventura">
        <div className="planner-intro"><span className="section-kicker">03 / TU VIAJE, A TU MANERA</span><h2>Diseña una aventura<br/><em>hecha para ti.</em></h2><p>Cuéntanos qué te gusta. Nuestro recomendador organiza una idea de recorrido según tus intereses, días disponibles y presupuesto.</p><div className="planner-benefits"><span><Sparkles size={17}/> Recomendaciones personalizadas</span><span><Wallet size={17}/> Presupuesto orientativo</span><span><Compass size={17}/> Destinos del Huila</span></div></div>
        <form className="planner-form" onSubmit={makeTrip}>
          <div className="form-top"><span className="form-icon"><Sparkles size={19}/></span><div><h3>Tu próxima aventura</h3><p>Solo toma un minuto</p></div><span className="step">01 — 03</span></div>
          <label className="field-label" htmlFor="trip-days"><span><CalendarDays size={16}/> ¿Cuántos días tienes?</span><b>{days} {days===1?"día":"días"}</b></label>
          <input id="trip-days" className="range" type="range" min="1" max="7" value={days} aria-valuetext={`${days} ${days===1?"día":"días"}`} onChange={e=>setDays(Number(e.target.value))} />
          <div className="range-ends"><span>1 día</span><span>7 días</span></div>
          <label className="field-label budget-label" htmlFor="budget"><span><Wallet size={16}/> ¿Cuál es tu presupuesto?</span></label>
          <div className="money-input"><span>$</span><input id="budget" type="number" min="0" max={MAX_BUDGET} step="1" value={budget} onChange={e=>{setBudget(e.target.value); setTripError("");}} aria-invalid={Boolean(tripError)} aria-describedby={tripError ? "budget-error" : undefined} required/><small>COP</small></div>
          {tripError && <p id="budget-error" className="form-error" role="alert">{tripError}</p>}
          <div className="field-label"><span><Heart size={16}/> ¿Qué te gustaría vivir?</span></div>
          <label className="field-label" htmlFor="trip-municipality">Municipio de la propuesta</label>
          <select className="trip-municipality" id="trip-municipality" value={tripMunicipality} onChange={event=>setTripMunicipality(event.target.value)}><option value="">Todos los municipios</option>{municipalities.map(value=><option key={value} value={value}>{value}</option>)}</select>
          <div className="interest-grid">{[{id:"naturaleza",name:"Naturaleza",emoji:"🌿"},{id:"cultura",name:"Cultura",emoji:"🗿"},{id:"aventura",name:"Aventura",emoji:"🥾"},{id:"relajación",name:"Relajación",emoji:"♨️"},{id:"gastronomía",name:"Gastronomía",emoji:"🍲"},{id:"familia",name:"En familia",emoji:"👨‍👩‍👧"}].map(item=><button type="button" key={item.id} className={interests.includes(item.id)?"interest selected":"interest"} aria-pressed={interests.includes(item.id)} onClick={()=>toggleInterest(item.id)}><span>{item.emoji}</span>{item.name}</button>)}</div>
          <button className="button button-dark submit-button" disabled={loading} type="submit">{loading?"Creando tu ruta…":"Crear mi itinerario"} <ArrowRight size={18}/></button>
          <p className="form-disclaimer">Los valores son estimaciones académicas, no cotizaciones de proveedores.</p>
        </form>
      </section>

      <div className="export-controls section-pad"><button type="button" className="export-button" disabled={!result || loading} onClick={exportTrip}>Descargar itinerario JSON</button><p>Exporta la última propuesta mostrada. Los valores son orientativos.</p>{exportError && <p role="alert">{exportError}</p>}</div>
      {result && <section className="results section-pad" id="resultado"><div className="section-heading"><div><span className="section-kicker">TU PROPUESTA PERSONALIZADA</span><h2>Tu ruta empieza aquí<span className="dot">.</span></h2><p>{result.summary}</p></div><div className="result-total"><small>COSTO ESTIMADO</small><b>{COP.format(result.estimated_total)}</b><span>Saldo estimado: {COP.format(result.remaining_budget)}</span></div></div>{result.itinerary?.length===0 && <p className="result-empty" role="status">No hay destinos disponibles para esta selección. Prueba Todos los municipios u otro municipio.</p>}<div className="result-list">{(result.itinerary||[]).map((d,i)=><article className="result-item" key={d.id}><span className="result-day">DÍA {i+1}</span><div className="result-emoji">{d.emoji}</div><div className="result-details"><h3>{d.name}</h3><p><MapPin size={14}/> {d.municipality} · {d.category}</p><span>{d.description}</span></div><b>{COP.format(d.price)}</b></article>)}</div><p className="result-notice">{result.method} {result.notice}</p></section>}

      <section className="closing section-pad"><div className="closing-art"><div className="closing-sun"></div><Mountain className="closing-mountain one"/><Mountain className="closing-mountain two"/><Waves className="closing-waves"/></div><div className="closing-copy"><span className="section-kicker">EL ORGULLO DE NUESTRA TIERRA</span><h2>El Huila no se cuenta.<br/><em>Se vive.</em></h2><a className="button button-light" href="#aventura">Planea tu aventura <ArrowRight size={17}/></a></div></section>
    </main>

    <footer className="footer"><a className="brand footer-brand" href="#inicio"><span className="brand-mark"><Compass size={21}/></span><span>OPITA <b>360</b><small>EL HUILA POR DESCUBRIR</small></span></a><p>Proyecto integrador · Ingeniería de Software · FET</p><p>Neiva, Huila, Colombia · 2026</p><span className="footer-line"></span><small>Proyecto académico. Información turística y costos sujetos a verificación.</small></footer>
  </div>;
}

createRoot(document.getElementById("root")).render(<App />);
