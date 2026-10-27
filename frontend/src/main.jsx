import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { ArrowDownRight, ArrowRight, Compass, MapPin, Sparkles, CalendarDays, Wallet, Heart, Menu, X, Mountain, Waves, Landmark, Search, ExternalLink } from "lucide-react";
import "./styles.css";

const API = "http://127.0.0.1:8000";
const COP = new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });
const fallbackDestinations = [
  {id:1,name:"Desierto de la Tatacoa",municipality:"Villavieja",category:"Naturaleza",price:85000,days:1,description:"Paisajes rojizos, senderos y observación del cielo nocturno.",emoji:"🌵",tags:["naturaleza","aventura","fotografía","astronomía"],color:"sand"},
  {id:2,name:"Parque Arqueológico de San Agustín",municipality:"San Agustín",category:"Cultura",price:120000,days:1,description:"Estatuas ancestrales, historia y patrimonio arqueológico.",emoji:"🗿",tags:["cultura","historia","familia","arqueología"],color:"green"},
  {id:3,name:"Malecón del río Magdalena",municipality:"Neiva",category:"Cultura",price:35000,days:1,description:"Un recorrido urbano para disfrutar el río y la identidad opita.",emoji:"🌅",tags:["cultura","gastronomía","familia","relajación"],color:"blue"},
  {id:4,name:"Salto de Bordones",municipality:"Isnos",category:"Naturaleza",price:95000,days:1,description:"Una imponente caída de agua rodeada de montañas y vegetación.",emoji:"💧",tags:["naturaleza","aventura","fotografía","senderismo"],color:"blue"},
  {id:5,name:"Estrecho del río Magdalena",municipality:"San Agustín",category:"Aventura",price:70000,days:1,description:"Un tramo singular del río entre grandes formaciones rocosas.",emoji:"🏞️",tags:["aventura","naturaleza","fotografía","senderismo"],color:"green"},
  {id:6,name:"Termales de Rivera",municipality:"Rivera",category:"Bienestar",price:65000,days:1,description:"Aguas termales y descanso en un entorno natural.",emoji:"♨️",tags:["relajación","naturaleza","familia","bienestar"],color:"sand"},
  {id:7,name:"Represa de Betania",municipality:"Yaguará",category:"Aventura",price:90000,days:1,description:"Paisajes acuáticos y actividades recreativas según disponibilidad local.",emoji:"🛶",tags:["aventura","naturaleza","familia","fotografía"],color:"blue"},
  {id:8,name:"Centro de Neiva y tradición opita",municipality:"Neiva",category:"Cultura",price:45000,days:1,description:"Sabores regionales, espacios culturales y tradición del Huila.",emoji:"🎭",tags:["cultura","gastronomía","historia","familia"],color:"sand"}
];
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
  const [search, setSearch] = useState("");
  const [days, setDays] = useState(2);
  const [budget, setBudget] = useState("200000");
  const [interests, setInterests] = useState(["naturaleza"]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/destinations`)
      .then(r => { if (!r.ok) throw new Error("API"); return r.json(); })
      .then(data => { setDestinations(data.destinations || fallbackDestinations); setApiStatus("conectada"); })
      .catch(() => setApiStatus("demostración"));
  }, []);

  const filtered = useMemo(() => destinations.filter(d => {
    const matchCategory = category === "Todos" || d.category === category;
    const q = search.trim().toLowerCase();
    return matchCategory && (!q || `${d.name} ${d.municipality} ${d.category}`.toLowerCase().includes(q));
  }), [destinations, category, search]);

  const toggleInterest = (interest) => setInterests(prev => prev.includes(interest) ? prev.filter(x => x !== interest) : [...prev, interest]);

  async function makeTrip(e) {
    e.preventDefault();
    setLoading(true);
    const payload = { days: Number(days), budget: Math.max(0, Number(budget) || 0), interests: interests.length ? interests : ["naturaleza"] };
    try {
      const response = await fetch(`${API}/api/recommendations`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
      if (!response.ok) throw new Error("API");
      setResult(await response.json());
    } catch {
      const chosen = destinations.filter(d => d.tags.some(t => payload.interests.includes(t)) || payload.interests.includes(d.category.toLowerCase())).sort((a,b)=>a.price-b.price).slice(0, Number(days));
      const itinerary = chosen.length ? chosen : destinations.slice(0, Number(days));
      const total = itinerary.reduce((sum,d)=>sum+d.price,0);
      setResult({summary:`Propuesta de ${itinerary.length} parada(s) para ${days} día(s).`,method:"Recomendación local de demostración.",itinerary,estimated_total:total,budget:payload.budget,remaining_budget:Math.max(payload.budget-total,0),notice:"Valores orientativos; confirma precios y disponibilidad antes de viajar."});
    }
    setLoading(false);
    setTimeout(() => document.getElementById("resultado")?.scrollIntoView({behavior:"smooth",block:"start"}), 80);
  }

  return <div className="app-shell">
    <div className="announcement"><span className="pulse"></span> Hecho en el Huila, pensado para quienes quieren descubrirlo <span className={`api-pill ${apiStatus}`}>{apiStatus === "conectada" ? "API conectada" : apiStatus === "probando" ? "Conectando API…" : "Modo demostración"}</span></div>
    <header className="nav-wrap">
      <a className="brand" href="#inicio" aria-label="OPITA 360 inicio"><span className="brand-mark"><Compass size={23}/></span><span>OPITA <b>360</b><small>EL HUILA POR DESCUBRIR</small></span></a>
      <button className="mobile-toggle" onClick={()=>setMobileMenu(!mobileMenu)} aria-label="Abrir menú">{mobileMenu?<X/>:<Menu/>}</button>
      <nav className={mobileMenu ? "nav-links open" : "nav-links"}>
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
        <div className="filter-row"><div className="searchbox"><Search size={17}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Busca un destino o municipio…"/></div><div className="filters">{["Todos","Naturaleza","Cultura","Aventura","Bienestar"].map(c=><button key={c} className={category===c?"filter active":"filter"} onClick={()=>setCategory(c)}>{c}</button>)}</div></div>
        <div className="destination-grid">{filtered.map((d,i)=><article className={`destination-card card-${d.color || "green"}`} key={d.id}>
          <div className="destination-image" style={{backgroundImage:`linear-gradient(180deg,transparent 40%,rgba(9,28,24,.72)),url("${photos[d.name] || photos["Desierto de la Tatacoa"]}")`}}>
            <span className="category-tag">{d.category}</span><button className="heart" title="Guardar destino" onClick={e=>e.currentTarget.classList.toggle("saved")}><Heart size={17}/></button>
            <span className="destination-number">0{(i+1).toString().slice(-1)}</span>
            <div className="destination-title"><span>{d.municipality} · HUILA</span><h3>{d.name}</h3></div>
          </div>
          <div className="destination-info"><p>{d.description}</p><div className="destination-meta"><span><Wallet size={15}/> Desde {COP.format(d.price)}</span><a href="#aventura" aria-label={`Planear visita a ${d.name}`}><ArrowUpRightIcon/></a></div></div>
        </article>)}</div>
        {filtered.length===0 && <div className="empty-state">No encontramos destinos con esa búsqueda. Prueba con otro nombre o categoría.</div>}
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
          <label className="field-label"><span><CalendarDays size={16}/> ¿Cuántos días tienes?</span><b>{days} {days===1?"día":"días"}</b></label>
          <input className="range" type="range" min="1" max="7" value={days} onChange={e=>setDays(e.target.value)} />
          <div className="range-ends"><span>1 día</span><span>7 días</span></div>
          <label className="field-label budget-label" htmlFor="budget"><span><Wallet size={16}/> ¿Cuál es tu presupuesto?</span></label>
          <div className="money-input"><span>$</span><input id="budget" type="number" min="0" step="10000" value={budget} onChange={e=>setBudget(e.target.value)} required/><small>COP</small></div>
          <div className="field-label"><span><Heart size={16}/> ¿Qué te gustaría vivir?</span></div>
          <div className="interest-grid">{[{id:"naturaleza",name:"Naturaleza",emoji:"🌿"},{id:"cultura",name:"Cultura",emoji:"🗿"},{id:"aventura",name:"Aventura",emoji:"🥾"},{id:"relajación",name:"Relajación",emoji:"♨️"},{id:"gastronomía",name:"Gastronomía",emoji:"🍲"},{id:"familia",name:"En familia",emoji:"👨‍👩‍👧"}].map(item=><button type="button" key={item.id} className={interests.includes(item.id)?"interest selected":"interest"} onClick={()=>toggleInterest(item.id)}><span>{item.emoji}</span>{item.name}</button>)}</div>
          <button className="button button-dark submit-button" disabled={loading} type="submit">{loading?"Creando tu ruta…":"Crear mi itinerario"} <ArrowRight size={18}/></button>
          <p className="form-disclaimer">Los valores son estimaciones académicas, no cotizaciones de proveedores.</p>
        </form>
      </section>

      {result && <section className="results section-pad" id="resultado"><div className="section-heading"><div><span className="section-kicker">TU PROPUESTA PERSONALIZADA</span><h2>Tu ruta empieza aquí<span className="dot">.</span></h2><p>{result.summary}</p></div><div className="result-total"><small>COSTO ESTIMADO</small><b>{COP.format(result.estimated_total)}</b><span>Saldo estimado: {COP.format(result.remaining_budget)}</span></div></div><div className="result-list">{(result.itinerary||[]).map((d,i)=><article className="result-item" key={d.id}><span className="result-day">DÍA {i+1}</span><div className="result-emoji">{d.emoji}</div><div className="result-details"><h3>{d.name}</h3><p><MapPin size={14}/> {d.municipality} · {d.category}</p><span>{d.description}</span></div><b>{COP.format(d.price)}</b></article>)}</div><p className="result-notice">{result.method} {result.notice}</p></section>}

      <section className="closing section-pad"><div className="closing-art"><div className="closing-sun"></div><Mountain className="closing-mountain one"/><Mountain className="closing-mountain two"/><Waves className="closing-waves"/></div><div className="closing-copy"><span className="section-kicker">EL ORGULLO DE NUESTRA TIERRA</span><h2>El Huila no se cuenta.<br/><em>Se vive.</em></h2><a className="button button-light" href="#aventura">Planea tu aventura <ArrowRight size={17}/></a></div></section>
    </main>

    <footer className="footer"><a className="brand footer-brand" href="#inicio"><span className="brand-mark"><Compass size={21}/></span><span>OPITA <b>360</b><small>EL HUILA POR DESCUBRIR</small></span></a><p>Proyecto integrador · Ingeniería de Software · FET</p><p>Neiva, Huila, Colombia · 2026</p><span className="footer-line"></span><small>Proyecto académico. Información turística y costos sujetos a verificación.</small></footer>
  </div>;
}
function ArrowUpRightIcon(){ return <ArrowRight size={18}/>; }

createRoot(document.getElementById("root")).render(<App />);
