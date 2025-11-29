"""
Script to scrape reviews from Trustpilot and save them as CSV
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime

def scrape_trustpilot_reviews(url, max_pages=5):
    """
    Scrape reviews from Trustpilot website
    
    Args:
        url (str): Trustpilot URL to scrape
        max_pages (int): Maximum number of pages to scrape
        
    Returns:
        list: List of review dictionaries
    """
    
    reviews = []
    
    # More comprehensive headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    # Create a session to persist cookies
    session = requests.Session()
    session.headers.update(headers)
    
    # Get base URL for constructing full URLs
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    print(f"Scraping reviews from: {url}")
    
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        
        # Construct page URL
        page_url = f"{url}?page={page}" if page > 1 else url
        
        try:
            # Send request with headers to mimic a browser
            response = session.get(page_url, timeout=10)
            response.raise_for_status()
            
            # Check if we got redirected to a challenge page
            if 'captcha' in response.text.lower() or 'challenge' in response.text.lower():
                print("Encountered CAPTCHA or challenge page. Stopping scraping.")
                break
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find review cards - Trustpilot structure
            review_cards = soup.find_all('article', {'data-review-id': True})
            
            # Alternative selectors if the above doesn't work
            if not review_cards:
                review_cards = soup.find_all('div', class_=re.compile('.*reviewCard.*', re.I))
            
            if not review_cards:
                review_cards = soup.find_all('article')
            
            if not review_cards:
                print(f"No reviews found on page {page}")
                # Print a snippet of the page content for debugging
                print(f"Page title: {soup.title.string if soup.title else 'No title'}")
                break
                
            print(f"Found {len(review_cards)} review elements on page {page}")
            
            # Extract data from each review card
            for i, card in enumerate(review_cards):
                try:
                    # Extract review ID
                    review_id = card.get('data-review-id', f'unknown_{i}')
                    if not review_id or review_id == 'unknown_0':
                        # Try alternative ways to get ID
                        review_id = card.get('id', f'unknown_{i}')
                    
                    # Extract rating
                    rating = 0
                    # Look for star rating elements
                    rating_elements = card.find_all(['img', 'div', 'span'], 
                                                   attrs={'alt': re.compile(r'(\d+)\s*out of 5 stars', re.I)})
                    if rating_elements:
                        for elem in rating_elements:
                            alt_text = elem.get('alt', '')
                            rating_match = re.search(r'(\d+)\s*out of 5 stars', alt_text, re.I)
                            if rating_match:
                                rating = int(rating_match.group(1))
                                break
                    
                    # Alternative: look for data-rating attributes
                    if rating == 0:
                        for attr in ['data-rating', 'data-score', 'rating']:
                            rating_attr = card.get(attr)
                            if rating_attr and rating_attr.isdigit():
                                rating = int(rating_attr)
                                break
                    
                    # Extract title
                    title = ''
                    title_elements = card.find_all(['h2', 'h3', 'h4'], 
                                                  attrs={'data-review-title-typography': True})
                    if not title_elements:
                        # Try other common title selectors
                        title_elements = card.find_all(['h2', 'h3', 'h4'], 
                                                     class_=re.compile('.*title.*', re.I))
                    
                    if title_elements:
                        title = title_elements[0].get_text(strip=True)
                    
                    # Extract review text
                    review_text = ''
                    text_elements = card.find_all('p', 
                                                 attrs={'data-review-content-typography': True})
                    if not text_elements:
                        # Try other common text selectors
                        text_elements = card.find_all('p')
                    
                    if text_elements:
                        review_text = text_elements[0].get_text(strip=True)
                    
                    # Extract date
                    date_str = ''
                    date_elements = card.find_all('time')
                    if date_elements:
                        date_str = date_elements[0].get('datetime', 
                                                       date_elements[0].get_text(strip=True))
                    
                    # Extract reviewer name
                    reviewer_name = 'Anonymous'
                    name_elements = card.find_all('span', 
                                                 attrs={'data-consumer-name-typography': True})
                    if not name_elements:
                        name_elements = card.find_all('span', 
                                                    class_=re.compile('.*consumer.*', re.I))
                    
                    if name_elements:
                        reviewer_name = name_elements[0].get_text(strip=True)
                    
                    # Create full review text combining title and content
                    full_text = f"{title} - {review_text}" if title else review_text
                    
                    # Only add reviews with content
                    if full_text.strip() and (title or review_text):
                        reviews.append({
                            'review_id': review_id,
                            'date': date_str,
                            'rating': rating,
                            'review_title': title,
                            'review_text': review_text,
                            'full_text': full_text,
                            'reviewer_name': reviewer_name
                        })
                        
                except Exception as e:
                    print(f"Error parsing review {i} on page {page}: {e}")
                    continue
            
            # Add delay to be respectful to the server
            time.sleep(random.uniform(2, 5))
            
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            break
    
    print(f"Scraped {len(reviews)} reviews in total")
    return reviews

def save_reviews_to_csv(reviews, filename='trustpilot_reviews.csv'):
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
    # Our pipeline expects: date, rating, review_text, review_title (optional)
    try:
        output_df = df[['date', 'rating', 'review_text', 'review_title']].copy()
    except KeyError:
        # If some columns are missing, use what we have
        available_cols = [col for col in ['date', 'rating', 'review_text', 'review_title'] if col in df.columns]
        output_df = df[available_cols].copy()
        # Add missing columns with empty values
        for col in ['date', 'rating', 'review_text', 'review_title']:
            if col not in output_df.columns:
                output_df[col] = ''
    
    # Save to CSV
    output_df.to_csv(filename, index=False)
    print(f"Saved {len(reviews)} reviews to {filename}")

def main():
    """
    Main function to scrape Trustpilot reviews and save to CSV
    """
    # Trustpilot URL for Groww
    url = "https://www.trustpilot.com/review/groww.in"
    
    # Scrape reviews (limiting to 3 pages for demo purposes)
    reviews = scrape_trustpilot_reviews(url, max_pages=3)
    
    # Save to CSV
    if reviews:
        save_reviews_to_csv(reviews, 'groww_trustpilot_reviews.csv')
        print(f"\nSuccess! Scraped {len(reviews)} reviews and saved to groww_trustpilot_reviews.csv")
        
        # Show sample of the data
        print("\nSample of scraped data:")
        df = pd.DataFrame(reviews)
        cols_to_show = [col for col in ['rating', 'review_title', 'review_text'] if col in df.columns]
        if cols_to_show:
            print(df[cols_to_show].head(3))
    else:
        print("No reviews were scraped")
        # Create a sample file for testing
        create_sample_file()

def create_sample_file():
    """
    Create a sample CSV file for testing when scraping fails
    """
    print("\nCreating sample file for testing...")
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
    
    df = pd.DataFrame(sample_data)
    df.to_csv('groww_trustpilot_reviews.csv', index=False)
    print("Created sample file: groww_trustpilot_reviews.csv")

if __name__ == "__main__":
    main()