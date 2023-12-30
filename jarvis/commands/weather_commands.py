import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from jarvis.components.speech_output import speak

WEATHER_API_KEY = '67d99f8b7b381d762a5c11365a4e107e'

def get_current_weather(location):
    """
    Fetches the current weather for the given location using OpenWeatherMap API.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=imperial'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        location_city = location.split(",")[0].strip()
        temperature_int = int(temp)
        temperature_decimals = int((temp - temperature_int) * 10)
        speak(f"The current weather in {location_city} is {temperature_int} point {temperature_decimals} degrees Fahrenheit with {weather_description}.")
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
