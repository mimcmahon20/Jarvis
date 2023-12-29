import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .ai_response_generator import get_spoken_response_from_command
from .google_authentication import authenticate_google_calendar

import sys
import os

# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

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


# Params: service - Google Calendar service object
#         day - 0 for today, 1 for tomorrow
def get_day_events(service, day):
    """Fetches events for a specific day from Google Calendar and speaks a summary."""
    now = datetime.datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=day)
    end_of_day = start_of_day + datetime.timedelta(days=1)
    start = start_of_day.isoformat() + 'Z'
    end = end_of_day.isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=start, 
                                            timeMax=end, singleEvents=True, 
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Prepare the response
    if not events:
        response = f'No events found for {start_of_day.strftime("%A, %B %d, %Y")}.'
    else:
        response = f'You have the following events on {start_of_day.strftime("%A, %B %d, %Y")}: '
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            response += f"{event['summary']} at {start}, "

    # Get the spoken summary from the AI model
    ai_response = get_spoken_response_from_command("calendar today", response)

    # Speak the AI-generated response
    if ai_response:
        speak(ai_response)
    else:
        speak("I'm sorry, I couldn't process your calendar events.")

def find_event(service, event_name):
    """Finds an event by name from Google Calendar then speaks the event time and date."""
    now = datetime.datetime.utcnow()
    start_of_month = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_month = start_of_month + datetime.timedelta(days=30)
    start = start_of_month.isoformat() + 'Z'
    end = end_of_month.isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=start, 
                                            timeMax=end, singleEvents=True, 
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Prepare the response
    if not events:
        response = f'No events found for the next 30 days.'
    else:
        response = f'We are looking for an event described as {event_name}. '
        response += f'Here are the events for the next 30 days: '
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            response += f"{event['summary']} on {start}, "

    # Feed events in readable string format to AI model
    ai_response = get_spoken_response_from_command(f"Find event described as {event_name} and report back the date and time if found", response)

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
        speak(f"{summary} added to your calendar.")
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
    elif "calendar today" in action.lower():
        get_day_events(service, 0)
    elif "calendar tomorrow" in action.lower():
        get_day_events(service, 1)
    elif "calendar on " in action.lower():
        date_str = action.lower().split("calendar on ")[1]
        days_from_today = get_days_from_today_from_date(date_str)
        if days_from_today:
            get_day_events(service, days_from_today)
    elif "find event" in action.lower():
        event_name = action.lower().split("find event ")[1]
        find_event(service, event_name)
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
    
#params: date_str - date string in the format YYYY-MM-DD
def get_days_from_today_from_date(date_str):
    """Returns the number of days from today from the given date string."""
    try:
        date = parse(date_str)
        today = datetime.datetime.now()
        return (date - today).days
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None
    