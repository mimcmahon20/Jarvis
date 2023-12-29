import speech_recognition as sr
from speech_output import speak
from commands.open_application import open_application
from commands.query_command import query_command
from commands.spotify_commands import spotify_commands
from utils.command_type_util import is_open_command, is_spotify_command

_update_gui = None

def set_update_gui_function(func):
    global _update_gui
    _update_gui = func

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
    if _update_gui:
        _update_gui('thinking')
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
    else:
        query_command(action)


