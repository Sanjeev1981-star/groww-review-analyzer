"""
Deployment script for the App Review Insights Analyzer
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'templates']
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    """Main deployment function"""
    print("Deploying App Review Insights Analyzer...")
    
    # Install requirements
    install_requirements()
    
    # Setup directories
    setup_directories()
    
    # Start the application
    print("Starting the application...")
    print("Open your browser and go to http://localhost:5000")
    
    # Run the Flask app
    os.system("python app.py")

if __name__ == "__main__":
    main()