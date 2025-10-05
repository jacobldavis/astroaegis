import csv
import json
import math
from typing import Dict, List, Tuple, Optional

# Configuration
CSV_FILE = "global_complete_k_values.csv"
OUTPUT_FILE = "tile_k_values_cache.json"
TILE_SIZE = (3, 3)
END_POS = (3085, 1542)
GRID_SIZE = 1.0  # degrees per cell for spatial hashing
RADIUS_KM = 20.0
K_VALUE_SIMILARITY_THRESHOLD = 0.0002

class SpatialHash:
    def __init__(self, grid_size: float):
        self.grid_size = grid_size
        self.hash_map: Dict[Tuple[int, int], List[dict]] = {}
    
    def get_grid_pos(self, lat: float, lon: float) -> Tuple[int, int]:
        return (int(math.floor(lon / self.grid_size)), 
                int(math.floor(lat / self.grid_size)))
    
    def add_point(self, point: dict):
        if "longitude" not in point or "latitude" not in point:
            return
        
        grid_pos = self.get_grid_pos(point["latitude"], point["longitude"])
        
        if grid_pos not in self.hash_map:
            self.hash_map[grid_pos] = []
        
        self.hash_map[grid_pos].append(point)
    
    def get_nearby_cells(self, lat: float, lon: float, search_radius: int = 1) -> List[dict]:
        center_cell = self.get_grid_pos(lat, lon)
        cells = []
        
        for dy in range(-search_radius, search_radius + 1):
            for dx in range(-search_radius, search_radius + 1):
                check_cell = (center_cell[0] + dx, center_cell[1] + dy)
                if check_cell in self.hash_map:
                    cells.extend(self.hash_map[check_cell])
        
        return cells

def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calculate distance between two points in km"""
    R = 6371.0  # km
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def load_data(filename: str) -> Tuple[List[dict], SpatialHash]:
    """Load CSV data and build spatial hash"""
    print(f"Loading data from {filename}...")
    
    data = []
    spatial_hash = SpatialHash(GRID_SIZE)
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Convert numeric fields
            entry = {}
            for key, val in row.items():
                if key in ["latitude", "longitude", "k_value"]:
                    entry[key] = float(val)
                else:
                    entry[key] = val
            
            data.append(entry)
            spatial_hash.add_point(entry)
    
    print(f"Loaded {len(data)} points")
    print(f"Built spatial hash with {len(spatial_hash.hash_map)} cells")
    
    return data, spatial_hash

def find_nearest_point(lat: float, lon: float, data: List[dict], 
                       spatial_hash: SpatialHash) -> Optional[dict]:
    """Find nearest point using spatial hash"""
    search_radius = 1
    max_search_radius = 5
    
    nearest_point = None
    min_dist = float('inf')
    
    while nearest_point is None and search_radius <= max_search_radius:
        candidates = spatial_hash.get_nearby_cells(lat, lon, search_radius)
        
        for point in candidates:
            dist = haversine_distance(lon, lat, point["longitude"], point["latitude"])
            if dist < min_dist:
                min_dist = dist
                nearest_point = point
        
        if nearest_point is None:
            search_radius += 1
    
    # Fallback to full search if needed
    if nearest_point is None:
        for point in data:
            if "longitude" not in point or "latitude" not in point:
                continue
            dist = haversine_distance(lon, lat, point["longitude"], point["latitude"])
            if dist < min_dist:
                min_dist = dist
                nearest_point = point
    
    return nearest_point

def find_k_and_description(lat: float, lon: float, data: List[dict], 
                           spatial_hash: SpatialHash) -> Tuple[Optional[dict], Optional[str]]:
    """Find k-value and relevant description for a lat/lon"""
    
    nearest_point = find_nearest_point(lat, lon, data, spatial_hash)
    
    if nearest_point is None:
        return None, None
    
    final_description = nearest_point.get("description", None)
    
    # Find nearby detailed points
    radius_in_degrees = RADIUS_KM / 111.0
    search_cells_radius = int(math.ceil(radius_in_degrees / GRID_SIZE)) + 1
    
    candidates = spatial_hash.get_nearby_cells(lat, lon, search_cells_radius)
    
    nearby_points = []
    for point in candidates:
        dist = haversine_distance(lon, lat, point["longitude"], point["latitude"])
        if dist <= RADIUS_KM:
            nearby_points.append(point)
    
    # Filter for detailed points
    detailed_points = [p for p in nearby_points if p.get("description", "") != "Interpolated"]
    
    if detailed_points:
        # Find closest detailed point
        closest_detailed = min(detailed_points, 
                              key=lambda p: haversine_distance(lon, lat, p["longitude"], p["latitude"]))
        
        k_main = nearest_point["k_value"]
        k_detail = closest_detailed["k_value"]
        
        if abs(k_main - k_detail) <= K_VALUE_SIMILARITY_THRESHOLD:
            final_description = closest_detailed["description"]
        else:
            final_description = f"Nearest detailed point geologically different (k={k_detail:.5f})"
    
    if final_description == "Interpolated":
        final_description = None
    
    return nearest_point, final_description

def precompute_tile_k_values(data: List[dict], spatial_hash: SpatialHash) -> dict:
    """Precompute k-values for all tiles"""
    
    tile_grid_size = (
        math.ceil(END_POS[0] / TILE_SIZE[0]),
        math.ceil(END_POS[1] / TILE_SIZE[1])
    )
    
    print(f"Precomputing k-values for {tile_grid_size[0]} x {tile_grid_size[1]} = {tile_grid_size[0] * tile_grid_size[1]} tiles...")
    
    tile_k_values = {}
    total_tiles = tile_grid_size[0] * tile_grid_size[1]
    
    for tile_y in range(tile_grid_size[1]):
        for tile_x in range(tile_grid_size[0]):
            # Convert tile position to pixel position (center of tile)
            pixel_x = tile_x * TILE_SIZE[0] + TILE_SIZE[0] / 2.0
            pixel_y = tile_y * TILE_SIZE[1] + TILE_SIZE[1] / 2.0
            
            # Convert pixel position to lat/lon
            lat = 90.0 * 2.0 * (pixel_y / END_POS[1] - 0.5)
            lon = 180.0 * 2.0 * (pixel_x / END_POS[0] - 0.5)
            
            # Find k-value and description
            nearest_point, description = find_k_and_description(lat, lon, data, spatial_hash)
            
            # Store with string key for JSON (only k_value to save space)
            key = f"{tile_x},{tile_y}"
            tile_k_values[key] = {
                "k_value": nearest_point["k_value"] if nearest_point else 0.0
            }
        
        # Progress indicator
        if tile_y % 50 == 0:
            progress = ((tile_y * tile_grid_size[0]) / total_tiles) * 100
            print(f"Progress: {progress:.1f}% ({tile_y}/{tile_grid_size[1]} rows)")
    
    print("Precomputation complete!")
    return tile_k_values

def main():
    print("=== Tile K-Value Cache Generator ===")
    print(f"Configuration:")
    print(f"  CSV File: {CSV_FILE}")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"  Tile Size: {TILE_SIZE}")
    print(f"  End Position: {END_POS}")
    print()
    
    # Load data
    data, spatial_hash = load_data(CSV_FILE)
    
    # Precompute tiles
    tile_k_values = precompute_tile_k_values(data, spatial_hash)
    
    # Save to JSON
    print(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(tile_k_values, f)
    
    print(f"Successfully saved {len(tile_k_values)} tiles to {OUTPUT_FILE}")
    
    # Print file size
    import os
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    main()