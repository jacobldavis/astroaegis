import pandas as pd
import numpy as np
import os

# --- 1. SETUP AND INITIALIZATION (RUNS ONCE) ---

# Define the path to your complete k-value dataset
data_filename = 'global_complete_k_values.csv'
print(f"Loading data from '{data_filename}'...")

# Check if the data file exists
if not os.path.exists(data_filename):
    print(f"\nFatal Error: Data file not found at '{data_filename}'.")
    exit()

# Load the entire dataset
df = pd.read_csv(data_filename)
df.dropna(subset=['latitude', 'longitude', 'k_value'], inplace=True)

# No need to build a tree, the data is ready to be queried.
print(f"✅ Data loaded. Ready to query {len(df)} points.")


# --- 2. THE DISTANCE AND QUERY FUNCTIONS (NO SKLEARN) ---

def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between one or more points on a sphere.
    Vectorized to handle pandas series.
    """
    R = 6371  # Earth radius in kilometers
    
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    distance = R * c
    return distance

def find_k_and_relevant_description(lat, lon, radius_km=20, k_value_similarity_threshold=2e-4):
    """
    Finds the nearest k-value by brute-force distance calculation, then finds the 
    closest detailed description from a geologically similar point within a radius.
    """
    try:
        # --- Part 1: Find the absolute nearest point (for the k-value) ---
        # This is the main change: calculate distance to all points
        distances = haversine_distance(lon, lat, df['longitude'], df['latitude'])
        
        # Find the index of the point with the minimum distance
        nearest_index = distances.idxmin()
        nearest_point_for_k = df.loc[nearest_index]
        final_description = nearest_point_for_k['description']

        # --- Part 2: Find the closest, geologically similar, detailed description ---
        # Find all points within the radius by filtering the distances
        nearby_points_df = df[distances <= radius_km]
        
        if not nearby_points_df.empty:
            detailed_points_df = nearby_points_df[nearby_points_df['description'] != 'Interpolated']

            if not detailed_points_df.empty:
                # Find the closest point within the detailed subset
                # We can reuse the main 'distances' Series and filter it
                detailed_distances = distances.loc[detailed_points_df.index]
                closest_detailed_index = detailed_distances.idxmin()
                closest_detailed_point = df.loc[closest_detailed_index]
                
                # Perform the similarity check
                k_value_main = nearest_point_for_k['k_value']
                k_value_detailed = closest_detailed_point['k_value']

                if abs(k_value_main - k_value_detailed) <= k_value_similarity_threshold:
                    final_description = closest_detailed_point['description']
                else:
                    final_description = f"Nearest detailed point is geologically different (k-value: {k_value_detailed:.5f})"

        # If the final description is just "Interpolated", return None
        if final_description == 'Interpolated':
            final_description = None

        return nearest_point_for_k, final_description

    except Exception as e:
        print(f"An error occurred during query: {e}")
        return None, "Error during search."

# --- 3. EXAMPLE USAGE ---

if __name__ == "__main__":
    print("\n--- Example Query ---")
    
    # Coordinates for Clemson University, SC
    query_latitude = 43.48 #34.6834
    query_longitude = 110.76 #-82.8374
    
    print(f"Querying coordinates: ({query_latitude}, {query_longitude})")
    print("(This may take a moment as it calculates distance to all points...)")
    
    nearest_point, description = find_k_and_relevant_description(query_latitude, query_longitude)
    
    if nearest_point is not None:
        print("\n--- Results ---")
        print("Absolute Nearest Point (for k-value):")
        print(f"  - Coordinates: ({nearest_point['latitude']}, {nearest_point['longitude']})")
        print(f"  - K-Value: {nearest_point['k_value']:.5f}")
        
        if description:
            print("\nRelevant Description:")
            print(f"  - Description: {description}")