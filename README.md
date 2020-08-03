# импорт музыки из плейлистов Яндекс Музыки в Спотифай

* **вариант 1.** Использование режима командной строки.

  `py-ym-to-spotify-cli.py [-h] [--sp_user SP_USER] [--spotify SPOTIFY]   [--debug DEBUG]   ym`

ym        -          Input Yandex Music playlist (Веб-ссылка на плейлист в Яндекс Музыки)

optional arguments (необязательные аргументы): 
  -h, --help         show this help message and exit (получить помощь об использовании)
  --sp_user SP_USER  Username Spotify  (пользователь Spotify)
  --spotify SPOTIFY  Output Spotify playlist (id плейлиста Spotify)
  --debug DEBUG      Debug flag (default: 0) (режим дебагинга, если 0, то выключен режим)

**шаг 1.** Экспорт треков из указанного плейлиста ym в файл my_playlist.csv

**шаг2.** Импорт треков из файла my_playlist.csv в указанный плейлист спотифай spotify пользователя sp_user

Если не --sp_user или --spotify будет не указан,  то импорт треков в Spotify будет пропущен.

шаг 1 нельзя пропустить, только шаг 2.