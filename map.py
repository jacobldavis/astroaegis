import pandas as pd
import folium
from folium.plugins import HeatMap

# Define the input and output filenames
input_filename = 'k_vals_sorted.csv'
output_filename = 'geo_map.html'

print(f"Reading coordinates from '{input_filename}'...")

try:
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(input_filename)

    # Remove any rows with missing lat/lon data to prevent errors
    df.dropna(subset=['latitude', 'longitude'], inplace=True)

    # Create a base map, centered for a global view
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    # Create a list of [latitude, longitude, k_value] for the heatmap
    heat_data = df[['latitude', 'longitude', 'k_value']].values.tolist()

    # Add the heatmap layer to the map
    HeatMap(heat_data, radius=15).add_to(world_map)
    
    # Add a title to the map
    title_html = '''
                 <h3 align="center" style="font-size:16px"><b>Seismic Efficiency (k-value) by Geologic Column</b></h3>
                 '''
    world_map.get_root().html.add_child(folium.Element(title_html))


    # Save the map to an HTML file
    world_map.save(output_filename)

    print(f"\n✅ Success! Interactive map has been saved to '{output_filename}'")
    print("Open this file in your web browser to view the map.")

except FileNotFoundError:
    print(f"Error: The file '{input_filename}' was not found. Please make sure it is in the correct directory.")
except Exception as e:
    print(f"An error occurred: {e}")