import React, { useEffect, useRef, useState } from "react";

const COP = new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });

/** One mounted instance per selection. Cleanup invalidates every pending response. */
export default function DestinationDetail({ destination, demo, api, trigger, onClose }) {
  const dialogRef = useRef(null);
  const closeRef = useRef(null);
  const [state, setState] = useState({ loading: !demo, data: demo ? destination : null,
    notice: demo ? "Modo demostración" : "", missing: false });

  useEffect(() => {
    const dialog = dialogRef.current;
    dialog.showModal();
    closeRef.current.focus();
    return () => {
      dialog.close();
      if (trigger?.isConnected) trigger.focus();
    };
  }, [trigger]);

  useEffect(() => {
    if (demo) return;
    const controller = new AbortController();
    let active = true;
    const timeout = setTimeout(() => controller.abort(), 5000);
    async function load() {
      try {
        const response = await fetch(`${api}/api/destinations/${destination.id}`, { signal: controller.signal });
        if (!active) return;
        if (response.status === 404) {
          setState({ loading: false, data: null, notice: "Destino no encontrado", missing: true });
          return;
        }
        if (!response.ok) throw new Error("Detalle no disponible");
        const { destination: detail } = await response.json();
        if (detail?.id !== destination.id || !detail.name || !Array.isArray(detail.tags)) throw new Error("Respuesta inválida");
        if (active) setState({ loading: false, data: detail, notice: "", missing: false });
      } catch {
        if (active) setState({ loading: false, data: destination,
          notice: "Datos del catálogo; detalle no disponible", missing: false });
      } finally {
        clearTimeout(timeout);
      }
    }
    load();
    return () => { active = false; clearTimeout(timeout); controller.abort(); };
  }, [api, destination, demo]);

  function handleKeyDown(event) {
    // The dialog currently has one interactive control: keep keyboard focus there.
    if (event.key === "Tab") { event.preventDefault(); closeRef.current.focus(); }
  }

  const data = state.data;
  return <dialog ref={dialogRef} className="destination-detail" aria-labelledby="destination-detail-title"
    onCancel={event => { event.preventDefault(); onClose(); }} onKeyDown={handleKeyDown}>
    <header className="detail-header"><h2 id="destination-detail-title">{state.missing ? "Destino no encontrado" : (data?.name || destination.name)}</h2>
      <button type="button" ref={closeRef} className="detail-close" onClick={onClose}>Cerrar</button></header>
    <p role="status" aria-live="polite">{state.loading ? "Cargando detalle…" : state.notice}</p>
    {data && <div className="detail-content">
      <p>{data.description}</p>
      <dl><dt>Municipio</dt><dd>{data.municipality}</dd><dt>Categoría</dt><dd>{data.category}</dd>
        <dt>Precio orientativo</dt><dd>{COP.format(data.price)}</dd><dt>Duración</dt><dd>{data.days} día(s)</dd></dl>
      <h3>Etiquetas</h3><ul>{data.tags.map(tag => <li key={tag}>{tag}</li>)}</ul>
      <p>Valores orientativos; confirma precios y disponibilidad antes de viajar.</p>
    </div>}
  </dialog>;
}
