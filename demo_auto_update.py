"""
Demo script showing how to automatically update reviews and analyze them
"""

import requests
import time
import os

def demo_auto_update():
    """
    Demonstrate the automatic update feature
    """
    print("App Review Insights Analyzer - Auto Update Demo")
    print("=" * 50)
    
    # URL of our Flask application
    base_url = "http://localhost:5000"
    
    try:
        # 1. Trigger automatic review update
        print("1. Triggering automatic review update...")
        response = requests.get(f"{base_url}/api/update_reviews")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print("   ✓ Reviews updated successfully!")
            else:
                print(f"   ✗ Failed to update reviews: {result.get('message')}")
        else:
            print(f"   ✗ HTTP Error: {response.status_code}")
        
        # 2. Wait a moment for files to be generated
        time.sleep(2)
        
        # 3. Check if the combined file exists
        combined_file = "all_reviews.csv"
        if os.path.exists(combined_file):
            print("2. Checking generated files...")
            file_size = os.path.getsize(combined_file)
            print(f"   ✓ Found {combined_file} ({file_size} bytes)")
        else:
            print("2. Checking generated files...")
            print(f"   ✗ {combined_file} not found")
        
        # 4. Show how to use the updated file
        print("3. Ready to analyze updated reviews!")
        print(f"   You can now visit {base_url} and upload the generated CSV file")
        print("   or use the 'all_reviews.csv' file directly in your analysis")
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the Flask application")
        print("  Please make sure the app is running at http://localhost:5000")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    demo_auto_update()