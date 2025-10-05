import pandas as pd
import geopandas as gpd
from owslib.wfs import WebFeatureService
import io
import time
import os

# --- 1. Setup ---
# Create a directory to store the output checkpoint files
output_folder = 'output_checkpoints2'
os.makedirs(output_folder, exist_ok=True)

# WFS Connection details
wfs_url = 'https://mapsref.brgm.fr/wxs/1GG/CGMW_Bedrock_and_Structural_Geology'
print(f"Connecting to WFS server at: {wfs_url}")

try:
    # Initialize the WFS client and get a valid output format
    wfs = WebFeatureService(url=wfs_url, version='2.0.0')
    layer_name = 'ms:World_CGMW_50M_GeologicalUnitsOnshore'
    get_feature_op = wfs.getOperationByName('GetFeature')
    supported_formats = get_feature_op.parameters['outputFormat']['values']
    output_format = next((fmt for fmt in supported_formats if 'gml' in fmt.lower()), None)
    
    if not output_format:
        raise ValueError("No suitable GML format found.")
    
    print(f"✅ Connection successful. Using layer '{layer_name}'.")

except Exception as e:
    print(f"Failed to connect or set up WFS. Error: {e}")
    exit()

# --- 2. Define Continental Bounding Boxes [min_lon, min_lat, max_lon, max_lat] ---
# --- THIS IS THE UPDATED SECTION ---
continents = {
    "North_America": (-170, 5, -50, 85),
    "South_America": (-85, -55, -30, 15),
    "Africa": (-20, -35, 55, 38),
    "Eurasia": (-10, 0, 180, 80),
    "Australia": (110, -45, 155, -10)
}

# --- 3. Tiling and Downloading with Checkpoints ---
step = 15  # Tile size in degrees
print("\nStarting targeted bulk download...")

for continent, bbox in continents.items():
    print(f"\n--- Processing {continent} ---")
    min_lon, min_lat, max_lon, max_lat = bbox
    continent_gdfs = []  # List to hold all the data tiles for this continent
    
    # Loop through the grid for the current continent
    for lon in range(min_lon, max_lon, step):
        for lat in range(min_lat, max_lat, step):
            tile_bbox = (lon, lat, lon + step, lat + step)
            print(f"  Requesting tile: {tile_bbox}...")
            
            try:
                # Request the data for one tile
                response = wfs.getfeature(typename=layer_name, bbox=tile_bbox, outputFormat=output_format)
                tile_gdf = gpd.read_file(io.BytesIO(response.read()))

                # If the tile has data, add it to our list for this continent
                if not tile_gdf.empty:
                    continent_gdfs.append(tile_gdf)
            except Exception as e:
                print(f"    --> Warning: Could not process tile. Error: {e}")
            
            # Be polite to the server
            time.sleep(1)

    # --- CHECKPOINT STEP: Save the raw data for this continent ---
    if continent_gdfs:
        print(f"  Combining tiles for {continent}...")
        
        # Combine all the downloaded tiles into a single GeoDataFrame
        continent_full_gdf = pd.concat(continent_gdfs, ignore_index=True)
        
        # Define the output filename for the checkpoint
        checkpoint_filename = os.path.join(output_folder, f'{continent}_geology.geojson')
        
        # Save the full, raw geographic data to the file
        continent_full_gdf.to_file(checkpoint_filename, driver='GeoJSON')
        
        print(f"  ✅ Checkpoint saved: {checkpoint_filename} ({len(continent_full_gdf)} features)")
    else:
        print(f"  No data was downloaded for {continent}.")

print("\n✅ All tasks complete!")