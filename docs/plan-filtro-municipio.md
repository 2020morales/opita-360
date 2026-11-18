Read skill `frontend-react`
Completed with input: {"skill":"frontend-react"}

Voy a revisar la documentación del proyecto, las instrucciones del frontend y todas las skills de `.github/skills`; después te presentaré el plan sin tocar archivos.

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\README.md"
}

Find files matching `**/AGENTS.md`

Find files matching `**/*`

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\AGENTS.md"
}

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\frontend\\AGENTS.md"
}

Read `SKILL.md`
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\.github\\skills\\frontend-react\\SKILL.md"
}

Read `SKILL.md`
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\.github\\skills\\backend-fastapi\\SKILL.md"
}

Las instrucciones confirman que el filtro debe ser solo del frontend, preservar la API y el modo demo, y combinarse con los filtros existentes. Ahora revisaré el estado actual y los scripts para que el plan cite puntos de integración concretos.

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\frontend\\src\\main.jsx"
}

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\frontend\\src\\styles.css"
}

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\frontend\\package.json"
}

Read 
Completed with input: {
  "path": "C:\\Users\\Bairon Morales\\Downloads\\opita-360-original\\backend\\AGENTS.md"
}

Find files matching `frontend/**/*.{test,spec}.{js,jsx,ts,tsx}`

Find files matching `frontend/src/**/*`

## Plan propuesto: filtro de destinos por municipio

Revisé el `README.md`, los tres archivos `AGENTS.md` del proyecto y las dos skills: `frontend-react` y `backend-fastapi`. El catálogo y los filtros actuales están en `main.jsx`; sus estilos están en `styles.css`. No encontré archivos de pruebas ni un script de test configurado en el frontend.

### Archivos previstos

- `frontend/src/main.jsx`: estado de selección, opciones de municipios derivadas del catálogo y combinación del nuevo filtro con búsqueda y categoría.
- `frontend/src/styles.css`: presentación del selector y adaptación al diseño responsive existente.

No se prevén cambios en API, dependencias ni contratos del backend: cada destino ya incluye el campo `municipality`.

### Pasos de implementación

1. Derivar la lista de municipios del catálogo activo (`destinations`), eliminando duplicados y ordenándolos; incluir «Todos los municipios» como opción inicial.
2. Añadir estado para el municipio seleccionado, iniciado en «Todos los municipios».
3. Incorporar un selector accesible junto a la búsqueda y los botones de categoría.
4. Actualizar el filtrado derivado para que categoría, municipio y búsqueda deban coincidir simultáneamente.
5. Si el catálogo cambia —por ejemplo, al llegar la respuesta de la API— y ya no contiene el municipio seleccionado, volver automáticamente a «Todos los municipios».
6. Mantener el comportamiento de modo demostración y el mensaje de lista vacía, ajustando su texto si hace falta para que contemple cualquier combinación de filtros.
7. Aplicar estilos coherentes con los controles existentes y comprobar su disposición en pantallas estrechas.

### Criterios de aceptación

- El selector muestra «Todos los municipios» y los municipios disponibles sin duplicados.
- Elegir un municipio muestra solo destinos de ese municipio; volver a «Todos» restaura los destinos permitidos por los demás filtros.
- Municipio, categoría y búsqueda se combinan sin que un filtro elimine el efecto de los otros.
- Una combinación sin resultados muestra un mensaje claro; limpiar o cambiar filtros vuelve a mostrar coincidencias.
- Si la respuesta de la API cambia el catálogo y el municipio elegido deja de existir, la selección se reinicia correctamente.
- El filtro funciona tanto con los datos de demostración como con la API disponible, sin cambiar sus contratos.
- El selector es identificable para tecnologías de asistencia y utilizable con teclado, y se adapta a escritorio y móvil.

### Pruebas previstas

- Ejecutar `npm run build` desde `frontend`.
- Probar manualmente «Todos los municipios», cada municipio disponible, una búsqueda combinada con municipio y categoría, una combinación sin resultados y la recuperación al cambiar o limpiar filtros.
- Repetir las comprobaciones en modo demostración y con la API conectada; verificar también que un cambio de catálogo reinicie una selección inválida.
- Revisar visualmente el selector en escritorio y móvil.

No modifiqué archivos ni ejecuté pruebas: espero tu revisión del plan antes de implementar.