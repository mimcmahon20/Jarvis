import os
import openai
from pathlib import Path
from playsound import playsound
import tempfile

def speak(text):
    """
    Converts the given text to speech using OpenAI's TTS API and plays the audio.
    """
    try:
        # Load API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("API key is not set. Please configure the OPENAI_API_KEY environment variable.")
            return

        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Create a temporary file to store the speech
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            speech_file_path = temp_file.name

        # Generate speech using OpenAI's TTS API
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=text
        )

        # Stream the response to a file
        response.stream_to_file(speech_file_path)

        # Play the generated speech
        playsound(speech_file_path)

    finally:
        # Remove the speech file
        if os.path.exists(speech_file_path):
            os.remove(speech_file_path)

