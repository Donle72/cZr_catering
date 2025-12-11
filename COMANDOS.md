# 🔧 Comandos Útiles - cZr Catering

## Docker Commands

### Iniciar/Detener Servicios

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar TODO (incluye volúmenes)
docker-compose down -v
```

### Reconstruir Imágenes

```bash
# Reconstruir todas las imágenes
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Reconstruir y reiniciar
docker-compose up -d --build
```

### Ejecutar Comandos en Contenedores

```bash
# Inicializar base de datos
docker-compose exec backend python init_db.py

# Shell en el backend
docker-compose exec backend bash

# Shell en PostgreSQL
docker-compose exec postgres psql -U catering_user -d catering_db

# Instalar dependencias Python
docker-compose exec backend pip install <paquete>

# Instalar dependencias Node
docker-compose exec frontend npm install <paquete>
```

---

## Backend Commands (Python/FastAPI)

### Desarrollo Local

```bash
cd backend

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload

# Iniciar en puerto diferente
uvicorn app.main:app --reload --port 8001

# Inicializar base de datos
python init_db.py
```

### Testing

```bash
# Ejecutar tests (cuando se implementen)
pytest

# Con coverage
pytest --cov=app

# Ver coverage en HTML
pytest --cov=app --cov-report=html
```

### Formateo y Linting

```bash
# Formatear código con Black
black app/

# Verificar con flake8
flake8 app/

# Type checking con mypy
mypy app/
```

### Base de Datos

```bash
# Crear migración (Alembic - cuando se configure)
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

---

## Frontend Commands (React/Vite)

### Desarrollo Local

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Iniciar en puerto diferente
npm run dev -- --port 3001

# Build para producción
npm run build

# Preview del build
npm run preview
```

### Gestión de Dependencias

```bash
# Instalar paquete
npm install <paquete>

# Instalar como dev dependency
npm install -D <paquete>

# Actualizar dependencias
npm update

# Ver dependencias desactualizadas
npm outdated

# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Linting

```bash
# Ejecutar ESLint
npm run lint

# Fix automático
npm run lint -- --fix
```

---

## Database Commands (PostgreSQL)

### Conexión

```bash
# Con Docker
docker-compose exec postgres psql -U catering_user -d catering_db

# Local (si tienes psql instalado)
psql -h localhost -U catering_user -d catering_db
```

### Comandos SQL Útiles

```sql
-- Ver todas las tablas
\dt

-- Describir tabla
\d ingredients

-- Ver ingredientes
SELECT id, name, current_cost, yield_factor, real_cost_per_usage_unit 
FROM ingredients;

-- Ver recetas con costos
SELECT id, name, recipe_type, yield_quantity, target_margin 
FROM recipes;

-- Ver eventos
SELECT id, event_number, name, client_name, event_date, status 
FROM events;

-- Contar registros
SELECT COUNT(*) FROM ingredients;
SELECT COUNT(*) FROM recipes;
SELECT COUNT(*) FROM events;

-- Backup de tabla
\copy ingredients TO '/tmp/ingredients_backup.csv' CSV HEADER;

-- Restaurar desde CSV
\copy ingredients FROM '/tmp/ingredients_backup.csv' CSV HEADER;

-- Eliminar todos los datos (¡CUIDADO!)
TRUNCATE TABLE ingredients CASCADE;

-- Salir
\q
```

### Backup y Restore

```bash
# Backup completo
docker-compose exec postgres pg_dump -U catering_user catering_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U catering_user catering_db < backup.sql

# Backup solo datos
docker-compose exec postgres pg_dump -U catering_user --data-only catering_db > data.sql

# Backup solo esquema
docker-compose exec postgres pg_dump -U catering_user --schema-only catering_db > schema.sql
```

---

## API Testing (curl)

### Ingredientes

```bash
# Listar todos
curl http://localhost:8000/api/v1/ingredients

# Buscar por nombre
curl "http://localhost:8000/api/v1/ingredients?search=papa"

# Filtrar por categoría
curl "http://localhost:8000/api/v1/ingredients?category=Carnes"

# Paginación
curl "http://localhost:8000/api/v1/ingredients?skip=0&limit=10"

# Obtener uno específico
curl http://localhost:8000/api/v1/ingredients/1

# Crear ingrediente
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

# Actualizar ingrediente
curl -X PUT http://localhost:8000/api/v1/ingredients/1 \
  -H "Content-Type: application/json" \
  -d '{"current_cost": 550}'

# Eliminar ingrediente
curl -X DELETE http://localhost:8000/api/v1/ingredients/1

# Actualización masiva de precios
curl -X POST "http://localhost:8000/api/v1/ingredients/bulk-price-update?category=Carnes&percentage_increase=15"
```

