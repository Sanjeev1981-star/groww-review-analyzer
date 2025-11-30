"""
Flask web application for the App Review Insights Analyzer
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename
from nodes.upload_reviews import upload_reviews
from nodes.clean_and_bucket import clean_and_bucket
from nodes.filter_target_week import filter_target_week
from nodes.llm_tag_theme_sentiment import llm_tag_theme_sentiment
from nodes.theme_stats import theme_stats
from nodes.llm_weekly_pulse import llm_weekly_pulse
from nodes.parse_email_json import parse_email_json
import subprocess
import sys

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Serve static files
app.static_folder = 'static'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file is present in request
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    # Check if file type is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Store filepath in session or pass as parameter
        return redirect(url_for('analyze', filename=filename))
    else:
        flash('Invalid file type. Please upload a CSV file.')
        return redirect(request.url)

@app.route('/analyze')
def analyze():
    filename = request.args.get('filename')
    if not filename:
        flash('No file specified')
        return redirect(url_for('index'))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if file exists
    if not os.path.exists(filepath):
        flash('File not found')
        return redirect(url_for('index'))
    
    # Get target week from query parameters or use default
    target_week = request.args.get('week', '2025-11-17')
    
    try:
        # Run the analysis pipeline
        reviews_raw = upload_reviews(filepath)
        reviews_clean = clean_and_bucket(reviews_raw)
        reviews_week = filter_target_week(reviews_clean, target_week)
        reviews_week_tagged = llm_tag_theme_sentiment(reviews_week)
        themes_week_stats = theme_stats(reviews_week_tagged)
        weekly_note_and_email = llm_weekly_pulse(themes_week_stats, reviews_week_tagged, target_week)
        email_df = pd.DataFrame([{"content": weekly_note_and_email}])
        parsed_email = parse_email_json(email_df)
        
        # Store results for display
        results = {
            "filename": filename,
            "target_week": target_week,
            "total_reviews": len(reviews_raw),
            "filtered_reviews": len(reviews_week),
            "themes_stats": themes_week_stats.to_dict('records'),
            "weekly_note": parsed_email.iloc[0]['weekly_note_md'],
            "email_subject": parsed_email.iloc[0]['email_subject'],
            "email_body": parsed_email.iloc[0]['email_body']
        }
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/download_sample')
def download_sample():
    # Create a sample CSV file for download
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
    
    sample_df = pd.DataFrame(sample_data)
    sample_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_reviews.csv')
    sample_df.to_csv(sample_path, index=False)
    
    return send_file(sample_path, as_attachment=True, download_name='sample_reviews.csv')

@app.route('/update_reviews', methods=['POST'])
def update_reviews_endpoint():
    """
    Endpoint to manually trigger review updates
    """
    try:
        # Run the auto update script
        script_path = os.path.join(os.path.dirname(__file__), 'auto_update_reviews.py')
        result = subprocess.run([
            sys.executable, 
            script_path
        ], capture_output=True, text=True, input='3')  # Option 3 for manual update only
        
        if result.returncode == 0:
            return jsonify({
                "status": "success", 
                "message": "Reviews updated successfully",
                "output": result.stdout
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to update reviews",
                "error": result.stderr
            })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error updating reviews: {str(e)}"
        })

@app.route('/api/update_reviews', methods=['GET'])
def api_update_reviews():
    """
    API endpoint to trigger review updates
    """
    try:
        # Run the Play Store scraper
        scraper_path = os.path.join(os.path.dirname(__file__), 'scrape_playstore.py')
        result1 = subprocess.run([
            sys.executable, 
            scraper_path
        ], capture_output=True, text=True)
        
        # Run the combiner
        combiner_path = os.path.join(os.path.dirname(__file__), 'combine_reviews.py')
        result2 = subprocess.run([
            sys.executable, 
            combiner_path
        ], capture_output=True, text=True)
        
        if result1.returncode == 0 and result2.returncode == 0:
            return jsonify({
                "status": "success", 
                "message": "Reviews updated successfully"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to update reviews",
                "errors": {
                    "scraper": result1.stderr if result1.returncode != 0 else None,
                    "combiner": result2.stderr if result2.returncode != 0 else None
                }
            })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error updating reviews: {str(e)}"
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)