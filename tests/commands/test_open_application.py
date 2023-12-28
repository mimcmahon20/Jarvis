import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jarvis.commands.open_application import open_application

def test_open_known_application():
    with patch('jarvis.commands.open_application.subprocess.Popen') as mock_popen:
        with patch('jarvis.commands.open_application.speak') as mock_speak:
            open_application("Chrome")
            mock_popen.assert_called_with('start chrome', shell=True)
            mock_speak.assert_called_with("Opening Chrome")

def test_open_unknown_application():
    with patch('jarvis.commands.open_application.subprocess.Popen') as mock_popen:
        with patch('jarvis.commands.open_application.speak') as mock_speak:
            open_application("UnknownApp")
            mock_popen.assert_not_called()
            mock_speak.assert_called_with("Executable for UnknownApp not found.")

def test_open_application_with_path():
    with patch('jarvis.commands.open_application.subprocess.Popen') as mock_popen:
        with patch('jarvis.commands.open_application.speak') as mock_speak:
            with patch('jarvis.commands.open_application.os.path.exists', return_value=True):
                open_application("SomeApp")
                # This assertion needs to match your path logic in open_application
                expected_path = f"\"C:\\Program Files\\SomeApp\\SomeApp.exe\""
                mock_popen.assert_called_with(expected_path, shell=True)
                mock_speak.assert_called_with("Opening SomeApp")
