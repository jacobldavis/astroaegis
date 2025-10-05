import pandas as pd
import folium
from folium.plugins import HeatMap
import glob
import os

# --- 1. SETUP FILE PATHS ---
# Folder where your new k-value CSVs are located
input_folder = 'k_value_outputs2'
# The name of the final output map
output_filename = 'continental_k_value_heatmap_water4.html'

# --- 2. FIND AND COMBINE ALL K-VALUE FILES ---
print(f"Looking for continental k-value files in '{input_folder}'...")
search_pattern = os.path.join(input_folder, '*_k_values.csv')
file_list = glob.glob(search_pattern)

if not file_list:
    print(f"Error: No k-value CSV files found in '{input_folder}'. Please run the previous script first.")
    exit()

print(f"Found {len(file_list)} files to combine: {file_list}")

# Read each CSV and append it to a list of DataFrames
all_dfs = [pd.read_csv(f) for f in file_list]

# Concatenate all DataFrames into a single one
df = pd.concat(all_dfs, ignore_index=True)
print(f"Successfully combined all data. Total entries: {len(df)}")


# --- SECTION 3 REMOVED ---
# The block of code that loaded the old 'k_vals_sorted.csv' has been deleted.
# The script now proceeds using only the data loaded above.


# --- 4. CREATE THE MAP ---
print("\nGenerating heatmap from continental data...")
try:
    # Remove any rows with missing lat/lon data to prevent errors
    df.dropna(subset=['latitude', 'longitude', 'k_value'], inplace=True)

    # Create a base map, centered for a global view
    world_map = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

    # Create a list of [latitude, longitude, k_value] for the heatmap
    heat_data = df[['latitude', 'longitude', 'k_value']].values.tolist()

    # Add the heatmap layer to the map
    HeatMap(heat_data, radius=10, blur=20).add_to(world_map)
    
    # Add a title to the map
    title_html = '''
                 <h3 align="center" style="font-size:16px"><b>Continental Seismic Efficiency (k-value)</b></h3>
                 '''
    world_map.get_root().html.add_child(folium.Element(title_html))

    # Save the map to an HTML file
    world_map.save(output_filename)

    print(f"\n✅ Success! Interactive map has been saved to '{output_filename}'")
    print("Open this file in your web browser to view the map.")

except Exception as e:
    print(f"An error occurred during map creation: {e}")