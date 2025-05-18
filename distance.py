import pandas as pd

# Función que redimensiona a metros
prueba = prueba.to_crs(epsg=32614)

def calcular_ancho_camellon(df, parallel_links):
    resultados = []
    for item in parallel_links:
        # Busca las filas correspondientes a cada LINK_ID
        row1 = df[df["LINK_ID"] == item["LINK_ID_1"]].iloc[0]
        row2 = df[df["LINK_ID"] == item["LINK_ID_2"]].iloc[0]
        
        # Calcula el ancho total de la calle para cada LINK_ID
        ancho1 = (row1["TO_LANES"] + row1["FROM_LANES"]) * 2.5
        ancho2 = (row2["TO_LANES"] + row2["FROM_LANES"]) * 2.5
        
        # Usa el mayor ancho (o el promedio, según tu criterio)
        ancho_calle = max(ancho1, ancho2)
        
        # Calcula el ancho del camellón
        ancho_camellon = item["distance"] - ancho_calle
        
        resultados.append({
            "LINK_ID_1": item["LINK_ID_1"],
            "LINK_ID_2": item["LINK_ID_2"],
            "distance": item["distance"],
            "ancho_calle": ancho_calle,
            "ancho_camellon": ancho_camellon
        })
    return pd.DataFrame(resultados)

# Uso:
df_camellon = calcular_ancho_camellon(prueba, parallel_links_with_distances)
print(df_camellon.head(10))
