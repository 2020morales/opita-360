# 002: Filtro por costo maximo

Estado: borrador. Implementacion: no iniciada. PR: pendiente. Alcance propuesto para OPITA 360, sin modificar los contratos existentes fuera de lo descrito.

## Criterios de aceptacion

- **AC-01** Dado destino de 35000 COP y limite 35000; cuando aplicar costo maximo; entonces el destino se incluye por limite inclusivo. Capa: unit.
- **AC-02** Dado filtros activos y costo vacio; cuando filtrar catalogo; entonces costo no limita; municipio, categoria y busqueda siguen activos. Capa: unit.
- **AC-03** Dado catalogo actual con precios positivos; cuando aplicar limite cero; entonces lista vacia y mensaje de recuperacion. Capa: browser.
- **AC-04** Dado entrada negativa o no numerica; cuando intentar aplicar el limite; entonces mensaje de validacion; no se aplica un filtro invalido. Capa: browser.

## Limites

Sin persistencia PostgreSQL, despliegue, autenticacion ni servicios de pago. Esta preparacion no demuestra implementacion o pruebas de la funcionalidad. Datos de demostracion deben identificarse. Cambios de alcance requieren aprobacion humana.
