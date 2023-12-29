import datetime
import os
import sys
from .spotify_commands import spotify_commands
from .open_application import open_application
from .google_calendar_commands import google_calendar_commands
from .google_gmail_commands import google_gmail_commands
from .stocks_commands import stock_commands
from .weather_commands import weather_commands
from utils.command_type_util import is_open_command, is_spotify_command, is_calendar_command, is_gmail_command
import json

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
                log_interaction(query, response.message.content.strip())
                answer = response.message.content.strip()  # Accessing the content attribute
                # Check for specific commands and execute corresponding functions
                if answer.lower().startswith("open "):
                    app_name = answer[5:].strip()
                    open_application(app_name)
                elif "play " in answer.lower() or "pause" in answer.lower() or "stop" in answer.lower() or "resume" in answer.lower() or "raise spotify volume" in answer.lower() or "lower spotify volume" in answer.lower() or "play playlist " in answer.lower() or "play artist " in answer.lower():
                    spotify_commands(answer)
                elif "add event" in answer.lower() or "calendar this week" in answer.lower() or "calendar today" in answer.lower() or "calendar tomorrow" in answer.lower() or "calendar on " in answer.lower() or "find event" in answer.lower():
                    google_calendar_commands(answer)
                elif "recent emails" in answer.lower():
                    google_gmail_commands(answer)
                elif "get price of" in answer.lower():
                    print("prompted AI:" + answer)
                    stock_commands(answer)
                elif "get weather at" in answer.lower():
                    weather_commands(answer)
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
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
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
        "7. 'Add event [event name] on [date] at [time]' to add an event to Google Calendar. For example, 'Add event Meeting with John on 2021-06-15 at 10:00'."
        "8. 'calendar today' to get a summary of events for the current day from Google Calendar. "
        "9. 'calendar tomorrow' to get a summary of events for the next day from Google Calendar. "
        "10. 'calendar on [date]' to get a summary of events for a specific date from Google Calendar. For example, 'What's on my calendar on 2021-06-15?'."
        "11. 'Find event [event name]' to find an event on Google Calendar. For example, 'Find event Meeting with John'."
        "12. 'Recent emails' to get a summary of recent emails from Gmail. "
        "13. 'Get price of [stock symbol]' to get the current price of a stock. For example, 'Get price of AAPL'."
        "14. 'Get weather at [location]' to get the current weather at a location. For example, 'Get weather at Austin,TX,US'."
        "If Maguire's request matches one of these commands, I should respond with the exact command format. "
        "For example, if Maguire asks how to listen to Taylor Swift on Spotify, I should respond with 'Play artist Taylor Swift'. "
        "For general queries that don't match these commands, I should provide a clear, concise, and informative response suitable for a voice assistant. "
        "All my responses should be brief and to the point, as they are spoken aloud."
        "The current date is: " + current_date + ". "
    )

    user_message = {"role": "user", "content": query}

    return [
        {"role": "system", "content": system_message},
        user_message
    ]


def log_interaction(prompt, completion, file_path='interaction_log.json'):
    data = {"prompt": prompt, "completion": completion}
    
    try:
        with open(file_path, 'r+') as file:
            # Load existing data and update
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        # If file doesn't exist, create new file and write data
        with open(file_path, 'w') as file:
            json.dump([data], file, indent=4)
