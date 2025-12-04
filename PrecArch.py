# Función para limpiar nombres
def limpiar_nombre(texto):
    if pd.isna(texto):
        return ""
    return str(texto).upper().replace('-', '').replace(' ', '').strip()
