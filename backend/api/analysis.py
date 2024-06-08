import pandas as pd

def calculate_statistics(data):
    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Initialize a dictionary to store statistics
    statistics = {}
    
    # Iterate over all columns in the DataFrame
    for column in df.columns:
        # Check if the column contains numerical data
        if pd.api.types.is_numeric_dtype(df[column]):
            # Calculate statistics for the numerical column
            max_value = df[column].max()
            min_value = df[column].min()
            mean_value = df[column].mean()
            median_value = df[column].median()
            std_deviation = df[column].std()
            mode_value = df[column].mode()[0] if not df[column].mode().empty else None
            value_counts = df[column].value_counts()
            most_repeated_value = value_counts.idxmax()
            least_repeated_value = value_counts.idxmin()
            
            # Store the statistics in the dictionary
            statistics[column] = {
                'max': max_value,
                'min': min_value,
                'mean': mean_value,
                'median': median_value,
                'std_deviation': std_deviation,
                'most_repeated': most_repeated_value,
                'least_repeated': least_repeated_value,
            }
    
    return statistics
