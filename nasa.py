import requests
import pandas as pd
import time

API_KEY = "BxKSbqqjb7sFVPtNtb7DES9itbQ7jVgZdabqbNwH" # Using DEMO_KEY is also an option
START_URL = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={API_KEY}"

# A list to store dictionaries, where each dictionary is a record for one NEO
neo_data_list = []
next_page_url = START_URL
TARGET_RECORDS = 1000

print(f"Starting data collection... Goal: at least {TARGET_RECORDS} records.")

# Loop as long as there is a next page AND we have not met our target
while next_page_url and len(neo_data_list) < TARGET_RECORDS:
    try:
        response = requests.get(next_page_url)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()

        # Process each object on the current page
        for neo in data.get("near_earth_objects", []):
            # Stop adding records if we've already hit the target within this page
            if len(neo_data_list) >= TARGET_RECORDS:
                break

            # Ensure there is close approach data to get velocity from
            if neo.get("close_approach_data"):
                neo_data_list.append({
                    'id': neo.get('id'),
                    'name': neo.get('name'),
                    'relative_velocity_kph': neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                    'estimated_diameter_min_m': neo['estimated_diameter']['meters']['estimated_diameter_min'],
                    'estimated_diameter_max_m': neo['estimated_diameter']['meters']['estimated_diameter_max'],
                    'is_potentially_hazardous': neo.get('is_potentially_hazardous_asteroid')
                })

        # Get the URL for the next page
        next_page_url = data.get("links", {}).get("next")
        
        print(f"Collected {len(neo_data_list)} / {TARGET_RECORDS} records. Fetching next page...")
        time.sleep(1) # Be polite to the API

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        break
    except KeyError as e:
        print(f"Error parsing data: could not find key {e}")
        break

# --- Convert the list to a pandas DataFrame ---
print("\nTarget reached. Converting data to DataFrame...")
df = pd.DataFrame(neo_data_list)

# --- Save the DataFrame to a CSV file ---
output_filename = "data.csv"
df.to_csv(output_filename, index=False)

print(f"✅ Success! All data has been saved to '{output_filename}'.")
print(f"Total records saved: {len(df)}")