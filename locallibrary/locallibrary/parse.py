from bs4 import BeautifulSoup
from urllib.request import urlopen

html_doc = urlopen('https://www.litmir.me/bs?rs=5%7C1%7C0&o=20&p=1').read()
soup = BeautifulSoup(html_doc)


def get_author(card):
    return card.find('span', itemprop='author').find_all('a')[0].get_text()


def get_title(card):
    return card.select('span', itemprop='name')[0].get_text()


def get_genre(card):
    return card.find('span', itemprop='genre').find_all('a')[0].get_text()


def get_book_summary(card):
    return card.find('div', class_='item_description').find('p').get_text()


for card in soup.find_all('table', style='max-height:750px;'):
    print(get_book_summary(card))