# Real Data Scraping Setup - Complete Guide

## ✅ What's Been Implemented

Your automated email system now scrapes **real reviews** from:
1. **Google Play Store** - Using the `google-play-scraper` library
2. **Trustpilot** - Using web scraping with BeautifulSoup

The system combines reviews from both sources and analyzes them together.

---

## 📊 How It Works

### Weekly Automated Flow (Every Monday 8 AM UTC):

1. **Scrape Play Store** → Fetches 100 most recent reviews from Groww app
2. **Scrape Trustpilot** → Fetches reviews from Groww's Trustpilot page
3. **Combine Data** → Merges both sources into one dataset
4. **Analyze** → Runs sentiment analysis and theme tagging
5. **Generate Report** → Creates weekly pulse note
6. **Send Email** → Delivers report to your inbox

---

## 🔧 Configuration

### App IDs Currently Set:
- **Play Store**: `com.nextbillion.groww` (Official Groww app)
- **Trustpilot**: `https://www.trustpilot.com/review/groww.in`

### To Change App or Add More Sources:

Edit `run_weekly_job.py`:

```python
# Line 44: Change Play Store app
playstore_app_id = "com.your.app.id"

# Line 49: Change Trustpilot URL
trustpilot_url = "https://www.trustpilot.com/review/your-company"
```

---

## 🧪 Testing Locally

### Test Play Store Scraper:
```bash
python scrape_playstore_real.py
```

### Test Trustpilot Scraper:
```bash
python scrape_trustpilot.py
```

### Test Full Pipeline:
```bash
python run_weekly_job.py
```

---

## 📈 Scraping Limits

### Play Store:
- **Current**: 100 reviews per run
- **Max recommended**: 200 (to avoid rate limiting)
- **Sorting**: Newest first

### Trustpilot:
- **Current**: 3 pages (~60 reviews)
- **Max recommended**: 10 pages
- **Note**: May encounter CAPTCHA if too aggressive

### To Adjust Limits:

In `run_weekly_job.py`:
```python
# Line 44: Increase Play Store reviews
playstore_reviews = scrape_playstore_reviews_real(playstore_app_id, count=200)

# Line 49: Increase Trustpilot pages
trustpilot_reviews = scrape_trustpilot_reviews(trustpilot_url, max_pages=10)
```

---

## ⚠️ Important Notes

### 1. Rate Limiting
- Play Store: Generally reliable, but don't exceed 500 reviews per run
- Trustpilot: May block if you scrape too frequently (use delays)

### 2. Data Quality
- Play Store reviews are always fresh and reliable
- Trustpilot may occasionally fail due to:
  - CAPTCHA challenges
  - Website structure changes
  - Network issues

### 3. Fallback Behavior
If scraping fails, the system will:
- Print an error message
- Fall back to sample data (for testing)
- Still generate and send a report

---

## 🔄 Updating Dependencies

If you need to update the scraping library:

```bash
pip install --upgrade google-play-scraper
```

Then update `requirements.txt` and push to GitHub.

---

## 📝 Next Steps (Optional Enhancements)

1. **Add More Sources**:
   - App Store (iOS) reviews
   - Twitter/X mentions
   - Reddit discussions

2. **Improve Data Quality**:
   - Filter out spam reviews
   - Deduplicate across sources
   - Add language detection

3. **Advanced Analytics**:
   - Trend analysis (week-over-week)
   - Competitor comparison
   - Custom theme categories

4. **Real LLM Integration**:
   - Replace mock LLM with OpenAI/Gemini API
   - Better sentiment analysis
   - More accurate theme tagging

---

## 🆘 Troubleshooting

### "No reviews fetched"
- Check internet connection
- Verify app ID is correct
- Try reducing count/pages

### "CAPTCHA encountered"
- Reduce Trustpilot pages to 1-2
- Add longer delays between requests
- Consider using a proxy service

### "Email not sent"
- Check GitHub Secrets are set
- Verify App Password is valid
- Check spam folder

---

## 📧 Support

If you encounter issues, check:
1. GitHub Actions logs (Actions tab)
2. Local test output
3. Error messages in email reports

---

**Last Updated**: December 1, 2025
**Version**: 2.0 (Real Data Scraping)
