import re
import csv 


COLUMNAS = [
    "Producto",
    "Medida",
    "Variante",
    "Cantidad",
    "Unidad",
    "Proveedor a consultar",
    "Información faltante",
]


def encontrar_medida(texto):
    """Busca una medida simple, como 3 mm, 3\" o 3/4."""
    patron = r"(?:\d+(?:\s+\d+/\d+)?\s*(?:mm|cm|m|[\"'])|\d+/\d+)"
    resultado = re.search(patron, texto, re.IGNORECASE)

    if resultado is None:
        return ""

    return resultado.group(0).strip()


def interpretar_anotacion(anotacion):
    """Convierte una anotación informal en una fila ordenada."""
    coincidencia_variantes = re.search(
        r"^(.*?)\s*\(\s*(\d+)\s+([a-záéíóúñ]+)\s+y\s+(\d+)\s+([a-záéíóúñ]+)\s*\)$",
        anotacion,
        re.IGNORECASE,
    )

    if coincidencia_variantes:
        producto = coincidencia_variantes.group(1).strip()
        filas = []
        for cantidad, variante in (
            (coincidencia_variantes.group(2), coincidencia_variantes.group(3)),
            (coincidencia_variantes.group(4), coincidencia_variantes.group(5)),
        ):
            filas.append(
                {
                    "Producto": producto,
                    "Medida": "Sin medida",
                    "Variante": variante,
                    "Cantidad": int(cantidad),
                    "Unidad": "unidad",
                    "Proveedor a consultar": "Pendiente",
                    "Información faltante": "Confirmar cantidad y proveedor",
                }
            )
        return filas

    coincidencia_cantidad = re.search(
        r"\((\d+)(?:\s+([a-záéíóúñ]+))?\)\s*$",
        anotacion,
        re.IGNORECASE,
    )

    if coincidencia_cantidad:
        cantidad = int(coincidencia_cantidad.group(1))
        unidad = coincidencia_cantidad.group(2) or "unidad"
        anotacion_sin_cantidad = anotacion[:coincidencia_cantidad.start()].strip()
    else:
        cantidad = 1
        unidad = "unidad"
        anotacion_sin_cantidad = anotacion

    partes = [parte.strip() for parte in anotacion_sin_cantidad.split("-") if parte.strip()]
    coincidencia = re.search(
        r"(?:\d+(?:\s+\d+/\d+)?\s*(?:mm|cm|m|pulgadas?|[\"'])|\d+/\d+)",
        anotacion_sin_cantidad,
        re.IGNORECASE,
    )
    raw_medida = coincidencia.group(0).strip() if coincidencia else ""
    medida = re.sub(r"\s*pulgadas?\s*$", '"', raw_medida, flags=re.IGNORECASE)

    producto = partes[0] if partes else anotacion.strip()
    texto_despues_de_medida = ""
    if coincidencia and partes and raw_medida in partes[0]:
        posicion_medida = partes[0].find(raw_medida)
        producto = partes[0][:posicion_medida].strip()
        texto_despues_de_medida = partes[0][posicion_medida + len(raw_medida):].strip()

    variantes = [variante for variante in partes[1:] if variante not in (raw_medida, medida)]
    if texto_despues_de_medida and len(partes) == 1:
        variantes.append(texto_despues_de_medida)
    variante = " - ".join(variantes)

    return {
        "Producto": producto,
        "Medida": medida or "Sin medida",
        "Variante": variante or "Sin variante",
        "Cantidad": cantidad,
        "Unidad": unidad,
        "Proveedor a consultar": "Pendiente",
        "Información faltante": "Confirmar cantidad y proveedor",
    }


def mostrar_tabla(filas):
    """Muestra las filas con las columnas alineadas."""
    anchos = {
        columna: max(len(columna), *(len(str(fila[columna])) for fila in filas))
        for columna in COLUMNAS
    }

    encabezado = " | ".join(columna.ljust(anchos[columna]) for columna in COLUMNAS)
    separador = "-+-".join("-" * anchos[columna] for columna in COLUMNAS)

    print("\n" + encabezado)
    print(separador)

    for fila in filas:
        print(" | ".join(str(fila[columna]).ljust(anchos[columna]) for columna in COLUMNAS))

def guardar_csv(filas):
    filas_para_csv = []
    for fila in filas:
        fila_csv = fila.copy()
        if fila_csv["Medida"] != "Sin medida":
            fila_csv["Medida"] = f'="{fila_csv["Medida"]}"'
        filas_para_csv.append(fila_csv)

    with open("inventario_organizado.csv", "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS, delimiter=";")
        escritor.writeheader()
        escritor.writerows(filas_para_csv)


def es_comando_de_ejecucion(texto):
    """Evita guardar como producto las líneas que muestra la terminal."""
    texto_normalizado = texto.lower().replace("/", "\\")
    return (
        "python.exe" in texto_normalizado
        or "python " in texto_normalizado
        or "saludo.py" in texto_normalizado
        or texto_normalizado.startswith("c:\\users\\")
    )


def main():
    print("Escribí una anotación por línea.")
    print("Cuando termines, presioná Enter en una línea vacía.\n")

    filas = []
    while True:
        anotacion = input("> ").strip()

        if not anotacion:
            break

        if es_comando_de_ejecucion(anotacion):
            print("Esa línea es un comando de la terminal y no se guardó.")
            continue

        resultado = interpretar_anotacion(anotacion)
        if isinstance(resultado, list):
            filas.extend(resultado)
        else:
            filas.append(resultado)

    guardar_csv(filas)

    if filas:
        mostrar_tabla(filas)
        print("\nInventario guardado en inventario_organizado.csv")
    else:
        print("No se ingresaron productos. Se creó un CSV vacío con los encabezados.")


if __name__ == "__main__":
    main()
