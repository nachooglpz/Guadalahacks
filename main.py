import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image

gdf = gpd.read_file("./STREETS_NAV/SREETS_NAV_4815441.geojson")
gdf = gdf.to_crs(epsg=4326)
minx, miny, maxx, maxy = gdf.total_bounds  # [left, bottom, right, top]
sat_image = Image.open("./docs/satellite_tile.png")
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(sat_image, extent=[minx, maxx, miny, maxy], aspect='equal')
gdf.plot(ax=ax, linewidth=0.8, color='blue')
ax.set_axis_off()

plt.tight_layout()
plt.show()

'''''
csv_df = pd.read_csv("./POIs/POI_4815441.csv")
geo_link_ids = gdf["link_id"].dropna().astype(int).unique()
csv_link_ids = csv_df["LINK_ID"].dropna().astype(int).unique()
missing_link_ids = set(csv_link_ids) - set(geo_link_ids)

print(f"LINK_IDs en el CSV que NO están en el GeoJSON: {missing_link_ids}")
print(f"Total faltantes: {len(missing_link_ids)}")
print(csv_df.columns)
'''''