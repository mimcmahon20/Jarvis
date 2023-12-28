import speech_recognition as sr
from speech_output import speak
from commands.open_application import open_application
from commands.query_command import query_command
from commands.spotify_commands import spotify_commands
from commands.google_calendar_commands import google_calendar_commands

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
    print("Executing action: " + action)
    if is_open_command(action):
        app_name = action[5:].strip()  # Extracting the application name
        open_application(app_name)
    elif is_spotify_command(action):
        spotify_commands(action)
    elif is_calendar_command(action):
        google_calendar_commands(action)
    else:
        query_command(action)

def is_spotify_command(action): 
    if action.lower().startswith("play ") or action.lower().startswith("pause") or action.lower().startswith("stop") or action.lower().startswith("resume") or action.lower().startswith("play") or action.lower().startswith("wake up") or action.lower().startswith("raise spotify volume") or action.lower().startswith("lower spotify volume") or action.lower().startswith("play playlist ") or action.lower().startswith("play artist "):
        return True
    else:
        return False
    
def is_open_command(action): 
    if action.lower().startswith("open "):
        return True
    else:
        return False
    
def is_calendar_command(action):
    if action.lower().startswith("calendar this week"):
        return True
    else:
        return False