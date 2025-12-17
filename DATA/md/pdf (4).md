# pdf (4)

cZr Catering - Especificación de
Requerimientos Funcionales (FRS)
ID del Proyecto: CZR-2025
Versión: 1.0.1
Estado: Aprobado para Desarrollo
Autor: Leo Zelvys
1. Introducción
1.1 Propósito
Este documento define el comportamiento funcional exacto del sistema cZr Catering. Sirve
como referencia única para desarrolladores y QA.
1.2 Reglas de Negocio Globales (BR)
● BR-01 (Inmutabilidad Comercial): Una vez generada una Propuesta para un cliente, los
precios y descripciones contenidas en ella NO deben cambiar, incluso si cambian los
costos base en el sistema.
● BR-02 (Segregación de Vistas): La vista del Cliente jamás debe tener acceso, ni
siquiera oculto en el HTML, a datos de costos, márgenes o proveedores.
● BR-03 (Unicidad de Receta): Una receta se define por su versión. Cualquier cambio en
ingredientes que afecte el costo en más de un 5% debe sugerir una nueva versión o
re-costeo explícito.
2. Actores del Sistema
1. Administrador/Chef (SuperUser): Acceso total a costos, configuración y usuarios.
2. Encargado de Compras: Acceso a Materia Prima y Proveedores. No puede modificar
margen de recetas.
3. Cliente Final: Acceso de solo lectura a Propuestas específicas mediante Token.
3. Casos de Uso Detallados (UC)
Módulo: Materia Prima
UC-01: Alta de Ingrediente con Enriquecimiento (IA/Scraping)
● Actor: Chef / Compras.
● Precondición: Usuario logueado en módulo Interno.
● Flujo Principal:
1. El usuario ingresa el nombre del producto en el buscador (ej: "Tomate Perita").
2. El sistema consulta API externa (Job de Scraping/IA).
3. El sistema despliega una tarjeta con datos sugeridos: Precio Promedio Mercado,

Estacionalidad, Datos Nutricionales.
4. El usuario confirma o edita los valores.
5. El usuario asigna un Proveedor Preferido (opcional).
6. El sistema guarda el ingrediente con versión: 1.
● Flujo Alternativo (Sin conexión):
1. El sistema alerta "Modo Offline".
2. Permite carga manual completa.
UC-02: Alta Rápida en Contexto ("Quick Add")
● Actor: Chef.
● Contexto: El usuario está dentro del diseñador de Recetas (UC-03).
● Flujo Principal:
1. El usuario busca un ingrediente que no existe.
2. El sistema muestra opción "Crear [Nombre] ahora".
3. Se despliega un modal simplificado (solo Nombre, Unidad y Costo Estimado).
4. Al guardar, el ingrediente se crea en BD y se asigna automáticamente a la receta
actual.
5. Se marca internamente como data_incompleta: true para revisión posterior.
Módulo: Ingeniería de Recetas
UC-03: Diseño de Receta (Híbrido)
● Actor: Chef.
● Flujo Principal:
1. Usuario crea nueva receta.
2. Modo Teclado: Usuario se posiciona en la grilla, escribe código o nombre parcial,
presiona Enter. Sistema agrega línea.
3. Modo Visual: Usuario arrastra ingrediente desde panel lateral "Despensa".
4. Sistema calcula en tiempo real: Costo Total = Sumatoria(Costo Unitario * Cantidad *
FactorMerma).
5. Sistema sugiere Precio de Venta basado en Margen Global configurado.
6. Usuario puede sobreescribir el Precio de Venta manual.
UC-04: Gestión de Sub-Recetas
● Regla: Una receta puede comportarse como ingrediente.
● Flujo:
1. Usuario selecciona tipo "Sub-Receta" (ej: Salsa Bechamel).
2. El sistema calcula el costo por unidad de medida (ej: $/litro) de esa preparación.
3. Esta sub-receta queda disponible en el buscador de ingredientes para otras recetas.
Módulo: Propuestas Comerciales
UC-05: Generación de Snapshot (Propuesta)
● Actor: Chef / Comercial.

● Precondición: Receta en estado "Activa".
● Flujo Principal:
1. Usuario selecciona una o varias recetas.
2. Usuario selecciona "Generar Propuesta Cliente".
3. El sistema solicita: Nombre del Cliente, Fecha de Validez, Tipo de Evento.
4. Proceso Crítico: El sistema realiza una Deep Copy (Copia profunda) de los datos
visuales y nutricionales. Descarta costos.
5. Genera un ID único (UUID) para acceso público.
6. Devuelve URL para compartir (ej: czr.catering/p/ax99-vk22).
4. Requerimientos No Funcionales (NFR)
● NFR-01 (Latencia): La búsqueda de ingredientes debe retornar resultados en < 200ms.
● NFR-02 (Disponibilidad): El módulo de Propuestas (Cliente) debe estar disponible
99.9%, desacoplado del módulo operativo.
● NFR-03 (Seguridad): Los endpoints de administración deben requerir autenticación
JWT con Claims de Rol adecuados.

