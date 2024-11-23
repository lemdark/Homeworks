import requests
from bs4 import BeautifulSoup
import re
import json

def parse_html():
    url = 'https://www.bbc.com/sport'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    news_items = soup.find_all('li', class_=re.compile('ssrcss-.{6,}-ListItem e1gp961v0'))
    results = []

    for news in news_items[:6]:
        cards = news.find_all('div', class_='ssrcss-tq7xfh-PromoContent exn3ah99')
        
        for card in cards:
            url = card.find('a').get('href')
            url = 'https://www.bbc.com' + url
            topic = card.find('div', class_='ssrcss-wdw1q-Stack e1y4nx260').find('span').text
            print(topic)
            print(url)

            results.append({'topic': topic, 'url': url})
    with open('bbc_news.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

parse_html()
