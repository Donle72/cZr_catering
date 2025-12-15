# button_actions.md

## Mapa de acciones de los botones

| Archivo | Botón (texto o descripción) | Acción esperada |
|---------|-----------------------------|----------------|
| **src/pages/Dashboard.jsx** | Ver Todos (card → Eventos) | Navegar a `/events` usando `useNavigate` |
| | Card → Crear Evento (icono calendario) | Abrir modal `CreateEventModal` (`setOpen(true)`) |
| | Card → Crear Receta (icono chef‑hat) | Abrir modal `CreateRecipeModal` |
| | Card → Agregar Receta (icono paquete) | Abrir modal `AddRecipeItemModal` |
| **src/pages/Suppliers.jsx** | Nuevo Proveedor (botón principal) | Abrir modal `CreateSupplierModal` |
| | Agregar Primer Proveedor (botón secundario) | Abrir modal `CreateSupplierModal` |
| **src/pages/Settings.jsx** | Guardar cambios (botón sin texto visible) | Enviar datos a `PUT /settings` y mostrar toast de éxito |
| **src/pages/Recipes.jsx** | Crear Receta (botón superior) | Abrir modal `CreateRecipeModal` |
| | Agregar Ingrediente (en tabla) | Abrir modal `AddRecipeItemModal` en modo ingrediente |
| | Eliminar Receta (icono papelera) | Llamar a `DELETE /recipes/{id}` y refrescar lista |
| **src/pages/RecipeDetail.jsx** | Editar Receta (cerca del título) | Abrir `CreateRecipeModal` con datos cargados |
| | Agregar Ingrediente (dentro del detalle) | Abrir `AddRecipeItemModal` (modo ingrediente) |
| | Agregar Sub‑Receta (cerca del detalle) | Abrir `AddRecipeItemModal` (modo sub‑recipe) |
| | Eliminar componente (icono X) | Llamar a `DELETE /recipe-components/{id}` y actualizar UI |
| **src/pages/Production.jsx** | Generar Lista de Preparación | Llamar a `GET /production/prep-list` y mostrar resultados |
| | Iniciar Producción | Cambiar estado del evento a `IN_PRODUCTION` vía `PATCH /events/{id}` |
| | Ver Rutas de Entrega | Navegar a `/logistics` o llamar a `GET /logistics/delivery-routes` |
| **src/pages/Ingredients.jsx** | Nuevo Ingrediente (botón superior) | Abrir modal `CreateIngredientModal` |
| | Importar CSV (icono importación) | Ejecutar `POST /ingredients/batch-import` con archivo CSV |
| | Editar (icono lápiz en fila) | Abrir `CreateIngredientModal` con datos del ingrediente |
| | Eliminar (icono papelera) | Llamar a `DELETE /ingredients/{id}` y refrescar tabla |
| **src/pages/Events.jsx** | Crear Evento (botón superior) | Abrir modal `CreateEventModal` |
| | Ver Detalle (icono ojo en fila) | Navegar a `/events/{id}` |
| | Editar (icono lápiz) | Abrir `CreateEventModal` con datos del evento |
| **src/components/Layout.jsx** | Menú hamburguesa (línea 57) | Alternar barra lateral (`setOpen(!open)`) |
| | Cerrar sesión (línea 98) | Ejecutar `firebase.auth().signOut()` y redirigir a `/login` |
| | Cambiar tema (línea 110) | Toggle de tema dark/light mediante Zustand store |
| **src/components/recipes/CreateRecipeModal.jsx** | Cancelar (botón cerrar) | Cerrar modal (`setOpen(false)`) |
| | Guardar (botón submit) | Enviar `POST /recipes` con datos del formulario y cerrar modal |
| **src/components/recipes/AddRecipeItemModal.jsx** | Cancelar | Cerrar modal |
| | Agregar (botón confirmar) | Enviar `POST /recipe-components` y actualizar receta |
| **src/components/ingredients/CreateIngredientModal.jsx** | Cancelar | Cerrar modal |
| | Guardar | Enviar `POST /ingredients` (quick‑add) y cerrar modal |
| **src/components/events/CreateEventModal.jsx** | Cancelar | Cerrar modal |
| | Guardar | Enviar `POST /events` y cerrar modal |

## Notas de accesibilidad

- Cada botón debe incluir `aria-label` descriptivo.
- Añadir `type="button"` o `type="submit"` según corresponda.
- Implementar `onKeyDown` que capture `Enter` o `Space` y dispare el mismo handler que `onClick`.
