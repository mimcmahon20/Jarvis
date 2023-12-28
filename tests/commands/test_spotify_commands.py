import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jarvis.commands.spotify_commands import spotify_commands

@pytest.fixture
def mock_spotify():
    mock_spotify_api = Mock()
    mock_spotify_api.current_playback.return_value = {'item': {'name': 'Some Track'}}
    mock_spotify_api.current_user_playlists.return_value = {'items': [{'name': 'Some Playlist'}]}
    mock_spotify_api.search.return_value = {'tracks': {'items': [{'id': '123'}]}}
    mock_spotify_api.artist_top_tracks.return_value = {'tracks': [{'uri': 'spotify:track:123'}]}
    return mock_spotify_api

def test_open_spotify():
    with patch('jarvis.commands.spotify_commands.subprocess.Popen') as mock_popen:
        mock_popen.side_effect = Exception("Error opening Spotify")
        with patch('jarvis.commands.spotify_commands.speak') as mock_speak:
            mock_speak.assert_not_called()

def test_play_spotify():
    with patch('jarvis.commands.spotify_commands.authenticate_spotify') as mock_auth:
        with patch('jarvis.commands.spotify_commands.speak') as mock_speak:
            spotify_commands("play")
            mock_auth.assert_called_once()
            spotify_commands("pause")

def test_play_spotify_song_neon_moon(mock_spotify):
    with patch('jarvis.commands.spotify_commands.authenticate_spotify', return_value=mock_spotify):
        with patch('jarvis.commands.spotify_commands.speak') as mock_speak:
            spotify_commands("play neon moon")
            mock_speak.assert_not_called()

def test_play_highway_to_hell(mock_spotify):
    with patch('jarvis.commands.spotify_commands.authenticate_spotify', return_value=mock_spotify):
        with patch('jarvis.commands.spotify_commands.play_spotify_track') as mock_play_track:
            spotify_commands("wake up")
            mock_play_track.assert_called_once_with(mock_spotify, "Highway to Hell")

