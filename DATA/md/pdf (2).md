# pdf (2)

cZr Catering - Especificación de API
(Contrato)
ID del Proyecto: CZR-2025
Formato: RESTful JSON
Base URL: https://api.czr.catering/v1
1. Authentication
Todos los endpoints privados requieren header:
Authorization: Bearer <Firebase_ID_Token>
2. Endpoints: Ingredientes
Buscar Ingredientes
GET /ingredients
Query Params:
● q: string (Término de búsqueda)
● limit: number (Default 20)
Response (200 OK):
{
"data": [
{
"id": "123",
"name": "Tomate Perita",
"cost": 1500,
"unit": "kg",
"source": "INTERNAL" // o "SCRAPING" si es sugerencia
}
]
}
Crear Ingrediente (Quick Add)
POST /ingredients
Payload:
{
"name": "Pimentón Ahumado",

"unit": "kg",
"initial_cost": 45000,
"category": "Especias",
"is_quick_add": true
}
Response (201 Created):
{
"id": "new_uuid_789",
"status": "created_pending_review"
}
3. Endpoints: Recetas
Calcular Receta (Borrador)
POST /recipes/calculate
Permite enviar una estructura de receta sin guardarla para obtener costos en tiempo real.
Payload:
{
"components": [
{ "id": "123", "qty": 0.5 },
{ "id": "456", "qty": 2 }
],
"margin": 300
}
Response (200 OK):
{
"total_cost": 5000,
"suggested_price": 20000,
"nutrition_summary": { "kcal": 450 }
}
4. Endpoints: Propuestas (Core Comercial)
Generar Snapshot (Congelar)

POST /proposals
Payload:
{
"recipe_ids": ["rec_01", "rec_02"],
"client_info": {
"name": "Empresa S.A.",
"event_date": "2025-12-24"
},
"validity_days": 15
}
Response (201 Created):
{
"proposal_id": "pub_999",
"public_url": "[https://czr.catering/view/pub_999](https://czr.catering/view/pub_999)",
"expiration": "2025-12-30T23:59:59Z"
}
Leer Propuesta (Público)
GET /public/proposals/{id}
Response (200 OK):
Nota: Este endpoint NO devuelve campos de costo bajo ninguna circunstancia.
{
"client": "Empresa S.A.",
"items": [
{
"name": "Ravioles de Lomo",
"description": "Pasta casera...",
"price": 20000,
"badges": ["NUTRI_A"]
}
]
}
5. Códigos de Error Estándar

● 400 Bad Request: Datos de entrada inválidos (ej: margen negativo).
● 401 Unauthorized: Token faltante o inválido.
● 403 Forbidden: Rol insuficiente (ej: Cocinero intentando ver costos).
● 404 Not Found: Receta o Ingrediente no existe.
● 409 Conflict: Intentando modificar una propuesta ya aceptada/cerrada.
● 422 Unprocessable Entity: Error de validación de negocio (ej: Ingrediente sin precio
base).

