import argparse
import csv
import os
from dotenv import load_dotenv  # pip3 install python-dotenv

from module.py_ya_music import open_playlist_ym_selenuim, get_tracks_from_htmlpage_yandexmusic
from module.py_spotify import Spoti, import_tracks_in_spotify_playlist


parser = argparse.ArgumentParser(description='Import tracks from Yandex Music playlist to Spotify playlist')
parser.add_argument('ym', type=str, help='Input Yandex Music playlist')
parser.add_argument('--sp_user', type=str, default='kaefik@outlook.com', help='Username Spotify')
parser.add_argument('--spotify', type=str, default='', help='Output Spotify playlist')
parser.add_argument('--debug', type=int, default='0', help='Debug flag (default: 0)')
args = parser.parse_args()
# print(args)

sp_url = args.spotify
debug = args.debug
ym = args.ym
user_spotify = args.sp_user

filename = 'playlist.html'
filename_playlist = 'my_playlist.csv'
open_playlist_ym_selenuim(ym, filename, hidden=True, debug=debug)

playlist_ym = None
with open(filename, 'r') as f:
    playlist_ym = f.read()

tracks_dict = get_tracks_from_htmlpage_yandexmusic(playlist_ym, debug=args.debug)

#  сохранение результата в файл
with open(filename_playlist, 'w') as f:
    f.write('artist%track\n')
    for key, el in tracks_dict.items():
        for song in el:
            row = f'{key}%{song}\n'
            f.write(row)
print(f'Сохранение плейлиста YandexMusic in {filename_playlist}')

if len(args.spotify) > 0:
    # TODO: сделать проверку на существование плейлиста

    print('Start import tracks to Spotify playlist.')

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    spotipy_client = os.getenv('SPOTIFY_CLIENT_ID')
    spotipy_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    filename = f'my_playlist.csv'
    outfilename = f'my_playlist_spoti.csv'

    spoti_playlist = []
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter='%')
        for row in reader:
            row['id_spoti'] = ''
            spoti_playlist.append(row)

    sp_playlist = import_tracks_in_spotify_playlist(spoti_playlist, playlist_id=sp_url, username=user_spotify,
                                                    spotipy_client=spotipy_client,
                                                    spotipy_client_secret=spotipy_client_secret)

    # запись в файл с найденными id
    fieldnames = ['artist', 'track', 'id_spoti']
    with open(outfilename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='%')
        writer.writeheader()
        for line in sp_playlist:
            print(line)
            writer.writerow(line)

    print('End import tracks to Spotify playlist.')
