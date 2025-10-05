import json
import os
import csv
import glob

# --- 1. DEFINE THE K-VALUE CALCULATION MODEL ---
# This is a simplified model. Replace with your own formula for scientific use.
def calculate_k_value(lithology_info):
    """
    Calculates a seismic efficiency 'k' value based on rock class.
    Args:
        lithology_info (dict): A dictionary containing details for one lithology.
    Returns:
        float: The calculated 'k' value.
    """
    rock_class = lithology_info.get('class')
    rock_group = lithology_info.get('group')

    if rock_class == 'metamorphic':
        return 0.9  # High efficiency for dense, crystalline metamorphic rocks
    elif rock_class == 'igneous':
        return 0.8  # High efficiency for crystalline igneous rocks
    elif rock_class == 'sedimentary':
        if rock_group == 'unconsolidated':
            return 0.2  # Low efficiency for loose sediments
        else:
            return 0.5  # Medium efficiency for consolidated sedimentary rocks
    else:
        return 0.0  # Default for unknown types

# --- 2. LOAD LITHOLOGY DEFINITIONS ---
print("Loading lithology definitions...")
try:
    with open('lith_defs.json', 'r') as f:
        lith_defs_data = json.load(f)['success']['data']
    
    # Create a fast-lookup dictionary using lith_id as the key
    lith_definitions = {item['lith_id']: item for item in lith_defs_data}
    print(f"Successfully loaded {len(lith_definitions)} lithology definitions.")

except FileNotFoundError:
    print("Error: 'lith_defs.json' not found. Please check your file setup.")
    exit()

# --- 3. PROCESS EACH LITHOLOGY FILE AND CALCULATE K-VALUES ---
output_data = []
lith_files_path = 'liths/lith_*.json'
lith_files = glob.glob(lith_files_path)

if not lith_files:
    print(f"Error: No lithology files found at '{lith_files_path}'. Please check your file setup.")
    exit()

print(f"\nFound {len(lith_files)} lithology files to process...")

for filepath in lith_files:
    try:
        # Extract the lithology ID from the filename (e.g., '1' from 'liths/lith_1.json')
        filename = os.path.basename(filepath)
        lith_id_str = filename.replace('lith_', '').replace('.json', '')
        lith_id = int(lith_id_str)

        # Get the definition and calculate k for this entire file
        if lith_id in lith_definitions:
            lith_info = lith_definitions[lith_id]
            k_value = calculate_k_value(lith_info)
            lith_name = lith_info.get('name', 'Unknown')
        else:
            # Skip if the lithology ID from the file doesn't have a definition
            continue
        
        # Open the location data file
        with open(filepath, 'r') as f:
            location_data = json.load(f)['success']['data']

        # Loop through each location in the file
        for location in location_data:
            lat = location.get('lat')
            lng = location.get('lng')

            if lat is not None and lng is not None:
                output_data.append({
                    'latitude': lat,
                    'longitude': lng,
                    'k_value': k_value,
                    'lithology_name': lith_name
                })

    except (ValueError, KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Warning: Could not process file {filepath}. Error: {e}")

print(f"\nProcessed all files. Found {len(output_data)} valid coordinate points.")

# --- 4. WRITE THE FINAL DATASET TO A CSV FILE ---
output_csv_file = 'k_values_by_coordinate.csv'
print(f"Writing output to '{output_csv_file}'...")

if output_data:
    with open(output_csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['latitude', 'longitude', 'k_value', 'lithology_name'])
        writer.writeheader()
        writer.writerows(output_data)
    print("✅ Done! Your dataset has been created successfully.")
else:
    print("No data was generated to write to the output file.")