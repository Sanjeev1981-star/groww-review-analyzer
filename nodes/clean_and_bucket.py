"""
Node: Clean + Add Week Bucket
Node name: Clean_And_Bucket
Type: Python Transform
Input: reviews_raw
Output: reviews_clean
"""

import pandas as pd

def clean_and_bucket(input_df):
    """
    Clean raw app store reviews and add week bucket information.
    
    Args:
        input_df (pandas.DataFrame): DataFrame containing raw reviews
        
    Returns:
        pandas.DataFrame: Cleaned DataFrame with week bucket information
    """
    df = input_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["date", "rating", "review_text"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["week_start"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")
    df["week_start"] = df["week_start"].dt.strftime("%Y-%m-%d")

    title_col = "review_title" if "review_title" in df.columns else None

    def combine(row):
        t = row[title_col] if title_col and pd.notna(row[title_col]) else ""
        r = row["review_text"] if pd.notna(row["review_text"]) else ""
        return f"{t} - {r}".strip(" -")

    df["full_text"] = df.apply(combine, axis=1)

    return df

# Example usage
if __name__ == "__main__":
    # Sample input data
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
    
    input_df = pd.DataFrame(sample_data)
    output_df = clean_and_bucket(input_df)
    print("Cleaned and bucketed reviews:")
    print(output_df)