import os
import csv
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv  # pip3 install python-dotenv


class Spoti:

    def __init__(self, username=''):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        #  аунтификация пользователя
        scope = 'user-read-private,playlist-modify-private,playlist-modify-public'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost',
                                                            username=username))
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

    def add_track(self, playlist_id, track):
        r = self.sp.user_playlist_add_tracks(user=self.user_id, playlist_id=my_playlist_id,
                                             tracks=[track])
        return r


if __name__ == '__main__':
    # плейлист куда добавлять песни
    my_playlist_id = '64AFVNsl40VrZw7l7y7Grc'
    sp = Spoti(username='kaefik@outlook.com')

    filename = 'my_playlist.csv'
    spoti_playlist = []
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter='%')
        print(reader)
        # reader = csv.reader(f)
        for row in reader:
            r = sp.search_artist_track(row['artist'], row['track'])
            if r == {}:
                row['id_spoti'] = ''
            else:
                row['id_spoti'] = r['id']
            spoti_playlist.append(row)

    # запись в файл с найденными id
    fieldnames = ['artist', 'track', 'id_spoti']
    with open('my_playlist_spoti.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='%')
        writer.writeheader()
        for line in spoti_playlist:
            print(line)
            writer.writerow(line)

    # добавление песен в мой плейлист
    for track in spoti_playlist:
        if len(track['id_spoti'])>0:
            print("ADD - ", track)
            sp.add_track(my_playlist_id, track['id_spoti'])
            time.sleep(3)
