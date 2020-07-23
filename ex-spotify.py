import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv  # pip3 install python-dotenv


# получение данных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# print((dotenv_path))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# app_api_id = os.getenv("TLG_APP_API_ID")
# app_api_hash = os.getenv("TLG_APP_API_HASH")
# app_name = os.getenv("TLG_APP_NAME")
# bot_token = os.getenv("I_BOT_TOKEN")
# api_key = os.getenv("API_KEY")
# END получение данных окружения

"""
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
"""

my_playlist_spotify = 'spotify:playlist:5l4fHC0b4canY6pqU0s8vE'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

