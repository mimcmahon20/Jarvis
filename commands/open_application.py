import subprocess
import sys
import os

# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

def open_application(app_name):
    """
    Opens an application based on the given app name.
    """
    print("Opening " + app_name)
    speak("Opening " + app_name)
    try:
        # Windows:
        subprocess.Popen(f'start {app_name}', shell=True)
        # MacOS (uncomment if using MacOS):
        # subprocess.Popen(['open', '-a', app_name])
        print(f"Opening {app_name}...")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")