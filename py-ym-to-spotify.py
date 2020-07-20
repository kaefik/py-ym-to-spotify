"""
 Получение валютных пар через API
 см. документацию: https://www.alphavantage.co/documentation/

https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=RUB&apikey=demo

https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo

"""

import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv  # pip3 install python-dotenv



# получение данных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# print((dotenv_path))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# app_api_id = os.getenv("TLG_APP_API_ID")

# END получение данных окружения


def srab_playlist():       

    urls = f"https://music.yandex.ru/users/IlnurSoft/playlists/3"

    # class = d-track typo-track d-track_selectable d-track_in-lib

    session = requests.Session()    
    r = session.get(urls)
    print(r.status_code)

    if (r.status_code == 200):
        print(r.headers)
        # print(r.content)
        print(r.text)
        soup = BeautifulSoup(r.text, "html.parser")
        news = soup.findAll('a', class_='d-track typo-track d-track_selectable d-track_in-lib')
        # print(news)

        with open('page.html', 'w') as f:
            f.write(r.text)




if __name__ =="__main__":
    srab_playlist()