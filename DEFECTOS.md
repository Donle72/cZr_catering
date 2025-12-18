# Registro de Defectos - cZr Catering

Fecha de creación: 2025-12-18

## Defectos Reportados

### DEF-001: No se pueden registrar etiquetas en las recetas

- **Tipo**: Error (E)
- **Fecha**: 2025-12-18 03:01
- **Descripción**: El sistema no permite registrar/asignar etiquetas (tags) a las recetas
- **Estado**: A ANALIZAR
- **Va al Backlog**: ✅ SÍ (Defecto real)
- **Módulo**: Recetas
- **Criticidad**: Pendiente análisis

### DEF-002: Ingredientes no utilizados no se pueden borrar

- **Tipo**: Error (E)
- **Fecha**: 2025-12-18 03:14
- **Descripción**: Ingredientes que no se utilizan en ninguna receta no se pueden eliminar (Ejemplo: "Tostada Para Bruscheta")
- **Estado**: A ANALIZAR
- **Va al Backlog**: ✅ SÍ (Defecto real)
- **Módulo**: Ingredientes
- **Criticidad**: Pendiente análisis

### DEF-003: Ingredientes no se borran al confirmar

- **Tipo**: Error (E)
- **Fecha**: 2025-12-18 03:45
- **Descripción**: Al presionar Delete en un ingrediente y confirmar, el ingrediente no se borra
- **Estado**: A ANALIZAR
- **Va al Backlog**: ✅ SÍ (Defecto real)
- **Módulo**: Ingredientes
- **Criticidad**: Pendiente análisis
- **Nota**: Puede estar relacionado con BACK-12 (validación agregada)

### DEF-004: No se pueden modificar etiquetas de recetas

- **Tipo**: Error (E)
- **Fecha**: 2025-12-18 03:45
- **Descripción**: Se pueden seleccionar etiquetas al crear receta, pero luego no se pueden modificar (agregar, sacar, etc.)
- **Estado**: A ANALIZAR
- **Va al Backlog**: ✅ SÍ (Defecto real)
- **Módulo**: Recetas
- **Criticidad**: Pendiente análisis
- **Nota**: Relacionado con BACK-2/BACK-9 recién implementado

### DEF-005: Ingredientes - Solución incorrecta borra historial

- **Tipo**: Error (E)
- **Fecha**: 2025-12-18 04:27
- **Descripción**: La solución implementada borra price_history, lo cual es INCORRECTO
- **Estado**: ❌ SOLUCIÓN INCORRECTA
- **Problema**:
  - Propuestas viejas quedan sin datos de precios históricos
  - Se pierde información valiosa para estadísticas
  - Historial necesario para análisis de costos
- **Solución correcta**: Implementar baja lógica (soft delete)
- **Módulo**: Ingredientes
- **Criticidad**: ALTA

### DEF-006: Falta implementar baja lógica en ingredientes

- **Tipo**: Error (E) - Arquitectura
- **Fecha**: 2025-12-18 05:15
- **Descripción**: Sistema no tiene soft delete, borra físicamente registros y su historial
- **Estado**: A ANALIZAR
- **Va al Backlog**: ✅ SÍ (Defecto de arquitectura)
- **Requerimiento**:
  - Agregar campo `is_active` o `deleted_at` a modelo Ingredient
  - Modificar DELETE para marcar como inactivo en lugar de borrar
  - Filtrar ingredientes inactivos en queries
  - Mantener historial de precios intacto
- **Módulo**: Ingredientes
- **Criticidad**: ALTA - Afecta integridad de datos históricos

### Mejora UX-001: Tag selector se cierra al agregar

- **Tipo**: Mejora (M)
- **Fecha**: 2025-12-18 04:27
- **Descripción**: Al agregar un tag, el selector se cierra. Hay que presionar "Agregar Tag" cada vez
- **Sugerencia**: Mantener selector abierto hasta que usuario lo cierre manualmente
- **Va al Backlog**: ✅ SÍ
- **Módulo**: Recetas

### Mejora UX-002: Botones en posiciones inconsistentes

- **Tipo**: Mejora (M)
- **Fecha**: 2025-12-18 04:27
- **Descripción**: Los botones (ej: flecha atrás) aparecen en diferentes lugares según el formulario
- **Sugerencia**: Estandarizar posición de botones de navegación y acciones
- **Va al Backlog**: ✅ SÍ (TEMA A DEFINIR)
- **Módulo**: Global/UX

---

## Historial

- 2025-12-18: Creación del archivo de defectos
- 2025-12-18: Registrado DEF-001 → RESUELTO
- 2025-12-18: Registrado DEF-002 → RESUELTO
- 2025-12-18: Registrado DEF-003 → RESUELTO
- 2025-12-18: Registrado DEF-004 → RESUELTO
- 2025-12-18: Registrado DEF-005 → RESUELTO
- 2025-12-18: Registrado UX-001, UX-002
