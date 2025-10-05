import pandas as pd
import geopandas as gpd
from owslib.wfs import WebFeatureService
import io

# The URL for the WFS GetCapabilities document
wfs_url = 'https://mapsref.brgm.fr/wxs/1GG/CGMW_Bedrock_and_Structural_Geology'

print(f"Connecting to WFS server at: {wfs_url}")

try:
    # Initialize the WFS client
    wfs = WebFeatureService(url=wfs_url, version='2.0.0')
    print("✅ Successfully connected to the WFS service.")

    # The layer for onshore geology
    layer_name = 'ms:World_CGMW_50M_GeologicalUnitsOnshore'

    # --- NEW, MORE ROBUST METHOD ---
    # Get the global list of supported output formats for GetFeature requests
    get_feature_op = wfs.getOperationByName('GetFeature')
    
    if not get_feature_op or 'outputFormat' not in get_feature_op.parameters:
        raise ValueError("Could not determine supported output formats from the server.")

    supported_formats = get_feature_op.parameters['outputFormat']['values']
    
    print("\nServer's globally supported formats for GetFeature:")
    for fmt in supported_formats:
        print(f"- {fmt}")

    # --- CHOOSE A RELIABLE FORMAT ---
    # We will look for a GML format, as it is standard and readable by GeoPandas.
    # 'text/xml; subtype=gml/3.2.1' is a great choice if available.
    output_format = None
    for fmt in supported_formats:
        if 'gml' in fmt.lower():
            output_format = fmt
            break
            
    if not output_format:
        raise ValueError("No suitable GML format found in the server's supported formats.")

    print(f"\nSelected format for download: {output_format}")

    # Define a bounding box to query [min_lon, min_lat, max_lon, max_lat]
    bbox = (15.0, -5.0, 25.0, 5.0) 

    print(f"Requesting features from layer '{layer_name}' for bounding box {bbox}...")
    
    # Make the GetFeature request
    response = wfs.getfeature(
        typename=layer_name,
        bbox=bbox,
        outputFormat=output_format
    )

    print("✅ Data received. Converting to GeoDataFrame...")

    # Read the response into a GeoDataFrame
    gdf = gpd.read_file(io.BytesIO(response.read()))

    print("\nSample of downloaded data:")
    print(gdf.head())

    # Save the data to a file
    output_filename = 'africa_geology_sample.geojson'
    gdf.to_file(output_filename, driver='GeoJSON')

    print(f"\n✅ Success! Sample data has been saved to '{output_filename}'")

except Exception as e:
    print(f"\nAn error occurred: {e}")