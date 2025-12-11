# 🚀 Guía de Inicio - cZr Catering

## ✅ Lo que ya está hecho

- ✅ PostgreSQL corriendo en Docker (puerto 5432)
- ✅ Código completo del backend y frontend
- ✅ Scripts de inicio automático
- ✅ Puertos configurados: Backend 8020, Frontend 3020

## 📋 Pasos para Ejecutar el Sistema

### 1️⃣ Backend (FastAPI)

**Opción A - Script Automático (Recomendado):**

```bash
cd backend
.\start.bat
```

**Opción B - Manual:**

```bash
cd backend

# Crear entorno virtual (solo la primera vez)
py -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# Inicializar base de datos (solo la primera vez)
py init_db.py

# Iniciar servidor
uvicorn app.main:app --reload --port 8020
```

El backend estará disponible en:

- **API**: <http://localhost:8020>
- **Documentación**: <http://localhost:8020/docs>

---

### 2️⃣ Frontend (React)

**Primero, instala Node.js si no lo tienes:**

- Descargar de: <https://nodejs.org/> (versión LTS recomendada)

**Luego:**

```bash
cd frontend

# Instalar dependencias (solo la primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en:

- **Aplicación**: <http://localhost:3020>

---

## 🎯 Resumen Rápido

```bash
# Terminal 1 - Backend
cd backend
.\start.bat

# Terminal 2 - Frontend (después de instalar Node.js)
cd frontend
npm install
npm run dev
```

---

## 🐛 Solución de Problemas

### PostgreSQL no está corriendo

```bash
docker run -d --name czr_catering_postgres -p 5432:5432 \
  -e POSTGRES_USER=catering_user \
  -e POSTGRES_PASSWORD=catering_pass_2025 \
  -e POSTGRES_DB=catering_db \
  postgres:15-alpine
```

### Error "python not found"

- Usar `py` en lugar de `python`
- O agregar Python al PATH

### Error "node not found"

- Instalar Node.js desde <https://nodejs.org/>

### Puerto 8020 ya en uso

```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :8020

# Matar el proceso (reemplazar PID)
taskkill /PID <PID> /F
```

### Puerto 3020 ya en uso

```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :3020

# Matar el proceso (reemplazar PID)
taskkill /PID <PID> /F
```

---

## 📊 Datos de Ejemplo

Después de ejecutar `py init_db.py`, tendrás:

- ✅ 8 unidades de medida
- ✅ 3 proveedores
- ✅ 10 ingredientes con factores de rendimiento

---

## 🎉 ¡Listo

Una vez que ambos servicios estén corriendo:

1. Abre <http://localhost:3020> en tu navegador
2. Explora el Dashboard
3. Ve a "Ingredientes" para ver los datos de ejemplo
4. Prueba la API en <http://localhost:8020/docs>

---

**¿Necesitas ayuda?** Revisa los logs en las terminales donde ejecutaste los comandos.
