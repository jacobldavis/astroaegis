# pip install rasterio geopandas shapely pydeck numpy
import rasterio, numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import pydeck as pdk

# Read raster
fp = "landscan-global-2023-colorized.tif"
with rasterio.open(fp) as src:
    arr = src.read(1, masked=True)
    transform = src.transform
    height, width = arr.shape

# Build coarse grid (e.g., every Nth cell -> reduce data)
step = 10  # aggregate factor; increase for speed
polys = []
vals = []
for i in range(0, height, step):
    for j in range(0, width, step):
        block = arr[i:i+step, j:j+step]
        if np.ma.count(block) == 0: 
            continue
        pop = float(np.ma.mean(block))  # or sum
        # get polygon bounds
        x1, y1 = rasterio.transform.xy(transform, i, j, offset='ul')
        x2, y2 = rasterio.transform.xy(transform, i+step, j+step, offset='lr')
        poly = Polygon([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])
        polys.append(poly)
        vals.append(pop)

gdf = gpd.GeoDataFrame({'population': vals, 'geometry': polys}, crs=src.crs)

# convert to lat/lon if needed
gdf = gdf.to_crs(epsg=4326)

# Convert to records for pydeck (centroid + population as height)
records = []
for _, row in gdf.iterrows():
    lon, lat = row.geometry.centroid.x, row.geometry.centroid.y
    records.append({'lon': lon, 'lat': lat, 'height': float(row.population)})

layer = pdk.Layer(
    "ColumnLayer",
    data=records,
    get_position=["lon","lat"],
    get_elevation="height",
    elevation_scale=100,   # tune to reasonable look
    radius=3000,           # meter radius
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1, pitch=45)
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html("population_extruded.html")
