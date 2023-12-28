import subprocess
import sys
import os

# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

def open_application(app_name):
    print("Opening " + app_name)
    speak("Opening " + app_name)

    app_path = ""
    app_name_lower = app_name.lower()

    # Known aliases or special cases
    if app_name_lower == "file explorer":
        app_path = 'explorer'
    elif app_name_lower == "chrome":
        app_path = 'start chrome'
    elif app_name_lower == "spotify":
        app_path = 'start spotify'
    else:
        # Default case: construct a path for the .exe file
        # You can add more common directories here
        common_paths = [
            f"C:\\Program Files\\{app_name}\\{app_name}.exe",
            f"C:\\Program Files (x86)\\{app_name}\\{app_name}.exe",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{app_name}\\{app_name}.exe"
        ]
        for path in common_paths:
            if os.path.exists(path):
                app_path = f'"{path}"'
                break

    try:
        if app_path:
            subprocess.Popen(app_path, shell=True)
            print(f"Opening {app_name}...")
        else:
            print(f"Executable for {app_name} not found.")
            speak(f"Executable for {app_name} not found.")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        speak(f"Error opening {app_name}")