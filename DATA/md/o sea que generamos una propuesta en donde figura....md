# o sea que generamos una propuesta en donde figura...

MODELO DE DOCUMENTO: PROPUESTA
DE CATERING (Template Maestro)
1. ENCABEZADO (Header)
[LOGO LEOCOZINA] Pasión, Historia y Estrategia.
Datos del Cliente Información del Evento
Cliente: {{client.name}} ID Propuesta: {{proposal.id}}
({{client.company}})
Contacto: {{client.email}} Fecha Evento: {{event.date}}
Teléfono: {{client.phone}} Horario: {{event.start_time}} a
{{event.end_time}} ({{event.duration}} hs)
Locación: {{event.venue_name}}
Invitados (Pax): {{event.pax_count}}
2. INTRODUCCIÓN (La Narrativa)
Hola {{client.first_name}},
Es un placer presentarte esta propuesta para {{event.name}}. En LeoCozina creemos que la
comida no es solo alimentación, es el vehículo para contar historias y generar momentos
inolvidables.
Basado en nuestra conversación, he diseñado un menú que fusiona
{{proposal.style_tagline}} (ej: "la tradición siria con toques modernos"), pensado
exclusivamente para el perfil de tus invitados. Nuestro objetivo es que vos te ocupes de
disfrutar, mientras nosotros nos encargamos de la magia operativa.
3. EXPERIENCIA GASTRONÓMICA (El Menú)
[INICIO BLOQUE: RECEPCIÓN]
🥂
Recepción: El comienzo de la historia
Un recorrido de sabores en formato finger-food, circulando entre los invitados.

{{menu.reception.items}} (Iteración de ítems seleccionados)
• {{item.name}}: {{item.description}} (Tags: {{item.dietary_tags}} - ej: Sin TACC,
Vegano)
[FIN BLOQUE: RECEPCIÓN]
[INICIO BLOQUE: PRINCIPAL]
🍽
Plato Principal: El protagonista
Servido en mesa / Buffet (según configuración).
Opción seleccionada:
{{menu.main_dish.name}} {{menu.main_dish.detailed_description}} Maridaje
sugerido: {{menu.main_dish.pairing_note}}
[FIN BLOQUE: PRINCIPAL]
[INICIO BLOQUE: POSTRE & DULCE]
🍰
Final Dulce
{{menu.dessert.name}}
Mesa Dulce / Café:
{{menu.sweet_table.description}}
[FIN BLOQUE: POSTRE & DULCE]
4. LOGÍSTICA Y SERVICIO (El "Backstage")
Para garantizar la excelencia operativa que nos caracteriza, el servicio incluye:
Recursos Humanos (Staff) Personal uniformado y asegurado (ART).
● {{staff.waiters_qty}} Camareros (Ratio 1 cada {{config.waiter_ratio}} pax).
● {{staff.chefs_qty}} Cocineros y Ayudantes.
● 1 Jefe de Evento (Coordinación general).
Infraestructura y Vajilla
● Vajilla completa (Platos, copas, cubiertos línea {{logistics.crockery_type}}).
● Mantelería y Servilletas (Color: {{logistics.linen_color}}).
● Equipamiento de cocina móvil (Hornos, anafes según requerimiento técnico).

Bebidas y Hielo
● Servicio de hielo ilimitado durante las {{event.duration}} horas.
● Bebidas sin alcohol (Agua con/sin gas, Gaseosas línea Coca-Cola).
● (Opcional/Si aplica): Vinos y Espumantes según consignación o descorche.
5. PRESUPUESTO E INVERSIÓN
Valores expresados en {{currency.code}} (Pesos Argentinos).
Concepto Detalle Valor Unitario Subtotal
Menú / Catering {{event.pax_count}} {{financials.unit_pri {{financials.food_su
pax x Menú ce}} btotal}}
"{{menu.name}}"
Logística y Staff Servicio integral - {{financials.logistic
operativo s_subtotal}}
Adicionales {{financials.extras_ - {{financials.extras_
description}} subtotal}}
SUBTOTAL {{financials.subtot
al}}
Bonificación {{financials.discoun -
t_note}} {{financials.discoun
t_amount}}
TOTAL FINAL {{financials.grand
_total}}
6. TÉRMINOS Y CONDICIONES (La Letra Chica
Importante)
1. Validez de la Oferta:
Debido a la volatilidad de costos de materia prima, este presupuesto tiene una validez de
{{config.validity_days}} días corridos desde la fecha de emisión ({{proposal.created_at}}).
Pasado este lapso, los valores están sujetos a re-cotización.
2. Política de Ajuste (Inflación):
El precio se congela en un {{financials.freeze_percent}}% al momento de la seña. El saldo

restante se ajustará según el índice {{financials.inflation_index}} (o costo de lista de
proveedores mayoristas) al momento del pago final.
3. Forma de Pago:
● Reserva de Fecha: {{financials.down_payment_percent}}% del total.
● Saldo: Debe estar cancelado 72hs hábiles antes del evento.
4. Modificaciones:
La cantidad de invitados puede ajustarse hasta {{config.lock_pax_days}} días antes del
evento. No se realizarán devoluciones por bajas informadas después de este plazo (costos de
materia prima ya ejecutados).
7. ACEPTACIÓN
Para confirmar la contratación de este servicio, por favor firmar al pie o hacer clic en el botón
de "Aceptar Propuesta" en la versión digital.
Firma Cliente: __________________________
Aclaración: _____________________________
Fecha: //2025
LeoCozina
Gerencia de Sistemas y Consultoría Gastronómica

