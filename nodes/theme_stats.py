"""
Node: Python – Aggregate Theme Stats
Node name: Theme_Stats
Type: Python Transform
Input: reviews_week_tagged
Output: themes_week_stats
"""

import pandas as pd

def theme_stats(input_df):
    """
    Aggregate statistics by theme.
    
    Args:
        input_df (pandas.DataFrame): DataFrame containing tagged reviews
        
    Returns:
        pandas.DataFrame: Aggregated theme statistics
    """
    df = input_df.copy()

    agg = df.groupby("theme").agg(
        review_count=("full_text", "count"),
        avg_rating=("rating", "mean"),
        negative_count=("sentiment", lambda s: (s == "NEGATIVE").sum())
    ).reset_index()

    agg["avg_rating"] = agg["avg_rating"].round(2)
    agg["neg_share"] = (agg["negative_count"] / agg["review_count"]).round(2)

    # Sort: more reviews and more negative first
    agg = agg.sort_values(["review_count", "neg_share"], ascending=[False, False])

    return agg

# Example usage
if __name__ == "__main__":
    # Sample input data
    sample_data = {
        "full_text": [
            "Great app! Easy to use and navigate.",
            "Could be better, some features are missing.",
            "App keeps crashing, very frustrating.",
            "Good overall but needs performance improvements.",
            "Easy onboarding process."
        ],
        "rating": [5, 3, 1, 4, 5],
        "theme": [
            "App Performance & Bugs",
            "App Performance & Bugs",
            "App Performance & Bugs",
            "Payments & SIP",
            "Onboarding & KYC"
        ],
        "sentiment": [
            "POSITIVE",
            "NEGATIVE",
            "NEGATIVE",
            "MIXED",
            "POSITIVE"
        ]
    }
    
    input_df = pd.DataFrame(sample_data)
    output_df = theme_stats(input_df)
    
    print("Theme statistics:")
    print(output_df)