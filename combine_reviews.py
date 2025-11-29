"""
Script to combine reviews from multiple sources into a single CSV file
"""

import pandas as pd
import glob
import os
from datetime import datetime

def combine_review_files(pattern="*reviews*.csv", output_file="combined_reviews.csv"):
    """
    Combine multiple review CSV files into a single file
    
    Args:
        pattern (str): File pattern to match
        output_file (str): Output combined CSV filename
    """
    
    # Find all CSV files matching the pattern
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        print(f"No CSV files found matching pattern: {pattern}")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {file}")
    
    # Read and combine all files
    combined_data = []
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            # Add source column
            df['source_file'] = os.path.basename(file)
            combined_data.append(df)
            print(f"Loaded {len(df)} reviews from {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if not combined_data:
        print("No data to combine")
        return
    
    # Combine all dataframes
    combined_df = pd.concat(combined_data, ignore_index=True)
    
    # Ensure we have the required columns for our analysis pipeline
    required_columns = ['date', 'rating', 'review_text']
    optional_columns = ['review_title', 'source_file']
    
    # Check and add missing columns
    for col in required_columns:
        if col not in combined_df.columns:
            combined_df[col] = ''  # Add empty column
    
    # Reorder columns
    all_columns = required_columns + [col for col in optional_columns if col in combined_df.columns]
    combined_df = combined_df[all_columns]
    
    # Save to CSV
    combined_df.to_csv(output_file, index=False)
    print(f"\nCombined {len(combined_df)} reviews from {len(csv_files)} files")
    print(f"Saved to {output_file}")
    
    # Show summary
    print("\nSummary:")
    print(f"  Total reviews: {len(combined_df)}")
    if 'rating' in combined_df.columns:
        print(f"  Average rating: {combined_df['rating'].mean():.2f}")
        print(f"  Rating distribution:")
        rating_counts = combined_df['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            print(f"    {rating} stars: {count} reviews")
    
    if 'source_file' in combined_df.columns:
        print(f"  Sources:")
        source_counts = combined_df['source_file'].value_counts()
        for source, count in source_counts.items():
            print(f"    {source}: {count} reviews")

def main():
    """
    Main function to combine review files
    """
    print("Combining review files...")
    print("=" * 40)
    
    combine_review_files("*reviews*.csv", "all_reviews.csv")

if __name__ == "__main__":
    main()