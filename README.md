# Organizador de inventario de ferretería

## Proceso real de trabajo elegido

Elegí el proceso de **organización y normalización de pedidos de materiales de ferretería** para preparar un inventario o una futura solicitud de compra.

En este contexto, las anotaciones suelen hacerse de forma informal, por ejemplo en un cuaderno o por mensaje. Una misma anotación puede incluir el producto, su medida, variante y cantidad, pero no siempre de forma ordenada o completa. Antes de preparar un inventario o consultar precios, hace falta transformar esas notas en datos claros y revisables.

El objetivo del proceso es convertir un conjunto de anotaciones informales en un inventario estructurado, detectar la información faltante y dejar preparado el material para una revisión humana y, en futuras etapas, para consultas a proveedores o una solicitud de compra.

## Descomposición del proceso y delegación a agentes

| Tarea | ¿Es delegable a un agente? | Herramientas posibles | Nivel de delegación | Justificación y aprobación humana |
|---|---|---|---|---|
| Relevar los productos físicos y tomar anotaciones | Parcialmente | Celular, cámara, planilla y asistente de IA | L2 | El agente puede ayudar a registrar u ordenar notas, pero una persona debe confirmar que el producto existe, su estado y su cantidad real. |
| Transformar anotaciones informales en registros ordenados | Sí | Python, reglas de procesamiento, CSV o planilla | L3 | Es una tarea repetitiva y verificable. El agente puede procesar las notas, pero el humano revisa excepciones o casos ambiguos. |
| Detectar información faltante | Sí | Python, reglas de validación y asistente de IA | L3 | El agente puede marcar campos sin medida, cantidad, unidad o variante. El humano debe completar o confirmar esos datos. |
| Identificar posibles proveedores | Sí, en una etapa futura | Búsqueda web, catálogos y correo electrónico | L3 | El agente puede reunir opciones, pero el humano decide cuáles son confiables y cuáles conviene contactar. |
| Consultar precios | Parcialmente | Sitios web, catálogos, correo o mensajería | L2 | El agente puede reunir precios publicados, pero una persona debe validar que correspondan exactamente al producto y a sus condiciones de venta. |
| Comparar precios y condiciones | Sí | Planilla, Python o asistente de IA | L3 | El agente puede ordenar precios, fechas, cantidades mínimas y condiciones. El humano revisa que la comparación sea válida. |
| Proponer un precio de venta o presupuesto | Parcialmente | Planilla y asistente de IA | L2 | El agente puede calcular o sugerir rangos, pero la decisión comercial final debe ser humana. |
| Decidir cómo y dónde vender o comprar | No completamente | IA como asistente, planilla y experiencia del negocio | L1-L2 | Depende de contexto comercial, confianza, urgencia y responsabilidad económica. La persona toma la decisión. |
| Preparar el inventario o solicitud de compra final | Sí, con supervisión | Python, CSV, Excel o planilla | L3 | El agente puede preparar el documento, pero el humano realiza la revisión y aprobación final antes de usarlo. |

## Niveles de delegación L0-L4

- **L0 — Sin delegación:** la tarea la realiza completamente una persona.
- **L1 — Asistencia:** la IA aporta ideas o información, pero la persona ejecuta la tarea.
- **L2 — Copiloto:** la IA realiza una parte importante del trabajo y propone resultados; el humano revisa y decide.
- **L3 — Delegación supervisada:** el agente puede ejecutar casi todo el flujo, con puntos definidos de validación humana.
- **L4 — Autonomía:** el agente ejecuta el proceso completo sin intervención humana.

En este proyecto no considero adecuado usar L4 para decisiones de proveedores, precios o venta. Aunque un agente puede agilizar el trabajo operativo, las decisiones económicas deben conservar una aprobación humana.

## Human in the loop

El concepto de **human in the loop** significa que una persona se mantiene dentro del proceso de decisión y validación.

En este caso, el agente puede ordenar información, detectar datos faltantes y preparar comparaciones. Sin embargo, el humano debe:

- Confirmar que los productos y cantidades sean correctos.
- Resolver anotaciones ambiguas.
- Validar proveedores y precios.
- Aprobar cualquier presupuesto, compra o precio de venta.
- Dar la aprobación final del inventario.

De esta manera, la IA ayuda a reducir trabajo repetitivo, pero no reemplaza el criterio ni la responsabilidad de la persona.

## Qué construí

