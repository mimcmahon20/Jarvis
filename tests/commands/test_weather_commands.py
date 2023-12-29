import pytest
from unittest.mock import patch, MagicMock
from jarvis.commands import weather_commands

# Mock for speech_output.speak
@patch('jarvis.commands.weather_commands.speak')
# Mock for requests.get
@patch('jarvis.commands.weather_commands.requests.get')
def test_get_current_weather(mock_get, mock_speak):
    mock_response = MagicMock()
    mock_get.return_value = mock_response

    # Mock successful response from OpenWeatherMap API
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'main': {'temp': 25},
        'weather': [{'description': 'clear sky'}]
    }
    weather_commands.get_current_weather('Blacksburg,US')
    mock_speak.assert_called_with("The current weather in Blacksburg,US is 25°C with clear sky.")

    # Mock no weather data case
    mock_response.json.return_value = {}
    weather_commands.get_current_weather('Blacksburg,US')
    mock_speak.assert_called_with("Could not find weather information for Blacksburg,US.")

    # Mock error case
    mock_response.status_code = 400
    weather_commands.get_current_weather('Blacksburg,US')
    mock_speak.assert_called_with("Failed to fetch weather data for Blacksburg,US.")

@pytest.mark.parametrize("command, expected_location, expected_call", [
    ("get weather at Blacksburg,US", "Blacksburg,US", "get_current_weather"),
    ("unknown command", None, None)
])
@patch('jarvis.commands.weather_commands.get_current_weather')
def test_weather_commands(mock_get_current_weather, command, expected_location, expected_call):
    weather_commands.weather_commands(command)

    if expected_call == "get_current_weather":
        mock_get_current_weather.assert_called_once_with(expected_location)
    else:
        assert not mock_get_current_weather.called
