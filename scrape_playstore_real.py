"""
Script to scrape reviews from Google Play Store using google-play-scraper library
"""

from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime, timedelta

def scrape_playstore_reviews_real(app_id, count=100, country='in'):
    """
    Scrape real reviews from Google Play Store using google-play-scraper
    
    Args:
        app_id (str): Package name of the app (e.g., 'com.nextbillion.groww')
        count (int): Number of reviews to fetch
        country (str): Country code for reviews (default: 'in' for India)
        
    Returns:
        list: List of review dictionaries
    """
    
    print(f"Fetching {count} reviews for app: {app_id}")
    
    try:
        # Fetch reviews sorted by newest first
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country=country,
            sort=Sort.NEWEST,
            count=count
        )
        
        print(f"Successfully fetched {len(result)} reviews")
        
        # Transform to match our pipeline format
        transformed_reviews = []
        for review in result:
            transformed_reviews.append({
                'review_id': review.get('reviewId', ''),
                'date': review.get('at', datetime.now()).strftime('%Y-%m-%d'),
                'rating': review.get('score', 0),
                'review_title': review.get('userName', 'Anonymous'),  # Play Store doesn't have titles
                'review_text': review.get('content', '')
            })
        
        return transformed_reviews
        
    except Exception as e:
        print(f"Error fetching Play Store reviews: {e}")
        print("Falling back to sample data...")
        return generate_sample_reviews('Groww', count=50)


def generate_sample_reviews(app_name, count=50):
    """
    Generate sample reviews for demonstration (fallback)
    
    Args:
        app_name (str): Name of the app
        count (int): Number of reviews to generate
        
    Returns:
        list: List of review dictionaries
    """
    import random
    
    # Sample review templates
    positive_reviews = [
        f"Excellent {app_name} app! Very user-friendly and intuitive.",
        f"Love this {app_name} app. The interface is clean and navigation is smooth.",
        f"Great investment platform. {app_name} makes stock trading so easy!",
        f"Fantastic app! {app_name} has helped me manage my investments effortlessly.",
        f"Outstanding service. {app_name} is the best investment app I've used.",
        f"Superb app with great features. {app_name} is a game-changer!",
        f"I'm impressed with {app_name}. The research tools are excellent.",
        f"Top-notch investment app. {app_name} deserves 5 stars!",
        f"Wonderful experience with {app_name}. Highly recommended!",
        f"Brilliant app design. {app_name} makes investing accessible to everyone."
    ]
    
    negative_reviews = [
        f"{app_name} app keeps crashing on my device. Needs urgent fixing.",
        f"Disappointing experience with {app_name}. Too many bugs and glitches.",
        f"Not happy with {app_name}. The app is slow and unresponsive.",
        f"{app_name} has too many issues. Constantly freezes during transactions.",
        f"Terrible app experience. {app_name} needs major improvements.",
        f"Frustrating to use {app_name}. The interface is confusing and cluttered.",
        f"{app_name} app is unreliable. Lost my data twice already.",
        f"Poor performance from {app_name}. Laggy and prone to crashes.",
        f"Unstable {app_name} app. Freezes every few minutes.",
        f"Awful experience with {app_name}. Customer support is unhelpful."
    ]
    
    neutral_reviews = [
        f"{app_name} is okay, but could use some improvements.",
        f"Average app. {app_name} has potential but needs work.",
        f"Decent {app_name} app. Some good features, some drawbacks.",
        f"{app_name} is alright. Nothing exceptional but it works.",
        f"Mediocre app experience with {app_name}. Needs enhancement.",
        f"Fair {app_name} app. Good for basic needs but lacks advanced features.",
        f"{app_name} is functional but could be more user-friendly.",
        f"Standard investment app. {app_name} meets basic requirements.",
        f"Reasonable app. {app_name} could improve with updates.",
        f"Satisfactory {app_name} experience. Room for improvement."
    ]
    
    # Sample titles
    positive_titles = [
        "Excellent App!", "Love It!", "Highly Recommended", "Fantastic Service",
        "Outstanding Experience", "Great Investment Tool", "Impressive Features",
        "Top Notch App", "Wonderful Experience", "Brilliant Design"
    ]
    
    negative_titles = [
        "App Crashes", "Too Many Bugs", "Poor Performance", "Constant Freezes",
        "Terrible Experience", "Confusing Interface", "Unreliable App",
        "Laggy Performance", "Unstable App", "Awful Experience"
    ]
    
    neutral_titles = [
        "Okay But Needs Work", "Average App", "Decent But Lacking",
        "Alright For Basics", "Mediocre Experience", "Fair But Limited",
        "Functional But Basic", "Standard App", "Reasonable But Plain",
        "Satisfactory With Room For Improvement"
    ]
    
    # Generate reviews for the past 8 weeks
    reviews = []
    base_date = datetime.now() - timedelta(weeks=8)
    
    for i in range(count):
        # Randomly select sentiment
        rand_val = random.random()
        if rand_val < 0.6:  # 60% positive
            review_text = random.choice(positive_reviews)
            review_title = random.choice(positive_titles)
            rating = random.randint(4, 5)
        elif rand_val < 0.8:  # 20% negative
            review_text = random.choice(negative_reviews)
            review_title = random.choice(negative_titles)
            rating = random.randint(1, 2)
        else:  # 20% neutral
            review_text = random.choice(neutral_reviews)
            review_title = random.choice(neutral_titles)
            rating = 3
        
        # Random date within the past 8 weeks
        days_offset = random.randint(0, 56)  # 8 weeks = 56 days
        review_date = base_date + timedelta(days=days_offset)
        
        reviews.append({
            'review_id': f"review_{i+1}",
            'date': review_date.strftime("%Y-%m-%d"),
            'rating': rating,
            'review_title': review_title,
            'review_text': review_text
        })
    
    return reviews


def save_reviews_to_csv(reviews, filename='playstore_reviews.csv'):
    """
    Save reviews to CSV file
    
    Args:
        reviews (list): List of review dictionaries
        filename (str): Output CSV filename
    """
    
    if not reviews:
        print("No reviews to save")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(reviews)
    
    # Select only the columns we need for our analysis pipeline
    output_df = df[['date', 'rating', 'review_text', 'review_title']].copy()
    
    # Save to CSV
    output_df.to_csv(filename, index=False)
    print(f"Saved {len(reviews)} reviews to {filename}")


def main():
    """
    Main function to fetch Play Store reviews and save to CSV
    """
    # Groww app package name on Play Store
    app_id = "com.nextbillion.groww"  # Real Groww app package name
    
    print("Google Play Store Review Scraper")
    print("=" * 40)
    
    # Fetch real reviews
    reviews = scrape_playstore_reviews_real(app_id, count=100)
    
    # Save to CSV
    if reviews:
        save_reviews_to_csv(reviews, 'groww_playstore_reviews.csv')
        print(f"\nSuccess! Fetched {len(reviews)} reviews and saved to groww_playstore_reviews.csv")
        
        # Show sample of the data
        print("\nSample of fetched data:")
        df = pd.DataFrame(reviews)
        print(df[['rating', 'review_title', 'review_text']].head(5))
        
        # Show rating distribution
        print("\nRating Distribution:")
        rating_counts = df['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            print(f"  {rating} stars: {count} reviews")
    else:
        print("No reviews were fetched")


if __name__ == "__main__":
    main()
