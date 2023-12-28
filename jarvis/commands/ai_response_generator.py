import os
from openai import OpenAI

def get_spoken_response_from_command(command, response):
    """
    Takes a command and its response, sends it to an AI model, 
    and gets a spoken response summary.
    """
    # Load API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("API key is not set. Please configure the OPENAI_API_KEY environment variable.")
        return None

    try:
        client = OpenAI(api_key=api_key)

        # Formulate a prompt for the AI model
        prompt = f"Summarize the following information into a brief spoken response:\nCommand: {command}\nResponse: {response}"

        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": prompt}]
        )

        # Extract and return the AI model's response
        if completion.choices:
            ai_response = completion.choices[0].message.content.strip()
            return ai_response
        else:
            print("No response was received from the AI model.")
            return None
    except Exception as e:
        print(f"Error while processing AI response: {e}")
        return None
