import requests
import json

# Define the coordinates for your point of interest (Clemson University)
latitude = 34
longitude = -82

# Construct the full API URL with the correct endpoint and coordinates
api_url = f"https://macrostrat.org/api/v2/mobile/point?lat={latitude}&lng={longitude}"

print(f"Querying API for coordinates: ({latitude}, {longitude})")

try:
    # Make the API request
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # The rock info is in the first item of the 'data' list
    rock_info = data['success']['data'][0]

    # Extract the specific fields you want
    lith_type = rock_info.get('lith_type', 'N/A')
    lithology = rock_info.get('lith', 'N/A')
    unit_name = rock_info.get('name', 'N/A')

    # Print the final result
    print("\n--- Geological Info ---")
    print(f"      Unit Name: {unit_name}")
    print(f"Lithology Class: {lith_type}")
    print(f"Specific Lithology: {lithology}")


except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request: {e}")
except (KeyError, IndexError) as e:
    print(f"Error parsing data. No data found for these coordinates. Error: {e}")