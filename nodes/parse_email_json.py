"""
Node: Extract JSON (Optional Python Helper)
Node name: Parse_Email_JSON
Type: Python Transform
Input: weekly_note_and_email (one-row text)
Output columns: weekly_note_md, email_subject, email_body
"""

import pandas as pd
import json
import re

def parse_email_json(input_df):
    """
    Parse JSON from weekly note and email content.
    
    Args:
        input_df (pandas.DataFrame): DataFrame containing weekly note and email content
        
    Returns:
        pandas.DataFrame: Parsed components (note, subject, body)
    """
    # Get the text content (assuming it's in the first cell of the first column)
    text = input_df.iloc[0, 0] if not input_df.empty else ""
    
    # Split note and JSON parts
    # Find the last occurrence of '{' to locate the start of JSON
    json_start = text.rfind("{")
    
    if json_start != -1:
        note_part = text[:json_start].strip()
        json_part = text[json_start:]
        
        try:
            # Parse JSON
            data = json.loads(json_part)
            
            # Create output dataframe
            output_df = pd.DataFrame([{
                "weekly_note_md": note_part,
                "email_subject": data.get("email_subject", ""),
                "email_body": data.get("email_body", "")
            }])
            
            return output_df
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return the entire text as the note
            output_df = pd.DataFrame([{
                "weekly_note_md": text,
                "email_subject": "",
                "email_body": ""
            }])
            return output_df
    else:
        # If no JSON found, return the entire text as the note
        output_df = pd.DataFrame([{
            "weekly_note_md": text,
            "email_subject": "",
            "email_body": ""
        }])
        return output_df

# Example usage
if __name__ == "__main__":
    # Sample input data (simulating the output from LLM_Weekly_Pulse)
    sample_note_and_email = """Groww App – Weekly Review Pulse (Week of 2025-11-17)

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

{
  "email_subject": "Weekly App Review Pulse - 2025-11-17",
  "email_body": "Groww App – Weekly Review Pulse (Week of 2025-11-17)\\n\\n• Executive summary\\n  - This week saw mixed feedback with performance issues being a key concern\\n  - Onboarding experience received positive feedback from new users\\n  - Payment-related features showed improvement compared to last week\\n\\n• Top Themes\\n  1. App Performance & Bugs: Several users reported crashes and slow loading times. \\"App keeps freezing when I try to access my portfolio.\\"\\n  2. Onboarding & KYC: New users found the registration process smooth. \\"Easy to sign up and verify my identity.\\"\\n  3. Payments & SIP: Users appreciated the streamlined payment process. \\"SIP setup was straightforward and quick.\\"\\n\\n[Action] Investigate and resolve app performance issues reported by multiple users\\n[Action] Enhance the payment confirmation flow based on user feedback\\n[Action] Optimize the onboarding flow for better conversion rates"
}
"""
    
    input_df = pd.DataFrame([{"content": sample_note_and_email}])
    output_df = parse_email_json(input_df)
    
    print("Parsed email components:")
    print(f"Weekly Note: {output_df['weekly_note_md'].iloc[0][:100]}...")
    print(f"Email Subject: {output_df['email_subject'].iloc[0]}")
    print(f"Email Body: {output_df['email_body'].iloc[0][:100]}...")