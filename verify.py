import pandas as pd
import geopandas as gpd

# --- SCRIPT TO ANALYZE YOUR K-VALUE FILE ---

try:
    # Load your final k-value dataset
    print("Loading your k-value data...")
    df_k_values = pd.read_csv('global_complete_k_values.csv')
    
    # Convert it to a GeoDataFrame
    gdf_k_values = gpd.GeoDataFrame(
        df_k_values,
        geometry=gpd.points_from_xy(df_k_values.longitude, df_k_values.latitude),
        crs="EPSG:4326"
    )

    # Load the world map to define the land areas
    print("Loading world map shapefile to identify land areas...")
    world = gpd.read_file("countries/ne_110m_admin_0_countries.shp")

    # Spatially join the k-value points to the land polygons
    # This keeps only the points that are located on land
    print("Performing spatial join to isolate land points...")
    land_points = gpd.sjoin(gdf_k_values, world, predicate='within', how="inner")

    print("\n--- Analysis of k-values for points on land ---")
    
    # Calculate and print summary statistics for the k-values on land
    stats = land_points['k_value'].describe()
    print(stats)

    # Calculate the percentage of land points with values close to the ocean value
    ocean_value = 1e-5
    low_value_threshold = 2e-5 # A threshold just above the ocean value
    low_value_count = land_points[land_points['k_value'] <= low_value_threshold].shape[0]
    total_land_points = len(land_points)
    low_value_percentage = (low_value_count / total_land_points) * 100

    print(f"\nPercentage of land points with k-values near the ocean value: {low_value_percentage:.2f}%")

except FileNotFoundError:
    print("\nError: Could not find 'global_complete_k_values.csv' or 'ne_110m_admin_0_countries.shp'.")
except Exception as e:
    print(f"\nAn error occurred: {e}")