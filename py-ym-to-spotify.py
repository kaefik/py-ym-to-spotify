import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# трек 
# class Track:
#     def __init__(self):
#         self.song = {}
#         self.author = {}


# сохранение всех треков из плейлиста Yandex Music
def open_playlist_ym_selenuim(urls, outfilename="my_playlist.html", hidden=True, debug=False):
    # настройки скрытого режима хрома
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    if hidden:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # END настройки скрытого режима хрома

    driver = webdriver.Chrome(options=chrome_options, executable_path='./drv/chromedriver')
    driver.get(urls)

    i = 0
    elem_exit = True
    last_song_old = ""
    my_playlist = ""
    while elem_exit:
        if debug:
            print("Шаг ", i)
        elem_sidebar = driver.find_elements_by_css_selector('body')
        elem_sidebar[0].send_keys(Keys.PAGE_DOWN)
        # TODO: надо убрать и сделать чтобы selenium дожидался сам загрузки
        time.sleep(5)

        if debug:
            print("Elem SideBar = ", elem_sidebar)
        i = i + 1
        elem_playlist = driver.find_elements_by_css_selector('div.d-track.typo-track.d-track_selectable')

        last_song = elem_playlist[-1].text
        if debug:
            print(last_song)
        if last_song == last_song_old:
            elem_exit = False
        else:
            last_song_old = last_song
            for el in elem_playlist:
                my_playlist = my_playlist + el.get_attribute("outerHTML")

    if debug:
        print("Достигли конца страницы")

    with open(outfilename, 'w') as f:
        f.write(my_playlist)


# выделение информации о треках
def get_tracks_from_htmlpage_yandexmusic(playlist_ym, debug=False):
    ym_link = 'https://music.yandex.ru'
    soup = BeautifulSoup(playlist_ym, 'html.parser')
    music = soup.select('div.d-track.typo-track.d-track_selectable')

    if debug:
        with open('music.html', 'w') as f:
            f.write(music[0].prettify())

    tracks_dict = {}  # ключ - это исполнитель, значение - массив с названиями треков-песен
    for item_music in music:
        author = {}
        song = {}

        # информация о песне
        song_d = item_music.select_one('div.d-track__name')
        song['name'] = song_d['title']
        song['link'] = ym_link + song_d.a['href']

        # информация об артисте
        author_d = item_music.select_one('span.d-track__artists')
        # TODO: сделать чтобы выделялись несколько исполнителей, если они есть
        author['name'] = author_d.a['title']
        author['link'] = ym_link + author_d.a['href']
        if author['name'] in tracks_dict:
            ss = tracks_dict[author['name']]
            tracks_dict[author['name']].add(song['name'])
        else:
            tracks_dict[author['name']] = {song['name']}

    return tracks_dict


if __name__ == "__main__":
    # urls = f"https://music.yandex.ru/users/IlnurSoft/playlists/3"
    urls= "https://music.yandex.ru/users/yamusic-daily/playlists/23758179"
    filename = "playlist.html"

    open_playlist_ym_selenuim(urls, filename, hidden=True, debug=False)

    playlist_ym = None
    with open(filename, 'r') as f:
        playlist_ym = f.read()

    tracks_dict = get_tracks_from_htmlpage_yandexmusic(playlist_ym, debug=False)

    #  сохранение результата в файл
    with open("my_playlist.csv", "w") as f:
        f.write('artist%track\n')
        for key, el in tracks_dict.items():
            for song in el:
                row = f"{key}%{song}\n"
                f.write(row)
