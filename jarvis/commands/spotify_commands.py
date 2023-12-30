import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyautogui
import os
import sys
import subprocess
import time
# Add the directory containing speech_output.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from jarvis.components.speech_output import speak

def authenticate_spotify():
    auth_manager = SpotifyOAuth(client_id='66af0542bb57499385d9a63583ae7232',
                                client_secret='442afe598a334d8b8d66556f89f2bb60',
                                redirect_uri='http://localhost:3000/callback',
                                scope='user-read-playback-state,user-modify-playback-state,user-read-currently-playing,user-read-playback-position,user-read-recently-played,user-top-read,playlist-read-private,playlist-read-collaborative,playlist-modify-public,playlist-modify-private')
    return spotipy.Spotify(auth_manager=auth_manager)

def spotify_commands(command):
    spotify = authenticate_spotify()
    if command.lower().startswith("play playlist "):    
        playlist_name = command[14:].strip()
        play_spotify_playlist(spotify, playlist_name)
    elif command.lower().startswith("play artist "):
        artist_name = command[12:].strip()
        play_spotify_artist(spotify, artist_name)
    elif command.lower().startswith("raise"):
        change_spotify_volume(spotify, 20)
    elif command.lower().startswith("lower"):
        change_spotify_volume(spotify, -20)
    elif command.lower().startswith("play "):
        open_spotify()  # Ensure Spotify is open
        track_name = command[5:].strip()
        play_spotify_track(spotify, track_name)
    elif command.lower().startswith("pause") or command.lower().startswith("stop") or command.lower().startswith("resume") or command.lower().startswith("play"):
        play_pause_spotify() # Pause or resume playback
    elif command.lower().startswith("wake up"):
        open_spotify()  # Ensure Spotify is open
        play_highway_to_hell(spotify)


def open_spotify():
    try:
        # Attempt to open Spotify - Adjust the path as needed
        subprocess.Popen('start spotify', shell=True)
        time.sleep(2) # Wait for Spotify to open
        play_pause_spotify() # Start playback to ensure this device is active
        play_pause_spotify() # Start playback to ensure this device is active
    except Exception as e:
        print(f"Error opening Spotify: {e}")

def play_pause_spotify():
    pyautogui.press('playpause')  # Simulates the play/pause media key

def play_spotify_track(spotify, track_name):
    try:
        # Search for the track on Spotify
        results = spotify.search(q='track:' + track_name, type='track')
        tracks = results['tracks']['items']
        if tracks:
            # Play the first track from the search results
            track_id = tracks[0]['id']
            spotify.start_playback(uris=[f'spotify:track:{track_id}'])
        else:
            print("Track not found")
            speak("Track not found")
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 404:
            print("No active Spotify device found. Please open Spotify and try again.")
            speak("No active Spotify device found. Please open Spotify and try again.")
        else:
            print(f"An error occurred: {e}")
            speak(f"An error occurred: {e}")

def play_highway_to_hell(spotify):
    # Play Highway to Hell by AC/DC
    play_spotify_track(spotify, "Highway to Hell")

def play_spotify_artist(spotify, artist_name):
    results = spotify.search(q='artist:' + artist_name, type='artist')
    artists = results['artists']['items']
    if artists:
        artist_id = artists[0]['id']
        top_tracks = spotify.artist_top_tracks(artist_id)
        track_uris = [track['uri'] for track in top_tracks['tracks']]
        if track_uris:
            spotify.start_playback(uris=track_uris)
        else:
            print(f"No top tracks found for artist: {artist_name}")
            speak(f"No top tracks found for artist: {artist_name}")
    else:
        print("Artist not found")
        speak("Artist not found")

def change_spotify_volume(spotify, volume_change):
    current_playback = spotify.current_playback()
    if current_playback and 'device' in current_playback:
        current_volume = current_playback['device']['volume_percent']
        new_volume = max(0, min(100, current_volume + volume_change))
        spotify.volume(new_volume)
    else:
        print("No active Spotify playback found")
        speak("No active Spotify playback found")

def play_spotify_playlist(spotify, playlist_name):
    playlists = spotify.current_user_playlists()
    if playlists:
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_id = playlist['id']
                spotify.start_playback(context_uri=f'spotify:playlist:{playlist_id}')

    else:
        print("Playlist not found")
        speak("Playlist not found")
