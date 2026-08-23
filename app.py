"""Primera pantalla de Ferretería Don Nicola.

Esta interfaz reutiliza el parser de saludo.py. No reemplaza el programa
original: suma una forma más cómoda de usarlo.
"""

import tkinter as tk
from tkinter import ttk

from saludo import COLUMNAS, guardar_csv, interpretar_anotacion


class AplicacionInventario:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Ferretería Don Nicola - Inventario")
        self.ventana.geometry("1080x650")
        self.ventana.minsize(800, 500)
        self.filas = []
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


if __name__ == "__main__":
    ventana = tk.Tk()
    AplicacionInventario(ventana)
    ventana.mainloop()
