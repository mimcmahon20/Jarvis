import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jarvis.commands.google_calendar_commands import google_calendar_commands

@pytest.fixture
def mock_google_calendar():
    mock_google_calendar_api = Mock()
    mock_google_calendar_api.events.return_value = {'items': [{'summary': 'Some Event'}]}
    return mock_google_calendar_api

def test_get_week_events(mock_google_calendar):
    with patch('jarvis.commands.google_calendar_commands.authenticate_google_calendar', return_value=mock_google_calendar):
        with patch('jarvis.commands.google_calendar_commands.speak') as mock_speak:
            google_calendar_commands("what's on this week")
            mock_speak.assert_called_once()

def test_get_week_events_no_events(mock_google_calendar):
    mock_google_calendar.events.return_value = {'items': []}
    with patch('jarvis.commands.google_calendar_commands.authenticate_google_calendar', return_value=mock_google_calendar):
        with patch('jarvis.commands.google_calendar_commands.speak') as mock_speak:
            google_calendar_commands("what's on this week")
            mock_speak.assert_called_once()
