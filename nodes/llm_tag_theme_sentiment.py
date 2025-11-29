"""
Node: LLM – Tag Theme + Sentiment Per Review
Node name: LLM_Tag_Theme_Sentiment
Type: LLM – Map over rows
Input: reviews_week
Output columns: theme, sentiment, summary_1line
"""

import pandas as pd
import json

# Mock LLM function - in a real implementation, this would call an actual LLM API
def mock_llm_call(prompt):
    """
    Mock LLM function that simulates tagging themes and sentiment.
    In a real implementation, this would call an actual LLM API.
    """
    # This is a simplified mock implementation
    # In reality, you would send the prompt to an LLM and parse the response
    
    # Extract review text from prompt (simplified approach)
    lines = prompt.split('\n')
    review_text = ""
    rating = 0
    
    for line in lines:
        if line.startswith("Review text:"):
            review_text = line.replace("Review text:", "").strip()
        elif line.startswith("Rating:"):
            try:
                rating = int(line.replace("Rating:", "").strip())
            except:
                rating = 0
    
    # Simple rule-based tagging for demo purposes
    if "kyc" in review_text.lower() or "onboard" in review_text.lower() or "register" in review_text.lower():
        theme = "Onboarding & KYC"
    elif "payment" in review_text.lower() or "sip" in review_text.lower() or "transaction" in review_text.lower():
        theme = "Payments & SIP"
    elif "withdraw" in review_text.lower() or "payout" in review_text.lower():
        theme = "Withdrawals & Payouts"
    elif "statement" in review_text.lower() or "report" in review_text.lower():
        theme = "Statements & Reports"
    else:
        theme = "App Performance & Bugs"
    
    # Simple sentiment analysis based on rating and keywords
    if rating >= 4:
        sentiment = "POSITIVE"
    elif rating <= 2:
        sentiment = "NEGATIVE"
    else:
        # Check for sentiment keywords
        negative_words = ["frustrating", "crash", "slow", "issue", "problem", "bad"]
        positive_words = ["great", "good", "excellent", "love", "amazing", "perfect"]
        
        neg_count = sum(1 for word in negative_words if word in review_text.lower())
        pos_count = sum(1 for word in positive_words if word in review_text.lower())
        
        if neg_count > pos_count:
            sentiment = "NEGATIVE"
        elif pos_count > neg_count:
            sentiment = "POSITIVE"
        else:
            sentiment = "NEUTRAL"
    
    # Create a simple summary
    summary = review_text[:50] + "..." if len(review_text) > 50 else review_text
    
    return {
        "theme": theme,
        "sentiment": sentiment,
        "summary_1line": summary
    }

def llm_tag_theme_sentiment(input_df):
    """
    Tag theme and sentiment for each review using LLM.
    
    Args:
        input_df (pandas.DataFrame): DataFrame containing reviews for the target week
        
    Returns:
        pandas.DataFrame: DataFrame with added theme, sentiment, and summary columns
    """
    df = input_df.copy()
    
    # System prompt
    system_prompt = """You are an insights analyst for the Groww app.

You read app reviews and assign:
- ONE theme label from this legend:
  1) Onboarding & KYC
  2) Payments & SIP
  3) Withdrawals & Payouts
  4) Statements & Reports
  5) App Performance & Bugs

If nothing fits perfectly, choose the closest theme.

Sentiment must be exactly one of:
- POSITIVE
- NEGATIVE
- MIXED
- NEUTRAL

Never include or invent PII like names, emails, phone numbers, or IDs."""
    
    # Process each row
    themes = []
    sentiments = []
    summaries = []
    
    for _, row in df.iterrows():
        # Create user prompt
        user_prompt = f"""Review text:
"{row['full_text']}"

Rating: {row['rating']}

Task:
1. Choose ONE theme from:
   - Onboarding & KYC
   - Payments & SIP
   - Withdrawals & Payouts
   - Statements & Reports
   - App Performance & Bugs

2. Choose ONE sentiment: POSITIVE, NEGATIVE, MIXED, NEUTRAL.
3. Write ONE 1-line summary in plain English. Do not include PII.

Return ONLY valid JSON:

{{
  "theme": "<one of the 5 themes>",
  "sentiment": "<POSITIVE/NEGATIVE/MIXED/NEUTRAL>",
  "summary_1line": "<1-line summary>"
}}"""
        
        # Call LLM (mock implementation)
        result = mock_llm_call(user_prompt)
        
        themes.append(result["theme"])
        sentiments.append(result["sentiment"])
        summaries.append(result["summary_1line"])
    
    # Add results to dataframe
    df["theme"] = themes
    df["sentiment"] = sentiments
    df["summary_1line"] = summaries
    
    return df

# Example usage
if __name__ == "__main__":
    # Sample input data
    sample_data = {
        "date": ["2025-11-17", "2025-11-18", "2025-11-19"],
        "rating": [5, 3, 1],
        "review_text": [
            "Great app! Easy to use and navigate.",
            "Could be better, some features are missing.",
            "App keeps crashing, very frustrating."
        ],
        "full_text": [
            "Great app! Easy to use and navigate.",
            "Could be better, some features are missing.",
            "App keeps crashing, very frustrating."
        ],
        "week_start": ["2025-11-17", "2025-11-17", "2025-11-17"]
    }
    
    input_df = pd.DataFrame(sample_data)
    output_df = llm_tag_theme_sentiment(input_df)
    
    print("Reviews tagged with themes and sentiment:")
    print(output_df[["full_text", "theme", "sentiment", "summary_1line"]])