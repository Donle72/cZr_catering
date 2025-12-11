# 🚀 Guía de Inicio Rápido - cZr Catering

## Opción 1: Inicio Rápido con Docker (Recomendado)

### Prerrequisitos

- Docker Desktop instalado y corriendo

### Pasos

1. **Levantar todos los servicios**

```bash
docker-compose up -d
```

2. **Esperar a que los servicios estén listos** (30-60 segundos)

3. **Inicializar la base de datos con datos de ejemplo**

```bash
docker-compose exec backend python init_db.py
```

4. **Acceder a la aplicación**

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:8000>
- Documentación API: <http://localhost:8000/docs>

5. **Ver logs** (opcional)

```bash
docker-compose logs -f
```

6. **Detener servicios**

```bash
docker-compose down
```

---

## Opción 2: Desarrollo Local (Sin Docker)

### Backend

1. **Crear entorno virtual**

```bash
cd backend
python -m venv venv
```

2. **Activar entorno virtual**

- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

```bash
copy .env.example .env
# Editar .env con tus configuraciones
```

5. **Asegurarse de que PostgreSQL esté corriendo**

- Puedes usar Docker solo para la DB:

```bash
docker run -d -p 5432:5432 -e POSTGRES_USER=catering_user -e POSTGRES_PASSWORD=catering_pass_2025 -e POSTGRES_DB=catering_db postgres:15-alpine
```

6. **Inicializar base de datos**

```bash
python init_db.py
```

7. **Iniciar servidor**

```bash
uvicorn app.main:app --reload
```

### Frontend

1. **Instalar dependencias**

```bash
cd frontend
npm install
```

2. **Configurar variables de entorno** (opcional)

```bash
# Crear archivo .env
echo "VITE_API_URL=http://localhost:8000" > .env
```

3. **Iniciar servidor de desarrollo**

```bash
npm run dev
```

4. **Acceder a la aplicación**

- <http://localhost:3000>

---

## 🧪 Probar la API

### Usando la documentación interactiva (Swagger)

1. Ir a <http://localhost:8000/docs>
2. Explorar los endpoints disponibles
3. Probar directamente desde el navegador

### Usando curl

**Listar ingredientes:**

```bash
curl http://localhost:8000/api/v1/ingredients
```

**Crear un ingrediente:**

```bash
curl -X POST http://localhost:8000/api/v1/ingredients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Azúcar",
    "category": "Endulzantes",
    "purchase_unit_id": 1,
    "usage_unit_id": 2,
    "conversion_ratio": 1000,
    "current_cost": 500,
    "yield_factor": 1.0
  }'
```

**Actualización masiva de precios (anti-inflación):**

```bash
curl -X POST "http://localhost:8000/api/v1/ingredients/bulk-price-update?category=Carnes&percentage_increase=15"
```

---

## 📊 Datos de Ejemplo

Después de ejecutar `init_db.py`, tendrás:

- ✅ 8 unidades de medida (kg, g, L, mL, etc.)
- ✅ 3 proveedores de ejemplo
- ✅ 10 ingredientes con factores de rendimiento realistas

---

## 🛠️ Comandos Útiles

### Docker

```bash
# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar un servicio
docker-compose restart backend

# Reconstruir imágenes
docker-compose build

# Limpiar todo (¡cuidado! borra los datos)
docker-compose down -v
```

### Base de Datos

```bash
# Conectarse a PostgreSQL (con Docker)
docker-compose exec postgres psql -U catering_user -d catering_db

# Ver tablas
\dt

# Ver ingredientes
SELECT id, name, current_cost, yield_factor FROM ingredients;
```

---

## 🐛 Solución de Problemas

### El frontend no se conecta al backend

- Verificar que el backend esté corriendo en <http://localhost:8000>
- Verificar CORS en `backend/app/core/config.py`

### Error de base de datos

- Verificar que PostgreSQL esté corriendo
- Verificar credenciales en `.env` o `docker-compose.yml`
- Intentar recrear la base de datos: `docker-compose down -v && docker-compose up -d`

### Puerto ya en uso

- Cambiar puertos en `docker-compose.yml`
- O detener el servicio que está usando el puerto

---

## 📚 Próximos Pasos

1. ✅ Explorar la página de Ingredientes
2. ✅ Probar la actualización masiva de precios
3. ✅ Revisar la documentación de la API
4. 🔜 Crear recetas (próximamente)
5. 🔜 Gestionar eventos (próximamente)

---

## 💡 Tips

- Usa la documentación interactiva en `/docs` para explorar la API
- Los ingredientes tienen un **factor de rendimiento** que calcula el costo real considerando mermas
- La actualización masiva de precios es clave para manejar inflación
- El sistema está diseñado para escalar con más funcionalidades

---

¡Listo para comenzar! 🎉
