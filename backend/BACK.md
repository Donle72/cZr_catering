# Product Backlog - cZr Catering

**Última actualización**: 2025-12-18 03:20

---

## ✅ COMPLETADOS

### BACK-1: Selectores de unidades

- **Prioridad**: P0
- **Esfuerzo**: 3 pts
- **Estado**: ✅ COMPLETADO 100%
- **Descripción**: Agregar selectores de unidades en formulario de ingredientes
- **Completado**:
  - ✅ Endpoint GET /units
  - ✅ Dropdowns en formulario
  - ✅ Validaciones backend

### BACK-4: Edición de ingredientes en recetas

- **Prioridad**: P1
- **Esfuerzo**: 2 pts
- **Estado**: ✅ COMPLETADO 100%
- **Descripción**: Editar ingredientes en recetas (cantidad, notas)
- **Completado**:
  - ✅ PUT /recipes/{id}/items/{item_id}
  - ✅ Schema RecipeItemUpdate
  - ✅ Botón Edit + Modal
  - ✅ Integración completa

### BACK-2: Sistema de tags

- **Prioridad**: P0
- **Esfuerzo**: 5 pts
- **Estado**: ✅ COMPLETADO 100%
- **Fecha**: 2025-12-18
- **Descripción**: Exponer sistema de tags en frontend para recetas
- **Completado**:
  - ✅ POST /recipes/{id}/tags/{tag_id}
  - ✅ DELETE /recipes/{id}/tags/{tag_id}
  - ✅ RecipeResponse incluye tags
  - ✅ Tags visibles en lista
  - ✅ Selector multi-select en modal
  - ✅ Asignar tags al crear/editar

### BACK-9: Registro de etiquetas en recetas

- **Prioridad**: P0
- **Esfuerzo**: 2 pts
- **Estado**: ✅ COMPLETADO 100%
- **Fecha**: 2025-12-18
- **Tipo**: Error (DEF-001) - RESUELTO
- **Descripción**: Implementado selector de tags en modal de recetas
- **Completado**:
  - ✅ Fetch tags disponibles
  - ✅ UI multi-select interactiva
  - ✅ Asignación al crear receta
  - ✅ Modificación al editar receta

### BACK-10: Modificar campos de receta

- **Prioridad**: P1
- **Esfuerzo**: 2 pts
- **Estado**: ✅ COMPLETADO 100%
- **Fecha**: 2025-12-18
- **Descripción**: Campos de receta (yield_quantity, servings, etc) son editables
- **Completado**:
  - ✅ Backend PUT endpoint soporta todos los campos
  - ✅ Frontend modal permite editar todos los campos
  - ✅ Validaciones funcionando

### BACK-12: Ingredientes no se pueden borrar

- **Prioridad**: P0
- **Esfuerzo**: 3 pts
- **Estado**: ✅ COMPLETADO 100%
- **Fecha**: 2025-12-18
- **Tipo**: Error (DEF-002) - RESUELTO
- **Descripción**: Validación de uso antes de eliminar ingredientes
- **Completado**:
  - ✅ Backend valida si ingrediente está en uso
  - ✅ Retorna error 409 con lista de recetas
  - ✅ Frontend muestra mensaje detallado
  - ✅ Sugerencias de acción alternativa

---

## 🟡 EN PROGRESO

(Ningún item en progreso actualmente)

---

## 🔴 DEFECTOS CRÍTICOS (P0)

### BACK-14: Ingredientes no se borran al confirmar (DEFECTO)

- **Prioridad**: P0
- **Esfuerzo**: 2 pts
- **Tipo**: Error (DEF-003)
- **Criticidad**: ALTA - Funcionalidad básica rota
- **Descripción**: Al presionar Delete y confirmar, el ingrediente no se borra
- **Módulo**: Ingredientes
- **Análisis Técnico**:
  - Probable causa: Error en implementación de BACK-12
  - La validación agregada puede estar bloqueando todos los DELETE
  - Necesita revisar lógica de validación y manejo de respuesta
- **Impacto**: CRÍTICO - Bloquea limpieza de datos
- **Esfuerzo estimado**: ~2 horas

### BACK-15: No se pueden modificar etiquetas de recetas (DEFECTO)

- **Prioridad**: P0
- **Esfuerzo**: 3 pts
- **Tipo**: Error (DEF-004)
- **Criticidad**: ALTA - Funcionalidad recién implementada no funciona completamente
- **Descripción**: Se pueden seleccionar etiquetas al crear receta, pero luego no se pueden modificar
- **Módulo**: Recetas
- **Análisis Técnico**:
  - Funciona al CREAR, NO funciona al EDITAR
  - Posibles causas: Tags no se cargan al abrir modal de edición, lógica de diff tiene bug
- **Impacto**: ALTO - Usuarios no pueden gestionar tags después de crear receta
- **Esfuerzo estimado**: ~3 horas

---

## 🟡 PRIORIDAD ALTA (P1)

### BACK-16: Mejorar UX selector de etiquetas con muchas tags

- **Prioridad**: P1
- **Esfuerzo**: 5 pts
- **Tipo**: Mejora UX
- **Criticidad**: MEDIA - Mejora de usabilidad
- **Descripción**: Evaluar si es cómodo que aparezcan todas las etiquetas cuando hay muchas
- **Módulo**: Recetas
- **Análisis Técnico**:
  - Problema: Con 20+ tags se vuelve difícil de usar
  - Soluciones: 1) Búsqueda/filtro (3 pts), 2) Dropdown multi-select (4 pts), 3) Categorías (8 pts)
  - Recomendación: Empezar con búsqueda/filtro
