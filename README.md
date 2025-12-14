# 🍽️ cZr Costeo Catering

**Versión:** 1.1.0 | **Estado:** ✅ Production Ready (con tests pendientes)

Sistema integral de gestión de catering con ingeniería gastronómica computacional.

## 🎯 Características Principales

### Fase 1: MVP Operativo (Actual)

- ✅ Gestión de Ingredientes con Factor de Rendimiento (Yield Management)
- ✅ Recetas con Costeo Recursivo
- ✅ Creación y Gestión de Eventos
- ✅ Generación de Hojas de Producción Consolidadas
- ✅ Listas de Compras Inteligentes
- ✅ Actualización Masiva de Precios (Anti-Inflación)
- ✅ **NUEVO:** Manejo de errores robusto
- ✅ **NUEVO:** Logging estructurado
- ✅ **NUEVO:** Validaciones mejoradas
- ✅ **NUEVO:** Seguridad reforzada

### Roadmap

- 📋 **Fase 2**: CRM, Propuestas Web, Firma Digital
- 📱 **Fase 3**: App Móvil Flutter, KDS, Facturación Electrónica
- 🤖 **Fase 4**: IA Predictiva, Analytics de Desperdicios

## 🛠️ Stack Tecnológico

### Backend

- **Python 3.11+** con FastAPI
- **PostgreSQL 15+** (Base de datos relacional)
- **Redis** (Caché y sesiones)
- **SQLAlchemy** (ORM)
- **Alembic** (Migraciones - próximamente)

### Frontend

- **React 18+** con JavaScript
- **Tailwind CSS** (Diseño moderno)
- **Vite** (Build tool)
- **React Query** (Estado del servidor)
- **React Router** (Navegación)

### DevOps

- **Docker & Docker Compose**
- **Nginx** (Reverse proxy - próximamente)

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker Desktop
- Node.js 18+ (para desarrollo frontend)
- Python 3.11+ (para desarrollo backend)

### Instalación con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd cZr_CosteoCatering

# 2. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con tus valores

# 3. Levantar todos los servicios
docker-compose up -d

# 4. Inicializar base de datos con datos de ejemplo
docker-compose exec backend python init_db.py

# 5. La aplicación estará disponible en:
# - Frontend: http://localhost:3020
# - Backend API: http://localhost:8020
# - Documentación API: http://localhost:8020/docs
# - Health Check: http://localhost:8020/health
```

### Desarrollo Local

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus valores

# Iniciar servidor
uvicorn app.main:app --reload --port 8020
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

## 📚 Documentación

### Documentación Principal

- **[QUICKSTART.md](./QUICKSTART.md)** - Guía de inicio rápido
- **[IMPLEMENTACION.md](./IMPLEMENTACION.md)** - Detalles de implementación
- **[MEJORAS_IMPLEMENTADAS.md](./MEJORAS_IMPLEMENTADAS.md)** - ✨ Mejoras v1.1.0

### Análisis y Planificación

- **[ANALISIS_Y_MEJORAS.md](./ANALISIS_Y_MEJORAS.md)** - Análisis completo del código
- **[PLAN_MEJORAS_PRIORITARIO.md](./PLAN_MEJORAS_PRIORITARIO.md)** - Roadmap de mejoras
- **[QUICK_WINS.md](./QUICK_WINS.md)** - Mejoras rápidas
- **[ESTADO_PROYECTO.md](./ESTADO_PROYECTO.md)** - Estado actual

### API

- **[API Docs (Swagger)](http://localhost:8020/docs)** - Documentación interactiva
- **[API Docs (ReDoc)](http://localhost:8020/redoc)** - Documentación alternativa

## 🧮 Algoritmos Clave

### Factor de Rendimiento (Yield Factor)

```
Costo Real = (Precio Compra / Ratio Conversión) / Rendimiento%
```

**Ejemplo:** Papa a $450/kg con 80% rendimiento = $562.50/kg real

### Escalado de Recetas (Recipe Conversion Factor)

```
RCF = Rendimiento Deseado / Rendimiento Original
Cantidad Escalada = Cantidad Original × RCF
```

### Ajuste de Precios por Inflación

```
Nuevo Costo = Costo Actual × (1 + Porcentaje/100)
Nuevo Precio Venta = Nuevo Costo / (1 - Margen Objetivo%)
```

## ✨ Novedades v1.1.0

### Seguridad

- ✅ Variables de entorno obligatorias (`.env`)
- ✅ Validación de `SECRET_KEY` (mínimo 32 caracteres)
- ✅ Sin credenciales hardcodeadas

### Manejo de Errores

- ✅ Sistema de excepciones personalizado
- ✅ Respuestas de error estructuradas y consistentes
- ✅ Logging de todos los errores

### Logging

- ✅ Logs estructurados (JSON en producción)
- ✅ Niveles de log configurables
- ✅ Trazabilidad completa de operaciones

### Validaciones

- ✅ Validación robusta de `yield_factor` (0-1)
- ✅ Validación de costos no negativos
- ✅ Mensajes de error descriptivos

### Observabilidad

- ✅ Health check mejorado con verificación de BD
- ✅ Logging de requests con duración
- ✅ Métricas de operaciones

Ver **[MEJORAS_IMPLEMENTADAS.md](./MEJORAS_IMPLEMENTADAS.md)** para detalles completos.

## 🔒 Configuración de Seguridad

### Variables de Entorno Requeridas

Crear `backend/.env` con:

```bash
# Security (REQUIRED)
SECRET_KEY=<generar-con-openssl-rand-hex-32>
DATABASE_URL=postgresql://user:password@postgres:5432/catering_db

# Redis
REDIS_URL=redis://redis:6379/0

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS
CORS_ORIGINS=http://localhost:3020,http://localhost:5173
```

**⚠️ IMPORTANTE:** Nunca commitear el archivo `.env` a Git.

## 📄 Licencia

Propietario - cZr © 2025

## 👥 Equipo

Desarrollado con ❤️ para revolucionar la gestión de catering en LatAm.

---

## 🆘 Soporte

- **Documentación:** Ver archivos `.md` en el repositorio
- **API Docs:** <http://localhost:8020/docs>
- **Health Check:** <http://localhost:8020/health>
- **Logs:** `docker-compose logs -f backend`
