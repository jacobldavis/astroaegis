import pandas as pd
import geopandas as gpd
import os
import glob
import json

def get_k_value_from_text(text_description):
    """
    Scans a text string for keywords to determine a seismic efficiency 'k' value.
    This is a simplified model.
    """
    if not isinstance(text_description, str):
        return 0.01  # Default for non-text or empty entries

    text_lower = text_description.lower()

    # Define keywords for each rock class
    metamorphic_keys = ['metamorphic', 'gneiss', 'schist', 'marble', 'mylonite', 'migmatite']
    igneous_keys = ['igneous', 'granite', 'basalt', 'volcanic', 'plutonic', 'gabbro', 'rhyolite', 'extrusive']
    unconsolidated_keys = ['sand', 'gravel', 'alluvium', 'quaternary', 'ooze', 'clay', 'undivided']
    sedimentary_keys = ['sedimentary', 'sandstone', 'limestone', 'shale', 'carbonate', 'conglomerate']

    # Check in a specific order of priority
    if any(key in text_lower for key in metamorphic_keys):
        return 0.05
    if any(key in text_lower for key in igneous_keys):
        return 0.03
    if any(key in text_lower for key in unconsolidated_keys):
        return 0.01
    if any(key in text_lower for key in sedimentary_keys):
        return 0.0005
    
    return 0.01 # Default value if no keywords are found

# --- SETUP AND FILE PROCESSING ---
input_folder = 'output_checkpoints2'
output_folder = 'k_value_outputs2'
os.makedirs(output_folder, exist_ok=True)
geojson_files = glob.glob(os.path.join(input_folder, '*.geojson'))

if not geojson_files:
    print(f"Error: No GeoJSON files found in the '{input_folder}' directory.")
    exit()

print(f"Found {len(geojson_files)} files to process...")

for filepath in geojson_files:
    filename = os.path.basename(filepath)
    print(f"\n--- Processing {filename} ---")

    try:
        gdf = gpd.read_file(filepath)
        output_data = []
        
        for index, row in gdf.iterrows():
            # --- THIS IS THE KEY FIX ---
            # Use the exact column names from your file: LITHO_EN and DESCR_EN
            lith_text = str(row.get('LITHO_EN', ''))
            desc_text = str(row.get('DESCR_EN', ''))
            full_description = f"{lith_text} {desc_text}"

            k_value = get_k_value_from_text(full_description)
            
            try:
                centroid = row.geometry.centroid
                lat = round(centroid.y, 4)
                lon = round(centroid.x, 4)
            except Exception:
                continue

            output_data.append({
                'latitude': lat,
                'longitude': lon,
                'k_value': k_value,
                'description': desc_text
            })
            
        results_df = pd.DataFrame(output_data)
        output_path = os.path.join(output_folder, filename.replace('.geojson', '_k_values.csv'))
        results_df.to_csv(output_path, index=False)
        print(f"✅ Success! Saved processed data to '{output_path}'")

    except Exception as e:
        print(f"  --> Error processing file {filename}. Error: {e}")

print("\nAll tasks complete!")