import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .ai_response_generator import get_spoken_response_from_command

import sys
import os

# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Shows basic usage of the Google Calendar API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_week_events(service):
    """Fetches events for the current week from Google Calendar and speaks a summary."""
    now = datetime.datetime.utcnow()
    start_of_week = now - datetime.timedelta(days=now.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    start = start_of_week.isoformat() + 'Z'
    end = end_of_week.isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=start, 
                                          timeMax=end, singleEvents=True, 
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Prepare the response
    if not events:
        response = 'No upcoming events found.'
    else:
        response = 'You have the following events this week: '
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            response += f"{event['summary']} at {start}, "

    # Get the spoken summary from the AI model
    ai_response = get_spoken_response_from_command("calendar this week", response)

    # Speak the AI-generated response
    if ai_response:
        speak(ai_response)
    else:
        speak("I'm sorry, I couldn't process your calendar events.")

def add_event(service, summary, start_time, end_time):
    """Adds an event to Google Calendar."""
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
    except Exception as e:
        print(f"An error occurred: {e}")

def google_calendar_commands(action):
    """Executes calendar-related commands based on the action."""
    service = authenticate_google_calendar()
    # Speak "One moment..." before processing the response
    speak("One moment...")
    if "add event" in action.lower():
        summary, start_time, end_time = parse_add_event_command(action)
        if summary and start_time and end_time:
            add_event(service, summary, start_time, end_time)
    elif "calendar this week" in action.lower():
        get_week_events(service)
    else:
        print("Calendar command not recognized")

import re
from dateutil.parser import parse

def parse_add_event_command(command):
    """
    Parses the command to extract event details.
    Command format: 'Add [event description] on [date] at [time]'
    Example: 'Add a meeting with John December 28th 2023 at 6:00 p.m.'
    """
    try:
        pattern = r'add (.+) on (.+) at (.+)'
        match = re.match(pattern, command.lower())
        if not match:
            print("Invalid command format for adding event.")
            return None, None, None
        # remove first word from summary (event)
        summary = match.group(1).split(' ', 1)[1]
        date_str = match.group(2)
        time_str = match.group(3)

        # Parsing natural language date and time
        start_datetime = parse(f"{date_str} {time_str}")
        end_datetime = start_datetime + datetime.timedelta(hours=1)  # Assuming 1 hour duration

        start_time = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        end_time = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        return summary, start_time, end_time
    except Exception as e:
        print(f"Error parsing command: {e}")
        return None, None, None