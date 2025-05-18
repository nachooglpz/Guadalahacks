import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
from shapely.ops import nearest_points
from rtree import index
import numpy as np

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

df_4815075 = merged_dict[4815075]
df_4815075
df_4815075.rename(columns = {"link_id_info": "LINK_ID"}, inplace= True)
df_4815075 = df_4815075[df_4815075["MULTIDIGIT"] == "Y"]
df_4815075[df_4815075["LINK_ID"] == 1296526969]
df_pois_4815075 = pois_dic[4815075]
prueba = df_4815075.merge(df_pois_4815075, on="LINK_ID", how="left")
prueba[prueba["LINK_ID"] == 702722866]


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

def validate_invalid_mdr(df_mm_sections):
    mdr_review_results = {}

    for sec, df in df_mm_sections.items():
        df_copy = df[df["POI_ID"].notna()].copy()

        # Inicializamos campos
        df_copy["MDR_STATUS"] = "Valid MDR"
        df_copy["FLAG_CAMELLON_REVIEW"] = False

        # Condiciones que invalidan un Multiply Digitised Road
        cond_frontage = df_copy["FRONTAGE"] == "Y"
        cond_structural = (
            (df_copy["BRIDGE"] == "Y") |
            (df_copy["TUNNEL"] == "Y") |
            (df_copy["RAMP"] == "Y")
        )

        cond_invalid_mdr = (df_copy["MULTIDIGIT"] == "Y") & (cond_frontage | cond_structural)

        # Marcamos los que no deben considerarse como MDR
        df_copy.loc[cond_invalid_mdr, "MDR_STATUS"] = "Invalid MDR"
        df_copy.loc[cond_invalid_mdr, "FLAG_CAMELLON_REVIEW"] = True

        mdr_review_results[sec] = df_copy

    return mdr_review_results

for sec, df in mdr_results.items():
    print(f"\nSección {sec} - Conteo de clasificación MDR:")
    print(df["MDR_STATUS"].value_counts())