Construí un programa simple en Python que toma anotaciones informales de productos de ferretería y las transforma en datos ordenados. El programa detecta producto, medida, variante, cantidad y unidad, y deja proveedor e información faltante como campos pendientes.

Este programa representa una primera implementación de la tarea “transformar anotaciones informales en un inventario estructurado”, que en la tabla anterior se puede delegar en nivel L3 con revisión humana.

Como evidencia del proyecto, el repositorio incluye el archivo `inventario_organizado.csv` con un ejemplo de inventario ordenado.

## Cómo se lo pedí

Estos fueron los principales prompts que utilicé, en el orden en que los fui usando:

> Quiero construir un pequeño programa en Python para organizar un inventario de productos de ferretería.
>
> Soy principiante total en programación, así que explicame qué vas haciendo paso a paso.
>
> El programa debe recibir anotaciones de productos escritas de forma informal, por ejemplo:
>
> Tanza 3 mm - cuadrada  
> Tanza 2 1/2 mm - redonda  
> Manguera plana 3" tipo manga  
> Caño corrugado PVC - electricidad - 3/4
>
> y transformarlas en datos ordenados con estas columnas:
>
> - Producto
> - Medida
> - Variante
> - Cantidad
> - Unidad
> - Proveedor a consultar
> - Información faltante
>
> Por ahora NO quiero buscar precios reales en Internet. Quiero primero lograr que el programa pueda tomar las anotaciones y generar una lista ordenada.
>
> Creá una primera versión muy simple y explicame qué estás haciendo. No hagas cambios adicionales sin explicármelo.

> Quiero mejorar el programa.
>
> Ahora también quiero que pueda detectar la cantidad y la unidad cuando aparecen en la anotación.
>
> Por ejemplo:
>
> "Caño corrugado PVC 3/4 - 2 rollos"
>
> debería producir:
>
> Producto: Caño corrugado PVC  
> Medida: 3/4  
> Cantidad: 2  
> Unidad: rollos
>
> Y:
>
> "Manguera plana 3 pulgadas tipo manga - 1 rollo"
>
> debería producir:
>
> Producto: Manguera plana  
> Medida: 3"  
> Variante: tipo manga  
> Cantidad: 1  
> Unidad: rollo
>
> No agregues todavía búsqueda de precios ni proveedores. Quiero modificar solamente esta parte y probarla con ejemplos. Explicame qué cambiaste antes de hacer otras modificaciones.

## Ejemplo de transformación

Anotación informal:

`Tanza 2 1/2 mm - redonda`

Resultado esperado:

| Producto | Medida | Variante | Cantidad | Unidad |
|---|---|---|---:|---|
| Tanza | 2 1/2 mm | redonda | 1 | rollo |

## Qué funciona

Probé el programa con ejemplos reales de inventario:

- Tanza 3 mm - cuadrada - 1 rollo
- Tanza 2 1/2 mm - redonda - 1 rollo
- Manguera plana 3" tipo manga - 1 rollo
- Caño corrugado PVC - electricidad - 3/4 - 2 rollos

El programa detectó correctamente el producto, la medida, la variante, la cantidad y la unidad.

El programa se ejecuta correctamente en Python 3.13 y fue probado desde VS Code.

## Qué falta o qué falló

El programa todavía no busca precios reales, no consulta proveedores automáticamente y todavía no guarda el inventario en Excel.

Durante las pruebas hubo que corregir el reconocimiento de medidas como `3/4` y agregar el reconocimiento de cantidades y unidades como `2 rollos`.

## Qué queda para futuras etapas

En una futura etapa, el proyecto podría incorporar:

- Procesamiento de un listado completo de anotaciones de una sola vez.
- Exportación del inventario a Excel.
- Identificación de proveedores potenciales.
- Consulta y comparación de precios.
- Propuestas de presupuesto o precio de venta.

Estas etapas requerirían nuevas herramientas y controles humanos. No forman parte de la versión actual del programa.

## Qué aprendí

Aprendí que no alcanza con pedirle a un agente que genere código: también hay que probarlo, detectar errores, pedir correcciones específicas y volver a probar.

También aprendí que puedo usar IA para transformar un problema cotidiano en un pequeño programa funcional, aunque sea principiante en Python.

La principal conclusión es que no todas las tareas deben automatizarse al máximo nivel. El agente puede encargarse del trabajo repetitivo y estructurable, mientras que las decisiones comerciales y las aprobaciones finales deben permanecer bajo responsabilidad humana.
