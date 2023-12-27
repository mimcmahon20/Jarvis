import speech_recognition as sr
import subprocess
from speech_output import speak

def listen_for_command():
    """
    Listens for a spoken command and converts it to text.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            process_command(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            print("Sorry, there was an error in speech recognition.")
            speak("Sorry, there was an error in speech recognition.")

def process_command(command_text):
    """
    Processes the command text and decides on the action to take.
    """
    # Determine the type of command and take appropriate action
    # This can be expanded or modified as needed
    execute_action(command_text)

def execute_action(action):
    """
    Executes the determined action based on the processed command.
    """
    # Implement the logic to execute actions based on the command
    # This can involve system commands, API calls, etc.
    print("Executing action: " + action)
    if action.lower().startswith("open "):
        app_name = action[5:].strip()  # Extracting the application name
        open_application(app_name)

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