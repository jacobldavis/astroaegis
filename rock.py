import requests
import json

for lith in range(221):
    try:
        response = requests.get(f"https://macrostrat.org/api/columns?lith_id={lith + 1}") #221
        response.raise_for_status()
        data = response.json()

        with open(f"liths/lith_{lith + 1}.json", 'w') as f:
            json.dump(data, f, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
    except KeyError as e:
        print(f"Error parsing data: could not find key {e}")