import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# Import real scrapers
from scrape_playstore_real import scrape_playstore_reviews_real, save_reviews_to_csv as save_playstore_csv
from scrape_trustpilot import scrape_trustpilot_reviews, save_reviews_to_csv as save_trustpilot_csv
from main_pipeline import run_app_review_analysis

def main():
    print("Starting Weekly App Review Job")
    print("=" * 40)

    # 1. Configuration
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    print("Debug: Checking Environment Variables...")
    print(f"RECIPIENT_EMAIL: {'Found' if recipient_email else 'MISSING'}")
    print(f"SENDER_EMAIL: {'Found' if sender_email else 'MISSING'}")
    print(f"SENDER_PASSWORD: {'Found' if sender_password else 'MISSING'}")
    
    email_config = None
    if recipient_email and sender_email and sender_password:
        email_config = {
            "recipient_email": recipient_email,
            "sender_email": sender_email,
            "sender_password": sender_password
        }
        print("✓ Email configuration found. Will send report.")
    else:
        print("! Email configuration missing. Will NOT send report.")
        print("  Set RECIPIENT_EMAIL, SENDER_EMAIL, and SENDER_PASSWORD env vars.")

    # 2. Scrape/Generate Data from Multiple Sources
    print("\nStep 1: Fetching reviews from multiple sources...")
    
    # 2a. Fetch Play Store reviews
    print("\n  Fetching Play Store reviews...")
    playstore_app_id = "com.nextbillion.groww"  # Real Groww app ID
    playstore_reviews = scrape_playstore_reviews_real(playstore_app_id, count=100)
    
    # 2b. Fetch Trustpilot reviews
    print("\n  Fetching Trustpilot reviews...")
    trustpilot_url = "https://www.trustpilot.com/review/groww.in"
    trustpilot_reviews = scrape_trustpilot_reviews(trustpilot_url, max_pages=3)
    
    # 2c. Combine reviews from both sources
    print(f"\n  Combining reviews...")
    print(f"    Play Store: {len(playstore_reviews)} reviews")
    print(f"    Trustpilot: {len(trustpilot_reviews)} reviews")
    
    # Convert to DataFrames and combine
    df_playstore = pd.DataFrame(playstore_reviews)
    df_trustpilot = pd.DataFrame(trustpilot_reviews)
    
    # Ensure both have the same columns
    required_cols = ['date', 'rating', 'review_text', 'review_title']
    for col in required_cols:
        if col not in df_playstore.columns:
            df_playstore[col] = ''
        if col not in df_trustpilot.columns:
            df_trustpilot[col] = ''
    
    # Add source column to track where reviews came from
    df_playstore['source'] = 'Play Store'
    df_trustpilot['source'] = 'Trustpilot'
    
    # Combine
    combined_df = pd.concat([df_playstore, df_trustpilot], ignore_index=True)
    
    # Save combined reviews
    csv_filename = "combined_reviews.csv"
    combined_df[required_cols].to_csv(csv_filename, index=False)
    print(f"  Total combined reviews: {len(combined_df)}")
    print(f"  Saved to: {csv_filename}")
    
    # 3. Determine Target Week
    # We want to analyze the last completed week.
    # We'll pick a date 7 days ago to ensure we have data.
    today = datetime.now()
    target_date = today - timedelta(days=7)
    # Align to Monday
    target_week_start = (target_date - timedelta(days=target_date.weekday())).strftime("%Y-%m-%d")
    
    print(f"\nTarget week start: {target_week_start}")

    # 4. Run Analysis
    print("\nStep 2: Running analysis pipeline...")
    try:
        run_app_review_analysis(csv_filename, target_week_start, email_config)
        print("\n✓ Job completed successfully.")
    except Exception as e:
        print(f"\n✗ Job failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
