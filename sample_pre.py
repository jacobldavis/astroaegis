import json
import math
import os

# --- 1. CONFIGURATION (Must match the precomputation script) ---
CACHE_FILE = "tile_k_values_cache.json"
TILE_SIZE = (3, 3)
END_POS = (3085, 1542)

# --- 2. LOAD THE PRECOMPUTED CACHE (RUNS ONCE) ---
print(f"Loading precomputed k-value cache from '{CACHE_FILE}'...")
if not os.path.exists(CACHE_FILE):
    print(f"\nFatal Error: Cache file not found at '{CACHE_FILE}'.")
    print("Please run the precomputation script first.")
    exit()

try:
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        tile_k_values_cache = json.load(f)
    print(f"✅ Cache loaded with {len(tile_k_values_cache)} tiles.")
except Exception as e:
    print(f"Fatal Error: Could not read or parse the cache file. Error: {e}")
    exit()


# --- 3. THE FAST QUERY FUNCTION ---

def get_k_from_cache(lat, lon):
    """
    Finds the precomputed k-value for a given lat/lon by looking it up in the cache.
    
    Args:
        lat (float): The latitude of the point to query.
        lon (float): The longitude of the point to query.
        
    Returns:
        float: The k-value for that tile, or None if not found.
    """
    try:
        # --- Reverse Mapping: Convert lat/lon back to tile coordinates ---

        # 1. Convert lat/lon to the pixel coordinate system
        # These are the inverse of the formulas in the precomputation script
        pixel_x = (lon / 360.0 + 0.5) * END_POS[0]
        pixel_y = (lat / 180.0 + 0.5) * END_POS[1]
        
        # 2. Convert pixel coordinates to tile coordinates
        tile_x = int(math.floor(pixel_x / TILE_SIZE[0]))
        tile_y = int(math.floor(pixel_y / TILE_SIZE[1]))
        
        # 3. Construct the key and look it up in the cache
        key = f"{tile_x},{tile_y}"
        
        if key in tile_k_values_cache:
            return tile_k_values_cache[key].get("k_value")
        else:
            return None # The coordinate is outside the precomputed grid

    except Exception as e:
        print(f"An error occurred during lookup: {e}")
        return None

# --- 4. EXAMPLE USAGE ---

if __name__ == "__main__":
    print("\n--- Example Query ---")
    
    # Coordinates for Clemson University, SC
    query_latitude = 34.6834
    query_longitude = -82.8374
    
    print(f"Querying precomputed k-value for coordinates: ({query_latitude}, {query_longitude})")
    
    k_value = get_k_from_cache(query_latitude, query_longitude)
    
    if k_value is not None:
        print("\n--- Result ---")
        print(f"  - Precomputed K-Value: {k_value:.5f}")
    else:
        print("\nCould not find a k-value for the specified coordinates.")