"""
Node: Pick the Week to Analyze
Node name: Filter_Target_Week
Type: Python Transform
Input: reviews_clean
Parameter: target_week_start (string, e.g. "2025-11-17")
Output: reviews_week
"""

import pandas as pd

def filter_target_week(input_df, target_week_start):
    """
    Filter reviews for a specific target week.
    
    Args:
        input_df (pandas.DataFrame): DataFrame containing cleaned reviews with week information
        target_week_start (str): Target week start date in format "YYYY-MM-DD"
        
    Returns:
        pandas.DataFrame: Filtered DataFrame for the target week
    """
    # Filter for the target week
    out = input_df[input_df["week_start"] == target_week_start].copy()
    out = out.reset_index(drop=True)
    
    return out

# Example usage
if __name__ == "__main__":
    # Sample input data with week information
    sample_data = {
        "date": ["2025-11-17", "2025-11-18", "2025-11-19", "2025-11-24"],
        "rating": [5, 3, 1, 4],
        "review_text": [
            "Great app! Easy to use and navigate.",
            "Could be better, some features are missing.",
            "App keeps crashing, very frustrating.",
            "Good overall but needs performance improvements."
        ],
        "week_start": ["2025-11-17", "2025-11-17", "2025-11-17", "2025-11-24"]
    }
    
    input_df = pd.DataFrame(sample_data)
    target_week_start = "2025-11-17"
    
    output_df = filter_target_week(input_df, target_week_start)
    print(f"Reviews for week starting {target_week_start}:")
    print(output_df)