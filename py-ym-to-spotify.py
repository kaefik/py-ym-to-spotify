
import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv  # pip3 install python-dotenv


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

# получение данных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# print((dotenv_path))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# app_api_id = os.getenv("TLG_APP_API_ID")

# END получение данных окружения


def open_playlist_ym(urls):       

    # class = d-track typo-track d-track_selectable d-track_in-lib

    session = requests.Session()    
    r = session.get(urls)
    print(r.status_code)

    # TODO: нужно сделать пролистывание страницы до конца чтобы все песни загрузились, а так загружается 150 шт

    if (r.status_code == 200):
        # print(r.headers)
        # print(r.content)
        # print(r.text)

        soup = BeautifulSoup(r.text, 'html.parser')
        
        save_to_html('page.html', soup.prettify())




if __name__ =="__main__":

    urls = f"https://music.yandex.ru/users/IlnurSoft/playlists/3"
    # open_playlist_ym(urls)


    playlist_ym = open_html('page.html')   

    # print(playlist_ym)

    soup = BeautifulSoup(playlist_ym, 'html.parser')
    # news = soup.findAll('div', class_='lightlist__cont')
    # d-track typo-track d-track_selectable d-track_in-lib d-track_selected
    #music = soup.findAll('div', class_='d-track typo-track d-track_selectable d-track_in-lib')
    music = soup.select('div.d-track.typo-track.d-track_selectable')

    print(len(music))
    #music_html = music.prettify()
    #print(music_html)
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
        #print(author_d)
        author['name'] = author_d.a['title']
        author['link'] = ym_link + author_d.a['href']
        # print(author)

        track = {'author': author, 'song': song}
        # print(track)
        tracks.append(track)

    print(len(tracks))


    
    


