"""
 Import tracks from saving playlist to Spotify
"""

import argparse
import csv
import sys
from module.py_spotify import Spoti, import_tracks_in_spotify_playlist

parser = argparse.ArgumentParser(description='Import tracks from saving playlist to Spotify')
parser.add_argument('filename_playlist', default='my_playlist.csv', type=str, help='Input Yandex Music playlist')
parser.add_argument('sp_user', type=str, default='', help='Username Spotify')
parser.add_argument('spotify', type=str, default='', help='Output Spotify playlist')
parser.add_argument('spotipy_client', type=str, default='', help='spotipy_client')
parser.add_argument('spotipy_client_secret', type=str, default='', help='spotipy_client_secret')
parser.add_argument('--debug', type=int, default='1', help='Debug flag (default: 0)')


def main():
    args = parser.parse_args()
    # print(args)

    sp_url = args.spotify
    debug = args.debug
    user_spotify = args.sp_user
    filename_playlist = args.filename_playlist

    spotipy_client = args.spotipy_client
    spotipy_client_secret = args.spotipy_client_secret

    print('Start import tracks to Spotify playlist.')

    filename = filename_playlist
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
