"""
 Save Yandex Music playlist to file
"""
import argparse
import csv
import os
import sys
from dotenv import load_dotenv  # pip3 install python-dotenv

from module.py_ya_music import open_playlist_ym_selenuim, get_tracks_from_htmlpage_yandexmusic

parser = argparse.ArgumentParser(description='Save Yandex Music playlist to file ')
parser.add_argument('ym', type=str, help='Input Yandex Music playlist')
parser.add_argument('filename_playlist', default='my_playlist.csv', type=str, help='Input Yandex Music playlist')
parser.add_argument('--debug', type=int, default='0', help='Debug flag (default: 0)')


def main():
    args = parser.parse_args()
    # print(args)

    debug = args.debug
    ym = args.ym
    filename_playlist = args.filename_playlist

    filename = 'playlist.html'
    # filename_playlist = 'my_playlist.csv'

    print(f'Start export tracks from Yandex Music playlist {ym}')
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
    print(f'Save tracks from playlist YandexMusic to {filename_playlist}')

    return 0


if __name__ == "__main__":
    sys.exit(main())
