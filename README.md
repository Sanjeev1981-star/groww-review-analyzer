# 📊 Groww App Review Insights Analyzer

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/yourusername/groww-review-analyzer)

An AI-powered web application that transforms **Groww app store reviews** into actionable insights through automated analysis, theme extraction, and weekly pulse reports.

![Groww Analyzer](https://img.shields.io/badge/Groww-Review%20Analyzer-00d09c?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgM0gxMVYxMUgzVjNaTTEzIDNIMjFWMTFIMTNWM1pNMyAxM0gxMVYyMUgzVjEzWk0xMyAxM0gyMVYyMUgxM1YxM1oiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPg==)

---

## 🎯 Project Overview

This milestone project builds an **App Review Insights Analyzer** that processes 8-12 weeks of App Store and Play Store reviews, transforming them into weekly one-page pulse reports with:

- 🎨 **Theme Extraction**: Automatically identifies top 5 recurring themes
- 💬 **Sentiment Analysis**: Classifies reviews as Positive, Neutral, or Negative
- 💡 **Actionable Insights**: Generates specific recommendations for product improvement
- 📧 **Email Drafts**: Creates ready-to-send summary emails for stakeholders
- 🌐 **Web Interface**: Modern, Groww-branded UI for easy access
- 🔄 **Auto-Update**: Scheduled review scraping and analysis

---

## 📂 Project Structure

```
Groww-Review-Analyzer/
├── app.py                          # Flask web application
├── main_pipeline.py                # Core analysis pipeline
├── requirements.txt                # Python dependencies
│
├── nodes/                          # Analysis pipeline nodes
│   ├── Clean_And_Bucket.py        # Data cleaning & weekly bucketing
│   ├── Theme.py                   # ML-based theme extraction
│   ├── Summarize.py               # Theme summarization
│   ├── Sentiment.py               # Sentiment analysis
│   ├── Quote.py                   # Representative quote extraction
│   ├── Insight.py                 # Actionable insight generation
│   └── Email.py                   # Email draft creation
│
├── templates/                      # HTML templates (Groww-branded)
│   ├── index.html                 # Main upload page
│   ├── results.html               # Analysis results display
│   └── showcase.html              # Feature showcase
│
├── static/                         # CSS, JS, and assets
│   └── custom.css                 # Groww green theme styling
│
├── scrape_playstore.py            # Google Play Store scraper
├── scrape_trustpilot.py           # Trustpilot review scraper
├── auto_update_reviews.py         # Automated review updates
│
├── sample_reviews.csv             # Sample review data
├── Weekly_Pulse_Report_Sample.md  # Sample weekly report
└── Email_Draft_Sample.md          # Sample email draft
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/groww-review-analyzer.git
cd groww-review-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the web application**
```bash
python app.py
```

4. **Open your browser**
```
http://localhost:5000
```

### Windows Users
You can also use the provided batch files:
```bash
start_app.bat          # Start the web application
run_full_analysis.bat  # Run complete analysis pipeline
```

---

## 💻 Usage

### Web Interface

1. **Update Reviews** (Optional)
   - Click "Generate Fresh Reviews" to scrape latest reviews from Trustpilot/Play Store
   - System generates sample data (direct scraping blocked by anti-bot measures)

2. **Upload CSV File**
   - Drag & drop or browse to select a CSV file with reviews
   - Required columns: `date`, `rating`, `review_text`, `review_title`

3. **Analyze**
   - Click "Analyze Groww Reviews"
   - View results including themes, sentiment, insights, and email draft

4. **Download Sample**
   - Use the sample CSV to test the analyzer

### Command Line

```bash
# Run full analysis pipeline
python main_pipeline.py

# Scrape fresh reviews
python scrape_playstore.py
python scrape_trustpilot.py

# Auto-update reviews (scheduled)
python auto_update_reviews.py
```

---

## 📊 Sample Outputs

### 📄 Weekly Pulse Report
A comprehensive one-page report including:
- Executive summary with key metrics
- Top 5 themes with sentiment breakdown
- Representative user quotes
- Actionable recommendations (Critical, Important, Backlog)
- Week-over-week trend analysis

**📥 View Sample:** [Weekly_Pulse_Report_Sample.md](Weekly_Pulse_Report_Sample.md)

### 📧 Email Draft
Ready-to-send email for stakeholders featuring:
- TL;DR summary
- Quick stats table
- Top themes with action items
- Team-specific next steps
- Attached reports and data

**📥 View Sample:** [Email_Draft_Sample.md](Email_Draft_Sample.md)

### 📁 Sample Review Data
Redacted sample CSV with real review structure:
- Date: 2025-11-17 to 2025-11-24
- Ratings: 1-5 stars
- Review text and titles
- 267 reviews covering various themes

**📥 Download:** [sample_reviews.csv](sample_reviews.csv)

---

## 🎨 Features

### 1. **Automated Data Pipeline**
```
Raw Reviews → Clean & Bucket → Theme Extraction → Sentiment Analysis → 
Insight Generation → Email Draft Creation → Output Reports
```

### 2. **ML-Powered Analysis**
- **TF-IDF Vectorization**: Converts text to numerical features
- **K-Means Clustering**: Groups similar reviews into themes
- **Sentiment Classification**: Rule-based sentiment scoring
- **Smart Summarization**: Extracts key points from each theme

### 3. **Groww-Branded UI**
- Modern gradient design with Groww's signature green (#00d09c)
- Responsive layout for all devices
- Drag-and-drop file upload
- Real-time loading states
- Interactive hover effects

### 4. **Automated Scraping**
- Trustpilot review scraper
- Google Play Store review scraper
- Scheduled auto-updates
- CSV export functionality

---

## 🔧 Configuration

### Review Sources
Edit scraping scripts to customize:
- URL targets
- Review count limits
- Date ranges
- Rating filters

### Theme Extraction
Adjust in `nodes/Theme.py`:
```python
num_themes = 5          # Number of themes to extract
max_features = 100      # TF-IDF feature limit
min_reviews_per_theme = 3  # Minimum reviews for valid theme
```

### Web Server
Modify in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 📈 Pipeline Nodes

| Node | Input | Output | Function |
|------|-------|--------|----------|
| **Clean_And_Bucket** | `reviews_raw.csv` | `reviews_clean.csv` | Removes duplicates, handles missing data, adds week buckets |
| **Theme** | `reviews_clean.csv` | `themes.csv` | Extracts top 5 themes using K-means clustering |
| **Summarize** | `themes.csv` | `theme_summaries.csv` | Generates concise summaries for each theme |
| **Sentiment** | `reviews_clean.csv` | `sentiment_scores.csv` | Analyzes sentiment (Positive/Neutral/Negative) |
| **Quote** | `reviews_clean.csv` | `representative_quotes.csv` | Selects best representative quotes per theme |
| **Insight** | All above | `insights.csv` | Generates actionable recommendations |
| **Email** | All above | `email_draft.txt` | Creates stakeholder email summary |

---

## 🛠️ Technologies Used

- **Backend**: Python 3.7+, Flask 2.0
- **Data Processing**: pandas, NumPy
- **Machine Learning**: scikit-learn (TF-IDF, K-Means)
- **Web Scraping**: BeautifulSoup4, requests
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5, Font Awesome, Custom CSS
- **Scheduling**: schedule library

---

## 📊 Sample Analysis Results

### Metrics from Sample Data (Nov 17-24, 2025)
- **Total Reviews**: 267
- **Average Rating**: 3.8/5.0
- **Sentiment Distribution**: 45% Positive, 30% Neutral, 25% Negative

### Top Themes Identified
1. **Performance & Stability** (35%)
2. **User Interface & Experience** (28%)
3. **Feature Requests** (20%)
4. **Customer Support** (10%)
5. **Security & Trust** (7%)

---

## 🔄 Automatic Updates

The system supports scheduled automatic review updates:

```bash
# Run auto-update service
python auto_update_reviews.py
```

Default schedule: Daily at 2:00 AM

Customize in `setup_automatic_task.py`:
```python
schedule.every().day.at("02:00").do(update_job)
```

---

## 🎯 Use Cases

1. **Product Teams**: Identify feature requests and pain points
2. **Engineering**: Prioritize bug fixes based on user impact
3. **Customer Success**: Understand support bottlenecks
4. **Marketing**: Track brand sentiment and competitive positioning
5. **Leadership**: Weekly pulse on product health

---

## 📝 CSV Format Requirements

Your review CSV must include these columns:

```csv
date,rating,review_text,review_title
2025-11-17,5,"Great app! Easy to use.",Excellent App
2025-11-18,3,"Could be better.",Needs Improvement
```

- **date**: YYYY-MM-DD format
- **rating**: Integer 1-5
- **review_text**: String (main review content)
- **review_title**: String (optional, can be empty)

---

## 🐛 Troubleshooting

### Issue: App won't start
```bash
# Check Python version
python --version  # Should be 3.7+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Colors not showing (browser cache)
```
Press Ctrl + Shift + R (Windows/Linux)
Press Cmd + Shift + R (Mac)
```

### Issue: Scraping fails
- Expected behavior: Direct scraping blocked by anti-bot measures
- Solution: System generates realistic sample data instead

---

## 🚀 Future Enhancements

- [ ] Real-time scraping with proxy rotation
- [ ] Multi-language support for international reviews
- [ ] Deep learning models for advanced theme detection
- [ ] Competitor comparison analysis
- [ ] Interactive data visualization dashboard
- [ ] Export to PowerPoint/PDF formats
- [ ] Slack/Teams integration for automated reports
- [ ] A/B testing impact analysis

---

## 📸 Screenshots

### Main Dashboard
![Dashboard](https://via.placeholder.com/800x400/00d09c/ffffff?text=Groww+App+Review+Insights+Analyzer)

### Analysis Results
![Results](https://via.placeholder.com/800x400/00d09c/ffffff?text=Analysis+Results+with+Themes+and+Insights)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Groww for inspiration
- Flask documentation and community
- scikit-learn for ML capabilities
- Bootstrap for responsive UI components

---

## 📞 Support

For questions or issues:
1. Check existing [GitHub Issues](https://github.com/yourusername/groww-review-analyzer/issues)
2. Create a new issue with detailed description
3. Reach out via email for urgent matters

---

<div align="center">

**⭐ Star this repository if you find it helpful! ⭐**

*Built with ❤️ for better product insights*

[![GitHub stars](https://img.shields.io/github/stars/yourusername/groww-review-analyzer.svg?style=social&label=Star)](https://github.com/yourusername/groww-review-analyzer)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/groww-review-analyzer.svg?style=social&label=Fork)](https://github.com/yourusername/groww-review-analyzer/fork)

</div>
