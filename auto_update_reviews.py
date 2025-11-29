"""
Script to automatically update review files on a schedule
"""

import schedule
import time
import os
import subprocess
import sys
from datetime import datetime

def update_reviews():
    """
    Update reviews by running the scraping scripts
    """
    print(f"[{datetime.now()}] Updating reviews...")
    
    try:
        # Run the Play Store scraper to generate fresh sample data
        print("Running Play Store scraper...")
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'scrape_playstore.py')
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Play Store scraper completed successfully")
        else:
            print(f"Play Store scraper failed: {result.stderr}")
            
        # Run the combiner to update the combined file
        print("Running review combiner...")
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'combine_reviews.py')
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Review combiner completed successfully")
            print(f"[{datetime.now()}] Reviews updated successfully!")
        else:
            print(f"Review combiner failed: {result.stderr}")
            
    except Exception as e:
        print(f"Error updating reviews: {e}")

def setup_auto_update():
    """
    Set up automatic review updates
    """
    print("Setting up automatic review updates...")
    print("Updates will run daily at 2:00 AM")
    print("Press Ctrl+C to stop")
    
    # Schedule daily update at 2:00 AM
    schedule.every().day.at("02:00").do(update_reviews)
    
    # Also run an update immediately
    update_reviews()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def setup_frequent_updates():
    """
    Set up more frequent updates for demonstration purposes
    """
    print("Setting up frequent review updates (every 30 minutes)...")
    print("Press Ctrl+C to stop")
    
    # Schedule update every 30 minutes
    schedule.every(30).minutes.do(update_reviews)
    
    # Also run an update immediately
    update_reviews()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    print("Auto Update Review System")
    print("=" * 30)
    
    # Ask user for update frequency
    print("Choose update frequency:")
    print("1. Daily (recommended for production)")
    print("2. Every 30 minutes (for demonstration)")
    print("3. Manual update only")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        setup_auto_update()
    elif choice == "2":
        setup_frequent_updates()
    elif choice == "3":
        update_reviews()
        print("Manual update completed")
    else:
        print("Invalid choice. Running manual update...")
        update_reviews()