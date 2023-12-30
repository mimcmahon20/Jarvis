import os
import openai
from pathlib import Path
from playsound import playsound
import tempfile
import librosa
from PyQt5.QtCore import QTimer

_update_gui = None
_toggle_gui = None
conversation_signal = None

def set_conversation_signal(signal):
    global conversation_signal
    conversation_signal = signal

def set_update_gui_function(func):
    global _update_gui
    _update_gui = func

def set_toggle_gui_function(func):
    global _toggle_gui
    _toggle_gui = func

# Global variable to hold the reference to JarvisWindow
_main_window = None

def set_main_window(window):
    global _main_window
    _main_window = window

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
            voice="onyx",
            input=text
        )
        if _update_gui and _toggle_gui:
            _update_gui('talking')
        # Stream the response to a file
        response.stream_to_file(speech_file_path)
        
        if _main_window:
            # Calculate word durations
            duration_per_word, words = get_word_durations(text, speech_file_path)
            # Emit the signal to start the update process
            _main_window.start_update_signal.emit(words, duration_per_word)
        # Play the generated speech
        playsound(speech_file_path)

    finally:
        # Remove the speech file
        if os.path.exists(speech_file_path):
            os.remove(speech_file_path)
            if _update_gui and _toggle_gui:
                _update_gui('listening')
                _toggle_gui()

def get_word_durations(text, audio_file_path):
    # Load the audio file
    audio, sr = librosa.load(audio_file_path, sr=None)
    total_duration = librosa.get_duration(y=audio, sr=sr)

    words = text.split()
    words.append('\n')  
    duration_per_word = total_duration / len(words)
    return duration_per_word, words

