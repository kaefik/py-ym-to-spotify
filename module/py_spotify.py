import os
import csv
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Spoti:

    def __init__(self, username, spotipy_client, spotipy_client_secret):
        #  аунтификация пользователя
        scope = 'user-read-private,playlist-modify-private,playlist-modify-public'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost',
                                                            username=username, client_id=spotipy_client,
                                                            client_secret=spotipy_client_secret))
        self.user_id = self.sp.me()['id']

    # поиск песни по артисту и названию песни
    def search_artist_track(self, name_artist, name_track):
        res = dict()
        query = f'track:{name_track} artist:{name_artist}'
        results = self.sp.search(q=query)
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            res['id'] = track['id']
            res['name'] = track['name']
            res['uri'] = track['uri']
        else:
            # print(f"Трек {name_track} не найден")
            pass
        return res

    # добавить трек в плейлист
    def add_track(self, playlist_id, track):
        r = self.sp.user_playlist_add_tracks(user=self.user_id, playlist_id=playlist_id,
                                             tracks=[track])
        return r


# импорт треков в плейлист с id playlist_id пользователя username с временем задержки добавления треков
def import_tracks_in_spotify_playlist(spoti_playlist, playlist_id, username, spotipy_client,
                                      spotipy_client_secret, sec=3):
    sp = Spoti(username=username, spotipy_client=spotipy_client, spotipy_client_secret=spotipy_client_secret)
    # получение id конкретных треков
    for row in spoti_playlist:
        r = sp.search_artist_track(row['artist'], row['track'])
        row['id_spoti'] = r['id'] if not (r == {}) else ''

    # добавление песен в мой плейлист
    for track in spoti_playlist:
        if len(track['id_spoti']) > 0:
            print(f"ADD - {track['artist']} - {track['track']}")
            sp.add_track(playlist_id, track['id_spoti'])
            time.sleep(sec)
    return spoti_playlist