### Recetas

```bash
# Listar recetas
curl http://localhost:8000/api/v1/recipes

# Obtener receta con costos
curl http://localhost:8000/api/v1/recipes/1
```

### Eventos

```bash
# Listar eventos
curl http://localhost:8000/api/v1/events

# Obtener evento con financials
curl http://localhost:8000/api/v1/events/1
```

### Health Check

```bash
# Verificar que la API está corriendo
curl http://localhost:8000/health

# Ver información general
curl http://localhost:8000/
```

---

## Git Commands

### Workflow Básico

```bash
# Ver estado
git status

# Agregar archivos
git add .

# Commit
git commit -m "feat: descripción del cambio"

# Push
git push origin main

# Pull
git pull origin main
```

### Branches

```bash
# Crear branch
git checkout -b feature/nueva-funcionalidad

# Cambiar de branch
git checkout main

# Ver branches
git branch

# Merge
git merge feature/nueva-funcionalidad

# Eliminar branch
git branch -d feature/nueva-funcionalidad
```

### Útiles

```bash
# Ver historial
git log --oneline --graph

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer cambios en archivo
git checkout -- archivo.py

# Ver diferencias
git diff

# Stash (guardar cambios temporalmente)
git stash
git stash pop
```

---

## Monitoring & Debugging

### Ver Recursos Docker

```bash
# Ver uso de recursos
docker stats

# Ver contenedores corriendo
docker ps

# Ver todos los contenedores
docker ps -a

# Ver imágenes
docker images

# Ver volúmenes
docker volume ls

# Limpiar recursos no usados
docker system prune
```

### Logs de Aplicación

```bash
# Backend logs
docker-compose logs -f backend

# Ver últimas 100 líneas
docker-compose logs --tail=100 backend

# Frontend logs
docker-compose logs -f frontend

# PostgreSQL logs
docker-compose logs -f postgres
```

### Debugging

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Ver variables de entorno
docker-compose exec backend env

# Ver procesos
docker-compose exec backend ps aux

# Verificar conectividad a la DB
docker-compose exec backend python -c "from app.core.database import engine; print(engine.connect())"
```

---

## Performance Testing

### Load Testing con Apache Bench

```bash
# Instalar (si no está)
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Test simple
ab -n 100 -c 10 http://localhost:8000/api/v1/ingredients

# Test con POST
ab -n 100 -c 10 -p data.json -T application/json http://localhost:8000/api/v1/ingredients
```

### Monitoring

```bash
# Ver uso de CPU/RAM del backend
docker stats backend

# Ver conexiones a PostgreSQL
docker-compose exec postgres psql -U catering_user -d catering_db -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## Troubleshooting

### Puerto ya en uso

```bash
# Windows - Ver qué usa el puerto 8000
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Matar proceso
# Windows: taskkill /PID <PID> /F
# Linux/Mac: kill -9 <PID>
```

### Reiniciar todo desde cero

```bash
# Detener y eliminar TODO
docker-compose down -v

# Eliminar imágenes
docker-compose down --rmi all

# Reconstruir y reiniciar
docker-compose up -d --build

# Reinicializar DB
docker-compose exec backend python init_db.py
```

### Problemas de permisos

```bash
# Dar permisos a archivos
chmod +x script.sh

# Cambiar dueño (Linux/Mac)
sudo chown -R $USER:$USER .
```

---

## Shortcuts & Aliases (Opcional)

Agregar a tu `.bashrc` o `.zshrc`:

```bash
# Docker Compose
alias dc='docker-compose'
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcbuild='docker-compose up -d --build'

# Backend
alias backend='docker-compose exec backend'
alias initdb='docker-compose exec backend python init_db.py'

# Frontend
alias frontend='docker-compose exec frontend'

# PostgreSQL
alias psql-catering='docker-compose exec postgres psql -U catering_user -d catering_db'

# Git
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
```

---

¡Estos comandos te harán mucho más productivo! 🚀
