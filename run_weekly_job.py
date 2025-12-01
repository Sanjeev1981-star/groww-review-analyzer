import os
import sys
from datetime import datetime, timedelta
from scrape_playstore import scrape_playstore_reviews, save_reviews_to_csv
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

    # 2. Scrape/Generate Data
    print("\nStep 1: Fetching reviews...")
    # In a real scenario, we would scrape. Here we generate sample data.
    # The scrape_playstore_reviews function in the current codebase generates sample data.
    reviews = scrape_playstore_reviews("com.groww.app", max_pages=5)
    csv_filename = "groww_playstore_reviews.csv"
    save_reviews_to_csv(reviews, csv_filename)
    
    # 3. Determine Target Week
    # We want to analyze the last completed week (e.g., starting last Monday)
    # For demonstration, we'll pick a date that ensures we have data from the sample generator.
    # The sample generator creates data for the past 8 weeks.
    # Let's pick 7 days ago as the target week start.
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
        sys.exit(1)

if __name__ == "__main__":
    main()
