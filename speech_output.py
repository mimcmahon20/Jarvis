import pyttsx3

def speak(text):
    """
    Converts the given text to speech.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example usage:
# speak("Hello, I am Jarvis")
