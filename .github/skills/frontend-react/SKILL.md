---
name: frontend-react
description: Implementar y revisar cambios de interfaz en React y Vite para OPITA 360, especialmente filtros de destinos y selección de municipios.
---

# Skill: cambios seguros en React

## Cuándo usar
Cuando una solicitud afecte `frontend/src/main.jsx`, `frontend/src/styles.css` o el comportamiento visual de filtros y formularios.

## Procedimiento
1. Leer `frontend/AGENTS.md` y los archivos afectados.
2. Identificar el estado existente y el flujo de datos entre API y modo demostración.
3. Proponer un plan breve con casos de prueba antes de editar.
4. Implementar cambios mínimos, sin mutar arrays de estado y sin romper filtros existentes.
5. Ejecutar `npm run build` desde `frontend` y probar manualmente búsqueda, categoría, municipio y combinaciones.
6. Registrar resultados reales, limitaciones y archivos modificados en el PR.

## Límites y permisos
Leer y editar solo archivos del frontend requeridos. No ejecutar comandos destructivos, no instalar paquetes nuevos sin aprobación y no fusionar PR. Solicitar aprobación humana para cambios de API o dependencias.
