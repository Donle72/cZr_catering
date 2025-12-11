# 🍽️ cZr Costeo Catering

Sistema integral de gestión de catering con ingeniería gastronómica computacional.

## 🎯 Características Principales

### Fase 1: MVP Operativo (Actual)

- ✅ Gestión de Ingredientes con Factor de Rendimiento (Yield Management)
- ✅ Recetas con Costeo Recursivo
- ✅ Creación y Gestión de Eventos
- ✅ Generación de Hojas de Producción Consolidadas
- ✅ Listas de Compras Inteligentes
- ✅ Actualización Masiva de Precios (Anti-Inflación)

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
- **Alembic** (Migraciones)

### Frontend

- **React 18+** con TypeScript
- **Tailwind CSS** (Diseño moderno)
- **Vite** (Build tool)
- **React Query** (Estado del servidor)
- **React Router** (Navegación)

### DevOps

- **Docker & Docker Compose**
- **Nginx** (Reverse proxy)

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker Desktop
- Node.js 18+ (para desarrollo frontend)
- Python 3.11+ (para desarrollo backend)

### Instalación con Docker

```bash
# Clonar el repositorio
git clone <repo-url>
cd cZr_CosteoCatering

# Levantar todos los servicios
docker-compose up -d

# La aplicación estará disponible en:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - Documentación API: http://localhost:8000/docs
```

### Desarrollo Local

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentación

- [Arquitectura del Sistema](./docs/arquitectura.md)
- [Modelo de Datos](./docs/modelo-datos.md)
- [API Reference](http://localhost:8000/docs) (cuando el servidor esté corriendo)
- [Guía de Desarrollo](./docs/desarrollo.md)

## 🧮 Algoritmos Clave

### Factor de Rendimiento (Yield Factor)

```
Costo Real = Precio Compra / Rendimiento%
```

### Escalado de Recetas (Recipe Conversion Factor)

```
RCF = Rendimiento Deseado / Rendimiento Original
```

### Ajuste de Precios por Inflación

```
Nuevo Precio Venta = Nuevo Costo / (1 - Margen Objetivo%)
```

## 📄 Licencia

Propietario - cZr © 2025

## 👥 Equipo

Desarrollado con ❤️ para revolucionar la gestión de catering en LatAm.
