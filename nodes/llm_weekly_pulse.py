"""
Node: LLM – Build Weekly One-Page Note (≤250 words)
Node name: LLM_Weekly_Pulse
Type: LLM – Table → Text
Inputs:
themes_week_stats (as table)
reviews_week_tagged (as table)
Output: plain text weekly_note_and_email (we'll include JSON at the end)
"""

import pandas as pd

# Mock LLM function - in a real implementation, this would call an actual LLM API
def mock_llm_call(system_prompt, user_prompt):
    """
    Mock LLM function that simulates generating a weekly pulse note.
    In a real implementation, this would call an actual LLM API.
    """
    # This is a simplified mock implementation
    # In reality, you would send the prompts to an LLM and parse the response
    
    # Extract week start from user prompt
    lines = user_prompt.split('\n')
    week_start = "2025-11-17"  # Default value
    for line in lines:
        if line.startswith("Week starting:"):
            week_start = line.replace("Week starting:", "").strip()
            break
    
    # Create a mock response based on the input data
    mock_response = f"""Groww App – Weekly Review Pulse (Week of {week_start})

• Executive summary
  - This week saw mixed feedback with performance issues being a key concern
  - Onboarding experience received positive feedback from new users
  - Payment-related features showed improvement compared to last week

• Top Themes
  1. App Performance & Bugs: Several users reported crashes and slow loading times. "App keeps freezing when I try to access my portfolio."
  2. Onboarding & KYC: New users found the registration process smooth. "Easy to sign up and verify my identity."
  3. Payments & SIP: Users appreciated the streamlined payment process. "SIP setup was straightforward and quick."

[Action] Investigate and resolve app performance issues reported by multiple users
[Action] Enhance the payment confirmation flow based on user feedback
[Action] Optimize the onboarding flow for better conversion rates

{{
  "email_subject": "Weekly App Review Pulse - {week_start}",
  "email_body": "Groww App – Weekly Review Pulse (Week of {week_start})\\n\\n• Executive summary\\n  - This week saw mixed feedback with performance issues being a key concern\\n  - Onboarding experience received positive feedback from new users\\n  - Payment-related features showed improvement compared to last week\\n\\n• Top Themes\\n  1. App Performance & Bugs: Several users reported crashes and slow loading times. \\"App keeps freezing when I try to access my portfolio.\\"\\n  2. Onboarding & KYC: New users found the registration process smooth. \\"Easy to sign up and verify my identity.\\"\\n  3. Payments & SIP: Users appreciated the streamlined payment process. \\"SIP setup was straightforward and quick.\\"\\n\\n[Action] Investigate and resolve app performance issues reported by multiple users\\n[Action] Enhance the payment confirmation flow based on user feedback\\n[Action] Optimize the onboarding flow for better conversion rates"
}}
"""
    
    return mock_response

def llm_weekly_pulse(themes_week_stats_df, reviews_week_tagged_df, target_week_start):
    """
    Generate weekly pulse note using LLM.
    
    Args:
        themes_week_stats_df (pandas.DataFrame): Theme statistics
        reviews_week_tagged_df (pandas.DataFrame): Tagged reviews
        target_week_start (str): Target week start date
        
    Returns:
        str: Weekly note and email content
    """
    # Convert dataframes to markdown tables for LLM prompt
    themes_table = themes_week_stats_df.to_markdown(index=False) if hasattr(themes_week_stats_df, 'to_markdown') else themes_week_stats_df.to_string()
    
    # Limit reviews to ~150 rows as specified
    limited_reviews_df = reviews_week_tagged_df.head(150)
    reviews_table = limited_reviews_df.to_markdown(index=False) if hasattr(limited_reviews_df, 'to_markdown') else limited_reviews_df.to_string()
    
    # System prompt
    system_prompt = """You are writing a weekly product pulse for the Groww app, for product, growth, support, and leadership.

Constraints:
- Max 5 themes overall.
- Weekly note must be ≤250 words.
- Use real user quotes, but paraphrase lightly and REMOVE any usernames, emails, phone numbers, or IDs.
- Output: (1) a readable note, (2) a JSON block for email subject & body.

User prompt:
Week starting: target_week_start

Theme stats:
themes_week_stats_table

Tagged reviews (theme, sentiment, rating, full_text, summary_1line):
reviews_week_tagged_table

Task:
1. Pick the **Top 3 themes** (by review volume and/or negative share).
2. For the weekly note (≤250 words total), write:

"Groww App – Weekly Review Pulse (Week of target_week_start)"

- 2–3 bullet **Executive summary**
- A short section **Top Themes**:
  - 3 themes, each with:
    - 1–2 sentence summary
    - 1 short user quote (paraphrased, no PII)
- **3 action ideas** total (label each `[Action]`).

3. After the note, output a JSON block:

{
  "email_subject": "<short subject line>",
  "email_body": "<plain-text email body including the note>"
}

Rules:
- Do NOT exceed 250 words for the note.
- Do NOT include any usernames, emails, phone numbers, or IDs."""

    # User prompt
    user_prompt = f"""Week starting: {target_week_start}

Theme stats:
{themes_table}

Tagged reviews (theme, sentiment, rating, full_text, summary_1line):
{reviews_table}

Task:
1. Pick the **Top 3 themes** (by review volume and/or negative share).
2. For the weekly note (≤250 words total), write:

"Groww App – Weekly Review Pulse (Week of {target_week_start})"

- 2–3 bullet **Executive summary**
- A short section **Top Themes**:
  - 3 themes, each with:
    - 1–2 sentence summary
    - 1 short user quote (paraphrased, no PII)
- **3 action ideas** total (label each `[Action]`).

3. After the note, output a JSON block:

{{
  "email_subject": "<short subject line>",
  "email_body": "<plain-text email body including the note>"
}}

Rules:
- Do NOT exceed 250 words for the note.
- Do NOT include any usernames, emails, phone numbers, or IDs."""

    # Call LLM (mock implementation)
    response = mock_llm_call(system_prompt, user_prompt)
    
    return response

# Example usage
if __name__ == "__main__":
    # Sample theme stats data
    theme_stats_data = {
        "theme": [
            "App Performance & Bugs",
            "Onboarding & KYC",
            "Payments & SIP"
        ],
        "review_count": [15, 8, 12],
        "avg_rating": [2.3, 4.5, 3.8],
        "negative_count": [10, 1, 3],
        "neg_share": [0.67, 0.12, 0.25]
    }
    
    themes_week_stats_df = pd.DataFrame(theme_stats_data)
    
    # Sample tagged reviews data
    reviews_data = {
        "theme": [
            "App Performance & Bugs",
            "App Performance & Bugs",
            "Onboarding & KYC",
            "Payments & SIP"
        ],
        "sentiment": [
            "NEGATIVE",
            "NEGATIVE",
            "POSITIVE",
            "MIXED"
        ],
        "rating": [1, 2, 5, 3],
        "full_text": [
            "App keeps crashing every time I open it",
            "Very slow performance, takes forever to load",
            "Registration was quick and easy",
            "Payment process works but could be faster"
        ],
        "summary_1line": [
            "App crashes frequently",
            "Slow performance issues",
            "Smooth registration process",
            "Payment process needs improvement"
        ]
    }
    
    reviews_week_tagged_df = pd.DataFrame(reviews_data)
    target_week_start = "2025-11-17"
    
    output_text = llm_weekly_pulse(themes_week_stats_df, reviews_week_tagged_df, target_week_start)
    
    print("Weekly pulse note:")
    print(output_text)