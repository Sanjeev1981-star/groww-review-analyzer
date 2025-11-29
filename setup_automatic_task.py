"""
Script to set up automatic task scheduling for review updates
"""

import os
import sys
import subprocess

def setup_windows_task():
    """
    Set up a Windows Task Scheduler task for automatic review updates
    """
    print("Setting up automatic review updates with Windows Task Scheduler...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "auto_update_reviews.py")
    
    # Create a batch file for the task
    task_script = os.path.join(current_dir, "scheduled_update.bat")
    with open(task_script, "w") as f:
        f.write("@echo off\n")
        f.write(f'cd /d "{current_dir}"\n')
        f.write(f'python "{script_path}"\n')
    
    print(f"Created task script: {task_script}")
    
    # Set up the scheduled task using schtasks
    task_name = "AppReviewInsightsUpdater"
    task_command = f'schtasks /create /tn "{task_name}" /tr "{task_script}" /sc daily /st 02:00'
    
    try:
        result = subprocess.run(task_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Successfully created scheduled task: {task_name}")
            print("  The task will run daily at 2:00 AM")
        else:
            print(f"✗ Failed to create scheduled task: {result.stderr}")
    except Exception as e:
        print(f"✗ Error setting up scheduled task: {e}")
    
    print("\nTo manually run the task:")
    print(f'  schtasks /run /tn "{task_name}"')
    
    print("\nTo delete the task:")
    print(f'  schtasks /delete /tn "{task_name}" /f')

def setup_linux_cron():
    """
    Set up a cron job for automatic review updates (Linux/Mac)
    """
    print("Setting up automatic review updates with cron...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "auto_update_reviews.py")
    
    # Create the cron job entry
    cron_entry = f"0 2 * * * cd '{current_dir}' && python '{script_path}'\n"
    
    # Add to crontab
    try:
        # Get current crontab
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_crontab = result.stdout
        
        # Check if our entry already exists
        if "auto_update_reviews.py" in current_crontab:
            print("✓ Cron job already exists")
        else:
            # Add our entry
            new_crontab = current_crontab + cron_entry
            process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
            process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                print("✓ Successfully added cron job")
                print("  The job will run daily at 2:00 AM")
            else:
                print("✗ Failed to add cron job")
                
    except Exception as e:
        print(f"✗ Error setting up cron job: {e}")
        print("  You may need to manually add this entry to your crontab:")
        print(f"  {cron_entry}")

def main():
    """
    Main function to set up automatic scheduling
    """
    print("Automatic Review Update Setup")
    print("=" * 30)
    
    # Detect OS
    if sys.platform.startswith("win"):
        setup_windows_task()
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        setup_linux_cron()
    else:
        print("Unsupported operating system")
        print("Please set up scheduling manually")

if __name__ == "__main__":
    main()