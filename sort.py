import pandas as pd

# Define the input and output filenames
input_filename = 'k_vals.csv'
output_filename = 'k_vals_sorted.csv'

try:
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(input_filename)

    print(f"Original number of entries: {len(df)}")
    
    # Group by latitude and longitude and calculate the average k_value.
    # We will also keep the first lithology name associated with each coordinate.
    df_averaged = df.groupby(['latitude', 'longitude']).agg(
        k_value=('k_value', 'mean'),
        lithology_name=('lithology_name', 'first')
    ).reset_index()

    print(f"Number of unique coordinates after averaging: {len(df_averaged)}")

    # Sort the resulting DataFrame by longitude
    df_sorted = df_averaged.sort_values(by='longitude', ascending=True)

    # Save the final, processed data to a new CSV file
    df_sorted.to_csv(output_filename, index=False)

    print(f"\n✅ Success! Averaged and sorted data has been saved to '{output_filename}'")

except FileNotFoundError:
    print(f"Error: The file '{input_filename}' was not found. Please make sure it is in the correct directory.")