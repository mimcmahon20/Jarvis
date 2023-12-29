import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from speech_output import speak

WEATHER_API_KEY = '67d99f8b7b381d762a5c11365a4e107e'

def get_current_weather(location):
    """
    Fetches the current weather for the given location using OpenWeatherMap API.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        speak(f"The current weather in {location} is {temp}°C with {weather_description}.")
    else:
        speak(f"Failed to fetch weather data for {location}.")

def weather_commands(command):
    """
    Processes a command related to weather information.
    """
    command = command.lower()
    if "get weather at " in command:
        location = command.split("get weather at ")[1].strip("'")
        get_current_weather(location)
    else:
        speak("Weather command not recognized.")
