import pyttsx3
import threading

# Global list to keep track of speech threads
active_speech_threads = []

def speak(text):
    """
    Converts the given text to speech in a non-blocking manner.
    """
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

        # Remove the thread from the active list when done
        active_speech_threads.remove(thread)

    # Create and start a new thread for the speech
    thread = threading.Thread(target=_speak)
    thread.start()
    # Add the thread to the active list
    active_speech_threads.append(thread)

def cleanup_speech_threads():
    """
    Waits for all active speech threads to complete.
    This function should be called during cleanup.
    """
    for thread in active_speech_threads:
        thread.join()