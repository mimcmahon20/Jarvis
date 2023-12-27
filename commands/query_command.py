import os
import sys
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
        completion = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a voice activated assistant named Jarvis speaking to a user named Maguire. You are helping Maguire with a query."},
                {"role": "user", "content": query}
            ]
        )

         # Inspect and properly access the response
        if completion.choices:
            response = completion.choices[0]
            if hasattr(response, 'message') and response.message:
                answer = response.message.content  # Accessing the content attribute
                speak(answer)
            else:
                speak("I received an unexpected response format from the API.")
        else:
            speak("No response was received from the API.")
    except Exception as e:
        speak(f"Sorry, there was an error processing your request: {e}")

