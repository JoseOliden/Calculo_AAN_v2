# Funciones para el procesamiento de RPT

def limpiar(valor):
  if isinstance(valor, str):
    # 1. quitar un solo espacio inicial si existe
    if valor.startswith(" "):
      valor = valor[1:]
  # 2. quitar espacios al final completamente
  valor = valor.rstrip()
  return valor

rpt_file = files.upload()  # Subir archivo .RPT
def procesar_RPT(rpt_file):
  # Usa : limpiar
  if rpt_file is not None:

    filename, data = next(iter(rpt_file.items()))
    # 1. Leer archivo desde buffer sin guardarlo
    contenido = data.decode("utf-8", errors="ignore")  # ya no uses .read()
    #contenido = rpt_file.read().decode("utf-8", errors="ignore")

    # Convertir a pandas como una línea por fila
    lineas = contenido.splitlines(keepends=True)  # conserva saltos de línea
    df = pd.DataFrame(lineas, columns=["linea"])

    # 2. Eliminar primeras 20 filas
    df = df.iloc[19:].reset_index(drop=True)

    # 3. Crear columna auxiliar
    df["sin_espacios"] = df["linea"].str.lstrip()

    # 4. Eliminar líneas según patrones
    patrones_excluir = ("Peak", "M =", "m =", "F =", "Error")
    df = df[~df["sin_espacios"].str.startswith(patrones_excluir)]

    # 5. Eliminar si empieza con 2 espacios exactos
    df = df[~df["linea"].str.startswith("  ")]

    # 6. Guardar sin columna auxiliar
    df = df.drop(columns=["sin_espacios"])

    # Eliminar líneas vacías (solo saltos de línea, espacios o tabs)
    df = df[~df["linea"].str.strip().eq("")]

    # Reinicia los indices
    df = df.reset_index(drop=True)

    # Limpia los espacios en blanco al inicio y final
    df = df.applymap(limpiar)

    # Separa y nombra columnas
    df_tab = df["linea"].str.split(r"\s+", expand=True)
    df_tab.columns = ["Tipo", "Peak No.", "ROI Start", "ROI End", "Peak Centroid",
                      "Energy (keV)", "Net Peak Area", "Net Peak Uncert", 
                      "Continuum Counts", "Tentative Nuclie"]

    # Generar texto procesado
    salida_texto = "".join(df["linea"].tolist())
    
    st.success("Archivo procesado correctamente")
    return df_tab
