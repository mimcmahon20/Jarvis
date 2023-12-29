import pytest
from unittest.mock import patch, MagicMock
from jarvis.commands import google_gmail_commands

# Mock for speech_output.speak
@patch('jarvis.commands.google_gmail_commands.speak')
# Mock for google_authentication.authenticate_google
@patch('jarvis.commands.google_gmail_commands.authenticate_google')
def test_get_recent_emails(mock_authenticate, mock_speak):
    mock_service = MagicMock()
    mock_authenticate.return_value = mock_service

    # Mock successful response from Gmail API
    mock_service.users().messages().list().execute.return_value = {
        'messages': [{'id': '123'}, {'id': '456'}]
    }
    mock_service.users().messages().get().execute.side_effect = [
        {'payload': {'headers': [{'name': 'Subject', 'value': 'Email 1'}]}},
        {'payload': {'headers': [{'name': 'Subject', 'value': 'Email 2'}]}}
    ]

    google_gmail_commands.get_recent_emails(mock_service)
    mock_speak.assert_called()

    # Mock empty response from Gmail API
    mock_service.users().messages().list().execute.return_value = {}
    google_gmail_commands.get_recent_emails(mock_service)
    # Check if 'speak' was ever called with a string containing "no" and "email"
    found_expected_call = any("no" in args[0] and "email" in args[0] 
                              for args, _ in mock_speak.call_args_list)
    assert found_expected_call

    # Mock error case
    mock_service.users().messages().list.side_effect = Exception("API Error")
    google_gmail_commands.get_recent_emails(mock_service)
    mock_speak.assert_called_with("I'm sorry, I encountered an error while fetching your emails.")

@pytest.mark.parametrize("action, expected_call", [
    ("recent emails", "get_recent_emails"),
    ("unknown command", None)
])
@patch('jarvis.commands.google_gmail_commands.get_recent_emails')
@patch('jarvis.commands.google_gmail_commands.authenticate_google')
@patch('jarvis.commands.google_gmail_commands.speak')
def test_google_gmail_commands(mock_speak, mock_authenticate, mock_get_recent_emails, action, expected_call):
    mock_service = MagicMock()
    mock_authenticate.return_value = mock_service

    google_gmail_commands.google_gmail_commands(action)

    if expected_call == "get_recent_emails":
        mock_get_recent_emails.assert_called_once_with(mock_service)
    else:
        mock_speak.assert_called_with("One moment...")
        assert not mock_get_recent_emails.called
