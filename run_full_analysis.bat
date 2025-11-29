@echo off
echo App Review Insights Analyzer - Full Analysis Pipeline
echo =====================================================
echo.

echo Step 1: Generating sample review data...
cd /d "c:\Users\HP\Desktop\Milestone _2.0"
python scrape_playstore.py
echo.

echo Step 2: Combining all review data...
python combine_reviews.py
echo.

echo Step 3: Starting web application...
echo Open your browser and go to http://localhost:5000
echo Press CTRL+C to stop the server
echo.
python app.py

pause