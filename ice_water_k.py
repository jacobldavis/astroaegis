import pandas as pd
import geopandas as gpd
import numpy as np
import os
from shapely.geometry import Point, Polygon

# --- 1. Setup ---
output_folder = 'k_value_outputs2'
os.makedirs(output_folder, exist_ok=True)
K_ICE = 0.03
K_ICELAND = 0.0005 # K-value for Iceland as requested
K_WATER = 0.0003
spacing = 2.0  # Spacing in degrees.

def generate_points_in_shape(shape, spacing, k_value, description):
    """Generates a grid of points that fall within a given geographic shape."""
    points = []
    min_lon, min_lat, max_lon, max_lat = shape.bounds
    
    lon_coords = np.arange(min_lon, max_lon, spacing)
    lat_coords = np.arange(min_lat, max_lat, spacing)
    grid_points = [Point(lon, lat) for lon in lon_coords for lat in lat_coords]
    
    valid_points = [p for p in grid_points if shape.contains(p)]
    
    for point in valid_points:
        points.append({
            'latitude': point.y,
            'longitude': point.x,
            'k_value': k_value,
            'description': description
        })
    return pd.DataFrame(points)

print("Loading world map data for accurate shapes...")
try:
    world = gpd.read_file("countries/ne_110m_admin_0_countries.shp")
    print("✅ Successfully loaded local world map file.")
except Exception as e:
    print(f"Fatal Error: Could not read 'ne_110m_admin_0_countries.shp'. Error: {e}")
    exit()

# --- 2. Generate Data for Greenland ---
print("\n--- Processing Greenland ---")
try:
    greenland_shape = world[world.ADMIN == 'Greenland'].geometry.iloc[0]
    df_greenland = generate_points_in_shape(greenland_shape, spacing, K_ICE, 'Ice Sheet')
    
    greenland_filename = os.path.join(output_folder, 'Greenland_k_values.csv')
    df_greenland.to_csv(greenland_filename, index=False)
    print(f"✅ Generated {len(df_greenland)} points. Saved to '{greenland_filename}'")
except (IndexError, KeyError):
    print("Could not find Greenland in the world map data.")

# --- NEW: GENERATE DATA FOR ICELAND ---
print("\n--- Processing Iceland ---")
try:
    # Select the shape for Iceland using its ADMIN name
    iceland_shape = world[world.ADMIN == 'Iceland'].geometry.iloc[0]
    
    # Generate points within Iceland's shape
    df_iceland = generate_points_in_shape(iceland_shape, spacing, K_ICELAND, 'Iceland')
    
    # Save the data to a new CSV file
    iceland_filename = os.path.join(output_folder, 'Iceland_k_values.csv')
    df_iceland.to_csv(iceland_filename, index=False)
    print(f"✅ Generated {len(df_iceland)} points. Saved to '{iceland_filename}'")
except (IndexError, KeyError):
    print("Could not find Iceland in the world map data.")

# --- 3. Generate Data for Antarctica ---
print("\n--- Processing Antarctica ---")
try:
    antarctica_shape = world[world.ADMIN == 'Antarctica'].geometry.iloc[0]
    df_antarctica = generate_points_in_shape(antarctica_shape, spacing, K_ICE, 'Ice Sheet')
    
    antarctica_filename = os.path.join(output_folder, 'Antarctica_k_values.csv')
    df_antarctica.to_csv(antarctica_filename, index=False)
    print(f"✅ Generated {len(df_antarctica)} points. Saved to '{antarctica_filename}'")
except (IndexError, KeyError):
    print("Could not find Antarctica in the world map data.")

# --- 4. Generate Data for Oceans ---
print("\n--- Processing Oceans (this may take a few minutes)... ---")
try:
    world_box = Polygon([(-180, -90), (180, -90), (180, 90), (-180, 90)])
    land_union = world.unary_union
    ocean_shape = world_box.difference(land_union)
    
    df_ocean = generate_points_in_shape(ocean_shape, spacing * 1.5, K_WATER, 'Ocean')

    ocean_filename = os.path.join(output_folder, 'Oceans_k_values.csv')
    df_ocean.to_csv(ocean_filename, index=False)
    print(f"✅ Generated {len(df_ocean)} points. Saved to '{ocean_filename}'")
except Exception as e:
    print(f"An error occurred while generating ocean data: {e}")

print("\n✅ All tasks complete!")