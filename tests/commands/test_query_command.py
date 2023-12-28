import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jarvis.commands.query_command import query_command

@pytest.fixture
def mock_openai():
    mock_openai_api = Mock()
    mock_openai_api.chat.completions.return_value = {'choices': [{'message': {'content': 'Some response'}}]}
    return mock_openai_api

def test_query_command(mock_openai):
    with patch('jarvis.commands.query_command.OpenAI', return_value=mock_openai):
        with patch('jarvis.commands.query_command.speak') as mock_speak:
            query_command("Hello")
            mock_speak.assert_called_once()

def test_query_command_no_api_key(mock_openai):
    # Mock the environment variable to simulate the API key not being set
    with patch.dict('jarvis.commands.query_command.os.environ', {'OPENAI_API_KEY': ''}):
        with patch('jarvis.commands.query_command.OpenAI', return_value=mock_openai):
            with patch('jarvis.commands.query_command.speak') as mock_speak:
                query_command("Hello")
                mock_speak.assert_called_once()
                #ensure that the speak function was called with the correct message
                assert mock_speak.call_args[0][0] == "API key is not set. Please configure the OPENAI_API_KEY environment variable."


