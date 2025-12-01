"""
Main pipeline that connects all nodes for the App Review Insights Analyzer.
"""

import pandas as pd
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nodes.upload_reviews import upload_reviews
from nodes.clean_and_bucket import clean_and_bucket
from nodes.filter_target_week import filter_target_week
from nodes.llm_tag_theme_sentiment import llm_tag_theme_sentiment
from nodes.theme_stats import theme_stats
from nodes.llm_weekly_pulse import llm_weekly_pulse
from nodes.parse_email_json import parse_email_json
from nodes.send_weekly_email import send_weekly_email

def run_app_review_analysis(csv_file_path, target_week_start, email_config=None):
    """
    Run the complete app review analysis pipeline.
    
    Args:
        csv_file_path (str): Path to the CSV file containing reviews
        target_week_start (str): Target week start date in format "YYYY-MM-DD"
        email_config (dict): Optional configuration for sending email
        
    Returns:
        dict: Results from each step of the pipeline
    """
    
    print("Starting App Review Insights Analysis Pipeline")
    print("=" * 50)
    
    # Node 1: Upload Reviews
    print("Node 1: Uploading reviews...")
    reviews_raw = upload_reviews(csv_file_path)
    print(f"Uploaded {len(reviews_raw)} reviews")
    
    # Node 2: Clean + Add Week Bucket
    print("\nNode 2: Cleaning and bucketing reviews...")
    reviews_clean = clean_and_bucket(reviews_raw)
    print(f"Cleaned {len(reviews_clean)} reviews")
    
    # Node 3: Pick the Week to Analyze
    print(f"\nNode 3: Filtering for week starting {target_week_start}...")
    reviews_week = filter_target_week(reviews_clean, target_week_start)
    print(f"Filtered to {len(reviews_week)} reviews for target week")
    
    # Node 4: LLM – Tag Theme + Sentiment Per Review
    print("\nNode 4: Tagging themes and sentiment...")
    reviews_week_tagged = llm_tag_theme_sentiment(reviews_week)
    print("Tagged all reviews with themes and sentiment")
    
    # Node 5: Python – Aggregate Theme Stats
    print("\nNode 5: Aggregating theme statistics...")
    themes_week_stats = theme_stats(reviews_week_tagged)
    print("Aggregated theme statistics")
    
    # Node 6: LLM – Build Weekly One-Page Note (≤250 words)
    print("\nNode 6: Generating weekly pulse note...")
    weekly_note_and_email = llm_weekly_pulse(themes_week_stats, reviews_week_tagged, target_week_start)
    print("Generated weekly pulse note and email content")
    
    # Node 7: Extract JSON (Optional Python Helper)
    print("\nNode 7: Parsing email JSON...")
    email_df = pd.DataFrame([{"content": weekly_note_and_email}])
    parsed_email = parse_email_json(email_df)
    print("Parsed email components")
    
    # Node 8: Send Email
    if email_config:
        print("\nNode 8: Sending weekly email...")
        if not parsed_email.empty:
            subject = parsed_email['email_subject'].iloc[0]
            body = parsed_email['email_body'].iloc[0]
            
            print(f"Debug: Email Subject found: {'Yes' if subject else 'No'}")
            print(f"Debug: Email Body found: {'Yes' if body else 'No'}")
            
            if subject and body:
                success = send_weekly_email(
                    email_subject=subject,
                    email_body=body,
                    to_email=email_config.get('recipient_email'),
                    sender_email=email_config.get('sender_email'),
                    sender_password=email_config.get('sender_password')
                )
                if not success:
                    raise Exception("Failed to send email. Check logs for details.")
            else:
                print("Skipping email: Subject or body missing in parsed content.")
                print(f"Parsed Data: {parsed_email.to_dict()}")
        else:
            print("Skipping email: Parsed email dataframe is empty.")

    # Return results from all steps
    results = {
        "reviews_raw": reviews_raw,
        "reviews_clean": reviews_clean,
        "reviews_week": reviews_week,
        "reviews_week_tagged": reviews_week_tagged,
        "themes_week_stats": themes_week_stats,
        "weekly_note_and_email": weekly_note_and_email,
        "parsed_email": parsed_email
    }
    
    print("\n" + "=" * 50)
    print("Pipeline completed successfully!")
    print("=" * 50)
    
    return results

# Example usage
if __name__ == "__main__":
    # Create sample data for demonstration
    sample_data = {
        "date": ["2025-11-17", "2025-11-18", "2025-11-19", "2025-11-20", "2025-11-21"],
        "rating": [5, 3, 1, 4, 2],
        "review_text": [
            "Great app! Easy to use and navigate. Love the new features!",
            "Could be better, some features are missing. Performance needs improvement.",
            "App keeps crashing, very frustrating. Can't complete transactions.",
            "Good overall but needs performance improvements. Slow loading times.",
            "Difficult to navigate. UI could be improved significantly."
        ],
        "review_title": [
            "Excellent App",
            "Needs Improvement",
            "Crashing Issues",
            "Good but Slow",
            "Poor Navigation"
        ]
    }
    
    # Save sample data to CSV
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv("sample_reviews.csv", index=False)
    print("Created sample_reviews.csv for demonstration")
    
    # Run the pipeline
    target_week = "2025-11-17"
    results = run_app_review_analysis("sample_reviews.csv", target_week)
    
    # Display final results
    print("\nFINAL RESULTS:")
    print("-" * 30)
    print("Weekly Note and Email Content:")
    print(results["weekly_note_and_email"])