# Instrucciones para el frontend de OPITA 360

Stack: React, Vite y lucide-react. Punto de entrada: `src/main.jsx`; estilos: `src/styles.css`.

- Mantener componentes accesibles: etiquetas, estados de carga, navegación por teclado y mensajes claros.
- Usar estado derivado para filtros y evitar mutar directamente los arreglos de React.
- Mantener la experiencia de demostración cuando la API no esté disponible.
- No cambiar la URL de la API ni los contratos sin coordinar con backend.
- Para filtros por municipio: incluir opción «Todos los municipios», combinar con búsqueda/categoría y reiniciar correctamente la selección si cambia el catálogo.
- Validar con `npm run build` y probar manualmente filtros vacíos, combinados y el modo demostración.
- Consultar `.github/skills/frontend-react/SKILL.md` cuando se trabaje en interfaz.
