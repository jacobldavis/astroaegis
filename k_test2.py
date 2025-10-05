import pandas as pd
import numpy as np
import json
import math
import os
from scipy.spatial import KDTree
from tqdm import tqdm

# --- 1. CONFIGURATION ---
CSV_FILE = "global_complete_k_values.csv"
OUTPUT_FILE = "tile_k_values_cache.json"
TILE_SIZE = (3, 3)
END_POS = (3085, 1542)
RADIUS_KM = 20.0
K_VALUE_SIMILARITY_THRESHOLD = 2e-4

# --- 2. HELPER FUNCTIONS ---
def latlon_to_xyz(lat, lon):
    """Convert latitude and longitude to 3D Cartesian coordinates."""
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return x, y, z

def haversine_distance(lon1, lat1, lon2, lat2):
    """Calculate the great-circle distance in kilometers."""
    R = 6371
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# --- 3. LOAD DATA AND BUILD KD-TREE (RUNS ONCE) ---
print(f"Loading data from '{CSV_FILE}'...")
if not os.path.exists(CSV_FILE):
    print(f"\nFatal Error: Data file not found at '{CSV_FILE}'.")
    exit()

df = pd.read_csv(CSV_FILE)
df.dropna(subset=['latitude', 'longitude', 'k_value'], inplace=True)

# Convert lat/lon to XYZ for the KDTree
xyz = np.array(latlon_to_xyz(df['latitude'], df['longitude'])).T
tree = KDTree(xyz)
print(f"✅ Data loaded and indexed. Ready to query {len(df)} points.")

# --- 4. FAST QUERY FUNCTION ---
def find_k_and_relevant_description(lat, lon):
    try:
        # Convert query point to XYZ and find the nearest neighbor in the tree
        query_xyz = latlon_to_xyz(lat, lon)
        dist, nearest_index = tree.query(query_xyz, k=1)
        nearest_point_for_k = df.iloc[nearest_index]
        final_description = nearest_point_for_k['description']

        # For radius search, we find the 50 nearest neighbors and then filter by actual distance
        distances, indices = tree.query(query_xyz, k=50)
        potential_neighbors = df.iloc[indices]
        
        # Calculate precise Haversine distance for this small subset
        actual_distances = haversine_distance(lon, lat, potential_neighbors['longitude'], potential_neighbors['latitude'])
        
        nearby_points_df = potential_neighbors[actual_distances <= RADIUS_KM]
        
        if not nearby_points_df.empty:
            detailed_points_df = nearby_points_df[nearby_points_df['description'] != 'Interpolated']
            if not detailed_points_df.empty:
                # Find the closest point within the detailed subset by distance
                closest_detailed_point = detailed_points_df.loc[actual_distances.loc[detailed_points_df.index].idxmin()]
                
                k_value_main = nearest_point_for_k['k_value']
                k_value_detailed = closest_detailed_point['k_value']

                if abs(k_value_main - k_value_detailed) <= K_VALUE_SIMILARITY_THRESHOLD:
                    final_description = closest_detailed_point['description']
                else:
                    final_description = f"Nearest detailed point is geologically different (k-value: {k_value_detailed:.5f})"

        if final_description == 'Interpolated':
            final_description = None
        return nearest_point_for_k, final_description

    except Exception as e:
        return None, "Error during search."

# --- 5. PRECOMPUTATION FUNCTION WITH PROGRESS BAR ---
def precompute_tile_k_values():
    tile_grid_size = (math.ceil(END_POS[0] / TILE_SIZE[0]), math.ceil(END_POS[1] / TILE_SIZE[1]))
    total_tiles = tile_grid_size[0] * tile_grid_size[1]
    print(f"\nPrecomputing k-values for {total_tiles} tiles...")
    
    tile_k_values = {}
    
    # Create a single loop and wrap it with tqdm for a continuous progress bar
    for i in tqdm(range(total_tiles), desc="Processing Tiles"):
        tile_x = i % tile_grid_size[0]
        tile_y = i // tile_grid_size[0]

        pixel_x = tile_x * TILE_SIZE[0] + TILE_SIZE[0] / 2.0
        pixel_y = tile_y * TILE_SIZE[1] + TILE_SIZE[1] / 2.0
        
        lat = 90.0 * 2.0 * (pixel_y / END_POS[1] - 0.5)
        lon = 180.0 * 2.0 * (pixel_x / END_POS[0] - 0.5)
        
        nearest_point, description = find_k_and_relevant_description(lat, lon)
        
        key = f"{tile_x},{tile_y}"
        tile_k_values[key] = {
            "k_value": nearest_point["k_value"] if nearest_point is not None else 0.0
        }
            
    print("Precomputation complete!")
    return tile_k_values

# --- 6. MAIN EXECUTION ---
def main():
    tile_k_values = precompute_tile_k_values()
    
    print(f"\nSaving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(tile_k_values, f)
    
    print(f"Successfully saved {len(tile_k_values)} tiles.")

if __name__ == "__main__":
    main()