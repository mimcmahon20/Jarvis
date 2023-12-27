# You must set your OpenAI API key here
api_key = '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'

import os
import sys
from openai import OpenAI
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

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
                {"role": "system", "content": "You are a helpful assistant."},
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


# Example usage: query_command("Hello!")
