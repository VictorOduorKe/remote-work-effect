import pandas as pd
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define file path relative to script location
file_path = os.path.join(script_dir, "..", "datasets", "2021_cleaned_data.csv")

try:
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Print all columns to identify relevant ones
    # print("--- Column Names ---")
    # for col in df.columns:
    #     print(col)
        
    print("\n--- Value Counts for Key Columns ---")
    
    cols_to_check = [
        'how_much_of_your_work', 
        'how_often_do_you_work',
        'relative_remote_productivity'
    ]
    
    for col in cols_to_check:
        if col in df.columns:
            print(f"\nValue Counts for '{col}':")
            print(df[col].value_counts(dropna=False))
        else:
            print(f"\nColumn '{col}' not found.")

except Exception as e:
    print(f"Error loading file: {e}")
