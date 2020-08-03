# импорт музыки из плейлистов Яндекс Музыки в Спотифай

**Первоначальная настройка скрипта:**

1. переименовать файл *.env-example* в *.env* и прописать *client id* и *client id secret* который берёте из  https://developer.spotify.com/dashboard/login и создаете приложение (create in app): в строке **Redirect URIs** прописываете http://localhost
2. установка бибилиотек для работы скрипта: `pip install -r requirements.txt`



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

шаг 1 нельзя пропустить, только можно пропустить шаг 2.

После авторизации на Spotify будет осуществлен редирект на http://localhost с кодом авторизации - эту веб-ссылку нужно скопировать и вставить после запроса: *Enter the URL you were redirected to: Opening in existing browser session*. и нажать <Enter>

Возможные ошибки при выполнении скрипта:

* ошибка в драйвере для chrome - скачивайте под конкретную версию браузера Google Chrome и операционной системы здесь https://chromedriver.chromium.org/downloads и скопируйте в папку drv

  





