"""Primera pantalla de Ferretería Don Nicola.

Esta interfaz reutiliza el parser de saludo.py. No reemplaza el programa
original: suma una forma más cómoda de usarlo.
"""

import tkinter as tk
from tkinter import ttk

from saludo import COLUMNAS, guardar_categoria_en_catalogo, guardar_csv, interpretar_anotacion


CATEGORIAS_DISPONIBLES = [
    "Electricidad e iluminación",
    "Gas y calefacción",
    "Sanitarios y plomería",
    "Pintura",
    "Seguridad industrial",
    "Herramientas y accesorios",
    "Construcción y albañilería",
    "Adhesivos, lubricantes y consumibles",
    "Productos de Jardinería",
    "Varios",
]


class AplicacionInventario:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Ferretería Don Nicola - Inventario")
        self.ventana.geometry("1080x760")
        self.ventana.minsize(800, 500)
        self.filas = []
        self.producto_a_clasificar = tk.StringVar()
        self.categoria_elegida = tk.StringVar()
        self.producto_para_precio = tk.StringVar()
        self.costo_producto = tk.StringVar()
        self.recargo_producto = tk.StringVar(value="40")
        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.ventana, padding=18)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Ferretería Don Nicola", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Pegá una anotación de inventario por línea y presioná Procesar inventario.",
        ).pack(anchor="w", pady=(0, 10))

        self.entrada = tk.Text(contenedor, height=8, font=("Segoe UI", 11), wrap="word")
        self.entrada.pack(fill="x")
        self.entrada.insert(
            "1.0",
            'Tanza 3 mm - cuadrada - 1 rollo\nCaño corrugado PVC - electricidad - 3/4 - 2 rollos',
        )

        acciones = ttk.Frame(contenedor)
        acciones.pack(fill="x", pady=10)
        ttk.Button(acciones, text="Procesar inventario", command=self.procesar_inventario).pack(side="left")
        ttk.Button(acciones, text="Limpiar", command=self.limpiar).pack(side="left", padx=(8, 0))

        tabla_contenedor = ttk.Frame(contenedor)
        tabla_contenedor.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(tabla_contenedor, columns=COLUMNAS, show="headings")
        for columna in COLUMNAS:
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=140, minwidth=90, stretch=True)

        barra_vertical = ttk.Scrollbar(tabla_contenedor, orient="vertical", command=self.tabla.yview)
        barra_horizontal = ttk.Scrollbar(tabla_contenedor, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        tabla_contenedor.rowconfigure(0, weight=1)
        tabla_contenedor.columnconfigure(0, weight=1)
        self.estado = ttk.Label(contenedor, text="Todavía no se procesó ningún inventario.")
        self.estado.pack(anchor="w", pady=(10, 0))

        clasificacion = ttk.LabelFrame(contenedor, text="Clasificar producto pendiente", padding=10)
        clasificacion.pack(fill="x", pady=(10, 0))
        ttk.Label(clasificacion, text="Producto sin categoría:").grid(row=0, column=0, sticky="w")
        self.selector_producto = ttk.Combobox(
            clasificacion, textvariable=self.producto_a_clasificar, state="readonly", width=32
        )
        self.selector_producto.grid(row=0, column=1, padx=8, sticky="ew")
        ttk.Label(clasificacion, text="Categoría:").grid(row=0, column=2, sticky="w")
        self.selector_categoria = ttk.Combobox(
            clasificacion,
            textvariable=self.categoria_elegida,
            values=CATEGORIAS_DISPONIBLES,
            state="readonly",
            width=32,
        )
        self.selector_categoria.grid(row=0, column=3, padx=8, sticky="ew")
        ttk.Button(clasificacion, text="Guardar categoría", command=self.guardar_categoria).grid(
            row=0, column=4, sticky="e"
        )
        clasificacion.columnconfigure(1, weight=1)
        clasificacion.columnconfigure(3, weight=1)

        precios = ttk.LabelFrame(contenedor, text="Calcular precio de venta", padding=10)
        precios.pack(fill="x", pady=(10, 0))
        ttk.Label(precios, text="Producto:").grid(row=0, column=0, sticky="w")
        self.selector_precio = ttk.Combobox(
            precios, textvariable=self.producto_para_precio, state="readonly", width=28
        )
        self.selector_precio.grid(row=0, column=1, padx=8, sticky="ew")
        ttk.Label(precios, text="Costo ($):").grid(row=0, column=2, sticky="w")
        ttk.Entry(precios, textvariable=self.costo_producto, width=14).grid(row=0, column=3, padx=8)
        ttk.Label(precios, text="Recargo (%):").grid(row=0, column=4, sticky="w")
        ttk.Entry(precios, textvariable=self.recargo_producto, width=8).grid(row=0, column=5, padx=8)
        ttk.Button(precios, text="Calcular", command=self.calcular_precio).grid(row=0, column=6)
        self.resultado_precio = ttk.Label(precios, text="Ingresá un costo para calcular el precio sugerido.")
        self.resultado_precio.grid(row=1, column=0, columnspan=7, pady=(8, 0), sticky="w")
        precios.columnconfigure(1, weight=1)

    def procesar_inventario(self):
        anotaciones = self.entrada.get("1.0", "end").strip().splitlines()
        self.filas = []
        for anotacion in anotaciones:
            anotacion = anotacion.strip()
            if not anotacion:
                continue
            resultado = interpretar_anotacion(anotacion)
            if isinstance(resultado, list):
                self.filas.extend(resultado)
            else:
                self.filas.append(resultado)

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for fila in self.filas:
            self.tabla.insert("", "end", values=[fila[columna] for columna in COLUMNAS])

        guardar_csv(self.filas)
        pendientes = sorted({fila["Producto"] for fila in self.filas if fila["Categoría"] == "Sin categoría"})
        self.selector_producto["values"] = pendientes
        self.producto_a_clasificar.set(pendientes[0] if pendientes else "")
        productos = sorted({fila["Producto"] for fila in self.filas})
        self.selector_precio["values"] = productos
        self.producto_para_precio.set(productos[0] if productos else "")
        cantidad = len(self.filas)
        self.estado.config(
            text=f"Se procesaron {cantidad} producto(s). El CSV se guardó automáticamente como inventario_organizado.csv."
        )

    def limpiar(self):
        self.entrada.delete("1.0", "end")
        self.filas = []
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.estado.config(text="Podés escribir nuevas anotaciones.")
        self.selector_producto["values"] = []
        self.producto_a_clasificar.set("")
        self.selector_precio["values"] = []
        self.producto_para_precio.set("")
        self.costo_producto.set("")
        self.resultado_precio.config(text="Ingresá un costo para calcular el precio sugerido.")

    def guardar_categoria(self):
        producto = self.producto_a_clasificar.get()
        categoria = self.categoria_elegida.get()
        if not producto or not categoria:
            self.estado.config(text="Elegí un producto pendiente y una categoría antes de guardar.")
            return

        guardar_categoria_en_catalogo(producto, categoria)
        self.procesar_inventario()
        self.categoria_elegida.set("")
        self.estado.config(f'"{producto}" quedó guardado en el catálogo como "{categoria}".')

    def calcular_precio(self):
        producto = self.producto_para_precio.get()
        try:
            costo = self.convertir_numero(self.costo_producto.get())
            recargo = self.convertir_numero(self.recargo_producto.get())
        except ValueError:
            self.resultado_precio.config(text="Ingresá números válidos para costo y recargo.")
            return

        if not producto or costo <= 0 or recargo < 0:
            self.resultado_precio.config(text="Elegí un producto e ingresá un costo positivo.")
            return

        precio_sugerido = round(costo * (1 + recargo / 100))
        self.resultado_precio.config(
            text=(
                f"{producto}: costo ${self.formatear_moneda(costo)} + {recargo:g}% "
                f"= precio sugerido ${self.formatear_moneda(precio_sugerido)}"
            )
        )

    @staticmethod
    def convertir_numero(texto):
        texto = texto.strip().replace("$", "").replace(" ", "")
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")
        return float(texto)

    @staticmethod
    def formatear_moneda(valor):
        return f"{valor:,.0f}".replace(",", ".")


if __name__ == "__main__":
    ventana = tk.Tk()
    AplicacionInventario(ventana)
    ventana.mainloop()