- **Impacto**: MEDIO - Mejora experiencia con muchas tags
- **Esfuerzo estimado**: ~5 horas

---

## 🟡 PRIORIDAD ALTA (P1)

### BACK-3: Mejorar UX alta de recetas

- **Prioridad**: P1
- **Esfuerzo**: 3 pts
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Mostrar ingredientes directamente en modal de alta
- **Tareas**:
  - Refactorizar modal
  - Unificar flujo alta/edición
  - Indicadores visuales

### BACK-10: Modificar campos de receta (rendimiento, etc)

- **Prioridad**: P1
- **Esfuerzo**: 2 pts
- **Tipo**: Mejora
- **Estado**: ⏳ PENDIENTE
- **Criticidad**: MEDIA - Funcionalidad básica esperada
- **Análisis**: Agregar campos editables en formulario de receta (yield, servings, etc)
- **Impacto**: Mejora gestión de recetas

---

## 🟠 PRIORIDAD MEDIA (P2)

### BACK-5: Categorías de ingredientes

- **Prioridad**: P2
- **Esfuerzo**: 2 pts
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Crear tabla ingredient_categories y CRUD

### BACK-6: Edición de rendimiento

- **Prioridad**: P2
- **Esfuerzo**: 1 pt
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Verificar/corregir campo rendimiento editable
- **Nota**: Quick win

### BACK-7: CRUD genérico configuración

- **Prioridad**: P2
- **Esfuerzo**: 8 pts
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Interfaz tipo hoja de cálculo para tablas de configuración

### BACK-11: Reemplazar modales por formularios inline

- **Prioridad**: P2
- **Esfuerzo**: 8 pts
- **Tipo**: Mejora UX
- **Estado**: ⏳ PENDIENTE
- **Criticidad**: MEDIA - Mejora experiencia pero no bloquea funcionalidad
- **Análisis**: Refactorización importante de UI. Afecta múltiples módulos (Recetas, Ingredientes, Eventos, etc). Requiere rediseño de flujos
- **Impacto**: Mejora significativa de productividad del usuario
- **Alcance**: Recetas, Ingredientes, Proveedores, Eventos, Assets

### BACK-13: Mensajes de error multilingües

- **Prioridad**: P2
- **Esfuerzo**: 3 pts
- **Tipo**: Mejora
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Migrar todos los mensajes de error hardcodeados a la tabla de traducciones (i18n)
- **Alcance**: Backend y Frontend
- **Análisis**: El sistema ya tiene infraestructura i18n completa. Necesita:
  - Identificar todos los mensajes hardcodeados
  - Agregar traducciones a tabla `translations`
  - Actualizar código para usar servicio de traducciones
- **Impacto**: Soporte completo multilingüe para errores y mensajes del sistema

### BACK-17: Tag selector se cierra al agregar

- **Prioridad**: P2
- **Esfuerzo**: 1 pt
- **Tipo**: Mejora UX (UX-001)
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Al agregar un tag en RecipeDetail, el selector se cierra automáticamente
- **Solución**: Mantener selector abierto hasta que usuario lo cierre manualmente
- **Módulo**: Recetas/RecipeDetail
- **Impacto**: Mejora productividad al agregar múltiples tags

### BACK-18: Estandarizar posición de botones

- **Prioridad**: P2
- **Esfuerzo**: 5 pts
- **Tipo**: Mejora UX (UX-002)
- **Estado**: A DEFINIR
- **Descripción**: Botones de navegación (ej: flecha atrás) aparecen en diferentes lugares según formulario
- **Solución**: Definir estándar de UI para posición de botones de navegación y acciones
- **Módulo**: Global/UX
- **Impacto**: Consistencia y mejor UX
- **Nota**: Requiere definición de estándares de UI

---

## 🔵 PRIORIDAD BAJA (P3)

### BACK-8: Normalizar documentación

- **Prioridad**: P3
- **Esfuerzo**: 3 pts
- **Estado**: ⏳ PENDIENTE
- **Descripción**: Consolidar archivos de información del proyecto

---

## 📊 ESTADÍSTICAS GENERALES

### Por Estado

- ✅ Completados: 2 items (16.7%)
- 🟡 En progreso: 1 item (8.3%)
- ⏳ Pendientes: 9 items (75%)
- **Total**: 12 items

### Por Prioridad

- 🔴 P0: 2 defectos + 1 en progreso = 3 items
- 🟡 P1: 2 items (1 completado, 1 pendiente)
- 🟠 P2: 4 items
- 🔵 P3: 1 item

### Por Puntos

- Completados: 5 pts (11.9%)
- En progreso: 3.5 pts (8.3%)
- Pendientes: 33.5 pts (79.8%)
- **Total**: 42 pts

### Por Tipo

- Defectos: 2 items (BACK-9, BACK-12)
- Mejoras funcionales: 7 items
- Mejoras UX: 2 items
- Documentación: 1 item

---

## 🎯 RECOMENDACIONES

**Quick Wins** (bajo esfuerzo, alto impacto):

1. BACK-6: Edición de rendimiento (1 pt)
2. BACK-10: Modificar campos de receta (2 pts)

**Defectos Críticos** (resolver primero):

1. BACK-9: Registro de etiquetas (2 pts)
2. BACK-12: Borrar ingredientes (3 pts)

**En Progreso** (completar):

1. BACK-2: Sistema de tags (1.5 pts restantes)
