import geopandas as gpd
import pandas as pd

seccions = [
    4815075, 4815078, 4815079, 4815081, 4815083, 4815084, 4815085, 4815086, 4815087,
    4815090, 4815091, 4815096, 4815097, 4815098, 4815099, 4815425, 4815428, 4815429,
    4815440, 4815441
]

# Dictionary to store the GeoDataFrames
street_info_dict = {}

for sec in seccions:
    geojson_file_path_street = rf'C:\Users\diego\OneDrive\Documentos\Tec\GDLHACKS\data\STREETS_NAV\SREETS_NAV_{sec}.geojson'
    try:
        street_info_dict[sec] = gpd.read_file(geojson_file_path_street)
    except Exception as e:
        print(f"Error reading file for section {sec}: {e}")

street_name_dict = {}

for sec in seccions:
    geojson_file_path_street_name = rf'C:\Users\diego\OneDrive\Documentos\Tec\GDLHACKS\data\STREETS_NAMING_ADDRESSING\SREETS_NAMING_ADDRESSING_{sec}.geojson'
    try:
        street_name_dict[sec] = gpd.read_file(geojson_file_path_street_name)
    except Exception as e:
        print(f"Error reading file for section {sec}: {e}")

merged_dict = {}

for sec in seccions:
    try:
        df_info = street_info_dict[sec]
        df_name = street_name_dict[sec]

        merged = df_info.merge(df_name, on='geometry', suffixes=('_info', '_name'))
        merged_dict[sec] = merged

    except Exception as e:
        print(f"Error merging section {sec}: {e}")

pois_dic = {}

for sec in seccions:
    try:
        pois_dic[sec] = pd.read_csv(rf'C:\Users\diego\OneDrive\Documentos\Tec\GDLHACKS\data\POIs\POI_{sec}.csv')
    except Exception as e:
        print(f"Error reading POI file for section {sec}: {e}")

pois_dic[4815075].columns

columns_pois = ["LINK_ID", "POI_ID", "FAC_TYPE", "POI_NAME", "POI_ST_NUM", "PERCFRREF"]
df_mm_sections = {}

for sec in seccions:
    try:
        # 1. we changed the link columns from the streets df so
        # we can merge with the POI data
        df_strets = merged_dict[sec].copy()
        df_strets.rename(columns={"link_id_info": "LINK_ID"}, inplace=True)

        # -> MULTIDIGIT STREETS DISTRIBUTION BEFORE FILTERING
        print(f"\n Seccion {sec} - MULTIDIGIT DISTRIBUTION BEFORE FILTERING")
        print(df_strets["MULTIDIGIT"].value_counts())

        # 2. we filter by only having multidigit streets
        df_strets = df_strets[df_strets["MULTIDIGIT"] == "Y"]

        # 3. we get only the deseareble columns in the POIs data
        df_pois = pois_dic[sec].copy()
        df_pois = df_pois[columns_pois]

        for col in ["LINK_ID", "POI_ID", "FAC_TYPE", "POI_ST_NUM"]:
            df_pois[col] = pd.to_numeric(df_pois[col], errors="coerce").astype("Int64")

        # we mantain the poi name column as string
        df_pois["POI_NAME"] = df_pois["POI_NAME"].astype(str)

        # 4. merge
        df_merge = df_strets.merge(df_pois, on="LINK_ID", how="left")

        # 6. save it on the final dicc
        df_mm_sections[sec] = df_merge

    except Exception as e:
        print(f"Error procesando sección {sec}: {e}")

def classify_non_existent_pois(df_mm_sections):
    non_existent_results = {}

    for sec, df in df_mm_sections.items():
        # Filtramos solo las filas con al menos un POI válido
        df_filtered = df[df["POI_ID"].notna()].copy()

        # Creamos columna vacía para la clasificación
        df_filtered["POI_STATUS"] = "Valid"
        df_filtered["MARKED_FOR_DELETION"] = False


        # Caso 1: ST_TYP_BEF ≠ ST_TYP_AFT
        cond_type_changed = df_filtered["ST_TYP_BEF"] != df_filtered["ST_TYP_AFT"]

        # Caso 2: MULTIDIGIT + (BRIDGE o TUNNEL o RAMP)
        cond_infra_issue = (
            (df_filtered["MULTIDIGIT"] == "Y") &
            (
                (df_filtered["BRIDGE"] == "Y") |
                (df_filtered["TUNNEL"] == "Y") |
                (df_filtered["RAMP"] == "Y")
            )
        )

        # Aplicamos ambas condiciones
        df_filtered.loc[cond_type_changed | cond_infra_issue, "POI_STATUS"] = "Non Existent POI"
        df_filtered.loc[cond_non_existent, "MARKED_FOR_DELETION"] = True

        # Guardamos resultados por sección
        non_existent_results[sec] = df_filtered

    return non_existent_results

classified_poi_dict = classify_non_existent_pois(df_mm_sections)

# Verificar resultados
for sec, df in classified_poi_dict.items():
    print(f"\nSección {sec} - Conteo de clasificaciones:")
    print(df["POI_STATUS"].value_counts())
