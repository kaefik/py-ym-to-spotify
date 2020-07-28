# запуск команды:
# python3 tst-gooey.py --ignore-gooey
import os
import csv

from gooey import Gooey, GooeyParser
from module.py_ya_music import open_playlist_ym_selenuim, get_tracks_from_htmlpage_yandexmusic
from module.py_spotify import Spoti, import_tracks_in_spotify_playlist


@Gooey(program_name='Playlist YandexMusic 2 Spotify',
       default_size=(900, 700), language='english')
def main():
    my_parser = GooeyParser()

    # добавить проверку на то что должен быть http урл
    my_parser.add_argument('ym_url', help='Enter url playlist Yandex Music',
                           type=str, default='')
    my_parser.add_argument('sp_url', help='Enter url playlist Spotify',
                           type=str, default='')
    my_parser.add_argument('user_spotify', help='Enter username spotify',
                           type=str, default='username')
    my_parser.add_argument('work', metavar='Варианты выполнения ',
                           default='playlist YandexMusic 2 File',
                           choices=['playlist YandexMusic 2 File', 'YandexMusic 2 Spotify'])
    my_parser.add_argument('-debug', metavar='Debug', action='store_true', help='')

    args = my_parser.parse_args()

    print(args)
    print(type(args))
    print(args)

    work = args.work
    debug = args.debug
    ym_url = args.ym_url
    sp_url = args.sp_url
    user_spotify = args.user_spotify

    filename = 'playlist.html'
    filename_playlist = 'my_playlist.csv'
    open_playlist_ym_selenuim(ym_url, filename, hidden=True, debug=debug)

    playlist_ym = None
    with open(filename, 'r') as f:
        playlist_ym = f.read()

    tracks_dict = get_tracks_from_htmlpage_yandexmusic(playlist_ym, debug=debug)

    #  сохранение результата в файл
    with open(filename_playlist, 'w') as f:
        f.write('artist%track\n')
        for key, el in tracks_dict.items():
            for song in el:
                row = f'{key}%{song}\n'
                f.write(row)
    print(f'Сохранение плейлиста YandexMusic in {filename_playlist}')

    if work=='YandexMusic 2 Spotify':
        # плейлист куда добавлять песни
        id = sp_url

        filename = f'my_playlist.csv'
        outfilename = f'my_playlist_spoti.csv'
        spoti_playlist = []
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter='%')
            for row in reader:
                row['id_spoti'] = ''
                spoti_playlist.append(row)

        sp_playlist = import_tracks_in_spotify_playlist(spoti_playlist,
                                                        playlist_id=id, username=user_spotify)

        # запись в файл с найденными id
        fieldnames = ['artist', 'track', 'id_spoti']
        with open(outfilename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='%')
            writer.writeheader()
            for line in sp_playlist:
                print(line)
                writer.writerow(line)

        print('End import tracks to Spotify playlist.')



if __name__ == "__main__":
    main()
