# Organizador de inventario de ferretería

## Qué construí
Construí un programa simple en Python que toma anotaciones informales de productos de ferretería y las transforma en datos ordenados. El programa detecta producto, medida, variante, cantidad y unidad, y deja proveedor e información faltante como campos pendientes.

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
> Por ahora NO quiero buscar precios reales en Internet.
> Quiero primero lograr que el programa pueda tomar las anotaciones y generar una lista ordenada.
>
> Creá una primera versión muy simple y explicame qué estás haciendo.
> No hagas cambios adicionales sin explicármelo.

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
> No agregues todavía búsqueda de precios ni proveedores.
> Quiero modificar solamente esta parte y probarla con ejemplos.
> Explicame qué cambiaste antes de hacer otras modificaciones.

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

Durante las pruebas hubo que corregir el reconocimiento de medidas como 3/4 y agregar el reconocimiento de cantidades y unidades como "2 rollos".

## Qué aprendí
Aprendí que no alcanza con pedirle a un agente que genere código: también hay que probarlo, detectar errores, pedir correcciones específicas y volver a probar.

También aprendí que puedo usar IA para transformar un problema cotidiano en un pequeño programa funcional, aunque sea principiante en Python.
