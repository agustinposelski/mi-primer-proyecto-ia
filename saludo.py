import re


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
	coincidencia_cantidad = re.search(
		r"-\s*(\d+)\s+([a-záéíóúüñ]+)\s*$",
		anotacion,
		re.IGNORECASE,
	)

	if coincidencia_cantidad:
		cantidad = int(coincidencia_cantidad.group(1))
		unidad = coincidencia_cantidad.group(2)
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


def main():
	print("Escribí una anotación por línea.")
	print("Cuando termines, presioná Enter en una línea vacía.\n")

	filas = []
	while True:
		anotacion = input("> ").strip()

		if not anotacion:
			break

		filas.append(interpretar_anotacion(anotacion))

	if filas:
		mostrar_tabla(filas)
	else:
		print("No se ingresaron productos.")


if __name__ == "__main__":
	main()