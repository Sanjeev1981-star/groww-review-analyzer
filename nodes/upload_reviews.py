"""
Node: Upload Reviews
Node name: Upload_Reviews
Type: File / CSV input
Output dataset name: reviews_raw
Config: upload your CSV here.
"""

import pandas as pd
import os

def upload_reviews(csv_file_path):
    """
    Upload and parse CSV file containing app reviews.
    
    Args:
        csv_file_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: DataFrame containing the raw reviews
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Ensure required columns exist
    required_columns = ["date", "rating", "review_text"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    return df

# Example usage
if __name__ == "__main__":
    # This would typically be replaced with actual file upload mechanism
    # For demonstration, we'll create a sample CSV
    sample_data = {
        "date": ["2025-11-17", "2025-11-18", "2025-11-19", "2025-11-20"],
        "rating": [5, 3, 1, 4],
        "review_text": [
            "Great app! Easy to use and navigate.",
            "Could be better, some features are missing.",
            "App keeps crashing, very frustrating.",
            "Good overall but needs performance improvements."
        ],
        "review_title": [
            "Excellent App",
            "Needs Improvement",
            "Crashing Issues",
            "Good but Slow"
        ]
    }
    
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv("sample_reviews.csv", index=False)
    print("Sample CSV created: sample_reviews.csv")