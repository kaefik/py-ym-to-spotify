import os
import time
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv  # pip3 install python-dotenv

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# константы
ym_link = 'https://music.yandex.ru'


# END константы

# трек 
class Track:
    def __init__(self):
        self.song = {}
        self.author = {}


def save_to_html(filename, htmlpage):
    with open(filename, 'w') as f:
        f.write(htmlpage)


def open_html(filename):
    result = None
    with open(filename, 'r') as f:
        result = f.read()
    return result


def open_playlist_ym(urls, outfilename="my_playlist.html"):
    session = requests.Session()
    r = session.get(urls)
    print(r.status_code)

    # TODO: нужно сделать пролистывание страницы до конца чтобы все песни загрузились, а так загружается 150 шт

    if (r.status_code == 200):
        # print(r.headers)
        # print(r.content)
        # print(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')

        save_to_html(outfilename, soup.prettify())


def open_playlist_ym_selenuim(urls, outfilename="my_playlist.html", hidden=True):
    # настройки скрытого режима хрома
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    if (hidden):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # END настройки скрытого режима хрома

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./drv/chromedriver')
    driver.get(urls)

    i = 0
    elem_exit = True
    last_song_old = ""
    my_playlist = ""
    while elem_exit:
        print("Шаг ", i)
        elem_sidebar = driver.find_elements_by_css_selector('body')
        elem_sidebar[0].send_keys(Keys.PAGE_DOWN)
        # TODO: надо убрать и сделать чтобы selenium дожидался сам загрузки
        time.sleep(5)

        print("Elem SideBar = ", elem_sidebar)
        i = i + 1
        elem_playlist = driver.find_elements_by_css_selector('div.d-track.typo-track.d-track_selectable')
        print('LEN elem_playlist = ', len(elem_playlist))
        last_song = elem_playlist[-1].text
        print(last_song)
        if last_song == last_song_old:
            elem_exit = False
        else:
            last_song_old = last_song
            for el in elem_playlist:
                my_playlist = my_playlist + el.get_attribute("outerHTML")



    print("Достигли конца страницы")
    save_to_html(outfilename, my_playlist)


if __name__ == "__main__":
    urls = f"https://music.yandex.ru/users/IlnurSoft/playlists/3"
    filename = "playlist.html"
    #open_playlist_ym_selenuim(urls, filename, False)

    playlist_ym = open_html(filename)

    # print(playlist_ym)

    soup = BeautifulSoup(playlist_ym, 'html.parser')
    music = soup.select('div.d-track.typo-track.d-track_selectable')

    print(len(music))
    # music_html = music.prettify()
    # print(music_html)
    save_to_html('music.html', music[0].prettify())

    # item_music = music[0]   
    tracks = []
    for item_music in music:
        author = {}
        song = {}

        # информация о песне
        song_d = item_music.select_one('div.d-track__name')
        song['name'] = song_d['title']
        song['link'] = ym_link + song_d.a['href']
        # print(song)

        # информация об артисте
        author_d = item_music.select_one('span.d-track__artists')
        # print(author_d)
        author['name'] = author_d.a['title']
        author['link'] = ym_link + author_d.a['href']
        # print(author)

        track = {'author': author, 'song': song}
        # print(track)
        tracks.append(track)

    print(len(tracks))

