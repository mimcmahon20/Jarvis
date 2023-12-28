import os
import sys
from .spotify_commands import spotify_commands
from .open_application import open_application
from .google_calendar_commands import google_calendar_commands

from openai import OpenAI
from dotenv import load_dotenv


# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

# Load environment variables from .env file
load_dotenv()

def query_command(query):
    """
    Sends the query to the OpenAI API and gets the response.
    """
    # Retrieve the API key from an environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        speak("API key is not set. Please configure the OPENAI_API_KEY environment variable.")
        return

    try:
        client = OpenAI(api_key=api_key)
        messages = create_openai_prompt(query)
        completion = client.chat.completions.create(
            model="gpt-4-0613",
            messages=messages,
        )

         # Inspect and properly access the response
        if completion.choices:
            response = completion.choices[0]
            if hasattr(response, 'message') and response.message:
                answer = response.message.content.strip()  # Accessing the content attribute
                # Check for specific commands and execute corresponding functions
                if answer.lower().startswith("open "):
                    app_name = answer[5:].strip()
                    open_application(app_name)
                elif "play " in answer.lower() or "pause" in answer.lower() or "stop" in answer.lower() or "resume" in answer.lower() or "raise spotify volume" in answer.lower() or "lower spotify volume" in answer.lower() or "play playlist " in answer.lower() or "play artist " in answer.lower():
                    spotify_commands(answer)
                elif "add event" in answer.lower() or "calendar this week" in answer.lower():
                    print("calendar event:" + answer)
                    google_calendar_commands(answer)
                else:
                    # If the response is not a recognized command, speak the response
                    print("prompted AI:" + answer)
                    speak(answer)
            else:
                speak("I received an unexpected response format from the API.")
        else:
            speak("No response was received from the API.")
    except Exception as e:
        speak(f"Sorry, there was an error processing your request: {e}")

def create_openai_prompt(query):
    system_message = (
        "I am a voice-activated assistant named Jarvis speaking to a user named Maguire. "
        "Maguire can give me specific commands, and my responses should be in the format of these commands. "
        "The command formats are: "
        "1. 'Open [application name]' to open an application. For example, 'Open Spotify'. "
        "2. 'Play', 'Pause', 'Stop', 'Resume' to control Spotify playback. "
        "3. 'Raise Spotify volume' or 'Lower Spotify volume' to adjust Spotify's volume by 20%. "
        "4. 'Play playlist [playlist name]' to play a specific Spotify playlist. For example, 'Play playlist Summer Hits'. "
        "5. 'Play artist [artist name]' to play songs from a specific artist on Spotify. For example, 'Play artist Taylor Swift'. "
        "6. 'What's on my calendar this week?' to get a summary of events for the current week from Google Calendar. "
        "7. 'Add event [event name] on [date] at [time]' to add an event to Google Calendar. For example, 'Add event Meeting with John on 2021-06-15 at 10:00'. Remember, the year is 2024 "
        "If Maguire's request matches one of these commands, I should respond with the exact command format. "
        "For example, if Maguire asks how to listen to Taylor Swift on Spotify, I should respond with 'Play artist Taylor Swift'. "
        "For general queries that don't match these commands, I should provide a clear, concise, and informative response suitable for a voice assistant. "
        "All my responses should be brief and to the point, as they are spoken aloud."
    )

    user_message = {"role": "user", "content": query}

    return [
        {"role": "system", "content": system_message},
        user_message
    ]