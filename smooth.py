import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
import glob
import os
from scipy.interpolate import griddata

# --- 1. LOAD AND COMBINE ALL KNOWN DATA POINTS ---
input_folder = 'k_value_outputs2'
output_map_filename = 'global_complete_heatmap.html'
output_csv_filename = 'global_complete_k_values.csv'

print(f"Looking for k-value files in '{input_folder}'...")
search_pattern = os.path.join(input_folder, '*.csv')
file_list = glob.glob(search_pattern)

if not file_list:
    print(f"Error: No k-value CSV files found in '{input_folder}'.")
    exit()

print(f"Found {len(file_list)} files to use for interpolation.")
df_known = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=True)
df_known.dropna(subset=['latitude', 'longitude', 'k_value'], inplace=True)
print(f"Successfully combined all data. Total known points: {len(df_known)}")

# --- 2. PREPARE DATA FOR INTERPOLATION ---
known_points = df_known[['longitude', 'latitude']].values
known_values = df_known['k_value'].values

# --- 3. CREATE A DENSE GLOBAL GRID TO INTERPOLATE ONTO ---
print("\nCreating a dense global grid...")
spacing = 1.0
lons = np.arange(-180, 181, spacing)
lats = np.arange(-90, 91, spacing)
grid_lons, grid_lats = np.meshgrid(lons, lats)
print(f"Grid created with {grid_lons.size} points.")

# --- 4. PERFORM THE INTERPOLATION ---
print("Interpolating k-values onto the grid (this may take a few minutes)...")
interpolated_k_values = griddata(
    known_points,
    known_values,
    (grid_lons, grid_lats),
    method='linear'
)
print("✅ Interpolation complete.")

# --- 5. CREATE, COMBINE, AND SAVE THE FINAL DATAFRAME ---
print("Preparing and combining final DataFrame...")
# Create a DataFrame with the new interpolated grid points
df_interpolated = pd.DataFrame({
    'latitude': grid_lats.ravel(),
    'longitude': grid_lons.ravel(),
    'k_value': interpolated_k_values.ravel(),
    'description': 'Interpolated' # Add a description for these points
})
df_interpolated.dropna(subset=['k_value'], inplace=True)

# --- THIS IS THE KEY FIX ---
# Combine the original data with the new interpolated grid
df_combined = pd.concat([df_known, df_interpolated], ignore_index=True)

# Remove any duplicate coordinates, keeping the ORIGINAL data point where there's an overlap
df_final = df_combined.drop_duplicates(subset=['latitude', 'longitude'], keep='first')
print(f"Combined data contains {len(df_final)} unique points.")

# Save the complete dataset (original + interpolated) to a CSV file
print(f"Saving combined data to '{output_csv_filename}'...")
df_final.to_csv(output_csv_filename, index=False)
print("✅ CSV file saved.")


# --- 6. CREATE THE FINAL MAP ---
print("Generating final heatmap...")
try:
    world_map = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")
    # Use the final, combined DataFrame for the map
    heat_data = df_final[['latitude', 'longitude', 'k_value']].values.tolist()

    HeatMap(heat_data, radius=10, blur=8, min_opacity=0.4).add_to(world_map)
    
    title_html = '''
                 <h3 align="center" style="font-size:16px"><b>Interpolated Global k-value</b></h3>
                 '''
    world_map.get_root().html.add_child(folium.Element(title_html))

    world_map.save(output_map_filename)

    print(f"\n✅ Success! Interpolated map has been saved to '{output_map_filename}'")

except Exception as e:
    print(f"An error occurred during map creation: {e}")