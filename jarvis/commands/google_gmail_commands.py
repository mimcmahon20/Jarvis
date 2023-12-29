import os
import datetime
import sys
from googleapiclient.discovery import build
from .google_authentication import authenticate_google_gmail
from .ai_response_generator import get_spoken_response_from_command

# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

def get_recent_emails(service, max_results=10):
    """Fetches the most recent emails from Gmail and speaks a summary."""
    try:
        # Fetch messages
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])

        # Prepare the response
        if not messages:
            response = 'No recent emails found.'
        else:
            response = 'Your most recent emails are: '
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
                headers = msg.get('payload', {}).get('headers', [])
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                response += f"{subject}, "

        # Get the spoken summary from the AI model
        ai_response = get_spoken_response_from_command("recent emails (summarize each one by saying subject line, from blank, about then one sentence summary of email.)", response)

        # Speak the AI-generated response
        if ai_response:
            speak(ai_response)
        else:
            speak("I'm sorry, I couldn't process your emails.")

    except Exception as e:
        print(f"Error fetching emails: {e}")
        speak("I'm sorry, I encountered an error while fetching your emails.")



def google_gmail_commands(action):
    """Executes Gmail-related commands based on the action."""
    service = authenticate_google_gmail()
    # Speak "One moment..." before processing the response
    speak("One moment...")

    if "recent emails" in action.lower():
        get_recent_emails(service)
    else:
        print("Gmail command not recognized")
